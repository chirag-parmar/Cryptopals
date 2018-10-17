from paddingOracle import encryptionOracle, paddingOracle
from fixedXOR import fixedXOR
import os

def crackCBC(blockSize=16):
	randomBlock = os.urandom(blockSize).encode("hex")
	
	cipherText, IV = encryptionOracle()
	cipherLen = len(cipherText)

	crackedText = ''

	foundBlock = ''
	previousBlock = IV

	for i in range(0, cipherLen, blockSize*2):
		cipherBlock = cipherText[i: i+(blockSize*2)]
		for j in range(256):
			newRandomBlock = randomBlock[:-2] + hex(j)[2:].zfill(2)
			if paddingOracle(newRandomBlock+cipherBlock, IV):
				padLen = findPaddingLength(newRandomBlock, cipherBlock, IV)
				foundBlock = findBlockByPadding(padLen, newRandomBlock, cipherBlock, IV)
				crackedText += fixedXOR(foundBlock,previousBlock).decode("hex")
				previousBlock = cipherBlock
			else:
				pass

	print crackedText

def findPaddingLength(randomBlock, cipherBlock, iv, blockSize=16):
	for i in range(len(randomBlock)/2):
		newRandomBlock = randomBlock[:i*2] + hex((int(randomBlock[i:i+1], 16) + 1)%256)[2:].zfill(2) + randomBlock[2*(i+1):]
		if not paddingOracle(newRandomBlock+cipherBlock, iv):
			return blockSize-i
	raise "Wrong random Text sent"

def findBlockByPadding(padLen, randomBlock, cipherBlock, IV, blockSize=16):

	foundBlock=''
	paddedRandomHits = randomBlock[(-1)*(padLen*2):]
	maskForHits = (hex(padLen)[2:].zfill(2))*(len(paddedRandomHits)/2)
	foundBlock = fixedXOR(paddedRandomHits, maskForHits)

	for k in range(blockSize-padLen):
		maskOne = (hex(0)[2:].zfill(2))*(blockSize-padLen) + (hex(padLen)[2:].zfill(2))*(padLen)
		maskTwo = (hex(0)[2:].zfill(2))*(blockSize-padLen) + (hex(padLen+1)[2:].zfill(2))*(padLen)
		padLen += 1
		randomBlock = fixedXOR(randomBlock, maskOne)
		randomBlock = fixedXOR(randomBlock, maskTwo)
		for j in range(256):
			randomBlock = randomBlock[:(blockSize-padLen)*2] + hex(j)[2:].zfill(2) + randomBlock[2*(blockSize-padLen+1):]
			if paddingOracle(randomBlock+cipherBlock, IV):
				foundBlock = fixedXOR(hex(j)[2:].zfill(2), hex(padLen)[2:].zfill(2)) + foundBlock
				break

	return foundBlock

crackCBC()