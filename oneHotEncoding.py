import numpy as np
from sklearn import preprocessing
import pandas as pd


def encoder(data_frame, referred_data_frame):
    """

    :param data_frame: dataframe x on witch will be done the one-hot-encoding
    :return: dataframe encoded: it deletes columns with less than 5 distinct values and adds a number of columns
    equal to the distinct values deleted. in each index_column values will be 0 or 1.
    """
    try:
        result = pd.DataFrame()
        if data_frame.equals(referred_data_frame) == 0:
            temp = data_frame.drop(axis=1, columns=["tupleset", "isfree"])
        else:
            temp = data_frame

        for column in referred_data_frame.columns:
            temp_df = pd.DataFrame(temp[column])

            if referred_data_frame[column].dtype == np.int64:
                result = pd.concat([result, temp_df], axis=1)
            else:
                max_distinct_values_of_a_categorical_column = 45
                if len(referred_data_frame[column].unique()) <= max_distinct_values_of_a_categorical_column:
                    new_columns = one_hot_encoding(referred_data_frame[column])
                    if temp.equals(referred_data_frame) == 0:
                        for temp_column in list(new_columns.columns.values):
                            result[temp_column] = 0
                            for row in range(temp.shape[0]):
                                if temp_column == temp[column].iloc[row]:
                                    result[temp_column].iloc[row] = 1
                    else:
                        result = pd.concat([result, new_columns], axis=1)

        if temp.equals(referred_data_frame) == 0:
            result = pd.concat([result, data_frame.tupleset], axis=1)
            result = pd.concat([result, data_frame.isfree], axis=1)
        print('dopo onehotencoding')
        print(result)
        return result

    except ValueError as ve:
        print(ve)
        print("Invalid dataframe")


def one_hot_encoding(column):
    """

    :param index_column: index_column on witch will be done the encoding
    :return: the dataframe with the columns changed that have to be added to the initial database
    """

    try:

        column_names = column.unique()
        for col in column_names:
            col = str(column) + col
        encoder = preprocessing.OneHotEncoder(categories=[column_names])
        result = pd.DataFrame(encoder.fit_transform(pd.DataFrame(column)).toarray())
        result.columns = column_names
        return result

    except ValueError as ve:
        print(ve)
        print("Invalid column")
