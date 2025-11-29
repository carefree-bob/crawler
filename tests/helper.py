# Generates gold files
import networkx as nx
import pydot
from PIL import Image # Pillow library
import io # Used to handle in-memory binary data

from src.lib.crawler_type import graph_t
import test_data.graph_simple as gs

def g_to_nx(g: graph_t) -> nx.DiGraph:
    return nx.from_dict_of_lists(g, create_using=nx.DiGraph)

def nx_to_g(nx_g: nx.DiGraph) -> graph_t:
    return nx.to_dict_of_lists(nx_g)

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
        # 1. Convert NetworkX graph to a pydot.Dot object (A)
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
        # This catches errors if Graphviz executables (like 'dot') are not found.
        print(f"An error occurred during rendering. Is Graphviz installed and configured? Error: {e}")


if __name__ == '__main__':
    g_name = 'graph1'
    print(f"dominator tree of {g_name}")
    g = get_dominator_tree_via_nx(gs.graph_1)
    print(g)
    print("---------------------------")
    print("opening with pillow")
    display_graph_with_pillow(g_to_nx(g))

