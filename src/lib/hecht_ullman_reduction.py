from src.lib.crawler_type import T1T2Data_t
from src.lib.crawler_type import graph_t, weights_t, Reduce
from src.lib.graph_utils import get_preds

"""
Ref: Matthew S. Hecht and Jeffrey D. Ullman. 1972. Flow graph reducibility. In Proceedings of the fourth annual ACM symposium on Theory of computing (STOC '72).

"""
def _reduce_t1(data: T1T2Data_t)->T1T2Data_t:
    """Do T1 reduction. The node that is modified is written
    to the log

    Args:
       data (T1T2Data_t): graph data for T1T2 Analysis

    Returns:
        (T1T2Data) reduced_graph

    """
    graph = data["graph"]
    preds = data["preds"]
    weights = data["weights"]
    log = data["log"]

    for node, anc in graph.items():
        # check for self-loop
        if node in anc:
            # log state first
            node_anc = [x for x in anc]
            node_pred = [x for x in graph[node]]
            log.append(
                (Reduce.T1, node,
                 (),
                 (),
                 tuple(node_anc),
                 tuple(node_pred),
                 weights[node]
                 )
            )
            graph[node] = [x for x in anc if x != node]
            preds[node] = [x for x in preds[node] if x != node]

    return data


def _reduce_t2(data: T1T2Data_t)->T1T2Data_t:
    """Apply T2 transformation. The node that is absorbed
       is written into the log. Mutates T1T2Data.

    Args:
        data (T1T2Data_t): graph data for reduction

    Returns:
        (T1T2Data) reduced graph

    """
    graph = data["graph"]
    preds = data["preds"]
    weights = data["weights"]
    log = data["log"]
    start = data["start"]

    to_traverse = {x:v for x, v in graph.items()}

    for node, _ in to_traverse.items():
        if node != start:
            pred = preds[node]
            if pred and len(pred) == 1 and pred != [node]:
                u = pred[0] # this the node that will absorb node
                # Log change before mutating
                u_preds = [x for x in preds[u]]
                u_succs = [x for x in graph[u]]
                node_preds = [x for x in preds[node]]
                node_succs = [x for x in graph[node]]

                log.append(
                    (Reduce.T2,
                        node,
                        tuple(u_succs),
                        tuple(u_preds),
                        tuple(node_succs),
                        tuple(node_preds),
                        weights[node]
                    )
                )

                # delete node as a child of u
                graph[u].remove(node)

                # add children of node back to u
                graph[u] += [x for x in graph[node] if x not in graph[u]]

                # fix predecessors of the children of node:
                #  - For every element that views itself as a child of node
                #  - it is now a child of u (if it wasn't before)
                for j in graph[node]:
                    if u not in preds[j]:
                        preds[j].append(u)
                    preds[j].remove(node)

                del preds[node]
                del graph[node]
                weights[u] += weights[node]
                del weights[node]

    return data

def reduce_t1t2_data(data: T1T2Data_t) -> T1T2Data_t:
    """Apply Hecht-Ullman T1 T2 Analysis to reduce graph. Mutates data.

    Args:
        data (T1T2Data_t): Graph data (call init_t1t2 to gen from graph)

    Returns:
        (T1T2Data) data

    """
    while True:
        ops_before = len(data["log"])
        data = _reduce_t2(_reduce_t1(data))
        ops_after = len(data["log"])

        if ops_before == ops_after:
            break

    return data

def init_t1t2(graph: graph_t, weights: weights_t | None=None) -> T1T2Data_t:
    # make copy as we will be mutating
    new_graph = {x: [t for t in v] for x, v in graph.items()}
    start, _ = next(iter(graph.items()))

    return {
        "start": start,
        "graph": new_graph,
        "preds": get_preds(new_graph),
        "weights": weights or {node: 1 for node, _ in new_graph.items()},
        "log": []
        }


def get_reduced_graph(graph: graph_t, weights: weights_t=None) -> T1T2Data_t:
    """Reduce graph according to T1-T2 Hecht-Ullman reduction.

    Args:
        graph (graph_t): graph to reduce
        weights (weight_t): weight dict of each node

    Returns:
        T1T2Data for the reduced graph

    """
    data = init_t1t2(graph, weights)
    return reduce_t1t2_data(data)


def recover_orig_data(data: T1T2Data_t) -> T1T2Data_t:
    """Recovers original graph by unwinding log. Mutates T1T2Data (including orig log)

    Args:
        data (T1T1Data): reduced data

    Returns:
        orig data
    """
    log = data["log"]
    graph = data["graph"]
    preds = data["preds"]
    weights = data["weights"]

    while log:
        action, node, parent_succs, parent_preds, node_succs, node_preds, node_weight = log.pop()

        node_succs = list(node_succs)
        node_preds = list(node_preds)

        if action is Reduce.T1:
            # add self-loop
            assert node in graph
            if graph[node]:
                graph[node].append(node)
            else:
                graph[node] = [node]
            # update preds
            preds[node].append(node)
            continue

        elif action is Reduce.T2:
            parent = node_preds[0]
            p_succs = list(parent_succs)
            p_preds = list(parent_preds)

            # fix up parent
            graph[parent] = p_succs
            preds[parent] = p_preds

            # add node to graph
            graph[node] = node_succs
            preds[node] = [parent]

            # make sure descendents of node have right predecessors
            for node_child in graph[node]:
                if node not in preds[node_child]:
                    preds[node_child].append(node)

                if parent in preds[node_child] and node_child not in graph[parent]:
                    preds[node_child].remove(parent)

            # make sure descendents of parent have the right predecessors
            for parent_child in graph[parent]:
                if parent not in preds[parent_child]:
                    preds[parent_child].append(parent)
                if node in preds[parent_child] and parent_child not in graph[node]:
                    preds[parent_child].remove(node)

            # make sure predecessors of node know they are predecessors
            for x in preds[node]:
                if node not in graph[x]:
                    graph[x].append(node)

                if parent in graph[x] and x not in preds[parent]:
                    graph[x].remove(parent)

            weights[parent] -= node_weight
            weights[node] = node_weight
            continue

        else:
            raise ValueError(f"Unrecognized action type {action}")

    return data

