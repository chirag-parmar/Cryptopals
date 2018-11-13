from fixedXOR import fixedXOR
from SHA1 import SHA1
from MD4 import MD4

def HMAC(key, message, hashFunction):

	keyLen = len(key)

	if hashFunction == "SHA1":
		hash = hash_sha1
		blockSize = 64
		outputSize = 20
	elif hashFunction == "MD4":
		hash = hash_md4
		blockSize = 64
		outputSize = 16
	elif not hashFunction == "MD4" and not hashFunction == "SHA1":
		raise Exception("Hash Function not supported")

	if keyLen > blockSize:
		key = hash(key).decode("hex")

	if (keyLen < blockSize):
		key = key + "00".decode("hex")*(blockSize-keyLen)
	
	o_key_pad = fixedXOR(key.encode('hex'), ("5c" * blockSize)).decode("hex")
	i_key_pad = fixedXOR(key.encode("hex"), ("36" * blockSize)).decode("hex")

	return hash(o_key_pad + hash(i_key_pad + message).decode("hex"))

def hash_sha1(message):
	h = SHA1()
	h.update(message)
	return h.hexdigest()

def hash_md4(message):
	h = MD4()
	h.update(message)
	return h.hexdigest()

if  __name__ == "__main__":
	print HMAC("YELLOW SUBMARINE", "Chirag is a good guy", "SHA1")