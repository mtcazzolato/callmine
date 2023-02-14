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
        self.tst = TG.TemporalGraph(filename="tgraph/tests/temporal_graph_inputs/abcde01_temporal.csv")
        self.df = self.tst.df_nodes
        self.df.set_index( TG.NODE_ID, inplace=True)

    def test_shape(self):
        n_rows = self.df.shape[0]
        n_columns = self.df.shape[1]
        self.assertEqual( n_rows, 5, "wrong # of rows")
        self.assertEqual( n_columns, 44, "wrong # of columns")

    def test_a(self):
        a_row = list(self.df.loc["a"])
        a_actual_values = [737636, 595259, 737636, 595259, 142377, 1332895, 440006.5, 737636, 1035265.5, 0.3173, 3,
                           4, 0.6667, 4, 0.8165, 3, 5, 3.5, 4, 4.5, 1.0776, 12,
                           339846.2857, 221996.898, 246947, 245228.7177, 600, 749193, 167424.5, 246947, 523667.5, 1.6385, 8,
                           3.125, 0.90625, 3, 1.0532, 2, 5, 2, 3, 4, 2.0234, 25]
        
        for exp_v, actual_v in zip(a_row, a_actual_values):
            self.assertAlmostEqual(exp_v, actual_v, places=2, msg="wrong information for node \'a\'")

    def test_b(self):
        b_row = list(self.df.loc["b"])
        b_actual_values = [968340, 79595, 968340, 79595, 888745, 1047935, 
                           928542.5, 968340, 1008137.5, 0.6898, 3,
                           2, 0, 2, 0, 2, 2, 2, 2, 2, 1.0986, 6,
                           737636, 595259, 737636, 595259, 142377, 1332895, 440006.5,
                           737636, 1035265.5, 0.3173, 3,
                           4, 0.6667, 4, 0.8165, 3, 5, 3.5, 4, 4.5, 1.0776, 12]
        
        for exp_v, actual_v in zip(b_row, b_actual_values):
            self.assertAlmostEqual(exp_v,
                                   actual_v,
                                   places=2,
                                   msg="wrong information for node \'b\'")
    
    def test_c(self):
        c_row = list(self.df.loc["c"])
        c_actual_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                           4, 0, 4, 0, 4, 4, 4, 4, 4, 0, 4,
                           529766.6667, 409222.2222, 445700, 470641.862, 0, 1143600,
                           222850, 445700, 794650, 0.5934, 4,
                           2.25, 0.875, 2, 1.09, 1, 4, 1.75, 2, 2.5, 1.273, 9]
        
        for exp_v, actual_v in zip(c_row, c_actual_values):
            self.assertAlmostEqual(exp_v,
                                   actual_v,
                                   places=2,
                                   msg="wrong information for node \'c\'")
    
    def test_d(self):
        d_row = list(self.df.loc["d"])
        d_actual_values = [608528, 196248, 681984, 216682.9769, 314156, 829444,
                           498070, 681984, 755714, 1.03, 4,
                           3.25, 1.25, 3, 1.3, 2, 5, 2, 3, 4.25, 1.306, 13,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                           2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 2]
        
        for exp_v, actual_v in zip(d_row, d_actual_values):
            self.assertAlmostEqual(exp_v,
                                   actual_v,
                                   places=2,
                                   msg="wrong information for node \'d\'")
    
    def test_e(self):
        e_row = list(self.df.loc["e"])
        e_actual_values = [594581, 452709.5, 433830.5, 550551.5766, 10663, 1500000,
                           327133.75, 433830.5, 701277.75, 0.9357, 5,
                           2.6, 0.88, 3, 1.02, 1, 4, 2, 3, 3, 1.5245, 13,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        for exp_v, actual_v in zip(e_row, e_actual_values):
            self.assertAlmostEqual(exp_v,
                                   actual_v,
                                   places=2,
                                   msg="wrong information for node \'e\'")

if __name__ == '__main__':

    # unittest.main()
    # the above is fine, but will give low verbosity

    # to control verbosity:
    t = unittest.TestLoader().loadTestsFromTestCase(TestTemporalGraph)
    unittest.TextTestRunner(verbosity=2).run(t)
