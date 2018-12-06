from Modules.AES import AESCBCencrypt, AESCBCdecrypt
from Modules.SHA1 import SHA1
import random
import os

def hexit(message):
	h = SHA1()
	h.update(message)
	MAC = h.hexdigest()
	return MAC.decode("hex")

#A -> B
p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2

a = int(os.urandom(random.randint(100, 200)).encode("hex"), 16)%p
A = pow(g, a, p)

print "A -> M"
print
print "P: " + str(hex(p)[2:].rstrip("L"))
print "G: " + str(g)
print "A: " + str(A)
print

print "M -> B"
print
print "P: " + str(hex(p)[2:].rstrip("L"))
print "G: " + str(g)
print "A: " + str(hex(p)[2:].rstrip("L"))
print

b = int(os.urandom(random.randint(100, 200)).encode("hex"), 16)%p
B = pow(g, b, p)

print "B -> M"
print
print "B: " + str(B)
print

print "M -> A"
print
print "B: " + str(hex(p)[2:].rstrip("L"))
print

commonKeyA = pow(p, a, p)
messageA = "Cooking MC's like a pound of bacon"
iv = os.urandom(16).encode("hex")

encryptedMessage = AESCBCencrypt(hexit(str(commonKeyA))[0:16], messageA.encode("hex"), iv)

print
print "A -> M"
print "Encrypted Message: " + encryptedMessage + " " + iv
print

#intercept the message here
print
print " MITM succesfull"
print "Intercepted Message: " + AESCBCdecrypt(hexit(str(0))[0:16], encryptedMessage, iv).decode("hex")
print

print
print "M -> A"
print "Encrypted Message: " + encryptedMessage + " " + iv
print

commonKeyB = pow(p, b, p)

print
print " B -> M"
print "Decrypted Message: " + AESCBCdecrypt(hexit(str(commonKeyB))[0:16], encryptedMessage, iv).decode("hex")
print

print
print " M -> A"
print "Decrypted Message: " + AESCBCdecrypt(hexit(str(commonKeyB))[0:16], encryptedMessage, iv).decode("hex")
print