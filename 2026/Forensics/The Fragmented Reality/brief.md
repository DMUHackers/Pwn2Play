# Challenge Brief: the fragmented reality 🏭

## Category
Forensics / Network Analysis

## Difficulty
Hard

## Description

A custom industrial protocol is communicating over **TCP port 8888**. Intelligence suggests the operator is hiding data in an unconventional way — **not in the packet payload**, but somewhere far less obvious.

You are given a packet capture: `industrial.pcap`

Recover the hidden flag.

## Artifacts

| File | Description |
|------|-------------|
| `industrial.pcap` | Network packet capture of industrial control traffic |

## Objectives

| # | Objective |
|---|-----------|
| 1 | Identify the packets relevant to the custom protocol (TCP port 8888) |
| 2 | Locate where the data is actually hidden within those packets |
| 3 | Understand how the hidden values are encoded |
| 4 | Reconstruct the correct order of the data |
| 5 | Decode the final message |

## Hints

- The payload of every packet is empty. Look elsewhere.
- TCP headers have more fields than just source/destination port and sequence number.
- Order matters — but the packets weren't sent in order.

## Flag Format

```
p2p{hex_string}
```
