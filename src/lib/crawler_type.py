from __future__ import annotations
from enum import Enum
from typing import Optional, List, Dict, TypedDict
from typing import TypeAlias

graph_t: TypeAlias=dict[int, list[int]]

weights_t: TypeAlias=dict[int, int]

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

class Reduce(Enum):
    T1 = "T1"
    T2 = "T2"

# list[Operation, node, (anc parent,), (preds parent,), (ancestor node,), (preds node, ), weight)
hu_log_t: TypeAlias=list[tuple[Reduce, int, tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...], int]]


class T1T2Data_t(TypedDict):
    start: int
    graph: graph_t
    preds: graph_t
    weights: weights_t
    log: hu_log_t

class SplitAlias_t(TypedDict):
    duplicate: int
    original: int

split_data_t: TypeAlias=tuple[SplitAlias_t,...]