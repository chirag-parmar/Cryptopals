#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *hex2ASCII(char *hexString){
	int hexLen = strlen(hexString);
	char buf[3];
	char *ASCIIString;
	ASCIIString = (char *)malloc(hexLen/2 + 1);

	for (int i=0; i<hexLen; i+=2){
		buf[0] = hexString[i];
		buf[1] = hexString[i+1];
		buf[2] = '\0';

		*ASCIIString = (char)strtol(buf, NULL, 16);
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