#include<stdio.h>
#include<stdlib.h>
#include<string.h>

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

int hammingDistance(char *stringOne, char *stringTwo){

	int convTable[16] = {0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4};
	
	int len = strlen(stringOne);
	int decimal, distance = 0;
	char output[len], temp;
	
	if(len != strlen(stringTwo)){
		return 0;
	}

	for (int i=0; i<len; i++)
	{
		temp = stringOne[i] ^ stringTwo[i];
		decimal = (int)temp;
		distance += convTable[(decimal%16)];
		distance += convTable[(decimal/16)];
	}

	return distance;
}

char *base642hex(char *base64String){

	char *base642bin[64] = {"000000","000001","000010","000011","000100","000101","000110","000111","001000","001001","001010","001011","001100","001101","001110","001111",
							"010000","010001","010010","010011","010100","010101","010110","010111","011000","011001","011010","011011","011100","011101","011110","011111",
							"100000","100001","100010","100011","100100","100101","100110","100111","101000","101001","101010","101011","101100","101101","101110","101111",
							"110000","110001","110010","110011","110100","110101","110110","110111","111000","111001","111010","111011","111100","111101","111110","111111"};

	char *dec2hex = "0123456789abcdef";

	int base64Len = strlen(base64String), decimal;

	char *hexString = (char *)malloc((base64Len*3)/2 + 1);

	char tempString[13], temp;
	char first[5], second[5], third[5];

	int equalPaddings = 0;

	for(int i=0; i<base64Len; i+=2){
		decimal = (int)base64String[i];

		if(decimal > 64 && decimal < 91){
			decimal -= 65;
		}
		else if(decimal > 96 && decimal < 123){
			decimal -= 71;
		}
		else if(decimal > 47 && decimal < 58){
			decimal += 4;
		}
		else if(decimal == 47){
			decimal = 63;
		}
		else if(decimal == 43){
			decimal = 62;
		}
		else if(decimal == 61){
			decimal = 0;
			equalPaddings++;
		}

		strcpy(tempString, base642bin[decimal]);
		decimal = (int)base64String[i+1];

		if(decimal > 64 && decimal < 91){
			decimal -= 65;
		}
		else if(decimal > 96 && decimal < 123){
			decimal -= 71;
		}
		else if(decimal > 47 && decimal < 58){
			decimal += 4;
		}
		else if(decimal == 47){
			decimal = 63;
		}
		else if(decimal == 43){
			decimal = 62;
		}
		else if(decimal == 61){
			decimal = 0;
			equalPaddings++;
		}

		strcat(tempString, base642bin[decimal]);

		//mask the first four
		strncpy(first,tempString,4);
		first[4] = '\0';
		*hexString = dec2hex[strtol(first,NULL,2)];
		hexString++;

		//mask the second four
		strncpy(second,&tempString[4],8);
		second[4] = '\0';
		*hexString = dec2hex[strtol(second,NULL,2)];
		hexString++;

		//mask the third four
		strncpy(third,&tempString[8],12);
		third[4] = '\0';
		*hexString = dec2hex[strtol(third,NULL,2)];
		hexString++;
	}
	hexString -= (equalPaddings*2);
	*hexString = '\0';
	hexString -= (base64Len*3/2 - (equalPaddings*2));
	return hexString;
}

int findKeySize(char *hexString, int maxKeySize, int pickSize){

	int hexLen = strlen(hexString);
	
	if(maxKeySize > hexLen) return -1;

	float distArray[maxKeySize-1], distance = 0.00, tempDistance = 0.00;
	char *subString[pickSize];

	for(int i=2; i<=maxKeySize; i++){

		if((pickSize*1) > hexLen) return -1;

		for(int j=0; j<hexLen/(i*pickSize); j++){
			for(int k=0; k<pickSize; k++){
				
				subString[k] = (char *)malloc(i + 1);
				
				strncpy(subString[k], hexString, i);
				
				subString[k] += i;
				*subString[k] = '\0';
				subString[k] -= i;
				
				hexString += i;

				if(k>0){
					//printf("%0.2f  ", (float)hammingDistance(subString[0],subString[k]));
					distance += (float)hammingDistance(subString[0],subString[k])/(i*8);
				}

				//printf("%s ", subString[k]);
			}
			distance /= (pickSize-1);
			//printf("\n");
			printf("%0.2f\n", distance);
			tempDistance += distance;
			distance = 0.00;
		}
		tempDistance /= (hexLen/(i*pickSize));
		//printf("Key Size %d: %.2f\n", i, tempDistance);
		distArray[i-2] = tempDistance;
		tempDistance = 0.00;
		hexString -= ((hexLen/(i*pickSize))*(i*pickSize));
	}

	float minimum = distArray[0];
	int minimumPos = 0;
	
	for(int i=1; i<maxKeySize-1; i++){
		if(distArray[i] < minimum){
			minimum = distArray[i];
			minimumPos = i;
		}
	}

	return minimumPos+2;
}

int main(int argc, char *argv[]){
	int retValue = findKeySize("DUDEDUDEDUDEDUDEDUDEDUDE", 4, 2);
}