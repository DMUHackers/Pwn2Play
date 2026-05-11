# Brief.md

# [Easy] Misc - Random Insight

## Category

Misc

## Difficulty

Easy

## Author

Skyzer Flyzer

## Description

A suspicious binary has been recovered from a group believed to be using it to protect their communications. The program appears to generate a random passcode before allowing access to the decrypted message.

The source code suggests that the passcode is generated using `rand()`, with the seed based on the current time. This makes the value difficult to predict before the program runs.

However, the passcode exists in memory after it has been generated and before the user is asked to enter it.

Your task is to inspect the running program, recover the generated passcode, and use it to reveal the hidden flag.

## Objective

Recover the correct passcode from the running binary and use it to reveal the flag.

## Provided Files

- `random_insight.c`
- `random_insight`
- `README.md`

## Flag Format

P2P{...}

## Notes

The binary is intended to run on Linux x86_64.

Participants are given both the compiled binary and the source code. The source code contains the overall program logic, but the intended solution requires inspecting the program at runtime rather than attempting to predict the random value in advance.


