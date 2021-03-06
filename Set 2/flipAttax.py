from CBCOracle import encryptionOracle, checkAdminOracle
from fixedXOR import fixedXOR
import itertools

def findBlockSize():
	message = ""
	prevLen = len(encryptionOracle(message))
	blockSize = 0

	while (blockSize == 0):
		message += "C"
		blockSize = (len(encryptionOracle(message)) - prevLen)/2

	return blockSize

def makeAdmin():
	blockSize = findBlockSize()

	inputText = "Z"*blockSize
	adminText = ";admin=true;f=k;"
	attaxText = fixedXOR(adminText.encode("hex"), inputText.encode("hex"))

	cipherText = encryptionOracle(inputText*2)
	cipherLen = len(cipherText)

	for i in range(cipherLen/(blockSize*2)-2):
		maskText = blockSize*i*2*"0" + attaxText + (cipherLen-(blockSize*2)-(blockSize*i*2))*"0"
		forgedText = fixedXOR(maskText, cipherText)
		if checkAdminOracle(forgedText):
			print "Hacked Through AES CBC mode"
			break

makeAdmin()