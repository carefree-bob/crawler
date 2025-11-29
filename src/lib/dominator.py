from crawler_type import graph_t, lt_graph_t
from lt_dominator import gen_lt_graph

def get_dominator_tree(g: graph_t)->graph_t:
    graph, pre, rev = gen_lt_graph(g)
    dom_tree = {}
    for pre_idx in graph:
        if rev[graph[pre_idx]["idom"]] not in dom_tree:
            dom_tree[rev[graph[pre_idx]["idom"]]] = rev[graph[pre_idx]]
        else:
            dom_tree[rev[graph[pre_idx]["idom"]]].append() = rev[graph[pre_idx]]
        dom_tree[rev[node["pre"]]] = node["idom"]