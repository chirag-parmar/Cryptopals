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

char *hex2ASCII(char *hexString){
	int hexLen = strlen(hexString);
	int decimal;
	char *ASCIIString;
	ASCIIString = (char *)malloc(hexLen/2 + 1);

	for (int i=0; i<hexLen; i+=2){
		decimal = (hex2int(hexString[i])*16 + hex2int(hexString[i+1]));
		if(decimal<128) *ASCIIString = (char)decimal;
		else *ASCIIString = '0';
		ASCIIString++;
	}

	*ASCIIString = '\0';
	ASCIIString -= (hexLen/2);

	return ASCIIString;
}

int main(int argc, char *argv[]){
	printf("ASCII: %s", hex2ASCII(argv[1]));
	return 0;
}