#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int hex2int(char ch)
{
    if (ch >= '0' && ch <= '9')
        return ch - '0';
    if (ch >= 'A' && ch <= 'F')
        return ch - 'A' + 10;
    if (ch >= 'a' && ch <= 'f')
        return ch - 'a' + 10;
    return -1;
}

char *ASCII2hex(char *asciiString){

	char *dec2hex = "0123456789abcdef";
	int asciiLen = strlen(asciiString), decimal;

	char *hexString, *tempString;
	
	tempString = (char *)malloc(3);
	hexString = (char *)malloc(2*asciiLen + 1);

	for(int i=0; i<asciiLen; i++){
		decimal = (int)asciiString[i];
		tempString[1] = dec2hex[(decimal%16)];
		tempString[0] = dec2hex[(decimal/16)];
		tempString[2] = '\0';
		if(i == 0){
			strcpy(hexString, tempString);
		}
		else{
			strcat(hexString, tempString);
		}
	}

	return hexString;
}

char *fixedXOR(char *hexStringOne, char *hexStringTwo){

	char *dec2hex = "0123456789abcdef";	
	int hexLen = strlen(hexStringOne);

	if(hexLen<1) {
		printf("Exception: NULL Strings");
		return 0;
	}

	char *XORString;
    XORString = (char *)malloc(hexLen+1);

	for(int i=0; i<hexLen; i++){		
		*XORString = dec2hex[hex2int(hexStringOne[i])^hex2int(hexStringTwo[i])];
		XORString++;
	}

	*XORString = '\0';
	XORString -= (hexLen);

	return XORString;
}

char *repeatKeyXOR(char *key, char *plainText){

	int keyLen = strlen(key);
	int textLen = strlen(plainText);

	char *encKey = (char *)malloc(textLen+1);
	
	strcpy(encKey, key);
	for(int i=1; i<textLen/keyLen; i++){
		strcat(encKey, key);
	}
	encKey[textLen] = '\0';
	for(int i=0; i<textLen%keyLen; i++){
		encKey[(textLen/keyLen)*keyLen + i] = key[i];
	}

	return fixedXOR(ASCII2hex(plainText), ASCII2hex(encKey));
}

int main(int argc, char *argv[]){
	printf("%s\n", repeatKeyXOR("ICE", "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"));
}