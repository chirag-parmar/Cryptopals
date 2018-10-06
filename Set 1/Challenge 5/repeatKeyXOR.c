#include <stdio.h>
#include <string.h>
#include <stdlib.h>

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

	char buf[2];
	long int charOne, charTwo;

	char *XORString;
    XORString = (char *)malloc(hexLen+1);

	for(int i=0; i<hexLen; i++){
		buf[0] = hexStringOne[i];
		buf[1] = '\0';
		charOne = strtol(buf, NULL, 16);

		buf[0] = hexStringTwo[i];
		buf[1] = '\0';
		charTwo = strtol(buf, NULL, 16);

		*XORString = dec2hex[charOne^charTwo];
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
	if(!strcmp(repeatKeyXOR("ICE", "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"),argv[1])) printf("Hurray!!");
}