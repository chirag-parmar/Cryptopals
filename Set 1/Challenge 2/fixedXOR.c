#include<stdio.h>
#include<stdlib.h>
#include<string.h>

char *fixedXOR(char *hexStringOne, char *hexStringTwo){

	//conversion table
	char *dec2hex = "0123456789abcdef";
	
	int hexLen = strlen(hexStringOne);

	//handle boundary conditions
	if(hexLen<1) {
		printf("Exception: NULL Strings");
		return 0;
	}

	char buf[2];
	long int charOne, charTwo;

	//intialize the result string pointer and dynamically allocate memory to it.
	char *XORString;
    XORString = (char *)malloc(hexLen+1);

    //iterate through the Strings
	for(int i=0; i<hexLen; i++){
		//compute the XOR of the integers and then append the corresponding HEX value into the result
		buf[0] = hexStringOne[i];
		buf[1] = '\0';
		charOne = strtol(buf, NULL, 16);

		buf[0] = hexStringTwo[i];
		buf[1] = '\0';
		charTwo = strtol(buf, NULL, 16);

		*XORString = dec2hex[charOne^charTwo];
		
		//increment the pointer
		XORString++;
	}

	//add a null character to terminate the string
	*XORString = '\0';

	//reset the pointer ot the start
	XORString -= (hexLen);

	return XORString;
}

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