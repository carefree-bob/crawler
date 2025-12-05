import unittest
import tests.test_data.graph_simple as gs

class BaseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graphs = gs.graphs


if __name__ == '__main__':
    unittest.main()
