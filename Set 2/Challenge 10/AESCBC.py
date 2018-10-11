import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii
import sys

def fixedXOR(hexString1, hexString2, chunkSize = 128):
	hexLen1 = len(hexString1)
	hexLen2 = len(hexString2)

	interInt1 = 0
	interInt2 = 0
	XORString = ''
	i = 0

	if hexLen1 != hexLen2:
		raise Exception("unequal string lengths (" + str(hexLen1) +", " + str(hexLen2) + ")")
	elif hexLen1 == 0 or hexLen2 == 0:
		raise Exception("NULL String")
	elif chunkSize > 512:
		raise Exception("chunk size too big")
	else:
		if chunkSize > hexLen1:
			chunkSize = hexLen1
		while (hexLen1 - (i*chunkSize)) >= chunkSize:
			interInt1 = int(hexString1[i*chunkSize:i*chunkSize + chunkSize], 16)
			interInt2 = int(hexString2[i*chunkSize:i*chunkSize + chunkSize], 16)
			XORString += hex(interInt1^interInt2)[2:].zfill(chunkSize+1).rstrip("L")
			i+=1
		if hexLen1%chunkSize != 0:
			interInt1 = int(hexString1[(i*chunkSize):], 16)
			interInt2 = int(hexString2[(i*chunkSize):], 16)
			XORString += hex(interInt1^interInt2)[2:].zfill((hexLen1%chunkSize)+1).rstrip("L")

	return XORString

def padMsg(msg, toBytes, inHex = False):
	msgLen = len(msg)

	if inHex:
		diff = (toBytes-msgLen)/2
	else:
		diff = toBytes-msgLen

	if msgLen > toBytes:
		raise Exception("Can't reduce length while padding")
	elif diff > 16:
		raise Exception("Can't pad more than 16 bytes")
	else:
		for i in range(diff):
			if not inHex:
				msg += (hex(diff)[2:].zfill(2).rstrip("L")).decode("hex")
			else:
				msg += (hex(diff)[2:].zfill(2).rstrip("L"))
	return msg

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
	hexString = readFile("Test.txt")
	IV = hex(0)[2:].zfill(len(key)*2).rstrip("L")
	plainText = AESCBCdecrypt(key, hexString, IV)

	print plainText.decode("hex")