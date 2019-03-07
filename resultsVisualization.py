import collections
import pydotplus
import numpy as np
from sklearn import tree


def tree_printer(classifier, dataframe_x, tuples_selection_type='', important_nodes=[]):
    """

    :param classifier: variable in which is built the decision tree
    :param dataframe_x:
    :param tuples_selection_type:
    :return: nothing, it prints the png image with the tree
    """

    switcher = {
        '': "tree_PO_MinMost.png",
        'c': "tree_PR_Cluster.png",
        'r': "tree_PR_Random.png"
    }
    path = switcher.get(tuples_selection_type)

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
                if len(important_nodes) > 0:
                    if int(dest.get_label().split("#")[1].split("\\")[0]) in important_nodes:
                        dest.set_fillcolor('green')

        graph.write_png(path)
        print("Tree " + path + " printed!")

    except ValueError as ve:
        print("Tree not printed!" + ve)


def path_finder(classifier, dataframe_x, list_y):
    """

    :param classifier:
    :param dataframe_x:
    :param list_y:
    :return: explanations is a set (list of unique elements) where each element is a dictionary
    """
    headers = list(dataframe_x.columns.values)
    matrix = classifier.decision_path(dataframe_x)
    children_left = classifier.tree_.children_left
    features = classifier.tree_.feature
    thresholds = classifier.tree_.threshold
    explanations = set()
    for elem in range(len(list_y)):
        if list_y[elem] != 0:
            tmp_matrix = matrix[elem, :]
            tmp_matrix = tmp_matrix.todense()
            tmp_matrix = np.squeeze(np.asarray(tmp_matrix))
            node_path = list()
            dictionaries = list()
            for index in range(len(tmp_matrix)):
                if tmp_matrix[index] != 0:
                    node_path.append(index)
                    if features[index] != -2:
                        dictionary = {'column': headers[features[index]],
                                      'symbol': '',
                                      'value': thresholds[index]}
                        dictionaries.append(dictionary)

            for index in range(len(node_path) - 1):
                if children_left[node_path[index]] == node_path[index + 1]:
                    dictionaries[index]['symbol'] = '<='
                else:
                    dictionaries[index]['symbol'] = '>'

            compressed_dictionaries = path_compressor(dictionaries)
            string_compressed_dictionaries = from_dictionaries_to_string(compressed_dictionaries)
            explanations.add(string_compressed_dictionaries)

    return explanations


def path_compressor(dictionaries):
    compressed_dictionaries = list()
    columns_set = set()
    for dictionary in dictionaries:
        columns_set.add(dictionary['column'])

    for unique_column in columns_set:
        unique_dictionary = list()
        for dictionary in dictionaries:
            if dictionary['column'] == unique_column:
                unique_dictionary.append(dictionary)

        greater_dict = list()
        less_dict = list()
        for dictionary in unique_dictionary:
            if dictionary['symbol'] == '>':
                greater_dict.append(dictionary['value'])
            else:
                less_dict.append(dictionary['value'])

        if len(greater_dict) > 0:
            greater_dict.sort(reverse=True, key=float)
            dictionary = {'column': unique_column,
                          'symbol': '>',
                          'value': greater_dict[0]}
            compressed_dictionaries.append(dictionary)

        if len(less_dict) > 0:
            less_dict.sort(key=float)
            dictionary = {'column': unique_column,
                          'symbol': '<=',
                          'value': less_dict[0]}
            compressed_dictionaries.append(dictionary)

    return compressed_dictionaries


def from_dictionaries_to_string(dictionaries):
    result = ''
    for index in range(len(dictionaries)):
        if index != 0:
            result += " and "

        result += dictionaries[index]['column'] + " " + dictionaries[index]['symbol'] + " " + str(
            dictionaries[index]['value'])

    return result


def print_explanations_to_terminal(explanations):
    print('\n' + '_' * 100 + '\n')
    print("\n" + "List of explanations :" + "\n")
    for expl in explanations:
        print(expl)
