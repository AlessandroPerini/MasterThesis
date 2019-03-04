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
