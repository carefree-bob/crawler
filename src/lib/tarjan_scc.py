from src.lib.crawler_type import graph_t

def get_tarjan_scc(graph: graph_t)->list[set[int]]:
    """Find strongly connected components

    Args:
        graph (graph_t): graph to search

    Returns:
        list of sets of nodes, each a strongly connected component

    """
    ids = {}  # Discovery time (id) of each node
    low = {}  # Low-link value
    on_stack = set()  # Fast lookup for "is node on recursion stack?"
    stack = []  # The actual Tarjan recursion stack (nodes)

    # simulates the call stack: (node, iterator_of_children)
    work_stack = []

    id_counter = 0
    results = []

    # Iterate over all nodes to handle disconnected graphs
    # list(graph) to ensure we don't modify the iterator if graph changes (though it shouldn't here)
    for start_node in graph:
        if start_node in ids:
            continue

        work_stack.append((start_node, iter(graph.get(start_node, []))))
        ids[start_node] = low[start_node] = id_counter
        id_counter += 1
        stack.append(start_node)
        on_stack.add(start_node)

        while work_stack:
            parent, children_iter = work_stack[-1]

            try:
                child = next(children_iter)

                if child not in ids:
                    # CASE A: Tree Edge (Child not visited)
                    # We pause the parent (leave it on stack) and "call" the child
                    ids[child] = low[child] = id_counter
                    id_counter += 1
                    stack.append(child)
                    on_stack.add(child)

                    # Push child to work_stack to process it next
                    work_stack.append((child, iter(graph.get(child, []))))

                elif child in on_stack:
                    # CASE B: Back Edge (child visited and currently active)
                    # Update low-link immediately
                    low[parent] = min(low[parent], ids[child])

            except StopIteration:
                # CASE C: All children processed (function return)
                # This block runs when the `for` loop would naturally finish
                work_stack.pop()

                # Check if parent is the root of an SCC
                if low[parent] == ids[parent]:
                    scc = []
                    while True:
                        node = stack.pop()
                        on_stack.remove(node)
                        scc.append(node)
                        if node == parent:
                            break
                    results.append(scc)

                # Propagate low-link to the caller
                if work_stack:
                    real_parent = work_stack[-1][0]
                    low[real_parent] = min(low[real_parent], low[parent])

    return results