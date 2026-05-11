# Brief.md

# [Easy] Crypto - Flag Enough and Time

## Category

Crypto

## Difficulty

Easy

## Author

Thetvdh

## Description

A flag has been encrypted using a simple time-based encryption routine. The challenge provides the encrypted flag output and the exact time at which the encryption took place.

The encryption may look unusual at first due to the non-standard characters in the output, but the key detail is hidden in plain sight: the timestamp.

Participants must work out how the timestamp is used during encryption and reverse the process to recover the original flag.

## Objective

Recover the original flag from the encrypted output and timestamp.

## Provided Files

- `chall.hs`
- `flag.txt`

## Flag Format

P2P{...}

## Notes

The challenge provides the following encrypted output:

Flag: Ա̗ԴބէׂЇͲە׈ߡ̇Ӥ̤շׂӷ۲̅ݸ
Time encrypted: 2025-04-15T14:27:38.497932242Z

Participants should inspect the provided Haskell source code to understand how the encryption key is generated and applied.