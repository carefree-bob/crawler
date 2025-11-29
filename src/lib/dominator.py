from crawler_type import graph_t, lt_graph_t
from lt_dominator import gen_lt_graph

def get_dominator_tree(g: graph_t)->graph_t:
    """Given a graph, return the dominator tree for the graph

    Args:
        g (graph_t): graph to transform

    Returns:
        graph_t object
    """
    graph, pre, rev = gen_lt_graph(g)
    dom_tree = {}
    for idx, _ in graph.items():
        idom_idx = graph[idx]["idom"]
        if idom_idx != idx:
            if rev[idom_idx] not in dom_tree:
                dom_tree[rev[idom_idx]] = [rev[idx]]
            else:
                dom_tree[rev[idom_idx]].append(idx)

    return dom_tree
