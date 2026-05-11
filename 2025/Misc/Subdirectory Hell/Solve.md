# solve.md


# [Easy] Misc - Subdirectory Hell - Solve Guide

## Overview

This challenge involves searching through a large nested directory structure filled with many files containing repeated junk data.

The goal is to identify the single file that differs from the rest and decode the hidden flag.

Flag:
`P2P{m4nY_D1r3c70r135_7h3r3_4R3}`

---

## Initial Analysis

Extract the archive:

```bash
tar -xvf subdir_hell.tar.gz
```

Inspecting the extracted directories reveals a huge number of nested folders and files.

Manually checking every file is technically possible, but extremely inefficient.

---

## Enumeration / Inspection

After inspecting several files, it becomes clear that almost all files contain one of two repeated messages.

The two repeated strings are:

```text
vdCB
gbm
```

This suggests that the correct file is the only one that does not match either pattern.

---

## Method

### Step 1 — Use Inverse Grep

Use `grep` with inverse matching to locate files that do not contain the repeated junk strings:

```bash
grep -vRE "(vdCB|gbm)" chall/
```

This returns a single suspicious entry containing Base64 data.

---

### Step 2 — Decode the Base64

Copy the returned Base64 string and decode it:

```bash
echo "<base64>" | base64 -d
```

The decoded output reveals the flag:

```text
P2P{m4nY_D1r3c70r135_7h3r3_4R3}
```

---

## Exploitation / Decryption / Solution Steps

1. Extract the archive
2. Observe repeated junk messages in files
3. Use inverse grep to find anomalous content
4. Identify the Base64 encoded string
5. Decode the Base64 data
6. Recover the flag

---

## Commands Used

```bash
tar -xvf subdir_hell.tar.gz
grep -vRE "(vdCB|gbm)" chall/
echo "<base64>" | base64 -d
```

---

## Scripts Used

No custom scripts were required.
