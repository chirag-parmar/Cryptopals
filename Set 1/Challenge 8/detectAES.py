import itertools
from crackSingleXOR import fixedXOR

def hammingDistance(hexString1, hexString2):
	XORed = fixedXOR(hexString1,hexString2)
	XORed = bin(int(XORed, 16))[2:]

	count = 0.00

	for bit in XORed:
		if bit == '1':
			count+=1

	return count

def scoreAESECB(hexString, keySize=32):
	hexLen = len(hexString)
	byteStrings = []
	distance = 0.00
	lowestDistance = 2.00

	for i in range(0,hexLen,keySize):
		byteStrings.append(hexString[i:i+keySize])

	combinations = list(itertools.combinations(byteStrings, 2))

	combLen = len(combinations)

	for pair in combinations:
		distance = (hammingDistance(pair[0], pair[1])/128)
		if(distance < lowestDistance):
			lowestDistance = distance

	return lowestDistance

if __name__ == "__main__":
	scoresByLines = {}
	lineNum = 1
	with open('Test.txt', 'r') as testFile:
		for line in testFile:
			scoresByLines[str(lineNum)] = scoreAESECB(line.strip())
			lineNum+=1

	AESECBLines = sorted(scoresByLines, key=scoresByLines.__getitem__)[:3]
	print "Line no. " + AESECBLines[0] + " is encrypted in ECB mode"
