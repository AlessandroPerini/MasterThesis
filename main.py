import tests
from databaseConnection import DBConnection
import pandas as pd

connection = DBConnection()
connection.database_connection()
x = pd.DataFrame(connection.query("select age, sex , workclass, race, hoursperweek from censusdata where id < 40"))
y = pd.DataFrame(connection.query("select age, sex from censusdata where id = 3 or id = 5 "))

print('\nDo you prefer a-priori (pr) or a-posteriory (po) free tuples selection?')
select = input()
if select == 'pr':
    tests.test_a_priori_free_tuples_selection(x, y)
else:
    tests.test_a_posteriori_free_tuples_selection(x, y)

connection.close_connection()
