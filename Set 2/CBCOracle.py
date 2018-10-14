from AES import AESCBCencrypt, AESCBCdecrypt
import os

key = os.urandom(16)
iv = os.urandom(16)
iv = iv.encode("hex")

def encryptionOracle(plainText):
	global key
	prepend = r"comment1=cooking%20MCs;userdata="
	append = r";comment2=%20like%20a%20pound%20of%20bacon"

	if ";" in plainText or "=" in plainText:
		raise Exception("Invalid Character")

	plainText = prepend + plainText + append

	return AESCBCencrypt(key, plainText.encode("hex"), iv)

def checkAdminOracle(cipherText):
	
	global key
	plainText = AESCBCdecrypt(key, cipherText, iv)
	plainText = plainText.decode("hex")
	meta = plainText.split(";")

	for item in meta:
		try:
			key, value = item.split("=")
		except:
			pass
		if key == "admin" and value == "true":
			return True

	return False

if __name__ == "__main__":
	if checkAdminOracle(encryptionOracle(";admin=true;")):
		print "hurray"
