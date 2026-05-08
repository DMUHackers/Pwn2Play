"""
# Brief.md

# [Difficulty] Pwn - LetsChat

## Category
Pwn

## Difficulty
Easy

## Author
Acfirth

## Description

You have been given a compiled binary for a simple chat application.

The program simulates a basic chat app where users can create a user profile and send a message to that user. The messaging functionality does not perform any real networked communication, but the application also allows users to leave feedback by rating the app.

Your task is to analyse the binary, identify the vulnerability, and exploit it to gain a shell.

## Objective

Exploit the vulnerable binary and retrieve the flag.

## Provided Files

- `LetsChat` binary
- Docker deployment files

## Setup

Extract the challenge ZIP, change into the `LetsChat` directory, build the Docker image, and run the service:
```
docker build -t letschat .
docker run --rm -it -p 1337:1337 letschat
```
Interact with the service using netcat:
```
nc 127.0.0.1 1337
```
## Flag Format
```
P2P{...}
```
## Notes

The binary presents itself as a simple chat application. Focus on user-controlled input fields and check whether any of them allow more data than the program safely handles.