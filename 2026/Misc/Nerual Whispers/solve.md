# Solve Guide: Nerual Whispers 🧠

## Flag
`P2P{wh1sp3rs_b3tw33n_th3_l1n3s}`

---

## Overview

`whispers.txt` is a Unicode steganography challenge. The essay looks visually identical to normal text, but certain characters have been silently replaced with **Cyrillic homoglyphs** — characters from the Cyrillic script that are visually indistinguishable from their Latin equivalents (e.g., Cyrillic `о` U+043E looks identical to Latin `o`). These substitutions encode a hidden binary message.

`selector.py` provides a **pre-trained neural classifier** that identifies which positions in the text are designated "carrier" positions — only those positions participate in encoding. At each carrier position, a homoglyph = bit `1`, a normal Latin character = bit `0`. Reading these bits MSB-first in groups of 8 gives ASCII bytes that spell the flag.

---

## Step 1 — Understand the `_NORM` Table in `selector.py`

The first clue is hiding in plain sight inside `selector.py`:

```python
_NORM = {
    '\u0430':'a', '\u0441':'c', '\u0435':'e', '\u043e':'o',
    '\u0440':'p', '\u0445':'x', '\u0443':'y', '\u0455':'s',
    '\u0456':'i', '\u0410':'A', '\u0412':'B', '\u0421':'C',
    '\u0415':'E', '\u041d':'H', '\u041a':'K', '\u041c':'M',
    '\u041e':'O', '\u0420':'P', '\u0422':'T', '\u0425':'X',
}
```

This maps 20 Cyrillic code points to their visually identical Latin equivalents. This is the homoglyph alphabet used for encoding. Open `whispers.txt` in a hex editor or run `unicodedata` on it — you'll find these Cyrillic characters scattered throughout what appears to be Latin text.

---

## Step 2 — Understand the Classifier

`selector.py` exports `model.classify(text, position) -> bool`. It's a two-layer neural network:

```
Input (5 features) -> Dense(5->8, tanh) -> Dense(8->1, sigmoid) -> threshold 0.5
```

The features are derived by hashing the **position index + the normalized 9-character context window** around that position using SHA-256. This makes the carrier selection deterministic and position-dependent, but not guessable without the model weights.

The key insight: **not every character in the text carries data**. The classifier acts as a steganographic key — only positions where `classify()` returns `True` AND the normalized character has a homoglyph equivalent are "usable carriers".

---

## Step 3 — Identify Usable Carrier Positions

```python
from selector import model, _NORM

with open('whispers.txt', 'r', encoding='utf-8') as f:
    text = f.read()

homoglyphs  = set(_NORM.keys())    # Cyrillic chars used as substitutes
homo_targets = set(_NORM.values()) # Latin chars that can be substituted

norm_text = model._normalize(text)  # Replace all Cyrillic -> Latin
carriers = []

for pos in range(len(text)):
    if model.classify(text, pos):                    # Neural net says: carrier?
        if norm_text[pos] in homo_targets:           # Can this char carry a bit?
            carriers.append(pos)

# Result: 807 usable carrier positions
```

---

## Step 4 — Extract the Bits

At each carrier position, check whether the **actual character** in `whispers.txt` is a Cyrillic homoglyph (bit = `1`) or the ordinary Latin character (bit = `0`):

```python
bits = []
for pos in carriers:
    ch = text[pos]
    bits.append(1 if ch in homoglyphs else 0)
```

---

## Step 5 — Decode Bits to ASCII

Group bits in sets of 8, MSB-first, and convert to ASCII:

```python
flag_chars = []
for i in range(0, len(bits), 8):
    byte = 0
    for j in range(8):
        byte = (byte << 1) | bits[i + j]
    if 0x20 <= byte <= 0x7e:
        flag_chars.append(chr(byte))
    else:
        break  # non-printable signals end of message

flag = ''.join(flag_chars)
# P2P{wh1sp3rs_b3tw33n_th3_l1n3s}
```

---

## Full Solve Script

```python
#!/usr/bin/env python3
from selector import model, _NORM

with open('whispers.txt', 'r', encoding='utf-8') as f:
    text = f.read()

homoglyphs   = set(_NORM.keys())
homo_targets = set(_NORM.values())
norm_text    = model._normalize(text)

carriers = [
    pos for pos in range(len(text))
    if model.classify(text, pos) and norm_text[pos] in homo_targets
]

bits = [1 if text[pos] in homoglyphs else 0 for pos in carriers]

chars = []
for i in range(0, len(bits) - 7, 8):
    byte = int(''.join(str(b) for b in bits[i:i+8]), 2)
    if 0x20 <= byte <= 0x7e:
        chars.append(chr(byte))

candidate = ''.join(chars)
# Scan for P2P{...} boundary
start = candidate.find('P2P{')
end   = candidate.find('}', start) + 1
print(candidate[start:end])
```

---

## Key Techniques

| Technique | Detail |
|-----------|--------|
| Unicode homoglyph steganography | Cyrillic chars (e.g. U+043E `о`) replace visually identical Latin chars (`o`) to encode bits |
| Neural carrier selection | A pre-trained 2-layer network selects which positions carry data, acting as a stego key |
| Binary encoding | Homoglyph present = `1`, Latin original = `0`; 8 bits per character, MSB-first |
| Cover text | A thematically on-brand AI essay provides plausible deniability for the substitutions |
| Detection hint | The `_NORM` table in `selector.py` directly lists every homoglyph pair used |
