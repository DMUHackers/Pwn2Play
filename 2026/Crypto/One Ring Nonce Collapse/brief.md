# Challenge Brief: One Ring Nonce Collapse 💍

## Category
Crypto

## Difficulty
Hard

## Description

*"One oracle to sign them all, one nonce to find them, one lattice to bring them all, and in the darkness bind them."*

A signing oracle has been discovered on a compromised server. It will sign any message you send — except the one that matters. Every signature it returns comes with a small gift: the top bits of the ephemeral signing nonce.

The oracle is generous, but not wise. Can you hear what it's telling you?

## Setup

```bash
docker pull biterra/one-ring-nonce-collapse:latest
docker run -p 5000:5000 biterra/one-ring-nonce-collapse:latest
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/pubkey` | GET | Returns curve parameters, public key, `unknown_bits`, `max_signatures` |
| `/sign` | POST `{"message": "..."}` | Signs a message; returns `r, s, h, nonce_msb, remaining` |
| `/verify` | POST `{"r": "...", "s": "..."}` | Verifies a signature for the protected message; returns flag if valid |

## Rules

- The oracle will sign any message **except** `"one ring to rule them all"`
- You have a maximum of **56** signature requests
- The `/verify` endpoint checks the protected message only

## Objectives

| # | Objective |
|---|-----------|
| 1 | Understand what `nonce_msb` reveals about the signing nonce `k` |
| 2 | Collect enough biased signatures from the oracle |
| 3 | Formulate the bias as a Hidden Number Problem (HNP) |
| 4 | Build a lattice and run LLL reduction to recover the private key |
| 5 | Forge a valid signature for the protected message |
| 6 | Submit to `/verify` and collect the flag |

## Flag Format

```
P2P{flag_content}
```

## Requirements

```
ecdsa
fpylll
requests
```
