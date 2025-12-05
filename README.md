# Some Graph Algorithms for Crawlers

Python implementation of graph traversal algorithms useful for symbolic execution:

* Lengauer-Tarjan for finding immediate dominators
* Tarjan SCC finding algorithm
* Hecht-Ullman T1/T2 analysis
* Janssen's controlled node splitting heuristic (not optimal)

All of these algorithms can be found in many places online, the networkx project is an excellent source for python graph algorithms. However, I wanted a self-contained test environment to benchmark different crawling algorithms without any third party dependencies. 
