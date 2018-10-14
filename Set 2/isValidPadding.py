def isValidPadding(plainText, blockSize=16):
	padCount = int(plainText[-1:].encode("hex"),16) if int(plainText[-1:].encode("hex"),16) < blockSize else 0
	interText = plainText[-padCount:]
	for i in range(padCount):
		if int(interText[i].encode("hex"),16) != padCount:
			raise Exception("Invalid Padding")

	return plainText[:(-1)*padCount]

if __name__ == "__main__":
	paddedString = "ICE ICE BABYBABYICE ICE BABYBABYICE ICE BABYBABYICE ICE BABYBABYICE ICE BABY\x04\x04\x04\x04"
	print isValidPadding(paddedString)

