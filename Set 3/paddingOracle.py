from AES import AESCBCencrypt, AESCBCdecrypt
import random
import os

key = os.urandom(16)

def encryptionOracle(blockSize=16):
	lines = []
	
	with open('./Tests/17.txt', 'r') as testFile:
		for line in testFile:
			lines.append(line);

	message = lines[random.randint(0,len(lines)-1)].decode("base64")

	iv = os.urandom(blockSize).encode("hex")
	cipherText = AESCBCencrypt(key, message.encode("hex"), iv);

	return cipherText, iv

def paddingOracle(cipher, iv):
	try:
		cipher = AESCBCdecrypt(key, cipher, iv)
		return True
	except:
		return False


if __name__ == "__main__":
	cipher, iv = encryptionOracle()
	print paddingOracle(cipher, iv)
