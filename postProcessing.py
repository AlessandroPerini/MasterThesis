import pandas as pd
import utility
from utility import heights_of_important_nodes


def most_important_node_first(classifier, x, y, list_y):
    result = pd.DataFrame()
    new_list_y = [0] * len(list_y)
    var = y.isfree.tolist()
    while 0 in var:
        y = y.loc[y.isfree != -1]
        print('\n' + '_' * 100 + '\n')
        print(y)
        x, y, list_y = utility.y_creator(x, y)
        important_nodes = utility.important_nodes_generator(classifier, x, list_y)
        print('Important nodes:')
        print(important_nodes)
        # Search for all the elements that are in the node 'c'
        for elem in range(y.shape[0]):
            list_y_index = 0
            y_list_ones_count = 0
            if y.isfree.iloc[elem] == 0:
                while y_list_ones_count != elem + 1:
                    if list_y[list_y_index] == 1:
                        y_list_ones_count += 1
                    list_y_index += 1
                new_list_y[list_y_index - 1] = 1
                result = pd.concat([result, y.iloc[[elem]]], axis=0)
                y.isfree.iloc[elem] = -1
        var = y.isfree.tolist()
    while 1 in y.isfree.tolist():
        print('la y.isfree.tolist() è:')
        print(y.isfree.tolist())
        y = y.loc[y.isfree != -1]
        print('\n' + '_' * 100 + '\n')
        print(y)
        x, y, list_y = utility.y_creator(x, y)
        important_nodes = utility.important_nodes_generator(classifier, x, list_y)
        print('Important nodes:')
        print(important_nodes)
        count_free_tuple_set_per_node = list()
        for important_node in important_nodes:
            different_free_sets = set()
            for elem in range(y.shape[0]):
                if important_nodes[elem] == important_node:
                    if y.isfree.iloc[elem] == 1:
                        different_free_sets.add(y.tupleset.iloc[elem])
            count_free_tuple_set_per_node.append(different_free_sets)
        most_important_index = 0
        for i in range(len(count_free_tuple_set_per_node)):
            if len(count_free_tuple_set_per_node[i]) >= len(count_free_tuple_set_per_node[most_important_index]):
                most_important_index = i

        most_important = important_nodes[most_important_index]
        print('Most important: ' + str(most_important))

        # Search for all the elements that are in the node 'c'
        for elem in range(y.shape[0]):
            list_y_index = 0
            y_list_ones_count = 0
            if important_nodes[elem] == most_important:
                if y.isfree.iloc[elem] == 1:
                    while y_list_ones_count != elem + 1:
                        if list_y[list_y_index] == 1:
                            y_list_ones_count += 1
                        list_y_index += 1
                    new_list_y[list_y_index-1] = 1

                    result = pd.concat([result, y.iloc[[elem]]], axis=0)
                    # For-loop on the elements of the set in order to set the 'isfree' column = -1
                    for row in range(y.shape[0]):
                        if y.tupleset.iloc[row] == y.tupleset.iloc[elem]:
                            y.isfree.iloc[row] = -1
                y.isfree.iloc[elem] = -1

    result = result.drop(axis=1, columns=["isfree"])
    return result, new_list_y


def min_altitude_first(x, y, list_y, classifier):

    # The decision estimator has an attribute called tree_  which stores the entire
    # tree structure and allows access to low level attributes. The binary tree
    # tree_ is represented as a number of parallel arrays. The i-th element of each
    # array holds information about the node `i`. Node 0 is the tree's root. NOTE:
    # Some of the arrays only apply to either leaves or split nodes, resp. In this
    # case the values of nodes of the other type are arbitrary!
    #
    # Among those arrays, we have:
    #   - left_child, id of the left child of the node
    #   - right_child, id of the right child of the node
    #   - feature, feature used for splitting the node
    #   - threshold, threshold value at the node
    node_depth, _ = heights_of_important_nodes(classifier, list_y, x)
    result = pd.DataFrame()
    new_list_y = [0] * len(list_y)
    var = y.isfree.tolist()
    while 0 in var:
        y = y.loc[y.isfree != -1]
        print('\n' + '_' * 100 + '\n')
        print(y)
        x, y, list_y = utility.y_creator(x, y)
        important_nodes = utility.important_nodes_generator(classifier, x, list_y)
        print('Important nodes:')
        print(important_nodes)
        # Search for all the elements that are in the node 'c'
        for elem in range(y.shape[0]):
            list_y_index = 0
            y_list_ones_count = 0
            if y.isfree.iloc[elem] == 0:
                while y_list_ones_count != elem + 1:
                    if list_y[list_y_index] == 1:
                        y_list_ones_count += 1
                    list_y_index += 1
                new_list_y[list_y_index - 1] = 1
                result = pd.concat([result, y.iloc[[elem]]], axis=0)
                y.isfree.iloc[elem] = -1
        var = y.isfree.tolist()
    while 1 in y.isfree.tolist():
        y = y.loc[y.isfree != -1]
        x, y, list_y = utility.y_creator(x, y)
        important_nodes = utility.important_nodes_generator(classifier, x, list_y)
        altitude_of_important_nodes = [-1] * len(important_nodes)
        index = 0
        for important_node in important_nodes:
            altitude_of_important_nodes[index] = node_depth[important_node]
            index += 1
        min_altitude = min(altitude_of_important_nodes)
        min_altitude_nodes = list()
        for i in range(len(altitude_of_important_nodes)):
            if altitude_of_important_nodes[i] == min_altitude:
                min_altitude_nodes.append(important_nodes[i])

        most_important = max(set(min_altitude_nodes), key=min_altitude_nodes.count)
        # Search for all the elements that are in the node 'c'
        for elem in range(y.shape[0]):
            list_y_index = 0
            y_list_ones_count = 0
            if important_nodes[elem] == most_important:
                if y.isfree.iloc[elem] == 1:
                    while y_list_ones_count != elem + 1:
                        if list_y[list_y_index] == 1:
                            y_list_ones_count += 1
                        list_y_index += 1
                    new_list_y[list_y_index - 1] = 1

                    result = pd.concat([result, y.iloc[[elem]]], axis=0)
                    # for loop on the elements of the set to set the isfree column = -1
                    for row in range(y.shape[0]):
                        if y.tupleset.iloc[row] == y.tupleset.iloc[elem]:
                            y.isfree.iloc[row] = -1
                    y.isfree.iloc[elem] = -1
    result = result.drop(axis=1, columns=["isfree"])
    return result, new_list_y
