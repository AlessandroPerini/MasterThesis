from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import graphviz

iris = load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

estimator = DecisionTreeClassifier(max_leaf_nodes=3, random_state=0)
estimator.fit(X_train, y_train)

with open("fruit_classifier.pdf", "w") as f:
    f = tree.export_graphviz(estimator, out_file=f)
    graph = graphviz.Source(f)
    graph.render("iris")

from subprocess import check_call
check_call(['dot','-Tpng','InputFile.dot','-o','OutputFile.png'])