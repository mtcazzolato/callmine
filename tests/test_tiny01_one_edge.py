'''
Goal: unit test for static_graph.py
'''

import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# from static_graph.StaticGraph import StaticGraph
# from IDEAL_LAYOUT.static_graph import StaticGraph
# from static_graph import StaticGraph
import static_graph as SG

class TestStaticGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.tst = SG.StaticGraph(filename="tests/tiny01_one_edge.csv")
        self.df = self.tst.df_nodes
        self.df.set_index( SG.NODE_ID, inplace=True)

    def test_shape(self):
        n_rows = self.df.shape[0]
        n_columns = self.df.shape[1]
        self.assertEqual( n_rows, 2, "wrong # of rows")
        self.assertEqual( n_columns, 6, "wrong # of columns")

    def test_mary(self):
        mary_row = list( self.df.loc["mary"])
        assert mary_row == [0, 1, 1, 0, 23, 23]

    def test_peter(self):
        peter_row = list( self.df.loc["peter"])
        assert peter_row == [1, 0, 1, 23, 0, 23]


if __name__ == '__main__':

    # unittest.main()
    # the above is fine, but will give low verbosity

    # to control verbosity:
    t = unittest.TestLoader().loadTestsFromTestCase(TestStaticGraph)
    unittest.TextTestRunner(verbosity=2).run(t)
