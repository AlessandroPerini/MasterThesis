
from databaseConnection import DBConnection
from tabulate import tabulate
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import numpy as np
from pandas import pandas
from sklearn import tree
from pydotplus import pydotplus
import collections
import graphviz

connection = DBConnection()
connection.database_connection()

connection = DBConnection()
connection.database_connection()
query = "SELECT id, Age, Sex FROM censusdata limit 5"
result = connection.query(query)
print(tabulate(result,  tablefmt="fancy_grid"))      #https://pypi.org/project/tabulate/ per info su tabulate

the_frame = pandas.DataFrame.from_dict(result)

print(the_frame)
print(the_frame.dtypes)
#print(the_frame.head(2))               #prime righe della table
#print(the_frame.tail(2))               #ultime righe della table
#print(the_frame.index)
#print(the_frame.sort_values(by='Age'))      #ordina table per value


classifier = tree.DecisionTreeClassifier()
classifier.fit(the_frame[["id", "Age"]], the_frame["Sex"])
print(classifier)


# Visualize data
dot_data = tree.export_graphviz(classifier,
                                feature_names=["id", "Age"],
                                out_file=None,
                                filled=True,
                                rounded=True)
graph = pydotplus.graph_from_dot_data(dot_data)

colors = ('turquoise', 'orange')
edges = collections.defaultdict(list)

for edge in graph.get_edge_list():
    edges[edge.get_source()].append(int(edge.get_destination()))

for edge in edges:
    edges[edge].sort()
    for i in range(2):
        dest = graph.get_node(str(edges[edge][i]))[0]
        dest.set_fillcolor(colors[i])

graph.write_png('tree.png')