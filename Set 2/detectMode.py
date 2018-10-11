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

message = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

if __name__ == "__main__":
	tests = []
	for i in range(0,1000):
		cipherText, mode = encryptionOracle(message)
		score = scoreCipher(cipherText)
		if score == 0:
			detectedMode = 'ECB'
		else:
			detectedMode = 'CBC'

		if mode == detectedMode:
			tests.append(1)
		else:
			tests.append(0)

	print str(sum(tests)) + "/" + str(len(tests)) + " Passed, Accuracy " + str(sum(tests)/len(tests)*100) + "%"