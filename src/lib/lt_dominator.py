from crawler_type import graph_t, lt_graph_t, g_map_t, g_node_t

"""
Ported to python from the javascript implementation (MIT License) at https://github.com/julianjensen/dominators/

-- Thank you, Julian Jensen.

"""

"""
Fake enums, to help with typos
"""
pre_ = "pre"
succs_ = "succs"
preds_ = "preds"
parent_ = "parent"
semi_ = "semi"
best_ = "best" # (smallest semi value)
bucket_ = "bucket"
idom_ = "idom"
anc_ = "anc"

def init_lt(graph: graph_t) -> tuple[lt_graph_t, g_map_t, g_map_t]:
    """Perform DFS to generate graph with g_node_t and produce mappings
    Args:
        graph (graph_t): array graph

    Returns:
        lt_graph (fat dictionary). All entries in lt_graph are in pre-order index
        pre_map (g_map_t) map from list index to pre-order index
        rev_map (g_map_t) reverse of pre_map, taking pre-order to list index
    """

    # 1. Initialization
    start = next(iter(graph.keys()))
    stack = [start]
    visited = {start}
    post_order = []  # Stores nodes in post-order (used to derive RPO)

    # Tracks the parent in the DFS spanning tree (Original ID -> Original ID)
    dfs_parent = {start: []}

    # Tracks the predecessors (Original ID -> list of Original IDs)
    pred_map = {node: [] for node in graph}

    # Tracking for the iterative DFS state
    next_child_index = {node: 0 for node in graph}

    # 2. Iterative DFS (Post-Order Sequence, Ancestor, and Predecessors)
    while stack:
        u = stack[-1]
        children = graph.get(u, ())

        # Check children
        if next_child_index[u] < len(children):
            v = children[next_child_index[u]]
            next_child_index[u] += 1

            # Every edge defines a predecessor relationship
            pred_map[v].append(u)

            if v not in visited:
                visited.add(v)
                stack.append(v)
                dfs_parent[v] = u  # u is the parent that pushed v onto the stack
        else:
            # All children/edges processed, FINISH the node
            stack.pop()
            post_order.append(u)

    # 3. Final Mappings (using RPO indices)
    rpo_sequence = tuple(reversed(post_order))
    N = len(rpo_sequence)

    # Pre: Original Node ID -> RPO Index (pre-order number)
    pre = {node: i for i, node in enumerate(rpo_sequence)}

    # Rev: RPO Index -> Original Node ID
    rev = {i: node for i, node in enumerate(rpo_sequence)}

    # Ancestor: RPO Index -> RPO Index of its DFS parent
    ancestor = {}
    for original_id, parent_id in dfs_parent.items():
        if parent_id:
            ancestor[pre[original_id]] = pre[parent_id]
        else:
            # The root (RPO Index 0) has no ancestor
            ancestor[pre[original_id]] = []

    # build up graph node
    graph = {pre_v: {
        pre_ : pre_v,
        succs_ : [pre[c] for c in graph[rev[pre_v]]],
        preds_ : [pre[u] for u in pred_map[rev[pre_v]]],
        parent_ :  pre[orig_parent_id] if (orig_parent_id := dfs_parent[rev[pre_v]]) else [],
        semi_ : pre_v, # initialize to each node
        best_ : pre_v, # initialize to each node
        bucket_ : [],  # initialize to empty
        idom_ : None,  # initialize to empty
        anc_ : ancestor[pre_v] if pre_v in ancestor else []
    } for pre_v in range(N)}

    return graph, pre, rev


def lt_eval(node: g_node_t, graph: lt_graph_t) -> g_node_t:
    """Performs Find(node) with path compression and best-link update."""

    # Check if the node is effectively the root of its current Union-Find tree
    n_anc_idx = node[anc_]
    if not n_anc_idx or not graph[n_anc_idx][anc_]:
        return graph[node[best_]]

    # Push entire ancestor chain (path compression)
    x = node
    path = []

    # Traverse the path and collect nodes for compression
    while x[anc_] and graph[x[anc_]][anc_]:
        path.append(x)
        x = graph[x[anc_]]  # Move up to the ancestor node object

    # Now, compress the path
    for node_to_compress in path:
        ancestor_node = graph[node_to_compress[anc_]]

        # 1. Update best_ link
        # If the ancestor's best semi-dominator is better than our current best, update ours.
        if graph[ancestor_node[best_]][semi_] < graph[node_to_compress[best_]][semi_]:
            node_to_compress[best_] = ancestor_node[best_]

        # 2. Path Compression: Make node point to its grandparent's index.
        node_to_compress[anc_] = ancestor_node[anc_]

    return graph[node[best_]]


def gen_lt_graph(g: graph_t)->tuple[lt_graph_t, g_map_t, g_map_t]:
    """Use Lengauer-Tarjan to calculate dominator. Returns a fat graph
    in reverse post-order indexing, and mapping dicts to get back to original graph

    Args:
        g (graph_t): original graph

    Returns:
        fat graph with immediate dominators and predecessors, index mapping from list index to reverse post order, index mapping from reverse post order to list index
    """
    graph, pre, rev = init_lt(g)
    for i in range(len(graph) - 1, 0, -1):
        n = graph[i]

        p_idx = n[parent_]
        p_node = graph[p_idx]

        for j in n[preds_]:
            best_j = lt_eval(graph[j], graph=graph)
            if best_j[semi_] < n[semi_]:
                n[semi_] = best_j[semi_]

        # update the bucket of the semi-dominator
        graph[n[semi_]][bucket_].append(n[pre_])

        # simple link (Union-Find link)
        n[anc_] = p_idx

        for b_idx in p_node[bucket_]:
            b_node = graph[b_idx]  # Get the actual node object for 'b'
            best_b = lt_eval(b_node, graph=graph)
            if best_b[semi_] < b_node[semi_]:
                b_node[idom_] = best_b[pre_]
            else:
                b_node[idom_] = p_idx

        p_node[bucket_] = []

    graph[0][idom_] = None
    return graph, pre, rev


