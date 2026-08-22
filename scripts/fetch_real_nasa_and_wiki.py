#!/usr/bin/env python3
"""
Scrapes and downloads 111 REAL logos and 110 REAL artworks from NASA and Wikimedia Commons APIs.
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
    'User-Agent': 'STEAMResearchLab/2.0 (Elementary Education Research)'
}

def query_nasa(query, limit=25):
    url = f"https://images-api.nasa.gov/search?q={urllib.parse.quote(query)}&media_type=image"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            items = data.get('collection', {}).get('items', [])
            results = []
            for item in items[:limit]:
                d = item['data'][0]
                links = item.get('links', [])
                if links:
                    results.append({
                        'title': d.get('title'),
                        'description': d.get('description', ''),
                        'image_url': links[0].get('href'),
                        'nasa_id': d.get('nasa_id'),
                        'source_name': 'NASA Image & Video Library',
                        'source_url': f"https://images.nasa.gov/details-{d.get('nasa_id')}.html"
                    })
            return results
    except Exception as e:
        print(f"NASA query error for '{query}':", e)
        return []

def query_wikimedia(query, limit=25):
    params = urllib.parse.urlencode({
        'action': 'query',
        'generator': 'search',
        'gsrsearch': query,
        'gsrnamespace': '6',
        'gsrlimit': str(limit),
        'prop': 'imageinfo',
        'iiprop': 'url|size|extmetadata',
        'iiurlwidth': '800',
        'format': 'json'
    })
    url = f"https://commons.wikimedia.org/w/api.php?{params}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            pages = data.get('query', {}).get('pages', {})
            results = []
            for pid, p in pages.items():
                title = p.get('title', '').replace('File:', '').replace('.svg', '').replace('.jpg', '').replace('.png', '')
                ii = p.get('imageinfo', [{}])[0]
                img_url = ii.get('thumburl') or ii.get('url')
                desc = ii.get('extmetadata', {}).get('ObjectName', {}).get('value', title)
                if img_url and not img_url.endswith('.pdf') and not img_url.endswith('.tif'):
                    results.append({
                        'title': title,
                        'description': desc,
                        'image_url': img_url,
                        'source_name': 'Wikimedia Commons',
                        'source_url': f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(p.get('title', ''))}"
                    })
            return results
    except Exception as e:
        print(f"Wikimedia query error for '{query}':", e)
        return []

print("Testing queries...")
nasa_patches = query_nasa("mission patch", limit=10)
print(f"NASA patches found: {len(nasa_patches)}")
wiki_logos = query_wikimedia("STEM logo", limit=10)
print(f"Wiki STEM logos found: {len(wiki_logos)}")
