from Oracle30 import generateAuthMessage, checkAuthentication
from Modules.MD4 import MD4, _pad
import os

def padding(message):
	return _pad(message)

def extensionAttack(authText, minKeyLen = 4, maxKeyLen = 21):
	message = authText[:-32]
	MAC = authText[-32:]

	for j in range(minKeyLen, maxKeyLen):
		state = []
		
		for i in range(0,len(MAC), 8):
			state.append(int(MAC[i: i+8], 16))
		
		key = os.urandom(j)
		
		forgedText = padding(key+message) + ";admin=true"

		paddedMessage = forgedText[j:]
		
		h = MD4()
		h.jumpStart(state, forgedText)
		
		forgedMac = h.hexdigest()

		if checkAuthentication(paddedMessage + forgedMac):
			print "Succesfully Executed the attack you are now an admin"
			print "Key Length: " + str(j)
			print "Forged Text: " + repr(paddedMessage)
			print "Forged MAC: " + forgedMac
			break

extensionAttack(generateAuthMessage())