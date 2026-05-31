# Challenge: Locate Me! 🌍

**Category:** OSINT  
**Difficulty:** Easy  
**Flag Format:** `P2P{LoungeName_IATACode_NearestGateNumber}`

---

## Description

A photo has been taken inside an airport lounge. Using only the image and any available metadata, identify:

1. **The name of the airport lounge** shown in the photo
2. **The IATA airport code** of the airport it is located in
3. **The nearest gate number** to that lounge

The signage, interior design, and branding visible in the image contain all the clues you need. Additional hints may be embedded in the image's metadata.

---

## Provided Asset

- `locate-me.jpg` — A photo taken inside an airport lounge.

---

## What You Need to Find

| Field | Description |
|---|---|
| `LoungeName` | The specific lounge name (no spaces) |
| `IATACode` | 3-letter IATA code of the airport |
| `NearestGateNumber` | Gate number nearest to the lounge (from official airport info) |

---

## Flag

`P2P{LoungeName_IATACode_NearestGateNumber}`
