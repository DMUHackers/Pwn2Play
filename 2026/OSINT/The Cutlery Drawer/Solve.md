# Solve.md

# [Easy] OSINT - The Cutlery Drawer - Solve Guide

## Overview

The Cutlery Drawer is an easy OSINT challenge where players are given an image of a distinctive carpet and must identify the location it belongs to.

The image shows a patterned Wetherspoons carpet. Wetherspoons pubs are known for having unique carpet designs, so the intended solve path is to recognise the carpet style, search for Wetherspoons carpet references, and match the design to the correct venue.

The correct location is:

```text
The Standing Order, Edinburgh
```

The final flag is:

```text
P2P{The_Standing_Order}
```

## Solve Walkthrough

### Step 1: Inspect the challenge prompt and image

The challenge description is intentionally minimal:

```text
God I just can't stand these challenges!
```

The word `stand` is a soft hint towards the venue name:

```text
The Standing Order
```

Open the provided image:

```text
OSINT.jpeg
```

At first glance, the image may look like an abstract pattern, wall design, or decorative artwork. The key observation is that it is actually a carpet.

Important visual clues:

```text
- The image shows a highly distinctive patterned carpet.
- The pattern has an ornate Wetherspoons-style design.
- Wetherspoons pubs are known for unique carpet designs.
- The challenge title, "The Cutlery Drawer", hints towards pubs, tables, and food venues.
- The word "stand" in the prompt hints towards "Standing".
```

### Step 2: Check image metadata

A sensible first check is to inspect the image metadata:

```bash
exiftool OSINT.jpeg
```

In this challenge, the EXIF data has been stripped, so the metadata does not directly reveal the location.

An optional file check can also be run:

```bash
file OSINT.jpeg
```

Since metadata does not solve the challenge, the player should focus on the visual content of the image.

### Step 3: Identify the image as a Wetherspoons carpet

The main OSINT leap is recognising that the image shows a Wetherspoons carpet.

Useful search terms include:

```text
wetherspoons carpet green ornate pattern
wetherspoons carpet Edinburgh
unique Wetherspoons carpets Scotland
wetherspoons carpet Standing Order
Wetherspoons carpets The Standing Order Edinburgh
```

A reverse image search may also help, depending on the search engine used.

Once the player identifies the design as a Wetherspoons carpet, the challenge becomes a venue-matching task.

### Step 4: Match the carpet to the venue

The carpet design matches the Wetherspoons venue:

```text
The Standing Order, Edinburgh
```

This also fits the soft hint in the challenge prompt:

```text
God I just can't stand these challenges!
```

The word `stand` points towards:

```text
Standing
```

### Step 5: Build the flag

The required flag format is:

```text
P2P{Name_of_place}
```

The location is:

```text
The Standing Order
```

Using underscores between the words gives:

```text
The_Standing_Order
```

The final flag is:

```text
P2P{The_Standing_Order}
```

## Final Answer

```text
P2P{The_Standing_Order}
```