import numpy as np
import pandas as pd
import utility


def most_important_node_first(classifier, x, y, list_y):
    result = pd.DataFrame()
    new_list_y = [0] * len(list_y)
    while 1 in y.isfree.tolist() or 0 in y.isfree.tolist():
        y = y.loc[y.isfree != -1]
        print('\n' + '_' * 100 + '\n')
        print(y)
        x, y, temp_list_y = utility.y_creator(x, y)
        important_nodes = utility.important_nodes_generator(classifier, x, temp_list_y)
        print('Important nodes:')
        print(important_nodes)
        most_important = max(set(important_nodes), key=important_nodes.count)
        print('Most important: ' + str(most_important))

        # Search for all the elements that are in the node 'c'
        for elem in range(y.shape[0]):
            list_y_index = 0
            y_ref = 0
            if important_nodes[elem] == most_important:
                if y.isfree.iloc[elem] == 1:
                    while y_ref != elem + 1:
                        if list_y[list_y_index] == 1:
                            y_ref += 1
                            new_list_y[list_y_index] = 1

                        list_y_index += 1

                    result = pd.concat([result, y.iloc[[elem]]], axis=0)
                    # For-loop on the elements of the set in order to set the 'isfree' column = -1
                    for row in range(y.shape[0]):
                        if y.tupleset.iloc[row] == y.tupleset.iloc[elem]:
                            y.isfree.iloc[row] = -1

                elif y.isfree.iloc[elem] == 0:
                    while y_ref != elem + 1:
                        if list_y[list_y_index] == 1:
                            y_ref += 1
                            new_list_y[list_y_index] = 1

                        list_y_index += 1

                    result = pd.concat([result, y.iloc[[elem]]], axis=0)

                y.isfree.iloc[elem] = -1

    result = result.drop(axis=1, columns=["isfree"])
    return classifier, result, new_list_y


def min_altitude_first(dataframe_x, y, list_y, classifier):

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

    n_nodes = classifier.tree_.node_count
    children_left = classifier.tree_.children_left
    children_right = classifier.tree_.children_right
    feature = classifier.tree_.feature
    threshold = classifier.tree_.threshold

    # The tree structure can be traversed to compute various properties such
    # as the depth of each node and whether or not it is a leaf.
    node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
    is_leaves = np.zeros(shape=n_nodes, dtype=bool)
    stack = [(0, -1)]  # seed is the root node id and its parent depth
    while len(stack) > 0:
        node_id, parent_depth = stack.pop()
        node_depth[node_id] = parent_depth + 1

        # If we have a test node
        if children_left[node_id] != children_right[node_id]:
            stack.append((children_left[node_id], parent_depth + 1))
            stack.append((children_right[node_id], parent_depth + 1))
        else:
            is_leaves[node_id] = True

    print("The binary tree structure has %s nodes and has "
          "the following tree structure:"
          % n_nodes)
    for i in range(n_nodes):
        if is_leaves[i]:
            print("%snode=%s leaf node." % (node_depth[i] * "\t", i))
        else:
            print("%snode=%s test node: go to node %s if X[:, %s] <= %s else to "
                  "node %s."
                  % (node_depth[i] * "\t",
                     i,
                     children_left[i],
                     feature[i],
                     threshold[i],
                     children_right[i],
                     ))

    #print(node_depth)
    important_nodes = utility.important_nodes_generator(classifier, dataframe_x, list_y)
    altitude_of_important_nodes = [-1] * len(important_nodes)
    #print('important nodes:')
    #print(important_nodes)
    #print('altitude_of_important_nodes')
    #print(altitude_of_important_nodes)
    index = 0
    for important_node in important_nodes:
        altitude_of_important_nodes[index] = node_depth[important_node]
        index += 1

    #print('altitude_of_important_nodes')
    #print(altitude_of_important_nodes)
    #print(min(altitude_of_important_nodes))
    result = pd.DataFrame()
    new_list_y = [0] * len(list_y)
    while 1 in y.isfree.tolist() or 0 in y.isfree.tolist():
        min_altitude = min(altitude_of_important_nodes)
        min_altitude_index = None
        i = 0
        while min_altitude_index == None:
            if altitude_of_important_nodes[i] == min_altitude:
                min_altitude_index = i

            i += 1

        #print("min_altitude_index")
        #print(min_altitude_index)
        most_important = important_nodes[min_altitude_index]
        #print('most important node')
        #print(most_important)
        altitude_of_important_nodes[min_altitude_index] = 100
        # Search for all the elements that are in the node 'c'
        for elem in range(y.shape[0]):
            list_y_index = 0
            y_ref = 0
            #print('important_nodes[elem] =')
            #print(important_nodes[elem])
            if important_nodes[elem] == most_important:
                #print('elem=')
                #print(elem)
                if y.isfree.iloc[elem] == 1:
                    while y_ref != elem + 1:
                        if list_y[list_y_index] == 1:
                            y_ref += 1
                            new_list_y[list_y_index] = 1

                        list_y_index += 1

                    result = pd.concat([result, y.iloc[[elem]]], axis=0)
                    # for loop on the elements of the set to set the isfree column = -1
                    for row in range(y.shape[0]):
                        if y.tupleset.iloc[row] == y.tupleset.iloc[elem]:
                            y.isfree.iloc[row] = -1

                elif y.isfree.iloc[elem] == 0:
                    while y_ref != elem + 1:
                        if list_y[list_y_index] == 1:
                            y_ref += 1
                            new_list_y[list_y_index] = 1

                        list_y_index += 1

                    result = pd.concat([result, y.iloc[[elem]]], axis=0)

                y.isfree.iloc[elem] = -1

    result = result.drop(axis=1, columns=["isfree"])
    return classifier, result, new_list_y
