import datetime


class FileWriter:

    path = 'performances.txt'
    f = open(path, "w+")

    def __init__(self, query_x, query_y, y):
        self.f.write(str(datetime.datetime.now()))
        self.f.write('\n\nQuery x: ' + str(query_x))
        self.f.write('\nQuery y: ' + str(query_y))
        self.f.write('\n\nDataframe y: \n' + str(y))
        self.f.close()

    def times_writer(self, times_list):
        f = open(self.path, "a+")
        f.write('\n\n' + '_' * 30 + ' Methods Performances ' + '_' * 30 + '\n')
        f.write('\nPR_Random: ' + str(times_list[0]) + ' seconds')
        f.write('\nPR_Cluster: ' + str(times_list[1]) + ' seconds')
        f.write('\nPO_Min: ' + str(times_list[2]) + ' seconds')
        f.write('\nPO_Most: ' + str(times_list[3]) + ' seconds')
        f.close()

    def explanations_writer(self, explanations_list):
        f = open(self.path, "a+")
        f.write('\n\n' + '_' * 30 + ' Methods Explanations ' + '_' * 30 + '\n')

        f.write('\nPR_Random:\n')
        for expl in explanations_list[0]:
            f.write(expl + '\n')

        f.write('\nPR_Cluster:\n')
        for expl in explanations_list[1]:
            f.write(expl + '\n')

        f.write('\nPO_Min:\n')
        for expl in explanations_list[2]:
            f.write(expl + '\n')

        f.write('\nPO_Most:\n')
        for expl in explanations_list[3]:
            f.write(expl + '\n')

        self.f.close()

    def purity_writer(self, purities):
        f = open(self.path, "a+")
        f.write('\n\n' + '_' * 30 + ' Methods Purities ' + '_' * 30 + '\n')
        f.write('\nPR_Random: ' + str(purities[0]) + ' %')
        f.write('\nPR_Cluster: ' + str(purities[1]) + ' %')
        f.write('\nPO_Min: ' + str(purities[2]) + ' %')
        f.write('\nPO_Most: ' + str(purities[3]) + ' %')
        self.f.close()

    def heights_writer(self, heights):
        f = open(self.path, "a+")
        f.write('\n\n' + '_' * 30 + ' Methods Max Heights ' + '_' * 30 + '\n')
        f.write('\nPR_Random: ' + str(heights[0]))
        f.write('\nPR_Cluster: ' + str(heights[1]))
        f.write('\nPO_Min: ' + str(heights[2]))
        f.write('\nPO_Most: ' + str(heights[3]))
        self.f.close()

    def number_important_nodes_writer(self, n_imp_nodes):
        f = open(self.path, "a+")
        f.write('\n\n' + '_' * 30 + ' Methods Number of Important Nodes ' + '_' * 30 + '\n')
        f.write('\nPR_Random: ' + str(n_imp_nodes[0]))
        f.write('\nPR_Cluster: ' + str(n_imp_nodes[1]))
        f.write('\nPO_Min: ' + str(n_imp_nodes[2]))
        f.write('\nPO_Most: ' + str(n_imp_nodes[3]))
        self.f.close()

    def best_method_writer(self, best_method, best_parameter):
        f = open(self.path, "a+")
        f.write('\n\n' + '_' * 30 + ' Best Method Selection ' + '_' * 30 + '\n')
        if best_method == 0:
            f.write('\nThe best method is Random and its parameter is: ' + str(best_parameter))
        if best_method == 1:
            f.write('\nThe best method is Cluster and its parameter is: ' + str(best_parameter))
        if best_method == 2:
            f.write('\nThe best method is Minimum Height first and its parameter is: ' + str(best_parameter))
        elif best_method == 3:
            f.write('\nThe best method is Most important node first and its parameter is: ' + str(best_parameter))
