import pandas as pd


def important_nodes_generator(classifier, dataframe_x, list_y):
    applied = classifier.apply(dataframe_x)
    important_nodes = list()
    for elem in range(len(list_y)):
        if list_y[elem] != 0:
            important_nodes.append(applied[elem])

    return important_nodes


def y_creator(dataframe_x, dataframe_y):
    """
    :param dataframe_x: main dataframe
    :param dataframe_y: dataframe with tuples that are congruent with the result
    :return: y list, reordered dataframe_x

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

    return dataframe_x, dataframe_y, y


def transform_y_to_all_results(dataframe_x, dataframe_results):
    """
    :param dataframe_x: main data frame
    :param dataframe_results: data frame of results that are visible to the user
    :return: y with all the tuples that have the attributes of dataframe_result also with columns 'isfree' and 'tupleset'
    """
    dataframe_results = dataframe_results.drop_duplicates()
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

    print('\nThis is y:')
    print(result)
    return result
