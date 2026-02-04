import urllib.request
import urllib.error

url = "https://1drv.ms/u/c/8F247B1B46E82304/IQDlMaSTMyRJSLVeesO1cwjfAUihdhxgnpRyMiQB9Z1cv1s"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=30) as response:
        print(f"Status: {response.getcode()}")
        print(f"Final URL: {response.geturl()}")
        content = response.read().decode('utf-8')
        with open("response.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Saved response to response.html")
except Exception as e:
    print(f"Error: {e}")
