'''
Goal: unit test for nd_cloud_labeled.py
'''

import unittest
import sys
import os

# 'out_degree', 'in_degree', 'core', 'weighted_out_degree', 'weighted_in_degree', 'weighted_degree'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import nd_cloud_labeled as NDC

class TestNdCloudLabeled(unittest.TestCase):
    def setUp(self) -> None:
        self.tst = NDC.nd_cloud_labeled(filename="tests/ndc_labeled_inputs/ndcl01_one_edge.csv",
                                        filename_label="tests/ndc_labeled_inputs/ndcl01_one_edge_label.csv")
        self.df = self.tst.df
        self.df.set_index(NDC.NODE_ID, inplace=True)
        self.df_label = self.tst.df_label
        self.df_label.set_index(NDC.NODE_ID, inplace=True)

    def test_shape_data(self):
        n_rows = self.df.shape[0]
        n_columns = self.df.shape[1]
        self.assertEqual(n_rows, 2, "wrong # of rows")
        self.assertEqual(n_columns, 6, "wrong # of columns")

    def test_shape_data_label(self):
        n_rows = self.df_label.shape[0]
        n_columns = self.df_label.shape[1]
        self.assertEqual(n_rows, 2, "wrong # of rows")
        self.assertEqual(n_columns, 1, "wrong # of columns")

    def test_mary(self):
        mary_row = list(self.df.loc["mary"])
        self.assertEqual(mary_row, [0, 1, 1, 0, 23, 23])

    def test_peter(self):
        peter_row = list(self.df.loc["peter"])
        self.assertEqual(peter_row, [1, 0, 1, 23, 0, 23])

    def test_mary_label(self):
        mary_row_label= list(self.df_label.loc["mary"])
        self.assertEqual(mary_row_label, ["a"])

    def test_peter_label(self):
        peter_row_label = list(self.df_label.loc["peter"])
        self.assertEqual(peter_row_label, ["b"])
    
    def test_label_order(self):
        node_index_order = list(self.df.index.values)
        label_index_order = list(self.df_label.index.values)
        self.assertEqual(node_index_order, label_index_order)

    def test_label_index_mary(self):
        label_index_a = list(self.tst.get_label_indexes("a"))
        self.assertEqual(label_index_a, [0])
    
    def test_label_index_peter(self):
        label_index_b = list(self.tst.get_label_indexes("b"))
        self.assertEqual(label_index_b, [1])

if __name__ == '__main__':
    # unittest.main()
    # the above is fine, but will give low verbosity

    # to control verbosity:
    t = unittest.TestLoader().loadTestsFromTestCase(TestNdCloudLabeled)
    unittest.TextTestRunner(verbosity=2).run(t)
