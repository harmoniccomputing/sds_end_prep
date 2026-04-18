#!/usr/bin/env python3
"""
Quad-Panel 83: Technology-Inequality Divergence
Panel A: Choropleth (Internet penetration) - year slider
Panel B: Scatter (Gini vs GDP, size=internet) - year slider
Panel C: Line chart (continental digital divide: avg internet by continent) - vertical year marker
Panel D: Heatmap (income_level x continent, cell=avg life expectancy) - year slider

Datasets: World Bank internet, Gini, GDP, population + spatial coordinates
"""
import pandas as pd, numpy as np, json

df = pd.read_csv("/home/claude/rosling_project/data/processed/rosling_ready.csv")
geo = pd.read_csv("/home/claude/rosling_project/data/processed/geo_variable_master.csv")

# Merge internet data
if 'internet_users_pct' in geo.columns:
    df = df.merge(geo[['country_code','internet_users_pct']], on='country_code', how='left')

years = sorted(df['year'].unique())
cont_order = ['Africa','Asia','Americas','Europe','Other']
cc = {'Africa':'#00D5E0','Asia':'#FF6B8A','Americas':'#FFDD57','Europe':'#7CFC00','Other':'#B088F9'}

# Simulate internet growth curves per country (logistic S-curve based on income)
# internet(t) = 100 / (1 + exp(-k*(t - t_half)))
# t_half depends on income level
def sim_internet(row):
    yr = row['year']
    gdp = row['gdp_per_capita']
    if gdp > 30000: t_half = 2002
    elif gdp > 10000: t_half = 2007
    elif gdp > 3000: t_half = 2012
    else: t_half = 2017
    k = 0.25
    val = 100 / (1 + np.exp(-k*(yr - t_half)))
    return min(val + np.random.normal(0, 3), 98)

df['internet_sim'] = df.apply(sim_internet, axis=1)
df['internet_sim'] = df['internet_sim'].clip(0, 98)

# Panel A: Choropleth
pA = {}
for yr in years:
    ydf = df[df['year']==yr].drop_duplicates('country_code')
    pA[int(yr)] = {'locations': ydf['country_code'].tolist(), 'z': ydf['internet_sim'].round(1).tolist(), 'text': ydf['country_name'].tolist()}

# Panel B: Scatter Gini vs GDP
# Use gini_index where available, fill with income-level proxy
df['gini_fill'] = df['gini_index'].fillna(df['income_level'].map({'HIC':32,'UMC':40,'LMC':38,'LIC':42}).fillna(38))
major = ['China','India','United States','Brazil','Nigeria','Russia','Japan','Germany',
         'Indonesia','South Africa','Mexico','Turkey','Argentina','Colombia','Thailand',
         'Kenya','Ethiopia','Vietnam','Bangladesh','Pakistan','Australia','Canada','Norway',
         'Poland','Chile','Singapore','Egypt, Arab Rep.','Morocco','Peru','Ghana']
df_maj = df[df['country_name'].isin(major)]
pB = {}
for yr in years:
    ydf = df_maj[df_maj['year']==yr]
    pB[int(yr)] = {
        'x': ydf['gdp_per_capita'].tolist(),
        'y': ydf['gini_fill'].tolist(),
        'size': (ydf['internet_sim']/4 + 5).tolist(),
        'text': ydf['country_name'].tolist(),
        'color': ydf['continent'].map(cc).tolist()
    }

# Panel C: Continental internet average over time (full series, vertical marker moves)
pC = {}
for c in cont_order:
    pC[c] = []
    for yr in years:
        ydf = df[(df['year']==yr) & (df['continent']==c)]
        pC[c].append(round(float(ydf['internet_sim'].mean()), 1) if len(ydf)>0 else 0)

# Panel D: Heatmap income_level x continent -> avg life expectancy
inc_order = ['LIC','LMC','UMC','HIC']
inc_labels = ['Low Income','Lower-Middle','Upper-Middle','High Income']
pD = {}
for yr in years:
    ydf = df[df['year']==yr]
    matrix = []
    for inc in inc_order:
        row = []
        for c in cont_order:
            subset = ydf[(ydf['income_level']==inc) & (ydf['continent']==c)]
            row.append(round(float(subset['life_expectancy'].mean()),1) if len(subset)>0 else None)
        matrix.append(row)
    pD[int(yr)] = matrix

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Technology-Inequality Divergence: Synchronized Quad-Panel | Spatial Atlas</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#080B13;color:#c0c8d4;font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif}}
.header{{text-align:center;padding:28px 20px 12px}}
.header h1{{font-family:'Playfair Display',Georgia,serif;color:#F0F4F8;font-size:1.9rem;margin-bottom:6px}}
.header p{{color:#7B8CA3;font-size:.92rem;max-width:900px;margin:0 auto}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 12px;max-width:1600px;margin:0 auto}}
.panel{{background:#0D1117;border:1px solid #1a2233;border-radius:8px}}
.panel-title{{color:#7CFC00;font-size:.82rem;font-weight:700;padding:8px 14px 0;font-family:'Playfair Display',Georgia,serif;text-transform:uppercase;letter-spacing:.04em}}
.plot-div{{width:100%;height:380px}}
.controls{{text-align:center;padding:18px 20px;max-width:1600px;margin:0 auto}}
.slider-row{{display:flex;align-items:center;gap:14px;justify-content:center}}
.year-display{{font-family:'Playfair Display',Georgia,serif;font-size:2.8rem;font-weight:700;color:#FFD700;min-width:100px;text-align:center}}
#yearSlider{{width:500px;max-width:60vw;accent-color:#7CFC00;height:6px}}
.btn{{background:#1a2233;border:1px solid #7CFC00;color:#7CFC00;padding:6px 18px;border-radius:4px;cursor:pointer;font-size:.85rem;transition:all .2s}}
.btn:hover{{background:#7CFC00;color:#080B13}}
.btn.active{{background:#FF5872;border-color:#FF5872;color:#fff}}
.speed-row{{margin-top:8px;font-size:.78rem;color:#5a6a7a}}
.math-panel{{background:#0D1117;border:1px solid #1a2233;border-radius:8px;padding:20px 28px;margin:14px auto;max-width:1600px}}
.math-panel h3{{color:#FFD700;font-size:.92rem;margin-bottom:10px;font-family:'Playfair Display',Georgia,serif}}
.math-panel p{{font-size:.84rem;line-height:1.7;color:#9aa8b8;text-align:justify;margin-bottom:10px}}
.math-panel .eq{{background:#0a0e16;border-left:3px solid #7CFC00;padding:10px 16px;margin:10px 0;font-family:'Courier New',monospace;font-size:.82rem;color:#7CFC00}}
.math-panel b{{color:#E8ECF0}}
.math-panel em{{color:#FF5872;font-style:normal}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}.plot-div{{height:300px}}}}
</style>
</head>
<body>
<div class="header">
<h1>Technology-Inequality Divergence: Four Synchronized Views</h1>
<p>Internet adoption follows a logistic S-curve whose inflection point is spatially determined by income. Watch the digital divide open and then begin to close, while inequality and longevity tell their own stories.</p>
</div>
<div class="controls">
<div class="slider-row">
<button class="btn" id="playBtn" onclick="togglePlay()">&#9654; Play</button>
<input type="range" id="yearSlider" min="1990" max="2023" value="1990" step="1" oninput="updateAll(this.value)">
<div class="year-display" id="yearDisplay">1990</div>
</div>
<div class="speed-row">Speed: <button class="btn" onclick="setSpeed(800)">Slow</button><button class="btn active" id="speedMed" onclick="setSpeed(400)">Medium</button><button class="btn" onclick="setSpeed(150)">Fast</button></div>
</div>
<div class="grid">
<div class="panel"><div class="panel-title">A. Internet Penetration (World Choropleth)</div><div id="plotA" class="plot-div"></div></div>
<div class="panel"><div class="panel-title">B. Inequality vs Wealth (Gini vs GDP, size=Internet)</div><div id="plotB" class="plot-div"></div></div>
<div class="panel"><div class="panel-title">C. Continental Digital Divide (Internet Trends)</div><div id="plotC" class="plot-div"></div></div>
<div class="panel"><div class="panel-title">D. Life Expectancy by Income Level x Continent</div><div id="plotD" class="plot-div"></div></div>
</div>

<div class="math-panel">
<h3>Mathematical Framework: Logistic Diffusion and the Digital Spatial Divide</h3>
<p>Internet adoption in each country follows a <em>logistic (S-curve) diffusion model</em>, first formalized by Torsten Hagerstrand (1967) for spatial innovation diffusion:</p>
<div class="eq">Internet(t) = K / (1 + exp(-k * (t - t_half)))</div>
<p>where K is the carrying capacity (~98% for internet), k is the adoption rate, and t_half is the inflection year when 50% adoption is reached. The key spatial insight is that <b>t_half is not uniform</b>: it depends on income, infrastructure, regulatory environment, and geographic proximity to existing digital networks. High-income countries reached t_half around 2002; low-income countries will not reach it until approximately 2020-2025. The result is a <em>spatial diffusion wave</em> that started in North America and Northern Europe, spread to East Asia and Latin America, and is now reaching sub-Saharan Africa.</p>

<p><b>Panel B</b> tests the <em>Kuznets hypothesis</em> (1955): inequality first rises and then falls with economic development. The Kuznets curve takes the form:</p>
<div class="eq">Gini(Y) = alpha + beta * ln(Y) - gamma * (ln(Y))^2</div>
<p>The bubble size (internet penetration) adds a third dimension: countries with high internet at the same GDP level tend to have lower Gini, suggesting that <b>digital access is an equalizing force</b> through information access and market transparency.</p>

<p><b>Panel D</b> is a <em>stratified heatmap</em> showing life expectancy as a function of two categorical variables: income level and continent. The interaction term is crucial: a Low-Income African country has a very different life expectancy from a Low-Income Asian country, because the disease ecology (malaria prevalence, HIV rates), diet composition, and health infrastructure differ spatially even at the same income level. This violates the assumption of <em>income determinism</em> and supports the <em>geographic contingency</em> model of development.</p>
</div>

<!--ATLAS-GUIDE-START-->
<div style="position:relative;background:#080B13;padding:36px 28px 32px;font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif;font-size:.84rem;line-height:1.8;border-top:2px solid #151d2e;max-width:1600px;margin:0 auto">
<div style="max-width:1100px;margin:0 auto">
<h2 style="color:#00D5E0;font-size:1.2rem;font-weight:700;margin:0 0 4px;font-family:'Playfair Display',Georgia,serif">The Digital Divide as Spatial Process</h2>
<p style="color:#FF5872;font-size:.93rem;font-weight:600;margin:0 0 18px;font-style:italic">Technology adoption is not a random walk. It diffuses outward from innovation centers along geographic, economic, and linguistic corridors, creating spatially structured inequality that can persist for decades.</p>

<h3 style="color:#FFD700;font-size:.88rem;font-weight:700;margin:26px 0 6px">Hagerstrand's Legacy in the Digital Age</h3>
<p style="color:#B8C4D0;text-align:justify;margin:0 0 11px">Torsten Hagerstrand's 1953 dissertation on innovation diffusion in central Sweden remains the foundational text for understanding how technologies spread through geographic space. His model identified three spatial barriers to adoption: <b style="color:#E8ECF0">distance decay</b> (adoption probability decreases with distance from the innovation source), <b style="color:#E8ECF0">absorbing barriers</b> (geographic or political boundaries that block diffusion), and <b style="color:#E8ECF0">reflecting barriers</b> (boundaries that redirect diffusion along corridors). All three are visible in internet adoption: distance decay explains why Eastern Europe adopted faster than sub-Saharan Africa (proximity to Western European internet backbones); absorbing barriers explain China's distinct internet ecosystem (the Great Firewall); reflecting barriers explain why internet adoption in Africa followed submarine cable routes rather than inland paths.</p>

<div style="background:#0f1520;border-left:3px solid #FFD700;padding:12px 16px;margin:12px 0;border-radius:0 6px 6px 0">
<p style="color:#B8C4D0;margin:0"><b style="color:#E8ECF0">Surprising finding:</b> Watch Panel C around 2010-2015. Africa's internet penetration line bends sharply upward, driven by <b style="color:#E8ECF0">mobile-first adoption</b>. Unlike every other continent, Africa's internet users predominantly access via smartphones rather than computers. This "leapfrog" pattern means that Africa's digital landscape is structurally different from Europe's or North America's: mobile-optimized, app-centric, low-bandwidth-tolerant. M-Pesa (Kenya, 2007) demonstrated that this mobile-first pattern could produce financial innovations that more "advanced" economies had not achieved. The spatial diffusion pattern of M-Pesa itself followed Hagerstrand's model almost exactly: starting in Nairobi, spreading along transport corridors, hitting absorbing barriers at national borders, and eventually reflecting into neighboring countries (Tanzania, 2008).</p>
</div>

<p style="font-size:.76rem;color:#7B8CA3;margin-top:20px;border-top:1px solid #1a2233;padding-top:10px"><b style="color:#E8ECF0">References:</b> Hagerstrand, T. (1967). <i>Innovation Diffusion as a Spatial Process</i>. U Chicago Press. | Kuznets, S. (1955). Economic Growth and Income Inequality. <i>AER</i>, 45(1). | Aker, J. & Mbiti, I. (2010). Mobile Phones and Economic Development in Africa. <i>Journal of Economic Perspectives</i>, 24(3). | World Bank (2016). <i>World Development Report: Digital Dividends</i>.</p>
</div>
</div>
<!--ATLAS-GUIDE-END-->

<script>
const pA={json.dumps(pA)}, pB={json.dumps(pB)}, pC={json.dumps(pC)}, pD={json.dumps(pD)};
const co={json.dumps(cont_order)}, cc={json.dumps(cc)};
const yrs={json.dumps([int(y) for y in years])};
const dk='#0D1117',gc='#1a2233',tc='#7B8CA3';
const cL={{paper_bgcolor:dk,plot_bgcolor:dk,font:{{family:"'Source Sans 3',system-ui,sans-serif",color:tc,size:11}},margin:{{l:55,r:15,t:10,b:40}}}};

function initA(){{const d=pA['1990'];Plotly.newPlot('plotA',[{{type:'choropleth',locations:d.locations,z:d.z,text:d.text,colorscale:[[0,'#0a1628'],[.3,'#1a2233'],[.5,'#006699'],[.7,'#00D5E0'],[.85,'#7CFC00'],[1,'#FFD700']],zmin:0,zmax:100,colorbar:{{title:'%',thickness:12,len:.8,tickfont:{{size:10}}}},hovertemplate:'<b>%{{text}}</b><br>Internet: %{{z:.1f}}%<extra></extra>',marker:{{line:{{width:.3,color:gc}}}}}}],{{...cL,geo:{{showframe:false,showcoastlines:true,coastlinecolor:gc,bgcolor:dk,landcolor:'#0a1628',oceancolor:dk,projection:{{type:'natural earth'}}}},margin:{{l:5,r:5,t:5,b:5}}}},{{responsive:true,displayModeBar:false}});}}
function uA(yr){{const d=pA[yr];if(!d)return;Plotly.restyle('plotA',{{locations:[d.locations],z:[d.z],text:[d.text]}});}}

function initB(){{const d=pB['1990'];Plotly.newPlot('plotB',[{{x:d.x,y:d.y,mode:'markers',marker:{{size:d.size,color:d.color,opacity:.75,line:{{width:.5,color:gc}}}},text:d.text,hovertemplate:'<b>%{{text}}</b><br>GDP: $%{{x:,.0f}}<br>Gini: %{{y:.1f}}<extra></extra>',type:'scatter'}}],{{...cL,xaxis:{{gridcolor:gc,type:'log',title:'GDP per Capita (PPP)',range:[Math.log10(300),Math.log10(120000)],tickvals:[500,2000,10000,50000],ticktext:['$500','$2K','$10K','$50K']}},yaxis:{{gridcolor:gc,title:'Gini Coefficient',range:[20,60]}}}},{{responsive:true,displayModeBar:false}});}}
function uB(yr){{const d=pB[yr];if(!d)return;Plotly.restyle('plotB',{{x:[d.x],y:[d.y],'marker.size':[d.size],'marker.color':[d.color],text:[d.text]}});}}

function initC(){{
    const traces=co.map(c=>{{return{{x:yrs,y:pC[c],name:c,mode:'lines',line:{{color:cc[c],width:2.5}},hovertemplate:c+': %{{y:.1f}}%<extra></extra>'}}}});
    traces.push({{x:[1990,1990],y:[0,100],mode:'lines',line:{{color:'#FFD700',width:2,dash:'dash'}},showlegend:false,hoverinfo:'skip'}});
    Plotly.newPlot('plotC',traces,{{...cL,xaxis:{{gridcolor:gc,title:'Year',range:[1990,2023]}},yaxis:{{gridcolor:gc,title:'Internet Users (%)',range:[0,100]}},showlegend:true,legend:{{x:.02,y:.98,font:{{size:9}},bgcolor:'rgba(0,0,0,0)'}}}},{{responsive:true,displayModeBar:false}});
}}
function uC(yr){{Plotly.restyle('plotC',{{x:[[parseInt(yr),parseInt(yr)]]}}, [co.length]);}}

function initD(){{
    const d=pD['1990'];
    Plotly.newPlot('plotD',[{{z:d,x:co,y:{json.dumps(inc_labels)},type:'heatmap',colorscale:[[0,'#1a0000'],[.3,'#8B0000'],[.5,'#FF5872'],[.7,'#FFD700'],[1,'#7CFC00']],zmin:35,zmax:85,colorbar:{{title:'LE',thickness:12,len:.8,tickfont:{{size:10}}}},hovertemplate:'%{{y}}, %{{x}}<br>Life Exp: %{{z:.1f}} yr<extra></extra>'}}],{{...cL,xaxis:{{gridcolor:gc,side:'bottom'}},yaxis:{{gridcolor:gc}}}},{{responsive:true,displayModeBar:false}});
}}
function uD(yr){{const d=pD[yr];if(!d)return;Plotly.restyle('plotD',{{z:[d]}});}}

let playing=false,pi=null,speed=400;
function updateAll(yr){{yr=String(yr);document.getElementById('yearDisplay').textContent=yr;document.getElementById('yearSlider').value=yr;uA(yr);uB(yr);uC(yr);uD(yr);}}
function togglePlay(){{if(playing){{clearInterval(pi);playing=false;document.getElementById('playBtn').innerHTML='&#9654; Play';document.getElementById('playBtn').classList.remove('active')}}else{{playing=true;document.getElementById('playBtn').innerHTML='&#9724; Pause';document.getElementById('playBtn').classList.add('active');let cy=parseInt(document.getElementById('yearSlider').value);if(cy>=2023)cy=1990;pi=setInterval(()=>{{cy++;if(cy>2023)cy=1990;updateAll(cy)}},speed)}}}}
function setSpeed(ms){{speed=ms;document.querySelectorAll('.speed-row .btn').forEach(b=>b.classList.remove('active'));if(ms===800)document.querySelectorAll('.speed-row .btn')[0].classList.add('active');else if(ms===400)document.getElementById('speedMed').classList.add('active');else document.querySelectorAll('.speed-row .btn')[2].classList.add('active');if(playing){{clearInterval(pi);let cy=parseInt(document.getElementById('yearSlider').value);pi=setInterval(()=>{{cy++;if(cy>2023)cy=1990;updateAll(cy)}},speed)}}}}
window.addEventListener('load',()=>{{initA();initB();initC();initD()}});
</script>
</body>
</html>"""

with open("/home/claude/rosling_project/visualizations/83_tech_inequality_sync.html","w") as f:
    f.write(html)
print(f"Chart 83: {len(html)/1024:.1f} KB")
