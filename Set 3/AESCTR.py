from AES import AESCTRencrypt, AESCTRdecrypt

if __name__ == "__main__":
	challengeString = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
	challengeString = challengeString.decode("base64").encode("hex")
	key = "YELLOW SUBMARINE"
	print AESCTRdecrypt(key, challengeString, 0).decode("hex")