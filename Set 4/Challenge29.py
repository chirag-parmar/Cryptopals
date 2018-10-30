from Oracle29 import generateAuthMessage, checkAuthentication
from Modules.SHA1 import SHA1
import os

def padding(stream):
        l = len(stream)  # Bytes
        hl = [int((hex(l*8)[2:]).rjust(16, '0')[i:i+2], 16)
              for i in range(0, 16, 2)]

        l0 = (56 - l) % 64
        if not l0:
            l0 = 64

        if isinstance(stream, str):
            stream += chr(0b10000000)
            stream += chr(0)*(l0-1)
            for a in hl:
                stream += chr(a)
        
        elif isinstance(stream, bytes):
            stream += bytes([0b10000000])
            stream += bytes(l0-1)
            stream += bytes(hl)

        return stream

def extensionAttack(authText, minKeyLen = 4, maxKeyLen = 20):
	message = authText[:-40]
	MAC = authText[-40:]

	for j in range(minKeyLen, maxKeyLen):
		state = []
		for i in range(0,len(MAC), 8):
			state.append(int(MAC[i: i+8], 16))
		
		key = os.urandom(j)
		
		forgedText = padding(key+message) + ";admin=true"
		paddedMessage = forgedText[j:]
		
		h = SHA1()
		h.jumpStart(state, forgedText)
		
		forgedMac = h.hexdigest()
		
		if checkAuthentication(paddedMessage + forgedMac):
			print "Succesfully Executed the attack you are now an admin"
			print "Key Length: " + str(j)
			print "Forged Text: " + repr(paddedMessage)
			print "Forged MAC: " + forgedMac

extensionAttack(generateAuthMessage())