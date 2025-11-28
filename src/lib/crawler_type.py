from __future__ import annotations
from typing import TypeAlias

graph_t: TypeAlias=dict[int, dict[int, ...]]
order_t: TypeAlias=tuple[int, ...]

# when we want to map one labelling to another instead of getting a tuple
g_map_t: TypeAlias=dict[int, int]

"""
LT Graph Node type is a dictionary of graph data:
    * "pre" -> the pre-ordering index of this node, treated as id
    * "succs" -> list of pre-indexes of graph node successors
    * "preds" -> list of all immediate predecessor graph nodes
    * "parent" -> pre-index of parent in spanning graph
    * "semi" -> pre-index of semi-dominator
    * "best" -> pre-index of best match for semi-dominator
    * "bucket" -> node bucket (list of pre-indices of other nodes) (in disjoint set union struct)
    * "idom" -> pre-index of immediate graph node dominator of the node
    * "anc" -> copy of dfs_parent we can modify for compression
"""
g_node_t: TypeAlias=dict[int, int|list[int]]



"""
map from pre-order index -> g_node
"""
lt_graph_t: TypeAlias=dict[int, g_node_t]