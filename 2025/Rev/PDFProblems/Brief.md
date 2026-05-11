# Brief.md

# [Medium] Rev - PDFProblems

## Category

Reverse Engineering (Rev)

## Difficulty

Medium

## Author

Thetvdh

## Description

A suspicious fiscal report PDF has been provided. Somewhere inside the document lies hidden functionality and a secret flag. The PDF contains embedded JavaScript that has been heavily obfuscated and encoded.

Can you inspect the document, reverse the obfuscation, and uncover the hidden flag?

## Objective

Analyze the PDF, extract the embedded JavaScript, deobfuscate it, identify the hidden request and decode the final payload to recover the flag.

## Provided Files
```
DMUHackers_2025_Fiscal_Report.pdf
```
## Flag Format
```
P2P{...}
```
## Notes

- The PDF contains embedded JavaScript.
- The JavaScript is obfuscated multiple times.
- Knowledge of PDF internals, JS deobfuscation and basic cryptography may help.
