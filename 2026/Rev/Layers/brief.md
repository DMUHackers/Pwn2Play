# Challenge Brief: Layers 🧅

## Category
Reverse Engineering

## Difficulty
Medium

## Description

*"Many layers await your discovery..."*

A binary has been recovered. It's not what it seems — what you see on the surface is designed to mislead you. The real payload is buried beneath multiple layers of obfuscation, encryption, and misdirection.

Peel back the layers.

## Artifacts

| File | Description |
|------|-------------|
| `challenge` | 64-bit x86-64 ELF binary, not stripped |

## What You're Up Against

The binary is deliberately deceptive:

- **Fake flags** are scattered throughout the strings to mislead static analysis
- **Anti-debug** protection will detect and disrupt naive dynamic analysis
- **Distraction functions** with convincing names do nothing useful
- **The real payload** is hidden and encrypted inside the binary itself

## Objectives

| # | Objective |
|---|-----------|
| 1 | Identify and bypass the anti-debug mechanism |
| 2 | Locate the encrypted payload in the binary |
| 3 | Recover the decryption key and decrypt the payload |
| 4 | Analyse the decrypted payload for the real flag logic |
| 5 | Reconstruct the flag transformation and decode it |

## Hints

- Not all strings are real. Not all functions matter.
- The binary carries something hidden in its `.data` section.
- The outer binary decrypts something — but never runs it. That's your job.

## Flag Format

```
P2P{flag_content}
```
