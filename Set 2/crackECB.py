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

def scoreCipher(hexString, blockSize=16):
	hexLen = len(hexString)
	byteStrings = []
	blockSize *= 2
	distance = 0.00
	lowestDistance = 2.00

	for i in range(0,hexLen,blockSize):
		byteStrings.append(hexString[i:i+blockSize])

	combinations = list(itertools.combinations(byteStrings, 2))

	combLen = len(combinations)

	for pair in combinations:
		distance = (hammingDistance(pair[0], pair[1])/blockSize*4)
		if(distance < lowestDistance):
			lowestDistance = distance

	return lowestDistance

def isAdjacentBlockEqual(cipherText, blockSize):
	blockSize *= 2
	prevBlock = cipherText[:blockSize]
	cipherLen = len(cipherText)
	counter = 0

	for i in range(blockSize, cipherLen, blockSize):
		if cipherText[i:i+blockSize] != prevBlock:
			prevBlock = cipherText[i:i+blockSize]
			counter += 1
		else:
			return counter
	return False


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
	prevLen = len(encryptionOracle(message))
	blockSize = 0

	while (blockSize == 0):
		message += "C"
		blockSize = (len(encryptionOracle(message)) - prevLen)/2

	return blockSize

def findLeadingBytes(blockSize):
	message = ""
	leadingBytes = 0
	timeout = 1000
	count = 0

	while not count and timeout>0:
		message += "A"
		count = isAdjacentBlockEqual(encryptionOracle(message), blockSize)
		leadingBytes += 1
		timeout -= 1

	if not timeout>0:
		leadingBytes = 0
	elif (leadingBytes%blockSize):
		leadingBytes = (count-1)*blockSize + (blockSize - leadingBytes%blockSize)
		count -= 1
	else:
		leadingBytes = count*blockSize

	return leadingBytes


def crackItOpen(blockSize):
	secretLen = len(encryptionOracle(""))/2
	foundString = ""
	leadingBytes = findLeadingBytes(blockSize)
	leadingNum = leadingBytes/blockSize if (leadingBytes%blockSize) == 0 else leadingBytes/blockSize + 1

	for k in range(1, secretLen/blockSize +1):
		scope = k if leadingBytes == 0 else k+leadingNum
		for j in range(1, blockSize+1):
			exploitMsg = "A"*(blockSize-j) + "A"*((blockSize - leadingBytes%blockSize)%blockSize)
			for i in range(0, 256):
				if encryptionOracle(exploitMsg)[:blockSize*2*scope] == encryptionOracle(exploitMsg + foundString + chr(i))[:blockSize*2*scope]:
					foundString += chr(i)
					break

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
		print "Not ECB mode or block size " + str(blockSize) + " unacceptable"