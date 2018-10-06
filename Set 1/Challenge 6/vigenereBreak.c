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
	hexString -= (base64Len*3/2 - (equalPaddings*2));
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

int maxFind(unsigned freq[]){
	int max = 0;
	int maxpos = -1;

	for(int j=0; j<256; j++){
		if(freq[j] > max){
			max = freq[j];
			maxpos = j;
		}
	}
	return maxpos;
}

char *int2hex(unsigned int decimal){

	char *dec2hex = "0123456789abcdef";

	char *hexString;
	hexString = (char *)malloc(3);

	hexString[1] = dec2hex[(decimal%16)];
	hexString[0] = dec2hex[(decimal/16)];
	hexString[2] = '\0';

	return hexString;
}

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

char *fixedXOR(char *hexStringOne, char *hexStringTwo){

	char *dec2hex = "0123456789abcdef";
	int hexLen = strlen(hexStringOne);

	if(hexLen<1) {
		printf("Exception: NULL Strings");
		return 0;
	}

	char buf[2];
	long int charOne, charTwo;

	char *XORString;
    XORString = (char *)malloc(hexLen+1);

	for(int i=0; i<hexLen; i++){
		buf[0] = hexStringOne[i];
		buf[1] = '\0';
		charOne = strtol(buf, NULL, 16);

		buf[0] = hexStringTwo[i];
		buf[1] = '\0';
		charTwo = strtol(buf, NULL, 16);

		*XORString = dec2hex[charOne^charTwo];
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
			score -= 1;
		}
		else if(isalpha(text[i])){
			alphabet = tolower(text[i]);
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

// char *breakSingleXOR(char *cipherText){

// 	char *masterKey[13] = {"65","74","61","6f","69","6e","20","73","68","72","64","6c","75"};

// 	int hexLen = strlen(cipherText);
	
// 	int max;
// 	int maxScore = 0, score;
// 	char *hexUnitKey;
// 	char *finalKey;
// 	char *plainText;
// 	char *finalText;
// 	char Key[hexLen+1];
// 	char buf[3];
// 	unsigned frequency[256] = {0};

// 	for(int i=0; i<hexLen; i=i+2){
// 		buf[0] = cipherText[i];
// 		buf[1] = cipherText[i+1];
// 		buf[2] = '\0';
// 		++frequency[strtol(buf,NULL,16)];
// 	}

// 	for(int j=0; j<13; j++){
		
// 		max = maxFind(frequency);
// 		frequency[max] = 0;
		
// 		hexUnitKey = fixedXOR(int2hex(max),masterKey[j]);
		
// 		strcpy(Key,hexUnitKey);
// 		for(int i=0; i<hexLen; i=i+2){
// 			Key[i] = hexUnitKey[0];
// 			Key[i+1] = hexUnitKey[1];
// 		}
// 		Key[hexLen] = '\0';

// 		plainText = hex2ASCII(fixedXOR(Key, cipherText));
// 		score = scoreText(plainText);
// 		//if(!isalpha((char)hex2ASCII(hexUnitKey))) score = 0;
// 		printf("%s %s %d\n", hexUnitKey, hex2ASCII(hexUnitKey), score);
// 		if(score > maxScore){
// 			maxScore = score;
// 			finalText = plainText;
// 			finalKey = hexUnitKey;
// 		}
// 	}
// 	printf("\n");

// 	//return finalText;
// 	return finalKey;
// }

char *breakTheString(char *cipherText){

	char *masterKey[13] = {"65","74","61","6f","69","6e","20","73","68","72","64","6c","75"};
	float letterFrequencies[13] = {0.12702, 0.09056, 0.08167, 0.07507, 0.06966, 0.06749, 0.6500, 0.06327, 0.06094, 0.05987, 0.04253, 0.04025, 0.02758};

	int hexLen = strlen(cipherText);
	
	int max, findJ;
	int maxScore = 0, score;
	float freq, minimum = 1.00;
	char *hexUnitKey, *finalKey;
	char Key[hexLen+1];
	char buf[3], *temp;
	unsigned frequency[256] = {0};

	for(int i=0; i<hexLen; i=i+2){
		buf[0] = cipherText[i];
		buf[1] = cipherText[i+1];
		buf[2] = '\0';
		frequency[strtol(buf,NULL,16)] += 1;
	}

	for(int j=0; j<13; j++){
		
		max = maxFind(frequency);

		freq = (float)(frequency[max]*2)/hexLen;

		frequency[max] = 0;
		findJ = 0;
		minimum = 1;

		for(int k=0; k<13; k++){
			if (fabs(freq - letterFrequencies[k]) < minimum){
				minimum = fabs(freq - letterFrequencies[k]);
				findJ = k;
			}
		}

		
		hexUnitKey = fixedXOR(int2hex(max),masterKey[findJ]);
		
		strcpy(Key,hexUnitKey);
		for(int i=0; i<hexLen; i=i+2){
			Key[i] = hexUnitKey[0];
			Key[i+1] = hexUnitKey[1];
		}
		Key[hexLen] = '\0';

		score = scoreText(hex2ASCII(fixedXOR(Key, cipherText)));
		temp = hex2ASCII(hexUnitKey);
		//if(!isalpha(*temp) && !isspace(*temp)) score = 0;
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

		if(j==0) strcpy(Key,breakTheString(transStrings[j]));
		else strcat(Key,breakTheString(transStrings[j]));
	}

	return Key;
}

char *readFile(char *fileName)
{
    FILE *file = fopen(fileName, "r");
    char *code, c;
    int num = 0;

    if (file == NULL) return NULL;

    code = (char *)malloc(4000);

    while ((c = fgetc(file)) != EOF)
    {
        if(c != '\n'){
        	*code++ = c;
        	num += 1;
        }
    }
    *code = '\0';        
    code -= num;
    return code;
}

int main(int argc, char *argv[]){
	char *hexString = base642hex(readFile("Test.txt"));
	int keySize = findKeySize(hexString, 100, 2);
	char *key = findKey(hexString, keySize);
	printf("%s\n", hex2ASCII(key));
}