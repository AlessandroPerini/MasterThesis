
from databaseConnection import DBConnection
from tabulate import tabulate
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import preprocessing
import pandas as pd
from sklearn import tree
from pydotplus import pydotplus
import collections

connection = DBConnection()
connection.database_connection()

connection = DBConnection()
connection.database_connection()
query = "SELECT  age, race FROM censusdata limit 5"
result = connection.query(query)
print(tabulate(result,  tablefmt="fancy_grid"))


the_frame = pd.DataFrame(result)

print(the_frame)
print(the_frame.dtypes)
#print(the_frame.head(2))               #prime righe della table
#print(the_frame.tail(2))               #ultime righe della table
#print(the_frame.index)
#print(the_frame.sort_values(by='age'))      #ordina table per value

X = the_frame[["race"]]
y = [0,1,0,1,0]         #sopra i 50 anni

race = the_frame.race.unique()
print(the_frame.race)

enc = preprocessing.OneHotEncoder(categories=[race])
encoded = enc.fit_transform(X).toarray()
print(encoded)
#print(enc.inverse_transform(encoded))          #ritrasforma con valori iniziali

print(the_frame)
the_frame = the_frame.drop(columns=['race'])
print(the_frame)


encoded_data_frame = pd.DataFrame(encoded)

print(encoded_data_frame)

the_frame = pd.concat([the_frame, encoded_data_frame], axis=1)

print(the_frame)

print(the_frame[0])

classifier = tree.DecisionTreeClassifier()
classifier.fit(the_frame.drop(columns=['age']), y)
print(classifier)


# Visualize data
dot_data = tree.export_graphviz(classifier,
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

