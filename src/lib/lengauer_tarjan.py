from src.lib.crawler_type import graph_t, lt_graph_t, g_map_t, g_node_t

PRE = "pre"
SUCCS = "succs"
PREDS = "preds"
PARENT = "parent"
SEMI = "semi"
BEST = "best"
BUCKET = "bucket"
IDOM = "idom"
ANC = "anc"


def init_lt(graph: graph_t) -> tuple[lt_graph_t, g_map_t, g_map_t]:
    """
    Initializes the graph for L-T algorithm.
    """
    start, _ = next(iter(graph.items()))
    stack = [start]
    visited = []

    # Track predecessors for ALL nodes initially
    raw_pred_map = {g: set() for g in graph}
    dfs_parent = {start: None}

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            # Use strict list to ensure order doesn't fluctuate
            children = graph.get(node, [])
            for child in reversed(children):
                raw_pred_map[child].add(node)
                if child not in visited:
                    dfs_parent[child] = node
                    stack.append(child)

    pre = {node: i for i, node in enumerate(visited)}
    rev = {i: node for i, node in enumerate(visited)}

    ancestor = {}
    for original_id, parent_id in dfs_parent.items():
        if original_id in pre:
            ancestor[pre[original_id]] = pre[parent_id] if parent_id is not None else None

    lt_graph = {idx: {
        PRE: idx,
        # Safety: Only include nodes that are actually in our DFS tree (reachable)
        SUCCS: [pre[c] for c in graph[rev[idx]] if c in pre],
        PREDS: [pre[u] for u in raw_pred_map[rev[idx]] if u in pre],
        PARENT: ancestor[idx] if idx in ancestor else None,
        SEMI: idx,
        BEST: idx,
        BUCKET: [],
        IDOM: None,
        ANC: None
    } for idx in range(len(visited))}

    return lt_graph, pre, rev


def lt_eval(node: g_node_t, graph: lt_graph_t) -> g_node_t:
    """
    Iterative version of Find/Compress.
    Simulates recursion by collecting the path to root and processing top-down.
    """
    ancestor_idx = node[ANC]

    # 1. Base case: If root of DSU tree, return node itself
    if ancestor_idx is None:
        return node

    # 2. Build the path from 'node' up to the DSU root
    # path will be [node, parent, grandparent, ... root]
    path = [node]
    curr = node
    while curr[ANC] is not None:
        parent_node = graph[curr[ANC]]
        path.append(parent_node)
        curr = parent_node

    # 3. Traverse the path Top-Down (Reverse order) to apply compression.
    # We skip the very last element (Root) and the second to last (Child of Root),
    # because the Child of Root points to Root and needs no update.
    # range(start, stop, step)
    # Start at Grandchild of Root (index len-3) down to Node (index 0)
    for i in range(len(path) - 3, -1, -1):
        curr_node = path[i]
        parent_node = path[i + 1]  # This is the parent in the original tree structure

        # At this point, thanks to the top-down loop, 'parent_node'
        # has already been compressed and points to the Root.

        # Update BEST if the parent's compressed best is better
        if graph[parent_node[BEST]][SEMI] < graph[curr_node[BEST]][SEMI]:
            curr_node[BEST] = parent_node[BEST]

        # Path Compression: Point current node directly to where parent points
        curr_node[ANC] = parent_node[ANC]

    return graph[node[BEST]]


def gen_lt_graph(g: graph_t) -> tuple[lt_graph_t, g_map_t, g_map_t]:
    graph, pre, rev = init_lt(g)

    # first pass (decreasing for semi-doms)
    for i in range(len(graph) - 1, 0, -1):
        curr_node = graph[i]
        parent_idx = curr_node[PARENT]
        parent_node = graph[parent_idx]

        for j in curr_node[PREDS]:
            j_node = graph[j]
            j_best_node = lt_eval(j_node, graph=graph)

            if j_best_node[SEMI] < curr_node[SEMI]:
                curr_node[SEMI] = j_best_node[SEMI]

        graph[curr_node[SEMI]][BUCKET].append(curr_node[PRE])

        # Link to DSU forest
        curr_node[ANC] = parent_idx

        while parent_node[BUCKET]:
            b_idx = parent_node[BUCKET].pop()
            b_node = graph[b_idx]

            best_b = lt_eval(b_node, graph=graph)

            if best_b[SEMI] < b_node[SEMI]:
                b_node[IDOM] = best_b[PRE]
            else:
                b_node[IDOM] = parent_idx

    # Second Pass (increasing) for idom
    for i in range(1, len(graph)):
        node = graph[i]
        if node[IDOM] != node[SEMI]:
            node[IDOM] = graph[node[IDOM]][IDOM]

    graph[0][IDOM] = None
    return graph, pre, rev