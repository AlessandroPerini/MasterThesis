import pandas as pd
import prova
from prova import DBConnection
from prettytable import PrettyTable

connection = DBConnection()
connection.database_connection()
query = "SELECT * FROM censusdata limit 5"
result = connection.query(query)
print(result)

# Per stampare solo una colonna dei risultati
column = 'id'
column_list = [item[column] for item in result]
print(column_list)
