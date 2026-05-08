# Solve.md

# [Hard] Crypto - Flippity-Flop - Solve Guide

## Overview

This challenge is a known plaintext attack against a stream cipher.

The stream cipher uses a 4-bit Linear Feedback Shift Register to generate a keystream. The plaintext is XORed with the keystream to produce the ciphertext.

We are given:

- The full ciphertext
- The first 8 bits of plaintext
- The knowledge that the LFSR has 4 registers

This is enough to recover the LFSR state, derive the taps, regenerate the full keystream, and decrypt the message.

## Initial Data

Known plaintext bits:
```
01010000
```
Ciphertext bits:
```
0000100100101100111000100100011001010001010011011111100010100101110011101010110101101111111001110001011110000001110010010001010100101110111000100110110101010101001101001111111010101010101001011001100100010011100000110000100111101000110100000110110101010000111101100110001001010010010010011111111110101010110100101001100100010111100101010000110010011101110000010110111101100011
```
## Recovering the Partial Keystream

For a stream cipher:

> ciphertext XOR keystream = plaintext

Therefore:

> plaintext XOR ciphertext = keystream

Using the first 8 bits:

Plaintext:
```
01010000
```
Ciphertext:
```
00001001
```
XOR result:
```
01011001
```
So the first 8 bits of the keystream are:
```
01011001
```
## Recovering the Initial State

We know the LFSR has 4 registers.

The first 4 bits of the recovered keystream provide the initial register state, but in reverse order.

Recovered first 4 keystream bits:
```
0101
```
Reversed:
```
1010
```
Therefore the initial state is:
```
1010
```
## Deriving the LFSR Taps

We now need to determine which taps are enabled.

The first few LFSR states and outputs are:
```
1010 => 1
1101 => 0
0110 => 0
0011 => 1
```
Let the tap coefficients be:
```
c0, c1, c2, c3
```
Working modulo 2, the equations are:
```
c3 +      c1      ≡ 1 mod 2
c3 + c2 +      c0 ≡ 0 mod 2
     c2 + c1      ≡ 0 mod 2
          c1 + c0 ≡ 1 mod 2
```
Solving these equations gives:
```
c0 = 1
c1 = 0
c2 = 0
c3 = 1
```
This means the feedback polynomial is:
```
x^4 + x^3 + 1
```
The feedback bit is produced by XORing bit 0 and bit 3.

## LFSR Implementation

The recovered LFSR can be implemented as follows:
```
initialState = 0b1010

def LFSR4():
    state = initialState

    for i in range(8 * 47):
        print(state & 1, end="")

        newBit = (state ^ (state >> 3)) & 1
        state = (state >> 1) | (newBit << 3)

LFSR4()
```
This generates the keystream:
```
0101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110101100100011110
```
## Decryption

Once the keystream has been regenerated, XOR it against the full ciphertext to recover the plaintext.

## Full Solve Script
```python
cipher_bits = (
    "000010010010110011100010010001100101000101001101111110001010010111001110"
    "101011010110111111100111000101111000000111001001000101010010111011100010"
    "011011010101010100110100111111101010101010100101100110010001001110000011"
    "000010011110100011010000011011010101000011110110011000100101001001001001"
    "111111111010101011010010100110010001011110010101000011001001110111000001"
    "0110111101100011"
)

initial_state = 0b1010

def generate_lfsr_bits(length):
    state = initial_state
    bits = []

    for _ in range(length):
        bits.append(str(state & 1))
        new_bit = (state ^ (state >> 3)) & 1
        state = (state >> 1) | (new_bit << 3)

    return "".join(bits)

def bits_to_bytes(bit_string):
    output = bytearray()

    for i in range(0, len(bit_string), 8):
        byte = bit_string[i:i + 8]
        if len(byte) == 8:
            output.append(int(byte, 2))

    return bytes(output)

key_bits = generate_lfsr_bits(len(cipher_bits))

plain_bits = "".join(
    str(int(c) ^ int(k))
    for c, k in zip(cipher_bits, key_bits)
)

plaintext = bits_to_bytes(plain_bits)

print(plaintext.decode())
```
## Output
```
P2P{570P_FL1P-FL0PP1N6_4r0UND_4ND_637_Cr4CK1N6}
```
## Flag
```
P2P{570P_FL1P-FL0PP1N6_4r0UND_4ND_637_Cr4CK1N6}
```
## Lessons Learned

This challenge demonstrates a known plaintext attack against a stream cipher using a Linear Feedback Shift Register.

The important steps were:

1. XOR the known plaintext with the matching ciphertext bits to recover part of the keystream.
2. Use the recovered keystream to determine the initial 4-bit LFSR state.
3. Use the observed LFSR outputs to derive the tap coefficients.
4. Reconstruct the LFSR.
5. Generate the full keystream.
6. XOR the keystream with the ciphertext to recover the flag.