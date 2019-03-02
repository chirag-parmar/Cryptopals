from Modules.AES import AESCBCencrypt, AESCBCdecrypt
from Modules.SHA1 import SHA1
from Modules.HMAC import HMAC
import random
import os

def hexit(message):
	h = SHA1()
	h.update(message)
	MAC = h.hexdigest()
	return MAC.decode("hex")

#C&S Agree on parameters
server_p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
server_g = 2
server_k = 3
server_I = "chirag@cryptopals"
server_P = "YELLOW SUBMARINE"

client_p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
client_g = 2
client_k = 3
client_I = "chirag@cryptopals"
client_P = "YELLOW SUBMARINE"

#S
server_salt = int(os.urandom(random.randint(100, 200)).encode("hex"), 16)

server_xH = hexit(str(server_salt) + server_P)
server_x = int(server_xH.encode("hex"), 16)

server_v = pow(server_g, server_x, server_p)

server_x = 0
server_xH = ""

#C -> S
client_a = int(os.urandom(random.randint(100, 200)).encode("hex"), 16)%client_p
client_A = pow(client_g, client_a, client_p)

print "C -> S"
print
print "I: " + client_I
print "A: " + str(client_A)
print

if(client_I == server_I):
	server_A = client_A

#S -> C
server_b = int(os.urandom(random.randint(100, 200)).encode("hex"), 16)%server_p
server_B = server_k*server_v + pow(server_g, server_b, server_p)

print "S -> C"
print
print "Salt: " + str(server_salt)
print "B: " + str(server_B)
print

client_salt = server_salt
client_B = server_B

#C,S
client_uH = hexit(str(client_A) + str(client_B))
client_u = int(client_uH.encode("hex"), 16)

server_uH = hexit(str(server_A) + str(server_B))
server_u = int(server_uH.encode("hex"), 16)

#C
client_xH = hexit(str(client_salt) + client_P)
client_x = int(client_xH.encode("hex"), 16)

client_v = pow(client_g, client_x, client_p)

temp1 = (client_B - (client_k * client_v))
temp2 = (client_a + (client_u*client_x))
client_S = pow(temp1, temp2, client_p)
client_K = hexit(str(client_S))

#S
server_S = pow((server_A*pow(server_v, server_u, server_p)), server_b, server_p)
server_K = hexit(str(server_S))

#C -> S
client_hmac = HMAC(client_K, str(client_salt), "SHA1")

print "C -> S"
print
print "HMAC: " + client_hmac
print

server_received_hmac = client_hmac
server_hmac = HMAC(server_K, str(server_salt), "SHA1")

print "S -> C"
print
if(server_hmac == server_received_hmac):
	print "Response: OK"
