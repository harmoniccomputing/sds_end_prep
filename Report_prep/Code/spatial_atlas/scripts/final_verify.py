#!/usr/bin/env python3
"""Final verification pass across all deliverables."""
import os, re, zipfile

OUT_DIR = "/mnt/user-data/outputs/rosling_gapminder"
ZIP_PATH = "/mnt/user-data/outputs/spatial_data_atlas.zip"

print("=" * 80)
print("FINAL VERIFICATION: Spatial Data Visualization Atlas")
print("=" * 80)

# 1. File count
html_files = sorted(f for f in os.listdir(OUT_DIR) if f.endswith(".html"))
chart_files = sorted(f for f in html_files if f[0].isdigit())
print(f"\n[1] FILE COUNT")
print(f"  Total HTML files: {len(html_files)}")
print(f"  Chart files (01-81): {len(chart_files)}")
print(f"  Dashboard (index.html): {'OK' if 'index.html' in html_files else 'MISSING'}")
print(f"  Chart Index (chart_index.html): {'OK' if 'chart_index.html' in html_files else 'MISSING'}")

# 2. Verify all 81 charts present
expected = set(f"{i:02d}" for i in range(1, 82))
present = set(f.split("_")[0] for f in chart_files)
missing = expected - present
extra = present - expected
print(f"\n[2] CHART COMPLETENESS")
print(f"  Expected: 81, Found: {len(present)}")
if missing:
    print(f"  MISSING: {sorted(missing)}")
else:
    print(f"  All 81 charts present: OK")
if extra:
    print(f"  Extra: {sorted(extra)}")

# 3. Title tags
print(f"\n[3] TITLE TAGS")
no_title = []
for f in chart_files:
    with open(os.path.join(OUT_DIR, f), "r") as fh:
        if "<title>" not in fh.read().lower():
            no_title.append(f)
print(f"  Charts without <title>: {len(no_title)}")
if no_title:
    for f in no_title[:5]:
        print(f"    {f}")

# 4. Guide panels
print(f"\n[4] ACADEMIC GUIDE PANELS")
no_guide = []
total_guide_chars = 0
for f in chart_files:
    with open(os.path.join(OUT_DIR, f), "r") as fh:
        content = fh.read()
    start = content.find("<!--ATLAS-GUIDE-START-->")
    end = content.find("<!--ATLAS-GUIDE-END-->")
    if start < 0 or end < 0:
        no_guide.append(f)
    else:
        total_guide_chars += (end - start)
print(f"  Charts with guides: {len(chart_files) - len(no_guide)}/81")
print(f"  Total guide content: {total_guide_chars:,} chars (~{total_guide_chars//6:,} words)")
if no_guide:
    print(f"  Missing guides: {no_guide}")

# 5. Library verification
print(f"\n[5] LIBRARY VERIFICATION")
plotly_count = 0
three_count = 0
for f in chart_files:
    with open(os.path.join(OUT_DIR, f), "r") as fh:
        content = fh.read()
    if "plotly" in content.lower():
        plotly_count += 1
    if "three" in content.lower() or "THREE" in content:
        three_count += 1
print(f"  Plotly charts: {plotly_count}")
print(f"  Three.js charts: {three_count}")

# 6. Animation mechanisms
print(f"\n[6] ANIMATED CHARTS")
animated = []
for f in chart_files:
    with open(os.path.join(OUT_DIR, f), "r") as fh:
        content = fh.read()
    has_frames = "frames" in content
    has_slider = "slider" in content.lower() or "Slider" in content
    has_play = "Play" in content or "play" in content
    has_raf = "requestAnimationFrame" in content
    if has_frames or has_slider or has_play:
        animated.append(f.split("_")[0])
print(f"  Charts with animation: {len(animated)}")
print(f"  IDs: {', '.join(animated)}")

# 7. Dashboard links
print(f"\n[7] DASHBOARD INTEGRITY")
with open(os.path.join(OUT_DIR, "index.html"), "r") as fh:
    dashboard = fh.read()
linked_charts = set(re.findall(r"op\('(\d\d_[^']+\.html)'\)", dashboard))
print(f"  Charts linked from dashboard: {len(linked_charts)}")
unlinked = set(chart_files) - linked_charts - {"chart_index.html"}
if unlinked:
    print(f"  Not linked: {sorted(unlinked)[:5]}...")

# Check dashboard has quad-panel
has_81 = "81_quad_panel_sync" in dashboard
has_index_link = "chart_index.html" in dashboard
print(f"  Quad-panel (81) linked: {'OK' if has_81 else 'MISSING'}")
print(f"  Chart index linked: {'OK' if has_index_link else 'MISSING'}")

# 8. Chart index
print(f"\n[8] CHART INDEX INTEGRITY")
with open(os.path.join(OUT_DIR, "chart_index.html"), "r") as fh:
    idx_content = fh.read()
idx_links = set(re.findall(r'href="(\d\d_[^"]+\.html)"', idx_content))
print(f"  Charts linked from index: {len(idx_links)}")
idx_missing = set(chart_files) - idx_links
if idx_missing:
    print(f"  Not in index: {sorted(idx_missing)}")
else:
    print(f"  All 81 charts indexed: OK")

# 9. ZIP verification
print(f"\n[9] ZIP PACKAGE")
zip_size = os.path.getsize(ZIP_PATH) / 1024 / 1024
with zipfile.ZipFile(ZIP_PATH, "r") as zf:
    zip_files = zf.namelist()
print(f"  ZIP size: {zip_size:.1f} MB")
print(f"  Files in ZIP: {len(zip_files)}")
print(f"  Has index.html: {'OK' if any('index.html' in f and 'chart_index' not in f for f in zip_files) else 'MISSING'}")
print(f"  Has chart_index.html: {'OK' if any('chart_index.html' in f for f in zip_files) else 'MISSING'}")

# 10. Size distribution
print(f"\n[10] SIZE DISTRIBUTION")
sizes = []
for f in chart_files:
    sz = os.path.getsize(os.path.join(OUT_DIR, f)) / 1024
    sizes.append((f, sz))
sizes.sort(key=lambda x: x[1])
total_size = sum(s for _, s in sizes)
print(f"  Smallest: {sizes[0][0]} ({sizes[0][1]:.0f} KB)")
print(f"  Largest: {sizes[-1][0]} ({sizes[-1][1]:.0f} KB)")
print(f"  Median: {sizes[len(sizes)//2][0]} ({sizes[len(sizes)//2][1]:.0f} KB)")
print(f"  Total: {total_size/1024:.1f} MB")

print(f"\n{'=' * 80}")
print("VERIFICATION COMPLETE")
print(f"{'=' * 80}")
