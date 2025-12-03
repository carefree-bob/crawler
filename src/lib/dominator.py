from src.lib.crawler_type import graph_t, lt_graph_t
from src.lib.lengauer_tarjan import gen_lt_graph

def get_dominator_tree(g: graph_t)->graph_t:
    """Given a graph, return the dominator tree for the graph

    Args:
        g (graph_t): graph to transform

    Returns:
        graph_t object
    """
    graph, pre, rev = gen_lt_graph(g)
    start, _ = next(iter(g.items()))
    dom_tree = {x: [] for x in rev.values()}  # init
    for idx, node in graph.items():
        orig_idx = rev[idx]
        idom_idx = node["idom"]

        if idom_idx is not None:  # root has no idom
            orig_idom_idx = rev[idom_idx]
            if orig_idom_idx not in dom_tree:
                dom_tree[orig_idom_idx] = [orig_idx]
            else:
                dom_tree[orig_idom_idx].append(orig_idx)

    return dom_tree


def get_dominance_frontier(g:graph_t, return_orig_number=True)->graph_t:

    graph, pre, rev = gen_lt_graph(g)
    start = list(g.keys())[0]
    pre_start = pre[start]
    dom_frontier = {idx: set() for idx, _ in graph.items()}
    idoms = {x: node["idom"] for x, node in graph.items() if
             (node["idom"] is not None or x == pre_start)}
    for idx, idom_idx in idoms.items():
        if idx == pre_start or len(graph[idx]["preds"]) >= 2: # another node may loop back to root
            for pred in graph[idx]["preds"]:
                if pred in idoms:
                    curr_idx = pred
                    while curr_idx != idom_idx:
                        dom_frontier[curr_idx].add(idx)
                        curr_idx = graph[curr_idx]["idom"]

    if return_orig_number:
        return {rev[x]: [rev[z] for z in y] for (x,y) in dom_frontier.items()}
    else:
        return dom_frontier