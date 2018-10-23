from MT19937StreamCipher import encryptionOracle, encrypt

def breakIt():
	message = "A"*14
	cipherText = encryptionOracle(message)

	last32 = cipherText[-8:]
	extractedNum = int(last32, 16)

	dummyMessage = cipherText[:-8].decode("hex") + "A"*4

	for i in range(65536):
		bruteKey = bin(i)[2:].zfill(16)
		last32 = encrypt(bruteKey, dummyMessage)[-8:]
		if int(last32, 16) == extractedNum:
			print "Found the key: " + bruteKey
			break

breakIt()