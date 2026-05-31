# [Trivial] Forensics - The Hello Packet - Solve Guide

## Overview
The provided PCAP contains a single crafted UDP packet. The flag is embedded in plaintext directly within the UDP payload — no encoding, encryption, or steganography is involved. Opening the file in any packet analysis tool and inspecting the payload is sufficient to retrieve the flag.

## Initial Analysis
The file is only 157 bytes total. Breaking that down:
- 24 bytes — PCAP global header
- 16 bytes — packet record header
- 117 bytes — actual packet data

A file this small contains a single packet, almost certainly hand-crafted rather than captured from real traffic. The challenge description's use of "Heartbeat" and "suspicious device" frames the packet as deliberate rather than organic.

## Enumeration / Inspection

The packet structure is as follows:

| Layer    | Details                                              |
|----------|------------------------------------------------------|
| Ethernet | `aa:bb:cc:dd:ee:ff` → `de:ad:be:ef:00:01`           |
| IPv4     | `10.0.0.66` → `10.0.0.1`, TTL=64, ID=0x1234         |
| UDP      | Src Port: 31337, Dst Port: 8080, Length: 83 bytes    |
| Payload  | 75 bytes of plaintext ASCII                          |

Notable markers confirming this is a crafted packet:
- **Source port 31337** — "leet" / "eleet", a classic CTF marker
- **Destination MAC `de:ad:be:ef:00:01`** — spells "DEADBEEF", another common marker
- **UDP checksum is zeroed (0x0000)** — typical of Scapy-crafted packets where checksum calculation is skipped
- **`scapy_rookie` tag in payload** — confirms the packet was built with Python's Scapy library

## Method
- **Technique:** Open PCAP, read payload — no transformation required
- **Encoding:** None; flag is plaintext ASCII in the UDP payload

## Exploitation / Decryption / Solution Steps

### Step 1 — Open the capture

**Option A — Wireshark (GUI):**
1. Open `heartbeat.pcap` in Wireshark
2. Click the single packet in the packet list
3. Expand `Data` in the packet details pane, or view the packet bytes pane at the bottom
4. The payload is visible in plaintext — read the flag directly

**Option B — tshark (CLI):**
```bash
tshark -r heartbeat.pcap -V
```
Full protocol dissection prints all layers including the decoded payload.

**Option C — strings (quickest):**
```bash
strings heartbeat.pcap
```
Since the flag is plaintext ASCII inside a binary file, `strings` extracts it instantly without needing a packet analysis tool.

### Step 2 — Read the payload

The UDP payload decodes to:
```
Heartbeat Check: scapy_rookie | Flag: p2p{7f7e91d04461176b6b7f329249767732}
```

Note the flag is in lowercase — normalise to the competition standard format.

**Flag:** `P2P{7f7e91d04461176b6b7f329249767732}`

## Commands Used

```bash
# Full packet dissection
tshark -r heartbeat.pcap -V

# Quickest extraction — strings over binary
strings heartbeat.pcap

# Show only the payload data field
tshark -r heartbeat.pcap -T fields -e data.text
```

## Scripts Used
None — no scripting required for this challenge.
