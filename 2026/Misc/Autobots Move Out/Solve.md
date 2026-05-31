# [Medium] Misc - Autobots Move Out - Solve Guide

## Overview
A password hash is provided alongside a pre-generated wordlist. Straight dictionary attacks fail because the password conforms to a strict policy requiring capitalisation, a four-digit suffix, and a trailing symbol. The wordlist contains the correct base word but in the wrong form — John the Ripper's rule and mask system must be used to apply the required transformations before cracking succeeds.

## Initial Analysis
The challenge title "Autobots Move Out" is a Transformers reference — the hint is "transform". The wordlist already exists, but the raw words don't match the policy. The three policy constraints define exactly what transformations are needed:

| Constraint | Transformation required |
|---|---|
| Starts with a capital letter | Capitalise first letter of each candidate |
| Ends in four digits | Append a 4-digit number (likely a year) |
| Ends in a symbol after the digits | Append one of `!@#$` etc. after the digits |

The base word in the wordlist is likely `innovationcentre` — directly referencing the organisation in the scenario, which is a very common real-world password pattern.

## Enumeration / Inspection

### Step 1 — Identify the hash type

Inspect the hash visually or use `hashid`:

```bash
hashid md5.txt
# or
hash-identifier
```

A 32-character hex string with no prefix is almost certainly **MD5**. John the Ripper uses `--format=Raw-MD5` for unsalted MD5 hashes.

## Method
- **Hash type:** MD5 (Raw, unsalted)
- **Technique:** Rule-based transformation with mask extension in John the Ripper — capitalise base word, append 4-digit year, append symbol

## Exploitation / Decryption / Solution Steps

### Step 2 — Crack with John using rules and a mask

John's `--mask` option extends each wordlist candidate with a fixed pattern. The `?w` token inserts the current wordlist word, allowing hybrid attacks that combine dictionary candidates with mask patterns.

```bash
john --format=Raw-MD5 \
     --wordlist=wordlist.txt \
     --rules=Single \
     --mask='?w?d?d?d?d?1' \
     --1='!@#$' \
     md5.txt
```

**Flag breakdown:**
- `--format=Raw-MD5` — specifies unsalted MD5
- `--wordlist=wordlist.txt` — base word source
- `--rules=Single` — applies built-in Single mode rules including capitalisation
- `--mask='?w?d?d?d?d?1'` — hybrid mask: word + 4 digits + 1 symbol from custom set
- `--1='!@#$'` — defines the custom character set for `?1`

John will mutate each base word (e.g. `innovationcentre` → `Innovationcentre`), then append every combination of 4 digits and a symbol from the set. The correct candidate `Innovationcentre1995!` will match the stored hash.

**Display the cracked password:**
```bash
john --show --format=Raw-MD5 md5.txt
```

### Step 3 — Alternative: informed guessing

If the tooling approach is unfamiliar, the password can also be reasoned out:

- The wordlist likely contains `innovationcentre` (the obvious organisation-linked base word)
- Apply the policy: capitalise → `Innovationcentre`
- Four digits → likely a year; try significant years (founding year, current year, common defaults like `2024`, `1995`)
- One symbol → `!` is by far the most common trailing symbol in real-world passwords

Test candidates directly:

```bash
echo -n "Innovationcentre1995!" | md5sum
# Compare output to the hash in md5.txt
```

### Step 4 — Format the flag

Convert the recovered password to uppercase and wrap in the flag format:

```
Innovationcentre1995!  →  INNOVATIONCENTRE1995!
```

**Flag:** `P2P{INNOVATIONCENTRE1995!}`

## Commands Used

```bash
# Identify hash type
hashid md5.txt

# Crack with John — rule + mask hybrid attack
john --format=Raw-MD5 \
     --wordlist=wordlist.txt \
     --rules=Single \
     --mask='?w?d?d?d?d?1' \
     --1='!@#$' \
     md5.txt

# Display cracked result
john --show --format=Raw-MD5 md5.txt

# Manual verification (alternative approach)
echo -n "Innovationcentre1995!" | md5sum
```

## Scripts Used
None — John the Ripper handles all transformation and cracking natively.
