# Solve.md

# [Medium] Rev - PDFProblems - Solve Guide

## Overview

This challenge revolves around reversing a malicious-style PDF document containing embedded JavaScript. The JavaScript is hidden within PDF objects, obfuscated using a JavaScript obfuscator and then encoded using JSFuck.

The goal is to extract the JavaScript, decode it, identify the hidden payload and recover the flag.

Flag:
`P2P{pdf5_c4n_c0n741n_j4v45cr1p7}`

---

## Initial Analysis

Opening the PDF normally does not immediately reveal anything suspicious. However, inspecting the PDF structure shows embedded JavaScript objects.

The challenge hint suggests:
1. The PDF contains a clue
2. JavaScript extraction is required
3. The code is heavily obfuscated

The PDF also contains compressed `FlateDecode` streams which store the majority of the document contents.

---

## Enumeration / Inspection

First inspect the PDF metadata and objects:

```bash
pdfinfo DMUHackers_2025_Fiscal_Report.pdf
```

Then inspect the raw PDF contents:

```bash
strings DMUHackers_2025_Fiscal_Report.pdf
```

or:

```bash
pdf-parser.py DMUHackers_2025_Fiscal_Report.pdf
```

Look for:

- `/JavaScript`
- `/JS`
- `FlateDecode`
- suspicious object references

Extract the JavaScript object from the PDF.

The extracted JavaScript appears as a massive block of symbols such as:

```js
[]!+[]+!![]...
```

This identifies the encoding as **JSFuck**.

---

## Method

### Step 1 — Decode JSFuck

Use an online JSFuck decoder such as:

- https://www.dcode.fr/jsfuck-language
- https://www.dcode.fr/javascript-deobfuscator

After decoding, readable JavaScript is revealed.

---

### Step 2 — Deobfuscate the JavaScript

The decoded JavaScript is still obfuscated using a standard JavaScript obfuscator.

Optional tools:

- JSNice
- de4js
- Prettier / Beautifier

Beautifying the script reveals a `fetch()` call and encoded data.

---

### Step 3 — Identify the Encoded Payload

The JavaScript contains a hidden encoded string.

The PDF hint suggests focusing on the `fetch()` section.

The encoded string is encrypted using:

1. Atbash cipher
2. Base64 encoding

---

### Step 4 — Decode the Payload

Use CyberChef:

Recipe:

1. Apply **Atbash Cipher**
2. Apply **From Base64**

This reveals the flag:

```text
P2P{pdf5_c4n_c0n741n_j4v45cr1p7}
```

---

## Exploitation / Decryption / Solution Steps

1. Open the PDF and inspect for hints
2. Extract embedded JavaScript from the PDF
3. Identify the JSFuck encoded payload
4. Decode the JSFuck
5. Deobfuscate the returned JavaScript
6. Locate the `fetch()` section
7. Extract the encoded payload
8. Decode using Atbash
9. Decode resulting Base64
10. Recover the flag

---

## Commands Used

```bash
pdfinfo DMUHackers_2025_Fiscal_Report.pdf
strings DMUHackers_2025_Fiscal_Report.pdf
pdf-parser.py DMUHackers_2025_Fiscal_Report.pdf
```

---

## Scripts Used

No custom scripts were required.

Online tools used:

- JSFuck decoder
- JavaScript deobfuscator
- CyberChef