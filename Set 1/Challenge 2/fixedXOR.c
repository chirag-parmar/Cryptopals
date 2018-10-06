#include<stdio.h>
#include<stdlib.h>
#include<string.h>

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
}s

int main(int argc, char *argv[]){
	
	unsigned passed = 0;

	int testCases = *argv[1] - '0';

	for(int i=2; i<argc; i+=3){
		if(!strcmp(argv[i+2],fixedXOR(argv[i], argv[i+1]))){
			printf("Test %d PASSED\n", (i-2)/3 + 1);
			passed++;
		}
		else{
			printf("Test %d FAILED\n", (i-2)/3 + 1);
			printf("Computed String: %s\n", fixedXOR(argv[i], argv[i+1]));
			printf("Given String: %s\n\n", argv[i+2]);
		}
	}

	printf("%d/%d Tests Passed", passed, testCases);

	return 0;
}