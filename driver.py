# Goal: 
#     create plots for the given input graph
#     It calls 'static_graph.py' to extract features in a csv file
#     And then calls 'nd_cloud.py' to do the plots
#####################################################

import static_graph as SG
import nd_cloud as NC
import argparse

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

    sg = SG.StaticGraph(filename)
    sg.my_print()

    if verbose > 1:
        print("\n\n ----")
        out_filename="nodeVectors.csv"
        sg.print_to_csv(out_filename)
        print(" check the file " + out_filename)
        ndc = NC.nd_cloud(out_filename)
        ndc.kitchen_sink(verbose, False, 0)

    print("---------------")
