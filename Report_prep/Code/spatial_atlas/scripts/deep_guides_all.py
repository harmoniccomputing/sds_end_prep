#!/usr/bin/env python3
"""Build deep academic guides for all 76 charts missing them."""
import os, re

VIZ_DIR = "visualizations"

CSS = '''<!--ATLAS-GUIDE-START-->
<style>
.guide{position:relative;z-index:1;background:#080B13;padding:36px 5% 50px;color:#C8D0DA;
font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif;font-size:.84rem;line-height:1.75;border-top:2px solid #151d2e}
.guide-inner{max-width:1100px;margin:0 auto}
.guide h2{color:#00D5E0;font-size:1.15rem;font-weight:700;margin:0 0 4px;font-family:'Playfair Display',Georgia,serif}
.guide .tl{color:#FF5872;font-size:.92rem;font-weight:600;margin:0 0 16px;font-style:italic}
.guide h3{color:#FFD700;font-size:.88rem;font-weight:700;margin:22px 0 6px;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid #1a2233;padding-bottom:4px}
.guide p{margin:0 0 10px;color:#B8C4D0;text-align:justify}
.guide .hl{background:#0f1520;border-left:3px solid #00D5E0;padding:12px 16px;margin:10px 0;border-radius:0 6px 6px 0}
.guide .w{border-left-color:#FF5872}.guide .g{border-left-color:#FFD700}.guide .v{border-left-color:#B10DC9}
.guide b{color:#E8ECF0}.guide em{color:#FFD700;font-style:normal}
.guide code{background:#1C2333;padding:1px 6px;border-radius:3px;font-size:.76rem;color:#00D5E0}
.guide .co{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin:10px 0}
@media(max-width:900px){.guide .co{grid-template-columns:1fr}}
.guide .co>div{background:#0c1018;border-radius:6px;padding:14px 16px;border:1px solid #151d2e}
.guide .co h4{color:#00D5E0;font-size:.8rem;margin:0 0 6px;font-weight:700}
</style>
'''
END = '<!--ATLAS-GUIDE-END-->'

def wrap(body):
    return CSS + '<div class="guide"><div class="guide-inner">\n' + body + '\n</div></div>\n' + END

def inj(fpath, body):
    html = open(fpath).read()
    if 'ATLAS-GUIDE-START' in html: return False
    blk = wrap(body)
    html = html.replace("</body>", blk + "</body>") if "</body>" in html else html + blk
    open(fpath, 'w').write(html)
    return True

# Read all guide bodies from the file we'll create
exec(open('guide_bodies.py').read())

count = 0
for fn in sorted(os.listdir(VIZ_DIR)):
    if not fn.endswith('.html') or fn == 'index.html': continue
    num = fn.split('_')[0]
    if num not in G: continue
    if inj(os.path.join(VIZ_DIR, fn), G[num]):
        count += 1
print(f"Injected {count} deep guides")

# Verify
missing = 0
for fn in sorted(os.listdir(VIZ_DIR)):
    if not fn.endswith('.html') or fn == 'index.html': continue
    if 'ATLAS-GUIDE-START' not in open(os.path.join(VIZ_DIR, fn)).read():
        missing += 1
        print(f"  MISSING: {fn}")
print(f"Total missing: {missing}")
