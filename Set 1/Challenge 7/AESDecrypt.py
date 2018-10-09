import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii

def readFile(filename):
	with open(filename, 'r') as myfile:
		data = myfile.read().replace('\n', '')

	hexString = data.decode("base64").encode("hex")

	return hexString

if __name__ == "__main__":
	hexString = readFile("Test.txt")
	key = "YELLOW SUBMARINE"
	plainText = ''
	backend = default_backend()
	cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
	decryptor = cipher.decryptor()
	plainText = decryptor.update(binascii.unhexlify(hexString))
	print plainText