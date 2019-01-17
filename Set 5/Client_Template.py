from pwn import *

r = remote('localhost', 1234)

p = 2
g = 3
A = 4

print "C: Sending initial DH params"
r.sendline(str(p))
r.sendline(str(g))
r.sendline(str(A))