from src.lib.crawler_type import graph_t, order_t

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


def dfs_post_order_traversal(graph: graph_t)->order_t:
    start, children = next(iter(graph.items()))
    stack = [start]
    processing = {g: 0 for g, _ in graph.items()} # points to index of processed child
    visited = []

    while stack:
        curr = stack[-1] # peek
        children = graph.get(curr)
        if len(children) > processing[curr]:
            # a child has not been processed
            curr_child = children[processing[curr]]
            if curr_child not in stack:
                stack.append(children[processing[curr]])
            processing[curr] += 1
        else:
            # all children processed
            if curr not in visited:
                visited.append(curr)
            stack.pop()

    return tuple(visited)
