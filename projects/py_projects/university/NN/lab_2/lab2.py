import random
import time
import math
from functools import reduce

list_merge = lambda s: reduce(lambda d, el: d.extend(el) or d, s, [])


class KohonenMap(object):
    def __init__(self, map_size: tuple=(3, 3), weight_size: int=3, ):
        self._neuron_list = []
        self._weight_size = weight_size
        self._map_size = map_size
        self._number_of_epochs = 100
        self._time = 0
        self._data = []
        self._data_with_class = []
        self._initial_learning_rate = 0.1
        self._number_training_vector = 0
        self._dump = None
        self.create_map()
        self.read_data('lab_2/data.txt')

    def create_map(self) -> None:
        self._neuron_list = [[Neuron(self._weight_size) for _ in range(self._map_size[1])] for _ in range(self._map_size[0])]

    def study(self, study: str = 'iterative') -> None:
        start_time = time.time()
        if study == 'iterative':
            self._iterative()
        elif study == 'batch_map':
            self._batch_map()
            [self._neuron_list[i][j].zero_data_list() for i in range(self._map_size[0]) for j in range(self._map_size[1])]
        else:
            assert False
        self._time = time.time() - start_time
        self.check_status()

    def check_status(self):
        for index_i in range(self._map_size[0]):
            for index_j in range(self._map_size[1]):
                self._neuron_list[index_i][index_j].status = True if self._neuron_list[index_i][index_j]._number_of_wins > 5 else False

    def get_time(self) -> int:
        return self._time

    def _find_winner_neuron(self, input_data: list) -> tuple:
        """
        :param input_data: вектор данных
        :return: индексы победителя
        """
        max_ = -math.inf
        index_winner = 0
        for index, neuron in enumerate(list_merge(self._neuron_list)):
            activation_function = math.exp(-self.euclidean_metric(neuron.weight_list, input_data))
            if max_ < activation_function and neuron.status is True:
                max_ = activation_function
                index_winner = index
        self._neuron_list[index_winner // self._map_size[0]][index_winner % self._map_size[0]].win()
        return index_winner // self._map_size[0], index_winner % self._map_size[0]

    @staticmethod
    def euclidean_metric(vector_1: list, vector_2: list) -> float:
        return math.sqrt(sum((math.pow(vector_1[index] - vector_2[index], 2) for index in range(len(vector_2)))))

    @staticmethod
    def error_data(vector_1: list, vector_2: list) -> float:
        return sum((math.pow(vector_1[index] - vector_2[index], 2) for index in range(len(vector_2))))

    def _iterative(self):

        for ii in range(self._number_of_epochs):
            error_all = 0
            for number_training_vector, training_vector in enumerate(self._data):
                self._number_training_vector += 1
                # self._number_training_vector = ii+1
                winner_x, winner_y = self._find_winner_neuron(training_vector)
                error_all += self.error_data(training_vector, self._neuron_list[winner_x][winner_y].weight_list)
                for index, neuron in enumerate(list_merge(self._neuron_list)):
                    if neuron.status is True:
                        current_x, current_y = index // self._map_size[0], index % self._map_size[0]
                        for index_2 in range(len(training_vector)):
                            neuron.weight_list[index_2] += self._training_speed() \
                                                       * self._distance_function((winner_x, winner_y), (current_x, current_y)) \
                                                       * (training_vector[index_2] - neuron.weight_list[index_2])
            #self.check_status()
            # print("epochs: {} error: {}".format(ii, error_all / len(self._data)))

    def _batch_map(self):

        for ii in range(self._number_of_epochs):
            error_all = 0
            for vector in self._data:
                winner_x, winner_y = self._find_winner_neuron(vector)
                self._neuron_list[winner_x][winner_y].data_list.append(vector)
                error_all += self.error_data(vector, self._neuron_list[winner_x][winner_y].weight_list)
            print("epochs: {} error: {}".format( ii, error_all / len(self._data)))
            # [print(self._neuron_list[i][j]._number_of_wins) for i in range(self._map_size[0]) for j in range(self._map_size[1])]
            self.check_status()
            for index, neuron_1 in enumerate(list_merge(self._neuron_list)):
                self._number_training_vector += 1
                # self._number_training_vector = ii +1
                a_upper = [0] * len(neuron_1.weight_list)
                a_botom = [0] * len(neuron_1.weight_list)
                # neuron_1.zero_weight_list()
                if neuron_1.status is True:
                    for index_2, neuron_2 in enumerate(list_merge(self._neuron_list)):
                        if neuron_2.status is True:
                            neuron_1_x, neuron_1_y = index // self._map_size[0], index % self._map_size[0]
                            neuron_2_x, neuron_2_y = index_2 // self._map_size[0], index_2 % self._map_size[0]
                            for index_3 in range(len(neuron_1.weight_list)):
                                a_upper[index_3] += (self.sum_(neuron_2, index_3) * self._distance_function((neuron_1_x, neuron_1_y), (neuron_2_x, neuron_2_y)))
                                a_botom[index_3] += (self._distance_function((neuron_1_x, neuron_1_y), (neuron_2_x, neuron_2_y)) * len(neuron_2.data_list))
                    for index_3 in range(len(neuron_1.weight_list)):
                        neuron_1.weight_list[index_3] = a_upper[index_3] / a_botom[index_3]

    @staticmethod
    def sum_(neuron, index: int):
        return sum([x[index] for x in neuron.data_list])

    def _training_speed(self) -> float:
        tau2 = 500  # – параметр, регулирующий убывание скорости обучения
        return self._initial_learning_rate * math.exp(-(self._number_training_vector / tau2))

    def _distance_function(self, winner: tuple = (None,), current: tuple = (None,)) -> float:
        d = pow(self.euclidean_metric(list(winner), list(current)), 2)
        t = 500  # – предполагаемое время обучения
        sigma_zero = min(self._map_size) // 2
        tau = t / sigma_zero
        sigma = sigma_zero * math.exp(-(self._number_training_vector / tau))
        try:
            result = math.exp(-(d / (2 * math.pow(sigma, 2))))
        except ZeroDivisionError:
            # print(sigma)
            # print(2 * math.pow(sigma, 2))
            result = math.exp(-(d / ((2 * math.pow(sigma, 2)) + 0.001)))
        return result

    def save(self, dump_file: str) -> None:
        with open(dump_file, 'wb') as w_file:
            for index_i in range(self._map_size[0]):
                for index_j in range(self._map_size[1]):
                    pro_type_1 = 0
                    pro_type_2 = 0
                    for vector_ in self._neuron_list[index_i][index_j].data_list:
                        if str(vector_[-2]) == "1.0" and str(vector_[-1]) == "0.0":
                            pro_type_1 += 1
                        elif str(vector_[-2]) == "0.0" and str(vector_[-1]) == "1.0":
                            pro_type_2 += 1
                    try:
                        pro_type_1 /= len(self._neuron_list[index_i][index_j].data_list)
                        pro_type_2 /= len(self._neuron_list[index_i][index_j].data_list)
                    except ZeroDivisionError:
                        pro_type_1 = 0
                        pro_type_2 = 0
                    pro_type_1 *= 100
                    pro_type_2 *= 100
                    w_file.write("Neuron[{}][{}] weight: {}\n".format(index_i, index_j, self._neuron_list[index_i][index_j].weight_list).encode())
                    w_file.write("Status: {}\n".format('Alive' if self._neuron_list[index_i][index_j].status else 'Death').encode())
                    w_file.write("****************************Data info*********************************************\n\n".encode())
                    w_file.write("type 1 0: {}%\ntype 0 1: {}%\n".format(pro_type_1, pro_type_2).encode())
                    # for vector_ in self._neuron_list[index_i][index_j].data_list:
                    #     w_file.write("{}\n".format([x for x in vector_]).encode())
                    # w_file.write("\n".format().encode())
                    w_file.write("*************************************************************************\n\n".encode())

    def categorize(self):
        error_all = 0
        for vector in self._data_with_class:
            winner_x, winner_y = self._find_winner_neuron(vector[:self._weight_size])
            self._neuron_list[winner_x][winner_y].data_list.append(vector)
            error_all += self.error_data(vector, self._neuron_list[winner_x][winner_y].weight_list)
        error_all /= len(self._data_with_class)
        print("Error: {}".format(error_all))
        return error_all

    def read_data(self, file: str) -> None:
        with open(file, 'r') as data:
            for line in data:
                self._data.append(list(map(lambda x: float(x), line.split(' ')[:self._weight_size])))
                self._data_with_class.append(list(map(lambda x: float(x), line.split(' '))))


    def __str__(self):
        ret_str = []
        list_zip = list(zip([x for x in range(self._map_size[0] ** 2)], [self._neuron_list[i][j].weight_list for i in range(self._map_size[0]) for j in range(self._map_size[1])]))
        ret_str.append('*************Kohonen Map info*******************')
        ret_str.append('{}'.format([(x, y) for x, y in list_zip]))
        return '\n'.join(ret_str)


class Neuron(object):
    __slots__ = ['_weight_list', '_number_of_wins', '_belonging', 'data_list', 'status', ]

    def __init__(self, weight_size: int = 0):
        random.seed()
        self._weight_list = [random.random() for _ in range(weight_size)]
        self._number_of_wins = 0
        self._belonging = None
        self.data_list = []
        self.status = True

    # def change_weight(self) -> None:
    #     pass

    def win(self) -> None:
        self._number_of_wins += 1

    def zero_weight_list(self) -> None:
        for index in range(len(self._weight_list)):
            self._weight_list[index] = 0.0

    def zero_data_list(self) -> None:
        self.data_list = []

    def get_weight_list(self) -> list:
        return self._weight_list

    @property
    def weight_list(self):
        return self._weight_list

    @weight_list.setter
    def weight_list(self, weight_list: list):
        self._weight_list = weight_list

    @weight_list.getter
    def weight_list(self) -> list:
        return self._weight_list
