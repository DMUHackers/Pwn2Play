# Solve: Locate Me! 🔍

**Flag:** `P2P{PlazaPremiumLounge_NBO_4}`

---

## Step-by-Step Solution

### Step 1 — Extract Image Metadata

Run `exiftool` (or any EXIF viewer) on `locate-me.jpg`:

```bash
exiftool locate-me.jpg
```

Key finding: The metadata contains a **geographic region tag pointing to Africa**.

---

### Step 2 — Identify the Lounge Brand

Look at the table card visible in the foreground of the image:

- **"The Art of Travel – Summer Edition"** — a Plaza Premium Group marketing campaign
- Bottom of the card: **PLAZA PREMIUM GROUP** branding
- Two services advertised:
  - **Allways Concierge** — "Your personal airport assistant"
  - **Airport Lounge** (co-branded **FIRST × Plaza Premium**) — "Your destination before departure"

This confirms the lounge operator is **Plaza Premium Group**.

---

### Step 3 — Cross-Reference Plaza Premium Lounges in Africa

Plaza Premium Group operates a limited number of lounges on the African continent. Researching their official website or lounge directories (e.g. LoungeBuddy, Priority Pass) for African locations:

- **Jomo Kenyatta International Airport, Nairobi, Kenya (NBO)** — Plaza Premium Lounge ✅
- Other African Plaza Premium locations exist but don't match the interior.

The interior visible in the background (elongated hall, exposed beam ceiling, warm pendant lighting, mixed seating areas with green upholstered chairs and cream booths) is consistent with the **Plaza Premium Lounge at JKIA, Nairobi**.

---

### Step 4 — Confirm via Lounge Interior Design

Searching for images of the Plaza Premium Lounge at Nairobi JKIA confirms:

- Long corridor-style layout with structural beam ceiling ✅
- Combination of booth and loose-chair seating ✅
- Warm pendant lighting at the far end ✅
- Colour palette matching the background in the photo ✅

**Airport confirmed: Nairobi Jomo Kenyatta International — IATA code `NBO`**

---

### Step 5 — Find the Nearest Gate Number

Navigate to the **Kenya Airports Authority** official website or JKIA terminal map:

> [https://www.kaa.go.ke](https://www.kaa.go.ke)

The terminal map for JKIA shows the Plaza Premium Lounge located in the **international departures** area. According to the airport's published gate layout, the nearest gate to the Plaza Premium Lounge is **Gate 4**.

---

## Flag Assembly

| Component | Value |
|---|---|
| Lounge Name | `PlazaPremiumLounge` |
| IATA Code | `NBO` |
| Nearest Gate | `4` |

```
P2P{PlazaPremiumLounge_NBO_4}
```

---

## Tools Used

| Tool | Purpose |
|---|---|
| `exiftool` | EXIF/metadata extraction → region: Africa |
| Plaza Premium website | Confirmed African lounge locations |
| Google Images / LoungeBuddy | Interior photo comparison for NBO lounge |
| JKIA / KAA terminal map | Gate number lookup |

---

## Key Takeaways

- **Metadata is always your first stop** — EXIF data cut the search space from global to one continent instantly.
- **Branding in images is a goldmine** — Plaza Premium Group's table card identified the operator and campaign.
- **Visual fingerprinting works** — matching the lounge's distinctive interior against reference photos is a reliable OSINT technique for airports.
- **Official airport websites** are authoritative for gate/lounge proximity data.
