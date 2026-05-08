# Solve.md

# [Medium] Misc - B.P.O - Solve Guide

## Overview

This challenge is based around the Typex machine, a British rotor cipher machine that acted as a five-rotor upgraded counterpart to the German Enigma machine.

The challenge provides six clues. These correspond to five rotor settings and one plugboard fill.

Once all six pieces are recovered, the ciphertext can be decrypted using a Typex implementation, such as the Typex operation in CyberChef.

Each rotor setting is in the following format:

Rotor, Ring Setting, Initial Value

## Recovered Configuration
```
Rotor 1: VIII, Z, X
Rotor 2: II, A, X
Rotor 3: IV, A, A
Rotor 4: VI, J, L
Rotor 5: V, S, P
```
Plugboard:
```
QWGBUJXLMVETPYKHCNZORDAFSI
```
## Clue 1 - Rotor 1

The first clue is an audio file hidden inside an MP4 video file.

Extract the audio from the video, then open it in Audacity. Switch the view to spectrogram mode.

The rotor setting becomes visible in the spectrogram:
```
VIII, Z, X
```
This gives:
```
Rotor 1: VIII, Z, X
```
## Clue 2 - Rotor 2

The second clue is an image transferred between two machines inside a `.pcap` file.

After extracting the transferred file from the packet capture, the image does not open correctly because it has a malformed header.

Repair the image header, then open the recovered image. The image reveals the second rotor setting:
```
II, A, X
```
This gives:
```
Rotor 2: II, A, X
```
## Clue 3 - Rotor 3

The third clue is a text file that has been encoded into an image.

Each byte of the original text file has been written into the RGB values of the image. To reverse this, read the image pixel data, flatten the RGB values, and write those values back out as bytes.

Use the following Python script:

```python
import numpy as np
from PIL import Image

input_image = "encoded_image.png"
output_file = "decoded.txt"

img = Image.open(input_image)
rgb_array = np.array(img)
flattened_rgb = rgb_array.flatten()

decoded_bytes = bytearray()

for i in range(0, len(flattened_rgb), 3):
    decoded_bytes.append(flattened_rgb[i])      # Red channel
    decoded_bytes.append(flattened_rgb[i + 1])  # Green channel
    decoded_bytes.append(flattened_rgb[i + 2])  # Blue channel

decoded_bytes = decoded_bytes.rstrip(b"\x00")

with open(output_file, "wb") as f:
    f.write(decoded_bytes)

print(f"Decoded text saved as {output_file}")
```

The decoded text reveals:
```
IV, A, A
```
This gives:
```
Rotor 3: IV, A, A
```
## Clue 4 - Rotor 4

The fourth clue is hidden in the EXIF metadata of an image.

Inspect the image metadata using a tool such as `exiftool`:

```bash
exiftool image.jpg
```

A Base64 string is hidden in the metadata. Decode the Base64 value to recover the rotor setting:
```
VI, J, L
```
This gives:
```
Rotor 4: VI, J, L
```
## Clue 5 - Rotor 5

The fifth clue is hidden in a video subtitle.

The subtitle flashes on screen for approximately `0.001` seconds, making it very difficult to see during normal playback.

Inspect the subtitle track or extract the subtitle file from the video. The subtitle reveals:
```
V, S, P
```
This gives:
```
Rotor 5: V, S, P
```
## Clue 6 - Plugboard Fill

The sixth clue provides the plugboard fill.

The file appears to be a `.jpeg`, but running the `file` command shows that it is actually a ZIP archive:

```bash
file clue6.jpeg
```

Rename the file from `.jpeg` to `.zip`:

```bash
mv clue6.jpeg clue6.zip
```

The ZIP archive is password protected. An accompanying `message.txt` points towards the password:
```
wecomeunseen
```
This is a reference to the Submarine Service motto.

After extracting the archive, a Morse code `.wav` file is recovered. Decode the Morse audio to reveal the plugboard fill:
```
QWGBUJXLMVETPYKHCNZORDAFSI
```
## Typex Decryption

With all rotor settings and the plugboard fill recovered, configure the Typex machine as follows:
```
Rotor 1: VIII, Z, X
Rotor 2: II, A, X
Rotor 3: IV, A, A
Rotor 4: VI, J, L
Rotor 5: V, S, P
```
Plugboard:
```
QWGBUJXLMVETPYKHCNZORDAFSI
```
Then decrypt the ciphertext:
```
MAOSU DOIER CHKZW IKTCE NBYOX
IFDMD XLWIO CREJZ NHBHS TPUIY
SGPFV GLLGM JEFDM CTNCS GNXPK
SNNRZ VFBVT UOCAX PHARJ EQHCR
OPHWM UUXIE
```
The plaintext is:
```
SOMET IMESI TISTH EPEOP LETHA TNOBO DYIMA GINES ANYTH INGOF THATD OTHET HINGS NOBOD YCANI MAGIN ETHEF LAGIS TYPEX BLETC HLEYC OVERT
```
Reformatted, this reads:
```
SOMETIMES IT IS THE PEOPLE THAT NOBODY IMAGINES ANYTHING OF THAT DO THE THINGS NOBODY CAN IMAGINE THE FLAG IS TYPEX BLETCHLEY COVERT

The flag is therefore:

P2P{TYPEXBLETCHLEYCOVERT}
```
## Flag
```
P2P{TYPEXBLETCHLEYCOVERT}
```