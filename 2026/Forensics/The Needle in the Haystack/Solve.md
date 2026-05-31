# [Easy] Forensics - The Needle in the Haystack - Solve Guide

## Overview
A packet capture contains a mix of ICMP Echo Request packets. An attacker has exfiltrated a secret key by hiding one byte of data per packet across a subset of packets that share a specific IP TTL value. All other packets are decoys. The solution requires filtering by TTL, extracting the first byte of each matching packet's raw payload, and concatenating them to form the flag.

## Initial Analysis
The challenge description states the data is hidden in ICMP packets sharing "the same TTL" and that all other packets are noise. This is a classic covert channel technique — using a non-obvious field (TTL) as a selector to distinguish real data from decoys, making automated detection harder.

The two key observations are:
- **Filter:** `IP.ttl == 42` isolates the relevant packets
- **Extraction:** The first byte of each packet's raw ICMP payload contributes one character of the flag

## Enumeration / Inspection

Open the capture in Wireshark and apply a display filter to get a first look:

```
icmp && ip.ttl == 42
```

This immediately reduces the traffic to only the packets carrying hidden data. Inspect the payload of a few packets to confirm that the first byte of each forms a printable ASCII character.

Alternatively, use `tshark` to list matching packets from the command line:

```bash
tshark -r exfil.pcap -Y "icmp && ip.ttl == 42" -T fields -e data
```

## Method
- **Technique:** Covert channel analysis — TTL-based packet filtering to isolate hidden data, followed by single-byte payload extraction and concatenation
- **Tools:** Wireshark / `tshark` for inspection; Python `scapy` for automated extraction

## Exploitation / Decryption / Solution Steps

### Step 1 — Open the capture and filter by TTL

**In Wireshark:**

1. Open `exfil.pcap`
2. Apply the display filter: `icmp && ip.ttl == 42`
3. Browse the filtered packets and inspect the `Data` field in the packet bytes pane — the first byte of each payload is the hidden character

**With tshark:**
```bash
tshark -r exfil.pcap -Y "icmp && ip.ttl == 42" -T fields -e data
```

Each line of output is the hex-encoded payload of one matching packet.

### Step 2 — Extract and concatenate the first byte of each payload

**Python with Scapy (recommended — fully automated):**

```python
from scapy.all import rdpcap, ICMP, IP, Raw

packets = rdpcap("exfil.pcap")

flag_bytes = []
for pkt in packets:
    if IP in pkt and ICMP in pkt and pkt[IP].ttl == 42:
        if Raw in pkt:
            flag_bytes.append(pkt[Raw].load[0])

flag = bytes(flag_bytes).decode()
print("Flag:", flag)
```

### Step 3 — Read the flag

The concatenated bytes spell out the flag directly.

**Flag:** `P2P{5a8c4f7a26f39e3c9888d3615e9e038d}`

## Commands Used

```bash
# Inspect matching packets with tshark
tshark -r exfil.pcap -Y "icmp && ip.ttl == 42" -T fields -e data

# Run the automated extraction script
pip install scapy
python3 solve.py
```

## Scripts Used

```python
# solve.py — extract flag from ICMP packets with TTL == 42
from scapy.all import rdpcap, ICMP, IP, Raw

packets = rdpcap("exfil.pcap")

flag_bytes = []
for pkt in packets:
    if IP in pkt and ICMP in pkt and pkt[IP].ttl == 42:
        if Raw in pkt:
            flag_bytes.append(pkt[Raw].load[0])

flag = bytes(flag_bytes).decode()
print("Flag:", flag)
```
