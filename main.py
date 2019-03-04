import tests
from databaseConnection import DBConnection
import pandas as pd

connection = DBConnection()
connection.database_connection()
x = pd.DataFrame(connection.query("select age, sex , workclass, race, hoursperweek from censusdata where id < 1000"))
y = pd.DataFrame(connection.query("select age, sex from censusdata where id = 3 or id = 5 or (id > 40 and id < 60) or (id > 589 and id < 600)"))

print('\nDo you want to compare all the methods?')
select = input()
if select == 'y':
    tests.test_all(x, y)
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
