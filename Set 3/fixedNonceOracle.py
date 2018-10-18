from AES import AESCTRencrypt
import os

key = os.urandom(16)

def readFileandEncrypt(filename):
	encrypted = []

	with open(filename, 'r') as myfile:
		for line in myfile:
			message = line.strip()
			message = message.decode("base64").encode("hex")
			encrypted.append(AESCTRencrypt(key, message, 0))
	return encrypted