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
x = pd.DataFrame(connection.query("select age, sex , workclass, race, hoursperweek from censusdata where id < 40"))
y = pd.DataFrame(connection.query("select age, sex from censusdata where id = 3 or id = 5 "))

print('\nDo you prefer a-priori (pr) or a-posteriory (po) free tuples selectio?')
select = input()
if select == 'pr':
    Tests().test_a_priori_free_tuples_selection(x, y)
else:
    Tests().test_a_posteriori_free_tuples_selection(x, y)

connection.close_connection()
