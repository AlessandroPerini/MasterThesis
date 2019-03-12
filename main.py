import tests
from databaseConnection import DBConnection
import pandas as pd

connection = DBConnection()
connection.database_connection()
# age, workclass, education, maritalstatus, occupation, relationship, race, sex, capitalgain, capitalloss, hoursperweek, nativecountry, income

query_x = "select age, workclass, education, maritalstatus, occupation, relationship, race, sex, capitalgain, capitalloss, hoursperweek, nativecountry, income from censusdata where id <1000"
query_y = "SELECT age, workclass FROM censusdata where id in(30, 32, 33, 34, 35, 36, 37, 38, 39, 40)"
x = pd.DataFrame(connection.query(query_x))
y = pd.DataFrame(connection.query(query_y))

print('\nInput the max tree depth (None = 0): ')
select = input()
max_depth = int(select)
if max_depth == 0:
    max_depth = None

print('\nDo you want to compare all the methods? (y/n)')
select = input()
if select == 'y':
    tests.test_all(x, y, query_x, query_y, max_depth)
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

    tests.test_a_priori_free_tuples_selection(x, y, tuples_selection_mode, max_depth)

else:
    print('\nDo you prefer a min_altitude_first(min) approach or a most_important_node_firts(most) approach?')
    selection = input()
    if selection == 'min':
        tuples_selection_mode = 'min'
    else:
        tuples_selection_mode = 'most'

    tests.test_a_posteriori_free_tuples_selection(x, y, tuples_selection_mode, max_depth)

connection.close_connection()
