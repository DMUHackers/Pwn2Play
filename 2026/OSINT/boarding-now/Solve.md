# [Medium] OSINT - Boarding Pass Exposure - Solve Guide

## Overview
The challenge requires us to perform barcode analysis on a partially redacted boarding pass to extract an airport code. From there, we pivot to open-source flight-tracking streams to identify a specific timeline checkpoint.

* **Destination Airport:** London Heathrow Airport (LHR)
* **Target Date:** March 29, 2026
* **Final Flag:** `P2P{UTC_05:43:46}`

## Initial Analysis
We are provided with `1774543915_BoardingPass.jpg`. While fields like name, flight number, origin, and destination are visibly blanked out on the paper ticket, the 2D matrix barcode on the bottom right has been left completely unredacted.

## Enumeration / Inspection
1. **Barcode Type:** The rectangular 2D barcode on the ticket is identified as a **PDF417** format, which is the universal standard for Bar Coded Boarding Passes (BCBP).
2. **Standard Profiling:** BCBP strings strictly follow the **IATA 797** standard format, meaning that even if the text on the front is missing, the raw data string retains structure fields like passenger names, operating airline, Julian date, and airport IATA codes.

## Method
1. **Extract and Decode:** Isolate the PDF417 matrix block from the image and process it using a barcode library or online tool to yield the raw ASCII payload string.
2. **Parse IATA Fields:** Read the decoded string to locate the 3-letter target destination token (`LHR`).
3. **OSINT Correlation:** Search for the phrase `'Flight Focus'` alongside the discovered airport to locate the exact streaming channel.
4. **Timeline Scrape:** Pinpoint the stream archive matching the travel date (March 29, 2026) and find the first timestamp stamped on the video player or overlay feed.

## Exploitation / Decryption / Solution Steps
1. **Decode Barcode:** Using an automated script or an online reader, decoding the PDF417 matrix outputs a standard BCBP data stream containing `LHR`. This reveals the destination is **London Heathrow Airport**.
2. **Pivoting to Stream:** A quick search reveals **Flight Focus 365**, a popular YouTube channel streaming 24/7 high-definition PTZ camera footage of aircraft arrivals and departures on Heathrow's North Runway.
3. **Finding the Timestamp:** Locate the archived stream broadcast for Sunday, March 29, 2026. Scrubbing directly to the beginning of that broadcast block reveals the first operational flight movement captured on the layout overlay happens exactly at **05:43:46 UTC**.

## Commands Used
If using CLI utilities to extract the raw string data:
```bash
# Extract data string from the cropped barcode region
zbarimg --raw -Spdf417.enable barcode_crop.png