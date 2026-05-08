"""
# Brief.md

# [Easy] Misc - Match me if you can

## Category
Misc

## Difficulty
Easy

## Author
Thetvdh

## Description

You are given a regular expression string.

The flag is hidden inside the regex itself. Your task is to inspect the expression, decode any encoded characters, and recover the flag.

## Objective

Read the regex, simplify it, decode the escaped ASCII values where needed, and recover the flag.

## Provided Files

- regex.txt

## Regex
```
(?:\x50)(?:2)(?:\x50)(?:\x7b)(?:(?:[r]|r))(?:\x33)(?:[g])(?:\x33)(?:x)(?:_|[\x5f])(?:(?:1)|(?:1))(?:(?:5))(?:_|[\x5f])(?:(?:4))(?:m)(?:4)(?:z)(?:1)(?:n)(?:g)(?:_|[\x5f])(?:b)(?:u)(?:7)(?:_|[\x5f])(?:4)(?:l)(?:5)(?:0)(?:_|[\x5f])(?:4)(?:w)(?:f)(?:u)(?:l)(?:\x7d)
```
## Flag Format
```
P2P{...}
```
## Notes

The regex may look more complicated than it actually is.

Focus on what each group matches. Some characters are written directly, while others are represented as hexadecimal escape sequences.