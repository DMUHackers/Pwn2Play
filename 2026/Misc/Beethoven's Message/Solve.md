# [Easy] Misc - Beethoven's Message - Solve Guide

## Overview
A provided audio file plays a sequence of piano notes. Each note maps directly to a letter of the alphabet (A through G), and the full sequence spells out the flag. The challenge requires identifying the note names in order — either by ear, or by using a pitch detection tool.

## Initial Analysis
The challenge description references a "scattered sequence of tones" intended for "a single recipient who would understand what others could not." Combined with the flag format `P2P{MESSAGE}` and the musical theme, the encoding is straightforward: musical note names (A, B, C, D, E, F, G) are used as characters.

The flag `P2P{EGGBEEBADGE}` confirms this — every character in the plaintext is a valid note name (A–G), and the full message is read directly from the note sequence in the audio.

## Enumeration / Inspection
Load the audio file and inspect it:

- Listen for a series of distinct, separated piano tones
- Each tone corresponds to one note and one letter of the flag
- The notes are played sequentially — no chords or overlapping tones to decode

Visualising the audio in a tool like Audacity or Sonic Visualiser can help separate notes and confirm the sequence, particularly if tones are close together.

## Method
- **Encoding:** Musical note names (A–G) used as a direct character substitution
- **Technique:** Pitch detection — either by ear, or using automated tools — to identify each note name in sequence

## Exploitation / Decryption / Solution Steps

### Step 1 — Obtain the audio file

Download or extract the provided audio file from the challenge.

### Step 2 — Identify the notes

**Option A — By ear:**

Listen to the audio and identify each piano note by pitch. If you have a reference instrument or a piano keyboard app, play along to match each tone. Write down the note names in order.

**Option B — Automated pitch detection (recommended):**

Use a tool to detect and label pitches automatically.

*Using `aubiooNotes` (CLI):*
```bash
sudo apt install aubio-tools
aubionotes -i beethoven.mp3
```
Output lists detected onset times and MIDI note numbers. Convert MIDI note numbers to note names (e.g. MIDI 64 = E4, MIDI 67 = G4).

*Using Sonic Visualiser (GUI):*
1. Open the audio file in [Sonic Visualiser](https://www.sonicvisualiser.org/)
2. Add a layer: `Layer > Add Note Layer`
3. Use the `Transform > Analyse > Note Tracker` plugin to label pitches
4. Read off the note names in sequence

*Using an online tool:*
- Upload the file to a browser-based pitch detector such as [musicnotes.com](https://www.musicnotes.com/) or a MIDI converter, then read the resulting note sequence

*Using Python (`librosa`):*
```python
import librosa
import numpy as np

y, sr = librosa.load('beethoven.mp3')
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

# Extract dominant pitch per frame
for t in range(pitches.shape[1]):
    index = magnitudes[:, t].argmax()
    pitch = pitches[index, t]
    if pitch > 0:
        note = librosa.hz_to_note(pitch)
        print(note)
```

### Step 3 — Assemble the flag

Read the note names in sequence, discarding octave numbers (e.g. `E4` → `E`). Concatenate the letters to form the message and wrap in the flag format.

**Note sequence:** `E, G, G, B, E, E, B, A, D, G, E`

**Flag:** `P2P{EGGBEEBADGE}`

## Commands Used

```bash
# Install aubio note detection tools
sudo apt install aubio-tools

# Detect notes from audio file
aubionotes -i beethoven.mp3

# Python pitch detection (requires librosa)
pip install librosa
python3 solve.py
```

## Scripts Used

```python
# solve.py — extract note sequence from audio
import librosa
import numpy as np

y, sr = librosa.load('beethoven.mp3')
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

notes = []
prev = None
for t in range(pitches.shape[1]):
    index = magnitudes[:, t].argmax()
    pitch = pitches[index, t]
    if pitch > 0:
        note = librosa.hz_to_note(pitch)[0]  # Strip octave number
        if note != prev:                      # Deduplicate held notes
            notes.append(note)
            prev = note

print("Note sequence:", notes)
print("Flag: P2P{" + "".join(notes) + "}")
```
