from oneHotEncoding import OneHotEncoding
from sklearn import tree
from utility import Utility


class Tests:

    @staticmethod
    def test_a_priori_free_tuples_selection(x, y):
        utility = Utility()
        classifier = tree.DecisionTreeClassifier()
        x, y, list_y = utility.preprocessing(x, y)
        classifier.fit(x, list_y)
        utility.tree_printer(classifier, x)
        utility.path_finder(classifier, x, list_y)

    @staticmethod
    def test_all_free_tuples_selection(x,y):
        """
        :param x: dataframe_x
        :param y: dataframe_y
        :return: fitted classifier + prints the tree
        """
        utility = Utility()
        classifier = tree.DecisionTreeClassifier()
        y = utility.transform_y_to_all_results(x, y)
        y = OneHotEncoding().encoder(y, x)
        x = OneHotEncoding().encoder(x, x)
        x, y, list_y = utility.y_creator(x, y)
        classifier.fit(x, list_y)
        utility.tree_printer(classifier, x)
        return classifier, x, y, list_y
