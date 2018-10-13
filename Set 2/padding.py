import binascii

def padMsg(msg, toBytes, inHex = False, keySize=16):
	msgLen = len(msg)

	if inHex:
		diff = (toBytes-msgLen)/2
	else:
		diff = toBytes-msgLen

	if msgLen > toBytes:
		raise Exception("Can't reduce length while padding")
	elif diff > 16:
		raise Exception("Can't pad more than 16 bytes")
	else:
		for i in range(diff):
			if not inHex:
				msg += (hex(diff)[2:].zfill(2).rstrip("L")).decode("hex")
			else:
				msg += (hex(diff)[2:].zfill(2).rstrip("L"))
	return msg