# Random Insight

## Description
We have retrieved the source code for a binary being run by gang to encrypt their communications.
It appears to generate a random number to use as a validation that the user is one of the gang members to initiate the decryption.
The issue is the random number is generated from a seed that is set based on the time that the binary is run at and therefore unpredictable.
There must be a way to know what this number is before the user is asked for it, but after it has been generated.
Can you find out how to decrypt the text?

## Requirements
- Compiled `random_insight.c`
- Source of `random_insight.c`