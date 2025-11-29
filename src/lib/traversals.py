from crawler_type import graph_t, order_t

def dfs_pre_order_traversal(graph: graph_t) -> order_t:
    """Perform depth first search and return post-order ordering

    Args:
        graph (g_dict): graph to traverse

    Returns:
        ordering type
    """
    start, children = next(iter(graph.items()))
    visited = []
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            # in case there is an order on siblings
            for child in reversed(graph[node]):
                if child not in visited:
                    stack.append(child)

    return tuple(visited)

