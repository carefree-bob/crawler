import unittest
import tests.test_data.graph_simple as gs
from tests.helper import validate


class BaseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graphs = gs.graphs
        for g in gs.graphs:
            validate(g)


if __name__ == '__main__':
    unittest.main()
