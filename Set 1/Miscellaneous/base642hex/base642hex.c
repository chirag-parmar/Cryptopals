#include<stdio.h>
#include<string.h>
#include<stdlib.h>

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

int main(int argc, char *argv[]){
	printf("HEX: %s\n", base642hex(argv[1]));
}