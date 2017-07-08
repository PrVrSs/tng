import sys


def df(first, second, third):
    first_ = "0x" + first
    second_ = "0x" + second
    third_ = "0x" + third
    if (int(first_, 16) ^ int(second_, 16)) - int(third_, 16) > 0:
        result = (int(first_, 16) ^ int(second_, 16)) - int(third_, 16)
    else:
        result = (int("0x100", 16)+(int(first_, 16) ^ int(second_, 16))) - int(third_, 16)
    return result

hex_string = sys.argv[1]
user_name = "31"*14 + "0a" + "00"
salt = "31"*14 + "0a" + "00"

hex_string_list = [hex_string[i:i + 8] for i in range(0, len(hex_string), 8)]
user_name_list = [user_name[i:i+8] for i in range(0, len(hex_string), 8)]
salt_list = [salt[i:i+8] for i in range(0, len(hex_string), 8)]
result = ''
for index in range(4):
    h = [hex_string_list[index][i-2:i] for i in range(8, 0, -2)]
    u = [user_name_list[index][i:i+2] for i in range(0, 8, 2)]
    s = [salt_list[index][i:i+2] for i in range(0, 8, 2)]
    answer = map(df, h, u, s)
    for index_ in answer:
        result += chr(index_)
sys.stdout.write(result)
