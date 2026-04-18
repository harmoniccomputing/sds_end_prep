#!/usr/bin/env python3
"""Repackage the complete Spatial Data Visualization Atlas ZIP."""
import zipfile, os, shutil

VIS_DIR = "/home/claude/rosling_project/visualizations"
OUT_DIR = "/mnt/user-data/outputs/rosling_gapminder"
ZIP_PATH = "/mnt/user-data/outputs/spatial_data_atlas.zip"

# First copy all files to output dir
os.makedirs(OUT_DIR, exist_ok=True)

count = 0
for fname in os.listdir(VIS_DIR):
    if fname.endswith(".html"):
        src = os.path.join(VIS_DIR, fname)
        dst = os.path.join(OUT_DIR, fname)
        shutil.copy2(src, dst)
        count += 1

print(f"Copied {count} HTML files to output directory")

# Build ZIP
with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
    for fname in sorted(os.listdir(OUT_DIR)):
        if fname.endswith(".html"):
            fpath = os.path.join(OUT_DIR, fname)
            zf.write(fpath, f"spatial_data_atlas/{fname}")

# Report
zip_size = os.path.getsize(ZIP_PATH)
print(f"\nZIP: {ZIP_PATH}")
print(f"Size: {zip_size/1024/1024:.1f} MB")

# Count contents
with zipfile.ZipFile(ZIP_PATH, "r") as zf:
    files = zf.namelist()
    print(f"Files in ZIP: {len(files)}")
    
    # Verify key files
    has_index = any("index.html" in f and "chart_index" not in f for f in files)
    has_chart_index = any("chart_index.html" in f for f in files)
    has_quad = any("81_quad" in f for f in files)
    print(f"  Dashboard (index.html): {'OK' if has_index else 'MISSING'}")
    print(f"  Chart Index (chart_index.html): {'OK' if has_chart_index else 'MISSING'}")
    print(f"  Quad Panel (81_quad_panel_sync.html): {'OK' if has_quad else 'MISSING'}")
    
    # Count by type
    charts_2d = sum(1 for f in files if any(f.endswith(x) for x in ['.html']) and 'index' not in f and 'chart_index' not in f)
    print(f"  Chart files: {charts_2d}")
