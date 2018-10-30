from Modules.AES import AESCTRencrypt, AESECBdecrypt, AESencrypt
from Modules.fixedXOR import fixedXOR
import random
import math
import os

globalKey = os.urandom(16)

def readFileandEncrypt(filename):

	with open(filename, 'r') as myfile:
		data = myfile.read()

	plainText = AESECBdecrypt("YELLOW SUBMARINE", data.decode("base64").encode("hex"))
		
	return AESCTRencrypt(globalKey, plainText, 0)

def big2little(a):
	littleString = "".join(reversed([a[i:i+2] for i in range(0, len(a), 2)]))
	return littleString

def edit(hexString, offset, newText, nonce=0, blockSize=16):
	hexLen = len(hexString)
	offset *= 2
	blockSize *= 2
	ctr = 0
	keyStream = ''

	for i in range(0, int(math.ceil(hexLen/(blockSize*1.0)))):
		hex_ctr = big2little(hex(ctr)[2:].zfill(16).rstrip("L"))
		hex_nonce = big2little(hex(nonce)[2:].zfill(16).rstrip("L"))
		ctr += 1
		keyStream += AESencrypt(globalKey, hex_nonce + hex_ctr)

	keyLen = len(keyStream)
	diffBytes = keyLen%hexLen
	if diffBytes > 0:
		keyStream = keyStream[:(-1)*diffBytes]

	if not offset < hexLen:
		raise Exception("offset off limits")

	seekKey = keyStream[offset:offset+2]
	newCipher = fixedXOR(newText.encode("hex"), seekKey)
	hexString = hexString[:offset] + newCipher + hexString[offset+2:]

	if not len(hexString) == hexLen:
		return False

	return hexString