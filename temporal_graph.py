# Goal: extract temporal features from nodes
#       wrt inter-arrival time and measure (duration)

import argparse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import entropy

np.seterr(divide='ignore', invalid='ignore')

# definition of expected column headers
SOURCE="source"
DESTINATION="destination"
MEASURE="measure"
TIMESTAMP="timestamp"

NODE_ID="node_ID"

# iat features
AVG_IAT="average_iat"
MAD_IAT="mad_iat"
MEDIAN_IAT="median_iat"
MIN_IAT="min_iat"
MAX_IAT="max_iat"
STD_IAT="std_iat"
QUANT25_IAT="quantile_25_iat"
QUANT50_IAT="quantile_50_iat"
QUANT75_IAT="quantile_75_iat"
ENTROPY_IAT="entropy_iat"

CALL_COUNT="call_count"

# measure/duration features
AVG_MEASURE="average_measure"
MAD_MEASURE="mad_measure"
MEDIAN_MEASURE="median_measure"
MIN_MEASURE="min_measure"
MAX_MEASURE="max_measure"
STD_MEASURE="std_measure"
QUANT25_MEASURE="quantile_25_measure"
QUANT50_MEASURE="quantile_50_measure"
QUANT75_MEASURE="quantile_75_measure"
ENTROPY_MEASURE="entropy_measure"
SUM_MEASURE="sum_measure"


class TemporalGraph():
    def __init__(self, filename):
        """
        extract temporal features from nodes: inter-arrival time (iat)
        and duration wrt the 'measure' attribute
        """
        self.filename = filename
        self.read_input_data()
        
        # get the set of all nodes (sources, and/or destinations)
        self.set_of_nodes = self.get_node_set()
        
        # start creating the output data frame, with one row per node
        self.df_nodes = pd.DataFrame(self.set_of_nodes)
        self.df_nodes.columns = [NODE_ID]

        # add columns with features, to the df_nodes dataframe
        self.graph2vec()
        
    def read_input_data(self):
        """
        read input data, with four required columns:
        source, destination, measure and timestamp
        """
        self.df = pd.read_csv(self.filename)
        self.headers = self.df.columns
        
        assert len(self.headers) == 4, "wrong # columns"
        assert self.headers[0] == SOURCE, "wrong header"
        assert self.headers[1] == DESTINATION, "wrong header"
        assert self.headers[2] == MEASURE, "wrong header"
        assert self.headers[3] == TIMESTAMP, "wrong header"
        
        self.headers = list(self.df.columns.values)
        
        self.df[MEASURE] = pd.to_numeric(self.df[MEASURE], errors='coerce')
        self.df.dropna(subset=[MEASURE])
        self.df = self.df[self.df[SOURCE] != self.df[DESTINATION]]
        self.df = self.df[self.df[MEASURE] > 0]
        
        self.df[TIMESTAMP] = self.df[TIMESTAMP].astype('datetime64[s]')
        
    def get_node_set(self):
        """
        gives the set of nodes (union of sources AND destinations)
        """
        set_of_unique_sources = set(self.df[SOURCE].unique())
        set_of_unique_destinations = set(self.df[DESTINATION].unique())
        set_nodes = set(set_of_unique_sources | set_of_unique_destinations)
        
        return(set_nodes)
    
    def graph2vec(self):
        """
        call functions to extract in and out features
        """
        self.get_in_features()
        self.get_out_features()
        
    def fill_features(self, node_direction=SOURCE, prefix='out_'):
        """
        extract in/out features of iat from TIMESTAMP column,
        grouped by SOURCE or DESTINATION
        populate df_nodes with iat features per node
        """
        # First: sort elements by source and timestamp
        df_aux = self.df.sort_values(by=[node_direction, TIMESTAMP]).reset_index(drop=True)

        # Group by source, get the difference (iat) between ts of every hash, convert it to timedelta
        df_aux['diff_ts'] = df_aux.groupby(by=[node_direction])[TIMESTAMP].diff().astype("timedelta64[s]")

        # Creates groups by ahash values, get the iat for every row
        group = df_aux.groupby(by=[node_direction], axis=0)['diff_ts']

        # Aggregate iat per group/hash
        df_iat_measure = pd.DataFrame()
        df_iat_measure[prefix+AVG_IAT]     = group.mean()
        df_iat_measure[prefix+MAD_IAT]     = group.mad()
        df_iat_measure[prefix+MEDIAN_IAT]  = group.median()
        df_iat_measure[prefix+STD_IAT]     = group.std(ddof=0)
        df_iat_measure[prefix+MIN_IAT]     = group.min()
        df_iat_measure[prefix+MAX_IAT]     = group.max()
        df_iat_measure[prefix+QUANT25_IAT] = group.quantile(q=0.25)
        df_iat_measure[prefix+QUANT50_IAT] = group.quantile(q=0.5)
        df_iat_measure[prefix+QUANT75_IAT] = group.quantile(q=0.75)
        df_iat_measure[prefix+ENTROPY_IAT]     = group.apply(lambda x : entropy(x.dropna().values))
        df_iat_measure[prefix+CALL_COUNT]  = group.size()
        
        # Creates groups by ahash values, get the duration of every row
        group = df_aux.groupby(by=[node_direction], axis=0)[MEASURE]
        
        df_iat_measure[prefix+AVG_MEASURE]     = group.mean()
        df_iat_measure[prefix+MAD_MEASURE]     = group.mad()
        df_iat_measure[prefix+MEDIAN_MEASURE]  = group.median()
        df_iat_measure[prefix+STD_MEASURE]     = group.std(ddof=0)
        df_iat_measure[prefix+MIN_MEASURE]     = group.min()
        df_iat_measure[prefix+MAX_MEASURE]     = group.max()
        df_iat_measure[prefix+QUANT25_MEASURE] = group.quantile(q=0.25)
        df_iat_measure[prefix+QUANT50_MEASURE] = group.quantile(q=0.5)
        df_iat_measure[prefix+QUANT75_MEASURE] = group.quantile(q=0.75)
        df_iat_measure[prefix+ENTROPY_MEASURE] = group.apply(lambda x : entropy(x.dropna().values))
        df_iat_measure[prefix+SUM_MEASURE]     = group.sum()

        df_iat_measure.reset_index(inplace=True)
        self.df_nodes = self.df_nodes.merge(df_iat_measure, left_on=NODE_ID, right_on=node_direction, how='left')
        self.df_nodes = self.df_nodes.drop(columns=[node_direction])
        self.df_nodes = self.df_nodes.fillna(0)
    
    def get_in_features(self):
        """
        extract features from the destination nodes
        """
        self.fill_features(node_direction=DESTINATION, prefix='in_')

    def get_out_features(self):
        """
        extract features from the source nodes
        """
        self.fill_features(node_direction=SOURCE, prefix='out_')
    
    def my_print(self):
        """
        for debugging - just prints the pandas frames
        :return:
        """
        print("")
        print("---- echoing the input ----")
        print(self.df)

        print("\n")
        print("---- RESULT (placeholder): data frame  of nodes -------------")
        print(self.df_nodes)
        print(self.df_nodes.values)
        
    def print_to_csv(self, out_file_name):
        """
        prints the df_nodes dataframe as a csv file,
        ready for nd_cloud processing
        :param out_file_name:
        :return:
        """
        self.df_nodes.to_csv(out_file_name, index=False)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="analysis for temporal graphs")
    parser.add_argument("-v", "--verbose",
                        help="level of verbosity (-v [-v ...])",
                        action="count",
                        default=0)
    parser.add_argument("filename", help="input file csv[.gz]")

    args = parser.parse_args()
    verbose = args.verbose
    filename = args.filename

    print('----- Working on ' + filename + "------")

    if verbose > 0:
        print("    *** verbose = ", verbose)
        print("    *** filename = ", filename)

    tg = TemporalGraph(filename)
    tg.my_print()

    if verbose > 1:
        print("\n\n ----")
        tg.print_to_csv("t_nodeVectors.csv")
        print(" check the file t_nodeVectors.csv ")

    print("---------------")

