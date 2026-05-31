# Solve.md

# [Easy] Misc - BIKINI State: RED - Solve Guide

## Overview

BIKINI State: RED is an OSINT, web enumeration, and mapping challenge themed around the Royal Observer Corps.

Players begin at:

```text
https://welbournesecurity.com/
```

The aim is to find a hidden control panel, download three ROC post reports, correct the recorded bearings, triangulate the final location using the ROC Network page, and build the final flag.

Final flag:

```text
P2P{HOLMPTON_THE_HOLE}
```

## Solve Walkthrough

### Step 1: Check the starting website

The challenge prompt points players towards:

```text
https://welbournesecurity.com/
```

It also hints at a hidden control panel:

```text
First step, where did I leave that pesky control panel... somewhere on https://welbournesecurity.com/ I believe
```

This suggests basic web enumeration.

Check the site’s `robots.txt` file:

```text
https://welbournesecurity.com/robots.txt
```

This reveals:

```text
/opt/traffic.txt
```

### Step 2: Inspect the hidden traffic file

Open the discovered file:

```text
https://welbournesecurity.com/opt/traffic.txt
```

It contains the Base64 value:

```text
cmctMTQyMXo=
```

Decode it:

```bash
echo "cmctMTQyMXo=" | base64 -d
```

Decoded output:

```text
rg-1421z
```

This gives the hidden route:

```text
https://welbournesecurity.com/rg-1421z/
```

### Step 3: Download the ROC post reports

The hidden control panel provides three reports:

```text
REPORT_A_TUNSTALL_55.txt
REPORT_B_KEYINGHAM_56.txt
REPORT_C_SKIRLAUGH_57.txt
```

Each report contains a GZI flash bearing and a GZI card error.

The TRUE bearing is calculated as:

```text
TRUE bearing = GZI flash bearing + GZI card error
```

### Step 4: Calculate the TRUE bearings

From Post 55, Tunstall:

```text
149.6 + 1.2 = 150.8
```

From Post 56, Keyingham:

```text
98.8 + 0.8 = 99.6
```

From Post 57, Skirlaugh:

```text
129.4 + (-1.1) = 128.3
```

The corrected TRUE bearings are:

```text
Tunstall  : 150.8 degrees
Keyingham : 99.6 degrees
Skirlaugh : 128.3 degrees
```

### Step 5: Triangulate the location

Open the ROC Network page:

```text
https://welbournesecurity.com/projects/roc-network/
```

Select or locate the three ROC posts:

```text
Tunstall
Keyingham
Skirlaugh
```

Enter the corrected TRUE bearings:

```text
Tunstall  : 150.8
Keyingham : 99.6
Skirlaugh : 128.3
```

The tool calculates the final GPS coordinate:

```text
53.684069966006874, 0.06750168441000179
```

This points to:

```text
RAF Holmpton
```

### Step 6: Build the flag

The RAF Holmpton nickname is:

```text
"The Hole"
```

The flag format is:

```text
P2P{NAME_NICK_NAME}
```

Using:

```text
NAME  = Holmpton
NICKNAME = "The Hole"
```

The final flag is:

```text
P2P{HOLMPTON_THE_HOLE}
```