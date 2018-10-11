#include<sodium.h>
int main(void)
{
    if (sodium_init() < 0) {
        printf("Wroking");
    }
    else{
    	printf("HAHA");
    }
    return 0;
}