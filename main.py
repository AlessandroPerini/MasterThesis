from databaseConnection import DBConnection
from tabulate import tabulate
import pandas as pd
from oneHotEncoding import OneHotEncoding
from sklearn import tree
from utility import Utility
from tests import Tests
from collections import Counter

connection = DBConnection()
connection.database_connection()
x = pd.DataFrame(connection.query("select age, sex , workclass from censusdata where id < 100"))
y = pd.DataFrame(connection.query("select age, sex from censusdata where id = 3 or id = 5 or (id > 20 and id < 30)"))

print('this is yor result table:')
print(y)
#Tests().test_a_priori_free_tuple_selection(x, y)

utility = Utility()
y = utility.transform_y_to_all_results(x, y)
y = OneHotEncoding().encoder(y, x)
x = OneHotEncoding().encoder(x, x)
x, y, list_y = utility.y_creator(x,y)
print(list_y)
classifier = tree.DecisionTreeClassifier()
classifier.fit(x, list_y)
utility.tree_printer(classifier, x)

applied = classifier.apply(x)
important_nodes = list()
for elem in range(len(list_y)):
    if list_y[elem] != 0:
        important_nodes.append(applied[elem])

print('important nodes PRIMA:')
print(important_nodes)

"""
children_left = classifier.tree_.children_left
print("ch. left:")
print(children_left)

features = classifier.tree_.feature
print("features:")
print(features)

thresholds = classifier.tree_.threshold
print("threshold:")
print(thresholds)

value = classifier.tree_.value
print("value:")
print(value)
"""


classifier2, y, list_y = utility.most_important_node_first(classifier, x, y, list_y)
applied = classifier2.apply(x)
print(y)
print(list_y)

important_nodes = list()
for elem in range(len(list_y)):
    if list_y[elem] != 0:
        important_nodes.append(applied[elem])

print('important nodes DOPO:')
print(important_nodes)

path = utility.path_finder(classifier2, x, list_y)
print(path)

connection.close_connection()
