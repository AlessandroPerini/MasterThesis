from databaseConnection import DBConnection
from tabulate import tabulate
import pandas as pd
from oneHotEncoding import OneHotEncoding
from sklearn import tree
from utility import Utility
import sklearn

connection = DBConnection()
connection.database_connection()
x = pd.DataFrame(connection.query("select age, sex, hoursperweek from censusdata where id < 100"))
y = pd.DataFrame(connection.query("select age, sex, hoursperweek from censusdata where id>50 and id<71"))
print('this is yor result table:')
print(y)
utility = Utility()
y = utility.transform_y_to_all_results(x, y)    #transforms y so that it will have all the attributes as X
print(y)
print('funziona???')
y = OneHotEncoding().encoder(y, x)
print(y)
print('do you prefer a random or a cluster choice of the free tuples? (r / c)')
random_cluster = input()
if random_cluster == 'r':
    y = utility.free_tuple_selection_random(y)
else:
    y = utility.free_tuple_selection_cluster(y)
x = OneHotEncoding().encoder(x, x)
list_y = utility.y_creator(x, y)
classifier = tree.DecisionTreeClassifier()
classifier.fit(x, list_y)
headers = list(x.columns.values)
utility.tree_printer(classifier, headers)
print(classifier.tree_.max_depth)

utility.path_finder(classifier, x, list_y, headers)

connection.close_connection()
