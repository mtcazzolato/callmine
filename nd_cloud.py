# Goal: produce several useful plots, for n-d cloud of points
#       (points  DO NOT have class labels)

import pandas as pd
import pandas.api.types as pat
# import matplotlib as mpl
# mpl.use('Agg')
# mpl.use('cairo')
import matplotlib.pyplot as plt
import plotly.express as px
import argparse
import numpy as np

class nd_cloud:
    '''
    Expects a data frame, with
    all of columns: numerical features

    and it provides several plots:
    histograms, 2d-contour plots, 3d interactive ones etc
    '''

    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_csv(filename)
        self.headers = list (self.df.columns.values)
        self.num_columns = len( self.headers)

        self.numerical_columns_list = list(range(0, len(self.headers)))
        # self.scale_list = {} # dictionary, with the scaling type of each column

        self.numerical_column_name_list = self.guess_numerical_columns()
        # auto-guess a column that is a primary key -> identifier
        self.key_column_name = self.guess_key_column()


    def guess_key_column(self) -> str:
        """ scans all columns, and returns the last one that is unique
        if none, returns None
        """
        key_column = None # by default
        for cname in self.headers:
            if self.is_primary_key(cname):
                key_column = cname
        return key_column

    def guess_numerical_columns(self) -> list[str]:
        numerical_column_name_list = []
        for cname in self.headers:
            if self.is_numerical(cname):
                numerical_column_name_list.append(cname)
        return numerical_column_name_list

    def count_unique(self, column_name: str) -> int:
        n = len( pd.unique( self.df[ column_name ]))
        return n

    def count_unique_all(self) -> None:
        # print ('count_unique_all called')
        for column_name in self.headers:
            n = self.count_unique(column_name)
            print( "{:>7d} unique values for {} ".format(n, column_name))

    def is_primary_key(self, column_name: str) -> bool:
        """
        True, if each row entry is unique
        """
        n_unique = self.count_unique( column_name)
        return len(self.df.index ) == n_unique

    def is_categorical(self, column_name: str)-> bool:
        return pat.is_string_dtype( self.df[column_name])

    def is_numerical(self, column_name: str)-> bool:
        return pat.is_numeric_dtype( self.df[ column_name])

    def show_type_all(self) -> None:
        for column_name in self.headers:
            if self.is_categorical(column_name):
                print("string:\t{}".format(column_name))
            elif self.is_numerical(column_name):
                print("number:\t{}".format(column_name))
            else:
                print("unknown:\t{}".format(column_name))

    # check if $i$ is a valid, numerical column
    # (ie, not first, not last)
    def is_in_range(self, i):
        if i in self.numerical_columns_list:
            return True
        else:
            return False

    def is_skewed_cn(self, column_name: str) -> bool:
        '''
        check if column $column_name is skewed -> log scales
        :param column_name: string
        :return:  boolean
        '''
        assert column_name in self.numerical_column_name_list,\
            "{} is not numeric".format(column_name)
        max_in_column = self.df[column_name].max()
        min_in_column = self.df[column_name].min()
        median_in_column = self.df[column_name].median()
        # if (min_in_column == 1 ) and ( max_in_column > 5*median_in_column) :
        if ( max_in_column > 5*median_in_column) :
            return True
        else:
            return False

    def prep(self,i):
        """ operates on the i-th column
        and returns log_flag (T/F), and offset (0.0/1.0) for log(x+1)
        """
        # log_flag = self.is_skewed(i)
        col_name = self.df.columns.values[i]
        # min_in_column = self.df[col_name].min()
        # assert min_in_column >=0, "column {} has negative entries {}".\
        #    format(col_name, min_in_column)
        # by default, no offset
        # offset = 0
        # # if log, and min==0, add an offset of 1, for log(x+1) transformation
        # if min_in_column == 0 and log_flag:
            # offset = 1
        # return log_flag, offset
        return self.prep_cn(col_name)

    def prep_cn(self, column_name: str) -> [bool, int]:
        """ operates on the 'column_name' column
        and returns log_flag and offset (for log(x+1) transformation
        """
        log_flag = self.is_skewed_cn(column_name)
        min_in_column = self.df[column_name].min()
        assert min_in_column >=0, "column {} has negative entries {}".\
            format(column_name, min_in_column)
        # by default, no offset
        offset = 0
        # if log, and min==0, add an offset of 1, for log(x+1) transformation
        if min_in_column == 0 and log_flag:
            offset = 1
        return log_flag, offset

    def print_stat(self) -> None:
        # for i in self.numerical_columns_list:
        for col_name in self.numerical_column_name_list:
            # col_name = self.df.columns.values[i]
            max_in_column = self.df[col_name].max()
            min_in_column = self.df[col_name].min()
            median_in_column = self.df[col_name].median()
            print("---")
            # print("col name:", self.headers[i])
            print("col name:", col_name)
            print("max , median, min:",
                  max_in_column, median_in_column, min_in_column)
            if self.is_skewed_cn(col_name):
                print(col_name, "is skewed")
            else:
                print (col_name, "is NOT skewed")

    def print_headers(self) -> None:
        for i in self.headers:
            print(">\t" + i)

    def zap_small(self, min_row_sum: int) -> None:
        '''
        Creates a copy that has only rows
        with row_sum >= min_row_sum
        '''
        print("min_row_sum = ", min_row_sum)
        assert min_row_sum >=0, "min_row_sum is negative {}".format(min_row_sum)
        if min_row_sum == 0:
            self.df_zapped = self.df
        else:
            self.df_zapped = self.df # needs to change
            df_local = self.df
            df_local["sum"] = df_local.sum(axis=1)
            df_local_short = \
                df_local[ df_local["sum"] >= min_row_sum]
            self.df_zapped = df_local_short[ self.df.columns.values.tolist()]

    def histogram_cn(self, column_name: str, print_flag: bool) -> None:
        """
        do the histogram for that column_name
        print it to png, if print_flag is True
        """
        logx_flag, x_offset = self.prep_cn(column_name)
        # x = self.df[ self.df.columns[i]]
        x = self.df[ column_name]
        xp = [ a+ x_offset for a in x]
        if logx_flag:
             xp = np.log10( xp )

        n, bins, patches = plt.hist(x = xp,
                                    log=True,
                                    bins='auto')
        my_xlabel = column_name
        if logx_flag:
            my_xlabel = column_name + " (log + " + str(x_offset) + ")"
        plt.xlabel(my_xlabel)
        plt.ylabel('count')
        plt.grid()

        if print_flag:
            fname = self.filename + "-" + column_name + ".png"
            plt.savefig(fname, format="png", dpi=400)
            plt.clf()
        else:
            plt.show()

    def histogram_all(self, print_flag: bool) -> None:
        assert len(self.numerical_column_name_list) >0, "no numerical columns to plot"
        for cname in self.numerical_column_name_list:
            self.histogram_cn(cname, print_flag)

    def interactive_3d_plot(self, i,j,k):
        logx_flag = False
        logy_flag = False
        logz_flag = False

        x = self.headers[i]
        # if self.is_skewed(i):
        logx_flag, x_offset = self.prep_cn(x)
        # if self.is_skewed_cn(x):
        #    logx_flag = True
        y = self.headers[j]
        logy_flag, y_offset = self.prep_cn(y)
        # if self.is_skewed_cn(y):
        #    logy_flag = True
        z = self.headers[k]
        logz_flag, z_offset = self.prep_cn(z)
        # if self.is_skewed_cn(z):
        #    logz_flag = True

        # color= self.headers[self.label_col]
        # operate on the zapped version,
        #     for faster reactions
        my_title = "{} - min_row_sum={}".format(self.filename, self.min_row_sum)
        fig = px.scatter_3d(self.df_zapped,
                            x, y, z,
                            # size=2,
                            # size_max=1, # does not seem to work...
                            # opacity=0.3, # works but not needed
                            title = my_title,
                            log_x = logx_flag,
                            log_y = logy_flag,
                            log_z = logz_flag
                            # color=color,
                            # hover_data = [self.headers[self.id_col]]
                            )
        # fig.update_traces(hoverinfo = "x+y+z+name", selector=dict(type='scatter3d'))
        fig.update_traces(marker_size=2, selector=dict(type='scatter3d'))
        fig.show()

    def interactive_3d_plot_all(self):
        """
        creates all the 3d plots (successive: <1,2,3>, <2,3,4> ...)
        """
        for i in self.numerical_columns_list[:-2]:
            # all but the last two
            self.interactive_3d_plot(i, i + 1, i+2)

    def interactive_2d_plot_cn(self, cname1: str, cname2: str, autoscale=True) -> None:
        # logx_flag, x_offset = self.prep(i)
        # logy_flag, y_offset = self.prep(j)
        logx_flag, x_offset = self.prep_cn(cname1)
        logy_flag, y_offset = self.prep_cn(cname2)

        # work on the zapped version, for faster
        #    interactive speed
        x = self.df_zapped[cname1]
        xp = x + x_offset

        y = self.df_zapped[cname2]
        yp = y + y_offset

        x_label = cname1 + " (+" + str(x_offset) + ")"
        y_label = cname2 + " (+" + str(y_offset) + ")"
        fig = px.scatter(self.df,
                         # x=self.headers[i],
                         # y=self.headers[j]
                         xp,
                         yp,
                         title="{} - min_row_sum={}".format(self.filename, self.min_row_sum),
                         log_x = logx_flag,
                         # marginal_x = "histogram",
                         log_y = logy_flag,
                         # marginal_y="histogram",
                         labels={'x': x_label,
                                 'y': y_label}
                         # size=1,
                         # color= self.headers[self.label_col],
                         # hover_data=[self.headers[self.id_col]]
                         )
        fig.show()

    def interactive_2d_plot_all(self):
        """
        goes over all the numerical attributes/columns,
        and plots the interactive scatterplots for (i, i+1)
        (it would be too time-consuming to plot all the n-choose-2 plots)
        """
        for i in range(len(self.numerical_column_name_list) - 1):
            cname1 = self.numerical_column_name_list[i]
            cname2 = self.numerical_column_name_list[i+1]
            self.interactive_2d_plot_cn(cname1, cname2)

    def hexbin_2d(self,
                  cname1: str,
                  cname2: str,
                  print_flag: bool) -> None:
        ''' creates the hexbin for columns
         cname1 and cname2
        '''

        # preparations: decide log/lin; log(x+1) or just log(x)
        logx_flag, x_offset = self.prep_cn(cname1)
        xscale = 'linear'
        if logx_flag:
            xscale = 'log'

        logy_flag, y_offset = self.prep_cn(cname2)
        yscale = 'linear'
        if logy_flag:
            yscale = 'log'

        x = self.df[ cname1 ]
        xp = x+x_offset

        y = self.df[ cname2 ]
        yp = y+y_offset

        # ready to plot
        plt.hexbin(xp,yp,
                   xscale = xscale,
                   yscale = yscale,
                   # marginals = True,
                   # vmin= 1,
                   mincnt = 1,
                   bins='log',
                   cmap='jet',
                   # cmap='inferno'
                   )
        plt.xlabel(cname1 + " (+"  + str(x_offset) + ")")
        plt.ylabel(cname2 + " (+"  + str(y_offset) + ")")
        cb = plt.colorbar()
        cb.set_label("log10(N)")
        plt.title(self.filename)
        plt.grid()

        if print_flag:
            fname = self.filename + "-" + cname1 + "-" + \
                    cname2 + ".png"
            plt.savefig(fname, format="png", dpi=400)
            plt.clf()
        else:
            plt.show()

    def hexbin_2d_all(self, print_flag):
        # column_list = self.numerical_columns_list
        n = len(self.numerical_column_name_list)
        for i in range(n-1):
            cname1 = self.numerical_column_name_list[i]
            cname2 = self.numerical_column_name_list[i+1]
            self.hexbin_2d(cname1,cname2, print_flag)
        return

    def kitchen_sink(self, verbose, print_flag, min_row_sum):
        """
        produces all the plots - avalanche - sigh!
        """
        self.min_row_sum = min_row_sum
        # create the zapped version first - no small row_sums
        self.zap_small(min_row_sum)
        print(self.df_zapped)

        self.show_type_all()
        print("key col = {}".format(self.key_column_name))
        print(" numerical column names =")
        print(self.numerical_column_name_list)
        n = len(self.numerical_column_name_list)

        if verbose > 1:
            if n > 0:
                self.histogram_all(print_flag)
        if verbose > 2:
            if n > 1:
                self.hexbin_2d_all(print_flag)
        if verbose>3:
            if n > 1:
                self.interactive_2d_plot_all()
        if verbose>4:
            if n > 2:
                self.interactive_3d_plot_all()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="2d/3d plots for clouds of n-dim points")
    parser.add_argument("-v", "--verbose",
                        help="level of verbosity (-v [-v ...])",
                        action="count",
                        default=0)
    parser.add_argument("-m", "--min_row_sum",
                        help="drop rows with smaller sum",
                        default=0)
    parser.add_argument("-p", "--print",
                        help="print to png",
                        action="store_true", default=False)
    parser.add_argument("filename",
                        help="input file csv.gz")
    # parser.add_argument("filename",
    #                    type=argparse.FileType('r'),
    #                    help="input file csv.gz")
    args = parser.parse_args()

    verbose = args.verbose
    filename = args.filename
    print_flag = args.print
    min_row_sum = int( args.min_row_sum )

    if verbose>1:
        print("verbose =", verbose)
        print("filename =", filename)
        print("print_flag =", print_flag)
        print("min_row_sum =", min_row_sum)

    ndc = nd_cloud(filename)
    if verbose>1:
        ndc.print_headers()

    if verbose>1:
        ndc.print_stat()

    ndc.kitchen_sink(verbose, print_flag, min_row_sum)
    # ndc.count_unique_all()
    # ndc.show_type_all()
    # print( "key col = {}".format(ndc.key_column_name))
    # print(" numerical column names =")
    # print( ndc.numerical_column_name_list)

