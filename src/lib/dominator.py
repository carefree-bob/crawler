from src.lib.crawler_type import graph_t, lt_graph_t
from src.lib.graph_utils import reverse_graph
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

def get_dominance_frontier_from_nodal(graph: lt_graph_t)->graph_t:
    """Accepts a fat graph with idoms, preds and returns a graph_t
    with the dominance frontier in pre-order"""
    start, _ = next(iter(graph.items()))
    dom_frontier = {idx: set() for idx, _ in graph.items()}
    idoms = {x: node["idom"] for x, node in graph.items() if
             (node["idom"] is not None or x == start)}
    for idx, idom_idx in idoms.items():
        if idx == start or len(graph[idx]["preds"]) >= 2:  # another node may loop back to root
            for pred in graph[idx]["preds"]:
                if pred in idoms:
                    curr_idx = pred
                    while curr_idx != idom_idx:
                        dom_frontier[curr_idx].add(idx)
                        curr_idx = graph[curr_idx]["idom"]

    return {x : list(v) for x, v in dom_frontier.items()}


def get_dominance_frontier(g:graph_t, return_orig_number=True
                           )->graph_t:
    graph, pre, rev = gen_lt_graph(g)
    dom_frontier = get_dominance_frontier_from_nodal(graph)

    if return_orig_number:
        return {rev[x]: [rev[z] for z in y] for (x,y) in dom_frontier.items()}
    else:
        return dom_frontier


def get_post_dominance_frontier(g: graph_t)-> graph_t:
    z = -1
    g_z = {k:v if v else [-1] for k,v in g} | {z: []}
    g_z = reverse_graph(g_z)
    graph_z, pre, rev = lt_graph_t(g_z)
    df = get_dominance_frontier_from_nodal(graph_z)
    return {x:v for x, v in df if x != z}
