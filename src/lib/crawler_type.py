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


class ONS_Node_t(TypedDict):
    """Data structure for ONS combines dominator tree relations
       with tracking data for SCC loop detection
    """
    pre: int
    succs: list[ONS_Node_t]
    preds: list[ONS_Node_t]
    idom: int | None
    succs_dom: list[ONS_Node_t]  # successors in the dom-tree graph
    level: int # depth in dominator tree
    weight: int # split weight
    copy: ONS_Node_t # holds reference to a temporary copy of this node used in splitting
    header: ONS_Node_t # points to header node, if this is the header node, points to itself
    done: bool # used when processing through entire graph
    active: bool # used to determine whether a successor node is also an ancestor of curr node
    sp_back_data: tuple[int, int] | None # used to store back-edge data

ons_graph_t: TypeAlias=dict[int, ONS_Node_t]

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