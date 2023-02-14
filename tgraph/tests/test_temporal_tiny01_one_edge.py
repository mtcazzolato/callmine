'''
Goal: unit test for temporal_graph.py
'''

import unittest
import sys
import os

# 'in_average_iat', 'in_mad_iat', 'in_median_iat', 'in_std_iat', 'in_min_iat', 'in_max_iat',
# 'in_quantile_25_iat', 'in_quantile_50_iat', 'in_quantile_75_iat', 'in_entropy_iat', 'in_call_count',

# 'in_average_measure', 'in_mad_measure', 'in_median_measure', 'in_std_measure', 'in_min_measure', 'in_max_measure',
# 'in_quantile_25_measure', 'in_quantile_50_measure', 'in_quantile_75_measure', 'in_entropy_measure', 'in_sum_measure'

# 'out_average_iat', 'out_mad_iat', 'out_median_iat', 'out_std_iat', 'out_min_iat', 'out_max_iat',
# 'out_quantile_25_iat', 'out_quantile_50_iat', 'out_quantile_75_iat', 'out_entropy_iat', 'out_call_count'

# 'out_average_measure', 'out_mad_measure', 'out_median_measure', 'out_std_measure', 'out_min_measure', 'out_max_measure',
# 'out_quantile_25_measure', 'out_quantile_50_measure', 'out_quantile_75_measure', 'out_entropy_measure', 'out_sum_measure'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import temporal_graph as TG

class TestTemporalGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.tst = TG.TemporalGraph(filename="tgraph/tests/temporal_graph_inputs/tiny01_one_edge_temporal.csv")
        self.df = self.tst.df_nodes
        self.df.set_index(TG.NODE_ID, inplace=True)

    def test_shape(self):
        n_rows = self.df.shape[0]
        n_columns = self.df.shape[1]
        self.assertEqual(n_rows, 2, "wrong # of rows")
        self.assertEqual(n_columns, 44, "wrong # of columns")

    def test_mary(self):
        mary_row = list(self.df.loc["mary"])
        self.assertEqual(mary_row,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                          23, 0, 23, 0, 23, 23, 23, 23, 23, 0, 23,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         "wrong Mary\'s information")

    def test_peter(self):
        peter_row = list(self.df.loc["peter"])
        self.assertEqual(peter_row,
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                          23, 0, 23, 0, 23, 23, 23, 23, 23, 0, 23],
                         "wrong Peter\'s information")

if __name__ == '__main__':

    # unittest.main()
    # the above is fine, but will give low verbosity

    # to control verbosity:
    t = unittest.TestLoader().loadTestsFromTestCase(TestTemporalGraph)
    unittest.TextTestRunner(verbosity=2).run(t)
