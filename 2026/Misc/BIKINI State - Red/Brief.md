# Brief.md

# [Easy] Misc - BIKINI State: RED

## Category

Misc

## Difficulty

Easy

## Author

T.Λ.R.S

## Description

```text
The year is 1975. You are working as part of the Royal Observer Corps, stationed deep within the York Group Control bunker.

Outside, the siren’s wail has been replaced by a deafening, unnatural silence. You have just transitioned to BIKINI State: RED. Fifteen feet below the topsoil, the air is stale and the lights flicker as the first "Flash" report from Skipsea Post reaches your desk. The clock reads 1421 Zulu.

Your task is to take the readings; the bearing of the fire and the weight of the air, and plot them on the master board.

You must use the TRUE bearing provided by the observers to ensure the strike is fixed with absolute precision.

The volunteers at the surface have seen the light and recorded the pressure. Now, it is up to you to triangulate the source.

Find the coordinate. Map the fallout. Save what can be saved.

First step, where did I leave that pesky control panel... somewhere on https://welbournesecurity.com/ I believe 👀
```

## Objective

Find the hidden control panel starting from `https://welbournesecurity.com/`, recover the required Royal Observer Corps traffic data, calculate the corrected TRUE bearings, use the ROC Network page to determine the target coordinate, and identify the location and motto needed to form the flag.

## Provided Files

No files are provided directly to players at the start of the challenge.

Players are only given the challenge brief and the starting website:

```text
https://welbournesecurity.com/
```

## Flag Format

```text
P2P{NAME_NICK_NAME}
```

## Notes

This challenge requires players to perform light web enumeration, identify a hidden route, retrieve the ROC traffic sheets, calculate corrected bearings, and use the ROC Network page to determine the final GPS coordinate.

The relevant starting point is:

```text
https://welbournesecurity.com/
```

The main ROC Network page may be useful once the correct traffic data has been recovered:

```text
https://welbournesecurity.com/projects/roc-network/
```