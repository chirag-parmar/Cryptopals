from AES import AESCBCencrypt, AESCBCdecrypt
import os

key = os.urandom(16)
iv = os.urandom(16)
iv = iv.encode("hex")

def encryptionOracle(plainText):
	prepend = r"comment1=cooking%20MCs;userdata="
	append = r";comment2=%20like%20a%20pound%20of%20bacon"

	if ";" in plainText or "=" in plainText:
		raise Exception("Invalid Character")

	plainText = prepend + plainText + append

	return AESCBCencrypt(key, plainText.encode("hex"), iv)

def checkAdminOracle(cipherText):
	
	plainText = AESCBCdecrypt(key, cipherText, iv)
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
	if checkAdminOracle(encryptionOracle(";admin=true;")):
		print "hurray"
