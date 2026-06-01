# Solve Guide: the fragmented reality 🏭

## Flag
`p2p{1a7f0e6e7d6b3c9b7e7a3f4c7d6b3c9b}`

---

## Overview

The challenge hides data inside **TCP Options** fields using NOP (`0x01`) bytes as carriers. The relevant packets originate from a fixed source port (`31337`) targeting `8888`, have **empty payloads**, and are deliberately sent **out of sequence order**. Reassembling them by TCP Sequence Number and decoding the embedded bytes recovers the flag.

---

## Step 1 — Filter the Relevant Packets

Open `industrial.pcap` in Wireshark or parse it with a script.

Apply the filter:
```
tcp.port == 8888
```

You'll find **31 packets** hitting port 8888. Most are noise from random source ports — the signal packets all originate from **source port `31337`** (a classic leet-speak indicator). Filter further to:
```
tcp.srcport == 31337 && tcp.dstport == 8888
```
This gives **19 packets** with Sequence Numbers `100, 200, 300, ... 1900`.

> All payloads are empty. The flag is not in the data section.

---

## Step 2 — Inspect the TCP Options Field

Each packet's TCP Options block (between the fixed 20-byte TCP header and the (absent) payload) looks like:

```
01 01 XX XX XX XX 01 01
```

- `01` = NOP option (kind=1, single byte, normally used as padding)
- The 4 middle bytes (`XX XX XX XX`) are **ASCII characters** representing a 4-character hex chunk

### Example (seq=100):
```
opts_hex = 0101373033320101
           ^^                = NOP
             ^^              = NOP
               37 30 33 32   = ASCII "7032"
                         ^^  = NOP
                           ^^= NOP
```

`"7032"` → this is 4 ASCII hex characters carrying one chunk of the flag.

---

## Step 3 — Extract and Sort All Chunks

Sort the 19 signal packets by their TCP Sequence Number (ascending) and extract the 4-byte middle section of each Options field:

| Seq  | opts_hex           | ASCII chunk |
|------|--------------------|-------------|
| 100  | `0101373033320101` | `7032`      |
| 200  | `0101373037620101` | `707b`      |
| 300  | `0101333136310101` | `3161`      |
| 400  | `0101333736360101` | `3766`      |
| 500  | `0101333036350101` | `306e` *(see note)* |
| 600  | `0101333636350101` | `366e`      |
| 700  | `0101333736340101` | `376e`      |
| ...  | ...                | ...         |
| 1900 | `0101376401010101` | `7d`        |

> **Note:** The last packet (seq=1900) only carries 2 meaningful bytes (`7d` = `}`), since the flag ends there.

---

## Step 4 — Concatenate and Decode

Join all chunks in sequence order:

```
7032707b31613766306536653764366233633962376537613366346337643662336339627d
```

This is a hex string. Decode it as ASCII:

```python
bytes.fromhex("7032707b31613766306536653764366233633962376537613366346337643662336339627d").decode()
# → p2p{1a7f0e6e7d6b3c9b7e7a3f4c7d6b3c9b}
```

The hidden data is the **ASCII representation of the flag**, itself encoded as hex — a double layer of obfuscation.

---

## Step 5 — Solve Script

```python
import struct

def parse_pcap(filename):
    with open(filename, 'rb') as f:
        magic = f.read(4)
        endian = '<' if magic == b'\xd4\xc3\xb2\xa1' else '>'
        f.read(20)  # skip global header remainder
        packets = []
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian+'IIII', hdr)
            packets.append(f.read(incl_len))
        return packets

packets = parse_pcap('industrial.pcap')
results = []

for data in packets:
    if len(data) < 14:
        continue
    if struct.unpack('>H', data[12:14])[0] != 0x0800:  # IPv4 only
        continue
    ip = data[14:]
    ihl = (ip[0] & 0xf) * 4
    if ip[9] != 6:  # TCP only
        continue
    tcp = ip[ihl:]
    src_port = struct.unpack('>H', tcp[0:2])[0]
    dst_port = struct.unpack('>H', tcp[2:4])[0]
    seq      = struct.unpack('>I', tcp[4:8])[0]
    data_offset = (tcp[12] >> 4) * 4

    # Only signal packets: 31337 -> 8888
    if src_port != 31337 or dst_port != 8888:
        continue

    opts = tcp[20:data_offset]
    # Extract ASCII hex chunk from bytes 2-6 (between NOP bookends)
    chunk = opts[2:6].decode('ascii', errors='ignore').rstrip('\x01')
    results.append((seq, chunk))

results.sort(key=lambda x: x[0])
flag_hex = ''.join(chunk for _, chunk in results)
flag = bytes.fromhex(flag_hex).decode('ascii')
print(flag)  # p2p{1a7f0e6e7d6b3c9b7e7a3f4c7d6b3c9b}
```

---

## Key Techniques

| Technique | Detail |
|-----------|--------|
| TCP Options abuse | NOP bytes (kind=1) repurposed to carry 4 ASCII hex chars per packet |
| Out-of-order transmission | Packets sent shuffled; must sort by TCP Sequence Number |
| Double encoding | Embedded bytes are ASCII hex of the flag string, not raw bytes |
| Source port as signal | Port `31337` (leet: "leet") distinguishes signal from noise packets |
