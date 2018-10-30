from Oracle27 import encryptionOracle, receiverOracle, checkKey
from Modules.AES import AESCBCdecrypt
from Modules.fixedXOR import fixedXOR

def findBlockSize():
	message = ""
	prevLen = len(encryptionOracle(message))
	blockSize = 0

	while (blockSize == 0):
		message += "C"
		blockSize = (len(encryptionOracle(message)) - prevLen)/2

	return blockSize

def extractKey():
	blockSize = findBlockSize()

	plainText = "C"*blockSize*4*2
	cipherText = encryptionOracle(plainText)

	cipherText = cipherText[:blockSize*2] + ("0"*blockSize*2) + cipherText[:blockSize*2] + cipherText[(blockSize*6):]

	try:
		receiverOracle(cipherText)
	except Exception as e:
		error, retrievedText = str(e).split(": ")

	retrievedText = retrievedText.encode("hex")

	P_1 = retrievedText[:blockSize*2]
	P_3 = retrievedText[(blockSize*4):(blockSize*6)]

	extractedKey = fixedXOR(P_1, P_3)

	print len(extractedKey)
	
	if checkKey(extractedKey.decode("hex")):
		print "YEAH!"
	else:
		print "LOLOLOLOL"

	print AESCBCdecrypt(extractedKey.decode("hex"), encryptionOracle(plainText), extractedKey).decode("hex")


extractKey()