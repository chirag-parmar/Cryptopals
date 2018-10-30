from Oracle26 import encryptionOracle, checkAdminOracle
from Modules.fixedXOR import fixedXOR
import math
import os

def findStartText():
	inputText = 'Z'*100
	cipherText = encryptionOracle(inputText)
	inputText2 = 'A'*100
	cipherText2 = encryptionOracle(inputText2)
	pos = 0

	for i in range(len(cipherText)/2):
		if not cipherText[(i*2):(i*2)+2] == cipherText2[(i*2):(i*2)+2]:
			pos = i
			break
	return pos

def flipper():
	pos = findStartText()

	adminText = ";admin=true;"
	inputText = encryptionOracle("000000000000000000000000".decode("hex"))[pos*2:(pos+len(adminText))*2]
	attaxText = fixedXOR(adminText.encode("hex"), inputText)

	cipherText = encryptionOracle(inputText)

	cipherText = cipherText[:pos*2] + attaxText + cipherText[(pos*2)+len(attaxText):]
	if checkAdminOracle(cipherText):
		print "Changed to Admin"
	else:
		print "Couldn't do it"

flipper()