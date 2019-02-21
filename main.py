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
query_x = 'SELECT age, occupation, race FROM censusdata limit 20'
table_x = connection.query(query_x)
table_y = connection.query('SELECT age, occupation, race FROM censusdata where id=3 or id=14')
print('ecco le tuple: \n ' + tabulate(table_x, tablefmt="fancy_grid"))

"""" Per estrarre una colonna dei risultati
column_id = [item['id'] for item in result]
column_Age = [item['Age'] for item in result"""

x = pd.DataFrame(table_x)
encod = OneHotEncoding()
encoded = encod.encoder(x)
print(encoded)

classifier = tree.DecisionTreeClassifier()
classifier.fit(encoded, y)
#print(classifier)
headers = list(encoded.columns.values)
Utility().tree_printer(classifier, headers)

#print(pd.DataFrame(table_y))
queryx = connection.query("select id, age from censusdata where id < 5")
queryy = connection.query("select id, age from censusdata where id = 1 or id = 2")
print(pd.DataFrame(queryx))
print(pd.DataFrame(queryy))
Utility().y_creator(pd.DataFrame(queryx), pd.DataFrame(queryy))

connection.close_connection()
