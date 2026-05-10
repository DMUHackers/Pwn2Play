# [Easy] Web - Flower Shop: The Re-Opening - Solve Guide

## Overview
The web application simulates an online flower shop, consisting of a shop front page with a search functionality, a login page, and an admin page locked behind authentication.

## Exploitation / Decryption / Solution Steps
The search functionality contains an SQL injection vulnerability which allows the user to extract the hashed password for the admin account. However, there is a mediocre SQL injection prevention in place that simply checks for key words within the input.

It checks for the words: "select", "SELECT", "from", "FROM", "where", "WHERE", "or", "OR", "and", "AND", "union", "UNION", "all", "ALL", "users", "USERS".
This can be bypassed by using mixed-case, for example: `'UniOn AlL selECt....` This bypasses the check.
This can also be done automatically within SQLMap using the flag `--tamper=randomcase`

Once the password hash is dumped from the database,it can be cracked using Hashcat or JohnTheRipper for example, then it is possible to log in using the email and password to get the flag from the **/admin** page.
