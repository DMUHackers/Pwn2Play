# Solve.md

# [Easy/Medium] Misc - Distributed Data - Solve Guide

## Overview

This challenge provides a broken torrent file.

The intended issue is that the torrent file has been edited or saved in a way that corrupts its original structure. Torrent files use bencoding, which is a strict binary-safe encoding format.

If the file is opened and edited with software that attempts to make the content human-readable, the bencoded structure can be damaged. This prevents torrent clients from parsing the file correctly.

## Initial Analysis

Start by inspecting the provided file type:

file challenge.torrent

If the torrent file is corrupted, a torrent client may reject it or fail to load it properly.

Torrent files are bencoded. A valid torrent file normally contains dictionary-style bencoded data, including fields such as:

- announce
- info
- name
- piece length
- pieces
- length

The `pieces` field is especially important because it contains binary SHA-1 hash data. If this binary data has been altered, escaped, reformatted, or made human-readable, the torrent will no longer work.

## Understanding the Issue

The challenge note indicates that editing the document with something that tries to make everything human-readable will corrupt the contents.

This means the file was likely modified by a text editor, pretty-printer, or tool that changed the raw bencoded byte stream.

Common corruption issues include:

- Added spaces
- Added newline characters
- Changed binary bytes
- Replaced raw bytes with escaped text
- Incorrect string lengths
- Human-readable formatting added to bencoded data

Because bencoding stores string lengths explicitly, even a small change can break parsing.

For example:
```
4:flag
```
means the next 4 bytes are the string `flag`.

If the content is changed but the length is not updated, the parser will fail.

## Method

The process is:

1. Inspect the torrent file in a hex editor or binary-safe editor.
2. Identify where the bencoded structure has been modified.
3. Repair the bencoding so the torrent file is valid again.
4. Save the file without changing binary content.
5. Open the repaired torrent file in a torrent client.
6. Download the flag file.

## Useful Tools

Useful tools for this challenge include:

- `file`
- `xxd`
- `hexdump`
- `bencode-tools`
- `transmission-show`
- `torrenttools`
- qBittorrent
- Transmission
- A hex editor such as HxD, Bless, or 010 Editor

## Checking the Torrent

Use a torrent inspection tool to check whether the file parses correctly:

transmission-show challenge.torrent

Or:

torrenttools show challenge.torrent

If the file is malformed, these tools should return an error indicating that the torrent metadata cannot be parsed.

## Repairing the File

Open the file in a binary-safe editor or hex editor.

Look for signs that the file has been made human-readable. This may include unexpected readable markers, added formatting, or broken bencoded lengths.

Once the corrupted section is corrected, save the file as a valid `.torrent` file.

Do not use a word processor or rich text editor. These may add formatting or change byte values.

## Loading the Torrent

After repairing the file, open it in a torrent client such as qBittorrent or Transmission.

Once the metadata is accepted, start the torrent and allow it to download the file.

The downloaded content should contain the flag.

## Key Finding

The challenge is not about cracking encryption or reversing a complex format. The core issue is that the `.torrent` file has been corrupted by unsafe editing.

Repairing the bencoded structure allows the torrent client to parse the file and download the flag.

## Flag
```
P2P{REDACTED}
```
## Lessons Learned

This challenge demonstrates the importance of preserving binary-safe file formats.

Torrent files may look partially readable, but they contain strict bencoded data and binary hash values. Editing them with normal text tools can corrupt the structure and make the file unusable.

The important steps were:

1. Recognise that the file is a corrupted torrent.
2. Understand that `.torrent` files use bencoding.
3. Avoid tools that rewrite or reformat binary data.
4. Repair the malformed bencoded structure.
5. Load the corrected torrent in a torrent client.
6. Retrieve the flag file.