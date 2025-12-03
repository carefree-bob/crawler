import unittest
import tests.test_data.graph_simple as gs

class BaseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graphs = []
        for n in range(1, 9):
            cls.graphs.append(getattr(gs, f"graph_{n}"))


if __name__ == '__main__':
    unittest.main()
