'''
Goal: unit test for merging static and temporal feature files
'''

import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import static_graph as SG
import temporal_graph as TG
import join_feature_files as JF

class TestFeatureMerging(unittest.TestCase):
    def setUp(self) -> None:
        self.tst_s = SG.StaticGraph(filename="tests/temporal_graph_inputs/abcde01_temporal.csv")
        self.tst_s.print_to_csv("TEMP_nodeVectors.csv")

        self.tst_t = TG.TemporalGraph(filename="tests/temporal_graph_inputs/abcde01_temporal.csv")
        self.tst_t.print_to_csv("TEMP_t_nodeVectors.csv")

        self.jf = JF.JoinFeatures("TEMP_nodeVectors.csv", "TEMP_t_nodeVectors.csv")
        self.df_all = self.jf.df_all
        
        self.df_all.set_index( TG.NODE_ID, inplace=True)

        # delete temporary files
        try:
            os.remove("TEMP_nodeVectors.csv")
            os.remove("TEMP_t_nodeVectors.csv")
        except:
            pass

    def test_shape(self):
        n_rows = self.df_all.shape[0]
        n_columns = self.df_all.shape[1]
        self.assertEqual( n_rows, 5, "wrong # of rows")
        self.assertEqual( n_columns, 50, "wrong # of columns")

    def test_a(self):
        a_row = list(self.df_all.loc["a"])
        a_actual_values = [4,1,2,25,12,37,
                           737636, 595259, 737636, 595259, 142377, 1332895, 440006.5, 737636, 1035265.5, 0.3173, 3,
                           4, 0.6667, 4, 0.8165, 3, 5, 3.5, 4, 4.5, 1.0776, 12,
                           339846.2857, 221996.898, 246947, 245228.7177, 600, 749193, 167424.5, 246947, 523667.5, 1.6385, 8,
                           3.125, 0.90625, 3, 1.0532, 2, 5, 2, 3, 4, 2.0234, 25]
        
        for exp_v, actual_v in zip(a_row, a_actual_values):
            self.assertAlmostEqual(exp_v, actual_v, places=2, msg="wrong information for node \'a\'")

    def test_b(self):
        b_row = list(self.df_all.loc["b"])
        b_actual_values = [1, 2, 2, 12, 6, 18,
                           968340, 79595, 968340, 79595, 888745, 1047935,
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
        c_row = list(self.df_all.loc["c"])
        c_actual_values = [2, 1, 2, 9, 4, 13,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
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
        d_row = list(self.df_all.loc["d"])
        d_actual_values = [1,2,2,2,13,15,
                           608528, 196248, 681984, 216682.9769, 314156, 829444,
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
        e_row = list(self.df_all.loc["e"])
        e_actual_values = [0,2,2,0,13,13,
                           594581, 452709.5, 433830.5, 550551.5766, 10663, 1500000,
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
    t = unittest.TestLoader().loadTestsFromTestCase(TestFeatureMerging)
    unittest.TextTestRunner(verbosity=2).run(t)
