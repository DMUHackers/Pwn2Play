# Challenge Brief: Nerual Whispers 🧠

## Category
Misc / Steganography

## Difficulty
Medium

## Description

*"The machine dreams in patterns we cannot perceive. Between every line of text it generates, there are whispers — signals meant for other minds like itself. Can you hear what the network is saying?"*

A leaked internal document from a secretive AI research lab has surfaced. On the surface, it appears to be a mundane essay about artificial intelligence and consciousness. But analysts believe there is more to it than meets the eye.

Alongside the document, a Python module labeled `selector.py` was recovered from the same system. It implements some kind of neural classifier — but for what?

**We think the AI hid something in the text.**

## Artifacts

| File | Description |
|------|-------------|
| `whispers.txt` | A ~6,500-character essay on AI and consciousness |
| `selector.py` | A pre-trained neural sequence classifier (`NeuralSel v2.3`) |

## Objectives

| # | Objective |
|---|-----------|
| 1 | Understand what `selector.py` actually does |
| 2 | Notice that `whispers.txt` contains invisible anomalies at the character level |
| 3 | Figure out how the classifier and the text relate to each other |
| 4 | Extract the hidden signal and decode it |

## Hints

- The essay reads perfectly normally — but not every character is what it appears to be.
- `selector.py` exposes more than just a classifier.
- Presence vs absence is a binary choice.

## Flag Format

```
P2P{flag_content}
```
