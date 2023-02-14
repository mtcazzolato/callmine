# Goal: Join feature files produced by static_graph and temporal_graph
# into a single file with all features (joined by column NODE_ID)
# =======================================================================

import argparse
import pandas as pd

NODE_ID="node_ID"

class JoinFeatures():
    def __init__(self, path_static, path_temporal):
        """
        join features from classes static_graph and temporal_graph
        saves a new files with all features joined by NODE_ID
        """
        
        df_static = pd.read_csv(path_static)
        df_temporal = pd.read_csv(path_temporal)

        self.df_all = df_static.set_index(NODE_ID).join(df_temporal.set_index(NODE_ID)).reset_index()
        self.df_all.fillna(0)

    def print_to_csv(self, out_file_name):
        """
        prints the dataframe with all features as a csv file,
        ready for nd_cloud processing
        :param out_file_name:
        :return:
        """
        self.df_all.to_csv(out_file_name, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Joining static and temporal features.')
    parser.add_argument("-v", "--verbose",
                        help="level of verbosity (-v [-v ...])",
                        action="count",
                        default=0)
    parser.add_argument('path_static_file',
                        help='input file with static features csv')
    parser.add_argument('path_temporal_file',
                        help='input file with temporal features csv')

    args = parser.parse_args()
    
    verbose=args.verbose
    path_static = args.path_static_file
    path_temporal = args.path_temporal_file

    jf = JoinFeatures(path_static, path_temporal)

    if verbose > 0:
        print("\n\n ----")
        jf.print_to_csv("allFeatures_nodeVectors.csv")
        print(" check the file allFeatures_nodeVectors.csv ")
    
    print("---------------")
