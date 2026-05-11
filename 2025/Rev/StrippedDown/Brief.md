# brief.md


# [Medium] Rev - StrippedDown

## Category

Reverse Engineering (Rev)

## Difficulty

Medium

## Author

Thetvdh

## Description

A stripped binary has been provided containing a hidden flag. The binary includes basic anti-debugging protections to make dynamic analysis more annoying.

Your task is to reverse the decryption routine, locate the hidden encrypted flag fragments and recover the original flag.

## Objective

Reverse engineer the binary, identify the XOR decryption logic, recover the encrypted flag fragments and reconstruct the original flag.

## Provided Files

- chall

## Flag Format
```
P2P{...}
```
## Notes

- The binary has been stripped.
- Basic anti-debugging checks are present.
- The flag is split into multiple encrypted fragments.
- Static analysis tools such as Ghidra are recommended.


---