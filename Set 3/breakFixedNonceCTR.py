from crackSingleXOR import crackSingleXOR, scoreText
from fixedXOR import fixedXOR
from repeatKeyXOR import repeatKeyXOR
from fixedNonceOracle import readFileandEncrypt

def moldMatrix(hexStrings, keyLen):
	repeatBins = ["" for x in range(keyLen)]

	for encryption in hexStrings:
		for i in range(0, len(encryption),2):
			repeatBins[(i/2)] += encryption[i:i+2]

	return repeatBins

if __name__ == "__main__":
	encryptedStrings = readFileandEncrypt("./Tests/20.txt")
	maxLen = 0.0
	key = ''

	for encryption in encryptedStrings:
		if(len(encryption) > maxLen):
			maxLen = len(encryption)

	repeatStrings = moldMatrix(encryptedStrings, maxLen/2)
	for eachString in repeatStrings:
		if len(eachString) > 0:
			key += crackSingleXOR(eachString)
		else:
			key += hex(0)[2:].zfill(2)

	keyLen = 0
	diffBytes = 0
	tempKeyStream = ''
	for encryption in encryptedStrings:
		keyLen = len(key)
		eLen = len(encryption)
		diffBytes = (keyLen - eLen)
		if diffBytes > 0:
			tempKeyStream = key[:(-1)*diffBytes]
			print fixedXOR(tempKeyStream, encryption).decode("hex")
		else:
			print fixedXOR(tempKeyStream, encryption[:len(tempKeyStream)]).decode("hex") + " - Trimmed Cipher due to unavailability of enough data"