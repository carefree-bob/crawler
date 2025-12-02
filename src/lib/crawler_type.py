from __future__ import annotations

from typing import Optional, List, Dict, TypedDict
from typing import TypeAlias

graph_t: TypeAlias=dict[int, list[int]]
order_t: TypeAlias=tuple[int, ...]

# when we want to map one labelling to another
g_map_t: TypeAlias=dict[int, int]

# data structures for l-t analysis
class LTNode(TypedDict):
    pre: int
    succs: List[int]
    preds: List[int]
    parent: Optional[int]
    semi: int
    best: int
    bucket: List[int]
    idom: Optional[int]
    anc: Optional[int]


g_node_t = LTNode
lt_graph_t = Dict[int, LTNode]
