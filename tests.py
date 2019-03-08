import postProcessing
import preProcessing
import utility
import resultsVisualization
from fileWriter import FileWriter
import pandas as pd
import oneHotEncoding
from sklearn import tree
import time


def test_a_priori_free_tuples_selection(x, y, tuples_selection_mode, max_depth=None):
    classifier = tree.DecisionTreeClassifier(max_depth=max_depth)
    x, y, list_y, computation_time = preProcessing.starter(x, y, tuples_selection_mode)
    #x.drop(axis=1, columns=['age', 'Male', 'Female'], inplace=True)
    classifier.fit(x, list_y)
    resultsVisualization.tree_printer(classifier, x, tuples_selection_mode)
    explanations = resultsVisualization.path_finder(classifier, x, list_y)
    resultsVisualization.print_explanations_to_terminal(explanations)
    purity, tree_height, n_imp_nodes = utility.tree_features_calculator(classifier, x, list_y)
    resultsVisualization.features_to_terminal(tuples_selection_mode, computation_time, purity, tree_height, n_imp_nodes)
    return explanations, computation_time, purity, tree_height, n_imp_nodes


def test_all_free_tuples_selection(x,y, max_depth=None):
    """
    :param x: dataframe_x
    :param y: dataframe_y
    :return: fitted classifier + prints the tree
    """
    classifier = tree.DecisionTreeClassifier(max_depth=max_depth)
    y = utility.transform_y_to_all_results(x, y)
    y = oneHotEncoding.encoder(y, x)
    x = oneHotEncoding.encoder(x, x)
    x, y, list_y = utility.y_creator(x, y)
    #x.drop(axis=1, columns=['age', 'Male', 'Female'], inplace=True)
    #y.drop(axis=1, columns=['age', 'Male', 'Female'], inplace=True)
    classifier.fit(x, list_y)
    resultsVisualization.tree_printer(classifier, x)
    return classifier, x, y, list_y


def test_a_posteriori_free_tuples_selection(x, y, tuples_selection_mode, max_depth=None):
    classifier, x, y, list_y = test_all_free_tuples_selection(x, y, max_depth)
    applied = classifier.apply(x)
    important_nodes = list()
    for elem in range(len(list_y)):
        if list_y[elem] != 0:
            important_nodes.append(applied[elem])

    print('Important nodes BEFORE:')
    print(important_nodes)
    start = time.time()
    if tuples_selection_mode == 'min':
        y, list_y = postProcessing.min_altitude_first(x, y, list_y, classifier)
    else:
        tuples_selection_mode = 'most'
        y, list_y = postProcessing.most_important_node_first(classifier, x, y, list_y)

    end = time.time()
    computation_time = end - start
    print('\nTime needed for \'post processing\': ' + str(end - start) + ' seconds\n')
    print(y)
    print(list_y)
    important_nodes = utility.important_nodes_generator(classifier, x, list_y)
    resultsVisualization.tree_printer(classifier, x, tuples_selection_mode, important_nodes)
    print('Important nodes AFTER:')
    print(important_nodes)
    explanations = resultsVisualization.path_finder(classifier, x, list_y)
    resultsVisualization.print_explanations_to_terminal(explanations)
    purity, tree_height, n_imp_nodes = utility.tree_features_calculator(classifier, x, list_y)
    resultsVisualization.features_to_terminal(tuples_selection_mode, computation_time, purity, tree_height, n_imp_nodes)
    return explanations, computation_time, purity, tree_height, n_imp_nodes


def test_all_free_tuples_combinations(x, y):

    y = utility.transform_y_to_all_results(x, y)
    results = list()
    results.append(pd.DataFrame())
    n_freesets = y.tupleset.unique().tolist()
    for set in n_freesets:
        result_temp = list()
        y_rows = y[y.tupleset == set]
        temp_results = len(results)
        for num_of_df in range(temp_results):
            for row in range(y_rows.shape[0]):
                k = pd.concat([results[num_of_df], y_rows.iloc[[row]]], axis=0)
                result_temp.append(k)

        results = result_temp

    print(results)


def test_all(x, y, query_x, query_y, max_depth):

    explanations_list = list()
    times_list = list()
    purities_list = list()
    heights_list = list()
    numbers_imp_nodes_list = list()

    expl1, time1, purity1, height1, n_imp_nodes1 = test_a_priori_free_tuples_selection(x, y, 'r', max_depth)
    expl2, time2, purity2, height2, n_imp_nodes2 = test_a_priori_free_tuples_selection(x, y, 'c', max_depth)
    expl3, time3, purity3, height3, n_imp_nodes3 = test_a_posteriori_free_tuples_selection(x, y, 'min', max_depth)
    expl4, time4, purity4, height4, n_imp_nodes4 = test_a_posteriori_free_tuples_selection(x, y, 'most', max_depth)

    explanations_list.extend((expl1, expl2, expl3, expl4))
    times_list.extend((time1, time2, time3, time4))
    purities_list.extend((purity1, purity2, purity3, purity4))
    heights_list.extend((height1, height2, height3, height4))
    numbers_imp_nodes_list.extend((n_imp_nodes1, n_imp_nodes2, n_imp_nodes3, n_imp_nodes4))

    file = FileWriter(query_x, query_y, y)
    file.times_writer(times_list)
    file.explanations_writer(explanations_list)
    file.purity_writer(purities_list)
    file.heights_writer(heights_list)
    file.number_important_nodes_writer(numbers_imp_nodes_list)
