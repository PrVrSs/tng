def main(name='qwerty'):
    len_name = len(name)-1
    answer = (ord(name[-1]) + ord(name[-1])) * len_name
    answer *= answer * 0x32
    print(answer)

if __name__ == '__main__':
    import sys
    kwargs = 'qwerty'
    if len(sys.argv) > 1:
        kwargs = sys.argv[1]
    main(kwargs)
