# Solve.md

# [Easy] Crypto - Flag Enough and Time - Solve Guide

## Overview

This challenge provides an encrypted flag and the timestamp used during encryption.

The encryption routine uses the time of encryption as part of the key material. Once the timestamp is converted into the same format used by the program, the encryption can be reversed to recover the plaintext flag.

The final flag is:
```
P2P{u_C4n_T3lL_t1M3}
```
## Initial Analysis

The challenge gives two important pieces of information:
```
Flag: Ա̗ԴބէׂЇͲە׈ߡ̇Ӥ̤շׂӷ۲̅ݸ
Time encrypted: 2025-04-15T14:27:38.497932242Z
```
The provided Haskell source imports time and bitwise operations, including:
```haskell
import Data.Time
import Data.Time.Clock.POSIX (utcTimeToPOSIXSeconds)
import Data.Bits (xor, shiftL)
```
This strongly suggests that the encryption process uses:

- the timestamp
- a conversion to Unix epoch time
- XOR-based encryption

Because XOR is reversible, the same operation can be used to decrypt the ciphertext.

## Enumeration / Inspection

The key observations are:

1. The timestamp is not just metadata. It is used as the encryption key.
2. The ISO timestamp must be converted into Unix epoch time.
3. The epoch value is used to generate or derive the XOR key.
4. XOR encryption can be reversed because:

ciphertext XOR key = plaintext
plaintext XOR key = ciphertext

The timestamp provided is:
```
2025-04-15T14:27:38.497932242Z
```
Converted to Unix epoch seconds, this becomes:
```
1744727258
```
This value is then used to reverse the encryption process.

## Method

The solution process is:

1. Read the encrypted flag from `flag.txt`.
2. Read the timestamp from the same file.
3. Parse the timestamp as UTC time.
4. Convert the timestamp to Unix epoch seconds.
5. Recreate the same key material used by the original encryption script.
6. XOR the encrypted characters with the generated key.
7. Recover the plaintext flag.

## Exploitation / Decryption / Solution Steps

A simple Python script can be used to reverse the encryption.

The important part is ensuring the timestamp is converted correctly and that the ciphertext characters are handled as Unicode codepoints.

```python
from datetime import datetime, timezone

ciphertext = "Ա̗ԴބէׂЇͲە׈ߡ̇Ӥ̤շׂӷ۲̅ݸ"
timestamp = "2025-04-15T14:27:38.497932242Z"

# Python only supports microseconds directly, so trim nanoseconds to microseconds
timestamp_trimmed = timestamp.replace("Z", "+00:00")
date_part, tz_part = timestamp_trimmed.split("+")
main_time, fractional = date_part.split(".")
fractional = fractional[:6]

dt = datetime.fromisoformat(f"{main_time}.{fractional}+{tz_part}")
epoch = int(dt.timestamp())

key = str(epoch)

plaintext = ""

for i, char in enumerate(ciphertext):
    key_char = key[i % len(key)]
    decrypted_char = chr(ord(char) ^ ord(key_char))
    plaintext += decrypted_char

print(plaintext)