import random, math, re
random.seed(58)
src = open('before-you-go-back-cover.svg').read()
blurb = re.search(r'  <!-- BLURB -->.*?\n  </g>\n', src, re.S).group(0)

W, H = 1600, 2400
# Milky Way band: runs from lower-left up to the right, below the blurb
ang = math.radians(-30)
cx, cy = 800, 1720
ux, uy = math.cos(ang), math.sin(ang)      # along band
nx, ny = -uy, ux                            # across band

stars = []
def add(x, y, r, o, c="#dfe6f2"):
    if 0 <= x <= W and 0 <= y <= H:
        # keep the blurb area calm
        if 150 < y < 1030 and 280 < x < 1320: o *= 0.35
        stars.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{c}" opacity="{o:.2f}"/>')

for _ in range(1300):                      # scattered field stars
    add(random.uniform(0, W), random.uniform(0, H), random.choice([0.6,0.7,0.8,1.0,1.2]), random.uniform(0.15, 0.7))
for _ in range(6500):                      # dense stars inside the band
    t = random.uniform(-1500, 1500); d = random.gauss(0, 120)
    add(cx + ux*t + nx*d, cy + uy*t + ny*d, random.choice([0.45,0.55,0.65,0.8]), random.uniform(0.15, 0.6),
        random.choice(["#dfe6f2"]*6 + ["#f3e2c0", "#c8d6ff"]))
bright = []
for _ in range(26):                        # a few brighter stars with a soft glow
    x, y = random.uniform(40, W-40), random.uniform(40, H-40)
    if 150 < y < 1030 and 280 < x < 1320: continue
    bright.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#e8eefb" opacity="0.12" filter="url(#glow)"/>'
                  f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(1.4,2.2):.2f}" fill="#f4f7fc" opacity="0.9"/>')

rot = math.degrees(ang)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#020307"/>
      <stop offset="0.55" stop-color="#060b17"/>
      <stop offset="1" stop-color="#0b1426"/>
    </linearGradient>
    <!-- soft falloff across the width of the band -->
    <linearGradient id="bandFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#fff" stop-opacity="1"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="dustFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#fff" stop-opacity="1"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="textShade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#020307" stop-opacity="0.3"/>
      <stop offset="0.75" stop-color="#020307" stop-opacity="0.2"/>
      <stop offset="1" stop-color="#020307" stop-opacity="0"/>
    </linearGradient>
    <filter id="fine" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.02 0.05" numOctaves="4" seed="21" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.8  0 0 0 0 0.85  0 0 0 0 0.95  2 0 0 0 -0.85" result="c"/>
      <feComposite in="c" in2="SourceGraphic" operator="in"/>
    </filter>
    <radialGradient id="core" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#f2c77c" stop-opacity="0.22"/>
      <stop offset="0.5" stop-color="#d9a860" stop-opacity="0.07"/>
      <stop offset="1" stop-color="#d9a860" stop-opacity="0"/>
    </radialGradient>
    <!-- cloudy galaxy light: noise kept only inside the band -->
    <filter id="clouds" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.005 0.016" numOctaves="6" seed="3" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.72  0 0 0 0 0.79  0 0 0 0 0.92  1.6 0 0 0 -0.55" result="c"/>
      <feComposite in="c" in2="SourceGraphic" operator="in"/>
    </filter>
    <filter id="dust" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.006 0.03" numOctaves="4" seed="9" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.01  0 0 0 0 0.015  0 0 0 0 0.03  2.4 0 0 0 -0.9" result="c"/>
      <feComposite in="c" in2="SourceGraphic" operator="in"/>
    </filter>
    <filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4"/></filter>
    <filter id="haze" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="11"/>
      <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.04 0"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#sky)"/>

  <!-- THE GALAXY -->
  <g transform="rotate({rot:.1f} {cx} {cy})">
    <rect x="-1000" y="{cy-260}" width="3600" height="520" fill="#7f8fb0" opacity="0.10" filter="url(#haze)"/>
    <rect x="-1000" y="{cy-230}" width="3600" height="460" fill="url(#bandFade)" filter="url(#clouds)" opacity="0.55"/>
    <rect x="-1000" y="{cy-120}" width="3600" height="240" fill="url(#bandFade)" filter="url(#clouds)" opacity="0.35"/>
    <rect x="-1000" y="{cy-200}" width="3600" height="400" fill="url(#bandFade)" filter="url(#fine)" opacity="0.45"/>
    <ellipse cx="{cx+260}" cy="{cy}" rx="520" ry="150" fill="url(#core)"/>
  </g>
  <g>
{chr(10).join("    "+s for s in stars)}
  </g>
  <g transform="rotate({rot:.1f} {cx} {cy})">
    <rect x="-1000" y="{cy-70}" width="3600" height="140" fill="url(#dustFade)" filter="url(#dust)" opacity="0.85"/>
  </g>
  <g>
{chr(10).join("    "+s for s in bright)}
  </g>

  <!-- soft dark behind the blurb so it stays readable -->
  <rect x="0" y="0" width="{W}" height="1300" fill="url(#textShade)"/>

{blurb}
  <!-- FOOTER: the Continuity's circle, title and author (bottom-left corner) -->
  <circle cx="156" cy="2252" r="36" fill="none" stroke="#dfe4ec" stroke-width="2" opacity="0.35"/>
  <g font-family="Inter, sans-serif" font-weight="300">
    <text x="216" y="2240" font-size="20" letter-spacing="8" fill="#6f7a8b">BEFORE YOU GO</text>
    <text x="216" y="2280" font-size="28" letter-spacing="10" fill="#c3cad5">TUCKER J SEARLE</text>
  </g>

  <!-- barcode area (placeholder for the ISBN) -->
  <rect x="1180" y="2150" width="300" height="170" fill="#f2f2f0"/>
  <text x="1330" y="2244" text-anchor="middle" font-family="Inter, sans-serif" font-size="18"
        letter-spacing="4" fill="#9a9a9a">ISBN / BARCODE</text>

  <rect width="{W}" height="{H}" filter="url(#grain)"/>
</svg>
'''
open('before-you-go-back-cover.svg', 'w').write(svg)
