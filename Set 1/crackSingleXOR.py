import sys
import json
import string
from fixedXOR import fixedXOR

def scoreText(plainText):

	if len(plainText) <= 0:
		raise Exception("NULL String")

	score = 0
	digitCount = 0.0
	restrictedCount = 0.0
	punctCount = 0.0
	letterCount = 0.0

	with open('frequentBigrams.json', 'r') as bigramsFile:
		frequentBigrams = json.load(bigramsFile)

	with open('frequentLetters.json', 'r') as lettersFile:
		frequentLetters = json.load(lettersFile)

	for letter in plainText:
		try:
			score += frequentLetters[letter]
		except:
			pass	
		if letter.isalpha():
			score += 2
		elif letter.isspace():
			score += 5
		elif letter.isdigit():
			digitCount+=1
		elif letter in string.punctuation:
			punctCount+=1
		else:
			restrictedCount+=1
			score-=3
		letterCount += 1

	for i in range(0,len(plainText),2):
		bigram = plainText[i*2:i*2+2]
		try:
			score += frequentBigrams[bigram]
		except:
			pass

	if (punctCount/letterCount) < 0.15:
		score += punctCount
	else:
		score -= (punctCount/2)
	if (digitCount/letterCount) < 0.15:
		score += digitCount
	if (restrictedCount/letterCount) > 0.4:
		score = 0

	return score

def crackSingleXOR(cipherText, retUnit=True, retScore=False):

	cipherLen = len(cipherText)
	bruteKey = ''
	finalKey = ''
	score = 0.00
	maxScore = 0.00

	for i in range(256):
		bruteKey = ''
		while len(bruteKey) != cipherLen:
			bruteKey += hex(i)[2:].zfill(2).rstrip("L")

		score = scoreText(fixedXOR(bruteKey,cipherText).decode("hex"))
		if(score > maxScore):
			maxScore = score
			finalKey = bruteKey
	if retUnit and (not retScore):
		return finalKey[:2]
	elif (not retUnit) and retScore:
		return maxScore
	elif retUnit and retScore:
		return finalKey[:2], maxScore 
	else:
		return finalKey

if __name__ == "__main__":
	Key = crackSingleXOR(sys.argv[1], False)
	print fixedXOR(Key, sys.argv[1]).decode("hex")