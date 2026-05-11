# solve.md

# [Medium] Rev - StrippedDown - Solve Guide

## Overview

This challenge focuses on reversing a stripped ELF binary that hides the flag in several encrypted fragments.

The binary contains:

- Basic anti-debugging protections
- XOR-based encryption
- Multiple separated flag fragments
- No symbols due to stripping

The intended solution path is static analysis using a reverse engineering tool such as Ghidra.

Flag:
`P2P{5pl1771ng_4nd_h1d1ng_fl4g5_15_n07_n1c3}`

---

## Initial Analysis

Start by identifying the file type:

```bash
file chall
```

Check for protections:

```bash
checksec chall
```

Running the binary under GDB may trigger anti-debugging protections, making dynamic analysis less useful.

The binary has also been stripped, meaning function names and symbols are removed.

---

## Enumeration / Inspection

Open the binary in Ghidra.

Since symbols are missing, begin by identifying suspicious functions manually.

Useful indicators include:

- XOR operations
- loops over byte arrays
- memory comparisons
- references to encoded data

One function performs XOR decryption on several arrays stored in the binary.

A comparison against `0x30` reveals that there are 6 encrypted parts to recover.

---

## Method

### Step 1 — Identify the XOR Decryption Function

In Ghidra, locate the function responsible for decrypting data.

Indicators include:

```c
buffer[i] ^= key;
```

or equivalent assembly instructions using XOR.

Recover:

- the XOR key
- the encrypted arrays
- the loop structure

---

### Step 2 — Locate the Encrypted Arrays

Find the offsets in the binary containing the encrypted flag fragments.

The flag is split into 6 separate arrays.

The number 6 can be inferred from the comparison against:

```c
0x30
```

which corresponds to 6 groups of 8 bytes.

Extract all encrypted byte arrays from the binary.

---

### Step 3 — Write a Decode Script

Once the XOR key and encrypted bytes are known, write a small Python script to recover the plaintext.

Example structure:

```python
parts = [
    [...],
    [...],
]

key = 0x00

flag = ""

for part in parts:
    flag += ''.join(chr(x ^ key) for x in part)

print(flag)
```

Running the script reveals the flag.

---

## Exploitation / Decryption / Solution Steps

1. Identify the binary type
2. Open the binary in Ghidra
3. Locate the XOR decryption routine
4. Recover the XOR key
5. Identify the encrypted flag arrays
6. Extract all 6 fragments
7. Write a Python script to XOR-decode the data
8. Concatenate the fragments
9. Recover the final flag

---

## Commands Used

```bash
file chall
checksec chall
strings chall
```

---

## Scripts Used

Example decoding script:

```python
parts = [
    # encrypted arrays
]

key = 0x00

flag = ""

for part in parts:
    flag += ''.join(chr(b ^ key) for b in part)

print(flag)
```