# Generates gold files
import io  # Used to handle in-memory binary data
import math
import random

import networkx as nx
from PIL import Image  # Pillow library

import tests.test_data.graph_simple as gs
from src.lib.crawler_type import graph_t, order_t
def validate(g: graph_t) -> graph_t:
    # make sure there are always ancestors
    for node, anc in g.items():
        if g[node] is None:
            raise ValueError("missing ancestor!")
        if not isinstance(g[node], list):
            raise ValueError("ancestors are not lists!")
        if len(anc) != len(set(anc)):
            raise ValueError("doubled path!")

    return g

def g_to_nx(g: graph_t) -> nx.DiGraph:
    return nx.from_dict_of_lists(g, create_using=nx.DiGraph)

def nx_to_g(nx_g: nx.DiGraph) -> graph_t:
    return nx.to_dict_of_lists(nx_g)

def get_nx_post_order(g:graph_t)-> order_t:
    nx_g = g_to_nx(g)
    start, _ = next(iter(g.items()))
    return tuple(nx.dfs_postorder_nodes(nx_g, source=start))

def get_nx_pre_order(g:graph_t) -> order_t:
    nx_g = g_to_nx(g)
    start, _ = next(iter(g.items()))
    return tuple(nx.dfs_preorder_nodes(nx_g, source=start))

def get_dominance_frontier_via_nx(g:graph_t)->graph_t:
    nx_g = g_to_nx(g)
    start_node, _ = next(iter(g.items()))
    return nx.dominance_frontiers(nx_g, start_node)

def get_dominator_tree_via_nx(g:graph_t)->graph_t:
    nx_g = g_to_nx(g)
    start_node, _ = next(iter(g.items()))
    idom_map = nx.immediate_dominators(nx_g, start_node)
    dom_tree = nx.DiGraph()
    dom_tree.add_nodes_from(nx_g.nodes)

    for node, idom in idom_map.items():
        if node != idom:
            dom_tree.add_edge(idom, node)
    return nx_to_g(dom_tree)

def display_graph_with_pillow(g: nx.DiGraph):
    """
    Converts a NetworkX graph to Pydot, renders it to PNG data in memory,
    and displays it using Pillow.
    """
    try:
        A = nx.nx_pydot.to_pydot(g)
        A.set_rankdir('TB')

        png_data = A.create_png()

        data_stream = io.BytesIO(png_data)
        img = Image.open(data_stream)
        print("Displaying graph...")
        img.show()

    except ImportError:
        print("Error: The 'pydot' or 'Pillow' library is missing. Please install both.")
    except Exception as e:
        print(f"An error occurred during rendering. Is Graphviz installed and configured? Error: {e}")

def gen_random_graph(max_total_nodes: int=20, max_outbound_each=10, degree_connectivity=3) ->graph_t:
    """Generate a random connected graph starting at zero

    Args:
        max_total_nodes (int): max number of nodes
        max_outbound_each (int): max outbound connections per node
        degree_connectivity (int): 0-9, the probability that an outbound is a back edge

    Returns:
        graph_t graph in dict form

    """
    node_count = 1
    graph = {0: []}
    worklist = [0]
    if max_outbound_each == 0:
        return {0:[]}

    while worklist:
        current_node = worklist.pop()
        space = max_total_nodes - node_count
        roll = random.random()
        total_conn = random.randint(1 if current_node == 0 else 0, max_outbound_each)
        max_back_count = current_node

        if max_back_count == 0:
            children_count = min(total_conn, space)
            back_conns = []
        else:
            z = str(round(roll, total_conn))[2:]
            back_conns = [x for i, x in enumerate(range(current_node)) if int(z[i]) < degree_connectivity]
            children_count = min(total_conn - len(back_conns), space)

        to_add = list(range(node_count + 1, node_count + children_count))

        graph[current_node] = back_conns + to_add

        worklist += to_add
        node_count += len(to_add) + children_count

    # finish up any missing nodes
    for j in range(node_count):
        if j-1 not in graph:
            graph[j-1] = []

    return graph


def sort_dict(d:dict)->dict:
    if isinstance(d, dict):
        return {k: sort_dict(val) for (k, val) in d.items()}
    elif isinstance(d, list):
        return sorted(d)
    else:
        return d


if __name__ == '__main__':
    g_name = 'graph1'
    print(f"dominator tree of {g_name}")
    g = get_dominator_tree_via_nx(gs.graph_1)
    print(g)
    print("---------------------------")
    print("opening with pillow")
    display_graph_with_pillow(g_to_nx(g))

