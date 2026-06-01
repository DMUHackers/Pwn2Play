# Solve Guide: Ghost Protocol 👻

## Flag
`P2P{n0_m0r3_sh4d0ws_1n_th3_m4ch1n3}`

---

## Overview

`ghost_protocol` is a MIPS 32-bit ELF binary that embeds a custom virtual machine called **SpecterVM**. The flag is never stored in plaintext — instead, the binary encrypts the bytecode, obfuscates operands, and validates input character-by-character through a chained transformation. The solve is entirely static: no binary execution required.

---

## Step 1 — Identify the SpecterVM Architecture

Load the binary in Ghidra or IDA. You'll find a VM dispatch loop (a `switch`/jump table) with **21 opcodes**. Key opcodes to identify:

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| `0x01` | `MOV_IMM` | Load immediate into register |
| `0x02` | `XOR` | XOR two registers |
| `0x03` | `ROL` | Rotate register left |
| `0x04` | `ADD` | Add registers (mod 256) |
| `0x0A` | `CMP` | Compare two registers — **this is where expected values live** |
| `0x0B` | `JNE` | Jump if not equal (fail path) |

The VM operates on 8-bit registers and processes one input character per loop iteration.

---

## Step 2 — Decrypt the Bytecode

The bytecode stored in the binary is encrypted with **two layers**:

### Layer 1 — Static XOR key `0xA7`
Every opcode byte is XORed with `0xA7` at build time.

### Layer 2 — ELF header-derived key
At runtime, the binary computes a key from the first 64 bytes of the ELF header:

```python
elf_key = 0
for i, b in enumerate(elf_header[:64]):
    elf_key ^= b
    elf_key = rotl8(elf_key, 1)
```

Apply both layers to recover the raw opcodes:
```python
decrypted_opcode = (raw_byte ^ 0xA7) ^ elf_key
```

---

## Step 3 — Deobfuscate Operands

Operands (register numbers and immediate values) are obfuscated separately from opcodes using a **position-based XOR** with seed `0x3C`:

```python
deobfuscated_operand = raw_operand ^ (position ^ 0x3C)
```

where `position` is the byte offset of the operand within the bytecode stream.

---

## Step 4 — Disassemble and Extract Expected Values

After decryption and deobfuscation, disassemble the VM program. For each of the 30 characters, the bytecode follows this pattern:

```
MOV_IMM  r1, <expected_value>   ; load the target transformed byte
CMP      r0, r1                 ; compare transformed input vs expected
JNE      <fail_addr>            ; bail out if wrong
```

Extract each `<expected_value>` from the `MOV_IMM` before every `CMP`. This gives you 30 expected bytes:

```
[0xa0, 0xbe, 0x44, 0x79, 0x44, 0x22, 0xf3, 0x3a, 0x1b, 0x4d,
 0x41, 0xaf, 0x60, 0x4e, 0x0b, 0x70, 0x7d, 0xd6, 0xcc, 0x2c,
 0x86, 0xac, 0x50, 0x31, 0x23, 0x94, 0x34, 0xce, 0x12, 0x31]
```

---

## Step 5 — Understand the Forward Transformation

From disassembly, the VM applies this to each input character `c[i]`:

```
v = c[i]
v ^= xor_key[i]          # position-derived XOR
v ^= chain               # running chain value
v = ROL(v, i % 7)        # rotate left by position mod 7
v = (v + add_key[i]) & 0xFF   # add key mod 256
expected[i] = v

# Update chain for next character
chain = expected[i] ^ ROL(chain, 1)
```

Where the key derivation formulas (extracted from the key-generation bytecode block) are:

```python
xor_key[i] = ((i * 37 + 13) ^ ((i * i + 7) & 0xFF)) & 0xFF
add_key[i] = ((i * 53 + 97) ^ ((i * 17 + 3) & 0xFF)) & 0xFF
chain_seed  = 0x5A   # initial chain value
```

---

## Step 6 — Reverse the Transformation

Invert each operation in reverse order to recover the original input:

```python
def rotr8(val, count):
    count %= 8
    return ((val >> count) | (val << (8 - count))) & 0xFF

def rotl8(val, count):
    count %= 8
    return ((val << count) | (val >> (8 - count))) & 0xFF

chain = 0x5A
flag  = ""

for i in range(30):
    v = expected[i]
    v = (v - add_key[i]) & 0xFF   # reverse ADD
    v = rotr8(v, i % 7)           # reverse ROL
    v ^= chain                    # reverse chain XOR
    v ^= xor_key[i]               # reverse position XOR
    flag += chr(v)
    chain = expected[i] ^ rotl8(chain, 1)   # advance chain (same as forward)

print(f"P2P{{{flag}}}")
# P2P{n0_m0r3_sh4d0ws_1n_th3_m4ch1n3}
```

---

## Full Standalone Solve Script

```python
#!/usr/bin/env python3

def rotl8(val, count):
    count %= 8
    return ((val << count) | (val >> (8 - count))) & 0xFF

def rotr8(val, count):
    count %= 8
    return ((val >> count) | (val << (8 - count))) & 0xFF

flag_len   = 30
chain_seed = 0x5A

xor_keys = [((i * 37 + 13) ^ ((i * i + 7) & 0xFF)) & 0xFF for i in range(flag_len)]
add_keys = [((i * 53 + 97) ^ ((i * 17 + 3) & 0xFF)) & 0xFF for i in range(flag_len)]

# Expected values extracted from CMP instructions after full bytecode decryption
expected = [
    0xa0, 0xbe, 0x44, 0x79, 0x44, 0x22, 0xf3, 0x3a, 0x1b, 0x4d,
    0x41, 0xaf, 0x60, 0x4e, 0x0b, 0x70, 0x7d, 0xd6, 0xcc, 0x2c,
    0x86, 0xac, 0x50, 0x31, 0x23, 0x94, 0x34, 0xce, 0x12, 0x31
]

chain = chain_seed
flag  = ""

for i in range(flag_len):
    v = expected[i]
    v = (v - add_keys[i]) & 0xFF
    v = rotr8(v, i % 7)
    v ^= chain
    v ^= xor_keys[i]
    flag += chr(v)
    chain = expected[i] ^ rotl8(chain, 1)

print(f"P2P{{{flag}}}")
```

---

## Key Techniques

| Technique | Detail |
|-----------|--------|
| Custom VM reversing | Identify dispatch loop, map 21 opcodes, trace execution flow |
| Dual-layer XOR decryption | Static key `0xA7` + runtime ELF header-derived key |
| Operand deobfuscation | Position XOR with seed `0x3C` on every operand byte |
| Chained transformation reversal | Walk backwards through XOR → ROTR → XOR chain → XOR key |
| Static-only solve | No binary execution needed once transformation is understood |
