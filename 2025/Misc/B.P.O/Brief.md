# Brief.md

# [Medium] Misc - B.P.O

## Category
Misc

## Difficulty
Medium

## Author
[T.A.R.S]

## Description

During restoration efforts at a decommissioned signals hut near Bletchley Park, a rusted field case was discovered beneath floorboards marked:

BPO - Confidential

Inside were a bundle of wartime documents, six damaged forensic artefacts, and a reel of encrypted radio traffic dated February 1944.

Curiously, the documents reference intercepted communications, but there is no clear indication of which cipher system was used. Some fragments bear marks resembling foreign equipment, while others show distinctly British nomenclature.

Your task is to reconstruct the original machine settings from the recovered artefacts and decrypt the intercepted transmission.

## Objective

Recover all required cipher machine settings from the six clues, then use them to decrypt the provided ciphertext.

## Provided Artefacts

The challenge contains six separate clues. Each clue reveals part of the final cipher configuration.

You will need to inspect multiple file types and extract hidden information from them, including audio, video, images, network captures, metadata, and encoded data.

## Ciphertext
```
MAOSU DOIER CHKZW IKTCE NBYOX
IFDMD XLWIO CREJZ NHBHS TPUIY
SGPFV GLLGM JEFDM CTNCS GNXPK
SNNRZ VFBVT UOCAX PHARJ EQHCR
OPHWM UUXIE
```
## Flag Format
```
P2P{...}
```
## Notes

This challenge is based around the Typex machine, a British rotor cipher machine derived from and improved upon the Enigma concept.

There are six clues in total:

- Five clues provide rotor settings
- One clue provides the plugboard fill

Each rotor setting follows this format:

Rotor, Ring Setting, Initial Value