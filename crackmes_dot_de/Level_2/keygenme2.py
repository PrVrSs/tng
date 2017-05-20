def main(name='qwerty'):
    import os
    first = 19
    for i in os.uname()[1]:
        first += ord(i)
    second = (ord(name[-1]) + len(os.uname()[1])) * (len(name) + len(os.uname()[1]))
    third = name[0:2] + os.uname()[1][0:2]
    print(str(first) + '-' + str(second) + '-' + third)

if __name__ == '__main__':
    import sys
    kwargs = 'qwerty'
    if len(sys.argv) > 1:
        kwargs = sys.argv[1]
    main(kwargs)

