# [Trivial] Forensics - The Hello Packet

## Category
Forensics / Network Analysis

## Difficulty
Trivial

## Author
x41x41x41 | JohnOP

## Description
A suspicious device on the network sent a single "Heartbeat" packet. We captured it in a file named `heartbeat.pcap`. Find the hidden message inside the packet's payload to get the flag.

## Objective
Open the provided packet capture and locate the flag within the packet's payload data.

## Provided Files
- `heartbeat.pcap` — a 157-byte packet capture containing a single crafted UDP packet

## Flag Format
P2P{...}

## Notes
- No decoding, encryption, or steganography is involved
- A basic packet analysis tool is all that is needed
- Tools that may help: `wireshark`, `tshark`, `strings`
