import sys

argv = sys.argv[1:]

for hexStrings in argv:
	print(hexStrings.decode("hex") + '\n' + hexStrings.decode("hex").encode("base64") + '\n')