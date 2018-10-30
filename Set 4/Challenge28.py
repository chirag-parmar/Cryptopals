from Modules.SHA1 import SHA1
import os

def authMessage(key, message):
	h = SHA1()
	h.update(key + message)
	MAC = h.hexdigest()
	if not len(MAC) == 40:
		print "Wrong MAC Length " + str(len(MAC))
	return message + MAC

def checkAuthentication(key, authText):
	MAC = authText[-40:]
	if MAC == authMessage(key, authText[:-40])[-40:]:
		return True
	else:
		return False


if __name__ == "__main__":
	ogMac = authMessage("YELLOW SUBMARINE", "You Owe me 10.00 dollars")
	if checkAuthentication("YELLOW SUBMARINE",ogMac):
		print "Authentication Verified"

	tamperedMac = ogMac[:-41] + "C" + ogMac[-40:]
	tamperedMessage = "You Owe me 100.0 dollars"

	if not checkAuthentication("YELLOW SUBMARINE", tamperedMac):
		print "Hence Proved - 1"

	if not checkAuthentication("YELLOW SUBMARINE", authMessage("YO YO YO HONEY", tamperedMessage)):
		print "Hence Proved - 2"