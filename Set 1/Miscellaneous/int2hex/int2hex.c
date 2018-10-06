#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *int2hex(unsigned int decimal){

	char *dec2hex = "0123456789abcdef";

	char *hexString;
	hexString = (char *)malloc(3);

	hexString[1] = dec2hex[(decimal%16)];
	hexString[0] = dec2hex[(decimal/16)];
	hexString[2] = '\0';

	return hexString;
}

int main(int argc, char *argv[]){
	printf("HEX VALUE: %s", int2hex(43));
}