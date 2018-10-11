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

def AESECBencrypt(key, hexString):
	hexLen = len(hexString)
	keySize = len(key)*2
	cipherText = ''

	if (hexLen%keySize) != 0:
		hexString = padMsg(hexString, hexLen + (keySize-(hexLen%keySize)), True)

	hexLen = len(hexString)
	for i in range(0, hexLen, keySize):
		cipherText += AESencrypt(key, hexString[i:i+keySize])

	return cipherText

def AESECBdecrypt(key, hexString):
	hexLen = len(hexString)
	keySize = len(key)*2
	plainText = ''

	if hexLen%keySize != 0:
		raise Exception("16(n) byte cipher text required - " + str(hexLen))
	else:
		for i in range(0, hexLen, keySize):
			plainText += AESdecrypt(key, hexString[i:i+keySize])

	return plainText

def AESCBCencrypt(key, hexString, IV):
	hexLen = len(hexString)
	keySize = len(key)*2
	previousMsg = IV
	cipherText = ''

	if (hexLen%keySize) != 0:
		hexString = padMsg(hexString, hexLen + (keySize-(hexLen%keySize)), True)

	hexLen = len(hexString)

	for i in range(0, hexLen, keySize):
		previousMsg = AESencrypt(key, fixedXOR(hexString[i:i+keySize], previousMsg))
		cipherText += previousMsg

	return cipherText

def AESCBCdecrypt(key, hexString, IV):
	hexLen = len(hexString)
	keySize = len(key)*2
	previousMsg = IV
	plainText = ''

	hexLen = len(hexString)
	if hexLen%keySize != 0:
		raise Exception("16(n) byte cipher text required- " + str(hexLen))
	else:
		for i in range(0, hexLen, keySize):
			plainText += fixedXOR(AESdecrypt(key, hexString[i:i+keySize]), previousMsg)
			previousMsg = hexString[i:i+keySize]

	paddingNum = int(plainText[len(plainText)-2:])
	if paddingNum < (keySize/2):
		plainText = plainText[:len(plainText)-(paddingNum*2)]

	return plainText

if __name__ == "__main__":
	key = "YELLOW SUBMARINE"
	hexString = readFile("./Tests/10.txt")
	IV = hex(0)[2:].zfill(len(key)*2).rstrip("L")
	plainText = AESCBCdecrypt(key, hexString, IV)

	print plainText.decode("hex")