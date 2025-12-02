import networkx as nx
import random
from typing import Dict, Any, Optional
from lengauer_tarjan import calculate_dominators, PRE, IDOM

NUM_TESTS = 1000
MAX_NODES = 200
EDGE_PROB = 0.2


def generate_random_gnp_graph(n_nodes: int, edge_prob: float) -> nx.DiGraph:
    """Generates a random connected directed graph that is guaranteed to have a root."""
    if n_nodes < 2:
        return nx.DiGraph()

    # 1. Generate a random graph using the G(n, p) model
    G = nx.fast_gnp_random_graph(n_nodes, edge_prob, directed=True)

    # 2. Check for connectivity and single entry point (node 0)
    # The L-T algorithm requires a single entry/start node (usually R or 0)

    # Ensure node 0 is the root by removing all incoming edges to 0
    in_edges_to_0 = list(G.in_edges(0))
    G.remove_edges_from(in_edges_to_0)

    # Ensure all other nodes are reachable from 0. If not, add edges.
    if not nx.is_strongly_connected(G.subgraph(G.nodes() - {0})):
        # If the graph is disconnected, we simplify the problem by adding a path from 0
        # to the rest of the graph. For simplicity, we just check reachability.
        if not nx.is_reachable(G, 0, n_nodes - 1):  # Heuristic check
            for i in range(1, n_nodes):
                if not nx.has_path(G, 0, i):
                    # Link 0 to any unreachable node to ensure reachability
                    G.add_edge(0, i)

    # We use 0 as the root node
    return G


def run_test_case(test_num: int, graph: nx.DiGraph) -> bool:
    """
    Runs one test case: compares the custom L-T implementation against NetworkX.
    """
    nodes = list(graph.nodes())
    if not nodes:
        print(f"Test {test_num}: Skipped (Empty Graph)")
        return True

    # 1. Get reference IDOMs from NetworkX
    try:
        nx_idom_map: Dict[Any, Optional[Any]] = nx.immediate_dominators(G, nodes[0])
    except nx.NetworkXNotImplemented:
        print(f"Test {test_num}: Skipped (NetworkX error)")
        return True

    # NetworkX returns the root dominating itself, which we exclude/set to None.
    nx_idom_map.pop(nodes[0], None)

    # 2. Get IDOMs from custom L-T implementation

    # Convert NetworkX DiGraph to the required dictionary format: {node: (succ1, succ2)}
    lt_graph_input = {node: tuple(G.successors(node)) for node in G.nodes()}

    # Run the custom function
    try:
        lt_graph_output, original_to_rpo, rpo_to_original = calculate_dominators(lt_graph_input)
    except Exception as e:
        print(f"Test {test_num} FAILED: L-T function crashed with error: {e}")
        # print(f"Graph: {lt_graph_input}")
        return False

    # 3. Compare Results

    # Convert L-T results (RPO index -> RPO index) back to Original ID -> Original ID
    lt_idom_map: Dict[Any, Optional[Any]] = {}

    for rpo_idx, rpo_node_data in lt_graph_output.items():
        original_id = rpo_to_original[rpo_idx]
        idom_rpo_idx = rpo_node_data[IDOM]

        if idom_rpo_idx is not None:
            # Map the idom index back to the original ID
            idom_original_id = rpo_to_original[idom_rpo_idx]
            lt_idom_map[original_id] = idom_original_id

        # Skip the root node (index 0) which has IDOM=None

    # Check for mismatches
    mismatches = False

    # Sort keys for consistent iteration and error reporting
    for node in sorted(nodes):
        if node == nodes[0]:  # Skip the root
            continue

        # Get the immediate dominator ID for the current node
        nx_idom = nx_idom_map.get(node)
        lt_idom = lt_idom_map.get(node)

        # Handle the case where a node might be unreachable in the DFS,
        # though the graph generation tries to prevent this.
        if nx_idom is None and lt_idom is None:
            continue

        if nx_idom != lt_idom:
            mismatches = True
            print(f"  Mismatch for node {node}: NX={nx_idom}, L-T={lt_idom}")

    if mismatches:
        print(f"Test {test_num} FAILED: Mismatches found.")
        # Optional: Print the graph for debugging
        # print(f"  Graph edges: {list(G.edges())}")
        return False

    print(f"Test {test_num} PASSED.")
    return True


def run_test_suite():
    """Main function to run the suite of random graph tests."""
    print(f"--- Running Dominator Tree Comparison Test Suite ({NUM_TESTS} cases) ---")
    passed_count = 0

    for i in range(1, NUM_TESTS + 1):
        # Generate a new random graph for each test
        n_nodes = random.randint(3, MAX_NODES)

        # Adjust edge probability slightly based on size to ensure some structure
        prob = min(EDGE_PROB, 1.0 / n_nodes)
        G = generate_random_flow_graph(n_nodes, prob)

        if G.number_of_nodes() < 2:
            continue

        if run_test_case(i, G):
            passed_count += 1

    print("-" * 50)
    if passed_count == NUM_TESTS:
        print(f"SUCCESS: All {NUM_TESTS} tests passed!")
    else:
        failed_count = NUM_TESTS - passed_count
        print(f"FAILURE: {failed_count} tests failed out of {NUM_TESTS}.")


if __name__ == "__main__":
    run_test_suite()