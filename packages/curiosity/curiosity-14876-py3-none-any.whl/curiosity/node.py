from typing import Optional, Any, Dict, List


class Node:
    """
        The `Node` type used by the library is a wrapper around either a known Node Type + Key pair,
        or the equivalent Unique Identifier (UID) used in the system. Both can be usually used interchangeable,
        and one can create a new Node object as follows:

        >>> nodeA = Node.UID("MyNodeUID")
        >>> nodeB = Node.Key("MyNodeType", "MyNodeKey")

        Methods that create or change nodes will always return a Node object you can use in subsequent calls
        (such as adding edges or aliases, restricting access or deleting it).
    """

    def __init__(self, U: Optional[str] = None, K: Optional[str] = None, T: str = None):
        self.U = U
        self.K = K
        self.T = T

    @classmethod
    def UID(cls, uid: str, node_type: str) -> 'Node':
        """

        :param uid: UID of the existing Node in the system.
        :param node_type: The node type of the existing node
        :return: Node for further use by the library
        """
        return Node(uid, None, node_type)

    @classmethod
    def Key(cls, node_type: str, key: str) -> 'Node':
        """

        :param node_type: The node type of the existing or new node
        :param key: The key of the existing or new node
        :return: Node for further use by the library
        """
        return Node(None, key, node_type)


class EmittedNode(Node):
    def __init__(self, U: Optional[str], K: Optional[str], T: str, C: Dict[str, Any], E: List['Edge']):
        super().__init__(U, K, T)
        self.C: Dict[str, Any] = C
        self.E: List['Edge'] = E

    def get_field(self, field: str) -> Any:
        if self.C is dict:
            if field in self.C:
                return self.C[field]
            else:
                raise Exception(f"Field '{field}' not found in the node content - either you forgot to emit it, or the name is incorrect.")

    def edges(self) -> List['Edge']:
        return self.E
