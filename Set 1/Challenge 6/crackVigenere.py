from crackSingleXOR import crackSingleXOR, fixedXOR, scoreText
from repeatKeyXOR import repeatKeyXOR

def hammingDistance(hexString1, hexString2):
	XORed = fixedXOR(hexString1,hexString2)
	XORed = bin(int(XORed, 16))[2:]

	count = 0.00

	for bit in XORed:
		if bit == '1':
			count+=1

	return count

def findKeyLength(cipherText, maxLen, top):

	cipherLen = len(cipherText)

	if maxLen*4 > cipherLen:
		raise Exception("max key length too big")
	elif top > maxLen:
		raise Exception("maximum length smaller than number of objects to be returned")
	distances = 0.00
	chunkCounts = 0
	subString1 = ''
	subString2 = ''
	keyLengths = {}

	for keyLen in range(2,maxLen+1):
		distances = 0.00
		chunkCounts = 0
		for chunkNumber in range(0,cipherLen,keyLen*4):
			try:
				subString1 = cipherText[chunkNumber:(chunkNumber+(keyLen*2))]
				subString2 = cipherText[(chunkNumber+(keyLen*2)):(chunkNumber+(keyLen*4))]
				distances += (hammingDistance(subString1, subString2)/(keyLen*8))
				chunkCounts += 1
			except:
				pass
		if chunkCounts != 0:
			keyLengths[str(keyLen)] = (distances/chunkCounts)

	return sorted(keyLengths, key=keyLengths.__getitem__)[:top]

def moldMatrix(hexString, keyLen):
	hexLen = len(hexString)
	repeatBins = ["" for x in range(keyLen)]

	for i in range(0,hexLen,2):
		repeatBins[(i/2)%keyLen] += hexString[i:i+2]

	return repeatBins

def readFile(filename):
	with open(filename, 'r') as myfile:
		data = myfile.read().replace('\n', '')

	hexString = data.decode("base64").encode("hex")

	return hexString

if __name__ == "__main__":
	hexString = readFile("Test.txt")
	keyLengths = findKeyLength(hexString, 100, 2)
	key = ''
	interText = ''
	finalText = ''
	score = 0.00
	maxScore = 0.00

	for keyLen in keyLengths:
		key = ''
		repeatStrings = moldMatrix(hexString, int(keyLen))
		for eachString in repeatStrings:
			key += crackSingleXOR(eachString)
		interText = repeatKeyXOR(key, hexString).decode("hex")
		score = scoreText(interText)
		if(score > maxScore):
			maxScore = score
			finalText = interText

	print finalText
