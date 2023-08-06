from typing import Any, Optional, Dict

from . import Node


class GraphOperation:
    def __init__(self, *, S: Optional[Node] = None, T: Optional[Node] = None, E: Optional[str] = None, C: Optional[Dict[str, Any]] = None, F: int = None):
        self.S = S
        self.T = T
        self.E = E
        self.C = C
        self.F = F

    @classmethod
    def Node(cls, node: Node, content: Dict[str, Any], flag: int) -> 'GraphOperation':
        return GraphOperation(S=node, C=content, F=flag)

    @classmethod
    def Edge(cls, from_node: Node, to_node: Node, edge_type: str, flag: int) -> 'GraphOperation':
        return GraphOperation(S=from_node, T=to_node, E=edge_type, F=flag)

    add_or_update_node = 0b000000000001
    try_add_node = 0b000000000010
    update_node = 0b000000000100
    delete_node = 0b000000001000
    add_edge = 0b000000010000
    add_unique_edge = 0b000000100000
    remove_all_edges_to = 0b000001000000
    remove_unique_edge = 0b000010000000
    add_alias = 0b000100000000
    clear_aliases = 0b001000000000

    flag_costs = {
        add_or_update_node:  1000,
        try_add_node:        1000,
        update_node:         1000,
        delete_node:         1,
        add_edge:            1,
        add_unique_edge:     1,
        remove_all_edges_to: 1,
        remove_unique_edge:  1,
        add_alias:           5,
        clear_aliases:       1,
    }

    def cost(self) -> int:
        if self.F in GraphOperation.flag_costs:
            return GraphOperation.flag_costs[self.F]
        else:
            return 1000
