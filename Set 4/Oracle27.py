from Modules.AES import AESCBCencrypt, AESCBCdecrypt
import os

key = os.urandom(16)
iv = key.encode("hex")

def encryptionOracle(plainText):
	prepend = r"comment1=cooking%20MCs;userdata="
	append = r";comment2=%20like%20a%20pound%20of%20bacon"

	if ";" in plainText or "=" in plainText:
		raise Exception("Invalid Character")

	plainText = prepend + plainText + append

	return AESCBCencrypt(key, plainText.encode("hex"), iv)

def receiverOracle(cipherText):
	
	plainText = AESCBCdecrypt(key, cipherText, iv)
	plainText = plainText.decode("hex")
	
	##check for high ascii value
	for char in plainText:
		if ord(char)>128:
			raise Exception("High ASCII Value in plaintext: " + plainText)

def checkKey(foundKey):
	if foundKey == key:
		return True
	return False

if __name__ == "__main__":
	print encryptionOracle("HELLO")
	receiverOracle(encryptionOracle("hello"))