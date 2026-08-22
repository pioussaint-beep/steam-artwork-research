# -*- coding: utf-8 -*-
"""
High-Aesthetic SVG Vector Generators for STEAM Logos & Artworks
Generates standalone, scalable 512x512 and 800x600 vector graphics with rich colors,
glowing filters, and distinctive iconography for elementary school STEAM lab inspiration.
"""

def generate_logo_svg(item):
    palette = item.get('color_palette', ["#0B132B", "#1C2541", "#5BC0BE", "#FFD166", "#EF476F"])
    c1 = palette[0] if len(palette) > 0 else "#0B132B"
    c2 = palette[1] if len(palette) > 1 else "#1C2541"
    c3 = palette[2] if len(palette) > 2 else "#5BC0BE"
    c4 = palette[3] if len(palette) > 3 else "#FFD166"
    c5 = palette[4] if len(palette) > 4 else "#EF476F"
    
    title = item.get('title', 'STEAM Lab')
    category = item.get('category', 'STEAM Lab')
    icon_type = item.get('svg_icon_type', 'default')
    
    # SVG Definition with gradients and filters
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}" />
      <stop offset="100%" stop-color="{c2}" />
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c3}" />
      <stop offset="50%" stop-color="{c4}" />
      <stop offset="100%" stop-color="{c5}" />
    </linearGradient>
    <linearGradient id="glowGrad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{c4}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{c3}" stop-opacity="0.9"/>
    </linearGradient>
    <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{c4}" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="{c5}" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="{c1}" stop-opacity="0"/>
    </radialGradient>
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="512" height="512" rx="48" fill="url(#bgGrad)" />
  <circle cx="256" cy="230" r="160" fill="url(#sunGlow)" />
  
  <!-- Outer Tech / Geometric Frame -->
  <circle cx="256" cy="230" r="170" fill="none" stroke="{c3}" stroke-width="3" stroke-dasharray="8 6" opacity="0.6"/>
  <circle cx="256" cy="230" r="185" fill="none" stroke="{c4}" stroke-width="1.5" opacity="0.4"/>
'''
    # Dynamic Icon Elements based on category and icon_type
    if "cosmic" in item.get("id", "") or "Space" in category:
        svg += f'''
  <!-- Cosmic Elements -->
  <g filter="url(#softShadow)">
    <!-- Orbit Rings -->
    <ellipse cx="256" cy="230" rx="130" ry="45" fill="none" stroke="url(#accentGrad)" stroke-width="5" transform="rotate(-25 256 230)" filter="url(#neonGlow)"/>
    <ellipse cx="256" cy="230" rx="140" ry="40" fill="none" stroke="{c4}" stroke-width="2" stroke-dasharray="6 4" transform="rotate(35 256 230)"/>
    
    <!-- Central Rocket / Core Icon -->
    <path d="M256,120 Q280,180 280,240 L232,240 Q232,180 256,120 Z" fill="url(#accentGrad)" filter="url(#neonGlow)"/>
    <path d="M232,240 L210,270 L236,260 Z" fill="{c5}"/>
    <path d="M280,240 L302,270 L276,260 Z" fill="{c5}"/>
    <circle cx="256" cy="180" r="14" fill="{c1}" stroke="{c4}" stroke-width="3"/>
    
    <!-- Rocket Thruster Flames -->
    <path d="M246,260 Q256,310 256,310 Q256,310 266,260 Z" fill="{c4}" filter="url(#neonGlow)"/>
    <path d="M250,260 Q256,290 256,290 Q256,290 262,260 Z" fill="#FFFFFF"/>
    
    <!-- Constellation Stars -->
    <circle cx="150" cy="150" r="5" fill="{c4}" filter="url(#neonGlow)"/>
    <circle cx="370" cy="140" r="6" fill="{c3}" filter="url(#neonGlow)"/>
    <circle cx="360" cy="300" r="4" fill="{c4}"/>
    <circle cx="140" cy="290" r="5" fill="{c5}"/>
    <line x1="150" y1="150" x2="200" y2="120" stroke="{c3}" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.7"/>
    <line x1="370" y1="140" x2="330" y2="170" stroke="{c4}" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.7"/>
  </g>
'''
    elif "gear" in item.get("id", "") or "Gears" in category:
        svg += f'''
  <!-- Gear & Tinkering Elements -->
  <g filter="url(#softShadow)">
    <!-- Central Large Gear -->
    <g transform="translate(256, 220)" filter="url(#neonGlow)">
      <circle cx="0" cy="0" r="75" fill="url(#accentGrad)"/>
      <circle cx="0" cy="0" r="35" fill="{c1}" stroke="{c4}" stroke-width="4"/>
      <!-- Gear Teeth -->
      <path d="M-15,-90 L15,-90 L12,-70 L-12,-70 Z M-90,-15 L-90,15 L-70,12 L-70,-12 Z M-15,70 L15,70 L12,90 L-12,90 Z M70,-15 L70,15 L90,12 L90,-12 Z" fill="{c3}"/>
      <path d="M-60,-60 L-40,-75 L-30,-55 L-50,-40 Z M60,-60 L40,-75 L30,-55 L50,-40 Z M-60,60 L-40,75 L-30,55 L-50,40 Z M60,60 L40,75 L30,55 L50,40 Z" fill="{c3}"/>
    </g>
    <!-- Secondary Interlocking Gear -->
    <g transform="translate(340, 150) rotate(15)">
      <circle cx="0" cy="0" r="45" fill="none" stroke="{c4}" stroke-width="12" stroke-dasharray="14 10"/>
      <circle cx="0" cy="0" r="20" fill="{c2}" stroke="{c5}" stroke-width="3"/>
    </g>
    <!-- Sprouting Lightbulb / Spark Core -->
    <path d="M256,150 Q280,180 270,210 L242,210 Q232,180 256,150 Z" fill="{c4}" opacity="0.85" filter="url(#neonGlow)"/>
    <line x1="256" y1="130" x2="256" y2="105" stroke="{c4}" stroke-width="4" stroke-linecap="round" filter="url(#neonGlow)"/>
    <line x1="220" y1="140" x2="200" y2="125" stroke="{c4}" stroke-width="4" stroke-linecap="round"/>
    <line x1="292" y1="140" x2="312" y2="125" stroke="{c4}" stroke-width="4" stroke-linecap="round"/>
  </g>
'''
    elif "mascot" in item.get("id", "") or "Mascot" in category:
        svg += f'''
  <!-- Mascot Robot / Friendly Explorer Elements -->
  <g filter="url(#softShadow)" transform="translate(256, 220)">
    <!-- Robot Head / Body Base -->
    <rect x="-85" y="-75" width="170" height="135" rx="35" fill="url(#accentGrad)" filter="url(#neonGlow)"/>
    <rect x="-65" y="-55" width="130" height="75" rx="18" fill="{c1}" stroke="{c4}" stroke-width="3"/>
    
    <!-- Heart / Expressive Screen Eyes -->
    <circle cx="-32" cy="-20" r="14" fill="{c4}" filter="url(#neonGlow)"/>
    <circle cx="32" cy="-20" r="14" fill="{c4}" filter="url(#neonGlow)"/>
    <circle cx="-35" cy="-24" r="4" fill="#FFFFFF"/>
    <circle cx="29" cy="-24" r="4" fill="#FFFFFF"/>
    <path d="M-15,8 Q0,20 15,8" fill="none" stroke="{c3}" stroke-width="4" stroke-linecap="round"/>
    
    <!-- Cute Antenna with Glowing Orb -->
    <line x1="0" y1="-75" x2="0" y2="-110" stroke="{c4}" stroke-width="5" stroke-linecap="round"/>
    <circle cx="0" cy="-115" r="16" fill="{c5}" filter="url(#neonGlow)"/>
    <circle cx="-4" cy="-119" r="4" fill="#FFFFFF"/>
    
    <!-- Headphone / Ear Dials -->
    <rect x="-98" y="-40" width="15" height="45" rx="7" fill="{c5}"/>
    <rect x="83" y="-40" width="15" height="45" rx="7" fill="{c5}"/>
    
    <!-- Chest Bowtie / Circuit Badge -->
    <polygon points="-25,75 25,75 0,95" fill="{c4}"/>
    <polygon points="-25,115 25,115 0,95" fill="{c4}"/>
    <circle cx="0" cy="95" r="7" fill="{c1}"/>
  </g>
'''
    elif "nature" in item.get("id", "") or "Nature" in category:
        svg += f'''
  <!-- Nature & Bio-Tech Elements -->
  <g filter="url(#softShadow)" transform="translate(256, 220)">
    <!-- Split Biomimicry Butterfly / Leaf Wings -->
    <!-- Left Wing (Organic) -->
    <path d="M0,-10 C-40,-90 -140,-80 -130,0 C-125,50 -60,90 0,60 Z" fill="url(#accentGrad)" filter="url(#neonGlow)" opacity="0.9"/>
    <!-- Right Wing (Circuit Tech) -->
    <path d="M0,-10 C40,-90 140,-80 130,0 C125,50 60,90 0,60 Z" fill="{c1}" stroke="{c4}" stroke-width="4"/>
    <!-- Circuit Lines on Right Wing -->
    <path d="M20,0 L60,-20 L90,-20 M40,20 L80,30 L100,10 M30,-40 L70,-60" fill="none" stroke="{c3}" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="90" cy="-20" r="5" fill="{c4}" filter="url(#neonGlow)"/>
    <circle cx="100" cy="10" r="5" fill="{c5}"/>
    <circle cx="70" cy="-60" r="5" fill="{c4}"/>
    
    <!-- Central Body Seed / Chrysalis -->
    <ellipse cx="0" cy="20" rx="14" ry="45" fill="{c4}" filter="url(#neonGlow)"/>
    <circle cx="0" cy="-30" r="12" fill="{c5}"/>
    <line x1="-5" y1="-40" x2="-25" y2="-70" stroke="{c3}" stroke-width="3" stroke-linecap="round"/>
    <line x1="5" y1="-40" x2="25" y2="-70" stroke="{c3}" stroke-width="3" stroke-linecap="round"/>
  </g>
'''
    elif "typo" in item.get("id", "") or "Typography" in category:
        svg += f'''
  <!-- Integrated Typography / Shield Monogram -->
  <g filter="url(#softShadow)" transform="translate(256, 215)">
    <!-- Crest Shield Frame -->
    <path d="M-100,-80 L100,-80 L100,20 Q100,110 0,140 Q-100,110 -100,20 Z" fill="url(#bgGrad)" stroke="url(#accentGrad)" stroke-width="6" filter="url(#neonGlow)"/>
    
    <!-- 4 Quadrant Grid -->
    <line x1="-95" y1="20" x2="95" y2="20" stroke="{c3}" stroke-width="3" stroke-dasharray="5 5" opacity="0.6"/>
    <line x1="0" y1="-75" x2="0" y2="130" stroke="{c3}" stroke-width="3" stroke-dasharray="5 5" opacity="0.6"/>
    
    <!-- 4 Quadrant STEAM Mini Icons -->
    <!-- Atom (Science) -->
    <ellipse cx="-45" cy="-30" rx="22" ry="9" fill="none" stroke="{c4}" stroke-width="2.5" transform="rotate(30 -45 -30)"/>
    <ellipse cx="-45" cy="-30" rx="22" ry="9" fill="none" stroke="{c4}" stroke-width="2.5" transform="rotate(-30 -45 -30)"/>
    <circle cx="-45" cy="-30" r="4" fill="{c5}"/>
    <!-- Circuit (Tech) -->
    <path d="M30,-45 L50,-45 L65,-25 L65,-10" fill="none" stroke="{c4}" stroke-width="2.5" stroke-linecap="round"/>
    <circle cx="30" cy="-45" r="4" fill="{c3}"/>
    <circle cx="65" cy="-10" r="4" fill="{c5}"/>
    <!-- Gear (Engineering) -->
    <circle cx="-45" cy="65" r="16" fill="none" stroke="{c4}" stroke-width="4" stroke-dasharray="6 4"/>
    <circle cx="-45" cy="65" r="6" fill="{c3}"/>
    <!-- Palette / Pi (Art & Math) -->
    <path d="M35,65 Q55,45 65,65 Q60,85 45,75 Z" fill="{c4}"/>
    <circle cx="48" cy="62" r="3" fill="{c1}"/>
    <circle cx="56" cy="68" r="3" fill="{c5}"/>
  </g>
'''
    else:
        # Renowned Real-World & General STEAM Badge
        svg += f'''
  <!-- General Renowned STEAM Crest -->
  <g filter="url(#softShadow)" transform="translate(256, 220)">
    <!-- Hexagonal Honeycomb Core -->
    <polygon points="0,-100 86,-50 86,50 0,100 -86,50 -86,-50" fill="url(#accentGrad)" stroke="{c4}" stroke-width="5" filter="url(#neonGlow)"/>
    <polygon points="0,-80 69,-40 69,40 0,80 -69,40 -69,-40" fill="{c1}" stroke="{c3}" stroke-width="2"/>
    
    <!-- Central Golden Spark / Atom -->
    <circle cx="0" cy="0" r="24" fill="{c4}" filter="url(#neonGlow)"/>
    <ellipse cx="0" cy="0" rx="60" ry="20" fill="none" stroke="{c3}" stroke-width="3" transform="rotate(45 0 0)"/>
    <ellipse cx="0" cy="0" rx="60" ry="20" fill="none" stroke="{c5}" stroke-width="3" transform="rotate(-45 0 0)"/>
    <circle cx="38" cy="38" r="5" fill="#FFFFFF"/>
    <circle cx="-38" cy="38" r="5" fill="{c4}"/>
  </g>
'''

    # Typography Ribbon / Banner at bottom of logo
    svg += f'''
  <!-- Bottom Text Banner -->
  <g filter="url(#softShadow)">
    <rect x="40" y="405" width="432" height="68" rx="20" fill="{c1}" stroke="url(#accentGrad)" stroke-width="2.5" />
    <text x="256" y="445" font-family="'Outfit', 'Inter', 'Segoe UI', sans-serif" font-weight="800" font-size="20" fill="{c4}" text-anchor="middle" letter-spacing="1.5">
      {title[:26].upper()}
    </text>
    <text x="256" y="464" font-family="'Inter', sans-serif" font-weight="600" font-size="11" fill="{c3}" text-anchor="middle" letter-spacing="3" opacity="0.9">
      {category.upper()}
    </text>
  </g>
</svg>
'''
    return svg


def generate_artwork_svg(item):
    palette = item.get('color_palette', ["#0B132B", "#1C2541", "#5BC0BE", "#FFD166", "#EF476F"])
    c1 = palette[0] if len(palette) > 0 else "#0B132B"
    c2 = palette[1] if len(palette) > 1 else "#1C2541"
    c3 = palette[2] if len(palette) > 2 else "#5BC0BE"
    c4 = palette[3] if len(palette) > 3 else "#FFD166"
    c5 = palette[4] if len(palette) > 4 else "#EF476F"
    
    title = item.get('title', 'STEAM Artwork')
    category = item.get('category', 'STEAM Art')
    
    # 600x800 Portrait Poster Canvas
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 800" width="100%" height="100%">
  <defs>
    <linearGradient id="artBgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{c1}" />
      <stop offset="60%" stop-color="{c2}" />
      <stop offset="100%" stop-color="{c3}" />
    </linearGradient>
    <linearGradient id="artAccent" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c4}" />
      <stop offset="100%" stop-color="{c5}" />
    </linearGradient>
    <radialGradient id="nebulaSun" cx="50%" cy="35%" r="60%">
      <stop offset="0%" stop-color="{c4}" stop-opacity="0.95"/>
      <stop offset="35%" stop-color="{c5}" stop-opacity="0.6"/>
      <stop offset="70%" stop-color="{c2}" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="{c1}" stop-opacity="0"/>
    </radialGradient>
    <filter id="artGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="12" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="600" height="800" fill="url(#artBgGrad)" />
  
  <!-- Outer Poster Border -->
  <rect x="24" y="24" width="552" height="752" rx="16" fill="none" stroke="{c4}" stroke-width="3" opacity="0.65"/>
  <rect x="32" y="32" width="536" height="736" rx="12" fill="none" stroke="{c3}" stroke-width="1" opacity="0.4"/>
  
  <!-- Grand Sun / Celestial Center Glow -->
  <circle cx="300" cy="300" r="220" fill="url(#nebulaSun)" />
'''

    # Distinctive visual compositions per artwork category
    if "jpl" in item.get("id", "") or "Space" in category:
        svg += f'''
  <!-- Cosmic Landscape / Exoplanet Horizons -->
  <g>
    <!-- Distant Mountain Ridges & Craters -->
    <polygon points="40,550 180,380 320,550" fill="{c2}" opacity="0.7"/>
    <polygon points="220,550 380,340 560,550" fill="{c1}" opacity="0.9"/>
    <polygon points="120,560 280,420 460,560" fill="{c5}" opacity="0.4"/>
    
    <!-- Planetary Rings Across Sky -->
    <ellipse cx="300" cy="260" rx="260" ry="70" fill="none" stroke="url(#artAccent)" stroke-width="8" transform="rotate(-15 300 260)" filter="url(#artGlow)"/>
    <ellipse cx="300" cy="260" rx="280" ry="60" fill="none" stroke="{c4}" stroke-width="2" stroke-dasharray="8 6" transform="rotate(-15 300 260)"/>
    
    <!-- Giant Glowing Celestial Body -->
    <circle cx="300" cy="240" r="85" fill="url(#artAccent)" filter="url(#artGlow)"/>
    <circle cx="280" cy="220" r="70" fill="{c1}" opacity="0.3"/>
    
    <!-- Retro Sci-Fi Explorer / Rover Silhouette -->
    <rect x="260" y="500" width="80" height="35" rx="8" fill="{c4}" filter="url(#artGlow)"/>
    <circle cx="280" cy="535" r="14" fill="{c1}" stroke="{c4}" stroke-width="3"/>
    <circle cx="320" cy="535" r="14" fill="{c1}" stroke="{c4}" stroke-width="3"/>
    <line x1="300" y1="500" x2="300" y2="470" stroke="{c4}" stroke-width="3"/>
    <circle cx="300" cy="465" r="6" fill="{c5}"/>
    
    <!-- Star Spangles -->
    <circle cx="100" cy="120" r="4" fill="#FFFFFF" filter="url(#artGlow)"/>
    <circle cx="480" cy="110" r="5" fill="{c4}" filter="url(#artGlow)"/>
    <circle cx="510" cy="200" r="3" fill="#FFFFFF"/>
    <circle cx="80" cy="240" r="4" fill="{c3}"/>
  </g>
'''
    elif "mural" in item.get("id", "") or "Mural" in category:
        svg += f'''
  <!-- Wall Mural & Architecture Composition -->
  <g>
    <!-- Isometric Blocks & Maker City -->
    <polygon points="300,160 460,240 300,320 140,240" fill="url(#artAccent)" filter="url(#artGlow)"/>
    <polygon points="140,240 300,320 300,480 140,400" fill="{c1}" opacity="0.85"/>
    <polygon points="460,240 300,320 300,480 460,400" fill="{c2}" opacity="0.95"/>
    
    <!-- Giant Gear & Kinetic Motion -->
    <g transform="translate(300, 320)" opacity="0.9">
      <circle cx="0" cy="0" r="110" fill="none" stroke="{c4}" stroke-width="16" stroke-dasharray="24 16" filter="url(#artGlow)"/>
      <circle cx="0" cy="0" r="60" fill="none" stroke="{c3}" stroke-width="6"/>
      <circle cx="0" cy="0" r="25" fill="{c5}"/>
    </g>
    
    <!-- Sprouting Tree Roots / Circuit Flow -->
    <path d="M140,400 Q200,500 240,560 M460,400 Q400,500 360,560 M300,480 L300,560" stroke="{c4}" stroke-width="6" stroke-linecap="round" fill="none" filter="url(#artGlow)"/>
  </g>
'''
    elif "bio" in item.get("id", "") or "Bio" in category:
        svg += f'''
  <!-- Bio-Art & Natural Wonders Composition -->
  <g>
    <!-- Giant Fibonacci Nautilus / Organic Spiral -->
    <path d="M300,320 C320,320 330,310 330,290 C330,260 305,240 270,240 C220,240 185,280 185,340 C185,420 245,480 335,480 C445,480 520,390 520,270 C520,130 400,40 250,40 C80,40 -20,165 -20,340" fill="none" stroke="url(#artAccent)" stroke-width="8" stroke-linecap="round" filter="url(#artGlow)"/>
    
    <!-- Cellular Micro-Spheres & Crystal Facets -->
    <circle cx="300" cy="300" r="45" fill="{c4}" opacity="0.8" filter="url(#artGlow)"/>
    <circle cx="210" cy="240" r="28" fill="{c3}" opacity="0.7"/>
    <circle cx="390" cy="220" r="32" fill="{c5}" opacity="0.75"/>
    <circle cx="350" cy="400" r="36" fill="{c4}" opacity="0.6"/>
    <circle cx="190" cy="380" r="24" fill="{c3}" opacity="0.8"/>
  </g>
'''
    elif "math" in item.get("id", "") or "Math" in category:
        svg += f'''
  <!-- Generative Math & Fractal Geometry Composition -->
  <g transform="translate(300, 320)">
    <!-- Concentric Harmonic Spirograph Rings -->
    <circle cx="0" cy="0" r="180" fill="none" stroke="{c4}" stroke-width="3" stroke-dasharray="10 8" filter="url(#artGlow)"/>
    <ellipse cx="0" cy="0" rx="170" ry="70" fill="none" stroke="{c3}" stroke-width="4" transform="rotate(0)"/>
    <ellipse cx="0" cy="0" rx="170" ry="70" fill="none" stroke="{c4}" stroke-width="4" transform="rotate(30)"/>
    <ellipse cx="0" cy="0" rx="170" ry="70" fill="none" stroke="{c5}" stroke-width="4" transform="rotate(60)"/>
    <ellipse cx="0" cy="0" rx="170" ry="70" fill="none" stroke="{c3}" stroke-width="4" transform="rotate(90)"/>
    <ellipse cx="0" cy="0" rx="170" ry="70" fill="none" stroke="{c4}" stroke-width="4" transform="rotate(120)"/>
    <ellipse cx="0" cy="0" rx="170" ry="70" fill="none" stroke="{c5}" stroke-width="4" transform="rotate(150)"/>
    
    <!-- Central Golden Core -->
    <circle cx="0" cy="0" r="35" fill="url(#artAccent)" filter="url(#artGlow)"/>
    <circle cx="0" cy="0" r="14" fill="{c1}"/>
  </g>
'''
    elif "inv" in item.get("id", "") or "Invention" in category:
        svg += f'''
  <!-- Invention Blueprint & Engineering Blueprint -->
  <g>
    <!-- Blueprint Drafting Grid Lines -->
    <line x1="60" y1="120" x2="540" y2="120" stroke="{c3}" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.5"/>
    <line x1="60" y1="240" x2="540" y2="240" stroke="{c3}" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.5"/>
    <line x1="60" y1="360" x2="540" y2="360" stroke="{c3}" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.5"/>
    <line x1="60" y1="480" x2="540" y2="480" stroke="{c3}" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.5"/>
    
    <!-- Flying Machine / Robotic Craft Wings -->
    <path d="M300,180 Q450,220 500,320 L300,300 L100,320 Q150,220 300,180 Z" fill="url(#artAccent)" opacity="0.85" filter="url(#artGlow)"/>
    <line x1="300" y1="180" x2="300" y2="480" stroke="{c4}" stroke-width="5"/>
    
    <!-- Caliper & Compass Dimension Rings -->
    <circle cx="300" cy="330" r="90" fill="none" stroke="{c4}" stroke-width="3" stroke-dasharray="8 6"/>
    <circle cx="300" cy="330" r="30" fill="{c1}" stroke="{c5}" stroke-width="4"/>
    <path d="M220,330 L380,330" stroke="{c4}" stroke-width="2"/>
    <text x="390" y="335" font-family="monospace" font-size="12" fill="{c4}">Ø 180mm</text>
  </g>
'''
    else:
        # STEAM Hero & Pioneer Portrait
        svg += f'''
  <!-- Historical Pioneer & STEAM Hero Iconography -->
  <g>
    <!-- Glowing Halo of Knowledge -->
    <circle cx="300" cy="280" r="140" fill="url(#artAccent)" opacity="0.85" filter="url(#artGlow)"/>
    
    <!-- Hero Bust Silhouette -->
    <path d="M300,180 C260,180 235,215 235,260 C235,305 260,340 300,340 C340,340 365,305 365,260 C365,215 340,180 300,180 Z M180,480 C180,410 240,370 300,370 C360,370 420,410 420,480 Z" fill="{c1}"/>
    
    <!-- Radiating Ideas & Formulas -->
    <circle cx="300" cy="280" r="170" fill="none" stroke="{c4}" stroke-width="3" stroke-dasharray="12 8"/>
    <circle cx="210" cy="180" r="16" fill="{c5}" filter="url(#artGlow)"/>
    <circle cx="390" cy="180" r="16" fill="{c3}" filter="url(#artGlow)"/>
    <circle cx="160" cy="310" r="12" fill="{c4}"/>
    <circle cx="440" cy="310" r="12" fill="{c5}"/>
  </g>
'''

    # Bottom Title Card
    svg += f'''
  <!-- Poster Typography Banner -->
  <g>
    <rect x="50" y="600" width="500" height="135" rx="16" fill="{c1}" stroke="{c4}" stroke-width="2" />
    <text x="300" y="642" font-family="'Outfit', 'Inter', sans-serif" font-weight="900" font-size="20" fill="{c4}" text-anchor="middle" letter-spacing="1">
      {title[:32].upper()}
    </text>
    <text x="300" y="668" font-family="'Inter', sans-serif" font-weight="700" font-size="12" fill="{c3}" text-anchor="middle" letter-spacing="3">
      {category.upper()}
    </text>
    <line x1="120" y1="685" x2="480" y2="685" stroke="{c5}" stroke-width="1.5" opacity="0.6"/>
    <text x="300" y="710" font-family="'Inter', sans-serif" font-weight="500" font-size="11" fill="#FFFFFF" text-anchor="middle" opacity="0.85">
      Elementary School STEAM Lab • Inspiring Awe &amp; Wonder
    </text>
  </g>
</svg>
'''
    return svg
