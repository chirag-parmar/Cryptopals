import os
import random
from AES import AESCBCencrypt, AESECBencrypt

globalKey = os.urandom(24)

def encryptionOracle(text):

	trailingPad = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
	text = text + trailingPad.decode("base64")

	cipherText = AESECBencrypt(globalKey, text.encode("hex"))

	return cipherText


if __name__ == "__main__":
	message = "YO YO YO CHIRAG!YO YO YO CHIRAG!"

	for i in range(10):
		print encryptionOracle(message)

