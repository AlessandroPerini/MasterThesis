from oneHotEncoding import OneHotEncoding
from sklearn import tree
from utility import Utility


class Tests:

    @staticmethod
    def test_a_priori_free_tuple_selection(x, y):
        utility = Utility()
        classifier = tree.DecisionTreeClassifier()
        x, list_y = utility.preprocessing(x, y)
        classifier.fit(x, list_y)
        utility.tree_printer(classifier, x)
        utility.path_finder(classifier, x, list_y)
