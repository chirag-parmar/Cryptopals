from fixedXOR import fixedXOR
from encryptionOracle import encryptionOracle
import itertools

def hammingDistance(hexString1, hexString2):
	XORed = fixedXOR(hexString1,hexString2)
	XORed = bin(int(XORed, 16))[2:]

	count = 0.00

	for bit in XORed:
		if bit == '1':
			count+=1

	return count

def scoreCipher(hexString, keySize=32):
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

def detectMode():
	message = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
	cipherText = encryptionOracle(message)
	score = scoreCipher(cipherText)
	if score == 0:
		detectedMode = 'ECB'
	else:
		detectedMode = 'CBC'

	return detectedMode


if __name__ == "__main__":
	for i in range(0,1000):
		print detectMode()