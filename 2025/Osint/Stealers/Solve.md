# Solve.md

# [Hard] OSINT - Stealers - Solve Guide

## Overview

This challenge begins with a small amount of threat intelligence relating to a suspected compromised persona.

The starting information is:

- traveljunkie_91@proton.me
- Date of compromise: March 25, 2025
- Stealer origin: Kraków region, Poland

The goal is to follow the trail from the email address to a stealer log, then use the recovered account information to locate a social media post containing a photo. The final answer is the exact building from which that photo was taken.

## Initial Analysis

The first step is to investigate whether the email address appears in any publicly indexed leaks, pastes, or breach-related content.

Searching for:

traveljunkie_91@proton.me

reveals that the email appears in a Pastebin entry:

https://pastebin.com/8AWbH8h2

The Pastebin entry contains a link to a Rentry page:

https://rentry.co/qquznm4y

## Following the Stealer Trail

The Rentry page presents itself as a fake infostealer note and contains a download link:

https://gofile.io/d/kN2Z36

Downloading the file provides a ZIP archive named:

logdump-0325-Krakow-ASUS.zip

This filename matches the challenge context:

- Compromise date: March 25, 2025
- Origin: Kraków region, Poland
- Device indicator: ASUS

## Inspecting the Archive

Opening the ZIP archive reveals three text files.

The important file is:

passwords.txt

Inspecting this file reveals credentials or account references linked to a Reddit account:

https://www.reddit.com/user/traveljunkie_91/

## Pivoting to Reddit

Visiting the Reddit profile shows activity from the user `traveljunkie_91`.

The account has posted an image to a newly created subreddit or page named `travelimages`.

Relevant post:

https://www.reddit.com/r/travelimages/comments/1kfc385/loved_this/

This post contains the image that must be geolocated.

## Image Geolocation

The next step is to analyse the posted image.

Useful geolocation checks include:

1. Inspect visible landmarks in the photo.
2. Look for skyline, roofline, architectural, road, tram, or river features.
3. Compare the view against mapping services and street-level imagery.
4. Identify the location shown in the image.
5. Work backwards from the perspective of the photograph to determine where the photo was taken from.

The important distinction is that the challenge does not ask for the place shown in the image. It asks for the exact building from which the photo was taken.

## Key Finding

The Reddit image can be geolocated to:

[REDACTED]

By analysing the angle, elevation, and visible landmarks, the photo can be traced back to the building it was taken from:

[REDACTED]

## Flag
```
P2P{REDACTED}
```
## Lessons Learned

This challenge demonstrates a realistic OSINT workflow involving credential exposure, stealer-log style artefacts, social media pivoting, and geolocation.

The key skills are:

1. Pivoting from an email address to public breach or paste data.
2. Following linked infrastructure such as Pastebin, Rentry, and file-hosting services.
3. Extracting useful account information from stealer-style logs.
4. Pivoting from credentials to social media presence.
5. Geolocating an image using perspective, landmarks, and environmental context.
6. Identifying the photographer's position rather than only the subject of the photo.