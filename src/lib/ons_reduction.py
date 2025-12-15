"""
Reference: 'Transforming Irreducible Regions of Control Flow Into
Reducible Regions by Optimized Node Splitting' Sebastian Unger
M.S. thesis, Humboldt University Berlin, Germany (1998).

"""
from src.lib.crawler_type import ONS_Node_t, ons_graph_t, lt_graph_t, g_node_t, graph_t
from src.lib.dominator import gen_lt_graph, get_dominator_tree, get_dominator_tree_from_nodal
from src.lib.graph_utils import dfs_post_order_traversal

PRE = "pre"
SUCCS = "succs"
PREDS = "preds"
IDOM = "idom"
SUCCS_DOM = "succs_dom"
LEVEL = "level"
WEIGHT = "weight"
COPY = "copy"
HEADER = "header"
DONE = "done"
ACTIVE = "active"
SP_BACK_DATA = "sp_back_data"


def _get_dom_post_order(g: ons_graph_t, start: ONS_Node_t, restrict_to: list[ONS_Node_t]=None)->list[ONS_Node_t]:
    """Perform post order traversal subject to node restriction"""
    if restrict_to and not start in restrict_to:
        return []

    stack = [start]
    visited = []
    processing = {g: 0 for g, _ in g.items()}

    while stack:
        curr = stack[-1]  # peek
        children = [node for node in curr.get(SUCCS_DOM)
                    if (not restrict_to) or node in restrict_to]

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

    return visited

def populate_pointers(graph:ons_graph_t) -> None:
    for idx, g in graph.items():
        g[SUCCS] = [graph[id_t] for id_t in g[SUCCS]]
        g[PREDS] = [graph[id_t] for id_t in g[PREDS]]
        for id_s in g[IDOM]:
            graph[id_s][SUCCS_DOM].append(g)

def mark_back_edges(graph: ons_graph_t, start_node: ONS_Node_t):
        """
        Finds back-edges (indicating loops) using iterative DFS.
        Returns a list of (source, target) tuples.
        """
        # call stack: stores (node, iterator_of_children)
        # We use iter() so we know exactly where we left off when we return to a node.
        stack = [(start_node, iter(start_node[SUCCS]))]
        path_set = {start_node}
        visited = {start_node}
        while stack:
            parent, children_iter = stack[-1]
            try:
                child = next(children_iter)
                if child in path_set:
                    parent[SP_BACK_DATA] = (parent[PRE], child[PRE])

                elif child not in visited:
                    visited.add(child)
                    path_set.add(child)
                    stack.append((child, iter(child[SUCCS])))

            except StopIteration:
                # We have finished all children of 'parent'.
                stack.pop()
                path_set.remove(parent)
        return

def _build_ons_graph_from_lt(g: lt_graph_t)->ons_graph_t:
    lt_graph, pre, rev = gen_lt_graph(g)
    post_order = dfs_post_order_traversal(lt_graph)
    ons_g = {idx: {
        PRE: idx,
        SUCCS: node["succs"],
        PREDS: node["preds"],
        IDOM: node["idom"],
        SUCCS_DOM: [],
        LEVEL: None,
        WEIGHT: 1,
        COPY: None,
        HEADER: None,
        DONE: False,
        ACTIVE: False,
        SP_BACK_DATA: None
    }
        for idx, node in lt_graph_t.items()
    }
    populate_pointers(ons_g)
    return ons_g

def clear_marks(ons_g: ons_graph_t):
    for idx, g in ons_graph_t.items():
        g[DONE] = False
        g[ACTIVE] = False

def clear_back_edges(ons_g: ons_graph_t):
    for idx, g in ons_graph_t.items():
        g[SP_BACK_DATA] = None

def init_ons(g: graph_t)->tuple[ons_graph_t, ONS_Node_t]:
    """Returns fresh graph with all
    dominator info and back-edges marked"""
    ons_g = _build_ons_graph_from_lt(g)
    start_node = ons_g[0]
    mark_back_edges(ons_g, start_node)
    return ons_g, start_node

def split_loops(start_node: ONS_Node_t, ons_graph: ons_graph_t, restrict_to: list[ONS_Node_t]=None)->bool:
    """
    Args:
        ons_graph (ons_graph_t):
        start_node (ONS_Node_t): Is the dominators whose subtree we will investigate
        restrict_to (list[OnsNode]): Do not leave this list (e.g. can be a domain or subgraph)

    Returns:
        (bool) true if there is an irreducible loop in this subtree

    """
    if restrict_to and start_node not in restrict_to:
        print(f"cannot process as start node not in restriction set")
        return False

    stack = [start_node]
    processing = {g: 0 for g, _ in ons_graph.items()} # points to index of processed child
    to_visit = []

    while stack:
        curr = stack[-1] # peek
        children = [x for x in ons_graph.get(SUCCS_DOM) if (not restrict_to or x in restrict_to)]
        if len(children) > processing[curr]:
            curr_child = children[processing[curr]]
            if curr_child not in stack:
                stack.append(children[processing[curr]])
            processing[curr] += 1
        else:
            # all children processed
            if curr not in to_visit:
                to_visit.append(curr)
            stack.pop()







