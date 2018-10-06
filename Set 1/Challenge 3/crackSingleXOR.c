#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

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
	}
	return score;
}

char *breakTheString(char *cipherText){

	char *masterKey[13] = {"65","74","61","6f","69","6e","20","73","68","72","64","6c","75"};

	int hexLen = strlen(cipherText);
	
	int max;
	int maxScore = 0, score;
	char *hexUnitKey;
	char *plainText;
	char *finalText;
	char Key[hexLen+1];
	char buf[3];
	unsigned frequency[256] = {0};

	for(int i=0; i<hexLen; i=i+2){
		buf[0] = cipherText[i];
		buf[1] = cipherText[i+1];
		buf[2] = '\0';
		++frequency[strtol(buf,NULL,16)];
	}

	for(int j=0; j<13; j++){
		
		max = maxFind(frequency);
		frequency[max] = 0;
		
		hexUnitKey = fixedXOR(int2hex(max),masterKey[j]);
		
		strcpy(Key,hexUnitKey);
		for(int i=0; i<hexLen; i=i+2){
			Key[i] = hexUnitKey[0];
			Key[i+1] = hexUnitKey[1];
		}
		Key[hexLen] = '\0';

		plainText = hex2ASCII(fixedXOR(Key, cipherText));
		score = scoreText(plainText);
		if(score > maxScore){
			maxScore = score;
			finalText = plainText;
		}
	}

	return finalText;
}

int main(int argc, char *argv[]){
	printf("Cracked: %s\n",breakTheString(argv[1]));
}