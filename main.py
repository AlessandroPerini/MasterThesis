from databaseConnection import DBConnection
from tabulate import tabulate
import pandas as pd
from oneHotEncoding import OneHotEncoding
from sklearn import tree
from utility import Utility
import sklearn

connection = DBConnection()
connection.database_connection()
print("scrivi la query per ricavare le tuple che vuoi analizzare (la X).  es: SELECT * FROM censusdata limit 4")
query = 'SELECT age, occupation, race FROM censusdata limit 10'
table = connection.query(query)
print('ecco le tuple: \n ' + tabulate(table, tablefmt="fancy_grid"))

"""" Per estrarre una colonna dei risultati
column_id = [item['id'] for item in result]
column_Age = [item['Age'] for item in result
"""

df_x = pd.DataFrame(connection.query("select age, capitalgain, capitalloss, hoursperweek from censusdata where id < 100"))
df_y = pd.DataFrame(connection.query("select age, hoursperweek from censusdata where id = 3 or  id = 4 or  id = 7  or  id = 22  or  id = 55"))
y = Utility().transform_y_to_all_results(df_x, df_y)
print(y)

y = Utility().free_tuple_selection_random(y)
print(y)


vect_y = Utility().y_creator(df_x, y)
enc = OneHotEncoding()
encoded = enc.encoder(df_x)
print(encoded)
classifier = tree.DecisionTreeClassifier()
classifier.fit(encoded, vect_y)
print(classifier)
headers = list(encoded.columns.values)
Utility().tree_printer(classifier, headers)


connection.close_connection()
