#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

int main(int argc, char * argv[]){
	printf("%d", hex2int(argv[1]));
}