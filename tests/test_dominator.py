import unittest

from src.lib.dominator import get_dominator_tree, get_dominance_frontier
from tests.base_test import BaseCase
from tests.helper import get_dominator_tree_via_nx, get_dominance_frontier_via_nx


def sort_dict(d:dict)->dict:
    return {k: sorted(val) for (k, val) in d.items()}

class TestDominator(BaseCase):

    def test_get_dominator_tree(self):
        for g in self.graphs:
            d_ours = get_dominator_tree(g)
            d_nx = get_dominator_tree_via_nx(g)

            self.assertEqual(sort_dict(d_nx), sort_dict(d_ours))

    def test_get_dominance_frontier(self):
        for i, g in enumerate(self.graphs):
            print(f"graph {i}")
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
