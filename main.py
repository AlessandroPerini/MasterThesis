from databaseConnection import DBConnection
from tabulate import tabulate
import pandas as pd
from oneHotEncoding import OneHotEncoding
from sklearn import tree
from utility import Utility
from tests import Tests

connection = DBConnection()
connection.database_connection()
x = pd.DataFrame(connection.query("select age, sex, hoursperweek, workclass from censusdata where id < 1000"))
y = pd.DataFrame(connection.query("select age, sex from censusdata where id>50 and id<71"))
print('this is yor result table:')
print(y)
#Tests().test_a_priori_free_tuple_selection(x, y)

connection.close_connection()
