"""
Implementation of Controlled Node Splitting

Ref:
"Making Graphs Reducible with Controlled Node
Splitting" Johan Janssen and Henk Corporaal (1997)
ACM Transactions on Programming Languages and Systems, Vol. 19, No. 6, November 1997.
"""
from src.lib.crawler_type import graph_t, lt_graph_t, T1T2Data_t, split_data_t, weights_t, g_node_t
from src.lib.dominator import gen_lt_graph
from src.lib.hecht_ullman_reduction import get_reduced_graph, reduce_t1t2_data


def build_strategy(lt_graph: lt_graph_t, strategy_name: str):

    idoms = { node['idom'] for _, node in lt_graph.items() if node['idom'] is not None }

    if strategy_name == 'back_edge':
        def func(node: g_node_t)-> bool:
            return len(set(node['preds']).intersection(idoms)) == 0
        return func
    elif strategy_name == 'normal_node':
        def func(node: g_node_t)->bool:
            return node['pre'] not in idoms
        return func

    raise ValueError(f"undefined strategy {strategy_name}")


def get_split(lt_graph: lt_graph_t, weights: weights_t, strategy_name="normal_mode")->g_node_t:

    best = (None, float("+Inf"))
    can_split = build_strategy(lt_graph, strategy_name=strategy_name)

    idoms = { node['idom'] for _, node in lt_graph.items() if node['idom'] is not None }

    # skip start
    for idx, node in lt_graph[1:].items():
        score = weights[idx] * ( len(node['preds']) - 1 )
        if score >= best[1]:
            continue
        else:
            if idx not in idoms:
                best = (node, score)
                continue
            else:
                if can_split(node):
                    best = (node, score)
                    continue
                else:
                    continue
    return best[0]


def split_graph(lt_graph: lt_graph_t, node_to_split: g_node_t, weights: weights_t)->tuple[T1T2Data_t, split_data_t]:
    """Splits node_to_split in lt_graph and returns a new graph within t1T2 structure, together with split data

    Args:
        weights (weights_t): array node -> weight
        lt_graph (lt_graph): graph with node to split
        node_to_split (g_node_t): node to split

    Returns:
        T1T2 data, split data

    """
    new_graph = {idx: node['succs'] for idx, node in lt_graph.items() if idx != node_to_split['pre']}

    new_preds = {idx: node['preds'] for idx, node in lt_graph.items() if idx != node_to_split['pre']}

    new_weights = list(weights)
    split_data = []

    for idx, p in enumerate(node_to_split['preds']):
        old_idx = node_to_split['pre']
        old_weight = weights[old_idx]
        l = len(new_graph)
        new_idx = old_idx if idx == 0 else l + idx
        new_graph[new_idx] = node_to_split['succs']

        succs = new_graph[p]['succs']
        new_preds[new_idx] = [p]

        if idx != 0:
            succs.remove(old_idx)
            succs.append(new_idx)
            new_weights[new_idx] = old_weight

        split_data.append({
            "duplicate": new_idx,
            "original": old_idx
        })

    return {
        "start": lt_graph[0]['pre'],
        "graph": new_graph,
        "preds": new_preds,
        "weights": new_weights,
        "log": []
    }, split_data


def cns_reduce(graph: graph_t, weights: weights_t=None)->list[tuple[T1T2Data_t, split_data_t]]:
    """Perform Hecht-Ullman reduction with controlled
    node splitting until the graph is a single node

    Args:
        graph (graph_t): graph
        weights (weights_t): weight

    Returns:
        list (T1T2 data, split_data)

    """
    if weights is None:
        weights = [1 for g in graph]
    t1_t2_curr = get_reduced_graph(graph, weights)
    res = [(t1_t2_curr, ())]

    while len(t1_t2_curr['graph']) > 1:
        graph_curr = t1_t2_curr['graph']
        weights = t1_t2_curr['weights']
        lt_graph_curr = gen_lt_graph(graph_curr)
        node_idx = get_split(lt_graph_curr, t1_t2_curr['weights'])
        new_t1t2, split_tuples = split_graph(lt_graph_curr, node_idx, weights)

        t1_t2_curr = reduce_t1t2_data(new_t1t2)

        res.append((t1_t2_curr, split_tuples))

    return res
