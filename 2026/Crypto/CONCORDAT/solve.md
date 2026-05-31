# CONCORDAT — Full Solve Walkthrough

---

## Stage 0 — Find the entry

The Concordat project is publicly listed at `/projects/concordat/`, but the
intercepts are not linked from there. The way in is a hidden anchor in the
page's prose.

1. Visit `https://welbournesecurity.com/projects/concordat/`. Read the
   middle section ("Three back rooms, one week of weather"). The phrase
   **watch schedule** in the "The watch" card is a hidden link.
2. Discovery routes:
   - Hover the phrase — cursor changes to pointer, status bar shows `/ops/sked.txt`.
   - Tab through focusable elements — the anchor takes focus with a ring.
   - View source — `<a href="/ops/sked.txt" style="color:inherit;text-decoration:none;">watch schedule</a>`.

3. Fetch `https://welbournesecurity.com/ops/sked.txt`:

   ```
   BBC MONITORING SERVICE — Y-SECTION
   WATCH SCHEDULE (ABRIDGED)

   EXERCISE: CONCORDAT
   ...

   Route group:

     c2VjdGlvbi1paWk=
   ```

4. Base64-decode `c2VjdGlvbi1paWk=` → `section-iii`.

5. Visit `https://welbournesecurity.com/section-iii/` — three intercept
   messages, three download links pointing at:
   - `/projects/concordat/intercepts/intercept-a/` (WAVERLY)
   - `/projects/concordat/intercepts/intercept-b/cable.html` (SOLO)
   - `/projects/concordat/intercepts/intercept-c/telegram-brief.txt` (KURYAKIN)
   - Pointer to `/projects/concordat/operator/` at the bottom (combined-flag workstation).

`robots.txt` is **not** a hint anymore — it only Disallows `/ops/traffic.txt`
(legacy ROC entry). The hidden anchor on the landing page is the only
discoverable starting point.

---

## Stage 1 — WAVERLY (MI6 / British)

Visit `/projects/concordat/intercepts/intercept-a/`. Four downloadable files:
`station-brief.txt`, `broadcast.ogg`, `keymat.txt`, `intercept-log.txt`.
Briefs are one-line metadata only; the watch log records when the broadcast
landed but no longer explains the decode procedure.

### Transcribe the broadcast

`broadcast.ogg` is an English-voice numbers station (in-house recording,
British voice, Opus 48 kbps mono, ~41 s). Transcript:

1. `Attention. Attention. Attention.`
2. `This is STATION X. Message follows.`
3. `Indicator:` then the indicator group spoken twice:
   **`Zero. Zero. Zero. Four. Two.`** → `00042`.
4. `Groups follow.` Then eight body groups, each preceded by `BREAK`:
   - `Four. Five. Three. One. Two.`    → `45312`
   - `One. Nine. Four. Six. Four.`     → `19464`
   - `Seven. Two. Eight. Zero. Nine.`  → `72809`
   - `Nine. Three. Five. Three. Eight.`→ `93538`
   - `Three. Zero. Four. Four. Nine.`  → `30449`
   - `Three. Nine. Zero. Seven. Two.`  → `39072`
   - `Seven. Six. Five. Five. Zero.`   → `76550`
   - `Five. Seven. Seven. One. Two.`   → `57712`
5. `Message ends. End of transmission.`

### Resolve the pad row

Indicator `00042` → use **row 042** from `keymat.txt`:

```
73849 21750 38461 28394 75692 81047 39582 64193
```

### Mod-10 decode (manual — no UI helper)

The WAVERLY page does NOT calculate for you. Use the in-page scratch notepad
(or any local tool) to compute `PT = (CT + PAD) mod 10` per digit, aligning
each ciphertext group with the corresponding pad group. Worked table:

| CT      | PAD     | PT (sum mod 10) |
|---------|---------|-----------------|
| `45312` | `73849` | `18151`         |
| `19464` | `21750` | `30114`         |
| `72809` | `38461` | `00260`         |
| `93538` | `28394` | `11822`         |
| `30449` | `75692` | `05031`         |
| `39072` | `81047` | `10019`         |
| `76550` | `39582` | `05032`         |
| `57712` | `64193` | `11805`         |

Concatenate: `18151 30114 00260 11822 05031 10019 05032 11805` →
`1815130114002601182205031100190503211805`.

### Read as 2-digit letter codes

Split into pairs: `18 15 13 01 14 00 26 01 18 22 05 03 11 00 19 05 03 21 18 05`.
Decode with A=01..Z=26, 00=space:

```
R  O  M  A  N  _  Z  A  R  V  E  C  K  _  S  E  C  U  R  E
```

Plaintext: **`ROMAN ZARVECK SECURE`**.

### Fragment

CONCORDAT fragment (second word of plaintext): **`ZARVECK`**.
No per-leg verifier — the player banks the answer and only confirms it
correct at the umbrella workstation once all three fragments are in.

---

## Stage 2 — SOLO (CIA / American)

Open `https://welbournesecurity.com/projects/concordat/intercepts/intercept-b/cable.html`.

The cable renders as a CIA Station Rome traffic sheet with multiple black
redaction bars across six numbered paragraphs. The brief (`cable.txt`) is a
one-line header; nothing tells the player which redaction is the target or
how to defeat the redaction.

### Reveal the redactions (text-select no longer works — DevTools required)

The current `.redact` class blocks text-selection (`user-select: none`) and
the visible content of each span is *noise glyphs* (`▓▓▓▓▓▓▓`), not the real
text. Naive text-select yields nothing.

**Recovery path — DevTools + base64.** Open DevTools → Inspect on a
redacted span:

```html
<p class="cable-subj">SUBJ: ASSET <span class="redact" data-c="S0VUUk9WRQ==">▓▓▓▓▓▓▓</span> DEBRIEF — FOLLOW-UP</p>
```

The real text is base64-encoded in the `data-c` attribute. Base64-decode
`S0VUUk9WRQ==` → `KETROVE`.

**Faster recovery — JS console.** Paste into the console:

```js
[...document.querySelectorAll('span.redact')].map(s => atob(s.dataset.c)).join('\n')
```

Returns every redaction in the cable as plaintext. Useful for sweeping the
body redactions and the three Cyrillic key candidates in one pass.

**Path that no longer works:** dragging across the redaction with a mouse
copies the noise glyphs (or nothing — `user-select: none`).

### Identify the fragment

The SUBJ line redaction is the asset codename: **`KETROVE`**.

Other body redactions are decoys (handler name `ROCKWELL`, meeting
locations `VIA DEL CORSO 14` / `PIAZZA NAVONA`, Soviet contact `VASILIEV`,
cover `MAARTEN VAN DEN BERG` / `DE TELEGRAAF`, programme codename
`DARK STAR ENGINE TEST DATA`, monetary `15,000`, asset cover
`AEROSPACE TRADE CONSULTANT`, signature `A. RANIERI`).

### Note for KURYAKIN — three Cyrillic redactions in paragraph 6

Paragraph 6 lists three Russian-side names under labels
"HANDLER REPORTING LINE", "OPERATION CODENAME", "FALLBACK PRINCIPAL":

```html
<span class="redact">ЛЕНИН</span>
<span class="redact">СТАЛИН</span>
<span class="redact">ХРУЩЕВ</span>
```

These are the candidate keys for KURYAKIN. The player keeps note of all three
and tests them in Stage 3.

### Fragment

**`KETROVE`** (SUBJ line). The cable has no per-leg verification on its own
page; the fragment is verified only at the combined-flag workstation.

---

## Stage 3 — KURYAKIN (KGB / Soviet)

Visit `/projects/concordat/intercepts/intercept-c/` — KURYAKIN now has its
own dossier-style page. Ciphertext shown inline; `telegram.txt` and
`telegram-brief.txt` available as downloads; scratch notepad and per-leg
self-check beneath.

### Inputs

- Ciphertext (also on the page and in `telegram.txt`): **`НЙЫЫЬЬ`** (6 letters).
- Brief: one-line metadata (`GCHQ H-DIVISION · LUBYANKA-INBOUND TELETYPE
  · 14 MAR 1989 · 0445 MSK`). No mention of cipher scheme.
- Telegram NOTES section: confirms `Six-letter ciphertext, no separators…
  Recovered keying material for this period is held alongside this telegram`.
- Inbox cue (on `/section-iii/`) AND operator note on the KURYAKIN page:
  `Period key not recovered locally.` — the signal that the key lives
  in another leg.
- Russian alphabet (33 letters, 0-indexed): `АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ`.

### Recognise the scheme

Short Cyrillic ciphertext + a known Russian alphabet + a candidate key word
strongly suggests Vigenère. Try each of the three Cyrillic redactions
recovered in Stage 2 as the key.

### Test each candidate key

Decryption formula: `P[i] = (C[i] − K[i mod n] + 33) mod 33`.

| Key      | Decryption | Plausible? |
|----------|-----------|------------|
| `СТАЛИН` | `ЬЧЫПУО`  | No — soft sign + rare letters. |
| `ХРУЩЕВ` | `ШЩЗВЧЪ`  | No — Ш-Щ adjacent doesn't occur in real Russian words. |
| `ЛЕНИН` | `ВЕНТОР`  | **Yes — legible Russian-shaped word.** |

### Work through the live key

| Position | C  | C idx | K  | K idx | (C − K + 33) mod 33 | P  |
|----------|----|-------|----|-------|---------------------|----|
| 1        | Н  | 14    | Л  | 12    | 2                   | В  |
| 2        | Й  | 10    | Е  | 5     | 5                   | Е  |
| 3        | Ы  | 28    | Н  | 14    | 14                  | Н  |
| 4        | Ы  | 28    | И  | 9     | 19                  | Т  |
| 5        | Ь  | 29    | Н  | 14    | 15                  | О  |
| 6        | Ь  | 29    | Л  | 12    | 17                  | Р  |

Plaintext: **`ВЕНТОР`** (Russian-looking invented name; not a real
historical figure).

### Transliterate

Unambiguous one-to-one: В=V, Е=E, Н=N, Т=T, О=O, Р=R → **`VENTOR`**.

### Fragment

**`VENTOR`**. (The combined workstation's input normaliser strips Cyrillic;
the Latin transliteration is what the player submits.) No per-leg verifier
— confirmation only at the umbrella workstation.

---

## Stage 4 — Assemble and verify

Visit `/projects/concordat/operator/`. Three inputs:

- WAVERLY: `ZARVECK`
- SOLO: `KETROVE`
- KURYAKIN: `VENTOR`

Page normalises each input (uppercase, `[A-Z0-9]` only), assembles
`P2P{ZARVECK_KETROVE_VENTOR}`, and SHA-256s against the embedded
`EXPECTED_FLAG_HASH = c3afb0cb75925055425bb29c6506e0ff23de7c6f2b0b0031b0e7b4e593a90ea1`.

**Combined flag: `P2P{ZARVECK_KETROVE_VENTOR}`** ✓

→ "✓ Combined flag confirmed. Submit P2P{ZARVECK_KETROVE_VENTOR} to the
Pwn2Play scoreboard."

---

## Summary

| Stage         | Recovered                  | Fragment    |
|---------------|----------------------------|-------------|
| Stage 0       | Entry: hidden "watch schedule" link → sked → section-iii | —    |
| WAVERLY       | `ROMAN ZARVECK SECURE` (OTP mod-10) | `ZARVECK` |
| SOLO          | `KETROVE` (CSS-redacted SUBJ span) + three Cyrillic key candidates | `KETROVE` |
| KURYAKIN      | `ВЕНТОР` (Vigenère, key `ЛЕНИН` from SOLO) → `VENTOR` | `VENTOR` |
| **Combined**  | **`P2P{ZARVECK_KETROVE_VENTOR}`**                  |          |

---

## Solver dependency graph

```
Stage 0 ──► Stage 1 (WAVERLY)   ──► fragment ZARVECK
        │
        ├─► Stage 2 (SOLO)      ──► fragment KETROVE
        │        │
        │        └─► gives key candidates {ЛЕНИН, СТАЛИН, ХРУЩЕВ}
        │                      │
        │                      ▼
        └─► Stage 3 (KURYAKIN) ──► fragment VENTOR
                              │
                              ▼
                          Stage 4 (combined) → P2P{ZARVECK_KETROVE_VENTOR}
```

SOLO is load-bearing: KURYAKIN cannot be solved without it. WAVERLY can be
solved in parallel with either of the other two; SOLO and KURYAKIN have a
strict order.

---

## Common player snags (anticipated)

- **Missing the hidden entry link.** Page reads as a normal educational
  tribute; players who scan rather than read may bounce. Fix in play: hover
  any plausible noun in the prose.
- **Brute-forcing KURYAKIN with the wrong key.** If a player tries
  СТАЛИН or ХРУЩЕВ first and sees gibberish, they may conclude the cipher
  isn't Vigenère. The "Period key not recovered locally" hint on the inbox
  is meant to nudge them to look elsewhere; if they don't, they may stall.
- **Entering Cyrillic at the workstation.** The combined-flag form strips
  non-`[A-Z0-9]` input, so Cyrillic gets silently dropped. The "Awaiting
  three fragments" message can mislead. Players must transliterate.
- **Audio: spoken English digits.** British voice, slow cadence, digits
  spoken one at a time. The "STATION X" self-identification is a Bletchley
  nod, not a clue. Transcription is straightforward; the only friction is
  catching the indicator (spoken twice, before the eight `BREAK`-separated
  body groups).
- **WAVERLY without a calculator.** Players expecting an auto-decoder will
  bounce off the empty notepad. The page provides materials and a scratch
  area — the math is theirs to do. Pen-and-paper or Python both work.
- **Trying to text-select the redactions.** Mouse-drag yields nothing
  (the `.redact` class sets `user-select: none`). Player must open DevTools
  to read the `data-c` attribute; the JS console one-liner is the fastest
  recovery path.
