import postProcessing
import preProcessing
import utility
import resultsVisualization
import oneHotEncoding
from sklearn import tree
import time


def test_a_priori_free_tuples_selection(x, y, tuples_selection_mode):
    classifier = tree.DecisionTreeClassifier()
    x, y, list_y, computation_time = preProcessing.starter(x, y, tuples_selection_mode)
    classifier.fit(x, list_y)
    resultsVisualization.tree_printer(classifier, x, tuples_selection_mode)
    explanations = resultsVisualization.path_finder(classifier, x, list_y)
    resultsVisualization.print_explanations_to_terminal(explanations)
    return computation_time


def test_all_free_tuples_selection(x,y):
    """
    :param x: dataframe_x
    :param y: dataframe_y
    :return: fitted classifier + prints the tree
    """
    classifier = tree.DecisionTreeClassifier()
    y = utility.transform_y_to_all_results(x, y)
    y = oneHotEncoding.encoder(y, x)
    x = oneHotEncoding.encoder(x, x)
    x, y, list_y = utility.y_creator(x, y)
    classifier.fit(x, list_y)
    resultsVisualization.tree_printer(classifier, x)
    return classifier, x, y, list_y


def test_a_posteriori_free_tuples_selection(x, y, tuples_selection_mode):
    classifier, x, y, list_y = test_all_free_tuples_selection(x, y)
    applied = classifier.apply(x)
    important_nodes = list()
    for elem in range(len(list_y)):
        if list_y[elem] != 0:
            important_nodes.append(applied[elem])

    print('Important nodes BEFORE:')
    print(important_nodes)
    start = time.time()
    if tuples_selection_mode == 'min':
        classifier2, y, list_y = postProcessing.min_altitude_first(x, y, list_y, classifier)
    else:
        classifier2, y, list_y = postProcessing.most_important_node_first(classifier, x, y, list_y)

    end = time.time()
    computation_time = end - start
    print('\nTime needed for \'post processing\': ' + str(end - start) + ' seconds\n')
    applied = classifier2.apply(x)
    print(y)
    print(list_y)

    important_nodes = list()
    for elem in range(len(list_y)):
        if list_y[elem] != 0:
            important_nodes.append(applied[elem])

    print('Important nodes AFTER:')
    print(important_nodes)
    explanations = resultsVisualization.path_finder(classifier2, x, list_y)
    resultsVisualization.print_explanations_to_terminal(explanations)
    return computation_time


def test_all(x, y):

    time1 = test_a_priori_free_tuples_selection(x, y, 'r')
    time2 = test_a_priori_free_tuples_selection(x, y, 'c')
    time3 = test_a_posteriori_free_tuples_selection(x, y, 'min')
    time4 = test_a_posteriori_free_tuples_selection(x, y, 'most')

    print('\n' + '_' * 30 + ' Methods Performances ' + '_' * 30)
    print('\nPR_Random: ' + str(time1))
    print('\nPR_Cluster: ' + str(time2))
    print('\nPO_Min: ' + str(time3))
    print('\nPO_Most: ' + str(time4))
