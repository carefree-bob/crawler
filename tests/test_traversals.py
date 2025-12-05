import unittest

from src.lib.graph_utils import dfs_pre_order_traversal, dfs_post_order_traversal
from tests.base_test import BaseCase
from tests.helper import get_nx_post_order, get_nx_pre_order


class TestTraversals(BaseCase):

    def test_pre_order(self):
        for g in self.graphs:
            traversal_ours = dfs_pre_order_traversal(g)
            traversal_nx = get_nx_pre_order(g)
            self.assertEqual(traversal_nx, traversal_ours)

    def test_post_order(self):
        for g in self.graphs:
            traversal_ours = dfs_post_order_traversal(g)
            traversal_nx = get_nx_post_order(g)
            self.assertEqual(traversal_nx, traversal_ours)


if __name__ == '__main__':
    unittest.main()
