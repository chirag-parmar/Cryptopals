from fixedXOR import fixedXOR
from encryptionOracle2 import encryptionOracle
import itertools

def hammingDistance(hexString1, hexString2):
	XORed = fixedXOR(hexString1,hexString2)
	XORed = bin(int(XORed, 16))[2:]

	count = 0.00

	for bit in XORed:
		if bit == '1':
			count+=1

	return count

def scoreCipher(hexString, blockSize=32):
	hexLen = len(hexString)
	byteStrings = []
	distance = 0.00
	lowestDistance = 2.00

	for i in range(0,hexLen,blockSize):
		byteStrings.append(hexString[i:i+blockSize])

	combinations = list(itertools.combinations(byteStrings, 2))

	combLen = len(combinations)

	for pair in combinations:
		distance = (hammingDistance(pair[0], pair[1])/128)
		if(distance < lowestDistance):
			lowestDistance = distance

	return lowestDistance

def detectMode(blockSize):
	message = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
	cipherText = encryptionOracle(message)
	score = scoreCipher(cipherText, blockSize)
	if score == 0:
		detectedMode = 'ECB'
	else:
		detectedMode = 'CBC'

	return detectedMode

def findBlockSize():
	message = ""
	for i in range (1,65):
		message += "C"
		cipherText = encryptionOracle(message)
		if cipherText[:i] == cipherText[i:2*i]:
			return i/2
	return 0


def crackItOpen(blockSize):
	secretLen = len(encryptionOracle(""))/2
	foundString = ""

	for k in range(1, (secretLen/blockSize)+1):
		for j in range(1, blockSize+1):
			exploitMsg = "A"*(blockSize-j)
			for i in range(0, 256):
				if encryptionOracle(exploitMsg)[:blockSize*2*k] == encryptionOracle(exploitMsg + foundString + chr(i))[:blockSize*2*k]:
					foundString += chr(i)
					break;

	foundString = foundString.encode("hex")
	paddingNum = int(foundString[-2:],16)
	if paddingNum < 16:
		foundString = foundString[:(-1)*paddingNum*2]
		print "No. of padding bytes: " + str(paddingNum) + '\n'

	return foundString.decode("hex")

	
if __name__ == "__main__":
	blockSize = findBlockSize()
	if blockSize > 0 and detectMode(blockSize) == 'ECB':
		print crackItOpen(blockSize)
	else:
		print "Not ECB mode"