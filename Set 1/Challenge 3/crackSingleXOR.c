#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

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
	char *hexUnitKey;
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
			finalText = plainText;
		}
	}

	return finalText;
}

int main(int argc, char *argv[]){
	printf("Cracked: %s\n",breakSingleXOR(argv[1]));
}