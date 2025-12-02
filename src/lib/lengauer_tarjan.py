from src.lib.crawler_type import graph_t, lt_graph_t, g_map_t, g_node_t

"""
Uses the 'simple' link-eval without tree rebalancing. 

"""

"""
Fake enums, to help with typos
"""
PRE = "pre" # pre-order ordering index (int, never empty)
SUCCS = "succs" # successors of node (list, [] if empty)
PREDS = "preds"  # predecessors of node (include those not in DFS) (list, [] only for root)
PARENT = "parent" # unique DFS parent (int, None only for root)
SEMI = "semi" # semi-dominator candidate (int, never empty)
BEST = "best" # smallest semi value (int, never null)
BUCKET = "bucket" # container (list, [] if empty)
IDOM = "idom" # immediate dominator (int, None if empty)
ANC = "anc" # link to forest DSU for this node (int, None if empty)


def init_lt(graph: graph_t) -> tuple[lt_graph_t, g_map_t, g_map_t]:
    """Perform DFS pre-order to generate graph with g_node_t and produce mappings
    Args:
        graph (graph_t): array graph

    Returns:
        lt_graph (fat dictionary). All entries in lt_graph are in pre-order index
        pre_map (g_map_t) map from list index to pre-order index
        rev_map (g_map_t) reverse of pre_map, taking pre-order to list index
    """

    start, _ = next(iter(graph.items()))
    stack = [start]
    visited = []
    pred_map = {g:set() for g, _ in graph.items()}  # track predecessors
    dfs_parent = {start: None}

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            for child in reversed(graph.get(node, [])):
                pred_map[child].add(node)
                if child not in visited:
                    dfs_parent[child] = node
                    stack.append(child)

    pre = {node: i for i, node in enumerate(visited)}

    # Rev: pre-order Index -> list Index
    rev = {i: node for i, node in enumerate(visited)}

    # Ancestor: pre-order Index -> Index of its DFS parent
    ancestor = {}
    for original_id, parent_id in dfs_parent.items():
        if parent_id is not None:
            ancestor[pre[original_id]] = pre[parent_id]
        else:
            # root has no ancestor
            ancestor[pre[original_id]] = None

    # build up graph node
    lt_graph = {idx: {
        PRE : idx,
        SUCCS : [pre[c] for c in graph[rev[idx]]], # the graph gives us successors!
        PREDS : [pre[u] for u in pred_map[rev[idx]]],
        PARENT : ancestor[idx] if idx in ancestor else None,
        SEMI : idx, # initialize to each node
        BEST : idx, # initialize to each node
        BUCKET : [],  # initialize to empty
        IDOM : None,  # initialize to empty
        ANC : None # this will hold link to DSU forest
    } for idx in range(len(visited))}

    return lt_graph, pre, rev


def lt_eval(node: g_node_t, graph: lt_graph_t) -> g_node_t:
    """Performs Find(node) with path compression and best-link update. Path
    compression updates ancestors to point at the (higher) best node: e.g. the
    node with the smallest RPO index. """

    anc_node = node[ANC]
    # check if this is a root node (only node with ancestor = None)
    if anc_node is None:
        return node

    # check if parent is a root node, so parent_ancestor is None
    if graph[anc_node][ANC] is None:
        return graph[node[BEST]]

    # Push entire ancestor chain (path compression)
    path = []
    x = node
    while True:
        path.append(x)
        if x[ANC] is None:
            break
        x = graph[x[ANC]]

    # Now, compress the path
    for idx, node_to_compress in enumerate(path[:-1]):
        ancestor_node = path[idx + 1]

        # If the ancestor's best semi-dominator is better than our current best, update ours.
        if graph[ancestor_node[BEST]][SEMI] < graph[node_to_compress[BEST]][SEMI]:
            node_to_compress[BEST] = ancestor_node[BEST]

        # 2. Path Compression: Make node point to its grandparent's index.
        node_to_compress[ANC] = ancestor_node[ANC]

    return graph[node[BEST]]


def gen_lt_graph(g: graph_t)->tuple[lt_graph_t, g_map_t, g_map_t]:
    """Use Lengauer-Tarjan to calculate dominator. Returns a fat graph
    in reverse post-order indexing, and mapping dicts to get back to original graph

    Args:
        g (graph_t): original graph

    Returns:
        fat graph with immediate dominators and predecessors, index mapping from list index to reverse post order, index mapping from reverse post order to list index
    """
    graph, pre, rev = init_lt(g)

    # 1. First Pass: Semi-Dominators and Implicit IDOMs
    for i in range(len(graph) - 1, 0, -1):
        curr_node = graph[i]

        parent_idx = curr_node[PARENT]
        parent_node = graph[parent_idx]

        # 1a. Compute Semi-dominator (semi) of all predecessors
        for j in curr_node[PREDS]:
            j_best_node = lt_eval(graph[j], graph=graph)
            if j_best_node[SEMI] < curr_node[SEMI]:
                curr_node[SEMI] = j_best_node[SEMI]

        # 1b. Place node in the bucket of its semi-dominator
        graph[curr_node[SEMI]][BUCKET].append(curr_node[PRE])

        # 1c. Link parent of current node to DSU (Union-Find Link)
        curr_node[ANC] = parent_idx

        # 1d. Compute Implicit Idoms (for nodes in parent's bucket)
        for b_idx in parent_node[BUCKET]:
            b_node = graph[b_idx]
            best_b = lt_eval(b_node, graph=graph)
            if best_b[SEMI] < b_node[SEMI]:
                b_node[IDOM] = best_b[PRE]
            else:
                b_node[IDOM] = parent_idx

        parent_node[BUCKET] = []

    # 2. Second Pass: Final Idom Fix-up
    for _, node in graph.items():
        if node[PARENT] is not None and node[IDOM] != node[SEMI]:
            node[IDOM] = graph[node[IDOM]][IDOM]

    graph[0][IDOM] = None
    return graph, pre, rev
