# Solve Guide: Layers 🧅

## Flag
`P2P{l4y3r5_up0n_l4y3r5s!}`

---

## Overview

The challenge is aptly named. Four distinct layers of obfuscation stand between you and the flag: a deceptive outer binary full of red herrings, an XOR-encrypted embedded ELF, a second binary with its own distractions, and a final multi-step decode chain that produces the flag.

---

## Layer 1 — The Outer Binary

### Initial Triage

```bash
file challenge
# ELF 64-bit LSB pie executable, x86-64, not stripped

nm challenge | grep ' T '
```

Key symbols:
| Symbol | Purpose |
|--------|---------|
| `anti_debug` | ptrace-based debugger detection — will kill the process |
| `fake_flag_check` | Validates nothing real; returns fake results |
| `fake_crypto` | Confusing crypto-looking operations; irrelevant |
| `string_obfuscation` | Builds decoy strings at runtime |
| `xor_decrypt` | **The real work** — decrypts the embedded payload |
| `main` | Calls anti_debug, then xor_decrypt, then munmaps and exits |

### Fake Flags

`strings challenge` reveals several red herrings deliberately placed to waste time:

```
P2P{fake...}
P2P{deco...}
P2P{hidd...}
P2P{this...}
```

None of these are the real flag. Ignore them.

### Anti-Debug Bypass

The `anti_debug` function calls `ptrace(PTRACE_TRACEME, 0, 0, 0)`. If a debugger is already attached, this returns -1 and the binary exits.

Bypass options:
- Patch the `ptrace` call to `NOP` in the binary
- Use `LD_PRELOAD` to hook and spoof `ptrace`
- Skip the check entirely — the flag can be recovered statically

---

## Layer 2 — Extracting the Encrypted Shellcode

`main` decrypts the `.data` section payload using `xor_decrypt` into an `mmap`'d RWX region, then immediately `munmap`s it and exits — **it never executes the decrypted code**. The decryption happens in memory only.

### Key Parameters (from binary)

```
Symbol: encrypted_shellcode       → offset 0x4020 in binary
Symbol: encrypted_shellcode_len   → 16592 bytes (0x40D0)
Symbol: xor_key                   → b'\xab\xcd\xef\x124Vx\x90'  (8 bytes)
```

### Decryption

The `xor_decrypt` function applies the 8-byte key cyclically:

```python
import struct

with open('challenge', 'rb') as f:
    data = f.read()

# Extract from .data section (file offset 0x3000 = section start, shellcode at +0x1020)
enc_offset = 0x3020          # file offset of encrypted_shellcode
enc_len    = 16592
key        = b'\xab\xcd\xef\x124Vx\x90'

enc = bytearray(data[enc_offset : enc_offset + enc_len])
dec = bytearray(enc[i] ^ key[i % 8] for i in range(enc_len))

with open('stage2', 'wb') as f:
    f.write(dec)
```

The decrypted blob is a valid ELF binary.

---

## Layer 3 — The Stage 2 Binary

```bash
file stage2
# ELF 64-bit LSB pie executable, x86-64, dynamically linked, not stripped

nm stage2 | grep ' T '
```

Key symbols:
| Symbol | Purpose |
|--------|---------|
| `junk_function` | Dead code — ignore |
| `fake_algorithm` | Red herring crypto — ignore |
| `fake_validation_routine` | Always returns false — ignore |
| `confusing_function` | Obfuscated no-op — ignore |
| `simple_decode` | **Real decode step** |
| `construct_flag` | **Assembles the flag from encoded chunks** |
| `validate_flag` | Calls construct_flag and checks the result |

---

## Layer 4 — Flag Reconstruction

### `construct_flag` Overview

Disassembling `construct_flag` reveals three hardcoded encoded chunks stored in the binary. Each is passed through `simple_decode`, then a final XOR pass produces the flag.

### `simple_decode` Transform

```
for each byte b:
    b = b ^ 0x55
    b = b - 5
```

### Final Pass

After all three chunks are decoded, a second XOR with `0x22` is applied to every byte.

### Full Decode

```python
def simple_decode(data):
    return bytes((b ^ 0x55) - 5 & 0xFF for b in data)

def final_pass(data):
    return bytes(b ^ 0x22 for b in data)

# Encoded chunks extracted from construct_flag disassembly
chunk1_enc = bytes([0x27, 0x45, 0x27, 0x0c, 0x1b, 0x43, 0x0e, 0x44, 0x05, 0x42])
chunk2_enc = bytes([0x4f, 0x4e, 0x06, 0x12, 0x13, 0x53, 0x09, 0x45, 0x53, 0x49, 0x13])
chunk3_enc = bytes([0x4f, 0x4e, 0x4e, 0x07, 0x14, 0x42])

decoded  = simple_decode(chunk1_enc + chunk2_enc + chunk3_enc)
flag_raw = final_pass(decoded)

print(flag_raw.decode())
# P2P{l4y3r5_up0n_l4y3r5s!}
```

---

## Summary of Layers

| Layer | What it is | How to get through |
|-------|-----------|-------------------|
| 1 | Outer ELF with fake flags, anti-debug, distraction functions | Identify `xor_decrypt` as the only meaningful function; bypass ptrace check |
| 2 | XOR-encrypted blob in `.data` | Extract `encrypted_shellcode`, key `\xab\xcd\xef\x124Vx\x90`, decrypt offline |
| 3 | Stage 2 ELF with its own distractions | Identify `construct_flag` and `simple_decode` as the only real functions |
| 4 | Three encoded flag chunks with two-pass decode | XOR 0x55 → subtract 5 → XOR 0x22 → flag |

---

## Recommended Tools

- **Static**: `objdump`, `ghidra`, `nm`, `strings`, `readelf`
- **Dynamic**: `gdb` with ptrace bypass, `strace` (limited — binary exits early)
- **Scripting**: Python for offline decryption and flag reconstruction
