import unittest
from src.lib.dominator import get_dominator_tree, get_dominance_frontier
from tests.test_data import graph_simple as gs
from tests.helper import get_dominator_tree_via_nx, get_dominance_frontier_via_nx



def sort_dict(d:dict)->dict:
    return {k: sorted(val) for (k, val) in d.items()}

class TestDominator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graphs = []
        for n in range(1,9):
            cls.graphs.append(getattr(gs, f"graph_{n}"))

    def test_get_dominator_tree(self):
        for g in self.graphs:
            d_ours = get_dominator_tree(g)
            d_nx = get_dominator_tree_via_nx(g)

            self.assertEqual(sort_dict(d_nx), sort_dict(d_ours))

    def test_get_dominance_frontier(self):
        for g in self.graphs:
            df_ours = get_dominance_frontier(g)
            df_nx = get_dominance_frontier_via_nx(g)
            print(f"g is {g}")
            self.assertEqual(sort_dict(df_nx), sort_dict(df_ours))

    def test_get_dominance_frontier_root(self):
        g = {
            0:[1],
            1:[0,2],
            2:[]
             }
        df_ours = get_dominance_frontier(g)
        df_nx = get_dominance_frontier_via_nx(g)
        print(f"g is {g}")
        self.assertEqual(sort_dict(df_nx), sort_dict(df_ours))

if __name__ == '__main__':
    unittest.main()
