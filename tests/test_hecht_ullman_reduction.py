import copy
import unittest

from src.lib.crawler_type import Reduce
from src.lib.graph_utils import get_preds
from src.lib.hecht_ullman_reduction import init_t1t2, get_reduced_graph, recover_orig_data
from tests.base_test import BaseCase
from tests.helper import g_to_nx, sort_dict


class TestHechtUllman(BaseCase):
    def test_init(self):
        for g in self.graphs:
            data = init_t1t2(g)
            nx_g = g_to_nx(g)
            preds = {node: list(nx_g.predecessors(node)) for node, _ in g.items()}

            self.assertEqual({
                "start": next(iter(g.keys())),
                "graph": g, "preds": preds,
                "weights": {n:1 for n, _ in g.items()}, "log": []
            }, data)  # add assertion here

    def test_reduce_trivial(self):
        g = {0:[]}
        data = get_reduced_graph(g)
        self.assertEqual({
            'start': 0,
            'graph': {0: []},
            'log': [],
            'preds': {0: []},
            'weights': {0: 1}
        }, data)

    def test_reduce_t1_single(self):
        g = {0:[0]}
        data = get_reduced_graph(g)
        self.assertEqual({
            'start': 0,
            'graph': {0: []},
            'log': [(Reduce.T1, 0, (), (), (0,), (0,), 1)],
            'preds': {0: []},
            'weights': {0: 1}
        }, data)

    def test_reduce_t2_single(self):
        g = {0:[1], 1:[]}
        data = get_reduced_graph(g)
        self.assertEqual({
            'start': 0,
            'graph': {0: []},
            'log': [(Reduce.T2, 1, (1,), (), (), (0,), 1)],
            'preds': {0: []},
            'weights': {0: 2}
        }, data)

    def test_reduce_t2_double(self):
        g = {0:[1], 1:[2], 2:[]}
        data = get_reduced_graph(g)
        self.assertEqual({
            'start': 0,
            'graph': {0: []},
            'log': [(Reduce.T2, 1, (1,), (), (2,), (0,), 1),
                    (Reduce.T2, 2, (2,), (), (), (0,), 1)],
            'preds': {0: []},
            'weights': {0: 3}
        }, data)

    def test_reduce_cycle(self):
        g = {0:[1], 1:[0]}
        data = get_reduced_graph(g)
        self.assertEqual(
            {'start': 0,
                'graph': {0: []},
                'log': [
                (Reduce.T2, 1, (1,), (1, ), (0,), (0,), 1),
                (Reduce.T1, 0, (), (), (0,), (0,), 2)],
             'preds': {0: []},
             'weights': {0: 2}
             }, data)

    def test_simple_graphs_weights(self):
        for g in self.graphs:
            data = get_reduced_graph(g)
            self.assertEqual(sum(data["weights"].values()), len(g))

    def test_simple_graphs_preds(self):
        # check that predecessors are correctly generated
        for i, g in enumerate(self.graphs):
            data = get_reduced_graph(g)
            preds = data["preds"]
            graph = data["graph"]
            exp_preds = get_preds(graph)
            self.assertEqual(sort_dict(exp_preds), sort_dict(preds))

    def test_simple_graph_reversible(self):
        for i, g in enumerate(self.graphs):
            h = copy.deepcopy(g)
            data = get_reduced_graph(g)
            data_recover = recover_orig_data(data)

            # check that we have not mutated g
            self.assertEqual(g, h)
            self.assertEqual(sort_dict(g), sort_dict(data_recover["graph"]))
            self.assertEqual(data_recover["log"], [])
            self.assertEqual(sort_dict(data), sort_dict(data_recover))


if __name__ == '__main__':
    unittest.main()
