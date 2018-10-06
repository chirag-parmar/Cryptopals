#include<stdio.h>
#include<stdlib.h>
#include<string.h>

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

int main(int argc, char *argv[]){
	printf("Hamming Distance: %d", hammingDistance(argv[1],argv[2]));
}