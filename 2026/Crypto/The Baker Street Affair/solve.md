# THE BAKER STREET AFFAIR — Full Solve Walkthrough

## Stage 0 — Find the entry

The Baker Street Affair is not linked from `/projects/` or `/projects/pwn2play/`.
The only public-facing card on Pwn2Play shows the challenge name and a
"Locked until post-event" overlay; clicking it does nothing. Discovery is
seeded from `robots.txt`.

1. The Pwn2Play page (`/projects/pwn2play/`) lists `THE BAKER STREET AFFAIR`
   as a fourth 2026 card. The name is a hint, no link.

2. Visit `https://welbournesecurity.com/robots.txt`:

   ```
   User-agent: *
   Allow: /

   # Legacy operator traffic is not part of the public crawl surface.
   Disallow: /ops/traffic.txt

   # Cabinet Noir filing — bureau de lecture interne.
   Disallow: /cabinet-noir/
   ```

   Two intentionally-disallowed paths. The first is the legacy RAVEN GLASS
   entry; the second is new. Visit `https://welbournesecurity.com/cabinet-noir/`.

3. The Cabinet Noir filing-room page renders (manila folder, "ARCHIVES —
   BUREAU DE LECTURE INTERNE" stamp). The page presents **almost nothing**
   beyond:

   - Two short paragraphs of period French prose. The second contains the
     only cipher-name hint: *"par habitude prise du temps de **Polybe** …
     il garde le tableau dans la tête."* (he keeps the table in his head).
   - A single flat line of 17 digit pairs:

     ```
     12  11  25  15  42  43  44  42  15  15  44  11  21  21  11  24  42
     ```

   No grid printed. No row/column convention stated. No worked example.
   No word division. No instructions on what to do with the result.

4. **Recognise the cipher.** The French word *Polybe* names the
   *carré de Polybe* / Polybius square — a 5×5 substitution grid where
   each letter is addressed by two digits. The standard French Cabinet
   Noir / Nihilist convention is `ABCDE / FGHIK / LMNOP / QRSTU / VWXYZ`
   with `I` and `J` sharing cell `24`.

5. **Pick a convention.** Pair values run 1–5 in both digits, so both
   "row-first" and "column-first" are syntactically valid; the slip does
   not say which. The first pair on the line is `12`. Under row-first,
   `12` = row 1, col 2 = **B**. Under column-first, `12` = col 1, row 2 =
   **F**. Decoding the entire line under each convention:

   - **Row-first:** `BAKERSTREETAFFAIR`  ← real English noun phrase.
   - **Column-first:** `FBIRECTUTSCKQGQDR`  ← junk.

   The legibility of the row-first output is its own confirmation.

6. **Word-segment.** The 17-letter string `BAKERSTREETAFFAIR` parses
   unambiguously as `BAKER` + `STREET` + `AFFAIR` (matches the case-file
   title, which is the only public name of the challenge). Lowercase and
   hyphenate to produce a URL fragment: `baker-street-affair`.

7. **Mount at the site root.** Visit
   `https://welbournesecurity.com/baker-street-affair/`. The path mirrors
   the existing `/rg-1421z/` (RAVEN GLASS) and `/section-iii/` (CONCORDAT)
   entries — all three live as top-level enumeration paths, none under
   `/projects/`. Cover
   page (Cabinet Noir folder, stamped CONFIDENTIEL / VU INSP. GANIMARD)
   presents two document cards (Holmes case-note, Lupin letter) and a
   wax seal at the foot of the file.

| Pair | R-C | Letter |    | Pair | R-C | Letter |    | Pair | R-C | Letter |
|------|-----|--------|----|------|-----|--------|----|------|-----|--------|
| 12   | 1·2 | **B**  |    | 43   | 4·3 | **S**  |    | 11   | 1·1 | **A**  |
| 11   | 1·1 | **A**  |    | 44   | 4·4 | **T**  |    | 21   | 2·1 | **F**  |
| 25   | 2·5 | **K**  |    | 42   | 4·2 | **R**  |    | 21   | 2·1 | **F**  |
| 15   | 1·5 | **E**  |    | 15   | 1·5 | **E**  |    | 11   | 1·1 | **A**  |
| 42   | 4·2 | **R**  |    | 15   | 1·5 | **E**  |    | 24   | 2·4 | **I**  |
|      |     |        |    | 44   | 4·4 | **T**  |    | 42   | 4·2 | **R**  |

The discovery channel is intentionally different from the existing two
challenges: RAVEN GLASS uses `/ops/traffic.txt` + base64, CONCORDAT uses
a hidden in-prose link + `/ops/sked.txt` + base64. Baker Street is the
first to use a top-level `/cabinet-noir/` path, the first to use a
Polybius / carré-de-Polybe encoding, and the first whose entry page
gives no decode walkthrough — the player must recognise the cipher
from its name alone.

---

## Stage 1 — Holmes (Dancing Men cipher)

Visit `/baker-street-affair/holmes/`.

Period English-serif "case note" addressed to Watson, written in Holmes's
private "Cubitt dancers" cipher (Conan Doyle, *The Adventure of the Dancing
Men*, 1903). The prose is a Doyle pastiche; the actionable content is
two SVG panels:

### Legend (partial)

Six stick-figure dancers, one per letter, labelled in alphabetical order:

```
A    D    N    R    S    T
```

Each figure has a distinct arm/leg pose:
- `A` — arms straight horizontal, legs apart
- `D` — left arm up, right arm slanting down, legs apart
- `N` — both arms down-and-out at 30°, legs apart
- `R` — both arms swung to the right, one leg in stride
- `S` — arms down at sides, legs together (only figure with a single leg-line)
- `T` — arms up in a Y, legs apart

### The dancers (encoded message)

Six figures in sequence:

```
[S] [T] [R] [A] [N] [D-with-flag]
```

The sixth figure carries a small triangular flag in its right hand —
Doyle's canonical convention is that the flag denotes the **end of the
message**, not a separate letter. The flagged figure is still `D`.

### Fragment

Plaintext: **`STRAND`**.

This is Fragment H. (`STRAND` = the address of *The Strand Magazine*,
where Conan Doyle published every Holmes story between 1891 and 1927;
players who know the canon recognise the answer.)

No verifier on the page — player banks the fragment for Stage 3.

---

## Stage 2 — Lupin (Baconian italics)

Visit `/baker-street-affair/lupin/`.

A copperplate-handwriting letter from Arsène Lupin to "Mon très cher
Holmes —", on Hôtel Britannique letterhead. Eight body paragraphs and a
signature.

### Surface signal: acrostic (red herring)

The first letter of each of the seven body paragraphs spells out, in
order:

```
D · I · A · M · A · N · T
```

**`DIAMANT`** — French for *diamond*. Tempting; obvious; **wrong**. The
case is *not* about the diamond. The acrostic exists to bait players who
stop reading at first-letter level.

### Real signal: Baconian cipher in italic / roman

Body of the letter is set in Petit Formal Script (handwriting) so italic
and roman are visually indistinguishable inside the running text. But
one sentence — explicitly framed by the prose ("**Tenez, pour le règlement —**")
— is set in a different typeface entirely (IM Fell English, period
typeset). The lore note on the cover hints at this:

> "The hand is steady; the typesetting is not."

The framed sentence is:

```
« Voici six lettres pour vous bel amis. »
```

30 alphabetic characters. Each is either italic or roman:

| Pos | Char | Italic? | Bit |     | Pos | Char | Italic? | Bit |
|-----|------|---------|-----|-----|-----|------|---------|-----|
|  1  | V    | no      | A   |     | 16  | p    | no      | A   |
|  2  | o    | yes     | B   |     | 17  | o    | no      | A   |
|  3  | i    | yes     | B   |     | 18  | u    | yes     | B   |
|  4  | c    | yes     | B   |     | 19  | r    | no      | A   |
|  5  | i    | yes     | B   |     | 20  | v    | no      | A   |
|  6  | s    | no      | A   |     | 21  | o    | yes     | B   |
|  7  | i    | no      | A   |     | 22  | u    | no      | A   |
|  8  | x    | no      | A   |     | 23  | s    | no      | A   |
|  9  | l    | no      | A   |     | 24  | b    | yes     | B   |
| 10  | e    | yes     | B   |     | 25  | e    | no      | A   |
| 11  | t    | yes     | B   |     | 26  | l    | no      | A   |
| 12  | t    | no      | A   |     | 27  | a    | no      | A   |
| 13  | r    | no      | A   |     | 28  | m    | no      | A   |
| 14  | e    | no      | A   |     | 29  | i    | no      | A   |
| 15  | s    | yes     | B   |     | 30  | s    | yes     | B   |

Bit string: `ABBBB AAAAB BAAAB AABAA BAABA AAAAB`

Decode in standard Baconian (5-bit groups, `A=00000 B=00001 … Z=11011`):

| Group   | Letter |
|---------|--------|
| `ABBBB` | Q      |
| `AAAAB` | B      |
| `BAAAB` | S      |
| `AABAA` | E      |
| `BAABA` | T      |
| `AAAAB` | B      |

Recovered string: **`QBSETB`**.

This is Fragment L *as Lupin wrote it*.

### The "à rebours" step

Two lines after the framed sentence:

> *"Et je signe à rebours, comme toujours."*  
> *— Lupin, Arsène.*

Two flags pointing at reversal:
1. The line literally says "I sign in reverse, as always."
2. The signature is `Lupin, Arsène` — surname before given name — which
   is also "in reverse" compared to the canonical "Arsène Lupin".

Apply Lupin's standing convention: reverse the fragment.

`QBSETB` reversed → **`BTESBQ`**.

This is Fragment L *as it should be read*.

### Recovery path notes

Players who can verify italic via DOM inspection (DevTools → check each
character's `font-style`) get a confirmed bit pattern. Players reading
visually need to spot the typeface change first, then count carefully;
the IM Fell English italic is unambiguously slanted vs the upright roman.

---

## Stage 3 — Reconcile

Now hold both fragments side by side:

| Fragment | Origin           | Value     |
|----------|------------------|-----------|
| H        | Dancing Men      | `STRAND`  |
| L        | Baconian italics | `BTESBQ`  |

Both fragments are 6 letters. Same length is the giveaway: one is a
Vigenère key, the other is the ciphertext.

Which is which? The cover gives **no format hint**. The Stage 2 Baconian
sentence is set in cold typeset (the "shape" Lupin writes for, not
against), and Holmes's note is written deliberately in a private hand
he names ("the figures are her husband's, not mine") — Stage 1's
output is therefore the *standing form*, the constant. Vigenère keys
are constants; ciphertexts are the message. **`STRAND` is the key,
`BTESBQ` is the ciphertext.**

### Vigenère decryption

`P[i] = (C[i] − K[i] + 26) mod 26` with `A=0..Z=25`.

| i | C  | C idx | K  | K idx | (C − K + 26) mod 26 | P  |
|---|----|-------|----|-------|---------------------|----|
| 1 | B  | 1     | S  | 18    | 9                   | J  |
| 2 | T  | 19    | T  | 19    | 0                   | A  |
| 3 | E  | 4     | R  | 17    | 13                  | N  |
| 4 | S  | 18    | A  | 0     | 18                  | S  |
| 5 | B  | 1     | N  | 13    | 14                  | O  |
| 6 | Q  | 16    | D  | 3     | 13                  | N  |

Plaintext: **`JANSON`**.

### From recovered word to flag

`JANSON` alone is not the flag. Out of context, the word is meaningless.
Two things on the case file route the player to its referent:

1. **Lupin's letter** (Stage 2 prose): *"…un certain jeune homme studieux
   dont je ne dirai pas le nom, et qui se croit, pauvre enfant, sur le
   point de me prendre."* This is Lupin's standing taunt about the young
   detective who pursues him through *L'Aiguille creuse* (1909).
2. **The cover's reader-notes** (rule iii): the affair returns
   *"a place, ordinary enough that the Préfecture filed it under a
   registry index and forgot it; ordinary enough that the young man in
   Lupin's hand — the one he does not name — walked into it every
   morning for six years."*

The "young man" is **Isidore Beautrelet** of *L'Aiguille creuse*. The
place he walked into every morning is the lycée he attends throughout
the novel: **Lycée Janson-de-Sailly**, 106 rue de la Pompe, Paris XVIᵉ
(opened 1884, named for the philanthropist Alexandre Janson de Sailly).

The recovered cipher word `JANSON` names the lycée; the lycée is what
the recovered word *means*.

### Wrap as flag

Pwn2Play house format: uppercase tokens, underscore-separated, wrapped
in `P2P{…}`. The site itself gives **no wrap hint** — this is a deliberate
break from the RAVEN GLASS / CONCORDAT pattern where the flag form was
telegraphed on the verifier UI.

**`P2P{LYCEE_JANSON_DE_SAILLY}`** — the primary flag.

(Note: `LYCEE` written without the acute on the `É`, matching the
Pwn2Play convention of ASCII-only flag content. Hyphen in
"Janson-de-Sailly" becomes underscore, also per house format.)

---

## Stage 4 — The wax seal (bonus tier — Cabinet Noir verdict)

The cover page renders a deep crimson wax seal at the foot of the file
labelled `CABINET NOIR · PARIS · 1908 · Bureau de Lecture`. Two notes
prime the player:

> "Cabinet Noir clerks routinely slipped a transcription précis behind
> the wax of dossiers they considered politically inconvenient."

> Rule iv. on the cover: "The wax seal at the foot of this file is —
> as M. Ganimard noted in the margin — *not for ornament*."

The seal is downloadable: `/baker-street-affair/src/seal.png`.

### What it is

`seal.png` is a 200×200 PNG with an extra `tEXt` ancillary chunk
spliced before the `IEND`. The chunk's keyword is `Slip`; the value is
a Latin-1-encoded transcription slip.

PNG decoders ignore unrecognised text chunks → the image renders
normally. Any tool that reads PNG metadata extracts the slip.

### Extraction paths

Fastest:
```bash
exiftool seal.png | grep -i slip
```

Or:
```bash
pngcheck -t -v seal.png
```

Or the lowest-tech path:
```bash
strings seal.png | grep -i CABINET
```

(The IDAT compressed stream returns garbled bytes; the `tEXt` chunk is
plaintext and `strings` surfaces it cleanly.)

Or with Python:
```python
from PIL import Image
img = Image.open("seal.png")
print(img.info.get("Slip"))
```

### The slip

```
CABINET NOIR -- INTERCEPT TRANSCRIPTION SLIP
Dossier No. 1908-VII-19  -  Confidentiel  -  Bureau de Lecture

Source: Hotel des Postes (Paris) -- wax-seal extraction, 19 July 1908
Routing: Prefecture de Police, Service de la Surete (cote retiree)

OBSERVATION (Inspecteur Ganimard, en marge):

  "L'affaire du diademe n'est qu'un leurre. Pendant que le bon
  Mr. Holmes court derriere une boucle d'oreille a Londres,
  notre ami s'installe dans la falaise creuse d'Etretat -- et
  ce qu'il y derobe n'est pas un bijou pris a une duchesse, mais
  le tresor amasse par tous les rois de France depuis Charles VII."

VERDICT (signe Ganimard):

  Le diademe          : recuperation secondaire, theatre pour Holmes.
  La cible veritable  : LE TRESOR DES ROIS.

The diadem was the stage; the kings' treasure was the act.

Submit verdict flag:  P2P{LE_TRESOR_DES_ROIS}
```

The slip names the larger crime Lupin was misdirecting from:
**`P2P{LE_TRESOR_DES_ROIS}`** — the bonus flag.

(Canon reference: the *Aiguille creuse* at Étretat was, in Leblanc,
the royal treasury of France from Charles VII through Louis XVI,
hidden in the chalk needle off the Normandy coast.)

---

## Summary

| Stage          | Recovered                              | Flag                          |
|----------------|----------------------------------------|-------------------------------|
| Stage 0        | Entry: `robots.txt` → `/cabinet-noir/` → recognise `Polybe` → standard 5×5 grid → row-first → 17 letters → segment as BAKER/STREET/AFFAIR → `baker-street-affair` | — |
| Stage 1        | `STRAND` (Dancing Men, 6 figures + flag) | Fragment H |
| Stage 2        | `QBSETB` (Baconian italics, IM Fell English blockquote) | Fragment L (Lupin's form) |
| Stage 3        | Reverse → `BTESBQ`; Vigenère decrypt with key `STRAND` → `JANSON`; map via Lupin's "young man" → **Lycée Janson-de-Sailly** | **`P2P{LYCEE_JANSON_DE_SAILLY}`** |
| Stage 4 (bonus)| Extract `tEXt` chunk from `seal.png` → slip → verdict | **`P2P{LE_TRESOR_DES_ROIS}`** |

---

## Solver dependency graph

```
Stage 0 ──► Stage 1 (Holmes / Dancing Men)  ──► fragment STRAND
        │
        ├─► Stage 2 (Lupin / Baconian)       ──► fragment QBSETB
        │                                          │
        │                                          ▼
        │                          (Lupin "à rebours" reversal)
        │                                          │
        │                                          ▼
        └─► Stage 3 (Vigenère reconciliation)  ──► JANSON
                                                   │
                                                   ▼
                                  (canon recognition: Beautrelet's lycée)
                                                   │
                                                   ▼
                                  P2P{LYCEE_JANSON_DE_SAILLY}

Stage 4 (parallel, independent of Stages 1-3):
   /baker-street-affair/src/seal.png
            │  (PNG tEXt chunk extraction)
            ▼
   Cabinet Noir slip → P2P{LE_TRESOR_DES_ROIS}
```

Stage 1 and Stage 2 are parallel; Stage 3 requires both. Stage 4 (the
bonus) is fully independent — players can solve the wax-seal stego
without ever decoding the cipher chain, and vice versa.

---

## Common player snags (anticipated)

- **Missing `robots.txt` as a discovery surface.** Players who haven't
  solved RAVEN GLASS first may not think to inspect `robots.txt`. The
  Baker Street card on Pwn2Play is the only other visible signpost, and
  it deliberately reveals nothing. Expected bounce rate is real; this is
  a launcher card, not a tutorial. Players who *have* solved RAVEN GLASS
  know to check `robots.txt` and will see the second `Disallow:` line.

- **Trying to base64-decode the Polybius coordinates.** Players who
  reached Baker Street via the RAVEN GLASS or CONCORDAT pattern may
  reflexively try base64 first. Base64 produces nothing useful on a
  flat-spaced digit string. The only cipher hint on the slip is the
  single French word *Polybe*, dropped into a sentence about old habits
  — the player must recognise it as the cipher name and look up the
  standard layout themselves. **No grid is printed.**

- **Column-first vs row-first ambiguity.** Standard Polybius variants
  disagree on order, and the slip says nothing. Decoding under
  column-first yields `FBIRECTUTSCKQGQDR` — garbled. Decoding under
  row-first yields `BAKERSTREETAFFAIR` — three English words. The
  legibility is the player's only confirmation. Players who do not
  notice the word break and try the unsegmented string
  `/bakerstreetaffair/` get a 404. Players who guess
  `/projects/baker-street-affair/` (an over-correction — the slip says
  *Bureau de Lecture / Cabinet Noir filing*, not *portfolio project*)
  also get a 404; the path is at the site root, like `/rg-1421z/` and
  `/section-iii/`.

- **Re-segmenting `BAKERSTREETAFFAIR`.** Some players see `BAKERS` +
  `TREET` + `AFFAIR` or `BAKE` + `RSTREET` + `AFFAIR` and bounce on a
  404. The challenge's only public name is "The Baker Street Affair";
  the segmentation matches that name. The Pwn2Play card title is the
  tiebreaker.

- **Falling for the DIAMANT acrostic.** The acrostic spells the obvious
  Belle-Époque jewel-theft word in French. Players who stop there will
  try `P2P{DIAMANT}`, `P2P{THE_DIAMANT_NEEDLE}`, `P2P{DIAMOND}` etc.
  and bounce. The lore deliberately frames the diadem as a decoy —
  re-reading the cover ("the diamonds were not the issue") nudges
  toward the typeset blockquote.

- **Not recognising the typeface change.** The IM Fell English
  blockquote is visually distinct from the surrounding Petit Formal
  Script handwriting. Players who skim may miss the typeface signal.
  The lore line "the hand is steady; the typesetting is not" is the
  diegetic hint.

- **Counting italic-vs-roman in the wrong font.** Petit Formal Script
  has no real italic variant — browsers render synthesised italics
  visually identical to roman in this font. Players who try to count
  the italic pattern inside the handwriting body get junk. Only the
  IM Fell English blockquote is the carrier; that's the whole point of
  the typeface switch.

- **Forgetting the "à rebours" reversal.** Vigenère decryption of the
  un-reversed `QBSETB` with key `STRAND` produces gibberish: `Y X N S O N`.
  Players may conclude the cipher is something else. The two reversal
  hints are inside Lupin's letter (signature "Lupin, Arsène" with
  surname-first and the explicit "je signe à rebours" line); the cover
  no longer telegraphs it.

- **Trying the cipher in the wrong direction.** Players who use `QBSETB`
  as the *key* and `STRAND` as the ciphertext get a non-word. Both
  fragments are 6 letters, so length alone doesn't disambiguate. The
  cover's rule i hints — *"the shape of one is the key to the other;
  the shape of the other, when read in the writer's manner, is what
  the key opens"* — that Holmes's fragment is the constant (the shape)
  and Lupin's, once reversed (read in *his* manner), is what opens.

- **Stopping at `JANSON`.** The cipher chain returns `JANSON` and the
  cover gives no wrapper hint. Players who recognise the name
  immediately (Leblanc readers) jump straight to the lycée; players
  who do not must trace Lupin's letter clue *"un certain jeune homme
  studieux dont je ne dirai pas le nom"* → Beautrelet → his school.
  Players who do neither will try `P2P{JANSON}` or `P2P{JANSON_DE_SAILLY}`
  and bounce against the Pwn2Play scoreboard. **The canonical school
  name is `LYCEE_JANSON_DE_SAILLY`**, founded 1881, still open at 106
  rue de la Pompe.

- **Trying to text-select the encoded blockquote.** Mouse-drag works
  and returns the literal sentence including `«` and `»`. The italic
  formatting is not preserved on copy — players must inspect the DOM
  via DevTools to confirm each character's italic state.

- **Missing the wax seal entirely.** The seal is at the bottom of the
  cover page, listed under "File seal" with a download link
  (`<a href="./src/seal.png" download>`). Players who solve the primary
  cipher and submit may not realise there's a bonus tier. The cover's
  rule iv. ("not for ornament") is the strongest hint.

- **Treating the seal as a normal image.** Right-click → Save As gives
  a valid PNG; opening it shows the seal. No visible hint of the slip.
  Players need to inspect the bytes — `exiftool`, `pngcheck -tv`,
  `strings`, `binwalk`, or a hex editor all work.

- **Looking for a PNG/ZIP polyglot.** The naming and the "vessel, not
  image" framing might suggest a PKZIP signature appended. There is no
  ZIP — the bonus is in a standard PNG ancillary `tEXt` chunk. Any PNG
  metadata reader extracts it.
