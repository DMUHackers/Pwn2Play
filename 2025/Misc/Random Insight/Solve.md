# Solve.md

# [Easy] Misc - Random Insight - Solve Guide

## Overview

This challenge provides a Linux x86_64 binary and its source code. The program generates a random passcode using `rand()` and compares user input against that value.

Although the passcode is seeded using the current microsecond value, making it difficult to predict reliably, the value is stored in memory after generation.

The intended solution is to debug the program, pause execution after the random value has been generated, inspect the `to_guess` variable, and then enter the recovered passcode.

The final flag is:

P2P{x1m4Wof?kRh?bNf gay_}_d

## Initial Analysis

The provided source code contains the main program logic:

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

The important lines are:

gettimeofday(&tv,NULL);
srand(tv.tv_usec + 1337);
int to_guess = rand();

The program seeds the pseudo-random number generator using the current microsecond value plus `1337`, then stores the generated value in `to_guess`.

The user is then asked to enter the passcode:

scanf("%d", &input);

The input is compared against `to_guess`:

if (input == to_guess)

If the values match, the program deobfuscates and prints the flag.

## Enumeration / Inspection

Running the binary normally gives:

./random_insight

Example output:

Please enter the passcode:

Entering a random value fails:

Invalid passcode

The passcode changes between executions because it is based on the current time. This means trying to brute force or manually predict the value is unreliable.

However, the source code shows that the value is stored in a local variable:

int to_guess = rand();

This means it can be recovered with a debugger such as `gdb`.

## Method

The intended method is:

1. Open the binary in `gdb`.
2. Set a breakpoint after `to_guess` has been assigned.
3. Run the binary.
4. Inspect the value of `to_guess`.
5. Continue execution.
6. Enter the recovered value when prompted.
7. Read the printed flag.

## Exploitation / Decryption / Solution Steps

Open the binary in `gdb`:

gdb ./random_insight

Set a breakpoint at `main`:

break main

Run the program:

run

Disassemble the function to identify where `rand()` is called and where the comparison happens:

disassemble main

Alternatively, if debug symbols are available, set a breakpoint after the `rand()` assignment:

break random_insight.c:13

Then continue execution:

continue

Once execution stops after `to_guess` has been created, print the variable:

print to_guess

Example output:

$1 = 123456789

Continue execution:

continue

When prompted:

Please enter the passcode:

Enter the value recovered from `gdb`.

If the value is correct, the program prints:

The flag is P2P{x1m4Wof?kRh?bNf gay_}_d

## Commands Used

Start debugging:

gdb ./random_insight

Set a breakpoint at `main`:

break main

Run the program:

run

Disassemble `main`:

disassemble main

Set a breakpoint after `rand()` if source lines are available:

break random_insight.c:13

Continue execution:

continue

Print the passcode variable:

print to_guess

Continue and enter the recovered value:

continue

## Scripts Used

No script is required for the intended solve.

Optional `gdb` command flow:

break main
run
next
next
next
next
print to_guess
continue

If the binary contains symbols and the line numbers match the provided source, this can also be used:

break random_insight.c:13
run
print to_guess
continue

Expected result:

The flag is P2P{x1m4Wof?kRh?bNf gay_}_d