from databaseConnection import DBConnection
from tabulate import tabulate
import pandas as pd
from oneHotEncoding import OneHotEncoding
from sklearn import tree
from utility import Utility
import sklearn

connection = DBConnection()
connection.database_connection()
df_x = pd.DataFrame(connection.query("select age, capitalgain, capitalloss, hoursperweek from censusdata where id < 1000"))
df_y = pd.DataFrame(connection.query("select age, hoursperweek from censusdata where id>20 and id<35"))
print('this is yor result table:')
print(df_y)
utility = Utility()
y = utility.transform_y_to_all_results(df_x, df_y)    #transforms y so that it will have all the attributes as X

print('do you prefer a random or a cluster choice of the free tuples? (r / c)')
random_cluster = input()
if random_cluster == 'r':
    y = utility.free_tuple_selection_random(y)
else:
    y = utility.free_tuple_selection_cluster(y)
vect_y = utility.y_creator(df_x, y)
encoded = OneHotEncoding().encoder(df_x)
classifier = tree.DecisionTreeClassifier()
classifier.fit(encoded, vect_y)
headers = list(encoded.columns.values)
utility.tree_printer(classifier, headers)
print(classifier.tree_.max_depth)
connection.close_connection()
