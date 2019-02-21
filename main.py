from databaseConnection import DBConnection
from tabulate import tabulate
import pandas as pd
from oneHotEncoding import OneHotEncoding
from sklearn import tree
from utility import Utility

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

df_x = pd.DataFrame(connection.query("select * from censusdata where id < 100"))
df_y = pd.DataFrame(connection.query("select race,age,sex from censusdata where id = 3 or id = 4"))
y = Utility().transform_y_to_all_results(df_x, df_y)
y = y.drop(axis=1, columns=["tupleset","isfree"])

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
