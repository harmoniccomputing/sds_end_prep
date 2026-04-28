#!/usr/bin/env python3
"""
1. Build sitemap.html - a site index with deep-linked anchors to every chart
2. Inject a floating back-link navigation bar into every chart HTML
All links are relative.
"""
import os, re
from collections import OrderedDict

VIS = "/home/claude/rosling_project/visualizations"

# ============================================================
# CHART METADATA (same canonical list)
# ============================================================
CHARTS = [
    (1, "01_gdp_vs_life_expectancy.html", "GDP vs Life Expectancy", "Animated bubble chart, 199 countries, 1990-2023", "Global Development Dynamics", "animated-bubble"),
    (2, "02_fertility_vs_life_expectancy.html", "Fertility vs Life Expectancy", "Animated bubble chart, demographic transition", "Global Development Dynamics", "animated-bubble"),
    (3, "03_child_mortality_vs_gdp.html", "Child Mortality vs GDP", "Animated scatter, inverse relationship", "Global Development Dynamics", "animated-scatter"),
    (4, "04_country_trajectories.html", "Country Development Trajectories", "Spaghetti plot, 30-year paths", "Global Development Dynamics", "line-plot"),
    (5, "05_continental_trends.html", "Continental Development Trends", "Area/line chart, continental averages", "Global Development Dynamics", "area-chart"),
    (6, "06_income_distribution_shift.html", "Income Distribution Shift", "Animated histogram, twin peaks collapse", "Global Development Dynamics", "animated-histogram"),
    (7, "07_coral_bleaching_map.html", "Coral Bleaching Risk Map", "Choropleth, thermal stress index", "Corals & Oceans", "choropleth"),
    (8, "08_ocean_sst_anomaly.html", "Ocean SST Anomaly Map", "World map, temperature anomalies", "Corals & Oceans", "choropleth"),
    (9, "09_urbanization_choropleth.html", "Global Urbanization Rates", "Choropleth, urban population %", "People", "choropleth"),
    (10, "10_slum_population_map.html", "Slum Population Distribution", "Choropleth, slum % of urban pop", "People", "choropleth"),
    (11, "11_extreme_poverty_map.html", "Extreme Poverty ($2.15/day)", "Choropleth, poverty headcount ratio", "Poverty", "choropleth"),
    (12, "12_gini_inequality_map.html", "GINI Inequality Map", "Choropleth, Gini coefficient", "Poverty", "choropleth"),
    (13, "13_internet_usage_choropleth.html", "Internet Penetration Rates", "Choropleth, internet users %", "Technology", "choropleth"),
    (14, "14_electricity_access_map.html", "Electricity Access Map", "Choropleth, electricity access %", "Technology", "choropleth"),
    (15, "15_mobile_subscriptions_map.html", "Mobile Phone Subscriptions", "Choropleth, subscriptions per 100", "Technology", "choropleth"),
    (16, "16_gdp_per_capita_map.html", "GDP per Capita World Map", "Choropleth, GDP PPP", "Money & Trade", "choropleth"),
    (17, "17_trade_openness_map.html", "Trade Openness Index", "Choropleth, (exports+imports)/GDP", "Money & Trade", "choropleth"),
    (18, "18_remittances_map.html", "Remittances as % of GDP", "Choropleth, diaspora remittances", "Money & Trade", "choropleth"),
    (19, "19_forest_cover_map.html", "Forest Cover Percentage", "Choropleth, forest area %", "Environment", "choropleth"),
    (20, "20_renewable_energy_map.html", "Renewable Energy Share", "Choropleth, renewable %", "Environment", "choropleth"),
    (21, "21_water_stress_map.html", "Water Stress Index", "Choropleth, water stress levels", "Environment", "choropleth"),
    (22, "22_bubble_map_gdp_health.html", "GDP-Health Bubble Map", "Proportional symbol map", "Geo-Variable Analysis", "bubble-map"),
    (23, "23_latitude_vs_gdp.html", "Latitude vs GDP per Capita", "Scatter, latitude hypothesis test", "Geo-Variable Analysis", "scatter"),
    (24, "24_megacity_distance_vs_lifeexp.html", "Megacity Distance vs Life Expectancy", "Scatter, proximity hypothesis", "Geo-Variable Analysis", "scatter"),
    (25, "25_latitude_vs_child_mortality.html", "Latitude vs Child Mortality", "Scatter, tropical mortality", "Geo-Variable Analysis", "scatter"),
    (26, "26_conflict_vs_development.html", "Conflict vs Development", "Scatter, conflict intensity vs HDI", "Geo-Variable Analysis", "scatter"),
    (27, "27_landlocked_vs_coastal.html", "Landlocked vs Coastal Nations", "Box/bar comparison", "Geo-Variable Analysis", "box-bar"),
    (28, "28_digital_divide_latitude.html", "Digital Divide by Latitude", "Scatter, internet vs latitude", "Geo-Variable Analysis", "scatter"),
    (29, "29_fertility_by_climate.html", "Fertility by Climate Zone", "Scatter/box, Koppen zones", "Geo-Variable Analysis", "scatter"),
    (30, "30_urbanization_vs_renewable.html", "Urbanization vs Renewable Energy", "Scatter, non-linear relationship", "Geo-Variable Analysis", "scatter"),
    (31, "31_water_stress_latitude.html", "Water Stress by Latitude", "Scatter, Hadley cell pattern", "Geo-Variable Analysis", "scatter"),
    (32, "32_physicians_latitude.html", "Physicians per 1000 by Latitude", "Scatter, Cuba outlier", "Geo-Variable Analysis", "scatter"),
    (33, "33_education_megacity_distance.html", "Education vs Megacity Distance", "Scatter, knowledge diffusion", "Geo-Variable Analysis", "scatter"),
    (34, "34_trade_longitude.html", "Trade Openness by Longitude", "Scatter, Eurasian trade belt", "Geo-Variable Analysis", "scatter"),
    (35, "35_maternal_mortality_forest.html", "Maternal Mortality vs Forest Cover", "Scatter, remoteness proxy", "Geo-Variable Analysis", "scatter"),
    (36, "36_remittances_latitude.html", "Remittances by Latitude", "Scatter, migration corridors", "Geo-Variable Analysis", "scatter"),
    (37, "37_india_lisa_clusters.html", "LISA Clusters (Voter Turnout)", "Spatial autocorrelation map, Moran's I=0.642", "India Elections 2024", "lisa-map"),
    (38, "38_india_area_outcomes.html", "Constituency Area vs Outcomes", "Scatter, area-turnout correlation", "India Elections 2024", "scatter"),
    (39, "39_india_moran_scatterplot.html", "Moran Scatterplot", "Spatial lag vs value, quadrants", "India Elections 2024", "scatter"),
    (40, "40_india_turnout_swing.html", "Turnout vs Swing Analysis", "Scatter, mobilization hypothesis", "India Elections 2024", "scatter"),
    (41, "41_india_distance_delhi_margin.html", "Distance from Delhi vs Margin", "Scatter, Delhi distance hypothesis", "India Elections 2024", "scatter"),
    (42, "42_india_political_cylinder.html", "India Political Cylinder", "3D cylindrical projection, Three.js", "3D Immersive", "3d-threejs"),
    (43, "43_development_globe.html", "Development Globe", "3D interactive globe, GDP extrusion", "3D Immersive", "3d-threejs"),
    (44, "44_democracy_helix.html", "Democracy-Development Helix", "3D DNA-like double helix", "3D Immersive", "3d-threejs"),
    (45, "45_continental_dev_space.html", "Continental Development Space", "3D scatter, GDP-health-education", "3D Immersive", "3d-plotly"),
    (46, "46_women_area_hypothesis.html", "Women Candidates vs Area", "Scatter, area-gender test", "India Elections 2024", "scatter"),
    (47, "47_3d_extruded_india.html", "3D Extruded India Map", "3D bar map, switchable metrics", "3D Immersive", "3d-threejs"),
    (48, "48_alliance_lisa_women.html", "Alliance LISA & Women Analysis", "Multi-panel LISA + gender", "India Elections 2024", "multi-panel"),
    (49, "49_gdp_bar_race.html", "GDP Bar Chart Race", "Animated bar race, top 15, 1992-2022", "Animated Temporal", "animated-bar"),
    (50, "50_india_electoral_swing.html", "India Electoral Swing Animation", "Animated constituency map", "Animated Temporal", "animated-map"),
    (51, "51_fertility_collapse.html", "Fertility Rate Collapse", "Animated scatter, TFR decline", "Animated Temporal", "animated-scatter"),
    (52, "52_mortality_plunge.html", "Child Mortality Plunge", "Animated scatter, mortality decline", "Animated Temporal", "animated-scatter"),
    (53, "53_convergence_race.html", "Economic Convergence Race", "Animated, catch-up hypothesis", "Animated Temporal", "animated-scatter"),
    (54, "54_women_lisa_fixed.html", "Women LISA Spatial Animation", "Animated LISA, women candidature", "Animated Temporal", "animated-lisa"),
    (55, "55_india_party_flip_3d.html", "India Party Flip 3D", "3D flip visualization, pulsing rings", "3D Immersive", "3d-threejs"),
    (56, "56_development_spiral.html", "Development Spiral", "3D spiral, GDP-health-time", "3D Immersive", "3d-threejs"),
    (57, "57_coral_temporal_pulse.html", "Coral Bleaching Temporal Pulse", "Animated, El Nino events", "Corals & Oceans", "animated-temporal"),
    (58, "58_animated_inequality.html", "Animated Global Inequality", "Animated Gini evolution", "People", "animated-scatter"),
    (59, "59_india_dev_terrain.html", "India Development Terrain", "3D terrain, switchable metrics", "3D Immersive", "3d-threejs"),
    (60, "60_india_food_geography_3d.html", "India Food Geography 3D", "3D crop production landscape", "3D Immersive", "3d-plotly"),
    (61, "61_literacy_gender_helix.html", "Literacy-Gender Helix", "3D helix, male vs female literacy", "3D Immersive", "3d-threejs"),
    (62, "62_constituency_aurora.html", "Constituency Aurora", "3D particle field, data art", "3D Immersive", "3d-threejs"),
    (63, "63_india_socioeconomic_3d.html", "India Socioeconomic Landscape 3D", "3D scatter, literacy-GDP-HDI", "3D Immersive", "3d-plotly"),
    (64, "64_gender_development_3d.html", "Gender-Development 3D Surface", "3D surface, gender-dev interaction", "3D Immersive", "3d-plotly"),
    (65, "65_silence_map.html", "The Silence Map", "Choropleth, 152 zero-women constituencies", "India Elections 2024", "choropleth"),
    (66, "66_the_gauntlet.html", "The Gauntlet (Women Funnel)", "Funnel, 458 to 74 women", "India Elections 2024", "funnel"),
    (67, "67_gender_gap_electorate.html", "Gender Gap in Electorate", "Bar/scatter, male-female voter gap", "India Elections 2024", "bar-scatter"),
    (68, "68_deposit_forfeiture.html", "Deposit Forfeiture Analysis", "Scatter, forfeiture predictors", "India Elections 2024", "scatter"),
    (69, "69_state_scoreboard.html", "State Gender Scoreboard", "Heatmap, multi-dimensional ranking", "India Elections 2024", "heatmap"),
    (70, "70_women_candidature_3d.html", "Women Candidature 3D Landscape", "3D terrain, women candidature", "3D Immersive", "3d-plotly"),
    (71, "71_delimitation_simulator.html", "Delimitation Seat Simulator", "Interactive, Webster/Sainte-Lague", "Delimitation & Fiscal", "interactive"),
    (72, "72_fiscal_returns.html", "Fiscal Returns by State", "Scatter, contribution vs receipts", "Delimitation & Fiscal", "scatter"),
    (73, "73_reservation_simulator.html", "Reservation Impact Simulator", "Interactive slider, women quotas", "Delimitation & Fiscal", "interactive"),
    (74, "74_moran_criteria_explorer.html", "Multi-Criteria Moran Explorer", "Interactive, Moran's I comparison", "Delimitation & Fiscal", "interactive"),
    (75, "75_punishment_value_3d.html", "Demographic Punishment Value 3D", "3D surface, population-fertility-seats", "Delimitation & Fiscal", "3d-plotly"),
    (76, "76_representation_inequality.html", "Representation Inequality (Lorenz)", "Lorenz curve, interactive slider", "Delimitation & Fiscal", "interactive"),
    (77, "77_fiscal_spine.html", "Fiscal Spine Chart", "Diverging bar, south-to-north", "Delimitation & Fiscal", "bar"),
    (78, "78_representation_treemap.html", "Representation Treemap", "Treemap, seats by state", "Delimitation & Fiscal", "treemap"),
    (79, "79_fiscal_gender_bubble.html", "Fiscal-Gender Nexus Bubble", "Bubble, fiscal x gender x development", "Delimitation & Fiscal", "bubble"),
    (80, "80_constituency_clustering.html", "Constituency Clustering (k-Means)", "Color map, 5 natural clusters", "Delimitation & Fiscal", "scatter"),
    (81, "81_quad_panel_sync.html", "Four Lenses: Global Development", "Quad-panel sync, year slider 1990-2023", "Synchronized Multi-View", "quad-sync"),
    (82, "82_health_environment_sync.html", "Health-Environment Nexus", "Quad-panel sync, aridity-mortality", "Synchronized Multi-View", "quad-sync"),
    (83, "83_tech_inequality_sync.html", "Technology-Inequality Divergence", "Quad-panel sync, digital divide", "Synchronized Multi-View", "quad-sync"),
    (84, "84_india_threshold_sync.html", "India Electoral Threshold Explorer", "Quad-panel sync, turnout threshold", "Synchronized Multi-View", "quad-sync"),
]

# Group by topic
groups = OrderedDict()
for num, fname, title, desc, group, chart_type in CHARTS:
    if group not in groups:
        groups[group] = []
    groups[group].append((num, fname, title, desc, chart_type))

# Build filename -> (num, title, group) lookup
chart_lookup = {}
for num, fname, title, desc, group, ct in CHARTS:
    chart_lookup[fname] = (num, title, group)

GROUP_COLORS = {
    "Global Development Dynamics": "#00D5E0",
    "Animated Temporal": "#FF5872",
    "Corals & Oceans": "#0099CC",
    "People": "#B088F9",
    "Poverty": "#FF8C00",
    "Technology": "#7CFC00",
    "Money & Trade": "#FFD700",
    "Environment": "#2ECC71",
    "Geo-Variable Analysis": "#00D5E0",
    "India Elections 2024": "#FF5872",
    "Delimitation & Fiscal": "#FFD700",
    "3D Immersive": "#B088F9",
    "Synchronized Multi-View": "#00D5E0",
}

TYPE_LABELS = {
    "animated-bubble": "Animated Bubble", "animated-scatter": "Animated Scatter",
    "animated-histogram": "Animated Histogram", "animated-bar": "Animated Bar Race",
    "animated-map": "Animated Map", "animated-lisa": "Animated LISA",
    "animated-temporal": "Animated Temporal", "choropleth": "Choropleth",
    "scatter": "Scatter Plot", "line-plot": "Line Plot", "area-chart": "Area Chart",
    "bubble-map": "Bubble Map", "box-bar": "Box/Bar", "bar-scatter": "Bar/Scatter",
    "heatmap": "Heatmap", "funnel": "Funnel", "multi-panel": "Multi-Panel",
    "lisa-map": "LISA Map", "3d-threejs": "3D (Three.js)", "3d-plotly": "3D (Plotly)",
    "interactive": "Interactive", "quad-sync": "Quad-Panel Sync",
    "bar": "Bar Chart", "treemap": "Treemap", "bubble": "Bubble Chart",
}

# ============================================================
# 1. BUILD SITEMAP PAGE
# ============================================================
toc_links = ""
body_sections = ""
total = 0

for group_name, charts in groups.items():
    gid = re.sub(r'[^a-z0-9]', '-', group_name.lower()).strip('-')
    color = GROUP_COLORS.get(group_name, "#00D5E0")
    toc_links += f'<a href="#g-{gid}" class="toc-link" style="--gc:{color}">{group_name} <span class="toc-count">{len(charts)}</span></a>\n'
    
    rows = ""
    for num, fname, title, desc, chart_type in charts:
        anchor = f"chart-{num:02d}"
        type_label = TYPE_LABELS.get(chart_type, chart_type)
        rows += f"""<tr id="{anchor}">
<td class="col-num" style="color:{color}">#{num:02d}</td>
<td class="col-title"><a href="{fname}">{title}</a></td>
<td class="col-desc">{desc}</td>
<td class="col-type"><span class="type-badge" style="--tc:{color}">{type_label}</span></td>
<td class="col-link"><a href="{fname}" class="open-link" style="color:{color}">Open &rarr;</a></td>
</tr>
"""
        total += 1
    
    body_sections += f"""
<div class="section" id="g-{gid}">
<h2 style="border-color:{color}"><span class="dot" style="background:{color}"></span>{group_name}</h2>
<table class="chart-table">
<thead><tr><th>#</th><th>Chart Title</th><th>Description</th><th>Type</th><th></th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
"""

sitemap_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="author" content="Vishakha Agrawal">
<title>Site Index | Spatial Data Visualization Atlas</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@300;400;600;700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#080B13;color:#c0c8d4;font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif}}
a{{color:#00D5E0;text-decoration:none}}a:hover{{text-decoration:underline}}

.page-header{{text-align:center;padding:36px 20px 16px;border-bottom:1px solid #1a2233}}
.page-header h1{{font-family:'Playfair Display',Georgia,serif;color:#F0F4F8;font-size:2rem;margin-bottom:6px}}
.page-header .byline{{color:#64748B;font-size:.82rem;margin-bottom:10px}}
.page-header .stats{{color:#94A3B8;font-size:.88rem}}
.page-header .stats b{{color:#FFD700;font-family:'Playfair Display',serif;font-size:1.1rem}}

.nav-bar{{display:flex;gap:12px;justify-content:center;padding:14px 20px;border-bottom:1px solid #1a2233;flex-wrap:wrap}}
.nav-bar a{{font-size:.82rem;color:#94A3B8;border:1px solid #1a2233;padding:5px 14px;border-radius:4px;transition:all .2s}}
.nav-bar a:hover{{border-color:#00D5E0;color:#00D5E0;text-decoration:none}}

.toc{{max-width:1100px;margin:20px auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:8px;justify-content:center}}
.toc-link{{font-size:.78rem;padding:5px 14px;border-radius:20px;background:rgba(255,255,255,.03);border:1px solid #1a2233;color:#94A3B8;transition:all .2s;display:flex;align-items:center;gap:6px}}
.toc-link:hover{{border-color:var(--gc);color:var(--gc);text-decoration:none;background:rgba(0,213,224,.04)}}
.toc-count{{font-size:.65rem;background:#1a2233;padding:1px 6px;border-radius:10px}}

.search-row{{text-align:center;margin:16px auto;max-width:500px;padding:0 20px}}
.search-row input{{width:100%;background:#0D1117;border:1px solid #1a2233;color:#F0F4F8;padding:10px 18px;border-radius:6px;font-size:.88rem;font-family:inherit}}
.search-row input:focus{{outline:none;border-color:#00D5E0}}

.content{{max-width:1100px;margin:0 auto;padding:0 20px 60px}}

.section{{margin:28px 0}}
.section h2{{font-family:'Playfair Display',Georgia,serif;color:#F0F4F8;font-size:1.15rem;padding:8px 0;margin-bottom:10px;border-bottom:2px solid;display:flex;align-items:center;gap:8px}}
.dot{{width:8px;height:8px;border-radius:50%;display:inline-block}}

.chart-table{{width:100%;border-collapse:collapse;font-size:.82rem}}
.chart-table th{{text-align:left;color:#64748B;font-weight:600;font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;padding:6px 10px;border-bottom:1px solid #1a2233}}
.chart-table td{{padding:8px 10px;border-bottom:1px solid rgba(26,34,51,.5);vertical-align:top}}
.chart-table tr:hover{{background:rgba(0,213,224,.02)}}
.chart-table tr:target{{background:rgba(255,215,0,.06);outline:1px solid rgba(255,215,0,.15)}}

.col-num{{font-family:'Playfair Display',serif;font-weight:700;font-size:.95rem;width:40px;white-space:nowrap}}
.col-title{{font-weight:600;color:#F0F4F8;min-width:180px}}
.col-title a{{color:#F0F4F8}}
.col-title a:hover{{color:#00D5E0}}
.col-desc{{color:#7B8CA3;font-size:.78rem;line-height:1.5}}
.col-type{{width:120px;white-space:nowrap}}
.type-badge{{font-size:.65rem;padding:2px 8px;border-radius:12px;background:rgba(0,213,224,.06);border:1px solid rgba(0,213,224,.12);color:var(--tc)}}
.col-link{{width:60px;text-align:right;white-space:nowrap}}
.open-link{{font-size:.78rem;font-weight:600}}

.footer{{text-align:center;padding:20px;color:#4a5568;font-size:.75rem;border-top:1px solid #1a2233;margin-top:30px}}

@media(max-width:768px){{
    .col-desc,.col-type{{display:none}}
    .chart-table td,.chart-table th{{padding:6px}}
}}
</style>
</head>
<body>
<div class="page-header">
<h1>Site Index</h1>
<div class="byline">By Vishakha Agrawal | Lab for Spatial Informatics, IIIT Hyderabad</div>
<div class="stats"><b>{total}</b> charts in <b>{len(groups)}</b> topic groups. Every chart is deep-linked and directly accessible.</div>
</div>

<div class="nav-bar">
<a href="index.html">&larr; Dashboard</a>
<a href="chart_index.html">Chart Index (cards)</a>
<a href="guided_tour.html">&#9654; Guided Tour</a>
</div>

<div class="toc">
{toc_links}
</div>

<div class="search-row">
<input type="text" id="q" placeholder="Search by title, type, or topic..." oninput="filter(this.value)">
</div>

<div class="content" id="content">
{body_sections}
</div>

<div class="footer">
Spatial &amp; Geographical Data Visualization Atlas. All links are relative. Permalink to any chart using <code>#chart-NN</code> anchors.
</div>

<script>
function filter(q) {{
    q = q.toLowerCase().trim();
    document.querySelectorAll('.chart-table tr').forEach(tr => {{
        if (tr.closest('thead')) return;
        tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
    }});
    document.querySelectorAll('.section').forEach(sec => {{
        const visible = sec.querySelectorAll('tbody tr[style=""], tbody tr:not([style])');
        let any = false;
        sec.querySelectorAll('tbody tr').forEach(tr => {{ if (tr.style.display !== 'none') any = true; }});
        sec.style.display = any ? '' : 'none';
    }});
}}
// Highlight row if hash target
if (window.location.hash) {{
    const el = document.querySelector(window.location.hash);
    if (el) {{ el.scrollIntoView({{ behavior: 'smooth', block: 'center' }}); }}
}}
</script>
</body>
</html>"""

with open(os.path.join(VIS, "sitemap.html"), "w") as f:
    f.write(sitemap_html)
print(f"sitemap.html: {len(sitemap_html)/1024:.1f} KB, {total} deep-linked charts")

# ============================================================
# 2. INJECT BACK-LINK BAR INTO ALL CHART PAGES
# ============================================================

# The back-link bar: a small fixed-position strip at top of each chart page
# with links to index, sitemap, and prev/next chart navigation.
# All relative links.

# Build prev/next mapping
chart_files_ordered = [fname for _, fname, _, _, _, _ in CHARTS]

def get_backlink_html(fname):
    """Generate the floating back-link bar for a given chart file."""
    info = chart_lookup.get(fname)
    if not info:
        return ""
    num, title, group = info
    color = GROUP_COLORS.get(group, "#00D5E0")
    
    # Find prev/next
    idx = chart_files_ordered.index(fname) if fname in chart_files_ordered else -1
    prev_file = chart_files_ordered[idx - 1] if idx > 0 else None
    next_file = chart_files_ordered[idx + 1] if idx < len(chart_files_ordered) - 1 else None
    
    prev_link = f'<a href="{prev_file}" class="bl-nav" title="Previous chart">&larr; Prev</a>' if prev_file else '<span class="bl-nav bl-disabled">&larr; Prev</span>'
    next_link = f'<a href="{next_file}" class="bl-nav" title="Next chart">Next &rarr;</a>' if next_file else '<span class="bl-nav bl-disabled">Next &rarr;</span>'
    
    return f"""<!--BACKLINK-START-->
<div id="atlasBacklink" style="position:fixed;top:0;left:0;right:0;z-index:9999;background:rgba(8,11,19,.92);backdrop-filter:blur(6px);border-bottom:1px solid #1a2233;padding:6px 16px;display:flex;align-items:center;gap:10px;font-family:'Source Sans 3',system-ui,sans-serif;font-size:.76rem;transition:transform .3s ease">
<a href="index.html" style="color:#00D5E0;text-decoration:none;font-weight:600;white-space:nowrap">&#9664; Atlas</a>
<span style="color:#1a2233">|</span>
<a href="sitemap.html#chart-{num:02d}" style="color:#94A3B8;text-decoration:none;white-space:nowrap">Site Index</a>
<span style="color:#1a2233">|</span>
<a href="chart_index.html" style="color:#94A3B8;text-decoration:none;white-space:nowrap">Chart Index</a>
<span style="flex:1"></span>
<span style="color:{color};font-weight:600;white-space:nowrap">#{num:02d}</span>
<span style="color:#64748B;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:250px">{title}</span>
<span style="flex:1"></span>
{prev_link.replace('class="bl-nav"', 'style="color:#94A3B8;text-decoration:none;white-space:nowrap"').replace('class="bl-nav bl-disabled"', 'style="color:#2a3040;white-space:nowrap;pointer-events:none"')}
{next_link.replace('class="bl-nav"', 'style="color:#94A3B8;text-decoration:none;white-space:nowrap"').replace('class="bl-nav bl-disabled"', 'style="color:#2a3040;white-space:nowrap;pointer-events:none"')}
<button onclick="document.getElementById('atlasBacklink').style.transform='translateY(-100%)'" style="background:none;border:none;color:#4a5568;cursor:pointer;font-size:.9rem;padding:0 2px" title="Hide bar">&times;</button>
</div>
<div style="height:32px"></div>
<!--BACKLINK-END-->"""

injected = 0
skipped = 0

for fname in sorted(os.listdir(VIS)):
    if not fname.endswith(".html"):
        continue
    # Skip non-chart pages
    if fname in ("index.html", "chart_index.html", "guided_tour.html", "sitemap.html", "index.html.bak"):
        continue
    if not fname[0].isdigit():
        continue
    
    fpath = os.path.join(VIS, fname)
    with open(fpath, "r") as f:
        content = f.read()
    
    # Remove any existing backlink
    content = re.sub(r'<!--BACKLINK-START-->.*?<!--BACKLINK-END-->', '', content, flags=re.DOTALL)
    
    # Generate backlink bar
    bar = get_backlink_html(fname)
    if not bar:
        skipped += 1
        continue
    
    # Insert after <body> tag
    if "<body>" in content:
        content = content.replace("<body>", "<body>\n" + bar, 1)
    elif "<body " in content:
        idx = content.find(">", content.find("<body "))
        if idx > 0:
            content = content[:idx+1] + "\n" + bar + content[idx+1:]
    else:
        # No body tag, insert at start
        content = bar + "\n" + content
    
    with open(fpath, "w") as f:
        f.write(content)
    injected += 1

print(f"Back-links injected: {injected} charts, {skipped} skipped")

# ============================================================
# 3. ADD SITEMAP LINK TO DASHBOARD AND OTHER INDEX PAGES
# ============================================================
# Add to dashboard nav/footer
for page in ["index.html", "chart_index.html", "guided_tour.html"]:
    fpath = os.path.join(VIS, page)
    with open(fpath, "r") as f:
        content = f.read()
    if "sitemap.html" not in content:
        if page == "index.html":
            # Add to sources footer
            content = content.replace(
                'Complete Chart Index (all 84 charts grouped by topic)',
                'Complete Chart Index (all 84 charts grouped by topic)</a></b> | <b style="color:#00D5E0">&#128279; <a href="sitemap.html" style="color:#00D5E0">Site Index (deep links)</a></b'
            )
        elif page == "chart_index.html":
            content = content.replace(
                '<a href="index.html">&larr; Back to Dashboard</a>',
                '<a href="index.html">&larr; Back to Dashboard</a> &nbsp; <a href="sitemap.html">&#128279; Site Index</a>'
            )
        elif page == "guided_tour.html":
            # Tour already has its own nav, just ensure we can get to sitemap from end screen
            pass
        with open(fpath, "w") as f:
            f.write(content)

print("Sitemap links added to dashboard and chart index")

# ============================================================
# VERIFY
# ============================================================
print("\nVERIFICATION:")

# Check sitemap has all 84 links
with open(os.path.join(VIS, "sitemap.html"), "r") as f:
    sm = f.read()
sm_links = re.findall(r'href="(\d\d_[^"]+\.html)"', sm)
sm_anchors = re.findall(r'id="(chart-\d\d)"', sm)
print(f"  Sitemap: {len(set(sm_links))} unique chart links, {len(sm_anchors)} anchors")

# Check back-links injected
backlinked = 0
for fname in sorted(os.listdir(VIS)):
    if fname[0].isdigit() and fname.endswith(".html"):
        with open(os.path.join(VIS, fname), "r") as f:
            if "BACKLINK-START" in f.read():
                backlinked += 1
print(f"  Charts with back-links: {backlinked}/84")

# Check all back-links use relative paths (no http://)
has_absolute = False
for fname in sorted(os.listdir(VIS)):
    if fname[0].isdigit() and fname.endswith(".html"):
        with open(os.path.join(VIS, fname), "r") as f:
            bl_section = re.search(r'<!--BACKLINK-START-->(.*?)<!--BACKLINK-END-->', f.read(), re.DOTALL)
            if bl_section and ("http://" in bl_section.group(1) or "https://" in bl_section.group(1)):
                has_absolute = True
                print(f"    ABSOLUTE URL in {fname}")
print(f"  All links relative: {'YES' if not has_absolute else 'NO'}")

# Check prev/next navigation chain
print(f"  Navigation chain: {chart_files_ordered[0]} -> ... -> {chart_files_ordered[-1]}")
