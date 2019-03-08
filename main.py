import tests
from databaseConnection import DBConnection
import pandas as pd

connection = DBConnection()
connection.database_connection()
query_x = "select age, sex, hoursperweek, race from censusdata where id < 1000"
query_y = "select age, sex from censusdata where id = 3 or (id > 6 and id < 300) or id = 88"
x = pd.DataFrame(connection.query(query_x))
y = pd.DataFrame(connection.query(query_y))

print('\nDo you want to compare all the methods? (y/n)')
select = input()
if select == 'y':
    tests.test_all(x, y, query_x, query_y)
    exit()

print('\nDo you prefer a-priori (pr) or a-posteriory (po) free tuples selection?')
select = input()

if select == 'pr':
    print('\nDo you prefer a random or a cluster choice of the free tuples? (r / c)')
    selection = input()
    if selection == 'c':
        tuples_selection_mode = 'c'
    else:
        tuples_selection_mode = 'r'

    tests.test_a_priori_free_tuples_selection(x, y, tuples_selection_mode)

else:
    print('\nDo you prefer a min_altitude_first(min) approach or a most_important_node_firts(most) approach?')
    selection = input()
    if selection == 'min':
        tuples_selection_mode = 'min'
    else:
        tuples_selection_mode = 'most'

    tests.test_a_posteriori_free_tuples_selection(x, y, tuples_selection_mode)

connection.close_connection()
