from lab_2 import KohonenMap
from lab_1 import NeuralNetwork
import click


@click.command()
@click.option('--lab_number', default=2, help='lab_number.')
@click.option('--map_size', default=8, help='map_size.')
@click.option('--weight_size', default=9, help='weight_size.')
@click.option('--study_mode', default='batch_map', help='study_mode: iterative or batch_map')
def main(lab_number, map_size, weight_size, study_mode):
    if lab_number == 1:
        er = []
        for _ in range(1):
            my_network = NeuralNetwork()
            layer_info = [13, 10, 15, 21, 15, 7, 8, 4, 5, 1]
            my_network.create_network_layer(layer_info, 30)
            my_network.train(1000)
            my_network.check()

            er.append(my_network.error)
        sr_arif = sum(er) / 1
        print("sr_arif: {}".format(sr_arif))
        sko = [(i-sr_arif) ** 2 for i in er]

        sko_ans = sum(sko) / 1
        print("sko: {}".format(sko_ans))

    elif lab_number == 2:
        time_ = []
        for _ in range(2):
            a = KohonenMap(map_size=(map_size, map_size), weight_size=weight_size)
            a.study(study=study_mode)
            error = a.categorize()
            a.save('lab_2/s.txt')
            # print(a)
            print(a._time)
            time_.append(error)
        sr_arif = sum(time_) / 2
        print("sr_arif: {}".format(sr_arif))
        sko = [(i - sr_arif) ** 2 for i in time_]
        sko_ans = sum(sko) / 2
        print("sko: {}".format(sko_ans))

    else:
        print("Only Two Laboratory!")


if __name__ == "__main__":
    main()
