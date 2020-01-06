xor_ = [0xC1, 0x8F, 0x04, 0x08]
with open('ch13', 'rb') as f1:
    a = [hex(i) for i in f1.read()]
index_ = 0
for index in range(len(a)):
    if a[index] == '0x7a' and a[index+1] == '0x8e' and a[index+2] == '0x4' and a[index+3] == '0x8':
        index_ = index
new_ = bytearray()
for i in range(0, len(a)):
    new_.append(int(a[i], 16) ^ xor_[i % 4]) if i >= index_ else new_.append(int(a[i], 16))
with open('file', 'r+b') as fh:
    fh.write(new_)
