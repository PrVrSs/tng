import random
import math
import numpy as np


class NeuralNetwork(object):

    def __init__(self):
        self._neural_layer_list = []
        self.alpha = 10
        self.epsilon = 0.0001
        self.len_vector_data = 0
        self.data_vector = []
        self.check_data_vector = []
        self.data_file = "lab_1/data.txt"
        self.error = 0

    def create_network_layer(self, neural_layer_size: list, start_layer_weight_size):
        self.len_vector_data = start_layer_weight_size
        self.read_data_file(self.len_vector_data)
        self._neural_layer_list = [NeuralLayer(neural_layer_size[0], self.len_vector_data)]
        for i in range(1, len(neural_layer_size)):
            self._neural_layer_list += [NeuralLayer(neural_layer_size[i], len(self._neural_layer_list[-1].neuron_list))]

    def train(self, number: int=0) -> None:

        for i in range(number):
            error_all = 0
            for index_train, train_vector in enumerate(self.data_vector):

                # прямой проход
                self._neural_layer_list[0].direct_distribution(train_vector[1], True)
                for index, neural_layer_list in enumerate(self._neural_layer_list[1:]):
                    neural_layer_list.direct_distribution(self._neural_layer_list[index].neuron_list)

                # ошибка
                error = self.check_error([train_vector[0]])
                error_all += error
                # print("{}: {}".format(train_vector, self.data_vector[train_vector]))
                # if i > 100:
                #    print("ideal: {} out: {}".format(train_vector[0], self._neural_layer_list[-1].neuron_list[0].out))
                # print("{}: {}".format(index_train, error))

                # обратный проход
                self._neural_layer_list[-1].find_delta([train_vector[0]])  # случай последнего слоя
                for index, neural_layer_list in enumerate(reversed(self._neural_layer_list[1:])):
                    neural_layer_list.return_distribution(self._neural_layer_list[-index - 2].neuron_list)
                self._neural_layer_list[0].return_distribution(train_vector[1], True)  # когда первый слой и ненадо считать дельту4
            print("ep error: {} ".format(error_all))

    def check(self):
        error_all = 0
        for index_check, check_vector in enumerate(self.check_data_vector):
            self._neural_layer_list[0].direct_distribution(check_vector[1], True)
            for index, neural_layer_list in enumerate(self._neural_layer_list[1:]):
                neural_layer_list.direct_distribution(self._neural_layer_list[index].neuron_list)
            error = self.check_error([check_vector[0]])
            error_all += error
            print("ideal: {} out: {}".format(check_vector[0], self._neural_layer_list[-1].neuron_list[0].out))
        self.error = error_all
        print("check error: {} ".format(error_all))

    def check_error(self, answer: list) -> float:
        return self._neural_layer_list[-1].check(answer)

    def read_data_file(self, len_vector_data: int):

        with open(self.data_file, "r") as data_file:
            list_vector = []
            for line in data_file:
                list_vector.append(float(line.split(' ')[1].strip('\n')))
        int(len(list_vector) * 0.8)
        _max = max(list_vector)
        # list_vector = [i / _max for i in list_vector]
        new_list = list_vector[:]

        list_vector = [i - new_list[index] for index, i in enumerate(new_list[1:])]

        train_list_vector = list_vector[:int(len(list_vector) * 0.8)]
        check_list_vector = list_vector[int(len(list_vector) * 0.8):]

        for i in range(self.len_vector_data+1, len(train_list_vector)):
            tr_vector = []
            for j in train_list_vector[i-self.len_vector_data-1:i-1]:
                    tr_vector.append(j)
            self.data_vector.append((train_list_vector[i-1], tr_vector ))

        for i in range(self.len_vector_data+1, len(check_list_vector)):
            tr_vector = []
            for j in check_list_vector[i-self.len_vector_data-1:i-1]:
                    tr_vector.append(j)
            self.check_data_vector.append((check_list_vector[i-1], tr_vector ))


class NeuralLayer(object):

    def __init__(self, number_of_neuron, number_of_weight):
        self.neuron_list = [Neuron(number_of_weight) for _ in range(number_of_neuron)]

    def direct_distribution(self, previous_layer_neuron_list: list, first: bool = False):
        for neuron in self.neuron_list:
            distribution = 0
            for index, previous_neuron in enumerate(previous_layer_neuron_list):
                if not first:
                    distribution += (previous_neuron.out * neuron.weight_list[index])
                else:  # если слой первый, то передается просто список значений типа float
                    distribution += (float(previous_neuron) * neuron.weight_list[index])
            neuron.out = self.sigmoid(distribution)

    def return_distribution(self, pr_layer_neuron_list: list, first: bool = False):
        alpha = 0.01
        epsilon = 0.01

        for index_1, previous_neuron in enumerate(pr_layer_neuron_list):
            if not first:
                delta = 0
                for index_2, neuron in enumerate(self.neuron_list):
                    # print(neuron.weight_list[index_1])
                    # print(len(neuron.weight_list))
                    delta += (neuron.weight_list[index_1] * neuron.delta)

                    grad = previous_neuron.out * neuron.delta
                    delta_weight = epsilon * grad + alpha * neuron.previous_weight_list[index_1]
                    # print(delta_weight)
                    neuron.weight_list[index_1] += delta_weight
                    neuron.previous_weight_list[index_1] = delta_weight
                delta *= self.sigmoid_output_to_derivative(previous_neuron.out)
                previous_neuron.delta = delta
            else:
                for index_2, neuron in enumerate(self.neuron_list):
                    grad = float(previous_neuron) * neuron.delta
                    delta_weight = epsilon * grad + alpha * neuron.previous_weight_list[index_1]

                    neuron.weight_list[index_1] += delta_weight
                    neuron.previous_weight_list[index_1] = delta_weight

    def find_delta(self, ideal):
        for index, neuron in enumerate(self.neuron_list):
            neuron.delta = (float(ideal[index]) - neuron.out) * self.sigmoid_output_to_derivative(neuron.out)

    @staticmethod
    def sigmoid(x: float) -> float:
        return 1 / (1 + math.exp(-x))

    def check(self, answer: list) -> float:
        result = 0

        for index, neuron in enumerate(self.neuron_list):
            result += ((float(answer[index]) - neuron.out) ** 2)
        result /= len(answer)
        return result

    @staticmethod
    def sigmoid_output_to_derivative(x: float) -> float:
            return x * (1 - x)


class Neuron(object):

    def __init__(self, weight_size: int = 0):
        random.seed()
        self.weight_list = [random.random() for _ in range(weight_size)]
        self.delta_list = [random.random() for _ in range(weight_size)]
        self.previous_weight_list = [0 for _ in range(weight_size)]
        self.direct_distribution = 0
        self.out = 0
        self.previous_weight = 0
        self.delta = 0
        self.old_weight = 0
