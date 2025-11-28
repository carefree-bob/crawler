from src.lib.crawler_type import g_dict, ordering

def dfs_pre_order_traversal(graph: g_dict) -> ordering:
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

