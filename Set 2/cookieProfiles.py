from AES import AESECBencrypt
import random
import os

key = ""

def profileParser(profileString):
	profile = {}
	meta = profileString.split("&")

	for field in meta:
		name, value = field.split("=")
		profile[name] = value

	print profile

def profileCreate(emailAddress):
	if "&" or "=" in emailAddress:
		raise Exception("Invalid Email Address")

	encodedString = "email="+ emailAddress + "&" + "uid=" + str(random.randint(0,100)) + "&" + "role=user"

	return encodedString

def encryptionOracle(emailAddress):
	global key 
	key = os.urandom(16)
	return AESECBencrypt(key, profileCreate(emailAddress))

def decryptionOracle(cipherText):
	global key
	return profileParser(AESECBencrypt(key, cipherText))

if __name__ == "__main__":
	profileParser("foo=bar&baz=qux&zap=zazzle")