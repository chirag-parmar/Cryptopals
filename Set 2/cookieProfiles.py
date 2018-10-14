from AES import AESECBencrypt, AESECBdecrypt
import random
import os

key = os.urandom(16)

def profileParser(profileString):
	profile = {}
	meta = profileString.split("&")

	for field in meta:
		name, value = field.split("=")
		profile[name] = value.strip()

	print profile

def profileCreate(emailAddress):
	if "&" in emailAddress or "=" in emailAddress:
		raise Exception("Invalid Email Address")

	encodedString = "email="+ emailAddress + "&" + "uid=007" + "&" + "role=user"

	return encodedString

def encryptionOracle(emailAddress):
	return AESECBencrypt(key, profileCreate(emailAddress).encode("hex"))

def decryptionOracle(cipherText):
	return profileParser(AESECBdecrypt(key, cipherText).decode("hex"))

if __name__ == "__main__":
	print encryptionOracle("chiragparmar12209@gmail.com")
