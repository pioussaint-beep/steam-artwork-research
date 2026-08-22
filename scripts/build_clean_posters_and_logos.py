#!/usr/bin/env python3
"""
Clean STEAM Logos & Posters Catalog Builder
Strictly curate 112 Graphic Logos/Icons/Badges and 112 Graphic Posters/Blueprints/Infographics.
Filters out all photos of people, crowds, and raw space photography.
Extracts 5-color palettes and writes data/steam_items.json & js/data.js.
"""

import os
import json
import urllib.request
import urllib.parse
import ssl
from PIL import Image

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0'}

os.makedirs('data', exist_ok=True)
os.makedirs('images/logos', exist_ok=True)
os.makedirs('images/artwork', exist_ok=True)

print("Scaffold initialized.")
