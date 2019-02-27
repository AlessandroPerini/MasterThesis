from pydotplus import pydotplus
import collections
from sklearn import tree
import pandas as pd
from random import randint
from sklearn.cluster import KMeans
import numpy as np
from oneHotEncoding import OneHotEncoding

class Utility:

    free_tuple_selection_type = ''

    def tree_printer(self, classifier, dataframe_x):
        """
        :param classifier: variable in witch is built the decision tree
        :param features: headers of columns of dataframe x
        :return: nothing, it prints the png image with the tree
        """
        try:
            features = list(dataframe_x.columns.values)
            dot_data = tree.export_graphviz(classifier,
                                            feature_names=features,
                                            out_file=None,
                                            filled=True,
                                            rounded=True,
                                            node_ids=True)
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

            graph.write_png(self.free_tuple_selection_type)
            print("Tree printed!")

        except ValueError as ve:
            print("Tree not printed!" + ve)

    @staticmethod
    def y_creator(dataframe_x, dataframe_y):
        """
        :param dataframe_x: main dataframe
        :param dataframe_y: dataframe with tuples that are congruent with the result
        :return: y list

        Note: dataframe_x must have less column than dataframe_y
        """

        dataframe_x = dataframe_x.sort_values(by=dataframe_x.columns.tolist())
        dataframe_y = dataframe_y.sort_values(by=dataframe_x.columns.tolist())
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
                new_rows = new_rows[
                    (new_rows[dataframe_results.columns.values[column]] == dataframe_results.iloc[row, column])]

            new_rows['tupleset'] = [row] * new_rows.shape[0]

            if new_rows.shape[0] == 1:
                new_rows['isfree'] = [0] * new_rows.shape[0]
            else:
                new_rows['isfree'] = [1] * new_rows.shape[0]

            result = pd.concat([result, new_rows], axis=0)

        print('this is the table with the new columns:')
        print(result)
        return result

    def free_tuple_selection_random(self, dataframe_y):
        """
        :param dataframe_y: dataframe from which we want to select randomly the tuple of every set of free tuples
        :return: dataframe y only with positive tuples
        """
        self.free_tuple_selection_type = 'treeRandom.png'
        result = pd.DataFrame()
        for set_index in range(len(dataframe_y.tupleset.unique())):
            tmp = dataframe_y[(dataframe_y.tupleset == set_index)]

            if tmp.shape[0] != 1:
                tmp = tmp.iloc[[randint(0, tmp.shape[0] - 1)]]

            result = pd.concat([result, tmp], axis=0)

        # result = result.drop(axis=1, columns=["tupleset", "isfree"])
        # Per ora non serve...
        print('this is y after the random selection of the free tuples')
        print(result)
        return result

    def free_tuple_selection_cluster(self, dataframe_y):
        """
        :param dataframe_y: dataframe from which we want to select the tuple of every set of free tuples using KMeans clusters
        :return: dataframe y only with positive tuples
        """

        self.free_tuple_selection_type = 'treeCluster.png'
        n_clusters = 3
        kmeans = KMeans(n_clusters=n_clusters).fit(dataframe_y)
        print(kmeans.labels_)
        dataframe_y['cluster'] = kmeans.labels_
        result = pd.DataFrame()

        while dataframe_y.shape[0]:
            tmp_cluster = dataframe_y.cluster.mode().values[0]  # takes the biggest cluster
            tmp = dataframe_y[(dataframe_y.cluster == tmp_cluster)]
            dataframe_y = dataframe_y[dataframe_y.cluster != tmp_cluster]

            for set in tmp.tupleset.unique():
                rows = tmp[tmp.tupleset == set]
                result = pd.concat([result, rows.iloc[[0]]], axis=0)
                dataframe_y = dataframe_y[dataframe_y.tupleset != set]

        print('this is y after the cluster selection of the free tuples')
        print(result)
        return result

    @staticmethod
    def path_finder(classifier, dataframe_x, list_y):
        """
        :param classifier: classifier
        :param dataframe_x: dataframe x
        :param list_y: y list
        :param headers: names of the features
        :return: string with explanations
        """
        headers = list(dataframe_x.columns.values)
        matrix = classifier.decision_path(dataframe_x)
        children_left = classifier.tree_.children_left
        features = classifier.tree_.feature
        thresholds = classifier.tree_.threshold

        """
        applied = classifier.apply(dataframe_x)
        important_nodes = list()
        for elem in range(len(list_y)):
            if list_y[elem] != 0:
                important_nodes.append(applied[elem])
        print('important nodes:')
        print(important_nodes)
        """

        explanations = list()
        for elem in range(len(list_y)):
            if list_y[elem] != 0:
                tmp_matrix = matrix[elem, :]
                tmp_matrix = tmp_matrix.todense()
                tmp_matrix = np.squeeze(np.asarray(tmp_matrix))
                node_path = list()
                attribute_path = list()
                threshold_path = list()

                for index in range(len(tmp_matrix)):
                    if tmp_matrix[index] != 0:
                        node_path.append(index)

                        if features[index] != -2:
                            attribute_path.append(headers[features[index]])
                            threshold_path.append(thresholds[index])

                explanation = list()
                for index in range(len(node_path) - 1):
                    if children_left[node_path[index]] == node_path[index + 1]:
                        explanation.append(attribute_path[index] + ' <= ' + str(threshold_path[index]))
                    else:
                        explanation.append(attribute_path[index] + ' > ' + str(threshold_path[index]))

                explanation_string = ''
                for index in range(len(explanation)):
                    if index != 0 and index < len(explanation):
                        explanation_string += ' and '
                    explanation_string += explanation[index]

                explanations.append(explanation_string)

        return explanations

    def preprocessing(self, x, y):
        y = self.transform_y_to_all_results(x, y)  # transforms y so that it will have all the attributes as X
        y = OneHotEncoding().encoder(y, x)
        print('do you prefer a random or a cluster choice of the free tuples? (r / c)')
        random_cluster = input()
        if random_cluster == 'r':
            y = self.free_tuple_selection_random(y)
        else:
            y = self.free_tuple_selection_cluster(y)
        x = OneHotEncoding().encoder(x, x)
        list_y = self.y_creator(x, y)
        return x, list_y
