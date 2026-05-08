"""
# Brief.md

# [Hard] Crypto - Flippity-Flop

## Category
Crypto

## Difficulty
Hard

## Author
Absolute Unit!

## Description

We've intercepted mission-critical data from the `LFSR Gang`.

What we know so far is that they use a Linear Feedback Shift Register with 4 registers to generate a seemingly random key to encode their top-secret messages.

We have managed to recover the entire ciphertext and the first 8 bits of the plaintext.

Your task is to reconstruct the LFSR, recover the keystream, and decrypt the message.

## Objective

Use the known plaintext and ciphertext to recover the LFSR configuration, generate the full keystream, and decrypt the flag.

## Provided Data

4-bit LFSR

Plain Bits:
```
01010000
```
Cipher Bits:
```
0000100100101100111000100100011001010001010011011111100010100101110011101010110101101111111001110001011110000001110010010001010100101110111000100110110101010101001101001111111010101010101001011001100100010011100000110000100111101000110100000110110101010000111101100110001001010010010010011111111110101010110100101001100100010111100101010000110010011101110000010110111101100011
```
## Flag Format
```
P2P{...}
```
## Notes

You are given enough information to perform a known plaintext attack.

The LFSR is known to be order 4, and the first 8 bits of plaintext are provided. Use this to recover part of the keystream, derive the initial state and taps, then decrypt the rest of the ciphertext.