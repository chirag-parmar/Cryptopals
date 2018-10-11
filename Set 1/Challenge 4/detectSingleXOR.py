from crackSingleXOR import crackSingleXOR, fixedXOR

if __name__ == "__main__":
	score = 0.00
	maxScore = 0.00
	detectedLine = ''

	with open('Test.txt', 'r') as testFile:
		for line in testFile:
			score = crackSingleXOR(line.strip(),False,True)
			if(score > maxScore):
				maxScore = score
				detectedLine = fixedXOR(crackSingleXOR(line.strip(),False),line.strip()).decode("hex")

	print detectedLine, maxScore