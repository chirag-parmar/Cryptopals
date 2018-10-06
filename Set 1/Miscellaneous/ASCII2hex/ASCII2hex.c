#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *ASCII2hex(char *asciiString){

	char *dec2hex = "0123456789abcdef";
	int asciiLen = strlen(asciiString), decimal;

	char *hexString;
	hexString = (char *)malloc(2*asciiLen + 1);

	for(int i=0; i<asciiLen; i++){
		decimal = (int)asciiString[i];
		*hexString++ = dec2hex[(decimal/16)];
		*hexString++ = dec2hex[(decimal%16)];
	}
	*hexString = '\0';
	hexString -= (asciiLen*2);

	return hexString;
}

int main(int argc, char *argv[]){
	printf("HEX: %s", ASCII2hex(argv[1]));
}