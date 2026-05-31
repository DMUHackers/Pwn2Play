# [Medium] Web - Local Matters of Inclusion

## Category
Web

## Difficulty
Medium (3 progressive levels)

## Author
x41x41x41 | JohnOP

## Description
This site includes all sorts but can you get the `/tmp/flag.txt`?

The challenge is split across three levels, each introducing an additional layer of filtering on the file inclusion parameter. All three levels share the same objective but require different bypass techniques.

## Objective
Exploit a Local File Inclusion (LFI) vulnerability in the `img` parameter of `images.php` to read the contents of `/tmp/flag.txt` on each of the three target instances.

## Provided Files
- **Level 1:** `http://lmi1.pwn2play.com/images.php?img=`
- **Level 2:** `http://lmi2.pwn2play.com/images.php?img=`
- **Level 3:** `http://lmi3.pwn2play.com/images.php?img=`

The LFI entry point can be identified via:
```
http://localhost:8000/images.php?img=/var/www/html/404hoodie.png
```

## Flag Format
P2P{...}

## Notes
- Each level adds a new input filter or path restriction — observe the server behaviour carefully before crafting your payload
- Level 1: No filters applied
- Level 2: Path must begin with the original directory (`/var/www/html/`)
- Level 3: Same as Level 2, but `../` sequences are stripped — however, stripping is **not** recursive
