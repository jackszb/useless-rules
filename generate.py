#!/usr/bin/env python3
import os
import json
import requests
from urllib.parse import urlparse

OUTPUT_DIR = "json"
RULES_FILE = "rules_list.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_domains_adguard(text):
    domains = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("!"):
            continue
        if line.startswith("||") and line.endswith("^"):
            domains.add(line[2:-1])
    return sorted(domains)

def filename_from_url(url):
    path = urlparse(url).path
    name = os.path.basename(path)
    if name.endswith(".txt"):
        name = name[:-4]
    name = name.replace("-", "_").replace(".", "_")
    return f"{name}.json"

def main():
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        urls = json.load(f)

    for url in urls:
        output = filename_from_url(url)
        print(f"Processing {url} → {output}")

        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        domains = extract_domains_adguard(resp.text)

        result = {
            "version": 3,
            "rules": [
                {
                    "domain_suffix": domains
                }
            ]
        }

        out_path = os.path.join(OUTPUT_DIR, output)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
