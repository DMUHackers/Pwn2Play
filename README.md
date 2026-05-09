# Pwn2Play

Archived Pwn2Play CTF challenges, files, and official solutions released by **DMUHackers** for public learning, practice, and reference.

Pwn2Play is a Capture The Flag event run by DMUHackers. This repository acts as the public archive for previous challenge sets, allowing students, competitors, and the wider cyber security community to revisit retired challenges after the event has concluded.

## About This Repository

This repository contains previous Pwn2Play CTF material organised by event year and category. Each challenge folder may include the original challenge files, source code, deployment notes, hints, flags, and official solution write-ups where available.

The current repository includes a `2025` archive folder with categories such as Crypto, Forensics, Full-Pwn, Misc, OSINT, Pwn, Rev, and Web. The repository is public and maintained under the DMUHackers organisation.

## Repository Structure
```
Pwn2Play/
├── 2025/
│   ├── Crypto/
│   ├── Forensics/
│   ├── Full-Pwn/
│   ├── Misc/
│   ├── Osint/
│   ├── Pwn/
│   ├── Rev/
│   └── Web/
└── README.md
```
Each year should follow a similar structure:
```
YEAR/
├── CATEGORY/
│   └── Challenge Name/
│       ├── README.md
│       ├── challenge files
│       ├── solve files
│       └── solution.md
```
## Challenge Categories

Challenges may be grouped into the following categories:

| Category | Description |
|---|---|
| Crypto | Cryptography, encoding, decoding, and cipher-based challenges |
| Forensics | File analysis, memory analysis, disk artefacts, packet captures, and evidence recovery |
| Full-Pwn | Multi-stage challenges involving enumeration, exploitation, privilege escalation, or chained attack paths |
| Misc | General problem-solving, scripting, logic, or unusual challenge types |
| OSINT | Open-source intelligence investigation and research-based challenges |
| Pwn | Binary exploitation, memory corruption, and exploitation fundamentals |
| Rev | Reverse engineering, static analysis, dynamic analysis, and crackmes |
| Web | Web application security, source review, injection, auth flaws, and browser-based exploitation |

## How To Use This Repository

Clone the repository:

`git clone https://github.com/DMUHackers/Pwn2Play.git`

Then enter the repository:

`cd Pwn2Play`

Navigate into a year and category:

`cd 2025/Web`

Each challenge should be treated as a retired CTF challenge. Read the challenge prompt first, attempt the challenge yourself, then refer to the official solution if provided.

## Suggested Challenge Folder Format

For consistency, challenge folders should ideally follow this format:
```
Challenge/
├── Brief.md         # Challenge prompt, difficulty, category, author, and player-facing information
├── Solve.md         # Official solution or write-up
└── Task Files/      # Files given to players
```
Suggested `Brief.md` format for each challenge:
## Brief.md Template

```markdown
# [Difficulty] Category - Challenge Name

## Category


## Difficulty


## Author


## Description


## Objective


## Provided Files


## Flag Format

P2P{...}

## Notes
```
Suggested `Solve.md` format for each challenge:
## Solve.md Template
```markdown
# [Difficulty] Category - Challenge Name - Solve Guide

## Overview


## Initial Analysis


## Enumeration / Inspection


## Method


## Exploitation / Decryption / Solution Steps


## Commands Used


## Scripts Used
## Description

Challenge description shown to players.

## Provided Files

- file1.zip
- source.py

## Flag Format

`P2P{example_flag}`

## Notes

Any deployment notes, intended learning outcomes, or challenge-specific information.
```
## Educational Purpose

This repository is intended for:

- Cyber security students practising retired CTF challenges
- DMUHackers members reviewing previous events
- Challenge authors documenting their work
- Learners building skills across practical cyber security disciplines
- Event organisers looking at previous Pwn2Play challenge structure

All material is provided for educational and ethical use only.

## Responsible Use

Do not use any code, techniques, or challenge material from this repository against systems you do not own or do not have explicit permission to test.

Some challenges may demonstrate offensive security concepts. These are included strictly to support controlled learning, defensive understanding, and authorised security education.

## Contributing

Contributions are welcome from Pwn2Play organisers and challenge authors.

When adding a retired challenge, please include:

1. The original challenge prompt
2. Any files provided to players
3. The intended flag
4. A short solution or full write-up
5. Any required setup or deployment instructions
6. The challenge author, category, difficulty, and event year

Please use a branch and submit a pull request for review before merging into the main archive.

## Maintainers

This repository is maintained by **DMUHackers**.

For more information, visit:

- DMUHackers GitHub: https://github.com/DMUHackers
- Pwn2Play Repository: https://github.com/DMUHackers/Pwn2Play

## Licence

Unless stated otherwise in individual challenge folders, this repository is provided for educational use by DMUHackers.

Challenge authors retain credit for their work. If you reuse or reference material from this repository, please credit DMUHackers and the original challenge author where listed.