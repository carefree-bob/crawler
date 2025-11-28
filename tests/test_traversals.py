import unittest
from src.lib.traversals import dfs_pre_order_traversal, dfs_reverse_post_order_traversal
from tests.test_data import graph_simple as gs

class MyTestCase(unittest.TestCase):
    def test_dfs(self):
        traversal = dfs_pre_order_traversal(gs.graph_6)
        self.assertEqual(traversal, (0, 1, 2, 3, 4))

    def test_dfs_post_order(self):
        traversal = dfs_reverse_post_order_traversal(gs.graph_6)
        self.assertEqual(traversal, (0, 1, 3, 4, 2))


if __name__ == '__main__':
    unittest.main()
