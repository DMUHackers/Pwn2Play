# [Medium] Misc - Autobots Move Out

## Category
Misc

## Difficulty
Medium

## Author
x41x41x41 | JohnOP

## Description
An employee at the Innovation Centre has left on "less than good" terms. We need to get access to his account — can you recover his password from the provided hash?

A wordlist has already been generated, but brute force attempts are failing.

Whilst enumerating the system, the following password policy was identified:

- 15+ characters
- Must start with a capital letter
- Must end in four digits, followed by a symbol

## Objective
Identify the hash type, construct appropriate transformation rules to match the enforced password policy, and crack the hash to recover the password.

## Provided Files
- `md5.txt` — file containing the password hash
- `wordlist.txt` — pre-generated wordlist (base words, untransformed)

## Flag Format
P2P{RECOVEREDPASSWORD} — all uppercase

## Notes
- The wordlist contains the base word but in the wrong form — transformations are required
- The challenge title hints at the approach: "Autobots... transform"
- Tools that may help: `hashid`, `hash-identifier`, `john`, `hashcat`
