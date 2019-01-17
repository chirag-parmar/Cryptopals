from pwn import *

s = listen(2345)

p = int(s.recvline(keepends = False))
print "S: received p ", p
g = int(s.recvline(keepends = False))
print "S: received g ", g
A = int(s.recvline(keepends = False))
print "S: received A ", A
