"""
# Brief.md

# [Hard] Crypto - NonceSense

## Category
Crypto

## Difficulty
Hard

## Author
Thetvdh

## Description

An ECDSA signing system has made a dangerous mistake.

Two different messages have been signed using the same nonce. This causes both signatures to share the same `r` value, which can be exploited to recover the nonce and then the private key.

Your task is to analyse the provided signature data, identify the vulnerability, recover the private key, and submit it as the flag.

## Objective

Recover the ECDSA private key from the provided signatures.

## Provided Files

- message.txt

## Challenge Data

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
## Flag Format
```
P2P{<hex_of_private_key>}
```
## Notes

In ECDSA, reusing the same nonce `k` across two different messages is fatal.

If two signatures share the same `r` value, this usually means the same nonce was reused.