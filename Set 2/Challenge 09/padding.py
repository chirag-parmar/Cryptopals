import binascii

def padMsg(msg, toBytes):
	msgLen = len(msg)

	if msgLen > toBytes:
		raise Exception("Can't reduce length while padding")
	elif toBytes-msgLen > 256:
		raise Exception("Can't pad more than 256 bytes")
	else:
		for i in range(toBytes-msgLen):
			msg += (hex(toBytes-msgLen)[2:].zfill(2).rstrip("L")).decode("hex")
	return msg