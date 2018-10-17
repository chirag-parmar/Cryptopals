import sys

def fixedXOR(hexString1, hexString2, chunkSize = 128):
	hexLen1 = len(hexString1)
	hexLen2 = len(hexString2)

	interInt1 = 0
	interInt2 = 0
	XORString = ''
	i = 0

	if hexLen1 != hexLen2:
		raise Exception("unequal string lengths " + str(hexLen1) + ", " + str(hexLen2))
	elif hexLen1 == 0 or hexLen2 == 0:
		raise Exception("NULL String")
	elif chunkSize > 512:
		raise Exception("chunk size too big")
	else:
		if chunkSize > hexLen1:
			chunkSize = hexLen1
		while (hexLen1 - (i*chunkSize)) >= chunkSize:
			interInt1 = int(hexString1[i*chunkSize:i*chunkSize + chunkSize], 16)
			interInt2 = int(hexString2[i*chunkSize:i*chunkSize + chunkSize], 16)
			if isinstance(interInt1^interInt2, long):
				XORString += hex(interInt1^interInt2)[2:].zfill(chunkSize+1).rstrip("L")
			else:
				XORString += hex(interInt1^interInt2)[2:].zfill(chunkSize).rstrip("L")
			i+=1
		if hexLen1%chunkSize != 0:
			interInt1 = int(hexString1[(i*chunkSize):], 16)
			interInt2 = int(hexString2[(i*chunkSize):], 16)
			if isinstance(interInt1^interInt2, long):
				XORString += hex(interInt1^interInt2)[2:].zfill((hexLen1%chunkSize)+1).rstrip("L")
			else:
				XORString += hex(interInt1^interInt2)[2:].zfill((hexLen1%chunkSize)).rstrip("L")
	return XORString

if __name__ == "__main__":
	argv = sys.argv[1:]
	for i in range(0, len(argv), 2):
		print fixedXOR(argv[i],argv[i+1],15).decode("hex")