import unittest

import networkx as nx

from src.lib.lengauer_tarjan import init_lt, gen_lt_graph
from tests.base_test import BaseCase
from tests.helper import g_to_nx

"""
Small unit tests to catch errors when initializing l-t data structures for pre-order traversals
"""

class TestInit(BaseCase):
    def test_init_lt_simple1(self):
        g = {0: [1,2], 1: [], 2: []}
        lt_g, pre, rev = init_lt(g)
        self.assertEqual(lt_g, {
            0: {'anc': None, 'best': 0, 'bucket': [],
                'idom': None, 'parent': None, 'pre': 0,
                'preds': [], 'semi': 0, 'succs': [1, 2]
                },
            1: {'anc': None, 'best': 1, 'bucket': [],
                'idom': None, 'parent': 0, 'pre': 1,
                'preds': [0], 'semi': 1, 'succs': []
                },
            2: {'anc': None, 'best': 2, 'bucket': [],
                'idom': None, 'parent': 0, 'pre': 2,
                'preds': [0], 'semi': 2, 'succs': []
                }
        })

    def test_init_lt_simple2(self):
        """
                    0
                1---+---2
                 \      |
                  \     |
                   +-- 3

        pre-order traversal: 0, 1, 3, 2

        relabelled graph:

                    0
                1---+---3
                 \      |
                  \     Y
                   +-> 2
        should have preds: 2 = 1, 3, preds 1 = 0, preds 3 = 0
        parent: 2 = 1 (pre-order parent)
        successor 3: 2, successor 1: 2, successor 0: 1, 3

        """
        g = {0: [1, 2], 1: [3], 2:[3], 3:[]}
        lt_g0, pre0, rev0 = init_lt(g)
        self.assertEqual(lt_g0,{
            0: {'anc': None, 'best': 0, 'bucket': [], 'idom': None, 'parent': None, 'pre': 0, 'preds': [], 'semi': 0, 'succs': [1, 3]
                },
            1: {'anc': None, 'best': 1, 'bucket': [], 'idom': None, 'parent': 0, 'pre': 1, 'preds': [0], 'semi': 1, 'succs': [2]
                },
            2: {'anc': None, 'best': 2, 'bucket': [], 'idom': None, 'parent': 1, 'pre': 2, 'preds': [1, 3], 'semi': 2, 'succs': []
                },
            3: {'anc': None, 'best': 3, 'bucket': [], 'idom': None, 'parent': 0, 'pre': 3, 'preds': [0], 'semi': 3, 'succs': [2]
                }
        })

    def test_init_lt_simple3(self):
        g = {0: [1, 2], 1: [4], 2:[3, 4, 0], 3: [], 4: [0]}
        lt_g0, pre0, rev0 = init_lt(g)
        self.assertEqual(lt_g0, {
            0: {'anc': None, 'best': 0, 'bucket': [],
                'idom': None, 'parent': None, 'pre': 0,
                'preds': [3, 2], 'semi': 0, 'succs': [1, 3]
                },
            1: {'anc': None, 'best': 1, 'bucket': [],
                'idom': None, 'parent': 0, 'pre': 1,
                'preds': [0], 'semi': 1, 'succs': [2]
                },
            2: {'anc': None, 'best': 2, 'bucket': [],
                'idom': None, 'parent': 1, 'pre': 2,
                'preds': [1, 3], 'semi': 2, 'succs': [0]
                },
            3: {'anc': None, 'best': 3, 'bucket': [],
                'idom': None, 'parent': 0, 'pre': 3,
                'preds': [0], 'semi': 3, 'succs': [4, 2, 0]
                },
            4: {'anc': None, 'best': 4, 'bucket': [],
                'idom': None, 'parent': 3, 'pre': 4,
                'preds': [3], 'semi': 4, 'succs': []
                }
        })

    def test_simple_bug2(self):
        g = {0:[1], 1:[2], 2:[3,4], 3:[4], 4:[5], 5:[4]}
        lt_g0, pre0, rev0 = init_lt(g)
        self.assertEqual(lt_g0, {
            0: {'anc': None, 'best': 0, 'bucket': [], 'idom': None, 'parent': None, 'pre': 0, 'preds': [], 'semi': 0, 'succs': [1]
                },
            1: {'anc': None, 'best': 1, 'bucket': [], 'idom': None, 'parent': 0, 'pre': 1, 'preds': [0], 'semi': 1, 'succs': [2]
                },
            2: {'anc': None, 'best': 2, 'bucket': [], 'idom': None, 'parent': 1, 'pre': 2, 'preds': [1], 'semi': 2, 'succs': [3, 4]
                },
            3: {'anc': None, 'best': 3, 'bucket': [], 'idom': None, 'parent': 2, 'pre': 3, 'preds': [2], 'semi': 3, 'succs': [4]
                },
            4: {'anc': None, 'best': 4, 'bucket': [], 'idom': None, 'parent': 3, 'pre': 4, 'preds': [2, 3, 5], 'semi': 4, 'succs': [5]
                },
            5: {'anc': None, 'best': 5, 'bucket': [], 'idom': None, 'parent': 4, 'pre': 5, 'preds': [4], 'semi': 5, 'succs': [4]}
        })

class TestExamples(BaseCase):

    def test_lt_with_examples(self):
        for i, g in enumerate(self.graphs):
            # print(f"graph {i}")
            start, _ = next(iter(g.items()))
            nx_g = g_to_nx(g)
            graph, pre, rev = gen_lt_graph(g)
            idoms_ours = {rev[idx]: rev[node["idom"]] for idx, node in graph.items() if node["idom"] is not None }

            idoms_nx = nx.immediate_dominators(nx_g, start=start)
            self.assertEqual(idoms_ours, idoms_nx)


if __name__ == '__main__':
    unittest.main()
