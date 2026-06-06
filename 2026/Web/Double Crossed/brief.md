# Challenge Brief: Double Crossed 🕸️

## Category
Web

## Difficulty
Medium

## Description

A social media platform has been deployed internally. It looks harmless — users can post, comment, like, and report content for moderation. But something about it feels off.

The name is a hint. So is the admin panel.

## Setup

```bash
docker pull <registry>/double-crossed:latest
docker run -p 3000:3000 <registry>/double-crossed:latest
```

Access at: `http://localhost:3000`

## Rules

- Do **not** access the Docker container directly — interact only via `http://localhost:3000`
- Registration is restricted

## Objectives

| # | Objective |
|---|-----------|
| 1 | Find a way to register an account |
| 2 | Get access to the admin panel |
| 3 | Discover what the admin panel can do |
| 4 | Use it to read the flag |

## Flag Format

```
P2P{flag_content}
```