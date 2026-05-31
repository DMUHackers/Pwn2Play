# [Easy] Misc - Mud on Your Face - Solve Guide

## Overview
A password-protected ZIP archive is provided. The password is a real phrase present in the `rockyou.txt` wordlist. The challenge requires running a dictionary attack against the archive to recover the password, then extracting the flag from the contents.

## Initial Analysis
The description hints "choose your words carefully" — a nudge toward a wordlist-based attack. Password-protected ZIPs store enough metadata for offline cracking without needing to interact with any remote service. This is a straightforward dictionary attack challenge.

The archive filename (`1774262373flag.zip`) is arbitrary and contains no meaningful hints beyond confirming a flag file is inside.

## Enumeration / Inspection
Confirm the archive is password protected:

```bash
unzip -l 1774262373flag.zip
# Output will prompt for a password or show encrypted entries
```

No hash extraction is needed for `fcrackzip` — it attacks the ZIP directly. If using `john` or `hashcat`, the hash must first be extracted with `zip2john`.

## Method
- **Vulnerability:** Weak password present in a common wordlist
- **Technique:** Dictionary attack against the ZIP archive using `rockyou.txt`

## Exploitation / Decryption / Solution Steps

### Step 1 — Obtain the wordlist

Most CTF environments and Kali Linux include `rockyou.txt` at:
```
/usr/share/wordlists/rockyou.txt
```

If using the provided wordlist variant:
```
rockyou_2025_03.txt
```

### Step 2 — Run the dictionary attack

**Option A — fcrackzip (recommended, fast for ZIPs):**
```bash
fcrackzip -u -D -p rockyou_2025_03.txt 1774262373flag.zip
```

Flags explained:
- `-u` — use `unzip` to verify candidate passwords (eliminates false positives)
- `-D` — dictionary mode
- `-p` — path to the wordlist

**Expected output:**
```
PASSWORD FOUND!!!!: pw == gnomeindahouse
```

**Option B — zip2john + john:**
```bash
zip2john 1774262373flag.zip > zip.hash
john zip.hash --wordlist=rockyou_2025_03.txt
john zip.hash --show
```

**Option C — zip2john + hashcat:**
```bash
zip2john 1774262373flag.zip > zip.hash
# Extract just the hash line for hashcat
hashcat -m 17225 zip.hash rockyou_2025_03.txt
```

### Step 3 — Extract the archive

Once the password `gnomeindahouse` is recovered, extract the contents:

```bash
unzip 1774262373flag.zip
# Enter password: gnomeindahouse
```

Open the extracted flag file to retrieve the flag.

**Flag:** `P2P{15e474d2946628dcdd1714fdaef07f59}`

## Commands Used

```bash
# Confirm archive is encrypted
unzip -l 1774262373flag.zip

# Dictionary attack with fcrackzip
fcrackzip -u -D -p rockyou_2025_03.txt 1774262373flag.zip

# Alternative: zip2john + john
zip2john 1774262373flag.zip > zip.hash
john zip.hash --wordlist=rockyou_2025_03.txt
john zip.hash --show

# Extract the archive
unzip 1774262373flag.zip
```

## Scripts Used
None — standard tooling is sufficient.
