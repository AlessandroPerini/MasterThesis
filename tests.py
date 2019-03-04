import postProcessing
import preProcessing
import utility
import resultsVisualization
import oneHotEncoding
from sklearn import tree
import time


def test_a_priori_free_tuples_selection(x, y):
    classifier = tree.DecisionTreeClassifier()
    x, y, list_y, tuples_selection_type = preProcessing.starter(x, y)
    classifier.fit(x, list_y)
    resultsVisualization.tree_printer(classifier, x, tuples_selection_type)
    explanations = resultsVisualization.path_finder(classifier, x, list_y)
    resultsVisualization.print_explanations_to_terminal(explanations)


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


def test_a_posteriori_free_tuples_selection(x,y):
    classifier, x, y, list_y = test_all_free_tuples_selection(x, y)
    applied = classifier.apply(x)
    important_nodes = list()
    for elem in range(len(list_y)):
        if list_y[elem] != 0:
            important_nodes.append(applied[elem])

    print('Important nodes BEFORE:')
    print(important_nodes)

    print('\nDo you prefer a min_altitude_first(min) approach or a most_important_node_firts(most) approach?')
    selection = input()
    start = time.time()
    if selection == 'min':
        classifier2, y, list_y = postProcessing.min_altitude_first(x, y, list_y, classifier)
    else:
        classifier2, y, list_y = postProcessing.most_important_node_first(classifier, x, y, list_y)

    end = time.time()
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
