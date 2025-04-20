"""
crawler.py
Read URLs from urls.txt, fetch each page with browser‑like headers,
extract main text, and save to Data/<n>.txt
"""
import os
import requests
from bs4 import BeautifulSoup

URL_FILE = "urls.txt"
DATA_DIR = "Data"
RAW_DIR = "Raw"
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/123.0 Safari/537.36"),
    "Accept-Language": "en-US,en;q=0.9",
}
TIMEOUT = 10


def read_urls(path):
    """Return a list of non‑empty lines."""
    with open(path, encoding="utf-8") as f:
        return [u.strip() for u in f if u.strip()]


def extract_text(html: str) -> str:
    """Strip scripts/styles and join all <p> tag text."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return "\n".join(p.get_text(" ", strip=True) for p in soup.find_all("p"))


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    urls = read_urls(URL_FILE)
    for idx, url in enumerate(urls):
        try:
            print(f"[+] Fetching ({idx}) {url}")
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            html = r.text
        except Exception as e:
            print(f"[-] Failed to fetch {url}: {e}")
            continue

        raw_path = os.path.join(RAW_DIR, f"{idx}.html")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(html)

        txt_path = os.path.join(DATA_DIR, f"{idx}.txt")
        text = extract_text(html)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"[+] Saved → {raw_path}  &  {txt_path}")


if __name__ == "__main__":
    main()