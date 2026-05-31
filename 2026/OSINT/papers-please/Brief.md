# [Medium] OSINT - Boarding Pass Exposure: Part 2

## Category
OSINT / Flight Tracking

## Difficulty
Medium

## Author
Joe | NQ

## Description
In Part 1 of our investigation, we successfully localized the target's destination airport as London Heathrow (LHR) and synchronized our operational clock to a public livestream tracking network. Now, we need to gather exact intelligence regarding the asset that occupied that tracking frame.

Identify the origin airport and official ATC callsign of the very first incoming flight captured on that morning broadcast stream on Sunday, March 29, 2026. 

## Objective
Utilize open-source flight registration databases, historic flight tracker lookups, or user-generated planespotter logs to isolate the exact route origin and registration callsign corresponding to the target landing event.

## Provided Files
* None (Relies on infrastructure established in Part 1)

## Flag Format
P2P{IATA_XYZ123A} (e.g., P2P{ATL_VIR104L})

## Notes
* Part 1 (`boarding.now`) must be solved first to pin down the timestamp framework.
* Historic flight radar historical playbacks can often be locked behind premium tiers after a few days, so pivot to public airport arrival records, regional planespotter archives, or targeted ADS-B history lookups.