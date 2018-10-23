from MT19937 import MT19937
from fixedXOR import fixedXOR
import random
import os

universalKey = ""
for i in range(16):
	universalKey += str(random.randint(0,1))

def encrypt(key, message):
	if len(key) > 16:
		raise Exception("key greater than 16 bits")

	keyStream = ''
	message = message.encode("hex")
	msgLen = len(message)
	seed = int(key,2)

	mt = MT19937(seed)
	for i in range(msgLen/8 + 3):
		keyStream += hex(mt.temper())[2:].zfill(8).rstrip('L')

	keyLen = len(keyStream)
	diffBytes = (keyLen - msgLen)
	if diffBytes > 0:
		tempKeyStream = keyStream[:(-1)*diffBytes]
		return fixedXOR(tempKeyStream, message)
	else:
		return fixedXOR(keyStream, message)

def decrypt(key, cipher):
	if len(key) > 16:
		raise Exception("key greater than 16 bits")

	keyStream = ''
	cipherLen = len(cipher)
	seed = int(key,2)

	mt = MT19937(seed)
	for i in range(cipherLen/8 + 1):
		keyStream += hex(mt.temper())[2:].zfill(8).rstrip('L')

	keyLen = len(keyStream)
	diffBytes = (keyLen - cipherLen)
	if diffBytes > 0:
		tempKeyStream = keyStream[:(-1)*diffBytes]
		return fixedXOR(tempKeyStream, cipher)
	else:
		return fixedXOR(keyStream, cipher)

def encryptionOracle(message):

	global universalKey

	print universalKey

	prefix = os.urandom(random.randint(5,30))
	
	message = prefix + message

	return encrypt(universalKey, message)

if __name__ == "__main__":
	print decrypt("1101001100001011", encrypt("1101001100001011", "Cooking MC's like a pound of a bacon")).decode("hex")
	print encryptionOracle("Cooking MC's like a pound of a bacon""")