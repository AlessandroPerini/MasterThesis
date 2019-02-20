from databaseConnection import DBConnection
from tabulate import tabulate
import pandas as pd


connection = DBConnection()
connection.database_connection()
print("scrivi la query per ricavare le tuple che vuoi analizzare (la X).  es: SELECT * FROM censusdata limit 3")
query = input()
table = connection.query(query)
print('ecco le tuple: \n ' + tabulate(table, tablefmt="fancy_grid"))

"""" Per estrarre una colonna dei risultati
column_id = [item['id'] for item in result]
column_Age = [item['Age'] for item in result"""

x = pd.DataFrame(table)
print('quale colonna vuoi usare come y?')
temp = input()
y = x.column = ['race']

connection.close_connection()
