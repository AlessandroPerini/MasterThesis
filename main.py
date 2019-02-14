from databaseConnection import DBConnection
from tabulate import tabulate

connection = DBConnection()
connection.database_connection()
query = "SELECT * FROM censusdata limit 5"
result = connection.query(query)
print(tabulate(result, tablefmt="fancy_grid"))

# Per estrarre una colonna dei risultati
column_id = [item['id'] for item in result]
column_Age = [item['Age'] for item in result]

connection.close_connection()