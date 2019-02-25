from pydotplus import pydotplus
import collections
from sklearn import tree
import pandas as pd
from random import randint
from sklearn.cluster import KMeans
import numpy as np

class Utility:

    @staticmethod
    def tree_printer(classifier, features):
        """

        :param classifier: variable in witch is built the decision tree
        :param features: headers of columns of dataframe x
        :return: nothing, it prints the png image with the tree
        """
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

            graph.write_png('treeRandom.png')
            print("Tree printed!")

        except ValueError as ve:
            print("Tree not printed!" + ve)

    @staticmethod
    def y_creator(dataframe_x, dataframe_y):
        """
        :param dataframe_x: main dataframe
        :param dataframe_y: dataframe with tuples that are congruent with the result
        :return: y vector

        Note: dataframe_x and dataframe_y must have the same number of parameters (column)
        """

        dataframe_x = dataframe_x.sort_values(by=dataframe_x.columns.tolist())
        dataframe_y = dataframe_y.sort_values(by=dataframe_x.columns.tolist())
        print('inizio y creator')
        print(dataframe_y)
        print(dataframe_x)
        col = len(dataframe_x.columns)
        y = [1] * dataframe_x.shape[0]
        count = 0

        for row in range(dataframe_x.shape[0]):
            if count < dataframe_y.shape[0]:
                for c in range(col):
                    if dataframe_x.iloc[row, c] != dataframe_y.iloc[count, c]:
                        y[row] = 0

                if y[row] == 1:
                    count += 1

            else:
                for r in range(row, dataframe_x.shape[0]):
                    y[r] = 0

        return y

    @staticmethod
    def transform_y_to_all_results(dataframe_x, dataframe_results):
        """
        :param dataframe_x: main data frame
        :param dataframe_results: data frame of results that are visible to the user
        :return: y with all the tuples that have the attributes of dataframe_result also with columns 'isfree' and 'tupleset'
        """
        result = pd.DataFrame()
        for row in range(dataframe_results.shape[0]):

            new_rows = dataframe_x

            for column in range(len(dataframe_results.columns)):

                new_rows = new_rows[(new_rows[dataframe_results.columns.values[column]] == dataframe_results.iloc[row, column])]

            new_rows['tupleset'] = [row] * new_rows.shape[0]

            if new_rows.shape[0] == 1:
                new_rows['isfree'] = [0] * new_rows.shape[0]
            else:
                new_rows['isfree'] = [1] * new_rows.shape[0]

            result = pd.concat([result, new_rows], axis=0)

        return result

    @staticmethod
    def free_tuple_selection_random(dataframe_y):
        """

        :param dataframe_y: is the dataframe from wich we want to select randomly the tuple of every set of free tuples
        :return: dataframe y only with positive tuples and without columns 'isfree' and 'tupleset'
        """
        result = pd.DataFrame()
        for set_index in range(len(dataframe_y.tupleset.unique())):
            tmp = dataframe_y[(dataframe_y.tupleset == set_index)]
            if tmp.shape[0] != 1:
                tmp = tmp.iloc[[randint(0, tmp.shape[0]-1)]]
            result = pd.concat([result, tmp], axis=0)

        print(result)       #printa la tabella di y con ancora le colonne 'tupleset' e 'isfree'
        result = result.drop(axis=1, columns=["tupleset", "isfree"])
        return result

    @staticmethod
    def free_tuple_selection_cluster(dataframe_y):
        n_clusters = 3
        kmeans = KMeans(n_clusters=n_clusters).fit(dataframe_y)
        unique, counts = np.unique(kmeans.labels_, return_counts=True)
        print(kmeans.labels_)
        dataframe_y['cluster'] = kmeans.labels_
        print(dataframe_y)
        result = pd.DataFrame()
        while dataframe_y.shape[0]:
            tmp_cluster = dataframe_y.cluster.mode().values[0]  #takes the biggest cluster with more tuples
            tmp = dataframe_y[(dataframe_y.cluster == tmp_cluster)]
            dataframe_y = dataframe_y[dataframe_y.cluster != tmp_cluster]
            print(dataframe_y)
            for set in tmp.tupleset.unique():
                rows = tmp[tmp.tupleset == set]
                result = pd.concat([result, rows.iloc[[0]]], axis=0)
                dataframe_y = dataframe_y[dataframe_y.tupleset != set]
            print(tmp)
            print(dataframe_y)
        print("RESULT")
        print(result)
        return result
