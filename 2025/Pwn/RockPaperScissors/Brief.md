# Brief.md

# [Medium] Pwn - RockPaperScissors

## Category
Pwn

## Difficulty
Medium

## Author
Thetvdh

## Description

You have been given a Rock Paper Scissors binary.

The goal is simple: beat the computer 100 times in a row.

That sounds straightforward, but the computer appears to be making its choices unpredictably. Analyse the binary, understand how the game decides its moves, and find a way to consistently win.

## Objective

Exploit the binary so that you can predict the computer's choices and win 100 consecutive games.

## Provided Files

- `rps`
- `rockpaperscissors.zip`

## Flag Format
```
P2P{...}
```
## Notes

The binary depends on runtime state. Pay attention to environment variables, random number generation, and any unsafe output handling.