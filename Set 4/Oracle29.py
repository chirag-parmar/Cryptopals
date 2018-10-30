from Modules.SHA1 import SHA1
import random
import os

key = os.urandom(random.randint(4,20))

def generateAuthMessage():
	message = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
	return message + generateMAC(key + message)

def generateMAC(message):
	h = SHA1()
	h.update(message)
	MAC = h.hexdigest()
	
	if not len(MAC) == 40:
		print "Wrong MAC Length " + str(len(MAC))
	return MAC

def checkAuthentication(authText):
	MAC = authText[-40:]
	if MAC == generateMAC(key + authText[:-40]):
		return True
	else:
		return False

if __name__ == "__main__":
	if checkAuthentication(generateAuthMessage()):
		print "Working"