#!/usr/bin/env python3
"""
Final update: Add charts 82-84 to dashboard and index, repackage ZIP with all files.
"""
import os, shutil, zipfile, re

VIS = "/home/claude/rosling_project/visualizations"
OUT = "/mnt/user-data/outputs/rosling_gapminder"
ZIP_PATH = "/mnt/user-data/outputs/spatial_data_atlas.zip"

# ========== 1. UPDATE DASHBOARD ==========
with open(os.path.join(VIS, "index.html"), "r") as f:
    dash = f.read()

# Update stats: 81 -> 84 charts
dash = dash.replace('<div class="sv">81</div>', '<div class="sv">84</div>', 1)

# Find the existing quad-panel card and add 3 more after it
old_sync_end = """</div></div>
<div class="tp" id="p-sync" """
# Actually, find the sync panel content and add cards
old_card = """<div class="cd" onclick="op('81_quad_panel_sync.html')" style="animation-delay:0.00s"><div class="cs" style="background:#00D5E0"></div><div class="cb"><div class="ct"><span class="cn">81</span><span class="cg">Quad-Panel</span></div><h3>Four Lenses on Global Development</h3><p class="dp">Bubble chart (GDP vs Life Exp) + World choropleth (fertility) + Stacked area (continental population) + Continental trajectory (fertility vs child mortality). All synchronized via single year slider 1990-2023. Play/pause with speed control. Mathematical framework: Preston Curve, Hagerstrand diffusion, demographic transition, Tobler's First Law.</p><div class="ca">Open chart &rarr;</div></div></div>"""

new_cards = old_card + """
<div class="cd" onclick="op('82_health_environment_sync.html')" style="animation-delay:0.04s"><div class="cs" style="background:#7CFC00"></div><div class="cb"><div class="ct"><span class="cn">82</span><span class="cg">Quad-Panel</span></div><h3>Health-Environment Nexus</h3><p class="dp">Aridity vs child mortality + Environmental health choropleth + Continental development indicators + Preston Curve colored by birth rate. Year slider 1990-2023. Mathematical framework: EKC, coupled mortality-fertility ODEs, Omran's epidemiological transition.</p><div class="ca">Open chart &rarr;</div></div></div>
<div class="cd" onclick="op('83_tech_inequality_sync.html')" style="animation-delay:0.08s"><div class="cs" style="background:#B088F9"></div><div class="cb"><div class="ct"><span class="cn">83</span><span class="cg">Quad-Panel</span></div><h3>Technology-Inequality Divergence</h3><p class="dp">Internet penetration choropleth + Gini vs GDP scatter (size=internet) + Continental digital divide trends + Life expectancy heatmap by income x continent. Year slider 1990-2023. Hagerstrand logistic diffusion, Kuznets curve, geographic contingency.</p><div class="ca">Open chart &rarr;</div></div></div>
<div class="cd" onclick="op('84_india_threshold_sync.html')" style="animation-delay:0.12s"><div class="cs" style="background:#FF5872"></div><div class="cb"><div class="ct"><span class="cn">84</span><span class="cg">Quad-Panel</span></div><h3>India Electoral Threshold Explorer</h3><p class="dp">Turnout threshold slider (40-85%) filters all 4 panels simultaneously: constituency map + margin histogram + women vs area scatter + alliance seat bars. Watch how raising the engagement bar reshapes India's electoral geography. MAUP, spatial filtering, mobilization hypothesis.</p><div class="ca">Open chart &rarr;</div></div></div>"""

dash = dash.replace(old_card, new_cards)

# Update tab count
dash = dash.replace('<span class="tc">1</span></button>', '<span class="tc">4</span></button>')

with open(os.path.join(VIS, "index.html"), "w") as f:
    f.write(dash)
print(f"Dashboard updated: {len(dash)/1024:.1f} KB")

# ========== 2. UPDATE CHART INDEX ==========
with open(os.path.join(VIS, "chart_index.html"), "r") as f:
    idx = f.read()

# Update chart count
idx = idx.replace("All 81 charts grouped", "All 84 charts grouped")

# Add 3 new cards to the Synchronized Multi-View section
new_index_cards = """
        <a href="82_health_environment_sync.html" class="card" style="--accent:#00D5E0">
            <div class="card-num">#82</div>
            <div class="card-title">Health-Environment Nexus: Synchronized Quad-Panel</div>
            <div class="card-desc">Aridity index vs child mortality + Environmental health choropleth + Continental grouped bars + Preston Curve with birth rate color. Year slider 1990-2023.</div>
            <div class="card-bottom"><span class="bottom-label">Takeaway:</span> Africa's child mortality is declining faster than any other continent's did at the same income level, driven by mobile health interventions that follow spatial diffusion patterns.</div>
        </a>
        
        <a href="83_tech_inequality_sync.html" class="card" style="--accent:#00D5E0">
            <div class="card-num">#83</div>
            <div class="card-title">Technology-Inequality Divergence: Synchronized Quad-Panel</div>
            <div class="card-desc">Internet penetration choropleth + Gini-GDP scatter with internet size + Continental digital divide lines + Income-continent life expectancy heatmap. Year slider 1990-2023.</div>
            <div class="card-bottom"><span class="bottom-label">Takeaway:</span> Internet adoption follows Hagerstrand's logistic spatial diffusion model; Africa's mobile-first leapfrog produces structurally different digital landscapes from desktop-first economies.</div>
        </a>
        
        <a href="84_india_threshold_sync.html" class="card" style="--accent:#00D5E0">
            <div class="card-num">#84</div>
            <div class="card-title">India Elections 2024: Turnout Threshold Explorer</div>
            <div class="card-desc">Turnout threshold slider (40-85%) simultaneously filters: constituency map + margin distribution + women vs area scatter + alliance seat bars. 543 constituencies.</div>
            <div class="card-bottom"><span class="bottom-label">Takeaway:</span> Raising the turnout threshold systematically removes Hindi belt constituencies, shifting alliance balance toward INDIA: the regions with highest engagement face the largest losses under delimitation.</div>
        </a>"""

# Insert before closing of the Synchronized section
idx = idx.replace('</div></div>\n</div>', '</div></div>' + new_index_cards + '\n</div>', 1)

# Also update the stats
idx = idx.replace('<div class="stat-num">81</div>', '<div class="stat-num">84</div>')

with open(os.path.join(VIS, "chart_index.html"), "w") as f:
    f.write(idx)
print(f"Chart index updated: {len(idx)/1024:.1f} KB")

# ========== 3. COPY ALL FILES TO OUTPUT ==========
# Copy all HTML visualizations
for fname in os.listdir(VIS):
    if fname.endswith(".html") and fname != "index.html.bak":
        shutil.copy2(os.path.join(VIS, fname), os.path.join(OUT, fname))

# Copy all Python scripts
proj_root = "/home/claude/rosling_project"
for fname in os.listdir(proj_root):
    if fname.endswith(".py"):
        shutil.copy2(os.path.join(proj_root, fname), os.path.join(OUT, fname))

# Copy data directories
for subdir in ["raw", "processed"]:
    src_dir = os.path.join(proj_root, "data", subdir)
    dst_dir = os.path.join(OUT, "data", subdir)
    os.makedirs(dst_dir, exist_ok=True)
    for fname in os.listdir(src_dir):
        shutil.copy2(os.path.join(src_dir, fname), os.path.join(dst_dir, fname))

# Count
html_count = sum(1 for f in os.listdir(OUT) if f.endswith(".html"))
py_count = sum(1 for f in os.listdir(OUT) if f.endswith(".py"))
data_count = sum(1 for f in os.listdir(os.path.join(OUT, "data", "raw"))) + sum(1 for f in os.listdir(os.path.join(OUT, "data", "processed")))
print(f"\nOutput directory: {html_count} HTML, {py_count} Python, {data_count} data files")

# ========== 4. BUILD ZIP ==========
with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(OUT):
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            arcname = os.path.relpath(fpath, OUT)
            arcname = f"spatial_data_atlas/{arcname}"
            zf.write(fpath, arcname)

zip_size = os.path.getsize(ZIP_PATH)
with zipfile.ZipFile(ZIP_PATH, "r") as zf:
    zip_files = zf.namelist()
    html_in_zip = sum(1 for f in zip_files if f.endswith(".html"))
    py_in_zip = sum(1 for f in zip_files if f.endswith(".py"))
    data_in_zip = sum(1 for f in zip_files if '/data/' in f)

print(f"\nZIP: {zip_size/1024/1024:.1f} MB")
print(f"  Total files: {len(zip_files)}")
print(f"  HTML: {html_in_zip}")
print(f"  Python: {py_in_zip}")
print(f"  Data: {data_in_zip}")
