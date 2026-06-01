# [Medium] OSINT - Boarding Pass Exposure: Part 2 - Solve Guide

## Overview
This challenge requires pivoting from a validated live-feed capture timestamp to historic flight telemetry databases to verify a physical commercial airframe's origin and transponder signature.

* **Origin Airport:** Hartsfield–Jackson Atlanta International Airport (ATL)
* **ATC Callsign:** VIR104L
* **Final Flag:** `P2P{ATL_VIR104L}`

## Initial Analysis
From the previous breakthrough in Part 1, we know the target flight landed at **London Heathrow Airport (LHR)** on and crossed the stream array metrics frame at approximately **05:43:46 UTC**.

## Enumeration / Inspection
1. **Target Matrix:** We need an arriving aircraft at LHR touching down immediately prior to or at 05:44 UTC.
2. **Telemetry Sources:** Because standard live aggregators (like Flightradar24 or RadarBox) restrict historical tracking lookups to a rolling 7-day window for basic users, alternate public record ledgers must be targeted:
   - Official Heathrow Airport daily historical arrival logs.
   - Publicly accessible ADS-B Exchange database records.
   - Planespotter user-generated community message boards or log databases tracking transatlantic early-morning arrivals.

## Method
1. **Correlate Time with Arrival Tables:** Cross-reference the timestamp (05:43:46 UTC) with LHR's arrivals directory for March 29, 2026, to identify the active flight string operating as the first runway occupant.
2. **Map the Route Designator:** Isolate the flight's commercial number to extract its point of departure (IATA code).
3. **Verify Transponder Callsign:** Extract the precise ICAO/ATC callsign suffix configuration (`VIR104L`) instead of merely the commercial itinerary format (`VS104`).

## Exploitation / Decryption / Solution Steps
1. **Querying Logistics:** Inspecting the landing timetable for early morning long-haul arrivals to LHR on March 29 shows Virgin Atlantic flight **VS104** landing right on the schedule threshold.
2. **Origin Lookup:** Examining flight schedules or route history for flight VS104 indicates a direct long-haul route from **Hartsfield–Jackson Atlanta International Airport (ATL)**.
3. **Determining the Transponder Call Sign:** Checking the open-source historical ADS-B payload details for that specific flight configuration shows that Virgin Atlantic structures this transponder profile using the Alpha-suffixed callsign format **VIR104L**.
4. **Constructing the Token:** Stitch the 3-letter departure code (`ATL`) together with the confirmed callsign (`VIR104L`).