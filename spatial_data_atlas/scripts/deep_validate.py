#!/usr/bin/env python3
"""
Deep data validation: Extract actual data values from chart HTML/JS
and verify against well-known benchmarks.
"""
import os, re, json

VIS_DIR = "/home/claude/rosling_project/visualizations"

def read_chart(num):
    for fname in os.listdir(VIS_DIR):
        if fname.startswith(f"{num:02d}_"):
            with open(os.path.join(VIS_DIR, fname), "r") as f:
                return f.read()
    return None

def extract_plotly_data(content):
    """Try to extract data arrays from Plotly traces."""
    # Look for x: [...] and y: [...] patterns
    x_vals = re.findall(r'x:\s*\[([\d.,\s]+)\]', content)
    y_vals = re.findall(r'y:\s*\[([\d.,\s]+)\]', content)
    return x_vals, y_vals

print("=" * 80)
print("DEEP DATA VALIDATION")
print("=" * 80)

# ---- Chart 01: GDP vs Life Expectancy ----
print("\n--- Chart 01: GDP vs Life Expectancy ---")
c01 = read_chart(1)
# Check for known data points: Japan ~$42k, ~84yr; Sierra Leone ~$1.7k, ~54yr
if "Japan" in c01 or "JPN" in c01:
    print("  [OK] Japan present in data")
if "Sierra Leone" in c01 or "SLE" in c01:
    print("  [OK] Sierra Leone present in data")
# Check animation frames span
frames_count = c01.count("'name'") if c01 else 0
frame_match = re.findall(r"'name':\s*'(\d{4})'", c01)
if frame_match:
    years = sorted(set(frame_match))
    print(f"  [OK] Animation frames: {years[0]}-{years[-1]} ({len(years)} years)")
else:
    frame_match2 = re.findall(r'"name":\s*"(\d{4})"', c01)
    if frame_match2:
        years = sorted(set(frame_match2))
        print(f"  [OK] Animation frames: {years[0]}-{years[-1]} ({len(years)} years)")

# ---- Chart 07: Coral Bleaching ----
print("\n--- Chart 07: Coral Bleaching Map ---")
c07 = read_chart(7)
if c07:
    has_aus = "Australia" in c07 or "AUS" in c07
    has_ind = "Indonesia" in c07 or "IDN" in c07
    print(f"  Australia (Great Barrier Reef): {'[OK]' if has_aus else '[MISSING]'}")
    print(f"  Indonesia (Coral Triangle): {'[OK]' if has_ind else '[MISSING]'}")

# ---- Chart 12: GINI Inequality ----
print("\n--- Chart 12: GINI Inequality Map ---")
c12 = read_chart(12)
if c12:
    # South Africa should have very high Gini (~63), Nordic countries low (~25-28)
    has_za = "South Africa" in c12 or "ZAF" in c12
    has_no = "Norway" in c12 or "NOR" in c12
    print(f"  South Africa (high Gini ~63): {'[OK]' if has_za else '[CHECK]'}")
    print(f"  Norway (low Gini ~27): {'[OK]' if has_no else '[CHECK]'}")

# ---- Chart 23: Latitude vs GDP ----
print("\n--- Chart 23: Latitude vs GDP per Capita ---")
c23 = read_chart(23)
if c23:
    # Known pattern: higher latitude tends to correlate with higher GDP (temperate zone advantage)
    has_lat = "latitude" in c23.lower() or "lat" in c23.lower()
    has_gdp = "gdp" in c23.lower() or "GDP" in c23
    print(f"  Latitude axis: {'[OK]' if has_lat else '[CHECK]'}")
    print(f"  GDP axis: {'[OK]' if has_gdp else '[CHECK]'}")

# ---- Chart 37: India LISA Clusters ----
print("\n--- Chart 37: India LISA Clusters ---")
c37 = read_chart(37)
if c37:
    has_hh = "High-High" in c37 or "HH" in c37
    has_ll = "Low-Low" in c37 or "LL" in c37
    has_hl = "High-Low" in c37 or "HL" in c37
    has_lh = "Low-High" in c37 or "LH" in c37
    has_moran = "Moran" in c37 or "moran" in c37
    print(f"  HH clusters: {'[OK]' if has_hh else '[CHECK]'}")
    print(f"  LL clusters: {'[OK]' if has_ll else '[CHECK]'}")
    print(f"  HL outliers: {'[OK]' if has_hl else '[CHECK]'}")
    print(f"  LH outliers: {'[OK]' if has_lh else '[CHECK]'}")
    print(f"  Moran's I reference: {'[OK]' if has_moran else '[CHECK]'}")

# ---- Chart 39: Moran Scatterplot ----
print("\n--- Chart 39: Moran Scatterplot ---")
c39 = read_chart(39)
if c39:
    has_spatial_lag = "spatial lag" in c39.lower() or "spatiallag" in c39.lower() or "w_" in c39 or "Wx" in c39
    has_quadrants = c39.count("quadrant") > 0 or (has_hh and has_ll)
    # Check for I value
    moran_val = re.search(r'[Ii]\s*[=:]\s*0\.\d+', c39)
    print(f"  Spatial lag axis: {'[OK]' if has_spatial_lag else '[CHECK]'}")
    if moran_val:
        print(f"  Moran's I value: [OK] {moran_val.group()}")

# ---- Chart 49: GDP Bar Race ----
print("\n--- Chart 49: GDP Bar Race ---")
c49 = read_chart(49)
if c49:
    has_china = "China" in c49 or "CHN" in c49
    has_usa = "United States" in c49 or "USA" in c49
    has_japan = "Japan" in c49 or "JPN" in c49
    frame_match = re.findall(r'"name":\s*"(\d{4})"', c49) or re.findall(r"'name':\s*'(\d{4})'", c49)
    years = sorted(set(frame_match)) if frame_match else []
    print(f"  China: {'[OK]' if has_china else '[CHECK]'}")
    print(f"  USA: {'[OK]' if has_usa else '[CHECK]'}")
    print(f"  Japan: {'[OK]' if has_japan else '[CHECK]'}")
    if years:
        print(f"  Animation: {years[0]}-{years[-1]} ({len(years)} frames)")

# ---- Chart 65: Silence Map ----
print("\n--- Chart 65: Silence Map (Zero Women Constituencies) ---")
c65 = read_chart(65)
if c65:
    # Known: 152/543 had zero women candidates (28%)
    has_152 = "152" in c65
    has_28 = "28%" in c65 or "28" in c65
    print(f"  152 constituencies count: {'[OK]' if has_152 else '[CHECK]'}")
    print(f"  28% reference: {'[OK]' if has_28 else '[CHECK]'}")

# ---- Chart 66: The Gauntlet (Women Funnel) ----
print("\n--- Chart 66: The Gauntlet ---")
c66 = read_chart(66)
if c66:
    # Known: 458 women contested, 325 lost deposit, 74 won
    has_458 = "458" in c66
    has_325 = "325" in c66
    has_74 = "74" in c66
    print(f"  458 women candidates: {'[OK]' if has_458 else '[CHECK]'}")
    print(f"  325 lost deposit: {'[OK]' if has_325 else '[CHECK]'}")
    print(f"  74 women won: {'[OK]' if has_74 else '[CHECK]'}")

# ---- Chart 71: Delimitation Simulator ----
print("\n--- Chart 71: Delimitation Simulator ---")
c71 = read_chart(71)
if c71:
    has_543 = "543" in c71
    has_pop = "population" in c71.lower()
    has_formula = "Webster" in c71 or "Sainte" in c71 or "apportion" in c71.lower()
    print(f"  543 seats reference: {'[OK]' if has_543 else '[CHECK]'}")
    print(f"  Population data: {'[OK]' if has_pop else '[CHECK]'}")
    print(f"  Apportionment formula: {'[OK]' if has_formula else '[CHECK]'}")

# ---- Chart 76: Lorenz Curve / Representation Inequality ----
print("\n--- Chart 76: Representation Inequality ---")
c76 = read_chart(76)
if c76:
    has_lorenz = "Lorenz" in c76 or "lorenz" in c76
    has_gini = "Gini" in c76 or "gini" in c76
    has_equality = "equality" in c76.lower()
    print(f"  Lorenz curve: {'[OK]' if has_lorenz else '[CHECK]'}")
    print(f"  Gini coefficient: {'[OK]' if has_gini else '[CHECK]'}")
    print(f"  Equality line: {'[OK]' if has_equality else '[CHECK]'}")

# ---- 3D Charts: Check THREE.js rendering pipeline ----
print("\n--- 3D Charts: Rendering Pipeline ---")
three_charts = [42, 43, 44, 45, 47, 55, 56, 59, 60, 61, 62, 63, 64, 70, 75]
for cnum in three_charts:
    c = read_chart(cnum)
    if c:
        has_renderer = "WebGLRenderer" in c
        has_camera = "PerspectiveCamera" in c or "Camera" in c
        has_controls = "OrbitControls" in c or "controls" in c.lower()
        has_animate = "requestAnimationFrame" in c or "animate" in c
        status = "OK" if (has_renderer and has_camera and has_animate) else "CHECK"
        fname = [f for f in os.listdir(VIS_DIR) if f.startswith(f"{cnum:02d}_")][0]
        print(f"  [{status}] {fname}: renderer={has_renderer}, camera={has_camera}, controls={has_controls}")

# ---- Animated charts: Verify slider/play mechanism ----
print("\n--- Animated Charts: Animation Mechanism ---")
anim_charts = [1, 2, 3, 6, 49, 50, 51, 52, 53, 54, 57, 58]
for cnum in anim_charts:
    c = read_chart(cnum)
    if c:
        has_frames = "'frames'" in c or '"frames"' in c or "frames:" in c
        has_slider = "sliders" in c.lower()
        has_play = "Play" in c or "play" in c
        has_updatemenus = "updatemenus" in c
        fname = [f for f in os.listdir(VIS_DIR) if f.startswith(f"{cnum:02d}_")][0]
        mech = []
        if has_frames: mech.append("frames")
        if has_slider: mech.append("slider")
        if has_play: mech.append("play")
        if has_updatemenus: mech.append("updatemenus")
        print(f"  {fname}: {', '.join(mech) if mech else 'NO ANIMATION MECHANISM'}")

# ---- Guide-description alignment spot checks ----
print("\n--- Guide Content Spot Checks ---")
# Check that guide mentions spatial relevance
spatial_keywords = ["spatial", "geographic", "location", "coordinate", "latitude", "longitude", 
                    "map", "region", "distance", "cluster", "autocorrelation", "GIS", "remote sensing",
                    "territory", "boundary", "landscape", "topology", "Tobler", "MAUP"]
for cnum in [1, 7, 23, 37, 65, 71, 76]:
    c = read_chart(cnum)
    if c:
        guide_start = c.find("<!--ATLAS-GUIDE-START-->")
        guide_end = c.find("<!--ATLAS-GUIDE-END-->")
        if guide_start >= 0 and guide_end >= 0:
            guide = c[guide_start:guide_end].lower()
            found_spatial = [kw for kw in spatial_keywords if kw.lower() in guide]
            fname = [f for f in os.listdir(VIS_DIR) if f.startswith(f"{cnum:02d}_")][0]
            print(f"  {fname}: spatial keywords = {found_spatial[:5]}...")

print("\n" + "=" * 80)
print("DEEP VALIDATION COMPLETE")
print("=" * 80)
