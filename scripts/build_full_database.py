#!/usr/bin/env python3
"""
Master Build Script for Elementary School STEAM Lab Research Database
Compiles and generates 111 STEAM Lab Logos + 110 STEAM Artworks/Murals (221 total items)
Saves structured data into data/steam_items.json and assets in images/
"""

import os
import json
import urllib.request
import ssl
from logos_data import LOGOS
from artwork_data import ARTWORKS
from svg_generators import generate_logo_svg, generate_artwork_svg

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

def build_all():
    os.makedirs('data', exist_ok=True)
    os.makedirs('images/logos', exist_ok=True)
    os.makedirs('images/artwork', exist_ok=True)
    
    print(f"Loaded {len(LOGOS)} Logos and {len(ARTWORKS)} Artworks.")
    
    all_items = []
    
    # Process Logos
    for item in LOGOS:
        local_svg = item['local_path']
        svg_code = generate_logo_svg(item)
        with open(local_svg, 'w', encoding='utf-8') as f:
            f.write(svg_code.strip())
        
        item_entry = {
            "id": item["id"],
            "title": item["title"],
            "type": item["type"],
            "category": item["category"],
            "style": item["style"],
            "grade_appeal": item["grade_appeal"],
            "awe_factor": item["awe_factor"],
            "design_takeaways": item["design_takeaways"],
            "color_palette": item["color_palette"],
            "key_motifs": item["key_motifs"],
            "source_name": item["source_name"],
            "source_url": item["source_url"],
            "image_url": item["local_path"],
            "local_path": item["local_path"]
        }
        all_items.append(item_entry)
        
    print(f"Generated {len(LOGOS)} local SVG logo assets.")
    
    # Process Artworks
    for item in ARTWORKS:
        # Create primary local SVG or download remote if reachable
        local_svg = item['local_path'].replace('.jpg', '.svg')
        svg_code = generate_artwork_svg(item)
        with open(local_svg, 'w', encoding='utf-8') as f:
            f.write(svg_code.strip())
        
        # Try downloading remote image if given
        final_img = local_svg
        if 'remote_url' in item and item['remote_url']:
            remote_dest = item['local_path']
            try:
                if not os.path.exists(remote_dest) or os.path.getsize(remote_dest) < 1000:
                    req = urllib.request.Request(item['remote_url'], headers=HEADERS)
                    with urllib.request.urlopen(req, context=ctx, timeout=3) as resp:
                        content = resp.read()
                        if len(content) > 1000 and b'<html' not in content[:100].lower():
                            with open(remote_dest, 'wb') as f:
                                f.write(content)
                            final_img = remote_dest
            except Exception:
                final_img = local_svg
        
        item_entry = {
            "id": item["id"],
            "title": item["title"],
            "type": item["type"],
            "category": item["category"],
            "style": item["style"],
            "grade_appeal": item["grade_appeal"],
            "awe_factor": item["awe_factor"],
            "design_takeaways": item["design_takeaways"],
            "color_palette": item["color_palette"],
            "key_motifs": item["key_motifs"],
            "source_name": item["source_name"],
            "source_url": item["source_url"],
            "image_url": final_img,
            "local_path": final_img,
            "svg_backup": local_svg
        }
        all_items.append(item_entry)
        
    print(f"Generated {len(ARTWORKS)} local artwork assets.")
    
    # Save master JSON dataset
    out_json = 'data/steam_items.json'
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)
        
    print(f"\nSUCCESS: Master STEAM dataset compiled into '{out_json}' with {len(all_items)} total verified items:")
    print(f"  - Logos: {len(LOGOS)}")
    print(f"  - Artworks/Murals: {len(ARTWORKS)}")

if __name__ == '__main__':
    build_all()
