# [Easy] Misc - It Sure Would Be Cewl - Solve Guide

## Overview
Two Linux credential files (`passwd` and `shadow`) are provided. The password is not in a generic wordlist — instead, it is a word scraped from the DMU Hackers website. The challenge requires generating a targeted wordlist using `cewl`, combining the credential files with `unshadow`, and cracking the hash with `john`.

## Initial Analysis
The challenge title is a direct hint — "Cewl" refers to **CeWL (Custom Word List generator)**, a tool that spiders a target website and generates a wordlist from the words found on its pages. This is a common real-world technique for cracking passwords linked to an organisation, as people frequently choose passwords related to their own community or interests.

Generic wordlists like `rockyou.txt` will not work here. The password is organisation-specific and only appears in content scraped from `https://dmuhackers.com/`.

## Enumeration / Inspection
Inspect the shadow file to confirm the hash format:

```bash
cat shadow
```

Hashes beginning with `$6$` are **SHA-512crypt** — the standard format for modern Linux systems. John the Ripper handles this natively with `--format=sha512crypt`.

Note that only one account in the shadow file has a crackable password — all others will not yield results against this wordlist.

## Method
- **Vulnerability:** Weak, organisation-specific password susceptible to a targeted wordlist attack
- **Technique:** CeWL website scrape → `unshadow` credential merge → John the Ripper dictionary attack

## Exploitation / Decryption / Solution Steps

### Step 1 — Generate a targeted wordlist with CeWL

Spider the DMU Hackers website and output every word found to a wordlist file:

```bash
cewl https://dmuhackers.com/ > wordlist.txt
```

CeWL crawls the site, extracts all words, and writes them one per line. By default it follows links to a depth of 2 and captures words of 3+ characters. The password `siegelocation` will be present in this output.

To increase coverage (deeper crawl, longer/shorter words):
```bash
cewl -d 3 -m 5 https://dmuhackers.com/ > wordlist.txt
```

### Step 2 — Combine passwd and shadow with unshadow

`john` expects a single merged file. `unshadow` combines `passwd` and `shadow` into the correct format:

```bash
unshadow passwd shadow > unshadowed
```

### Step 3 — Crack the hash with John the Ripper

Run a dictionary attack using the generated wordlist against the SHA-512crypt hashes:

```bash
john --wordlist=wordlist.txt --format=sha512crypt unshadowed
```

John will crack the target password in under 2 seconds. All other hashes in the file are not crackable with this wordlist.

**Display cracked credentials:**
```bash
john --show unshadowed
```

**Expected output:**
```
john:siegelocation:...
```

### Step 4 — Format the flag

Take the cracked username and password, convert both to uppercase, and wrap in the flag format:

```
Username: john  →  JOHN
Password: siegelocation  →  SIEGELOCATION
```

**Flag:** `P2P{JOHN:SIEGELOCATION}`

## Commands Used

```bash
# Step 1 — Generate targeted wordlist from the target website
cewl https://dmuhackers.com/ > wordlist.txt

# Step 2 — Merge passwd and shadow files
unshadow passwd shadow > unshadowed

# Step 3 — Run dictionary attack
john --wordlist=wordlist.txt --format=sha512crypt unshadowed

# Step 4 — Display cracked passwords
john --show unshadowed
```

## Scripts Used
None — standard tooling is sufficient.
