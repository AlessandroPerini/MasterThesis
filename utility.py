from pydotplus import pydotplus
from sklearn import tree
import collections
from sklearn import tree


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

        y = [0] * dataframe_x.shape[0]
        count = 0

        for row in range(dataframe_x.shape[0]):
            if dataframe_x.iloc[row] == dataframe_y.iloc[count]:
                y[row] = 1
                count = count + 1

        return y
