import unittest
import networkx as nx
from tests.helper import g_to_nx
from src.lib.tarjan_scc import get_tarjan_scc
from tests.base_test import BaseCase

class MyTestCase(BaseCase):

    def test_tarjan_scc(self):
        for g in self.graphs:
            scc_ours = get_tarjan_scc(g)
            scc_nx = list(nx.strongly_connected_components(g_to_nx(g)))
            # since our code is just a port of nx this should always be true
            self.assertEqual(scc_nx, scc_ours)  # add assertion here


if __name__ == '__main__':
    unittest.main()
