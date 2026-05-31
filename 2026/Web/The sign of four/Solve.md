# Solve.md

# [Varied] Web - The Sign of Four - Solve Guide

## Overview

The Sign of Four is a four-part web challenge where each stage hides a separate flag in a different part of the application.

The challenge is designed to be solved manually using:

```text
- Browser navigation
- robots.txt inspection
- Browser Developer Tools
- Console inspection
- Interaction with the terminal-style feature
- JavaScript source review
- Basic XOR decoding
```

Automated scanning, brute-forcing, fuzzing, or disruptive testing is not required. The full challenge can be solved through normal browser interaction and source code inspection.

The four flags are:

```text
The Sign of Four (I)   : P2P{St0p_L00K1nG_W31Rdo}
The Sign of Four (II)  : P2P{y0u_f0und_th3_c0ns0le}
The Sign of Four (III) : P2P{cmd_1nj3ct10n_ftw}
The Sign of Four (IV)  : P2P{gh0st_1n_th3_c1rcu1t}
```

## Solve Walkthrough

### Part I - robots.txt

The first stage can be found through basic web enumeration.

Navigate to the challenge site and check:

```text
/robots.txt
```

For example:

```text
https://challenge-site/robots.txt
```

The `robots.txt` file contains the first flag.

Recovered flag:

```text
P2P{St0p_L00K1nG_W31Rdo}
```

### Part II - Browser Console

The second stage is hidden in the browser console.

Open Developer Tools using one of the following:

```text
F12
Ctrl + Shift + I
Right click -> Inspect
```

Then open the Console tab.

The second flag is printed in the console output.

Recovered flag:

```text
P2P{y0u_f0und_th3_c0ns0le}
```

### Part III - Terminal Command Chaining

The third stage is hidden in the terminal-style feature on the main page.

Locate the terminal component in the hero section and interact with it normally first. The terminal appears to expect a specific input, but it does not safely restrict the command being passed through.

This allows command chaining using a shell separator such as:

```text
&&
```

The intended payload is:

```bash
ls && cat flag.txt
```

This chains a second command onto the expected terminal behaviour and reads the flag file.

Recovered flag:

```text
P2P{cmd_1nj3ct10n_ftw}
```

### Part IV - JavaScript XOR Decoding

The final stage is hidden inside the loaded JavaScript source.

Open Developer Tools and inspect the source files:

```text
Developer Tools -> Sources
```

Look for:

```text
main.js
```

Inside `main.js`, there is a section labelled as phase calibration data:

```javascript
// Phase calibration seeds - do not modify
const _pcS = [0x12,0x70,0x12,0x39,0x25,0x2a,0x72,0x31,0x36,0x1d,0x73,0x2c,0x1d,0x36,0x2a,0x71,0x1d,0x21,0x73,0x30,0x21,0x37,0x73,0x36,0x3f];
const _pcK = 0x42;
```

The variable `_pcS` contains the encoded bytes, and `_pcK` contains the XOR key.

To decode the final flag, XOR each byte in `_pcS` with `_pcK`.

Example Python helper:

```python
#!/usr/bin/env python3

data = [
    0x12, 0x70, 0x12, 0x39, 0x25,
    0x2a, 0x72, 0x31, 0x36, 0x1d,
    0x73, 0x2c, 0x1d, 0x36, 0x2a,
    0x71, 0x1d, 0x21, 0x73, 0x30,
    0x21, 0x37, 0x73, 0x36, 0x3f
]

key = 0x42

decoded = ''.join(chr(byte ^ key) for byte in data)

print(decoded)
```

Expected output:

```text
P2P{gh0st_1n_th3_c1rcu1t}
```

Recovered flag:

```text
P2P{gh0st_1n_th3_c1rcu1t}
```

## Commands and Checks Used

Check `robots.txt`:

```text
https://challenge-site/robots.txt
```

Open Developer Tools:

```text
F12
Ctrl + Shift + I
Right click -> Inspect
```

Inspect JavaScript source:

```text
Developer Tools -> Sources -> main.js
```

Useful searches inside the source:

```text
Ctrl + F -> calibration
Ctrl + F -> _pcS
Ctrl + F -> _pcK
Ctrl + F -> xor
```

Terminal command used for Part III:

```bash
ls && cat flag.txt
```

Python helper used for Part IV:

```bash
python3 solve_xor.py
```

## Final Answers

```text
The Sign of Four (I)   : P2P{St0p_L00K1nG_W31Rdo}
The Sign of Four (II)  : P2P{y0u_f0und_th3_c0ns0le}
The Sign of Four (III) : P2P{cmd_1nj3ct10n_ftw}
The Sign of Four (IV)  : P2P{gh0st_1n_th3_c1rcu1t}
```