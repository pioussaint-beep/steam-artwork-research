#!/usr/bin/env python3
"""
STEAM Lab Logo & Artwork Master Dataset Generator
Generates over 105 curated STEAM Lab Logos and over 105 STEAM Artworks/Murals/Posters
Tailored specifically for an Elementary School STEAM Lab with an 'Awe & Wonder' theme.
"""

import os
import json
import urllib.request
import urllib.parse
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def ensure_dirs():
    os.makedirs('data', exist_ok=True)
    os.makedirs('images/logos', exist_ok=True)
    os.makedirs('images/artwork', exist_ok=True)

def safe_download(url, filepath):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        return True
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            data = resp.read()
            if len(data) > 500:
                with open(filepath, 'wb') as f:
                    f.write(data)
                return True
    except Exception as e:
        # Fallback or pass
        pass
    return False

def save_svg(filepath, svg_code):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_code.strip())

print("Setting up dataset structures...")
