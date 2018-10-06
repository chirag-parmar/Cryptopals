#include<stdio.h>
#include<stdlib.h>
#include<string.h>

char *hex2base64(char *hexString){
	char *hex2bin[16] = { "0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111" };
	char *dec2base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

	int zeroPaddings = 0;
	int hexLen = strlen(hexString);
	zeroPaddings = (hexLen%3);
	
	char buf[2];
	char unitBuffer[12];
	char first[7];
	char second[7];
	char *converted;
    converted = (char*)malloc(((hexLen*4)/6) + zeroPaddings + 1);
	int j = 0;

	for(int i=0; i<(hexLen - zeroPaddings); i=i+3){
		buf[0] = hexString[i];
		strcpy(unitBuffer, hex2bin[strtol(buf,NULL,16)]);
		buf[0] = hexString[i+1];
		strcat(unitBuffer, hex2bin[strtol(buf,NULL,16)]);
		buf[0] = hexString[i+2];
		strcat(unitBuffer, hex2bin[strtol(buf,NULL,16)]);
		
		strncpy(first,unitBuffer,6);
		first[6] = '\0';
		strcpy(second,&unitBuffer[6]);
		second[6] = '\0';

		converted[j] = dec2base64[strtol(first,NULL,2)];
		converted[j+1] = dec2base64[strtol(second,NULL,2)];
		j = j+2;
	}

	if(zeroPaddings == 1){
		buf[0] = hexString[hexLen-1];
		strcpy(unitBuffer, hex2bin[strtol(buf,NULL,16)]);
		strcat(unitBuffer, "00");
		
		strncpy(first,unitBuffer,6);
		first[6] = '\0';
		
		converted[j] = dec2base64[strtol(first,NULL,2)];
		converted[j+1] = '=';
		converted[j+2] = '=';
		j = j + 3;
	}
	else if(zeroPaddings == 2){
		buf[0] = hexString[hexLen-2];
		strcpy(unitBuffer, hex2bin[strtol(buf,NULL,16)]);
		buf[0] = hexString[hexLen-1];
		strcat(unitBuffer, hex2bin[strtol(buf,NULL,16)]);
		strcat(unitBuffer, "0000");
		
		strncpy(first,unitBuffer,6);
		first[6] = '\0';
		strcpy(second,&unitBuffer[6]);
		second[6] = '\0';
		
		converted[j] = dec2base64[strtol(first,NULL,2)];
		converted[j+1] = dec2base64[strtol(second,NULL,2)];
		converted[j+2] = '=';
		j = j + 3;
	}


	converted[j] = '\0';
	return converted;
}

int main(int argc, char *argv[]){
	printf("%s", hex2base64(argv[1]));
}