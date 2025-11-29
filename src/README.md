# Data structures

We store graphs as a dictionary: 
```
node -> list[node]
```
All nodes are integers and the first node is zero.

All graphs are assumed connected. We assume nodes are integers.

Python dictionary keys are ordered (we are on Python 3.14). The first
key is the start node:

```
start, children = next(iter(my_dict.items())) // O(1) lookup
```
