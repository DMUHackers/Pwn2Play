# [Easy] Forensics - The Needle in the Haystack

## Category
Forensics

## Difficulty
Easy

## Author
x41x41x41 | JohnOP

## Description
An attacker exfiltrated a secret key by hiding it across multiple ICMP Echo Request packets. However, they only hid data in packets with the same TTL. All other packets are noise.

## Objective
Analyse the provided packet capture, filter for the relevant ICMP packets, and extract the hidden key from their payloads.

## Provided Files
- `exfil.pcap` — a packet capture containing a mix of ICMP traffic

## Flag Format
P2P{...}

## Notes
- Not all ICMP packets are relevant — identify what distinguishes the signal from the noise
- The hidden data is distributed across multiple packets; each contributes one byte
- Tools that may help: `wireshark`, `tshark`, `scapy`, Python with `pyshark` or `dpkt`
