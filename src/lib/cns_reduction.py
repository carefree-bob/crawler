"""
Implementation of Controlled Node Splitting

Ref:
"Making Graphs Reducible with Controlled Node
Splitting" Johan Janssen and Henk Corporaal (1997)

"""

"""
Outline:
1. reduce graph. If length 1 then stop.
2. Find immediate dominators
3. find SCC
4. find MSED sets -- they will be dominated by an immed. dominator
5. find reachable common nodes in SED sets -- they dominate an SED set and 
are reachable from *that* set. Might as well assume it's an MSED set or SCC.
find minimum of nodes among MSED sets that minimize weight * (num-predecessors -1)
split along that node
6. go back to 1
"""

"""
idom->MSED
"""
