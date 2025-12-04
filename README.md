# Some Graph Algorithms for Crawlers

Python implementation of graph traversal algorithms useful for symbolic execution:

* Lengauer-Tarjan for finding immediate dominators
* Tarjan SCC finding algorithm
* Hecht-Ullman T1/T2 analysis
* Janssen's controlled node splitting heuristic (not optimal)

All of these algorithms can be found in many places online, the networkx project is an excellent source for python graph algorithms. However, I wanted a self-contained test environment to benchmark different crawling models without any third party dependencies. 

The main model presented here is to 
1) perform T1/T2 reduction combined with Janssen's node splitting in order to reduce a graph to a single "fat" node
2) Unroll the fat node to obtain a crawl plan for the graph.

I am unaware of any existing python implementation of Janssen's node splitting heuristic.

Any crawl plan has to decide on how to deal with loops. A simple approach is to traverse each loop only once, although there are numerous more sophisticated approaches depending on the analysis being performed. Here, I mark the loops and the in the example implementation crawl each loop a fixed number of times. 











