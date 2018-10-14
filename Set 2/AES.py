from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from fixedXOR import fixedXOR
from padding import padMsg
import binascii
import sys
import os

def readFile(filename):
	with open(filename, 'r') as myfile:
		data = myfile.read().replace('\n', '')

	hexString = data.decode("base64").encode("hex")

	return hexString

def AESdecrypt(key, hexString):
	backend = default_backend()
	decryptor = Cipher(algorithms.AES(key), modes.ECB(), backend=backend).decryptor()
	plainText = decryptor.update(hexString.decode("hex")) + decryptor.finalize()
	return plainText.encode("hex")

def AESencrypt(key, hexString):
	backend = default_backend()
	encryptor = Cipher(algorithms.AES(key), modes.ECB(), backend=backend).encryptor()
	cipherText =  encryptor.update(hexString.decode("hex")) + encryptor.finalize()
	return cipherText.encode("hex")

def isValidPadding(plainText, blockSize=16):
	padCount = int(plainText[-1:].encode("hex"),16) if int(plainText[-1:].encode("hex"),16) < blockSize else 0
	interText = plainText[-padCount:]
	for i in range(padCount):
		if int(interText[i].encode("hex"),16) != padCount:
			raise Exception("Invalid Padding")

	return plainText[:(-1)*padCount]

def AESECBencrypt(key, hexString):
	hexLen = len(hexString)
	blockSize = 32
	cipherText = ''

	if (hexLen%blockSize) != 0:
		hexString = padMsg(hexString, hexLen + (blockSize-(hexLen%blockSize)), True, blockSize)

	hexLen = len(hexString)
	for i in range(0, hexLen, blockSize):
		cipherText += AESencrypt(key, hexString[i:i+blockSize])

	return cipherText

def AESECBdecrypt(key, hexString):
	hexLen = len(hexString)
	blockSize = 32
	plainText = ''

	if hexLen%blockSize != 0:
		raise Exception("16(n) byte cipher text required - " + str(hexLen))
	else:
		for i in range(0, hexLen, blockSize):
			plainText += AESdecrypt(key, hexString[i:i+blockSize])

	plainText = isValidPadding(plainText.decode("hex"))

	return plainText.encode("hex")

def AESCBCencrypt(key, hexString, IV):
	hexLen = len(hexString)
	blockSize = 32
	previousMsg = IV
	cipherText = ''

	if (hexLen%blockSize) != 0:
		hexString = padMsg(hexString, hexLen + (blockSize-(hexLen%blockSize)), True)

	hexLen = len(hexString)

	for i in range(0, hexLen, blockSize):
		previousMsg = AESencrypt(key, fixedXOR(hexString[i:i+blockSize], previousMsg))
		cipherText += previousMsg

	return cipherText

def AESCBCdecrypt(key, hexString, IV):
	hexLen = len(hexString)
	blockSize = 32
	previousMsg = IV
	plainText = ''

	hexLen = len(hexString)
	if hexLen%blockSize != 0:
		raise Exception("16(n) byte cipher text required- " + str(hexLen))
	else:
		for i in range(0, hexLen, blockSize):
			plainText += fixedXOR(AESdecrypt(key, hexString[i:i+blockSize]), previousMsg)
			previousMsg = hexString[i:i+blockSize]

	plainText = isValidPadding(plainText.decode("hex"))
	
	return plainText.encode("hex")

if __name__ == "__main__":
	key = "YELLOW SUBMARINE"
	hexString = readFile("./Tests/10.txt")
	IV = hex(0)[2:].zfill(len(key)*2).rstrip("L")
	plainText = AESCBCdecrypt(key, hexString, IV)

	print plainText.decode("hex")