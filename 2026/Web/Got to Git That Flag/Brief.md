# [Easy] Web - I Got to Git That Flag

## Category
Web

## Difficulty
Easy

## Author
x41x41x41 | JohnOP

## Description
Someone pushed a little too much to production.

## Objective
Recover a deleted flag from an exposed `.git` repository left accessible on a production web server.

## Provided Files
- Web application with an exposed `/.git` directory

## Flag Format
P2P{...}

## Notes
- The challenge name is a hint — something Git-related has been accidentally exposed
- The flag was committed to the repository at some point, then deleted — but Git never forgets
- Tools that may help: `wget`, `git-dumper`, `git log`, `git show`
