from crackSingleXOR import crackSingleXOR, fixedXOR
import sys

def repeatKeyXOR(key, text):
	keyLen = len(key)
	textLen = len(text)

	repeatKey = ''
	i = 0

	while (textLen - (i*keyLen)) >= keyLen:
		repeatKey += key
		i+=1
	if textLen%keyLen != 0:
		repeatKey += key[:(textLen%keyLen)]

	return fixedXOR(repeatKey, text)

if __name__ == "__main__":
	print repeatKeyXOR(sys.argv[1], "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal")