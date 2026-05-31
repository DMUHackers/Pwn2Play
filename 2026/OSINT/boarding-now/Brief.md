# [Medium] OSINT - Boarding Pass Exposure

## Category
OSINT / Digital Forensics

## Difficulty
Medium

## Author
Joe | NQ

## Description
An high-value target recently posted a photo of their travel setup to social media, inadvertently exposing their physical boarding pass. Security operations needs to map out their arrival vectors to establish a chronological profile of their movements.

Using the provided image (`1774543915_BoardingPass.jpg`), analyze the leaked boarding document to discover the target's destination airport. Once identified, cross-reference public flight tracking livestreams covering that specific hub on the day the data was leaked to find the very first operational timestamp captured on-screen.

## Objective
Decode the obscured destination airport from the boarding pass, find the corresponding 'Flight Focus' livestream archive for that specific day, and extract the first visible UTC timestamp.

## Provided Files
* `1774543915_BoardingPass.jpg`

## Flag Format
P2P{UTC_HH:MM:SS}

## Notes
* The challenge relies on decoding standard matrix barcodes used by the aviation industry.
* The date of travel matches the day the social media post went live: Sunday, March 29, 2026.