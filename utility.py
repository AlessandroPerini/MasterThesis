from pydotplus import pydotplus
from sklearn import tree
import collections
from sklearn import tree
import numpy as np


class Utility:

    @staticmethod
    def tree_printer(classifier, features):

        try:
            dot_data = tree.export_graphviz(classifier,
                                            feature_names=features,
                                            out_file=None,
                                            filled=True,
                                            rounded=True)
            graph = pydotplus.graph_from_dot_data(dot_data)

            colors = ('turquoise', 'orange')
            edges = collections.defaultdict(list)

            for edge in graph.get_edge_list():
                edges[edge.get_source()].append(int(edge.get_destination()))

            for edge in edges:
                edges[edge].sort()
                for i in range(2):
                    dest = graph.get_node(str(edges[edge][i]))[0]
                    dest.set_fillcolor(colors[i])

            graph.write_png('tree.png')
            print("Printed!")

        except ValueError as ve:
            print("Tree not printed!" + ve)

    @staticmethod
    def y_creator(dataframe_x, dataframe_y):

        col = len(dataframe_x.columns)
        y = [1] * dataframe_x.shape[0]
        count = 0

        for row in range(dataframe_x.shape[0]):
            print('row:')
            print(row)
            if count < dataframe_y.shape[0]:

                for c in range(col):

                    if dataframe_x.iloc[row, c] != dataframe_y.iloc[count, c]:

                        y[row] = 0

                if y[row] == 1:

                    count = count + 1

            else:

                print('else')
                for r in range(row, dataframe_x.shape[0]):

                    y[r] = 0

        print(y)
        return y

