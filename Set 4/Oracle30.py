from Modules.MD4 import MD4
import random
import os

key = os.urandom(random.randint(4,20))

def generateAuthMessage():
	message = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"

	return message + generateMAC(key + message)

def generateMAC(message):
	h = MD4()
	h.update(message)
	MAC = h.hexdigest()
	
	if not len(MAC) == 32:
		print "Wrong MAC Length " + str(len(MAC))
	return MAC

def checkAuthentication(authText):
	MAC = authText[-32:]
	message = (key + authText[:-32]).encode("hex").decode("hex")

	return MAC == generateMAC(key + authText[:-32])

if __name__ == "__main__":
	if checkAuthentication(generateAuthMessage()):
		print "Working"