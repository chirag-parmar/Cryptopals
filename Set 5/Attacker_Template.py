from pwn import *

l = listen(1234)
r = remote('localhost', 2345)

p = int(l.recvline(keepends = False))
print "C->M: received p ", p
g = int(l.recvline(keepends = False))
print "C->M: received g ", g
A = int(l.recvline(keepends = False))
print "C->M: received A ", A

# Send on mitm parameters to server
print "M->S: sending params "
r.sendline(str(p))
r.sendline(str(g))
r.sendline(str(p))