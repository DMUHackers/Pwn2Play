# Challenge Brief: Ghost Protocol 👻

## Category
Reverse Engineering

## Difficulty
Hard

## Description

A mysterious binary was recovered from a compromised server during an incident response engagement. Analysts believe it contains the **activation code** for a dormant threat actor's command infrastructure.

The binary appears to implement a custom **protocol verification system** — it accepts input and validates it against an internal expected value. No source code is available.

Your mission: reverse engineer the binary and extract the protocol key.

## Artifacts

| File | Description |
|------|-------------|
| `ghost_protocol` | ELF binary (MIPS 32-bit) implementing a custom virtual machine |

## What You're Up Against

- The binary implements a **custom SpecterVM** — a bespoke 21-opcode virtual machine
- The VM bytecode is **dual-layer encrypted** at rest inside the binary
- Operands are **obfuscated** using positional XOR
- Input characters are individually **transformed** through a chained sequence of XOR, rotation, and addition operations
- Packets (characters) are verified one at a time via `CMP` instructions inside the VM

## Objectives

| # | Objective |
|---|-----------|
| 1 | Identify the SpecterVM architecture and its 21 opcodes |
| 2 | Decrypt the bytecode (dual-layer XOR: static key + ELF header-derived key) |
| 3 | Deobfuscate operands (position XOR with seed `0x3C`) |
| 4 | Disassemble the VM program and locate `CMP` instructions |
| 5 | Extract the expected (transformed) values from each `CMP r0, r1` |
| 6 | Reverse the per-character transformation to recover the original input |

## Flag Format

```
P2P{flag_content}
```
