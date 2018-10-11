#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>
#include<math.h>

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
	hexString -= ((base64Len*3/2) - equalPaddings - 1;
	return hexString;
}

int findKeySize(char *hexString, int maxKeySize, int pickSize){

	int hexLen = strlen(hexString);
	
	if(maxKeySize > hexLen) return -1;

	double distArray[maxKeySize-1], distance = 0.00, tempDistance = 0.00;
	char *subString[pickSize];

	for(int i=2; i<=maxKeySize; i++){

		if((pickSize*i) > hexLen) return -1;

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
					distance += (double)hammingDistance(subString[0],subString[k])/(i*8);
				}

				//printf("%s ", subString[k]);
			}
			free(subString);
			distance /= (pickSize-1);
			//printf("\n");
			//printf("%0.2f\n", distance);
			tempDistance += distance;
			distance = 0.00;
		}
		tempDistance /= (hexLen/(i*pickSize));
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

char *int2hex(unsigned int decimal){

	if(decimal>256) return "00";
	char *dec2hex = "0123456789abcdef";

	char *hexString;
	hexString = (char *)malloc(3);

	hexString[1] = dec2hex[(decimal%16)];
	hexString[0] = dec2hex[(decimal/16)];
	hexString[2] = '\0';

	return hexString;
}

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
}

int scoreText(char *text){
	char alphabet;
	int score = 0;
	for(int i=0; i<strlen(text); i++){
		if(!isalnum(text[i]) && !isspace(text[i]) && !ispunct(text[i])){
			score -= 5;
		}
		else if(isalpha(text[i])){
			alphabet = text[i];
			switch(alphabet){
				case 'e':
					score += 13;
					break;
				case 't':
					score += 12;
					break;
				case 'a':
					score += 11;
					break;
				case 'o':
					score += 10;
					break;
				case 'i':
					score += 9;
					break;
				case 'n':
					score += 8;
					break;
				case 's':
					score += 7;
					break;
				case 'h':
					score += 6;
					break;
				case 'r':
					score += 5;
					break;
				case 'd':
					score += 4;
					break;
				case 'l':
					score += 3;
					break;
				case 'u':
					score += 2;
					break;
				default:
					score += 1;
				break;
			}
		}
		else if(isspace(text[i])){
			score += 5;
		}
	}
	return score;
}

char *breakSingleXOR(char *cipherText){

	int hexLen = strlen(cipherText);
	
	int maxScore = 0, score;
	char *hexUnitKey, *finalKey;
	char *plainText;
	char *finalText;
	char Key[hexLen+1];

	for(int i=0; i<256; i++){
		hexUnitKey = int2hex(i);

		strcpy(Key,hexUnitKey);
		for(int i=0; i<hexLen/2; i++){
			strcat(Key, hexUnitKey);
		}
		Key[hexLen] = '\0';

		plainText = hex2ASCII(fixedXOR(Key, cipherText));
		score = scoreText(plainText);
		if(score > maxScore){
			maxScore = score;
			finalKey = hexUnitKey;
		}
	}

	return finalKey;
}

char *findKey(char *hexString, char keySize){

	int hexLen = strlen(hexString);
	int oddOneOuts = (hexLen%(keySize*2))/2;
	int iterations = hexLen/keySize;
	char *transStrings[keySize];
	char *Key = (char *)malloc(keySize + 1);

	for(int k=0; k<hexLen; k+=2){
		if((k/2)<keySize){
			transStrings[(k/2)%keySize] = (char *)malloc(iterations + 2);
		}
		*transStrings[(k/2)%keySize]++ = hexString[k];
		*transStrings[(k/2)%keySize]++ = hexString[k+1];
	}

	for(int j=0; j<keySize; j++){
		*transStrings[j] = '\0';
		
		if(oddOneOuts>0){
			if(j<oddOneOuts) transStrings[j] -= (iterations + 1);
			else transStrings[j] -= (iterations-1);
		}
		else{
			transStrings[j] -= iterations;
		}

		if(j==0) strcpy(Key,breakSingleXOR(transStrings[j]));
		else strcat(Key,breakSingleXOR(transStrings[j]));
	}

	return Key;
}

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

	return fixedXOR(plainText, encKey);
}

char *readFile(char *fileName)
{
    FILE *file = fopen(fileName, "r");
    char *code;
    int c;
    int num = 0;

    if (file == NULL) return NULL;

    code = (char *)malloc(5000);

    while ((c = fgetc(file)) != -1)
    {
        if(c == (-1)) break;
	else if(c != '\n'){
        	printf("%c",c);
		*code++ = (char)c;
        	num += 1;
        }
    }
    *code = '\0';
    code -= num;
    return code;
}

int main(int argc, char *argv[]){
	char *hexString = base642hex(readFile("Test.txt"));
	int keySize = findKeySize(hexString, 100, 5);
	char *key = findKey(hexString, keySize);
	char *plainText = repeatKeyXOR(key, hexString);
	printf("PLAIN TEXT: %s", hex2ASCII(plainText));
}
