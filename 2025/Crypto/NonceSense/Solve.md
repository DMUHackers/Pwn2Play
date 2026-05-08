# Solve.md

# [Hard] Crypto - NonceSense - Solve Guide

## Overview

This challenge involves exploiting nonce reuse in ECDSA.

ECDSA requires a fresh random nonce `k` for every signature. If the same nonce is reused to sign two different messages with the same private key, the private key can be recovered.

In this challenge, both signatures use the same `r` value:

0x32fc9cc541a21eb26d189a25ef38c9b5ba9fafa8c5bd829674c26fe9911b7478

This indicates that the same nonce was reused.

## Given Data

Curve:
```
secp256k1
```
Message 1:
```
Hello ECDSA! How are you today?

r1:

0x32fc9cc541a21eb26d189a25ef38c9b5ba9fafa8c5bd829674c26fe9911b7478

s1:

0x22b3eccd7f2db1fdb44ef97d367289dd8617155cfbfc0a831799574a3d34930a
```
Message 2:
```
Don't reuse nonces! (why isn't there a better word for it...)

r2:

0x32fc9cc541a21eb26d189a25ef38c9b5ba9fafa8c5bd829674c26fe9911b7478

s2:

Provided in `message.txt`
```
## The Vulnerability

ECDSA signatures are generated using:
```
s = k^-1 * (z + r * d) mod n
```
Where:

- `s` is the signature value
- `k` is the nonce
- `z` is the hash of the message
- `r` is derived from `kG`
- `d` is the private key
- `n` is the order of the curve

If two messages are signed with the same nonce `k`, then the same `r` value appears in both signatures.

For two signatures:
```
s1 = k^-1 * (z1 + r * d) mod n

s2 = k^-1 * (z2 + r * d) mod n
```
Subtracting them gives:
```
s1 - s2 = k^-1 * (z1 - z2) mod n
```
Therefore:
```
k = (z1 - z2) * (s1 - s2)^-1 mod n
```
Once `k` is known, recover the private key:
```
d = (s1 * k - z1) * r^-1 mod n
```
## Method

The solving process is:

1. Hash both messages with SHA256.
2. Convert the hashes into integers.
3. Confirm both signatures share the same `r`.
4. Recover the reused nonce `k`.
5. Use `k` to recover the private key.
6. Submit the private key as hexadecimal inside the flag format.

## Solve Script

Replace the `s2` value with the value provided in `message.txt`.
```python
from hashlib import sha256

# secp256k1 curve order
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

message1 = b"Hello ECDSA! How are you today?"
message2 = b"Don't reuse nonces! (why isn't there a better word for it...)"

r = 0x32fc9cc541a21eb26d189a25ef38c9b5ba9fafa8c5bd829674c26fe9911b7478

s1 = 0x22b3eccd7f2db1fdb44ef97d367289dd8617155cfbfc0a831799574a3d34930a

# Replace this with the s2 value from message.txt
s2 = 0xREPLACE_ME

z1 = int.from_bytes(sha256(message1).digest(), "big")
z2 = int.from_bytes(sha256(message2).digest(), "big")

def inv_mod(x, n):
    return pow(x, -1, n)

# Recover reused nonce
k = ((z1 - z2) * inv_mod(s1 - s2, n)) % n

# Recover private key
private_key = ((s1 * k - z1) * inv_mod(r, n)) % n

print(hex(private_key))
print(f"P2P{{{private_key:064x}}}")
```
## Explanation

The key step is recovering the reused nonce:
```
k = (z1 - z2) * inverse(s1 - s2) mod n
```
This works because both signatures used the same nonce, which caused the same `r` value to appear in both signatures.

Once the nonce is recovered, the ECDSA signing equation can be rearranged to solve for the private key:
```
d = (s1 * k - z1) * inverse(r) mod n
```
## Key Finding

The repeated `r` value proves that the same nonce was reused across two ECDSA signatures.

This makes the private key recoverable.

## Flag
```
P2P{92b0cd2bd80433e0a2f362a712897dcddad1c53299c4799d8a44af231048d79a}
```
## Lessons Learned

This challenge demonstrates why nonce reuse in ECDSA is catastrophic.

The important steps were:

1. Identify that both signatures share the same `r`.
2. Understand that reused `r` implies reused nonce `k`.
3. Hash both messages with SHA256.
4. Recover the nonce using both signatures.
5. Recover the private key from the nonce.
6. Submit the private key as the flag.