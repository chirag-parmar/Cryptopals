from Modules.AES import AESCTRencrypt, AESCTRdecrypt
import random
import os

key = os.urandom(16)
nonce = random.randint(0,999999999)

def encryptionOracle(plainText):
	prepend = r"comment1=cooking%20MCs;userdata="
	append = r";comment2=%20like%20a%20pound%20of%20bacon"

	if ";" in plainText or "=" in plainText:
		raise Exception("Invalid Character")

	plainText = prepend + plainText + append

	return AESCTRencrypt(key, plainText.encode("hex"), nonce)

def checkAdminOracle(cipherText):
	
	plainText = AESCTRdecrypt(key, cipherText, nonce)
	plainText = plainText.decode("hex")
	meta = plainText.split(";")
	metakey = ""
	value = ""

	for item in meta:
		try:
			metakey, value = item.split("=")
		except:
			pass
		if metakey == "admin" and value == "true":
			return True

	return False

if __name__ == "__main__":
	if checkAdminOracle(encryptionOracle("hello")):
		print "hurray"