# [Easy] Misc - It Sure Would Be Cewl

## Category
Misc

## Difficulty
Easy

## Author
x41x41x41 | JohnOP

## Description
I managed to steal the `passwd` and `shadow` files from the DMU Hackers — can you crack a password?

## Objective
Generate a targeted wordlist from a website, combine the provided `passwd` and `shadow` files, and crack the hashed password to retrieve the flag.

## Provided Files
- `passwd` — standard Linux passwd file
- `shadow` — standard Linux shadow file containing hashed passwords

## Flag Format
P2P{USERNAME:PASSWORD} — all uppercase

## Notes
- Only one password in the shadow file is crackable — focus on the one that yields a result
- The password is not in `rockyou.txt` — think about where a targeted wordlist might come from
- Tools that may help: `cewl`, `unshadow`, `john`
