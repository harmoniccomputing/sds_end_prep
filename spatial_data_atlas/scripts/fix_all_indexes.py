#!/usr/bin/env python3
"""
Fix all discrepancies between dashboard and chart index.
Issues found:
1. Dashboard subtitle says "81 interactive" instead of "84 interactive"
2. Dashboard footer link says "all 81 charts" instead of "all 84 charts"  
3. Chart index: charts 82-84 placed outside the Synchronized section
4. Chart index: Synchronized group count says "(1 charts)" instead of "(4 charts)"
Strategy: Rebuild chart_index.html from scratch, fix dashboard text.
"""
import os, shutil

VIS = "/home/claude/rosling_project/visualizations"
OUT = "/mnt/user-data/outputs/rosling_gapminder"

# ========== FIX 1: REBUILD CHART INDEX FROM SCRATCH ==========

CHARTS = [
    # (num, filename, title, description, bottomline, group)
    (1, "01_gdp_vs_life_expectancy.html", "GDP vs Life Expectancy", "Animated bubble chart showing the Preston Curve across 199 countries (1990-2023). Bubble size = population, color = continent.", "Richer countries live longer, but the relationship is logarithmic: the first $5,000 matters enormously; the next $50,000 barely moves the needle.", "Global Development Dynamics"),
    (2, "02_fertility_vs_life_expectancy.html", "Fertility vs Life Expectancy", "Animated bubble chart tracing the demographic transition: as life expectancy rises, fertility falls. 1990-2023.", "The world has converged dramatically: in 1990, fertility ranged from 1.2 to 7.5; by 2023, most countries cluster between 1.5 and 4.0.", "Global Development Dynamics"),
    (3, "03_child_mortality_vs_gdp.html", "Child Mortality vs GDP", "Animated scatter showing the inverse relationship between wealth and under-5 mortality. Log-scale GDP axis.", "Child mortality has halved globally since 1990, but the poorest countries still lose 10x more children than the richest.", "Global Development Dynamics"),
    (4, "04_country_trajectories.html", "Country Development Trajectories", "Spaghetti plot tracing individual country paths through GDP-health space over three decades.", "Most trajectories move right and up (richer and healthier), but conflict zones show dramatic reversals.", "Global Development Dynamics"),
    (5, "05_continental_trends.html", "Continental Development Trends", "Area/line chart comparing continental averages across key development indicators over time.", "Asia's rise is the dominant story: its average GDP per capita tripled in 30 years, driven by China and India.", "Global Development Dynamics"),
    (6, "06_income_distribution_shift.html", "Income Distribution Shift", "Animated histogram showing how the global income distribution has changed shape from 1990 to 2023.", "The bimodal 'twin peaks' distribution of 1990 (rich vs poor) has collapsed into a single peak centered at middle income.", "Global Development Dynamics"),
    (49, "49_gdp_bar_race.html", "GDP Bar Chart Race", "Animated bar race showing the top 15 countries by GDP per capita (PPP) racing from 1992 to 2022.", "Ireland's meteoric rise is partly a statistical artifact of corporate tax haven effects; Qatar's lead reflects hydrocarbon wealth divided by a tiny citizen population.", "Animated Temporal"),
    (50, "50_india_electoral_swing.html", "India Electoral Swing Animation", "Animated map showing constituency-level electoral swings across Indian states.", "Electoral swings are spatially clustered: neighboring constituencies tend to swing in the same direction, following regional political waves.", "Animated Temporal"),
    (51, "51_fertility_collapse.html", "Fertility Rate Collapse", "Animated chart showing the dramatic decline of fertility rates worldwide.", "Bangladesh's fertility dropped from 6.2 to 2.0 in one generation without reaching high income, disproving the 'wealth causes low fertility' hypothesis.", "Animated Temporal"),
    (52, "52_mortality_plunge.html", "Child Mortality Plunge", "Animated visualization of the global decline in under-5 mortality rates from 1990 onward.", "Sub-Saharan Africa saw the steepest absolute declines after 2005, driven by anti-malaria bed nets and oral rehydration therapy.", "Animated Temporal"),
    (53, "53_convergence_race.html", "Economic Convergence Race", "Animated comparison showing whether poor countries are catching up to rich ones in GDP per capita.", "Conditional convergence is real (poor countries grow faster IF they have good institutions), but unconditional convergence remains elusive.", "Animated Temporal"),
    (54, "54_women_lisa_fixed.html", "Women LISA Spatial Animation", "Animated Local Indicators of Spatial Association for women's candidature patterns across Indian constituencies.", "Spatial clustering of women's political exclusion is persistent: the same 'silence zones' appear year after year.", "Animated Temporal"),
    (7, "07_coral_bleaching_map.html", "Coral Bleaching Risk Map", "Choropleth map showing global coral reef bleaching severity, colored by thermal stress index.", "Bleaching severity follows equatorial SST anomalies, with the Coral Triangle most at risk due to narrow thermal tolerance.", "Corals & Oceans"),
    (8, "08_ocean_sst_anomaly.html", "Ocean SST Anomaly Map", "World map of sea surface temperature anomalies relative to long-term baseline.", "The spatial pattern of warming is not uniform: Arctic amplification is 2-3x the global average.", "Corals & Oceans"),
    (57, "57_coral_temporal_pulse.html", "Coral Bleaching Temporal Pulse", "Animated time series showing the pulse-like nature of mass bleaching events tied to El Nino cycles.", "The three global mass bleaching events (1998, 2010, 2015-16) all coincided with El Nino warm phases.", "Corals & Oceans"),
    (9, "09_urbanization_choropleth.html", "Global Urbanization Rates", "Choropleth map of urban population percentage by country.", "Urbanization is the single strongest spatial predictor of development outcomes.", "People"),
    (10, "10_slum_population_map.html", "Slum Population Distribution", "Map showing the percentage of urban population living in slum conditions by country.", "90% of the world's slum dwellers live in three regions: sub-Saharan Africa, South Asia, and East Asia.", "People"),
    (58, "58_animated_inequality.html", "Animated Global Inequality", "Animated visualization of the Gini coefficient evolution across countries over time.", "Latin America has been reducing inequality since 2000, while several Asian economies have seen rising inequality.", "People"),
    (11, "11_extreme_poverty_map.html", "Extreme Poverty ($2.15/day)", "Choropleth showing the percentage of population living below $2.15/day (2017 PPP).", "70% of the extreme poor now live in sub-Saharan Africa.", "Poverty"),
    (12, "12_gini_inequality_map.html", "GINI Inequality Map", "World map colored by Gini coefficient.", "South Africa (Gini ~63) and the Nordic countries (Gini ~25-28) represent the extremes.", "Poverty"),
    (13, "13_internet_usage_choropleth.html", "Internet Penetration Rates", "Choropleth of internet users as percentage of population.", "The digital divide mirrors the development divide: sub-Saharan Africa averages 30% vs 90%+ in Europe.", "Technology"),
    (14, "14_electricity_access_map.html", "Electricity Access Map", "Map showing percentage of population with access to electricity.", "600 million Africans still lack electricity access.", "Technology"),
    (15, "15_mobile_subscriptions_map.html", "Mobile Phone Subscriptions", "Choropleth of mobile subscriptions per 100 people.", "Mobile leapfrogging: Africa skipped landlines entirely, and M-Pesa demonstrates spatial network effects.", "Technology"),
    (16, "16_gdp_per_capita_map.html", "GDP per Capita World Map", "Choropleth of GDP per capita (PPP) across all countries.", "The 30 richest countries are overwhelmingly above 30 degrees latitude.", "Money & Trade"),
    (17, "17_trade_openness_map.html", "Trade Openness Index", "Map of trade openness (exports + imports as % of GDP).", "Landlocked nations average 20% lower trade openness than coastal ones.", "Money & Trade"),
    (18, "18_remittances_map.html", "Remittances as % of GDP", "Choropleth showing diaspora remittance dependency.", "Tajikistan, Tonga, and Nepal receive 20-30% of GDP from remittances.", "Money & Trade"),
    (19, "19_forest_cover_map.html", "Forest Cover Percentage", "World map of forest area as percentage of total land.", "Deforestation follows the forest transition curve.", "Environment"),
    (20, "20_renewable_energy_map.html", "Renewable Energy Share", "Choropleth of renewable energy percentage.", "Iceland (100% renewable) vs Saudi Arabia (<1%): energy transition is a spatial problem.", "Environment"),
    (21, "21_water_stress_map.html", "Water Stress Index", "Map of water stress levels by country.", "The MENA region has the highest stress, but South Asia is catching up.", "Environment"),
    (22, "22_bubble_map_gdp_health.html", "GDP-Health Bubble Map", "Proportional symbol map overlaying GDP and health on geographic coordinates.", "Spatial clustering of prosperity is visible at continental scale.", "Geo-Variable Analysis"),
    (23, "23_latitude_vs_gdp.html", "Latitude vs GDP per Capita", "Scatter plot testing the 'latitude hypothesis'.", "The correlation is r=0.45 for Northern Hemisphere but near zero for Southern.", "Geo-Variable Analysis"),
    (24, "24_megacity_distance_vs_lifeexp.html", "Distance from Megacity vs Life Expectancy", "Scatter of distance from nearest megacity vs. life expectancy.", "Countries far from megacities have lower life expectancy.", "Geo-Variable Analysis"),
    (25, "25_latitude_vs_child_mortality.html", "Latitude vs Child Mortality", "Scatter showing latitude correlation with under-5 mortality.", "Tropical countries have 5x higher child mortality than temperate ones.", "Geo-Variable Analysis"),
    (26, "26_conflict_vs_development.html", "Conflict vs Development", "Scatter of armed conflict intensity vs. HDI.", "Countries neighboring conflict zones show 0.05-0.15 lower HDI.", "Geo-Variable Analysis"),
    (27, "27_landlocked_vs_coastal.html", "Landlocked vs Coastal Nations", "Box/bar comparison of development indicators.", "Landlocked countries have 40% lower trade volumes and 0.1 lower HDI.", "Geo-Variable Analysis"),
    (28, "28_digital_divide_latitude.html", "Digital Divide by Latitude", "Scatter of internet penetration vs. latitude.", "Internet access follows the same latitude gradient as GDP.", "Geo-Variable Analysis"),
    (29, "29_fertility_by_climate.html", "Fertility Rate by Climate Zone", "Scatter/box of TFR grouped by Koppen climate classification.", "Tropical climates average TFR of 4.2 vs. 1.6 for temperate.", "Geo-Variable Analysis"),
    (30, "30_urbanization_vs_renewable.html", "Urbanization vs Renewable Energy", "Scatter of urbanization rate vs. renewable energy share.", "The relationship is non-linear: very rural and very urban countries score higher.", "Geo-Variable Analysis"),
    (31, "31_water_stress_latitude.html", "Water Stress by Latitude", "Scatter showing water stress variation with latitude.", "The 20-35 degree band is the global hotspot, aligned with the Hadley cell.", "Geo-Variable Analysis"),
    (32, "32_physicians_latitude.html", "Physicians per 1000 by Latitude", "Scatter of physician density vs. latitude.", "Cuba (latitude 22) is an outlier rivaling Northern Europe.", "Geo-Variable Analysis"),
    (33, "33_education_megacity_distance.html", "Education vs Megacity Distance", "Scatter of schooling years vs. distance from megacities.", "Schooling drops by 0.8 years per 1000 km from megacity.", "Geo-Variable Analysis"),
    (34, "34_trade_longitude.html", "Trade Openness by Longitude", "Scatter of trade openness vs. longitude.", "The 'Eurasian trade belt' (30-120 degrees East) shows highest openness.", "Geo-Variable Analysis"),
    (35, "35_maternal_mortality_forest.html", "Maternal Mortality vs Forest Cover", "Scatter testing the link between forest cover and maternal health.", "Dense forest correlates with higher maternal mortality, proxying for remoteness.", "Geo-Variable Analysis"),
    (36, "36_remittances_latitude.html", "Remittances by Latitude", "Scatter of remittance-to-GDP ratio vs. latitude.", "Highest dependency at 10-30 degrees latitude: tropics-to-temperate migration.", "Geo-Variable Analysis"),
    (37, "37_india_lisa_clusters.html", "LISA Clusters (Voter Turnout)", "Spatial autocorrelation map of turnout across 543 constituencies.", "Turnout Moran's I = 0.642: HH clusters in South, LL clusters in UP/Bihar.", "India Elections 2024"),
    (38, "38_india_area_outcomes.html", "Constituency Area vs Outcomes", "Scatter of constituency size vs. victory margin or turnout.", "Larger constituencies have lower turnout (r = -0.3).", "India Elections 2024"),
    (39, "39_india_moran_scatterplot.html", "Moran Scatterplot", "Classic Moran scatterplot with spatial lag, quadrant classification.", "I = 0.643 confirms strong spatial autocorrelation, p < 0.001.", "India Elections 2024"),
    (40, "40_india_turnout_swing.html", "Turnout vs Swing Analysis", "Scatter of turnout vs. victory margin swing.", "High-turnout constituencies tend to have narrower margins.", "India Elections 2024"),
    (41, "41_india_distance_delhi_margin.html", "Distance from Delhi vs Margin", "Scatter testing the 'Delhi distance' hypothesis.", "Weak positive correlation: farther from Delhi = higher margins.", "India Elections 2024"),
    (46, "46_women_area_hypothesis.html", "Women Candidates vs Area", "Scatter testing whether larger constituencies field fewer women.", "Relationship is weak: party gatekeeping matters more than area.", "India Elections 2024"),
    (48, "48_alliance_lisa_women.html", "Alliance LISA & Women", "Multi-panel combining alliance LISA clustering with women's patterns.", "NDA and INDIA dominance zones have distinct spatial signatures.", "India Elections 2024"),
    (65, "65_silence_map.html", "The Silence Map", "Choropleth of 152/543 constituencies with zero women candidates.", "28% had zero women candidates, clustered in UP, Bihar, Maharashtra.", "India Elections 2024"),
    (66, "66_the_gauntlet.html", "The Gauntlet (Women Funnel)", "Funnel: 458 candidates, 133 retained deposit, 74 won.", "71% of women lost their deposit (325/458), vs ~55% for men.", "India Elections 2024"),
    (67, "67_gender_gap_electorate.html", "Gender Gap in Electorate", "Bar/scatter of male-female voter gap across states.", "Kerala: 1,084 F per 1,000 M; Bihar: 907.", "India Elections 2024"),
    (68, "68_deposit_forfeiture.html", "Deposit Forfeiture Analysis", "Scatter analyzing predictors of women losing their deposit.", "Women in reserved (SC/ST) constituencies are less likely to forfeit.", "India Elections 2024"),
    (69, "69_state_scoreboard.html", "State Gender Scoreboard", "Heatmap ranking states on women's representation dimensions.", "No state scores high on all dimensions simultaneously.", "India Elections 2024"),
    (71, "71_delimitation_simulator.html", "Delimitation Seat Simulator", "Interactive simulator for population-based seat redistribution.", "Population-based delimitation would transfer ~80 seats from South to North.", "Delimitation & Fiscal"),
    (72, "72_fiscal_returns.html", "Fiscal Returns by State", "Scatter of state fiscal contribution vs. receipts.", "Southern states contribute more than they receive; northern states get 2-3x.", "Delimitation & Fiscal"),
    (73, "73_reservation_simulator.html", "Reservation Impact Simulator", "Interactive tool simulating women's reservation policies.", "33% reservation would guarantee 181 women MPs vs. current 74.", "Delimitation & Fiscal"),
    (74, "74_moran_criteria_explorer.html", "Multi-Criteria Moran Explorer", "Interactive Moran's I exploration across different variables.", "Turnout (I=0.642) is far more autocorrelated than women's candidature (I=0.062).", "Delimitation & Fiscal"),
    (75, "75_punishment_value_3d.html", "Demographic Punishment Value (3D)", "3D surface: population growth x fertility x seat reallocation.", "States that reduced TFR the most face the largest seat losses.", "Delimitation & Fiscal"),
    (76, "76_representation_inequality.html", "Representation Inequality (Lorenz)", "Lorenz curve for seat distribution relative to population.", "Current frozen delimitation creates a representation Gini of ~0.15.", "Delimitation & Fiscal"),
    (77, "77_fiscal_spine.html", "Fiscal Spine Chart", "Diverging bar comparing state contributions vs. receipts.", "Net contributors cluster in the south, net recipients in the north.", "Delimitation & Fiscal"),
    (78, "78_representation_treemap.html", "Representation Treemap", "Treemap of seat allocation by state, colored by seats-per-million.", "Per-capita representation varies 8-fold across India.", "Delimitation & Fiscal"),
    (79, "79_fiscal_gender_bubble.html", "Fiscal-Gender Nexus Bubble", "Bubble chart: fiscal dependency vs. women's candidature by state.", "Highest fiscal transfer states have lowest women's candidature rates.", "Delimitation & Fiscal"),
    (80, "80_constituency_clustering.html", "Constituency Clustering (k-Means)", "k-Means clustering of 543 constituencies on 5 variables.", "Five natural clusters emerge from the data.", "Delimitation & Fiscal"),
    (42, "42_india_political_cylinder.html", "India Political Cylinder (3D)", "Cylindrical projection: height = latitude, angle = longitude, color = alliance.", "Vertical striations reveal party dominance bands.", "3D Immersive Visualizations"),
    (43, "43_development_globe.html", "Development Globe (3D)", "Interactive globe with countries extruded by GDP, colored by life expectancy.", "Spinning reveals the 'Northern ridge' vs. 'Southern plain'.", "3D Immersive Visualizations"),
    (44, "44_democracy_helix.html", "Democracy-Development Helix (3D)", "3D helix tracing democracy-development co-evolution.", "Democracy and development spiral upward together with 5-10 year lag.", "3D Immersive Visualizations"),
    (45, "45_continental_dev_space.html", "Continental Development Space (3D)", "3D scatter in GDP-health-education space by continent.", "Continents form distinct clouds; Asia spans the entire range.", "3D Immersive Visualizations"),
    (47, "47_3d_extruded_india.html", "3D Extruded India Map", "Constituencies extruded by victory margin, colored by alliance.", "The NDA 'mountain range' vs. INDIA alliance 'plateau'.", "3D Immersive Visualizations"),
    (55, "55_india_party_flip_3d.html", "India Party Flip (3D)", "3D visualization of constituencies that flipped between alliances.", "Flip constituencies cluster at alliance boundary zones.", "3D Immersive Visualizations"),
    (56, "56_development_spiral.html", "Development Spiral (3D)", "3D spiral: GDP-health-time space.", "The spiral accelerates after 2000 but kinks in 2020 (COVID).", "3D Immersive Visualizations"),
    (59, "59_india_dev_terrain.html", "India Development Terrain (3D)", "3D terrain mapping states by development indicators.", "Kerala and Goa are 'peaks'; Bihar and Jharkhand are 'valleys'.", "3D Immersive Visualizations"),
    (60, "60_india_food_geography_3d.html", "India Food Geography (3D)", "3D food production landscape.", "The Indo-Gangetic plain is India's food backbone.", "3D Immersive Visualizations"),
    (61, "61_literacy_gender_helix.html", "Literacy-Gender Helix (3D)", "3D helix: male vs female literacy across states.", "Gender literacy gap: 6 pts in Kerala vs 23 pts in Rajasthan.", "3D Immersive Visualizations"),
    (62, "62_constituency_aurora.html", "Constituency Aurora (3D)", "Artistic 3D aurora of constituency-level electoral energy.", "Aurora intensity reveals hidden engagement patterns.", "3D Immersive Visualizations"),
    (63, "63_india_socioeconomic_3d.html", "India Socioeconomic Landscape (3D)", "3D surface mapping multiple socioeconomic indicators.", "GDP, education, and health do not perfectly covary.", "3D Immersive Visualizations"),
    (64, "64_gender_development_3d.html", "Gender-Development 3D Surface", "3D surface: gender indicators x development metrics.", "A 'gender plateau' where women's indicators stall below a threshold.", "3D Immersive Visualizations"),
    (70, "70_women_candidature_3d.html", "Women Candidature 3D Landscape", "3D visualization of women's candidature mapped onto India.", "Hotspots (Kerala, West Bengal) surrounded by deserts (UP, Bihar).", "3D Immersive Visualizations"),
    # === SYNCHRONIZED MULTI-VIEW (4 charts) ===
    (81, "81_quad_panel_sync.html", "Four Lenses: Global Development", "Bubble (GDP vs Life Exp) + Choropleth (fertility) + Stacked area (continental pop) + Trajectory (fertility vs child mortality). Year slider 1990-2023.", "COVID-19 was a mortality shock visible in the bubble chart but invisible in the fertility map.", "Synchronized Multi-View"),
    (82, "82_health_environment_sync.html", "Health-Environment Nexus", "Aridity vs child mortality + Environmental health choropleth + Continental grouped bars + Preston Curve by birth rate. Year slider 1990-2023.", "Africa's child mortality is declining faster than any continent at the same income level, via mobile health diffusion.", "Synchronized Multi-View"),
    (83, "83_tech_inequality_sync.html", "Technology-Inequality Divergence", "Internet choropleth + Gini-GDP scatter (size=internet) + Continental digital divide + Income-continent life expectancy heatmap. Year slider 1990-2023.", "Internet adoption follows Hagerstrand logistic diffusion; Africa's mobile-first leapfrog creates structurally different digital landscapes.", "Synchronized Multi-View"),
    (84, "84_india_threshold_sync.html", "India Electoral Threshold Explorer", "Turnout threshold slider (40-85%) filters: constituency map + margin histogram + women vs area scatter + alliance seat bars. 543 constituencies.", "Raising turnout threshold removes Hindi belt constituencies, shifting balance toward INDIA alliance: engagement and representation pull opposite.", "Synchronized Multi-View"),
]

# Group
from collections import OrderedDict
groups = OrderedDict()
for num, fname, title, desc, bl, group in CHARTS:
    if group not in groups:
        groups[group] = []
    groups[group].append((num, fname, title, desc, bl))

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
    "3D Immersive Visualizations": "#B088F9",
    "Synchronized Multi-View": "#00D5E0",
}

cards_html = ""
for group_name, charts in groups.items():
    color = GROUP_COLORS.get(group_name, "#00D5E0")
    cards_html += f"""
    <div class="group-section">
        <h2 class="group-title" style="border-color:{color}"><span class="group-dot" style="background:{color}"></span>{group_name} <span class="group-count">({len(charts)} charts)</span></h2>
        <div class="cards-grid">
    """
    for num, fname, title, desc, bl in charts:
        cards_html += f"""
        <a href="{fname}" class="card" style="--accent:{color}">
            <div class="card-num">#{num:02d}</div>
            <div class="card-title">{title}</div>
            <div class="card-desc">{desc}</div>
            <div class="card-bottom"><span class="bottom-label">Takeaway:</span> {bl}</div>
        </a>"""
    cards_html += "\n        </div>\n    </div>"

index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Complete Chart Index | Spatial Data Visualization Atlas</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@300;400;600;700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#080B13;color:#c0c8d4;font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif}}
.page-header{{text-align:center;padding:40px 20px 20px}}
.page-header h1{{font-family:'Playfair Display',Georgia,serif;color:#F0F4F8;font-size:2.2rem;margin-bottom:8px}}
.page-header p{{color:#7B8CA3;font-size:.95rem;max-width:800px;margin:0 auto}}
.stats-bar{{display:flex;justify-content:center;gap:30px;padding:14px 20px;margin-bottom:10px}}
.stat{{text-align:center}}
.stat-num{{font-family:'Playfair Display',Georgia,serif;color:#FFD700;font-size:1.8rem;font-weight:700}}
.stat-label{{color:#5a6a7a;font-size:.78rem;text-transform:uppercase;letter-spacing:.05em}}
.back-link{{text-align:center;margin-bottom:24px}}
.back-link a{{color:#00D5E0;text-decoration:none;font-size:.9rem;border:1px solid #1a2233;padding:6px 18px;border-radius:4px;transition:all .2s}}
.back-link a:hover{{background:#00D5E0;color:#080B13}}
.content{{max-width:1200px;margin:0 auto;padding:0 20px 60px}}
.group-section{{margin-bottom:36px}}
.group-title{{font-family:'Playfair Display',Georgia,serif;color:#F0F4F8;font-size:1.25rem;padding:10px 0 8px;margin-bottom:14px;border-bottom:2px solid;display:flex;align-items:center;gap:10px}}
.group-dot{{width:10px;height:10px;border-radius:50%;display:inline-block}}
.group-count{{color:#5a6a7a;font-size:.8rem;font-weight:400}}
.cards-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:12px}}
.card{{display:block;background:#0D1117;border:1px solid #1a2233;border-radius:8px;padding:16px 18px;text-decoration:none;transition:all .25s;border-left:3px solid var(--accent)}}
.card:hover{{background:#111822;border-color:var(--accent);transform:translateY(-2px);box-shadow:0 4px 20px rgba(0,0,0,.4)}}
.card-num{{color:var(--accent);font-size:.72rem;font-weight:700;font-family:'Playfair Display',Georgia,serif;margin-bottom:2px;opacity:.7}}
.card-title{{color:#F0F4F8;font-size:.95rem;font-weight:700;margin-bottom:6px;font-family:'Playfair Display',Georgia,serif}}
.card-desc{{color:#7B8CA3;font-size:.78rem;line-height:1.6;margin-bottom:8px}}
.card-bottom{{background:#0a0e16;border-radius:4px;padding:8px 10px;font-size:.76rem;line-height:1.5;color:#9aa8b8}}
.bottom-label{{color:var(--accent);font-weight:700;text-transform:uppercase;font-size:.68rem;letter-spacing:.03em}}
.search-bar{{text-align:center;margin-bottom:24px}}
.search-bar input{{background:#0D1117;border:1px solid #1a2233;color:#F0F4F8;padding:10px 20px;border-radius:6px;width:400px;max-width:80vw;font-size:.9rem;font-family:inherit}}
.search-bar input:focus{{outline:none;border-color:#00D5E0}}
@media(max-width:700px){{.cards-grid{{grid-template-columns:1fr}}.stats-bar{{flex-wrap:wrap;gap:16px}}}}
</style>
</head>
<body>
<div class="page-header">
<h1>Complete Chart Index</h1>
<p>Spatial &amp; Geographical Data Visualization Atlas, Lab for Spatial Informatics, IIIT Hyderabad. All {len(CHARTS)} visualizations grouped by topic.</p>
</div>
<div class="stats-bar">
<div class="stat"><div class="stat-num">{len(CHARTS)}</div><div class="stat-label">Charts</div></div>
<div class="stat"><div class="stat-num">{len(groups)}</div><div class="stat-label">Topic Groups</div></div>
<div class="stat"><div class="stat-num">199</div><div class="stat-label">Countries</div></div>
<div class="stat"><div class="stat-num">543</div><div class="stat-label">India Constituencies</div></div>
<div class="stat"><div class="stat-num">1990-2023</div><div class="stat-label">Time Span</div></div>
</div>
<div class="back-link"><a href="index.html">&larr; Back to Dashboard</a></div>
<div class="search-bar">
<input type="text" id="searchInput" placeholder="Search charts by title, topic, or keyword..." oninput="filterCards(this.value)">
</div>
<div class="content" id="content">
{cards_html}
</div>
<script>
function filterCards(q) {{
    q = q.toLowerCase().trim();
    document.querySelectorAll('.card').forEach(card => {{
        card.style.display = card.textContent.toLowerCase().includes(q) ? '' : 'none';
    }});
    document.querySelectorAll('.group-section').forEach(section => {{
        let anyVisible = false;
        section.querySelectorAll('.card').forEach(c => {{
            if (c.style.display !== 'none') anyVisible = true;
        }});
        section.style.display = anyVisible ? '' : 'none';
    }});
}}
</script>
</body>
</html>"""

# Write chart index
for target_dir in [VIS, OUT]:
    with open(os.path.join(target_dir, "chart_index.html"), "w") as f:
        f.write(index_html)
print(f"Chart index rebuilt: {len(index_html)/1024:.1f} KB, {len(CHARTS)} charts in {len(groups)} groups")

# ========== FIX 2: DASHBOARD TEXT FIXES ==========
for target_dir in [VIS, OUT]:
    fpath = os.path.join(target_dir, "index.html")
    with open(fpath, "r") as f:
        dash = f.read()
    
    dash = dash.replace("81 interactive visualizations", "84 interactive visualizations")
    dash = dash.replace("all 81 charts grouped", "all 84 charts grouped")
    
    with open(fpath, "w") as f:
        f.write(dash)

print("Dashboard text fixed: '84 interactive visualizations', 'all 84 charts'")

# ========== VERIFY ==========
import re

# Check chart index
with open(os.path.join(OUT, "chart_index.html"), "r") as f:
    idx = f.read()
idx_links = set(re.findall(r'href="(\d\d_[^"]+\.html)"', idx))
print(f"\nChart index links: {len(idx_links)}")
# Check Synchronized section has 4
sync_match = re.search(r'Synchronized Multi-View.*?\((\d+) charts\)', idx)
if sync_match:
    print(f"Synchronized group count: {sync_match.group(1)}")
quad_links = [l for l in idx_links if l.startswith(('81_','82_','83_','84_'))]
print(f"Quad-panel links in index: {quad_links}")

# Check dashboard
with open(os.path.join(OUT, "index.html"), "r") as f:
    dash = f.read()
dash_links = set(re.findall(r"op\('(\d\d_[^']+\.html)'\)", dash))
print(f"\nDashboard links: {len(dash_links)}")
quad_dash = [l for l in dash_links if l.startswith(('81_','82_','83_','84_'))]
print(f"Quad-panel links in dashboard: {quad_dash}")

# Check text
has_84_vis = "84 interactive" in dash
has_84_idx = "all 84 charts" in dash
print(f"Dashboard says '84 interactive': {has_84_vis}")
print(f"Dashboard says 'all 84 charts': {has_84_idx}")
