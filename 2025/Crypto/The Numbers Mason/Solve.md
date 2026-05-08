# Solve.md

# [Easy] Crypto - The Numbers Mason - Solve Guide

## Overview

This challenge provides a Russian-language transmission containing a repeated sequence of decimal values.

The key Russian phrases are:
```
Повторить. = Repeat.

Завершить передачу. = End transmission.

The repeated decimal values are:

57 12 140 125 114 71 52 44 216 16 15 47 111 119 13 101 214 112 229

These values form the one-time pad needed to decrypt the challenge ciphertext.
```
## Initial Analysis

The transmission gives the following decimal byte sequence:
```
57 12 140 125 114 71 52 44 216 16 15 47 111 119 13 101 214 112 229
```
Convert these decimal values into hexadecimal:
```
39 0C 8C 7D 72 47 34 2C D8 10 0F 2F 6F 77 0D 65 D6 70 E5
```
This gives the one-time pad:
```
39 0C 8C 7D 72 47 34 2C D8 10 0F 2F 6F 77 0D 65 D6 70 E5
```
## Ciphertext

The ciphertext is Base64 encoded:
```
ejzAGQV0Rk+qaX97ABB/JKYYnA==
```
Decode the Base64 ciphertext into bytes, then XOR each ciphertext byte with the corresponding byte from the one-time pad.

## Method

The decryption process is:

1. Extract the decimal values from the transmission.
2. Convert the decimal values to bytes.
3. Decode the Base64 ciphertext.
4. XOR the ciphertext bytes with the extracted byte sequence.
5. Wrap the recovered plaintext in the expected flag format.

## Solve Script

```python
import base64

ciphertext_b64 = "ejzAGQV0Rk+qaX97ABB/JKYYnA=="

otp_decimal = [
    57, 12, 140, 125, 114, 71, 52, 44, 216, 16,
    15, 47, 111, 119, 13, 101, 214, 112, 229
]

ciphertext = base64.b64decode(ciphertext_b64)

plaintext = "".join(
    chr(c ^ k)
    for c, k in zip(ciphertext, otp_decimal)
)

flag = f"P2P{{{plaintext}}}"

print(flag)