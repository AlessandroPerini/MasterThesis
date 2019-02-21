from databaseConnection import DBConnection
from tabulate import tabulate
import pandas as pd
from oneHotEncoding import OneHotEncoding
from sklearn import tree
from utility import Utility

connection = DBConnection()
connection.database_connection()
print("scrivi la query per ricavare le tuple che vuoi analizzare (la X).  es: SELECT * FROM censusdata limit 4")
#query = input()
query = 'SELECT age, occupation, race FROM censusdata limit 10'
table = connection.query(query)
print('ecco le tuple: \n ' + tabulate(table, tablefmt="fancy_grid"))

"""" Per estrarre una colonna dei risultati
column_id = [item['id'] for item in result]
column_Age = [item['Age'] for item in result"""

df_x = pd.DataFrame(connection.query("select * from censusdata where id < 200"))
df_y = pd.DataFrame(connection.query("select race,age,sex from censusdata where id = 3 or id = 4 or id = 5 or id = 6"))
print(Utility().transform_y_to_all_results(df_x, df_y))


"""
y = Utility().y_creator(df_x, df_y)

encod = OneHotEncoding()
encoded = encod.encoder(df_x)
print(encoded)
print(y)

classifier = tree.DecisionTreeClassifier()
classifier.fit(encoded, y)
print(classifier)

headers = list(encoded.columns.values)
Utility().tree_printer(classifier, headers)
"""

connection.close_connection()
