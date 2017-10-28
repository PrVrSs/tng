from pylab import *
from numpy import random
from prettytable import PrettyTable


def main():
    pretty_table = PrettyTable()
    N = 10000
    y, x = [], []
    for j in range(1, 5):
        x_x = linspace(-6, 6, N)
        for i in x_x:
            a = random.uniform(-4, 4)
            if (i ** 2 + a ** 2) <= 16:
                x.append(i)
                y.append(a)
    else:
        x = x[:N]
        y = y[:N]
    a = list(map(lambda x1, x2: (x1-2) ** 2 + (x2-2) ** 2, x, y))
    b = list(map(lambda x1, x2: (x1-3) ** 2 + 4 * x2 ** 2, x, y))
    mas = np.array([list(i) for i in zip(a, b)])
    min_x, min_y = np.min(mas, 0)
    max_y = mas[np.argwhere(mas == min_x)[0][0]][1]
    pareto_x, pareto_y, pareto_x_v2, pareto_y_v2 = [], [], [], []
    pareto_x.append(min_x)
    pareto_y.append(max_y)
    pareto_x_v2.append(x[np.argwhere(mas == min_x)[0][0]])
    pareto_y_v2.append(y[np.argwhere(mas == min_x)[0][0]])
    while 1:
        x_next = inf
        y_next = -inf
        count = 0
        for i in mas:
            if not (not (i[0] < x_next) or not (i[0] > min_x)) and i[1] < max_y:
                x_next, y_next = i[0], i[1]
                res = count
            count += 1
        if x_next == inf:
            break
        pareto_x.append(x_next)
        pareto_y.append(y_next)
        pareto_x_v2.append(x[res])
        pareto_y_v2.append(y[res])
        min_x, max_y = x_next, y_next
    _, ax = plt.subplots()
    ax.plot(a, b, 'o')
    ax.plot(pareto_x, pareto_y, 'r')
    l, ax = plt.subplots()
    ax.plot(x, y, 'o')
    ax.plot(pareto_x_v2, pareto_y_v2, 'o')
    pretty_table.add_column("X1", pareto_x)
    pretty_table.add_column("X2", pareto_y)
    pretty_table.add_column("F1", pareto_x_v2)
    pretty_table.add_column("F2", pareto_y_v2)
    print(pretty_table)
    show()


if __name__ == '__main__':
    main()
