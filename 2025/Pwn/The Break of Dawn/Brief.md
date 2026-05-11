# Brief.md

# [Easy] Pwn - The Break Of Dawn

## Category

Pwn

## Difficulty

Easy

## Author

Absolute Unit!

## Description

An Elder Scrolls themed pwn challenge.

Nothing much more can be said without giving the game away, so see what you can find.

Participants are provided with a compiled 32-bit binary and must investigate the program to identify the vulnerability and recover the flag.

## Objective

Analyse the provided binary, identify the vulnerability, and exploit it to retrieve the flag.

## Provided Files

- `theBreakOfDawn`
- `the-break-of-dawn.zip`

## Flag Format
```
P2P{...}
```
## Notes

This challenge is intended to introduce players to basic binary exploitation concepts, including stack-based buffer overflows and return-oriented programming style control flow redirection.

### Local Setup

Build the Docker image:

```bash
docker build -t the-break-of-dawn .
```

Run the Docker image:

```bash
docker run -p 4306:4306 the-break-of-dawn
```

Connect locally:

```bash
nc localhost 4306
```
