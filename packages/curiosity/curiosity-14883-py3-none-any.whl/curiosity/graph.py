import base64
import hashlib
import json
import mimetypes
import tempfile
import urllib
from contextlib import ContextDecorator
from pathlib import Path
from typing import Dict
from typing import List, Union, Any, Optional

import requests

from . import endpoints, Node
from .endpoints import library
from .graph_operation import GraphOperation
from .helpers import DateTimeEncoder, del_none
from .mosaik.core.languages import Language, Languages
from .query.query import Query
from .query.query_result import QueryResults


class Graph(ContextDecorator):
    """
    The Graph manages the connection to the Curiosity system and provides methods to interact with the Graph.
    To start a new session connect to Curiosity using a context manager.

    >>> with Graph.connect(url,token,connector_name) as graph:
    >>>     ...

    """

    def __init__(self, endpoint: str, token: str, connector_name: str):
        assert endpoint is not None, "Missing endpoint to server"
        assert token is not None, "Missing token"
        assert connector_name is not None, "You need to give this connector a name"

        self._endpoint: str = self._normalize_endpoint(endpoint)
        self._connector_name: str = connector_name
        self._token: str = "Bearer " + token.replace("Bearer ", "")
        self._auto_commit_every_cost: int = 100_000

        self._successful_run: bool = True

        self._operations: List[GraphOperation] = []
        self._operations_cost: int = 0

        self._toCommit_index: int = 0
        self._commited_index: int = 0

        # self._type_mapper: Dict[Type, NodeMapper] = {}

    def _normalize_endpoint(self, endpoint: str) -> str:
        if endpoint.endswith("/api/"):
            endpoint = endpoint[0:-len("/api/")]
        if endpoint.endswith("/api"):
            endpoint = endpoint[0:-len("/api")]
        if not endpoint.endswith("/"):
            return endpoint + "/"
        return endpoint

    @classmethod
    def connect(cls, endpoint: str, token: str, connector_name: str) -> 'Graph':
        """
        Connects to a given Curiosity system.

        :param endpoint:
        :param token: A `Library Token` used to authenticate the connector with your Curiosty instance.
               See `here <http://docs.curiosity.ai/en/articles/4714114-getting-started-python-data-connector>`_ on how to generate a `Library Token` for your Curiosity instance.
        :param connector_name: The display name of this connector. This is how it is shown in the configuration interface.
        :return: A graph object to interact with the Curiosity Graph.
        """
        return Graph(endpoint, token, connector_name)

    def __enter__(self) -> 'Graph':
        return self

    def close(self) -> None:
        """
        Close the connection to Curiosity
        """
        self.__exit__()

    def __exit__(self, *exc) -> None:
        if len(self._operations) > 0:
            self._commit_operations()

    def _commit_operations(self) -> None:
        try:
            self._post_message(endpoints.library.start_connector__full, query_params={"name": self._connector_name})
            self._post_message(endpoints.library.commit__full, self._operations)
            self._post_message(endpoints.library.finish_connector__full, query_params={"name": self._connector_name, "success": self._successful_run})
            self._operations.clear()
            self._operations_cost = 0

        except Exception as e:
            # todo log
            raise e

    def commit_pending(self) -> None:
        """
        Commits all not yet committed graph operations.
        """
        if any(self._operations):
            self._commit_operations()

    def _post_message(self, endpoint: str, content: Union[Dict, List[Dict], None] = None, *, query_params: Dict[str, str] = None, headers: Dict[str, str] = None) -> Union[str, Dict]:
        endpoint = self._endpoint + endpoint
        if isinstance(query_params, dict):
            endpoint = endpoint + "?" + urllib.parse.urlencode(query_params)

        # if isinstance(content, types.GeneratorType):
        #     response = requests.post(self._endpoint + endpoint, data=(json.dumps(e, cls=DateTimeEncoder).encode() for e in content), headers={"Authorization": self._token})
        # else:
        if isinstance(headers, dict):
            headers.update({"Authorization": self._token})
        else:
            headers = {"Authorization": self._token}

        response = requests.post(endpoint, data=json.dumps(del_none(content), cls=DateTimeEncoder), headers=headers)

        if response.status_code == requests.codes.ok:
            lib_resp = response.json()
            if not lib_resp['Success']:
                raise Exception(lib_resp['Message'])
            if lib_resp['Payload'] is None or lib_resp['Payload'] == "":
                return ""
            elif isinstance(lib_resp['Payload'], str) or isinstance(lib_resp['Payload'], dict) or isinstance(lib_resp['Payload'], list):
                return lib_resp['Payload']
            else:
                raise Exception(f"Unknown reponse payload {lib_resp['Payload']}")
        else:
            raise Exception(f"Received response: {response}")

    def _add_operation(self, operation: GraphOperation, operation2: Optional[GraphOperation] = None) -> None:
        self._operations.append(operation)
        if isinstance(operation2, GraphOperation):
            self._operations.append(operation2)
        self._operations_cost += operation.cost()
        if isinstance(operation2, GraphOperation):
            self._operations_cost += operation2.cost()
        self._check_commit()

    def set_auto_commit_cost(self, every_nodes: int, every_edges=0) -> 'Graph':
        """

        :param every_nodes:
        :param every_edges:
        :return:
        """
        self._auto_commit_every_cost = max(0, max(every_nodes * 1000, every_edges))
        return self

    def _check_commit(self, force: bool = False) -> None:
        if self._operations_cost > self._auto_commit_every_cost or force:
            if any(self._operations):
                self._commit_operations()

    def create_edge_schema(self, edges: List[str]) -> None:
        """
        **Not Implemented**

        :param edges:
        :return:
        """
        # for edge in edges:
        #     self.post_message(endpoints.library.edge_schema__full + "?" + urllib.parse.urlencode({'edge': edge}), {})
        raise NotImplementedError

    def create_node_schema(self) -> None:
        """
        **Not Implemented**

        :return:
        """
        raise NotImplementedError

    def add_or_update_by_key(self, node_type: str, key: str, content: Dict[str, Any]) -> Node:
        """
        If a node with the given node type and key does not exist in the system, creates it with the given content.
        If the node does exist, updates the content of the node.

        The given node type is expected to exist in the system already. See :py:meth:`create_node_schema` how to create a node schema.

        Args:
            node_type: Node type of the node to create or update
            key: Unique key of this node for this node type
            content: Content dictionary that follows the schema of this node type. See :py:meth:`create_node_schema` how to create a node schema.

        Returns:
             A reference to the added or updated node in the system.

        """

        n = Node.Key(node_type, key)
        self._add_operation(GraphOperation.Node(n, content, GraphOperation.add_or_update_node))
        return n

    def add_or_update(self, node: Node, content: Dict[str, Any]) -> Node:
        """
        If the given node does not exist in the system, creates it with the given content.
        If the node does exist, updates the content of the node.

        The given node type is expected to exist in the system already. See :py:meth:`create_node_schema` how to create a node schema.

        Args:
            node: Unique node reference :py:class:`Node`
            content: Content dictionary that follows the schema of this node type.

        Returns:
            A reference to the added or updated node in the system.

        """

        self._add_operation(GraphOperation.Node(node, content, GraphOperation.add_or_update_node))
        return node

    def try_add_by_key(self, node_type: str, key: str, content: Dict[str, Any]) -> Node:
        """
        Only creates a node if no node with the given node type and key exists.

        The given node type is expected to exist in the system already. See :py:meth:`create_node_schema` how to create a node schema.

        Args:
            node_type: Node type of the node to create or update
            key: Unique key of this node for this node type
            content: Content dictionary that follows the schema of this node type. See :py:meth:`create_node_schema` how to create a node schema.

        Returns:
            Created node reference object of the given node type and key.

        """
        n = Node.Key(node_type, key)
        self._add_operation(GraphOperation.Node(n, content, GraphOperation.try_add_node))
        return n

    def try_add(self, node: Node, content: Dict[str, Any]) -> Node:
        """
        Only creates a node if the node does not yet exist in the system.

        The given node type is expected to exist in the system already. See :py:meth:`create_node_schema` how to create a node schema.

        Args:
            node: Unique node reference
            content: Content dictionary that follows the schema of this node type.

        Returns:
            The reference of the given node.

        """
        self._add_operation(GraphOperation.Node(node, content, GraphOperation.try_add_node))
        return node

    def update_by_key(self, node_type: str, key: str, content: Dict[str, Any]) -> Node:
        """
        Updates the content of an existing node in the system.

        Args:
            node_type: Node type of the existing node
            key: Unique key of this node type of the existing node
            content: The content the node content is set to

        Returns:
            A Node reference of the node that is updated.
        """

        n = Node.Key(node_type, key)
        self._add_operation(GraphOperation.Node(n, content, GraphOperation.update_node))
        return n

    def update(self, node: Node, content: Dict[str, Any]) -> Node:
        """
        Updates the content of an existing node in the system.

        Args:
            node: Node reference to the existing node
            content: The content the node content is set to

        Returns:
            A Node reference of the node that is updated.
        """
        self._add_operation(GraphOperation.Node(node, content, GraphOperation.update_node))
        return node

    def delete_by_key(self, node_type: str, key: str) -> None:
        """
        Deletes a node in the system based on a given node type and key.

        Args:
            node_type: Node type of the existing node
            key: Unique key of this node type of the existing node

        """
        n = Node.Key(node_type, key)
        self._add_operation(GraphOperation.Node(n, None, GraphOperation.delete_node))

    def delete(self, node: Node) -> None:
        """
        Deletes a node of the given node reference in the system.

        Args:
            node: Node reference to the existing node

        """
        self._add_operation(GraphOperation.Node(node, None, GraphOperation.delete_node))

    def link(self, from_node: Node, to_node: Node, edge_type: str, unique: bool = True) -> None:
        """
        Adds an edge from the node from_node ot the node to_node

        Examples:
            This creates the single edge ``John`` -> ``BrotherOf`` -> ``Anna``

            >>> graph.link(john, anna, "BrotherOf")

        Notes:
            It is important to not mix the usage of unique for a given edge type, as it is only enforced when adding the new edge.  In most scenarios, you would like to use the default unique edges option.

        Args:
            from_node: The source node of the edge
            to_node: The target node of the edge
            edge_type: The type of the edge that is created
            unique: ``True`` if it should be checked that only a single unqiue edge between these exact given nodes should be created. If set to ``False`` multiple edges of this type between these exact nodes can be created.
        """
        self._add_operation(GraphOperation.Edge(from_node, to_node, edge_type, GraphOperation.add_unique_edge if unique else GraphOperation.add_edge))

    def link_bidirect(self, a: Node, b: Node, edge_type_a_to_b: str, edge_type_b_to_a: str, unique: bool = True) -> None:
        """
        Adds an edge from the node ``a`` ot the node ``b`` of the type ``edge_type_a_to_b`` and an edge of the type ``edge_type_b_to_a`` in reverse.
        Edges are usually unique (i.e. uniquely identified by the relationship From + To + Edge Type). If you would like to add non-unique edges, add ``unique = False`` to the call.

        Examples:
            This creates both ``John`` -> ``BrotherOf`` -> ``Anna`` and ``Anna`` -> ``SisterOf`` -> ``John``

            >>> graph.link(john, anna, "BrotherOf", "SisterOf")

        Notes:
            It is important to not mix the usage of unique for a given edge type, as it is only enforced when adding the new edge.  In most scenarios, you would like to use the default unique edges option.

        References:

        See Also:

        Args:
            a:
            b:
            edge_type_a_to_b:
            edge_type_b_to_a:
            unique: ``True`` if it should be checked that only a single unqiue edge between these exact given nodes should be created in each direction. If set to ``False`` multiple edges of this type between these exact nodes can be created.

        Returns:

        """

        self._add_operation(GraphOperation.Edge(a, b, edge_type_a_to_b, GraphOperation.add_unique_edge if unique else GraphOperation.add_edge),
                            GraphOperation.Edge(b, a, edge_type_b_to_a, GraphOperation.add_unique_edge if unique else GraphOperation.add_edge))

    def unlink(self, from_node: Node, to_node: Node, edge_type: str, unique: bool = True) -> None:
        """



        Args:
            from_node:
            to_node:
            edge_type:
            unique: TODO what does this mean here

        Returns:

        """

        self._add_operation(GraphOperation.Edge(from_node, to_node, edge_type, GraphOperation.remove_unique_edge if unique else GraphOperation.remove_all_edges_to))

    def unlink_bidirect(self, a: Node, b: Node, edge_type_a_to_b: str, edge_type_b_to_a: str, unique: bool = True) -> None:
        """

        Args:
            a:
            b:
            edge_type_a_to_b:
            edge_type_b_to_a:
            unique: TODO what does this mean here

        Returns:

        """
        self._add_operation(GraphOperation.Edge(a, b, edge_type_a_to_b, GraphOperation.remove_unique_edge if unique else GraphOperation.remove_all_edges_to),
                            GraphOperation.Edge(b, a, edge_type_b_to_a, GraphOperation.remove_unique_edge if unique else GraphOperation.remove_all_edges_to))

    def add_alias(self, from_node: Node, language: Language, alias: str, ignore_case: bool) -> None:
        """
        Aliases are used for the linking of entities captured by the NLP pipelines to nodes in the graph. They provide a way of adding "nicknames" for your nodes, so that they can multiple forms of referring to them in text are linked correctly in the graph.

        Examples:

            >>> graph.add_alias(john, Language.Any, "Mr. John Doe", ignore_case: False)
            >>> graph.add_alias(john, Language.Any, "Johnny Doe", ignore_case: False)

        Args:
            from_node:
            language:
            alias:
            ignore_case:

        """
        self._add_operation(GraphOperation.Edge(from_node, Node.Key(Languages.enum_to_code(language), alias.strip()), "ig" if ignore_case else "cs", GraphOperation.add_alias))

    def clear_alias(self, from_node: Node) -> None:
        """
        Deletes any previous existing aliases for the given node.

        Examples:
            To remove all existing aliases before adding new ones (for example if your aliases definition changed), use the ClearAliases method first:


            >>> graph.clear_alias(john)
            >>> graph.add_alias(john, Language.Any, "Johnny Doe", ignoreCase: False)

        Notes:
            You shouldn't always clear and add new aliases, as this will result in the NLP models continuously being recreated due to changes in the graph. Use ClearAliases only in the case where you really need to delete all previous existing aliases, and then remove the call afterwards.

        Args:
            from_node:
        """
        self._add_operation(GraphOperation.Node(from_node, None, GraphOperation.clear_aliases))

    def create_user(self, user_name: str, email: str, first_name: str, last_name: str) -> Node:
        """

        Args:
            user_name:
            email:
            first_name:
            last_name:

        Returns:

        """
        user_payload = self._post_message(endpoints.library.create_user__full, query_params={ 'userName' : user_name, 'email': email, 'firstName': first_name, 'lastName': last_name})
        return Node.UID(user_payload.strip("\""), "_User")

    def create_team(self, team_name: str, description: str = None) -> Node:
        """

        Args:
            team_name:
            description:

        Returns:

        """
        user_payload = self._post_message(endpoints.library.create_team__full, query_params={'teamName': team_name, 'description': description})
        return Node.UID(user_payload.strip("\""), "_AccessGroup")

    def upload_file_by_path(self, file_path: str, filename: str, source_name: str, owner_user_or_group: Node = None) -> Node:
        """

        Args:
            file_path:
            filename:
            source_name:
            owner_user_or_group:

        Returns:

        """
        with open(file_path, "rb") as f:
            self.upload_file(f, filename, source_name, owner_user_or_group)

    def upload_file(self, file, filename: str, source_name: str, owner_user_or_group: Node = None) -> Node:
        """
        Uploads a file to the system.


        Examples:
            >>> with open("sample.pdf", "rb") as f:
            >>>    file_node = graph.upload_file(f, "sample.pdf", "Samples")

        See Also:
            :py:meth:`upload_file_by_path`

        Args:
            file: Byte stream of a file to upload to the system
            filename: Name of the file in the system
            source_name: Descriptive name TODO source ref
            owner_user_or_group: If now user or group is provided, the file is considered *Public* and therfore accessible by all users of the system. User or group that owns the file. Owners of files can find files and view them. A file can have multiple owners. TODO auth ref

        Returns:
            A reference node of the file. E.g. used for linking entities to files.

        """
        if Path(filename).name.startswith("~$"):
            raise Exception("Don't upload temporary MS Office files")

        file_hash_payload = self._post_message(endpoints.library.file_hash__full, query_params={"filename": filename, "source": source_name})

        file_resp = json.loads(file_hash_payload)

        if file_resp['Exists']:
            if not file.seekable():  # todo enable
                tmp_stream = tempfile.TemporaryFile(mode="w+b", delete=True, buffering=4096)
                tmp_stream.write(file.read())
                tmp_stream.flush()
                file.close()
                file = tmp_stream

            file.seek(0)
            bytes = file.read()  # read entire file as bytes
            hash = hashlib.sha256(bytes).digest()
            current_hash = base64.b64encode(hash)
            file.seek(0)
            if file_resp['Hash'].encode() == current_hash:
                return Node.UID(file_resp['UID'], "_FileEntry")

        query_params = {"filename": filename, "source": source_name}
        if owner_user_or_group is not None:
            query_params["ownerUID"] = owner_user_or_group.U

        endpoint = self._endpoint + endpoints.library.upload_file__full
        if isinstance(query_params, dict):
            endpoint = endpoint + "?" + urllib.parse.urlencode(query_params)

        headers = {"Authorization": self._token}

        type, encoding = mimetypes.guess_type(filename)

        response = requests.post(endpoint, data={}, files={"file": (filename, file, type)}, headers=headers)

        if response.status_code == requests.codes.ok:
            lib_resp = response.json()
            if not lib_resp['Success']:
                raise Exception(lib_resp['Message'])
            file_payload = lib_resp['Payload'] if isinstance(lib_resp['Payload'], str) else ""
        else:
            raise Exception(f"Received response: {response}")

        return Node.UID(file_payload.strip('"'), "_FileEntry")

    def delete_file(self, filename: str, source_name: str, owner_user_or_group: Node = None) -> None:
        """
        Removes the file from the system


        Args:
            filename:
            source_name:
            owner_user_or_group:

        Returns:

        """
        query_params = {"filename": filename, "source": source_name}
        if owner_user_or_group is not None:
            query_params["ownerUID"] = owner_user_or_group.U

        self._post_message(endpoints.library.delete_file__full, query_params=query_params)

    def delete_folder(self, path: str, source_name: str, owner_user_or_group: Node = None) -> None:
        """

        Args:
            path:
            source_name:
            owner_user_or_group:

        Returns:

        """
        query_params = {"path": path, "source": source_name}
        if owner_user_or_group is not None:
            query_params["ownerUID"] = owner_user_or_group.U

        self._post_message(endpoints.library.delete_folder__full, query_params=query_params)

    def mark_file_as_private(self, file_node: Node) -> None:
        """
            Removes the ``PublicAccessGroup`` from the file.

        Warnings:
            Files without a owners are *public*! If the file has no other owners it will *stay public*. Add a call to
            :py:meth:`restrict_access_to_team` or :py:meth:`restrict_access_to_user` to make the file private to that user or group.

            TODO ref access management

        Args:
            file_node:

        """
        file_node.T = "_FileEntry"
        public_node = Node.UID("PUBL1CaccesSgr8up11111", "_AccessGroup")
        self._add_operation(GraphOperation.Edge(file_node, public_node, "_OwnedBy", GraphOperation.remove_unique_edge))

    def add_user_to_team(self, user_node: Node, team_node: Node) -> None:
        """
        Adds the user to the team. The user will then have the same access rights to files and nodes as the team.
        A user can have both, direct access to a node and access via a team.

        See Also:
            To remove the access rights that are given to the user by the team, call :py:meth:`remove_user_from_team`. This will remove the access from the user of the nodes the team has access to.

        Args:
            user_node:
            team_node:

        """
        user_node.T = "_User"
        team_node.T = "_AccessGroup"
        self._add_operation(GraphOperation.Edge(user_node, team_node, "_MemberOf", GraphOperation.add_unique_edge),
                            GraphOperation.Edge(team_node, user_node, "_HasMember", GraphOperation.add_unique_edge))

    def remove_user_from_team(self, user_node: Node, team_node: Node) -> None:
        """
        Removes the user from the team. A user can have both, direct access to a node and access via a team. This will only remove the access via the team.

        See Also:
            To add a user to a team, see :py:meth:`add_user_to_team`.

        Args:
            user_node:
            team_node:
        """
        user_node.T = "_User"
        team_node.T = "_AccessGroup"
        self._add_operation(GraphOperation.Edge(user_node, team_node, "_MemberOf", GraphOperation.remove_unique_edge),
                            GraphOperation.Edge(team_node, user_node, "_HasMember", GraphOperation.remove_unique_edge))

    def restrict_access_to_team(self, node: Node, team_node: Node) -> None:
        """
        Adds access of the team to a node. Each member of the team can then access the node.

        Args:
            node:
            team_node:
        """
        team_node.T = "_AccessGroup"
        self._add_operation(GraphOperation.Edge(node, team_node, "_OwnedBy", GraphOperation.add_unique_edge),
                            GraphOperation.Edge(team_node, node, "_Owns", GraphOperation.add_unique_edge))

    def restrict_access_to_user(self, node: Node, user_node: Node) -> None:
        """
        Adds access to a node to the user.

        Args:
            node:
            user_node:

        Returns:

        """
        user_node.T = "_User"
        self._add_operation(GraphOperation.Edge(node, user_node, "_OwnedBy", GraphOperation.add_unique_edge),
                            GraphOperation.Edge(user_node, node, "_Owns", GraphOperation.add_unique_edge))

    def log(self, message: str) -> None:
        """
        Log a message to the system to show it on the admin ui.

        Args:
            message: Error message to log
        """
        self._post_message(endpoints.library.message_from_connector__full, query_params={"name": self._connector_name, "message": "[INFO] " + message})

    def log_error(self, message: str) -> None:
        """
        Log a **error** message to the system to show it on the admin ui.

        Args:
            message: Text message to log
        """
        self._post_message(endpoints.library.message_from_connector__full, query_params={"name": self._connector_name, "isError": True, "message": "[FAIL] " + message})

    def add_embeddings_to_index_async(self, index_uid: str, vectors: Dict[Node, List[float]], batch_size: int = 1_000) -> None:
        """

        Args:
            index_uid:
            vectors:
            batch_size:

        Returns:

        """
        raise NotImplementedError("test and finish impl")
        # for batch in chunks(vectors, batch_size):
        #     self._post_message(endpoints.library.add_embeddings_to_index__full, json.dumps(batch), query_params={"indexUID": index_uid})

    def query(self, query: Query) -> QueryResults:
        """

        Args:
            query:

        Returns:

        """
        result = self._post_message(endpoints.library.query__full, query.query)
        return QueryResults(result["R"] if "R" in result else None, result["C"] if "C" in result else None, result["MS"] if "MS" in result else -1)
