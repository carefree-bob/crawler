"""









/* Before the algorithm is actually called, some data structures have to be initialized
and dead code has to be removed:
*/
remove_dead_code(start) ; //assume connected from start
build_dominator_tree(start) ; // builds dominator tree
set_level(start,1); // recursively walks through tree to assign levels to nodes
mark_undone(start); // cleans marks recursively walks down tree
search_sp_back(start); // calculates all back edges (recursively walks down from root)
mark_undone(start); // cleans up marks after back edge search, but does not delete the sp_back container
split_loops(start, new_list (node)); // enter actual function

/*
The first argument to split_loops is the node that dominates all nodes that have
yet to be done. The second argument is a list of nodes that, if it is not empty,
defines a region that should not be left since all nodes outside have already been
done and have not changed. The function returns true if the given node has any
edges that indicate an irreducible loop at its level.

/*
bool split_loops(node top_node, list[node] set) {
    bool cross;
    node child;
    node pred;
    cross = false;
    foreach (child in top_node.succs_dom) {
        if (is_empty(set) || in_list(child, set)) {
            if (split_loops(child, set)) {
                cross = true;
            }
        }
    }

    if (cross) handle_ir_children(top_node, set);
    /*
        First all levels below the given node are handled as long as this does not leave
        the current region of interest. If any of these calls return true, then a child
        of top_node has detected an irreducible loop on the level just below top_node.
        This is handled after all children so that the domains in that loop are already
        reducible.
    */
    foreach (pred in top_node.preds) {
        if (is_sp_back(pred, top_node) &&
            !dom(top_node, pred)) {
                return true;
        }
    }

    return false;
    /*
        After the children of the current top_node have been handled completely, it is
        checked whether there is any edge that indicates an irreducible loop on the level
        of top_node itself and the result is returned.
    */

/*
    The function handle_ir_children is called with the external dominator node
    as an argument. It has to find all SED-maximal loop-sets and then split the
    irreducible
*/
void handle_ir_children(node top_node, list[node] set) {
    node child;
    node tmp;
    list[node] dfs_list;
    list[node] scc;
    list[list[node]] scc_list;
    dfs_list = new list[node]();
    scc_list = new list[list[node]]();


    foreach (child in top_node.succs_dom) {
        if ((!child.done) &&
        (is_empty(set) || in_list(child, set))) {
            SCC1(dfs_list, child, set, top_node.level) ;
        }
    }
    /*
        SCC1 implements the first pass of the SCC-algorithm. But instead of numbering
        the nodes they are collected
    */
    foreach (tmp in dfs_list) {
        if (tmp.done) {
            scc = new_list (node) ;
            SCC2(scc, tmp, top_node. level) ;
            add_list(scc, scc_list);
        }
    }
    /*
        Starting with the “highest numbered” node SCC2 is called, which implements the
        second pass of the SCC-algorithm. Each new call to SCC2 starts a new tree and,
        therefore, a new SCC. These SCCs are all collected in the list scc_list.
    */
    foreach (scc in scc_list) {
        if (size_list(scc) > 1) {
            handle_scc(top_node, scc);
        }
    }
    /*
        After all SCCs have been found, they are now converted by handle_scc one by one.
    */
}

void handle_scc(node top_node, list[node] scc) {
    node tmp;
    list[node] msed;
    list[node] tops;
    msed = new_list (node) ;
    foreach (tmp in scc) {
        if (tmp.level == top_node.level + 1) {
            GetWeight (tmp, tmp, scc);
            add_list(tmp, msed) ;
        }
    }
    if (size_list(msed) <= 1) return;
    /*
        handle_scc first determines, which nodes of the SCC are in the MSED-set by
        comparing the level of the nodes with that of the external dominator. For each
        node in the MSED-set the function GetWeight is called, which sums up the weight
        of all nodes in its domain and sets the header links. If the MSED-set consists
        of just one node, the SCC is a reducible loop and does not need any further
        processing.
    */
    tmp = ChooseNode(msed) ;
    SplitSCC(tmp, scc);
    /*
        Otherwise ChooseNode is called, which applies the heuristic and chooses the heay-
        iest node. SplitSCC then splits all nodes in the SCC except the chosen node and
        its domain, rearranges the control flow graph and changes the dominator infor-
        mation such that the copied regions are independent subtrees in the dominator
        tree.
    */
    build_dominator_tree(start) ;
    set_level(start,1);
    mark_undone(start) ;
    search_sp_back(start) ;
    mark_undone(start) ;
    /*
        Since the changes made by SplitSCC may have made the dominator tree invalid,
        it is recomputed. However, to rebuild the entire tree is rather inefficient since
        only the nodes below top_node have changed. A more elaborate algorithm would
        use top_node as the argument and build_dominator_tree would use the old
        information to rebuild just the subtree below it. The same is also true for the
        remaining re-initializations.
    /*
    tops = new_list (node) ;
    find_top_nodes(scc, tops);
    foreach (tmp in tops) {
        split_loops(tmp, scc);
    }
    /*
        After all structures have been rebuild, find_top_nodes is used to collect the nodes
        that may have become external dominators. For these, split_loops is called
        recursively to resolve any remaining irreducibility. However, such irreducible
        regions will always be subsets of the SCC that was just split. Thus the current
        SCC is given as the second argument such that split_loops will never recurse
        out of it.
    */
}

void SplitSCC(node header_node, list[node] scc) {
    node tmp;
    node tmp1;
    foreach (tmp in scc) {
        if (tmp.header != header_node) {
            tmp.copy = copy(tmp) ;
        }
    }
    /*
        SplitSCC first makes a copy for every node that is to be split. The component
        header has been set by the previous call to GetWeight and points to the header
        of the domain the node belongs to. That way it is simple to find out which nodes
        are in the domain of the node that should not be split.
        Note that copy is supposed to copy at least all of the information in the members
        listed in the last section.
    */
    foreach (tmp in scc) {
        if (tmp.header != header_node) {
            if (tmp.idom.copy == NULL) {
                add_list(tmp.copy, tmp.idom.succs_dom) ;
            } else {
                remove_list(tmp, tmp.idom.copy.succs_dom) ;
                add_list(tmp.copy, tmp.idom.copy.succs_dom) ;
                tmp.copy.idom = tmp.idom.copy;

                foreach (tmp1 in tmp.succs_dom) {
                    if (tmp1.copy == NULL) {
                        remove_list(tmp1, tmp.copy.succs_dom) ;
                    }
                }
                /*
                After the copies are made several steps are done on each node that got a copy.
                First, the dominator information is adjusted: If the node had an immediate
                dominator outside the copied region, then the copy has the same dominator and
                thus becomes another successor in the dominator tree. If the node’s dominator
                has itself got a copy, then the dominance relation between the copies is made
                the same as between the originals. As a last step regarding the dominators the
                successors are updated. Successors within the copied regions have already been
                corrected by the previous step. But if any node has a successor outside the
                copied region, its copy has got that successor as well, thereby destroying the
                tree structure. This is corrected by letting the outside node be a child of the
                original only and removing it from the list succs_dom of the copy. This does not
                reflect the true dominance relations but retains the tree structure on which an
                incremental build_dominator_tree
                */
                foreach (tmp1 in tmp.succs) {
                    if (tmpl.copy != NULL) {
                        rmv_list(tmp1, tmp.copy.succs);
                        add_list(tmp1.copy, tmp.copy.succs) ;
                        rmv_list(tmp, tmp1.copy.preds) ;
                        add_list(tmp.copy, tmp1.copy.preds) ;
                    } else {
                        add_list(tmp.copy, tmp1.preds) ;
                    }
                }
                /*
                Once the dominator information has been corrected, the successor links are ad-
                justed in a similar way. Links between nodes inside the copied regions are just
                replicated on the copies. If a successor is outside the copied region it has got just
                one more predecessor.
                */
                foreach (tmp1 in tmp.preds) {
                    if (tmp1.copy == NULL) {
                        if (!in_list(tmp1, scc)) {
                            rmv_list(tmp1, tmp.copy.preds) ;
                        } else {
                            rmv_list(tmp1, tmp.preds) ;
                            rmv_list(tmp, tmp1.succs) ;
                            add_list(tmp.copy, tmp1.succs) ;
                        }
                    }
                }
            }
        }
    /*
        The last step adjusts the predecessor links. Again, the predecessors inside the
        split region have already been corrected. What has to be done with a predecessor
        outside depends on whether it is in the domain of h; (header_node) or not. In the
        first case, it remains a predecessor of the original and has to be removed from the
        preds-list of the copy. In the second case, it becomes a predecessor of the copy
        alone.
    */
    foreach (tmp in scc) {
        add_list(tmp.copy, scc);
        tmp.copy = NULL;
    }
}

/*
    After all connections between the nodes have been updated, the new nodes be-
    come part of the SCC and the copy members are reset so that subsequent invo-
    cations of SplitSCC do not get confused. Note that the list used in the foreach-
    statement is changed in the body of that statement. It is assumed, that the
    foreach-statement is executed for the original members of the list only and not
    for the newly added ones.
*/

void SCC1(list[node] dfs_list, node cnode,
    list[node] set, integer level) {
    node child;
    cnode.done = true;
    foreach (child in cnode.succs) {
        if (!child.done && child.level > level &&
            (is_empty(set) || in_list(child, set))) {
            SCC1(dfs_list, child, set, level);
        }
    }
    add_list(cnode, dfs_list);
}
/*
    SCC1 traverses the control flow graph in a depth-first search collecting the nodes
    in the list dfs_list. The only things special in that search are that it never
    traverses to a level higher (or lower numbered) than the level given, which was
    the level of the external dominator, and that it never leaves the region defined
    by set.
*/

void SCC2(list[node] scc, node cnode, integer level) {
    node pred;
    cnode.done = false;
    foreach (pred in cnode.preds) {
        if (pred.done && pred.level > level) {
            SCC2(scc, pred, level);
        }
    }
    add_list(cnode, scc);
}
/*
    To avoid at least one call to mark_undone, SCC2 uses the member done in the
    inverse meaning. A node with done being false has actually been done or was
    outside of set in the call to SCC1. That way SCC2 also stays within that region.
*/

void find_top_nodes(list[node] scc, list[node] tops) {
    node tmp;
    node top;
    foreach (tmp in scc) {
        top = tmp.idom;
        while (in_list(top, scc)) {
            top = top.idom;
        }
        if (!in_list(top, tops)) {
            add_list(top, tops);
        }
    }
}
/*
    The split SCC may have fallen into several pieces dominated by different nodes.
    Since all of these may still be irreducible, split_nodes must be called for each
    node that dominates such a piece. Therefore, find_top_nodes collects all of these
    in the list tops.
*/


/*
ChooseNode implements the heuristic and returns the heaviest node of the given
MSED-set.
*/
node ChooseNode(list[node] msed) {
    integer MaxWeight ;
    node MaxNode;
    node tmp;
    MaxWeight = 0;
    foreach (tmp in msed) {
        if (tmp.weight > MaxWeight) {
            MaxWeight = tmp.weight;
            MaxNode = tmp;
        }
    }
    return MaxNode;
}


/*
    GetWeight sums up the weight of the nodes in each domain and sets the header
    node’s weight-member.
*/
void GetWeight (node tmp, node header_node, list[node] scc) {
    node child;
    tmp.weight = sigma(tmp) ;
    foreach (child in tmp.succs_dom) {
        if (in_list(child, scc)) {
            GetWeight(child, header_node, scc);
            tmp.weight = tmp.weight + child.weight;
        }
    }
    tmp.header = header_node;
}


/*
search_sp_back marks all sp_back-edges as such.
*/
void search_sp_back(node cnode) {
    node child;
    cnode.done = true;
    cnode.active = true;
    remove_marks(cnode) ;
    foreach (child in cnode.succs) {
        if (child.active) {
            mark_sp_back(cnode, child);
        } else {
            if (!child.done) {
                search_sp_back (child) ;
            }
        }
    }
    cnode.active = false;
}

/* set_level is used to calculate the depth of each node in the dominator-tree. */

void set_level(node cnode, integer level) {
    node child;
    cnode.level = level;
    foreach (child in cnode.succs_dom) {
        set_level(child, level + 1);
    }
}

/*
    mark_undone resets the done-flag used by various other functions. The active-
    flag may as well be reset just once in main before the first call to search_sp_back.
    The algorithm then manages to reset this flag on the way.
*/
void mark_undone(node cnode) {
    node child;
    cnode.done = false;
    cnode.active = false;
    foreach (child in cnode.succs_dom) {
        mark_undone (child) ;
    }
}
"""