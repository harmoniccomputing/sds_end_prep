#!/usr/bin/env python3
"""
=============================================================================
  GAPMINDER SPATIAL DATA ATLAS
  A Complete Reproduction of Hans Rosling's Work + Spatial Analysis
=============================================================================

  Master runner script. Execute this single file to:
    1. Download all datasets from World Bank API, Gapminder, NOAA
    2. Process and merge into analysis-ready dataframes
    3. Generate 36 interactive Plotly visualizations
    4. Build a tabbed HTML dashboard (index.html)
    5. Package everything as a ZIP

  CONFIGURATION: Edit the section below to change paths.

  Requirements:
    pip install gapminder wbgapi plotly pandas numpy kaleido requests

  Data Sources (all CC-BY or public domain):
    - World Bank Open Data: https://data.worldbank.org/  (24 indicators)
    - Gapminder Foundation:  https://www.gapminder.org/data/
    - NOAA ERSST v5:         https://www.ncei.noaa.gov/products/extended-reconstructed-sst
    - NOAA Coral Reef Watch: https://coralreefwatch.noaa.gov/
    - UCDP/PRIO:             https://ucdp.uu.se/  (conflict reference)
=============================================================================
"""

import os
import sys
import subprocess
import zipfile
import shutil

# ===================================================================
# CONFIGURATION -- Edit these paths as needed.
# All paths are relative to this script's location.
# ===================================================================
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = SCRIPT_DIR  # change if scripts/ is a subfolder

DATA_RAW     = os.path.join(PROJECT_ROOT, "data", "raw")
DATA_PROC    = os.path.join(PROJECT_ROOT, "data", "processed")
VIZ_DIR      = os.path.join(PROJECT_ROOT, "visualizations")
OUTPUT_DIR   = os.path.join(PROJECT_ROOT, "output")
ZIP_NAME     = "gapminder_spatial_atlas.zip"

# World Bank year ranges
WB_YEAR_RANGE_MAIN  = range(1960, 2024)
WB_YEAR_RANGE_SHORT = range(2000, 2024)
WB_YEAR_RANGE_RECENT = range(2010, 2024)

# ===================================================================
# END CONFIGURATION
# ===================================================================

for d in [DATA_RAW, DATA_PROC, VIZ_DIR, OUTPUT_DIR]:
    os.makedirs(d, exist_ok=True)

print("=" * 72)
print("  GAPMINDER SPATIAL DATA ATLAS -- Master Runner")
print("=" * 72)
print(f"  Project root:   {PROJECT_ROOT}")
print(f"  Raw data:       {DATA_RAW}")
print(f"  Processed data: {DATA_PROC}")
print(f"  Visualizations: {VIZ_DIR}")
print(f"  Output/ZIP:     {OUTPUT_DIR}")
print("=" * 72)

# Run each phase as a subprocess so this file stays clean
# and each phase can also be run independently.
phases = [
    ("phase1_data_acquisition.py",       "Phase 1: Data Acquisition"),
    ("phase2_data_processing.py",        "Phase 2: Data Processing"),
    ("phase3_visualizations.py",         "Phase 3: Rosling Classic Charts (01-06)"),
    ("phase4_spatial_visualizations.py",  "Phase 4: Spatial Maps (07-22)"),
    ("phase5a_geo_variables.py",          "Phase 5A: Geo-Variable Analysis (23-36)"),
    ("phase5b_dashboard_zip.py",          "Phase 5B: Dashboard & ZIP Packaging"),
]

failed = []
for script, label in phases:
    spath = os.path.join(PROJECT_ROOT, script)
    if not os.path.exists(spath):
        print(f"\n[SKIP] {label}: {script} not found")
        failed.append(script)
        continue
    print(f"\n{'='*72}")
    print(f"  RUNNING: {label}")
    print(f"{'='*72}")
    result = subprocess.run(
        [sys.executable, spath],
        cwd=PROJECT_ROOT,
        timeout=300,
    )
    if result.returncode != 0:
        print(f"  [WARN] {script} exited with code {result.returncode}")
        failed.append(script)

print(f"\n{'='*72}")
print("  PIPELINE COMPLETE")
print(f"{'='*72}")

# Final report
html_count = len([f for f in os.listdir(VIZ_DIR) if f.endswith(".html")])
zip_path = os.path.join(OUTPUT_DIR, ZIP_NAME)
zip_exists = os.path.exists(zip_path)

print(f"  Visualizations generated: {html_count}")
print(f"  ZIP packaged:            {zip_exists} ({zip_path})")
if failed:
    print(f"  Phases with issues:      {failed}")
else:
    print(f"  All phases succeeded.")

print(f"\n  To view: open {os.path.join(VIZ_DIR, 'index.html')} in a browser.")
print(f"  To share: distribute {zip_path}")
