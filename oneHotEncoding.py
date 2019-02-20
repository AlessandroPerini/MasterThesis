
from databaseConnection import DBConnection
from tabulate import tabulate
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import preprocessing
import pandas as pd
from sklearn import tree
from utility import Utility

connection = DBConnection()
connection.database_connection()

connection = DBConnection()
connection.database_connection()
query = "SELECT  age, race FROM censusdata limit 10"
result = connection.query(query)
#print(tabulate(result,  tablefmt="fancy_grid"))


the_frame = pd.DataFrame(result)

print(the_frame)
print(the_frame.dtypes)

#print(the_frame.head(2))               #prime righe della table
#print(the_frame.tail(2))               #ultime righe della table
#print(the_frame.index)
#print(the_frame.sort_values(by='age'))      #ordina table per value

X = the_frame[["race"]]
y = [0,1,0,1,0,1,1,1,1,1]         #sopra i 50 anni

race = the_frame.race.unique()
print(race)

#selezionare in automatico colonne non int e farne il onehot encoding

enc = preprocessing.OneHotEncoder(categories=[race])
encoded = enc.fit_transform(X).toarray()
print(encoded)
#print(enc.inverse_transform(encoded))          #ritrasforma con valori iniziali

print(the_frame)
the_frame = the_frame.drop(columns=['race'])
print(the_frame)

encoded_data_frame = pd.DataFrame(encoded)
encoded_data_frame.columns = race

print(encoded_data_frame)

the_frame = pd.concat([the_frame, encoded_data_frame], axis=1)

print(the_frame)

classifier = tree.DecisionTreeClassifier()
classifier.fit(the_frame, y)
print(classifier)

headers = list(the_frame.columns.values)
print(headers)

Utility().tree_printer(classifier, headers)
