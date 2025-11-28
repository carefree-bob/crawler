# Data structures

We store graphs as a dictionary: 
```
node -> tuple[node, ...]
```
All nodes are integers and the first node is zero.

traversals and crawls are both tuples of nodes (integers):

```
depth_first_search(graph: dict[int,tuple[int, ...]])->tuple[int, ...]:
```

representing the parent -> child relationship

All graphs are assumed connected. We assume nodes are integers.

Python dictionary keys are ordered (we are on Python 3.14). The first
key is the start node:

```
0, children = start, children = next(iter(my_dict.items())) // O(1) lookup
```

Although we don't want to be gratuitously slow, this is python and the goal of the project is to explore suitability of various approaches in a rapid application development environment.