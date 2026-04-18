#!/usr/bin/env python3
"""Add Guided Tour button to the dashboard header and repackage."""
import os, shutil, zipfile

VIS = "/home/claude/rosling_project/visualizations"
OUT = "/mnt/user-data/outputs/rosling_gapminder"
ZIP_PATH = "/mnt/user-data/outputs/spatial_data_atlas.zip"

# ===== 1. Add tour button to dashboard =====
fpath = os.path.join(VIS, "index.html")
with open(fpath, "r") as f:
    dash = f.read()

# Check if already added
if "guided_tour" not in dash:
    # Add CSS for the tour button
    tour_css = """
.tour-launch{display:inline-flex;align-items:center;gap:8px;margin-top:1rem;background:transparent;border:2px solid var(--ac);color:var(--ac);padding:10px 28px;border-radius:50px;font-family:'Source Sans 3',sans-serif;font-size:.88rem;font-weight:600;cursor:pointer;letter-spacing:.03em;transition:all .3s ease;animation:tourPulse 3s ease-in-out infinite}
.tour-launch:hover{background:var(--ac);color:var(--bg);box-shadow:0 0 30px rgba(0,213,224,.25);transform:translateY(-2px)}
.tour-launch .tri{width:0;height:0;border-left:8px solid currentColor;border-top:5px solid transparent;border-bottom:5px solid transparent}
@keyframes tourPulse{0%,100%{box-shadow:0 0 0 0 rgba(0,213,224,0)}50%{box-shadow:0 0 0 8px rgba(0,213,224,.08)}}
"""
    # Insert CSS before closing </style>
    dash = dash.replace('</style>', tour_css + '</style>', 1)
    
    # Add button after the stats bar (after closing </div></div> of .ss)
    # Find the stats section and add after it
    stats_end = '</div></div></div><nav'
    tour_button = '</div></div><button class="tour-launch" onclick="window.location.href=\'guided_tour.html\'"><span class="tri"></span> Take the Guided Tour</button></div><nav'
    dash = dash.replace(stats_end, tour_button, 1)
    
    with open(fpath, "w") as f:
        f.write(dash)
    print(f"Dashboard updated with tour button: {len(dash)/1024:.1f} KB")
else:
    print("Tour button already present in dashboard")

# ===== 2. Also add link in chart_index.html =====
idx_path = os.path.join(VIS, "chart_index.html")
with open(idx_path, "r") as f:
    idx = f.read()

if "guided_tour" not in idx:
    old_back = '<div class="back-link"><a href="index.html">&larr; Back to Dashboard</a></div>'
    new_back = '<div class="back-link"><a href="index.html">&larr; Back to Dashboard</a> &nbsp; <a href="guided_tour.html" style="border-color:#FFD700;color:#FFD700">&#9654; Guided Tour</a></div>'
    idx = idx.replace(old_back, new_back)
    with open(idx_path, "w") as f:
        f.write(idx)
    print("Chart index updated with tour link")

# ===== 3. Copy everything to output =====
# HTML files
for fname in os.listdir(VIS):
    if fname.endswith(".html") and fname != "index.html.bak":
        shutil.copy2(os.path.join(VIS, fname), os.path.join(OUT, fname))

# Python scripts
proj_root = "/home/claude/rosling_project"
for fname in os.listdir(proj_root):
    if fname.endswith(".py"):
        shutil.copy2(os.path.join(proj_root, fname), os.path.join(OUT, fname))

# Data
for subdir in ["raw", "processed"]:
    src = os.path.join(proj_root, "data", subdir)
    dst = os.path.join(OUT, "data", subdir)
    os.makedirs(dst, exist_ok=True)
    for fname in os.listdir(src):
        shutil.copy2(os.path.join(src, fname), os.path.join(dst, fname))

# Count
html_count = sum(1 for f in os.listdir(OUT) if f.endswith(".html"))
py_count = sum(1 for f in os.listdir(OUT) if f.endswith(".py"))
print(f"\nOutput: {html_count} HTML, {py_count} Python scripts")
print(f"Guided tour: {'EXISTS' if os.path.exists(os.path.join(OUT, 'guided_tour.html')) else 'MISSING'}")

# ===== 4. Build ZIP =====
with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(OUT):
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            arcname = "spatial_data_atlas/" + os.path.relpath(fpath, OUT)
            zf.write(fpath, arcname)

sz = os.path.getsize(ZIP_PATH) / 1024 / 1024
with zipfile.ZipFile(ZIP_PATH) as zf:
    n = len(zf.namelist())
    has_tour = any("guided_tour" in f for f in zf.namelist())
print(f"\nZIP: {sz:.1f} MB, {n} files")
print(f"Tour in ZIP: {has_tour}")

# ===== 5. Verify tour links all exist =====
import re
with open(os.path.join(OUT, "guided_tour.html"), "r") as f:
    tour = f.read()
tour_files = re.findall(r'file:\s*"([^"]+)"', tour)
missing = [f for f in tour_files if not os.path.exists(os.path.join(OUT, f))]
print(f"\nTour references {len(tour_files)} charts")
print(f"Missing chart files: {missing if missing else 'None'}")

# Verify dashboard has tour button
with open(os.path.join(OUT, "index.html"), "r") as f:
    d = f.read()
print(f"Dashboard has tour button: {'guided_tour' in d}")
print(f"Chart index has tour link: {'guided_tour' in open(os.path.join(OUT, 'chart_index.html')).read()}")
