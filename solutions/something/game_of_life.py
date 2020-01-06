import itertools


def neigbors(point):
    x, y = point
    for i, j in itertools.product(range(-1, 2), repeat=2):
        if x + i >= 0 and y + j >= 0 and any((i, j)):
            yield (x + i, y + j)


def advance(board, alive):
    newstate = set()
    recalc = board
    for point in recalc:
        count = sum([(neigh in alive) for neigh in neigbors(point)])
        if (count == 3 or count == 2) and point in alive:
            newstate.add(point)
        elif count == 3 and point not in alive:
            newstate.add(point)
    return newstate


map1 = []
width, height = [int(i) for i in input().split()]
for i in range(height):
    line = input()
    map1.append(list(line))
board = ((i, j) for i in range(height) for j in range(width))
alive = [(i, j) for i in range(height) for j in range(width) if map1[i][j] == '1']
answer = []
a = advance(board, alive)
for i in range(0, height):
    for j in range(0, width):
        answer.append(1) if (i, j) in a else answer.append(0)
for index, a in enumerate(answer):
    print(a, end='')
    if index % width == width-1:
        print()
