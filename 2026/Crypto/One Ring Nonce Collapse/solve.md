# Solve Guide: One Ring Nonce Collapse 💍

## Flag
`P2P{0n3_r1ng_n0nc3_70_ru13_7h3_curv3}`

---

## Overview

The server signs messages using ECDSA on secp256k1, but leaks `nonce_msb` — the top bits of the ephemeral nonce `k` — with every signature. With only 20 bits of `k` unknown, this creates a **Hidden Number Problem (HNP)** that can be solved with a lattice reduction (LLL algorithm) to recover the private key. Once the key is known, a forged signature for the protected message claims the flag.

---

## Step 1 — Understand the Vulnerability

### ECDSA Signing

Each ECDSA signature uses a secret ephemeral nonce `k`:

```
r = (k · G).x  mod  n
s = k⁻¹ · (h + r·d)  mod  n
```

where `d` is the private key and `h = SHA256(message)`.

If `k` is fully known, the private key can be recovered trivially:

```
d = r⁻¹ · (s·k − h)  mod  n
```

### The Leak

The server returns `nonce_msb` with every signature:

```python
nonce_msb = k >> UNKNOWN_BITS          # top (256-20) bits of k — known
nonce_low  = secrets.randbits(20)      # bottom 20 bits — unknown
k = (nonce_msb << 20) | nonce_low
```

So:

```
k = nonce_msb × 2²⁰ + j,   j ∈ [0, 2²⁰)
```

Only **20 bits** are hidden. This turns the problem into the **Hidden Number Problem**.

---

## Step 2 — Formulate as HNP

From the ECDSA equation:

```
s = k⁻¹(h + r·d)  mod  n
⟹  k = s⁻¹(h + r·d)  mod  n
```

Substituting `k = msb × 2²⁰ + j`:

```
j ≡ s⁻¹·r·d + s⁻¹·h − msb·2²⁰   (mod n)
```

Setting `aᵢ = s⁻¹·r mod n` and `bᵢ = s⁻¹·h − msb·2²⁰ mod n`:

```
j ≡ aᵢ·d + bᵢ   (mod n)
```

with the constraint that `j` is **small** (< 2²⁰). This is exactly the HNP: finding the secret `d` such that `aᵢ·d + bᵢ` is small mod `n` for many `i`.

---

## Step 3 — Build the Lattice

Collect `m` signatures (42 is sufficient for 20 unknown bits). Construct a lattice of dimension `m + 2`:

```
Matrix structure (rows correspond to equations):

For i in 0..m-1:
  row i:    [ n·n at col i, 0 elsewhere ]

Row m:      [ a₀·n, a₁·n, ..., a_{m-1}·n,  2²⁰,        0     ]
Row m+1:    [ t₀·n, t₁·n, ..., t_{m-1}·n,   0,    2²⁰·n ]

where tᵢ = bᵢ − 2¹⁹ (shift to centre the residues)
```

The target vector `[j₀, j₁, ..., j_{m-1}, d, 1]` (scaled) is short and lies in the lattice. LLL reduction will find it.

```python
from fpylll import IntegerMatrix, LLL

x_bound = 1 << unknown_bits  # 2^20

dim = len(sigs) + 2
matrix = [[0] * dim for _ in range(dim)]

for i, sig in enumerate(sigs):
    inv_s = pow(sig['s'], -1, n)
    a_i = (inv_s * sig['r']) % n
    b_i = (inv_s * sig['h'] - x_bound * sig['nonce_msb']) % n

    matrix[i][i] = n * n
    matrix[-2][i] = a_i * n
    matrix[-1][i] = (b_i - x_bound // 2) * n

matrix[-2][-2] = x_bound
matrix[-1][-1] = x_bound * n

basis = IntegerMatrix.from_matrix(matrix)
LLL.reduction(basis)
```

---

## Step 4 — Extract the Private Key

After LLL, scan the reduced basis rows for the key. The target row satisfies:

- `row[-1] == ± x_bound * n`  (the scaling factor on `d`)
- `row[-2] % x_bound == 0`   (the `d` entry is divisible by `x_bound`)

```python
for row_idx in range(dim):
    vec = [basis[row_idx, j] for j in range(dim)]
    for sign in (1, -1):
        v = [sign * x for x in vec]
        if v[-1] != x_bound * n:
            continue
        if v[-2] % x_bound != 0:
            continue
        d_candidate = (v[-2] // x_bound) % n
        # Verify against the public key
        if d_candidate * G == PUBLIC_KEY:
            print(f"Private key recovered: {d_candidate}")
```

---

## Step 5 — Forge and Submit

With `d` in hand, produce a valid signature for `"one ring to rule them all"` using any random nonce (the server has no nonce-reuse protection on `/verify`):

```python
import random

def forge_signature(message, d, n, G):
    h_msg = sha256_int(message)
    while True:
        k = random.randrange(1, n)
        r = int((k * G).x()) % n
        if r == 0:
            continue
        s = pow(k, -1, n) * (h_msg + d * r) % n
        if s != 0:
            return r, s

r, s = forge_signature("one ring to rule them all", d, n, G)
```

POST to `/verify`:

```json
{ "r": "<r>", "s": "<s>" }
```

Response:

```json
{ "status": "accepted", "flag": "P2P{0n3_r1ng_n0nc3_70_ru13_7h3_curv3}" }
```

---

## Full Exploit

```bash
pip install ecdsa fpylll requests
python3 exploit.py --url http://localhost:5000
```

The provided `exploit.py` implements all steps above end-to-end.

---

## Why 42 Signatures?

The lattice attack on ECDSA with `b` unknown bits requires roughly `m ≥ b / log₂(n/m)` equations for stable recovery. For `b = 20` and `n ≈ 2²⁵⁶`, about 40+ signatures is a comfortable margin. Using fewer risks the target vector not being the shortest in the reduced basis.

---

## Key Techniques

| Technique | Detail |
|-----------|--------|
| ECDSA partial nonce leakage | Leaking `nonce_msb` constrains `k` to a narrow band — only 2²⁰ values |
| Hidden Number Problem (HNP) | Reformulate the ECDSA equations so `d` appears as a short secret |
| LLL lattice reduction | Finds the short vector `[j₀, ..., j_{m-1}, d, 1]` in polynomial time |
| Signature forgery | Once `d` is known, producing a valid signature is trivial |

## Real-World Relevance

- **PlayStation 3** (2010): Sony used a constant `k`, making `d` recoverable from two signatures
- **Bitcoin wallet drains**: Wallets with reused nonces have been drained on-chain
- **Biased nonce lattice attacks**: Even a few bits of bias enable HNP attacks with far fewer signatures than shown here
- **Mitigation**: Use RFC 6979 deterministic nonce derivation; never expose any part of `k`
