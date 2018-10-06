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

int main(int argc, char *argv[]){
	printf("HEX: %s", ASCII2hex(argv[1]));
}