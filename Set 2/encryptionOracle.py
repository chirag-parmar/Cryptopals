import os
import random
from AES import AESCBCencrypt, AESECBencrypt

def encryptionOracle(text, keySize=128): 
	
	leadingPad = os.urandom(random.randint(5,10))
	trailingPad = os.urandom(random.randint(5,10))

	text = leadingPad + text + trailingPad

	if random.randint(0,1):
		mode = "CBC"
		cipherText = AESCBCencrypt(os.urandom(keySize/8), text.encode("hex"), os.urandom(keySize/8).encode("hex"))
	else:
		mode = "ECB"
		cipherText = AESECBencrypt(os.urandom(keySize/8), text.encode("hex"))

	return cipherText, mode


if __name__ == "__main__":
	message = "YO YO YO CHIRAG!YO YO YO CHIRAG!"
	for i in range(10):
		print encryptionOracle(message)

