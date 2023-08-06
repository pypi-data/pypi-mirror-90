from .node import Node


class Edge:
    def __init__(self, N: str, U: str, T: str):
        self._N = N
        self._U = U
        self._T = T

    def to(self) -> Node:
        return Node.UID(self._U, self._N)

    def edge_type(self) -> str:
        return self._T
