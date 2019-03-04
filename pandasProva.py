import utility
from resultsVisualization import tree_printer
from databaseConnection import DBConnection
from tabulate import tabulate
from pandas import pandas
from sklearn import tree

connection = DBConnection()
connection.database_connection()
query = "SELECT id, Age, Sex FROM censusdata limit 5"
result = connection.query(query)
print(tabulate(result,  tablefmt="fancy_grid"))
# https://pypi.org/project/tabulate/ per info su tabulate

the_frame = pandas.DataFrame.from_dict(result)

print(the_frame)
print(the_frame.dtypes)

"""
print(the_frame.head(2))               #prime righe della table
print(the_frame.tail(2))               #ultime righe della table
print(the_frame.index)
print(the_frame.sort_values(by='Age'))      #ordina table per value
"""

classifier = tree.DecisionTreeClassifier()
classifier.fit(the_frame[["id", "Age"]], the_frame["Sex"])
print(classifier)

tree_printer(utility.tree_path, tree, classifier, ["id", "Age"])
