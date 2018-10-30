from Oracle25 import readFileandEncrypt, edit

if __name__ == "__main__":
	
	cipherText = readFileandEncrypt("./Tests/25.txt")
	cipherLen = len(cipherText)/2
	foundText = ''

	for i in range(cipherLen):
		foundText += edit(cipherText, i, cipherText[(i*2):(i*2)+2].decode("hex"))[(i*2):(i*2)+2]

	print foundText.decode("hex")