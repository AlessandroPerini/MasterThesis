import time
from random import randint
import pandas as pd
from kneed import KneeLocator
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
import oneHotEncoding
import utility


def starter(x, y, tuples_selection_mode):
    y = utility.transform_y_to_all_results(x, y)
    y = oneHotEncoding.encoder(y, x)
    if tuples_selection_mode == 'r':
        y, computation_time = free_tuple_selection_random(y)
    else:
        y, computation_time = free_tuple_selection_cluster(y)

    x = oneHotEncoding.encoder(x, x)
    x, y, list_y = utility.y_creator(x, y)
    return x, y, list_y, computation_time


def free_tuple_selection_random(dataframe_y):
    """
    :param dataframe_y: dataframe from which we want to select randomly the tuple of every set of free tuples
    :return: dataframe y only with positive tuples
    """
    result = pd.DataFrame()
    start = time.time()
    for set_index in range(len(dataframe_y.tupleset.unique())):
        tmp = dataframe_y[(dataframe_y.tupleset == set_index)]
        if tmp.shape[0] != 1:
            tmp = tmp.iloc[[randint(0, tmp.shape[0] - 1)]]

        result = pd.concat([result, tmp], axis=0)

    end = time.time()
    computation_time = end - start
    print('\nTime needed to select random tuples: ' + str(computation_time) + ' seconds\n')
    print('This is y after the random selection of the free tuples')
    print(result)
    return result, computation_time


def free_tuple_selection_cluster(dataframe_y):
    """
    :param dataframe_y: dataframe from which we want to select the tuple of every set of free tuples using KMeans clusters
    :return: dataframe y only with positive tuples
    """

    n_clusters = knee_extractor(dataframe_y)
    print('\nThe best number of clusters is: ' + str(n_clusters) + '\n')
    start = time.time()
    kmeans = KMeans(n_clusters=n_clusters).fit(dataframe_y)
    dataframe_y['cluster'] = kmeans.labels_
    print('\nDataframe y: ')
    print(dataframe_y)
    result = pd.DataFrame()
    while dataframe_y.shape[0]:
        tmp_cluster = dataframe_y.cluster.mode().values[0]  # Takes the bigger cluster
        print('\n' + '_' * 100 + '\n' + 'The bigger cluster is: ' + str(tmp_cluster))
        tmp = dataframe_y[(dataframe_y.cluster == tmp_cluster)]
        dataframe_y = dataframe_y[dataframe_y.cluster != tmp_cluster]
        for set in tmp.tupleset.unique():
            rows = tmp[tmp.tupleset == set]
            temp_rows = rows.drop(axis=1, columns=["cluster"])
            print('\n' + '_' * 100 + '\n' + 'rows:')
            print(temp_rows)
            closest = pairwise_distances_argmin(kmeans.cluster_centers_, temp_rows)
            # Returns for each element of x (center) the index of the nearest element of y (row)
            print('The index of the row that is closer to the centroid of the ' +str(tmp_cluster)+ '° cluster is: ' + str(closest[tmp_cluster]))
            print('The row is then: ')
            print(rows.iloc[[closest[tmp_cluster]]])
            result = pd.concat([result, rows.iloc[[closest[tmp_cluster]]]], axis=0)
            dataframe_y = dataframe_y[dataframe_y.tupleset != set]

    end = time.time()
    computation_time = end - start
    print('\nTime needed to select tuples with clusters: ' + str(computation_time) + ' seconds\n')
    print('This is y after the cluster selection of the free tuples')
    print(result)
    return result, computation_time


def knee_extractor(dataframe_y):
    sum_of_squared_distances = []
    clusters = range(1, 11)
    try:
        for k in clusters:
            km = KMeans(n_clusters=k).fit(dataframe_y)
            sum_of_squared_distances.append(km.inertia_)

        plt.plot(clusters, sum_of_squared_distances, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Sum_of_squared_distances')
        plt.title('Elbow Method For Optimal k')
        plt.show()
        best_k = KneeLocator(clusters, sum_of_squared_distances, curve='convex', direction='decreasing')

    except ValueError:
        return 2

    return best_k.knee
