import requests

url = "https://1drv.ms/u/c/8F247B1B46E82304/IQDlMaSTMyRJSLVeesO1cwjfAUihdhxgnpRyMiQB9Z1cv1s"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

try:
    response = requests.get(url, headers=headers, allow_redirects=True, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Final URL: {response.url}")
    print(f"Content Type: {response.headers.get('Content-Type')}")
    with open("response.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Saved response to response.html")
except Exception as e:
    print(f"Error: {e}")
