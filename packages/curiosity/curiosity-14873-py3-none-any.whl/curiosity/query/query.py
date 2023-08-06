from typing import Union, List

from .. import Node


class Query:
    def __init__(self):
        self.query = []

    def start_at(self, n: Union[str, Node, List[Node]]) -> 'Query':
        """

        Query all nodes of a given node type, a specific node or a list of nodes.
        This sets the initial set of elements in the current querie. The qu
        These queries
        :param n:
        :return:
        """

        if isinstance(n, str):
            self.query.append({"op": "StartAt", "args": {"nodeType": n}})
        elif isinstance(n, Node):
            self.query.append({"op": "StartAt", "args": {"node": n}})
        elif isinstance(n, list):
            self.query.append({"op": "StartAt", "args": {"nodes": n}})
        else:
            raise ValueError(f"Can't StartAt for type {type(n)}")
        return self

    def out(self, n: Union[str, Node, List[Node]], e: Union[str, List[str]] = None) -> 'Query':
        current_out = {}

        if isinstance(n, str):
            current_out = {"nodeType": n}
        elif isinstance(n, Node):
            current_out = {"node": n}
        elif isinstance(n, list):
            current_out = {"nodes": n}
        else:
            raise ValueError(f"Can't out for type {type(n)}")

        if e is not None:
            if isinstance(e, str):
                current_out.update({"edgeType": e})
            elif isinstance(e, list):
                current_out.update({"edgeTypes": e})
            else:
                raise ValueError(f"Can't out for type {type(n)}")
        self.query.append({"op": "Out", "args": current_out})
        return self

    def out_many(self, levels: int, node_types: List[str], edge_types: List[str], distinct: bool = True) -> 'Query':
        self.query.append({"op": "OutMany", "args": {"levels": levels, "nodeTypes": node_types, "edgeTypes": edge_types, "distinct": distinct}})
        return self

    def similar(self, index: str, count: int, tolerance: float) -> 'Query':
        self.query.append({"op": "Similar", "args": {"index": index, "count": count, "tolerance": tolerance}})
        return self

    def skip(self, count: int) -> 'Query':
        self.query.append({"op": "Skip", "args": {"count": count}})
        return self

    def take(self, count: int) -> 'Query':
        self.query.append({"op": "Take", "args": {"count": count}})
        return self

    def emit(self, emit_key: str, fields: List[str] = None) -> 'Query':
        current_emit = {"emitKey": emit_key}
        if fields is not None:
            {"emitKey": emit_key}.update({"fields": fields})
        self.query.append({"op": "Emit", "args": current_emit})
        return self

    def emit_count(self, emit_key: str) -> 'Query':
        self.query.append({"op": "EmitCount", "args": {"emitKey": emit_key}})
        return self

    def emit_with_edges(self, emit_key: str, fields: List[str] = None) -> 'Query':
        current_emit_with_edges = {"emitKey": emit_key}
        if fields is not None:
            current_emit_with_edges.update({"fields", fields})
        self.query.append({"op": "EmitWithEdges", "args": current_emit_with_edges})
        return self

    def of_type(self, node_type: str) -> 'Query':
        self.query.append({"op": "OfType", "args": {"nodeType": node_type}})
        return self

    def of_types(self, node_types: str) -> 'Query':
        self.query.append({"op": "OfTypes", "args": {"nodeTypes": node_types}})
        return self

    def except_type(self, node_type: str) -> 'Query':
        self.query.append({"op": "ExceptType", "args": {"nodeType": node_type}})
        return self

    def except_types(self, node_types: List[str]) -> 'Query':
        self.query.append({"op": "ExceptTypes", "args": {"nodeTypes": node_types}})
        return self

    def is_related_to(self, n: Union[str, List[str], Node, List[Node]], assume_bidirectional_edges: bool = True) -> 'Query':
        if isinstance(n, Node):
            self.query.append({"op": "IsRelatedTo", "args": {"node": n, "assumeBidirectionalEdges": assume_bidirectional_edges}})
        elif isinstance(n, str):
            self.query.append({"op": "IsRelatedTo", "args": {"nodeType": n}})
        elif isinstance(n, list):
            if isinstance(n[0], str):
                self.query.append({"op": "IsRelatedTo", "args": {"nodeTypes": n}})
            elif isinstance(n[0], Node):
                self.query.append({"op": "IsRelatedTo", "args": {"nodes": n, "assumeBidirectionalEdges": assume_bidirectional_edges}})
            else:
                raise ValueError
        else:
            raise ValueError
        return self

    def is_not_related_to(self, n: Union[str, List[str], Node, List[Node]], assume_bidirectional_edges: bool = True) -> 'Query':
        if isinstance(n, Node):
            self.query.append({"op": "IsNotRelatedTo", "args": {"node": n, "assumeBidirectionalEdges": assume_bidirectional_edges}})
        elif isinstance(n, str):
            self.query.append({"op": "IsNotRelatedTo", "args": {"nodeType": n}})
        elif isinstance(n, list):
            if isinstance(n[0], str):
                self.query.append({"op": "IsNotRelatedTo", "args": {"nodeTypes": n}})
            elif isinstance(n[0], Node):
                self.query.append({"op": "IsNotRelatedTo", "args": {"nodes": n, "assumeBidirectionalEdges": assume_bidirectional_edges}})
            else:
                raise ValueError
        else:
            raise ValueError
        return self

    def sort_by_timestamp(self, oldest_first: bool = True) -> 'Query':
        self.query.append({"op": "SortByTimestamp", "args": {"oldestFirst": oldest_first}})
        return self

    def sort_by_connectivity(self, most_connected_first: bool = True) -> 'Query':
        self.query.append({"op": "SortByConnectivity", "args": {"mostConnectedFirst": most_connected_first}})
        return self
