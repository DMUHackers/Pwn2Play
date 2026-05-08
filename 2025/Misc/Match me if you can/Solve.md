# Solve.md

# [Easy] Misc - Match me if you can - Solve Guide

## Overview

This challenge provides a regex string that directly describes the flag.

The regex uses a mixture of:

- Literal characters
- Character classes
- Non-capturing groups
- Hexadecimal ASCII escape sequences

The goal is to read the regex from left to right and convert each part into the character it matches.

## Initial Analysis

The regex begins with:
```
(?:\x50)(?:2)(?:\x50)(?:\x7b)
```
Decode the hexadecimal escape sequences:
```
\x50 = P
\x7b = {
```
This gives:
```
P2P{
```
So the regex begins with the expected flag format.

## Decoding the Regex

Continue reading each regex group from left to right.

For example:
```
(?:(?:[r]|r)) = r
(?:\x33) = 3
(?:[g]) = g
(?:\x33) = 3
(?:x) = x
(?:_|[\x5f]) = _
```
This gives:
```
r3g3x_
```
Continuing the same process across the full expression reveals the complete flag content.

## Useful Hex Values

The important hexadecimal escape values are:
```
\x50 = P
\x7b = {
\x33 = 3
\x5f = _
\x7d = }
```
## Manual Decoding

Regex:
```
(?:\x50)(?:2)(?:\x50)(?:\x7b)(?:(?:[r]|r))(?:\x33)(?:[g])(?:\x33)(?:x)(?:_|[\x5f])(?:(?:1)|(?:1))(?:(?:5))(?:_|[\x5f])(?:(?:4))(?:m)(?:4)(?:z)(?:1)(?:n)(?:g)(?:_|[\x5f])(?:b)(?:u)(?:7)(?:_|[\x5f])(?:4)(?:l)(?:5)(?:0)(?:_|[\x5f])(?:4)(?:w)(?:f)(?:u)(?:l)(?:\x7d)
```
Decoded:
```
P2P{r3g3x_15_4m4z1ng_bu7_4l50_4wful}
```
## Optional Solve Script

This challenge can be solved manually, but a small script can help decode the obvious hexadecimal escape sequences.
```python
import re

regex = r"(?:\x50)(?:2)(?:\x50)(?:\x7b)(?:(?:[r]|r))(?:\x33)(?:[g])(?:\x33)(?:x)(?:_|[\x5f])(?:(?:1)|(?:1))(?:(?:5))(?:_|[\x5f])(?:(?:4))(?:m)(?:4)(?:z)(?:1)(?:n)(?:g)(?:_|[\x5f])(?:b)(?:u)(?:7)(?:_|[\x5f])(?:4)(?:l)(?:5)(?:0)(?:_|[\x5f])(?:4)(?:w)(?:f)(?:u)(?:l)(?:\x7d)"
```
# One simple way is to manually simplify the regex after replacing hex escapes.
decoded_hex = regex.encode().decode("unicode_escape")
print(decoded_hex)

## Key Finding

The regular expression itself matches the flag exactly.

By simplifying the groups and decoding the hexadecimal ASCII values, the flag can be read directly.

## Flag
```
P2P{r3g3x_15_4m4z1ng_bu7_4l50_4wful}
```
## Lessons Learned

This challenge demonstrates that regex can be used to hide readable data through unnecessary complexity.

The important steps were:

1. Read the regex from left to right.
2. Decode hexadecimal ASCII escape sequences.
3. Simplify non-capturing groups and character classes.
4. Reconstruct the matched string.
5. Recover the flag.