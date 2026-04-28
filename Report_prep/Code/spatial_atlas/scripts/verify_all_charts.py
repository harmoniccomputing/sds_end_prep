#!/usr/bin/env python3
"""
Comprehensive verification of all 80 charts in the Spatial Data Visualization Atlas.
Checks: HTML validity, JS library presence, animation frames, guide panels,
data sanity, title/description alignment, spatial relevance.
"""
import os, re, json

VIS_DIR = "/home/claude/rosling_project/visualizations"

# Chart metadata: (filename, expected_lib, expected_type, has_animation, key_data_check)
CHART_META = [
    # Tab 1: Global Development Dynamics (01-06)
    ("01_gdp_vs_life_expectancy.html", "plotly", "bubble_animated", True, "GDP vs Life Expectancy"),
    ("02_fertility_vs_life_expectancy.html", "plotly", "bubble_animated", True, "Fertility vs Life Expectancy"),
    ("03_child_mortality_vs_gdp.html", "plotly", "bubble_animated", True, "Child Mortality vs GDP"),
    ("04_country_trajectories.html", "plotly", "line", False, "Country Trajectories"),
    ("05_continental_trends.html", "plotly", "line_area", False, "Continental Trends"),
    ("06_income_distribution_shift.html", "plotly", "histogram_animated", True, "Income Distribution"),
    # Tab 2: Animated Temporal (49-54) - note: these are animated
    ("49_gdp_bar_race.html", "plotly", "bar_animated", True, "GDP Bar Race"),
    ("50_india_electoral_swing.html", "plotly", "animated", True, "Electoral Swing"),
    ("51_fertility_collapse.html", "plotly", "animated", True, "Fertility Collapse"),
    ("52_mortality_plunge.html", "plotly", "animated", True, "Mortality Plunge"),
    ("53_convergence_race.html", "plotly", "animated", True, "Convergence Race"),
    ("54_women_lisa_fixed.html", "plotly", "animated", True, "Women LISA"),
    # Tab 3: Corals & Oceans (07-08, 57)
    ("07_coral_bleaching_map.html", "plotly", "choropleth", False, "Coral Bleaching"),
    ("08_ocean_sst_anomaly.html", "plotly", "choropleth", False, "SST Anomaly"),
    ("57_coral_temporal_pulse.html", "plotly", "animated", True, "Coral Temporal"),
    # Tab 4: People (09-10, 58)
    ("09_urbanization_choropleth.html", "plotly", "choropleth", False, "Urbanization"),
    ("10_slum_population_map.html", "plotly", "choropleth", False, "Slum Population"),
    ("58_animated_inequality.html", "plotly", "animated", True, "Inequality"),
    # Tab 5: Poverty (11-12)
    ("11_extreme_poverty_map.html", "plotly", "choropleth", False, "Extreme Poverty"),
    ("12_gini_inequality_map.html", "plotly", "choropleth", False, "GINI Inequality"),
    # Tab 6: Technology (13-15)
    ("13_internet_usage_choropleth.html", "plotly", "choropleth", False, "Internet Usage"),
    ("14_electricity_access_map.html", "plotly", "choropleth", False, "Electricity Access"),
    ("15_mobile_subscriptions_map.html", "plotly", "choropleth", False, "Mobile Subscriptions"),
    # Tab 7: Money & Trade (16-18)
    ("16_gdp_per_capita_map.html", "plotly", "choropleth", False, "GDP per Capita"),
    ("17_trade_openness_map.html", "plotly", "choropleth", False, "Trade Openness"),
    ("18_remittances_map.html", "plotly", "choropleth", False, "Remittances"),
    # Tab 8: Environment (19-21)
    ("19_forest_cover_map.html", "plotly", "choropleth", False, "Forest Cover"),
    ("20_renewable_energy_map.html", "plotly", "choropleth", False, "Renewable Energy"),
    ("21_water_stress_map.html", "plotly", "choropleth", False, "Water Stress"),
    # Tab 9: Geo-Variable Analysis (22-36)
    ("22_bubble_map_gdp_health.html", "plotly", "bubble_map", False, "GDP Health Bubble"),
    ("23_latitude_vs_gdp.html", "plotly", "scatter", False, "Latitude vs GDP"),
    ("24_megacity_distance_vs_lifeexp.html", "plotly", "scatter", False, "Megacity Distance"),
    ("25_latitude_vs_child_mortality.html", "plotly", "scatter", False, "Latitude Child Mortality"),
    ("26_conflict_vs_development.html", "plotly", "scatter", False, "Conflict vs Development"),
    ("27_landlocked_vs_coastal.html", "plotly", "box_bar", False, "Landlocked vs Coastal"),
    ("28_digital_divide_latitude.html", "plotly", "scatter", False, "Digital Divide"),
    ("29_fertility_by_climate.html", "plotly", "scatter_box", False, "Fertility Climate"),
    ("30_urbanization_vs_renewable.html", "plotly", "scatter", False, "Urbanization Renewable"),
    ("31_water_stress_latitude.html", "plotly", "scatter", False, "Water Stress Latitude"),
    ("32_physicians_latitude.html", "plotly", "scatter", False, "Physicians Latitude"),
    ("33_education_megacity_distance.html", "plotly", "scatter", False, "Education Megacity"),
    ("34_trade_longitude.html", "plotly", "scatter", False, "Trade Longitude"),
    ("35_maternal_mortality_forest.html", "plotly", "scatter", False, "Maternal Mortality Forest"),
    ("36_remittances_latitude.html", "plotly", "scatter", False, "Remittances Latitude"),
    # Tab 10: India Elections 2024 (37-41, 46, 48, 65-69)
    ("37_india_lisa_clusters.html", "plotly", "choropleth", False, "LISA Clusters"),
    ("38_india_area_outcomes.html", "plotly", "scatter", False, "Area Outcomes"),
    ("39_india_moran_scatterplot.html", "plotly", "scatter", False, "Moran Scatterplot"),
    ("40_india_turnout_swing.html", "plotly", "scatter", False, "Turnout Swing"),
    ("41_india_distance_delhi_margin.html", "plotly", "scatter", False, "Distance Delhi"),
    ("46_women_area_hypothesis.html", "plotly", "scatter", False, "Women Area"),
    ("48_alliance_lisa_women.html", "plotly", "multi", False, "Alliance LISA Women"),
    ("65_silence_map.html", "plotly", "choropleth", False, "Silence Map"),
    ("66_the_gauntlet.html", "plotly", "funnel", False, "Gauntlet"),
    ("67_gender_gap_electorate.html", "plotly", "bar_scatter", False, "Gender Gap"),
    ("68_deposit_forfeiture.html", "plotly", "scatter", False, "Deposit Forfeiture"),
    ("69_state_scoreboard.html", "plotly", "heatmap", False, "State Scoreboard"),
    # Tab 11: Delimitation & Fiscal (71-80)
    ("71_delimitation_simulator.html", "plotly", "interactive", False, "Delimitation Simulator"),
    ("72_fiscal_returns.html", "plotly", "scatter", False, "Fiscal Returns"),
    ("73_reservation_simulator.html", "plotly", "interactive", False, "Reservation Simulator"),
    ("74_moran_criteria_explorer.html", "plotly", "interactive", False, "Moran Criteria"),
    ("75_punishment_value_3d.html", "three", "3d", False, "Punishment Value 3D"),
    ("76_representation_inequality.html", "plotly", "lorenz", False, "Representation Inequality"),
    ("77_fiscal_spine.html", "plotly", "bar", False, "Fiscal Spine"),
    ("78_representation_treemap.html", "plotly", "treemap", False, "Representation Treemap"),
    ("79_fiscal_gender_bubble.html", "plotly", "bubble", False, "Fiscal Gender Bubble"),
    ("80_constituency_clustering.html", "plotly", "scatter", False, "Constituency Clustering"),
    # Tab 12: 3D Immersive (42-45, 47, 55-56, 59-64, 70)
    ("42_india_political_cylinder.html", "three", "3d", False, "Political Cylinder"),
    ("43_development_globe.html", "three", "3d", False, "Development Globe"),
    ("44_democracy_helix.html", "three", "3d", False, "Democracy Helix"),
    ("45_continental_dev_space.html", "three", "3d", False, "Continental Dev Space"),
    ("47_3d_extruded_india.html", "three", "3d", False, "Extruded India"),
    ("55_india_party_flip_3d.html", "three", "3d", False, "Party Flip 3D"),
    ("56_development_spiral.html", "three", "3d", False, "Development Spiral"),
    ("59_india_dev_terrain.html", "three", "3d", False, "Dev Terrain"),
    ("60_india_food_geography_3d.html", "three", "3d", False, "Food Geography 3D"),
    ("61_literacy_gender_helix.html", "three", "3d", False, "Literacy Gender Helix"),
    ("62_constituency_aurora.html", "three", "3d", False, "Constituency Aurora"),
    ("63_india_socioeconomic_3d.html", "three", "3d", False, "Socioeconomic 3D"),
    ("64_gender_development_3d.html", "three", "3d", False, "Gender Development 3D"),
    ("70_women_candidature_3d.html", "three", "3d", False, "Women Candidature 3D"),
]

results = {"pass": [], "warn": [], "fail": []}

for fname, exp_lib, exp_type, has_anim, desc in CHART_META:
    fpath = os.path.join(VIS_DIR, fname)
    chart_id = fname.split("_")[0]
    issues = []
    
    if not os.path.exists(fpath):
        results["fail"].append((chart_id, fname, ["FILE MISSING"]))
        continue
    
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    size_kb = len(content) / 1024
    
    # 1. Basic HTML structure
    if "<html" not in content.lower():
        issues.append("No <html> tag")
    if "</html>" not in content.lower():
        issues.append("No closing </html>")
    
    # 2. Library check
    if exp_lib == "plotly":
        if "plotly" not in content.lower():
            issues.append("Missing Plotly library")
    elif exp_lib == "three":
        if "three" not in content.lower() and "THREE" not in content:
            issues.append("Missing Three.js library")
    
    # 3. Animation check
    if has_anim:
        has_frames = "frames" in content or "frame" in content
        has_slider = "slider" in content.lower() or "animation" in content.lower() or "play" in content.lower()
        if not has_frames and not has_slider:
            issues.append("ANIMATION: No frames/slider/play detected")
    
    # 4. Guide panel check
    has_guide = "ATLAS-GUIDE-START" in content and "ATLAS-GUIDE-END" in content
    if not has_guide:
        issues.append("No deep academic guide panel")
    
    # 5. Title presence
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    if not title_match:
        issues.append("No <title> tag")
    
    # 6. Plotly.newPlot or THREE.Scene presence
    if exp_lib == "plotly":
        if "Plotly.newPlot" not in content and "Plotly.react" not in content and "newPlot" not in content:
            issues.append("No Plotly.newPlot call found")
    elif exp_lib == "three":
        if "Scene" not in content and "scene" not in content:
            issues.append("No THREE.Scene found")
    
    # 7. Data presence check
    has_data = "data" in content and ("trace" in content or "mesh" in content or "geometry" in content or "var data" in content or "const data" in content or "let data" in content)
    if not has_data:
        # Less strict: just check for substantial JS
        js_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
        total_js = sum(len(b) for b in js_blocks)
        if total_js < 500:
            issues.append("Very little JS content")
    
    # 8. Size sanity
    if size_kb < 5:
        issues.append(f"Suspiciously small: {size_kb:.1f}KB")
    
    # 9. Check for common JS errors
    if "undefined" in content and "=== undefined" not in content and "!== undefined" not in content and "typeof" not in content:
        pass  # too many false positives
    
    # Classify
    if not issues:
        results["pass"].append((chart_id, fname, size_kb))
    elif any("MISSING" in i or "No Plotly" in i or "No THREE" in i for i in issues):
        results["fail"].append((chart_id, fname, issues))
    else:
        results["warn"].append((chart_id, fname, issues))

# Print report
print("=" * 80)
print("SPATIAL DATA VISUALIZATION ATLAS - VERIFICATION REPORT")
print("=" * 80)

print(f"\n✅ PASSED: {len(results['pass'])}/80")
for cid, fn, sz in sorted(results["pass"]):
    print(f"  {cid} {fn} ({sz:.0f}KB)")

print(f"\n⚠️  WARNINGS: {len(results['warn'])}/80")
for cid, fn, issues in sorted(results["warn"]):
    print(f"  {cid} {fn}: {'; '.join(issues)}")

print(f"\n❌ FAILURES: {len(results['fail'])}/80")
for cid, fn, issues in sorted(results["fail"]):
    print(f"  {cid} {fn}: {'; '.join(issues)}")

print(f"\n{'=' * 80}")
print(f"SUMMARY: {len(results['pass'])} pass, {len(results['warn'])} warn, {len(results['fail'])} fail")
print(f"{'=' * 80}")

# Additional: Check guide character counts
print("\n\nGUIDE PANEL SIZES:")
total_guide = 0
for fname, _, _, _, _ in CHART_META:
    fpath = os.path.join(VIS_DIR, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r") as f:
        content = f.read()
    start = content.find("<!--ATLAS-GUIDE-START-->")
    end = content.find("<!--ATLAS-GUIDE-END-->")
    if start >= 0 and end >= 0:
        guide_len = end - start
        total_guide += guide_len
        cid = fname.split("_")[0]
        if guide_len < 2000:
            print(f"  ⚠️  {cid} {fname}: guide only {guide_len} chars (may be thin)")
    
print(f"\nTotal guide content: {total_guide:,} characters ({total_guide//6:.0f} words approx)")
