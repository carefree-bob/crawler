from src.lib.crawler_type import graph_t

"""
Tarjan SCC, ported from networkx library (BSD License) 

"""
def get_tarjan_scc(graph: graph_t)->list[set[int]]:
    """get list of scc components

    Args:
        graph (graph_t):

    Returns:
        list[set(SCC)]
    """
    all_scc = []
    preorder = {}
    low_link = {}
    scc_found = set()
    scc_queue = []
    i = 0  # Preorder counter
    for source in graph:
        if source not in scc_found:
            queue = [source]
            while queue:
                v = queue[-1]
                if v not in preorder:
                    i = i + 1
                    preorder[v] = i
                done = True
                for w in graph[v]:
                    if w not in preorder:
                        queue.append(w)
                        done = False
                        break
                if done:
                    low_link[v] = preorder[v]
                    for w in graph[v]:
                        if w not in scc_found:
                            if preorder[w] > preorder[v]:
                                low_link[v] = min([low_link[v], low_link[w]])
                            else:
                                low_link[v] = min([low_link[v], preorder[w]])
                    queue.pop()
                    if low_link[v] == preorder[v]:
                        scc = {v}
                        while scc_queue and preorder[scc_queue[-1]] > preorder[v]:
                            k = scc_queue.pop()
                            scc.add(k)
                        scc_found.update(scc)
                        all_scc.append(scc)
                    else:
                        scc_queue.append(v)
    return all_scc