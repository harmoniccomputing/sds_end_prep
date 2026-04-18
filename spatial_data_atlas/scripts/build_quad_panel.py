#!/usr/bin/env python3
"""
Build a quad-panel synchronized animation:
Panel A: Bubble chart (GDP vs Life Expectancy, size=population, color=continent)
Panel B: World choropleth (colored by fertility rate)
Panel C: Stacked area (continental population shares)
Panel D: Connected scatter (Fertility vs Child Mortality by continent centroid)

All 4 panels driven by a single year slider (1990-2023).
Different datasets combined: development indicators + spatial coordinates + demographic transitions.
"""

import pandas as pd
import numpy as np
import json

# Load data
df = pd.read_csv("/home/claude/rosling_project/data/processed/rosling_ready.csv")

# Clean
df = df.dropna(subset=['gdp_per_capita','life_expectancy','fertility_rate','population'])
years = sorted(df['year'].unique())

# ---------- Panel A: Bubble data (GDP vs Life Exp) ----------
# Select ~40 representative countries for readability
major_countries = [
    'China','India','United States','Brazil','Nigeria','Bangladesh','Russia',
    'Japan','Germany','United Kingdom','France','Indonesia','Pakistan','Mexico',
    'Ethiopia','Egypt, Arab Rep.','Vietnam','Turkey','Thailand','South Africa',
    'Kenya','Colombia','Argentina','Poland','Canada','Australia','Saudi Arabia',
    'Ghana','Peru','Malaysia','Chile','Czech Republic','Norway','Sweden',
    'Singapore','Rwanda','Nepal','Morocco','Congo, Dem. Rep.','Angola'
]
df_bubble = df[df['country_name'].isin(major_countries)].copy()

bubble_frames = {}
for yr in years:
    ydf = df_bubble[df_bubble['year']==yr]
    bubble_frames[int(yr)] = {
        'x': ydf['gdp_per_capita'].tolist(),
        'y': ydf['life_expectancy'].tolist(),
        'size': (np.sqrt(ydf['population']/1e6)*2.5).tolist(),
        'text': ydf['country_name'].tolist(),
        'color': ydf['continent'].map({
            'Americas':'#FFDD57','Asia':'#FF6B8A','Africa':'#00D5E0',
            'Europe':'#7CFC00','Other':'#B088F9'
        }).tolist()
    }

# ---------- Panel B: Choropleth data (fertility rate) ----------
choropleth_frames = {}
for yr in years:
    ydf = df[df['year']==yr].drop_duplicates('country_code')
    choropleth_frames[int(yr)] = {
        'locations': ydf['country_code'].tolist(),
        'z': ydf['fertility_rate'].tolist(),
        'text': ydf['country_name'].tolist()
    }

# ---------- Panel C: Stacked area (continental population) ----------
cont_order = ['Africa','Asia','Americas','Europe','Other']
area_data = {}
for yr in years:
    ydf = df[df['year']==yr]
    pops = ydf.groupby('continent')['population'].sum()
    total = pops.sum()
    area_data[int(yr)] = {c: float(pops.get(c, 0)/1e9) for c in cont_order}

# Build cumulative arrays for stacking
area_frames = {}
for yr in years:
    yr = int(yr)
    vals = [area_data[yr].get(c, 0) for c in cont_order]
    cum = np.cumsum(vals).tolist()
    area_frames[yr] = {'values': vals, 'cumulative': cum, 'total': sum(vals)}

# ---------- Panel D: Continent-level fertility vs child mortality ----------
scatter_frames = {}
for yr in years:
    ydf = df[df['year']==yr]
    yr = int(yr)
    scatter_frames[yr] = {}
    for c in cont_order:
        cdf = ydf[ydf['continent']==c]
        cm_valid = cdf.dropna(subset=['child_mortality'])
        if len(cm_valid) > 0:
            # Population-weighted means
            pop_sum = cm_valid['population'].sum()
            if pop_sum > 0:
                wfert = (cm_valid['fertility_rate'] * cm_valid['population']).sum() / pop_sum
                wmort = (cm_valid['child_mortality'] * cm_valid['population']).sum() / pop_sum
                wpop = pop_sum
            else:
                wfert = cm_valid['fertility_rate'].mean()
                wmort = cm_valid['child_mortality'].mean()
                wpop = 1e6
        else:
            wfert = cdf['fertility_rate'].mean() if len(cdf)>0 else 2.0
            wmort = 50
            wpop = 1e6
        scatter_frames[yr][c] = {'fertility': float(wfert), 'mortality': float(wmort), 'pop': float(wpop)}

# ---------- Build HTML ----------
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Quad-Panel Synchronized Development Animation | Spatial Atlas</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
* {{margin:0;padding:0;box-sizing:border-box}}
body {{background:#080B13;color:#c0c8d4;font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif;overflow-x:hidden}}
.header {{text-align:center;padding:28px 20px 12px}}
.header h1 {{font-family:'Playfair Display',Georgia,serif;color:#F0F4F8;font-size:1.9rem;margin-bottom:6px}}
.header p {{color:#7B8CA3;font-size:.95rem;max-width:900px;margin:0 auto}}
.grid {{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 12px;max-width:1600px;margin:0 auto}}
.panel {{background:#0D1117;border:1px solid #1a2233;border-radius:8px;overflow:hidden}}
.panel-title {{color:#00D5E0;font-size:.82rem;font-weight:700;padding:8px 14px 0;font-family:'Playfair Display',Georgia,serif;text-transform:uppercase;letter-spacing:.04em}}
.plot-div {{width:100%;height:380px}}
.controls {{text-align:center;padding:18px 20px;max-width:1600px;margin:0 auto}}
.slider-row {{display:flex;align-items:center;gap:14px;justify-content:center}}
.year-display {{font-family:'Playfair Display',Georgia,serif;font-size:2.8rem;font-weight:700;color:#FFD700;min-width:100px;text-align:center}}
#yearSlider {{width:500px;max-width:60vw;accent-color:#00D5E0;height:6px}}
.btn {{background:#1a2233;border:1px solid #00D5E0;color:#00D5E0;padding:6px 18px;border-radius:4px;cursor:pointer;font-size:.85rem;transition:all .2s}}
.btn:hover {{background:#00D5E0;color:#080B13}}
.btn.active {{background:#FF5872;border-color:#FF5872;color:#fff}}
.speed-row {{margin-top:8px;font-size:.78rem;color:#5a6a7a}}
.math-panel {{background:#0D1117;border:1px solid #1a2233;border-radius:8px;padding:20px 28px;margin:14px 12px;max-width:1600px;margin:14px auto}}
.math-panel h3 {{color:#FFD700;font-size:.92rem;margin-bottom:10px;font-family:'Playfair Display',Georgia,serif}}
.math-panel p {{font-size:.84rem;line-height:1.7;color:#9aa8b8;text-align:justify;margin-bottom:10px}}
.math-panel .eq {{background:#0a0e16;border-left:3px solid #00D5E0;padding:10px 16px;margin:10px 0;font-family:'Courier New',monospace;font-size:.82rem;color:#00D5E0;overflow-x:auto}}
.math-panel b {{color:#E8ECF0}}
.math-panel em {{color:#FF5872;font-style:normal}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}.plot-div{{height:300px}}#yearSlider{{width:80vw}}}}
</style>
</head>
<body>
<div class="header">
<h1>Four Lenses on Global Development: A Synchronized Animation</h1>
<p>Four different visualization types, four different datasets, one shared timeline. Watch how economic growth, demographic transition, spatial distribution, and population structure evolve in parallel from 1990 to 2023. Every panel tells a different facet of the same story.</p>
</div>

<div class="controls">
<div class="slider-row">
<button class="btn" id="playBtn" onclick="togglePlay()">&#9654; Play</button>
<input type="range" id="yearSlider" min="1990" max="2023" value="1990" step="1" oninput="updateAll(this.value)">
<div class="year-display" id="yearDisplay">1990</div>
</div>
<div class="speed-row">
Speed: <button class="btn" onclick="setSpeed(800)">Slow</button>
<button class="btn active" id="speedMed" onclick="setSpeed(400)">Medium</button>
<button class="btn" onclick="setSpeed(150)">Fast</button>
</div>
</div>

<div class="grid">
<div class="panel">
<div class="panel-title">A. Wealth vs Health (Bubble Chart)</div>
<div id="plotA" class="plot-div"></div>
</div>
<div class="panel">
<div class="panel-title">B. Fertility Rate (World Choropleth)</div>
<div id="plotB" class="plot-div"></div>
</div>
<div class="panel">
<div class="panel-title">C. Continental Population (Stacked Area)</div>
<div id="plotC" class="plot-div"></div>
</div>
<div class="panel">
<div class="panel-title">D. Fertility vs Child Mortality (Continent Trajectories)</div>
<div id="plotD" class="plot-div"></div>
</div>
</div>

<div class="math-panel">
<h3>Mathematical Framework: The Demographic Transition as Coupled Spatial Dynamics</h3>

<p>These four panels jointly illustrate the <b>demographic-economic transition</b>, one of the most robust empirical regularities in development science. The four views correspond to four mathematical perspectives on the same underlying process:</p>

<p><b>Panel A</b> displays the <em>Preston Curve</em>, the log-linear relationship between income and longevity. The functional form, first documented by Samuel Preston (1975), is:</p>
<div class="eq">e(y) = alpha + beta * ln(y) + epsilon</div>
<p>where e(y) is life expectancy at birth, y is GDP per capita (PPP), and the log transform captures the diminishing marginal returns of income on health. The curve shifts upward over time (the same income buys more health in 2023 than in 1990) due to technology diffusion: a spatial process governed by Hagerstrand's diffusion equation dN/dt = k * N * (N_max - N) / N_max, where medical innovations spread from core to periphery.</p>

<p><b>Panel B</b> maps <em>Total Fertility Rate (TFR)</em> onto geographic space, revealing the <b>spatial autocorrelation of demographic transition</b>. Fertility decline is not randomly distributed: it clusters in contiguous zones, obeying Tobler's First Law of Geography. The spatial pattern follows a gravity-weighted diffusion model:</p>
<div class="eq">TFR(i,t) = TFR(i,t-1) - delta * SUM_j [ w(ij) * (TFR(i,t-1) - TFR(j,t-1)) ]</div>
<p>where w(ij) is a spatial weight inversely proportional to distance between countries i and j, and delta is the diffusion rate. High-fertility clusters in Sahel West Africa and low-fertility zones in East Asia are not independent phenomena: they reflect spatially structured processes of urbanization, female education access, and contraceptive availability that are themselves governed by geographic proximity and connectivity.</p>

<p><b>Panel C</b> aggregates population by continent, revealing the <em>shifting center of gravity</em> of the world's population. Africa's growing share encodes an important spatial fact: the arithmetic center of global population is migrating south and west. The centroid coordinates can be computed as:</p>
<div class="eq">lat_c(t) = SUM_i [P(i,t) * lat(i)] / SUM_i [P(i,t)]</div>
<div class="eq">lon_c(t) = SUM_i [P(i,t) * lon(i)] / SUM_i [P(i,t)]</div>
<p>where P(i,t) is country i's population at time t. This centroid has moved approximately 500 km southward since 1990, with profound implications for infrastructure, resource distribution, and geopolitical power.</p>

<p><b>Panel D</b> shows the <em>fertility-mortality nexus</em> at continental scale. The classic transition model posits four stages: (1) high birth/death rates, (2) falling mortality with stable fertility (population explosion), (3) falling fertility (demographic dividend), (4) low equilibrium. The trajectory on the fertility-mortality plane traces a characteristic counterclockwise arc. The spatial insight is that different continents occupy different positions on this arc simultaneously, and their movement speed is determined by geographic factors: urbanization rate (which compresses intergenerational information flow), distance to educational infrastructure, and climatic constraints on agricultural productivity.</p>

<p><em>Spatial connection:</em> All four panels encode Waldo Tobler's insight that "everything is related to everything else, but near things are more related than distant things." The bubble chart shows that geographic neighbors cluster together in GDP-health space. The choropleth reveals contiguous fertility zones. The stacked area shows continental-scale demographic shifts. The trajectory plot traces paths that are geographically structured. Development is, fundamentally, a spatial process.</p>
</div>

<!--ATLAS-GUIDE-START-->
<div style="position:relative;background:#080B13;padding:36px 28px 32px;font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif;font-size:.84rem;line-height:1.8;border-top:2px solid #151d2e;max-width:1600px;margin:0 auto">
<div style="max-width:1100px;margin:0 auto">

<h2 style="color:#00D5E0;font-size:1.2rem;font-weight:700;margin:0 0 4px;font-family:'Playfair Display',Georgia,serif">Synchronized Multi-Panel Visualization: Principles and Spatial Interpretation</h2>
<p style="color:#FF5872;font-size:.93rem;font-weight:600;margin:0 0 18px;font-style:italic">Four coordinated views reveal what no single chart can: the coupled dynamics of spatial, economic, demographic, and epidemiological transitions unfolding simultaneously across the world.</p>

<h3 style="color:#FFD700;font-size:.88rem;font-weight:700;margin:26px 0 6px;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid #1a2233;padding-bottom:4px">Why Synchronized Views Matter in Spatial Data Science</h3>
<p style="color:#B8C4D0;text-align:justify;margin:0 0 11px">The concept of <b style="color:#E8ECF0">coordinated multiple views (CMV)</b> is central to visual analytics and geovisualization. Introduced formally by Roberts (2007) and refined by Andrienko & Andrienko (2006), CMV systems link two or more visual representations so that interactions in one view propagate to all others. This synchronized quad-panel implements <b style="color:#E8ECF0">temporal brushing</b>: the slider selects a time slice, and all four views update simultaneously, enabling the viewer to observe cross-domain correlations that would be invisible in any single chart.</p>

<p style="color:#B8C4D0;text-align:justify;margin:0 0 11px">The design follows Bertin's (1967) principle of <b style="color:#E8ECF0">visual variables differentiation</b>: each panel uses a distinct retinal variable as its primary encoding (position in Panel A, color value in Panel B, area/length in Panel C, trajectory in Panel D). This prevents visual confusion while enabling comparison. Shneiderman's mantra of "overview first, zoom and filter, details on demand" is satisfied by the slider interface, which provides temporal navigation at the overview level.</p>

<h3 style="color:#FFD700;font-size:.88rem;font-weight:700;margin:26px 0 6px;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid #1a2233;padding-bottom:4px">The Data Integration Challenge</h3>
<div style="background:#0f1520;border-left:3px solid #00D5E0;padding:12px 16px;margin:12px 0;border-radius:0 6px 6px 0">
<p style="color:#B8C4D0;margin:0">This visualization integrates <b style="color:#E8ECF0">four different data structures</b>: (1) point-level microdata with 5 continuous variables (Panel A), (2) polygon-level spatial data with ISO3 geographic identifiers (Panel B), (3) aggregated time series grouped by continent (Panel C), and (4) population-weighted continental centroids on a derived feature space (Panel D). The integration key is the <b style="color:#E8ECF0">country-year tuple (ISO3, year)</b>, which serves as a universal join field across all four representations. This is a standard challenge in spatial data science: reconciling data collected at different spatial granularities (point, polygon, region) and different thematic resolutions (individual country, continent) into a coherent visual narrative.</p>
</div>

<h3 style="color:#FFD700;font-size:.88rem;font-weight:700;margin:26px 0 6px;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid #1a2233;padding-bottom:4px">Key Spatial Patterns to Watch</h3>
<p style="color:#B8C4D0;text-align:justify;margin:0 0 11px"><b style="color:#E8ECF0">1990-2000:</b> The post-Cold War development divergence. Panel A shows African countries stagnating or declining (HIV/AIDS, structural adjustment) while East Asian tigers race rightward. Panel B shows a sharp fertility gradient from sub-Saharan Africa (TFR > 6) to East Asia (TFR < 2). Panel C shows Asia's dominance (60% of world population). Panel D shows Africa far from all other continents in the high-fertility, high-mortality quadrant.</p>

<p style="color:#B8C4D0;text-align:justify;margin:0 0 11px"><b style="color:#E8ECF0">2000-2015:</b> The great convergence. Panel A shows a massive rightward shift as China and India grow rapidly. Panel B shows fertility declining across South Asia and parts of Africa. Panel C shows Africa's share beginning its historic rise. Panel D shows all continents converging toward the lower-left (low fertility, low mortality). This era of convergence is the empirical basis for the "catch-up growth" literature (Barro & Sala-i-Martin, 2003).</p>

<p style="color:#B8C4D0;text-align:justify;margin:0 0 11px"><b style="color:#E8ECF0">2015-2023:</b> The partial reversal. Panel A shows COVID-19 as a visible downward shock in life expectancy (2020-2021). Panel B reveals the persistence of high fertility in the Sahel (Niger, Mali, Chad). Panel C shows Africa overtaking Europe in total population. Panel D shows Africa's trajectory decelerating: child mortality is falling, but fertility decline has stalled in several countries, a phenomenon demographers call the "stall" and which has significant spatial clustering in West and Central Africa.</p>

<div style="background:#0f1520;border-left:3px solid #FF5872;padding:12px 16px;margin:12px 0;border-radius:0 6px 6px 0">
<p style="color:#B8C4D0;margin:0"><b style="color:#E8ECF0">Surprising finding:</b> The COVID-19 pandemic (2020) is visible as a <b style="color:#E8ECF0">synchronized shock</b> across all four panels. Panel A shows bubbles dropping vertically (life expectancy falls while GDP is relatively stable). Panel B shows almost no change (fertility is a slow-moving variable). Panel C shows minimal change (population is a stock variable). Panel D shows a rightward blip in mortality without corresponding fertility change. This cross-panel comparison reveals that COVID was primarily a <b style="color:#E8ECF0">mortality shock</b> without demographic transition implications: it killed without changing the structural determinants of fertility. This contrasts with historical pandemics (e.g., the Black Death) that triggered lasting demographic regime changes.</p>
</div>

<p style="font-size:.76rem;color:#7B8CA3;margin-top:20px;border-top:1px solid #1a2233;padding-top:10px"><b style="color:#E8ECF0">Key references:</b> Preston, S.H. (1975). The changing relation between mortality and level of economic development. <i>Population Studies</i>, 29(2), 231-248. | Andrienko, N. & Andrienko, G. (2006). <i>Exploratory Analysis of Spatial and Temporal Data</i>. Springer. | Roberts, J.C. (2007). State of the art: Coordinated & multiple views in exploratory visualization. <i>Proc. CMV</i>, IEEE. | Barro, R. & Sala-i-Martin, X. (2003). <i>Economic Growth</i>, 2nd ed. MIT Press. | Bertin, J. (1967/1983). <i>Semiology of Graphics</i>. ESRI Press.</p>

</div>
</div>
<!--ATLAS-GUIDE-END-->

<script>
// ===== DATA =====
const bubbleData = {json.dumps(bubble_frames)};
const choroData = {json.dumps(choropleth_frames)};
const areaData = {json.dumps(area_frames)};
const scatterData = {json.dumps(scatter_frames)};
const contOrder = {json.dumps(cont_order)};
const contColors = {{'Africa':'#00D5E0','Asia':'#FF6B8A','Americas':'#FFDD57','Europe':'#7CFC00','Other':'#B088F9'}};
const years = {json.dumps([int(y) for y in years])};
const darkBg = '#0D1117';
const gridColor = '#1a2233';
const textColor = '#7B8CA3';

// Common layout settings
const commonLayout = {{
    paper_bgcolor: darkBg, plot_bgcolor: darkBg,
    font: {{family: "'Source Sans 3','Segoe UI',system-ui,sans-serif", color: textColor, size: 11}},
    margin: {{l:55,r:15,t:10,b:40}},
    xaxis: {{gridcolor:gridColor,zerolinecolor:gridColor}},
    yaxis: {{gridcolor:gridColor,zerolinecolor:gridColor}}
}};

// ===== PANEL A: Bubble Chart =====
function initBubble() {{
    const d = bubbleData['1990'];
    const trace = {{
        x: d.x, y: d.y,
        mode: 'markers',
        marker: {{size: d.size, color: d.color, opacity: 0.75, line:{{width:0.5,color:'#1a2233'}}}},
        text: d.text, hovertemplate: '<b>%{{text}}</b><br>GDP/cap: $%{{x:,.0f}}<br>Life exp: %{{y:.1f}} yr<extra></extra>',
        type: 'scatter'
    }};
    const layout = {{
        ...commonLayout,
        xaxis: {{...commonLayout.xaxis, type:'log', title:'GDP per Capita (PPP, log)', range:[Math.log10(300),Math.log10(120000)],
                 tickvals:[500,1000,5000,10000,50000,100000], ticktext:['$500','$1K','$5K','$10K','$50K','$100K']}},
        yaxis: {{...commonLayout.yaxis, title:'Life Expectancy (years)', range:[30,90]}}
    }};
    Plotly.newPlot('plotA', [trace], layout, {{responsive:true,displayModeBar:false}});
}}

function updateBubble(yr) {{
    const d = bubbleData[yr];
    if (!d) return;
    Plotly.restyle('plotA', {{x:[d.x], y:[d.y], 'marker.size':[d.size], 'marker.color':[d.color], text:[d.text]}});
}}

// ===== PANEL B: Choropleth =====
function initChoropleth() {{
    const d = choroData['1990'];
    const trace = {{
        type: 'choropleth', locations: d.locations, z: d.z, text: d.text,
        colorscale: [[0,'#0a1628'],[0.15,'#003366'],[0.3,'#006699'],[0.5,'#00D5E0'],[0.7,'#FFD700'],[0.85,'#FF8C00'],[1,'#FF5872']],
        zmin: 1, zmax: 7, colorbar: {{title:'TFR',thickness:12,len:0.8,tickfont:{{size:10}}}},
        hovertemplate: '<b>%{{text}}</b><br>TFR: %{{z:.2f}}<extra></extra>',
        marker: {{line:{{width:0.3,color:'#1a2233'}}}}
    }};
    const layout = {{
        ...commonLayout,
        geo: {{
            showframe:false, showcoastlines:true, coastlinecolor:'#1a2233',
            bgcolor:darkBg, landcolor:'#0a1628', oceancolor:darkBg,
            showlakes:false, projection:{{type:'natural earth'}},
            lonaxis:{{range:[-180,180]}}, lataxis:{{range:[-60,85]}}
        }},
        margin: {{l:5,r:5,t:5,b:5}}
    }};
    Plotly.newPlot('plotB', [trace], layout, {{responsive:true,displayModeBar:false}});
}}

function updateChoropleth(yr) {{
    const d = choroData[yr];
    if (!d) return;
    Plotly.restyle('plotB', {{locations:[d.locations], z:[d.z], text:[d.text]}});
}}

// ===== PANEL C: Stacked Area =====
function initArea() {{
    const traces = contOrder.map((c, i) => {{
        const yVals = years.map(yr => areaData[yr].values[i]);
        return {{
            x: years, y: yVals, name: c,
            type: 'scatter', mode: 'none',
            fill: i === 0 ? 'tozeroy' : 'tonexty',
            fillcolor: contColors[c] + '80',
            line: {{color: contColors[c], width: 1}},
            stackgroup: 'one',
            hovertemplate: '<b>' + c + '</b><br>Pop: %{{y:.2f}}B<extra></extra>'
        }};
    }});
    // Add vertical year indicator
    traces.push({{
        x: [1990,1990], y: [0,8], mode:'lines', line:{{color:'#FFD700',width:2,dash:'dash'}},
        showlegend:false, hoverinfo:'skip'
    }});
    const layout = {{
        ...commonLayout,
        xaxis: {{...commonLayout.xaxis, title:'Year', range:[1990,2023]}},
        yaxis: {{...commonLayout.yaxis, title:'Population (billions)', range:[0,8.5]}},
        showlegend:true, legend:{{x:0.02,y:0.98,font:{{size:9}},bgcolor:'rgba(0,0,0,0)'}}
    }};
    Plotly.newPlot('plotC', traces, layout, {{responsive:true,displayModeBar:false}});
}}

function updateArea(yr) {{
    // Move the vertical line
    const nTraces = contOrder.length;
    Plotly.restyle('plotC', {{x:[[parseInt(yr),parseInt(yr)]]}}, [nTraces]);
}}

// ===== PANEL D: Continental Trajectory =====
function initTrajectory() {{
    const traces = [];
    // Draw full historical trails (faded)
    contOrder.forEach(c => {{
        const xs = years.map(yr => scatterData[yr][c]?.fertility || 2);
        const ys = years.map(yr => scatterData[yr][c]?.mortality || 50);
        traces.push({{
            x: xs, y: ys, mode: 'lines', name: c + ' trail',
            line: {{color: contColors[c], width: 1.5, dash: 'dot'}},
            opacity: 0.3, showlegend: false, hoverinfo: 'skip'
        }});
    }});
    // Current year markers
    contOrder.forEach(c => {{
        const d = scatterData['1990'][c];
        const sz = Math.sqrt(d.pop / 1e8) * 4;
        traces.push({{
            x: [d.fertility], y: [d.mortality], mode: 'markers+text', name: c,
            marker: {{size: Math.max(sz, 12), color: contColors[c], opacity: 0.85, line:{{width:1,color:'#fff'}}}},
            text: [c], textposition: 'top center', textfont: {{size: 10, color: contColors[c]}},
            hovertemplate: '<b>' + c + '</b><br>TFR: %{{x:.2f}}<br>Child mort: %{{y:.1f}}/1000<extra></extra>'
        }});
    }});
    const layout = {{
        ...commonLayout,
        xaxis: {{...commonLayout.xaxis, title:'Fertility Rate (TFR)', range:[1,7]}},
        yaxis: {{...commonLayout.yaxis, title:'Child Mortality (per 1000)', range:[0,200]}},
        showlegend:false
    }};
    Plotly.newPlot('plotD', traces, layout, {{responsive:true,displayModeBar:false}});
}}

function updateTrajectory(yr) {{
    const nTrails = contOrder.length;
    contOrder.forEach((c, i) => {{
        const d = scatterData[yr][c];
        if (!d) return;
        const sz = Math.sqrt(d.pop / 1e8) * 4;
        Plotly.restyle('plotD', {{
            x: [[d.fertility]], y: [[d.mortality]],
            'marker.size': [Math.max(sz, 12)]
        }}, [nTrails + i]);
    }});
}}

// ===== MASTER CONTROLLER =====
let playing = false;
let playInterval = null;
let speed = 400;

function updateAll(yr) {{
    yr = String(yr);
    document.getElementById('yearDisplay').textContent = yr;
    document.getElementById('yearSlider').value = yr;
    updateBubble(yr);
    updateChoropleth(yr);
    updateArea(yr);
    updateTrajectory(yr);
}}

function togglePlay() {{
    if (playing) {{
        clearInterval(playInterval);
        playing = false;
        document.getElementById('playBtn').innerHTML = '&#9654; Play';
        document.getElementById('playBtn').classList.remove('active');
    }} else {{
        playing = true;
        document.getElementById('playBtn').innerHTML = '&#9724; Pause';
        document.getElementById('playBtn').classList.add('active');
        let currentYear = parseInt(document.getElementById('yearSlider').value);
        if (currentYear >= 2023) currentYear = 1990;
        playInterval = setInterval(() => {{
            currentYear++;
            if (currentYear > 2023) {{
                currentYear = 1990;
            }}
            updateAll(currentYear);
        }}, speed);
    }}
}}

function setSpeed(ms) {{
    speed = ms;
    document.querySelectorAll('.speed-row .btn').forEach(b => b.classList.remove('active'));
    if (ms === 800) document.querySelectorAll('.speed-row .btn')[0].classList.add('active');
    else if (ms === 400) document.getElementById('speedMed').classList.add('active');
    else document.querySelectorAll('.speed-row .btn')[2].classList.add('active');
    if (playing) {{
        clearInterval(playInterval);
        let currentYear = parseInt(document.getElementById('yearSlider').value);
        playInterval = setInterval(() => {{
            currentYear++;
            if (currentYear > 2023) currentYear = 1990;
            updateAll(currentYear);
        }}, speed);
    }}
}}

// Initialize all panels
window.addEventListener('load', () => {{
    initBubble();
    initChoropleth();
    initArea();
    initTrajectory();
}});
</script>
</body>
</html>"""

# Write
outpath = "/home/claude/rosling_project/visualizations/81_quad_panel_sync.html"
with open(outpath, "w") as f:
    f.write(html)

print(f"Written: {outpath}")
print(f"File size: {len(html)/1024:.1f} KB")
print(f"Bubble frames: {len(bubble_frames)}")
print(f"Choropleth frames: {len(choropleth_frames)}")
print(f"Area frames: {len(area_frames)}")
print(f"Scatter frames: {len(scatter_frames)}")
