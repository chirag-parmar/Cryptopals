#include<stdio.h>
#include<stdlib.h>
#include<string.h>

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

int hammingDistance(char *stringOne, char *stringTwo){

	int convTable[16] = {0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4};
	
	int len = strlen(stringOne);
	long int decimal;
	int distance = 0;
	char temp1[2], temp2[2];
	
	if(len != strlen(stringTwo)){
		return 0;
	}

	for(int i=0; i<len; i++){
		temp1[0] = stringOne[i];
		temp2[0] = stringTwo[i];
		temp1[1] = '\0';
		temp2[1] = '\0';
		decimal = strtol(temp1, NULL, 16) ^ strtol(temp2, NULL, 16);
		distance += convTable[(decimal%16)];
		distance += convTable[(decimal/16)];
	}

	return distance;
}

int main(int argc, char *argv[]){
	printf("Hamming Distance: %d", hammingDistance(ASCII2hex("this is a test"),ASCII2hex("wokka wokka!!!")));
}