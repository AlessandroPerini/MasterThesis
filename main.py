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
x = pd.DataFrame(connection.query("select age, sex , workclass, race, hoursperweek from censusdata where id < 1000"))
y = pd.DataFrame(connection.query("select age, sex from censusdata where id = 3 or id = 5 or (id > 20 and id < 30)"))

print('do you prefer a-priori (pr) or a-posteriory (po) free tuples selectio?')
select = input()
if select == 'pr':
    Tests().test_a_priori_free_tuples_selection(x, y)
else:
    Tests().test_a_posteriori_free_tuples_selection(x, y)


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

connection.close_connection()
