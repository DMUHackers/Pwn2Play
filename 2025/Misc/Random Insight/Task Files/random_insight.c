#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <libs/obfuscator.h>


int main(){
    char flag[] = "UDNSeGIxbTRXb2Y/a1JoP2JOZiBnYX95f2Q=";
    struct timeval tv;
    gettimeofday(&tv,NULL);
    srand(tv.tv_usec + 1337);
    int to_guess = rand();
    int input;
    printf("Please enter the passcode: \n");
    scanf("%d", &input);
    if (input == to_guess) {
        char * actual_flag = deobfuscate(flag);
        printf("The flag is %s\n", actual_flag);
        free(actual_flag);
    }else{
        printf("Invalid passcode\n");
    }
    return 0;
}