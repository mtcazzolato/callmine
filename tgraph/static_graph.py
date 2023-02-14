# Goal: 
#	- read a something like the 'tiny_graph.csv'
#	- extract features into, say, 'feature.csv'
#	- and generate several plots, outliers, etc

import sys
import pandas as pd
import argparse
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# definition of expected column headers
SOURCE="source"
DESTINATION="destination"
MEASURE="measure"

NODE_ID = "node_ID"
OUT_DEGREE = "out_degree"
IN_DEGREE = "in_degree"
WEIGHTED_OUT_DEGREE = "weighted_out_degree"
WEIGHTED_IN_DEGREE = "weighted_in_degree"
WEIGHTED_DEGREE = "weighted_degree"
CORE = "core"

class StaticGraph():

    def __init__(self, filename):
        """
        expects a filename (csv, 3 columns, with the right headers)
        and builds the output data frame, with nodes and their features
        :param filename:
        """
        self.filename = filename
        
        self.df = pd.read_csv(filename, usecols=[SOURCE, DESTINATION, MEASURE])
        self.headers = list(self.df.columns.values)

        assert len(self.headers) == 3, "wrong # columns"
        
        assert self.headers[0] == SOURCE, "wrong header"
        assert self.headers[1] == DESTINATION, "wrong header"
        assert self.headers[2] == MEASURE, "wrong header"
        
        self.df[MEASURE] = pd.to_numeric(self.df[MEASURE], errors='coerce')
        self.df.dropna(subset=[MEASURE])
        self.df = self.df[self.df[SOURCE] != self.df[DESTINATION]]
        self.df = self.df[self.df[MEASURE] > 0]
        self.df = self.df.groupby([SOURCE, DESTINATION]).sum().add_suffix('').reset_index()

        # get the set of all nodes (sources, and/or destinations)
        self.set_of_nodes = self.get_node_set()

        # start creating the output data frame, with one row per node
        self.df_nodes = pd.DataFrame(self.set_of_nodes)
        self.df_nodes.columns = [NODE_ID]

        # add columns with features, to the df_nodes dataframe
        self.graph2vec()

    def get_node_set(self):
        """
        gives the set of nodes (union of sources AND destinations)
        """
        set_of_unique_sources = set( self.df[SOURCE].unique())
        set_of_unique_destinations = set(self.df[DESTINATION].unique())
        set_nodes = set( set_of_unique_sources |set_of_unique_destinations)
        return(set_nodes)

    def graph2vec(self):
        """
        given the input graph
        compute numerical features for each node
        (like in-degree, out-degree, in-weight, etc)
        and add those columns to the df_nodes data frame
        :return:
        """
        G = nx.from_pandas_edgelist(self.df, source=SOURCE, target=DESTINATION, create_using=nx.DiGraph())
        self.fill_out_degree(G) 
        self.fill_in_degree(G)
        self.fill_main_core(G)

        WG = nx.from_pandas_edgelist(self.df, source=SOURCE, target=DESTINATION, create_using=nx.DiGraph(), edge_attr=MEASURE)
        self.fill_weighted_out_degree(WG) 
        self.fill_weighted_in_degree(WG)
        self.fill_weighted_degree(WG)

        if False:
            print(self.df_nodes)

    def fill_out_degree(self, G):
        """
        for each node in the node_set, computes the out-degree
        and adds the column to the df_nodes dataframe
        :return:
        """
        
        out_degs = [(node, val) for (node, val) in G.out_degree()] #type is list 
        out_degs_df = pd.DataFrame(out_degs, columns=[SOURCE, OUT_DEGREE])
        self.df_nodes = self.df_nodes.merge(out_degs_df, left_on=NODE_ID, right_on=SOURCE,how='left')
        self.df_nodes = self.df_nodes.drop(columns=[SOURCE])


    def fill_in_degree(self, G):
    #     """
    #     for each node in node_set, compute in-degree
    #     and adds the column to the df_nodes data frame
    #     :return:
    #     """

        in_degs = [(node, val) for (node, val) in G.in_degree()]
        in_degs_df = pd.DataFrame(in_degs, columns=[SOURCE, IN_DEGREE])
        self.df_nodes = self.df_nodes.merge(in_degs_df, left_on=NODE_ID, right_on=SOURCE, how='left')
        self.df_nodes = self.df_nodes.drop(columns=[SOURCE])


    def fill_main_core(self, G):
        G.add_edges_from(nx.selfloop_edges(G))
        G.remove_edges_from(nx.selfloop_edges(G))
        cores = nx.core_number(G)
        core_df = pd.DataFrame.from_dict(cores,orient='index',columns=[CORE])
        core_df[NODE_ID] = core_df.index
        self.df_nodes = self.df_nodes.merge(core_df, on=NODE_ID, how='left')

    def fill_weighted_in_degree(self, G):
        in_degs = [(node, val) for (node, val) in G.in_degree(weight=MEASURE)]
        in_degs_df = pd.DataFrame(in_degs, columns=[SOURCE, WEIGHTED_IN_DEGREE])
        self.df_nodes = self.df_nodes.merge(in_degs_df, left_on=NODE_ID, right_on=SOURCE, how='left')
        self.df_nodes = self.df_nodes.drop(columns=[SOURCE])

    def fill_weighted_out_degree(self, G):
        out_degs = [(node, val) for (node, val) in G.out_degree(weight=MEASURE)]
        out_degs_df = pd.DataFrame(out_degs, columns=[SOURCE, WEIGHTED_OUT_DEGREE])
        self.df_nodes = self.df_nodes.merge(out_degs_df, left_on=NODE_ID, right_on=SOURCE, how='left')
        self.df_nodes = self.df_nodes.drop(columns=[SOURCE])

    def fill_weighted_degree(self, G):
        degs = [(node, val) for (node, val) in G.degree(weight=MEASURE)]
        degs_df = pd.DataFrame(degs, columns=[SOURCE, WEIGHTED_DEGREE])
        self.df_nodes = self.df_nodes.merge(degs_df, left_on=NODE_ID, right_on=SOURCE, how='left')
        self.df_nodes = self.df_nodes.drop(columns=[SOURCE])

    def make_log_feature(self, feature, plusone = False):

        if(plusone == False):
            self.df[str(feature + '_log')]= np.log(self.df[feature]) 
        else:
            self.df[str(feature + '_log_p1')]= np.log(self.df[feature] + 1) 
        self.df = self.df.drop(columns=[feature])

    def deepdive(self, caller, measure_thresh=0):
        #     """
        #     for one caller, looks at its one and two hop calls
        #     and plots one hops
        #     
        #     :return:
        #     """
        one_hop = self.df[(self.df[SOURCE] == caller) | (self.df[DESTINATION] == caller)]
        one_hop = one_hop[one_hop[MEASURE]>measure_thresh]
        sources = one_hop[SOURCE].unique() 
        destinations = one_hop[DESTINATION].unique() 
        two_hops = np.append(sources, destinations) 
        two_hops = np.unique(two_hops)
        two_hops = two_hops.tolist()
        two_hops = self.df[(self.df[SOURCE].isin(two_hops) ) | (self.df[DESTINATION].isin(two_hops))]

        G = nx.from_pandas_edgelist(one_hop, edge_attr=MEASURE, create_using=nx.DiGraph(), source=SOURCE,target=DESTINATION)
        pos = nx.spring_layout(G)

        nx.draw_networkx_nodes(G, pos, node_size=10)
        nx.draw_networkx_edges(G,pos)

        plt.show()
        return(one_hop, two_hops, pos)

    def my_print(self):
        """
        for debugging - just prints the (adjacency/graph) pandas frame
        :return:
        """
        print("")
        print("---- echoing the input ----")
        print(self.df)

        print("\n")
        print("---- RESULT (placeholder): data frame  of nodes -------------")
        print(self.df_nodes)

    def print_to_csv(self, out_file_name):
        """
        prints the df_nodes dataframe as a csv file,
        ready for nd_cloud processing
        :param out_file_name:
        :return:
        """
        self.df_nodes.to_csv(out_file_name, index=False)


if __name__ =="__main__":
    parser = argparse.ArgumentParser(description="analysis for static graphs")
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

    sg = StaticGraph(filename)
    sg.my_print()

    if verbose > 1:
        print("\n\n ----")
        sg.print_to_csv("nodeVectors.csv")
        print(" check the file nodeVectors.csv ")

    print("---------------")
