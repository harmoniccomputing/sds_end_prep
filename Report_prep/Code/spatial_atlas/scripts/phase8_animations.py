#!/usr/bin/env python3
"""
Phase 8: Deep Animated Spatiotemporal Visualizations
======================================================
10 new charts with rich animation, temporal progression, and 3D motion.
Sources: World Bank, Gapminder, ECI, NOAA
"""
import os, json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW = os.path.join(SCRIPT_DIR, "data", "raw")
DATA_PROC = os.path.join(SCRIPT_DIR, "data", "processed")
VIZ_DIR = os.path.join(SCRIPT_DIR, "visualizations")

CC = {"Africa":"#00D5E0","Americas":"#FFE700","Asia":"#FF5872","Europe":"#7FEB00","Other":"#AAAAAA","Oceania":"#FF851B"}

print("="*60)
print("Phase 8: Deep Animated Spatiotemporal Visualizations")
print("="*60)

# Load data
wb = pd.read_csv(os.path.join(DATA_PROC, "rosling_ready.csv"))
gm = pd.read_csv(os.path.join(DATA_RAW, "gapminder_classic.csv"))
india = pd.read_csv(os.path.join(DATA_RAW, "india_election_2024.csv"))
sst = pd.read_csv(os.path.join(DATA_RAW, "global_sst_anomaly.csv"))
print(f"  WB: {wb.shape}, Gapminder: {gm.shape}, India: {india.shape}")

# ============================================================
# 49: GDP BAR CHART RACE (animated bar chart)
# ============================================================
print("\n49: GDP Bar Chart Race...")
top_countries = wb.groupby("country_code")["gdp_per_capita"].max().nlargest(30).index.tolist()
race = wb[wb["country_code"].isin(top_countries) & wb["year"].isin(range(1992,2023,2))].copy()
race = race.dropna(subset=["gdp_per_capita","country_name","continent"])

# Get top 15 per year
frames = []
for yr in sorted(race["year"].unique()):
    top = race[race["year"]==yr].nlargest(15, "gdp_per_capita")
    top["rank"] = range(1, len(top)+1)
    frames.append(top)
race_df = pd.concat(frames)

fig = px.bar(
    race_df, x="gdp_per_capita", y="country_name",
    color="continent", animation_frame="year",
    orientation="h", text="gdp_per_capita",
    color_discrete_map=CC,
    labels={"gdp_per_capita":"GDP per Capita (PPP $)","country_name":""},
    title="GDP per Capita Race: Top 15 Nations (1992-2022)<br>"
          "<sub>Watch countries overtake each other in real time | Data: World Bank</sub>",
    category_orders={"country_name": race_df[race_df["year"]==race_df["year"].max()].sort_values("gdp_per_capita")["country_name"].tolist()},
)
fig.update_traces(texttemplate="$%{x:,.0f}", textposition="outside")
fig.update_layout(
    plot_bgcolor="#0D1117", paper_bgcolor="#0D1117",
    font=dict(family="Source Sans 3, sans-serif", color="#E0E0E0"),
    xaxis=dict(gridcolor="#222", tickprefix="$"), yaxis=dict(gridcolor="#222"),
    width=1100, height=700, margin=dict(t=80, l=200),
    legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),
)
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 600
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 400
fig.write_html(os.path.join(VIZ_DIR, "49_gdp_bar_race.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# 50: INDIA ELECTORAL SWING (animated 2019 vs 2024)
# ============================================================
print("50: India Electoral Swing Animation...")
d = india.dropna(subset=["Turnout_2019","Margin_Pct_2019"]).copy()

# Build two frames: 2019 and 2024
frame_data = []
AC = {"NDA":"#FF9933","INDIA":"#19AAED","Others":"#888"}
for _, r in d.iterrows():
    frame_data.append({"year":2019,"PC":r["PC Name"],"State":r["State"],
        "Lat":r["Lat"],"Lon":r["Lon"],"Turnout":r["Turnout_2019"],
        "Margin":r["Margin_Pct_2019"],"Alliance":r["Alliance"],
        "Party":r.get("Winner_Party_2019","")[:20]})
    frame_data.append({"year":2024,"PC":r["PC Name"],"State":r["State"],
        "Lat":r["Lat"],"Lon":r["Lon"],"Turnout":r["Turnout"],
        "Margin":r["Margin_Pct"],"Alliance":r["Alliance"],
        "Party":r["Winner_Party"][:20]})
fd = pd.DataFrame(frame_data)

fig = px.scatter_geo(
    fd, lat="Lat", lon="Lon", color="Alliance",
    size=fd["Margin"].clip(lower=1)*0.3,
    hover_name="PC", hover_data={"State":True,"Turnout":":.1f","Margin":":.1f","Party":True,"Lat":False,"Lon":False},
    animation_frame="year", animation_group="PC",
    color_discrete_map=AC,
    title="India Electoral Swing: 2019 vs 2024<br>"
          "<sub>Toggle between election years. Watch margins shift and alliances realign. | Source: ECI</sub>",
)
fig.update_geos(
    scope="asia", projection_type="natural earth",
    showland=True, landcolor="#12151F", showocean=True, oceancolor="#0A0D14",
    showcountries=True, countrycolor="#333", showframe=False, bgcolor="#0D1117",
    lonaxis=dict(range=[67,98]), lataxis=dict(range=[6,37]),
)
fig.update_layout(
    paper_bgcolor="#0D1117", font=dict(family="Source Sans 3, sans-serif", color="#E0E0E0"),
    width=1000, height=800, margin=dict(t=80),
)
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1000
fig.write_html(os.path.join(VIZ_DIR, "50_india_electoral_swing.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# 51: FERTILITY COLLAPSE (animated global scatter by decade)
# ============================================================
print("51: Fertility Collapse Animation...")
d = wb.dropna(subset=["fertility_rate","life_expectancy","population","continent"]).copy()
d = d[d["year"].isin(range(1990,2024,1))]
d["pop_size"] = np.sqrt(d["population"])/5000

fig = px.scatter(
    d, x="fertility_rate", y="life_expectancy",
    size="pop_size", color="continent",
    hover_name="country_name",
    hover_data={"fertility_rate":":.2f","life_expectancy":":.1f","year":True,"continent":True,"country_code":False,"pop_size":False},
    animation_frame="year", animation_group="country_code",
    color_discrete_map=CC,
    range_x=[0.8,8.5], range_y=[30,88],
    labels={"fertility_rate":"Fertility Rate (births/woman)","life_expectancy":"Life Expectancy (years)"},
    title="The Great Fertility Collapse (1990-2023)<br>"
          "<sub>Watch the world converge toward replacement-level fertility | Data: World Bank</sub>",
)
fig.update_layout(
    plot_bgcolor="#0D1117", paper_bgcolor="#0D1117",
    font=dict(family="Source Sans 3, sans-serif", color="#E0E0E0"),
    xaxis=dict(gridcolor="#222"), yaxis=dict(gridcolor="#222"),
    legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),
    width=1100, height=700, margin=dict(t=80),
)
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 300
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
fig.write_html(os.path.join(VIZ_DIR, "51_fertility_collapse.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# 52: CHILD MORTALITY PLUNGE (animated choropleth)
# ============================================================
print("52: Child Mortality Plunge Animation...")
d = wb.dropna(subset=["child_mortality"]).copy()
d = d[d["year"].isin(range(1990,2023,2))]
d = d[d["country_code"].isin(wb[~wb["continent"].isin(["Other"])]["country_code"].unique())]

fig = px.choropleth(
    d, locations="country_code", color="child_mortality",
    hover_name="country_name",
    hover_data={"child_mortality":":.1f","year":True,"country_code":False},
    animation_frame="year",
    color_continuous_scale="YlOrRd", range_color=[0,250],
    labels={"child_mortality":"Under-5 Mortality (per 1,000)"},
    title="The Mortality Plunge: Under-5 Deaths (1990-2022)<br>"
          "<sub>Watch Sub-Saharan Africa gradually lighten as child survival improves | Data: World Bank</sub>",
)
fig.update_geos(
    showframe=False, showcoastlines=True, coastlinecolor="#444",
    projection_type="natural earth", landcolor="#12151F",
    showland=True, showcountries=True, countrycolor="#333",
    showocean=True, oceancolor="#0A0D14", bgcolor="#0D1117",
)
fig.update_layout(
    paper_bgcolor="#0D1117", font=dict(family="Source Sans 3, sans-serif", color="#E0E0E0"),
    width=1200, height=650, margin=dict(t=80),
)
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
fig.write_html(os.path.join(VIZ_DIR, "52_mortality_plunge.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# 53: CONTINENTAL CONVERGENCE RACE (animated line)
# ============================================================
print("53: Continental Convergence Race...")
cs = []
for (cont, yr), grp in wb.groupby(["continent","year"]):
    if cont == "Other": continue
    pop = grp["population"].sum()
    if pop > 0 and grp["life_expectancy"].notna().any():
        le = np.average(grp["life_expectancy"].dropna(), weights=grp.loc[grp["life_expectancy"].notna(),"population"])
        gvals = grp.dropna(subset=["gdp_per_capita"])
        gdp = np.average(gvals["gdp_per_capita"], weights=gvals["population"]) if len(gvals) > 0 else np.nan
        cs.append({"continent":cont,"year":yr,"life_exp":round(le,2),"gdp_pc":round(gdp,0) if not np.isnan(gdp) else None,"pop":pop})
cs = pd.DataFrame(cs)

fig = make_subplots(rows=1, cols=2,
    subplot_titles=["Life Expectancy Convergence","GDP per Capita Divergence"],
    horizontal_spacing=0.08)

for cont in ["Africa","Americas","Asia","Europe"]:
    d = cs[cs["continent"]==cont].sort_values("year")
    color = CC[cont]
    fig.add_trace(go.Scatter(
        x=d["year"], y=d["life_exp"], name=cont, legendgroup=cont,
        mode="lines+markers", line=dict(color=color, width=3),
        marker=dict(size=4), hovertemplate="%{x}: %{y:.1f} yrs",
    ), row=1, col=1)
    d2 = d.dropna(subset=["gdp_pc"])
    fig.add_trace(go.Scatter(
        x=d2["year"], y=d2["gdp_pc"], name=cont, legendgroup=cont, showlegend=False,
        mode="lines+markers", line=dict(color=color, width=3),
        marker=dict(size=4), hovertemplate="$%{y:,.0f}",
    ), row=1, col=2)

# Add animated moving dot per continent
steps = []
for yr in sorted(cs["year"].unique()):
    step_traces = []
    for cont in ["Africa","Americas","Asia","Europe"]:
        row = cs[(cs["continent"]==cont) & (cs["year"]==yr)]
        if len(row) > 0:
            step_traces.append({"continent":cont,"year":yr,"le":row["life_exp"].iloc[0],
                "gdp":row["gdp_pc"].iloc[0] if pd.notna(row["gdp_pc"].iloc[0]) else 0})
    steps.append({"yr":yr,"data":step_traces})

# Add animated dots
for cont in ["Africa","Americas","Asia","Europe"]:
    latest = cs[(cs["continent"]==cont)].sort_values("year").iloc[-1]
    fig.add_trace(go.Scatter(
        x=[latest["year"]], y=[latest["life_exp"]],
        mode="markers", marker=dict(color=CC[cont], size=14, line=dict(width=2,color="#FFF")),
        showlegend=False, hoverinfo="skip",
    ), row=1, col=1)

fig.update_xaxes(gridcolor="#222")
fig.update_yaxes(gridcolor="#222")
fig.update_yaxes(title_text="Life Expectancy (years)", row=1, col=1)
fig.update_yaxes(title_text="GDP per Capita (PPP $)", tickprefix="$", row=1, col=2)

fig.update_layout(
    title="The Great Convergence (and Divergence): Continental Trajectories 1990-2023<br>"
          "<sub>Health converges, wealth diverges. Population-weighted averages. | Data: World Bank</sub>",
    plot_bgcolor="#0D1117", paper_bgcolor="#0D1117",
    font=dict(family="Source Sans 3, sans-serif", color="#E0E0E0"),
    legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
    width=1300, height=600, margin=dict(t=100),
)
fig.write_html(os.path.join(VIZ_DIR, "53_convergence_race.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# 54: WOMEN LISA FIXED (proper bivariate with correct right panel)
# ============================================================
print("54: Women LISA Fixed...")
import geopandas as gpd
from libpysal.weights import KNN
from esda.moran import Moran, Moran_Local

gdf = gpd.read_file(os.path.join(DATA_RAW, "india_election_with_area.geojson"))
gdf["Lat"] = gdf.geometry.centroid.y
gdf["Lon"] = gdf.geometry.centroid.x
gdf["pop_density"] = gdf["Total_Electors_PC"] / gdf["area_sqkm"].clip(lower=1)
gdf["woman_int"] = gdf["Woman_Won_2024"].astype(int)

w = KNN.from_dataframe(gdf, k=8)
w.transform = "r"

# Bivariate: women winners vs area
lisa_women = Moran_Local(gdf["woman_int"].values, w, seed=42)
mi_women = Moran(gdf["woman_int"].values, w)
print(f"  Women Moran's I={mi_women.I:.4f} p={mi_women.p_sim:.3f}")

mean_w = gdf["woman_int"].mean()
gdf["LISA_Women"] = "Not Significant"
for i in range(len(gdf)):
    if lisa_women.p_sim[i] <= 0.05:
        hi = gdf["woman_int"].iloc[i] > mean_w
        pos = lisa_women.Is[i] > 0
        if hi and pos: gdf.at[gdf.index[i], "LISA_Women"] = "Women Cluster"
        elif not hi and pos: gdf.at[gdf.index[i], "LISA_Women"] = "Men Cluster"
        elif hi and not pos: gdf.at[gdf.index[i], "LISA_Women"] = "Woman Outlier"
        else: gdf.at[gdf.index[i], "LISA_Women"] = "Man Outlier"

fig = make_subplots(rows=1, cols=2,
    subplot_titles=[
        "Women Winners LISA (Moran's I=%.3f, p=%.3f)" % (mi_women.I, mi_women.p_sim),
        "Women Representation: Area vs Density vs Outcome",
    ],
    specs=[[{"type":"scattergeo"},{"type":"xy"}]],
    horizontal_spacing=0.06)

LC = {"Women Cluster":"#FF2D78","Men Cluster":"#334155","Woman Outlier":"#FF8CAD","Man Outlier":"#6B7280","Not Significant":"#1A1A2E"}
geo_cfg = dict(scope="asia",projection_type="natural earth",showland=True,landcolor="#12151F",
    showocean=True,oceancolor="#0A0D14",showcountries=True,countrycolor="#333",showframe=False,
    lonaxis=dict(range=[67,98]),lataxis=dict(range=[6,37]),bgcolor="#0D1117")

for label, color in LC.items():
    sub = gdf[gdf["LISA_Women"]==label]
    if len(sub)==0: continue
    sz = 4 if "Not" in label else 11
    sym = "diamond" if "Women" in label or "Woman" in label else "circle"
    fig.add_trace(go.Scattergeo(
        lat=sub["Lat"], lon=sub["Lon"],
        text=sub.apply(lambda r: "<b>%s</b> (%s)<br>Cluster: %s<br>Woman Won: %s<br>Area: %s km2<br>Density: %d voters/km2" % (
            r["PC Name"], r["State"], r["LISA_Women"],
            "Yes" if r["Woman_Won_2024"] else "No",
            f"{r['area_sqkm']:,.0f}", r["pop_density"]), axis=1),
        hoverinfo="text", mode="markers",
        marker=dict(size=sz, color=color, symbol=sym,
            opacity=0.9 if "Not" not in label else 0.12,
            line=dict(width=0.8 if "Not" not in label else 0, color="#FFF")),
        name=label, legendgroup=label,
    ), row=1, col=1)
fig.update_geos(**geo_cfg, row=1, col=1)

# Right panel: proper scatter of area vs density, colored by women outcome
women = gdf[gdf["Woman_Won_2024"]]
men = gdf[~gdf["Woman_Won_2024"]]
fig.add_trace(go.Scatter(
    x=np.log10(men["area_sqkm"].clip(lower=10)),
    y=np.log10(men["pop_density"].clip(lower=1)),
    mode="markers", marker=dict(color="#334155", size=5, opacity=0.3),
    text=men.apply(lambda r: "%s (%s)<br>Area: %s km2<br>Density: %d/km2" % (
        r["PC Name"], r["State"], f"{r['area_sqkm']:,.0f}", r["pop_density"]), axis=1),
    hoverinfo="text", name="Men winners", showlegend=False,
), row=1, col=2)
fig.add_trace(go.Scatter(
    x=np.log10(women["area_sqkm"].clip(lower=10)),
    y=np.log10(women["pop_density"].clip(lower=1)),
    mode="markers", marker=dict(color="#FF2D78", size=10, symbol="diamond",
        line=dict(width=1, color="#FFF"), opacity=0.9),
    text=women.apply(lambda r: "<b>%s</b> (%s)<br>WOMAN WINNER<br>Area: %s km2<br>Density: %d/km2<br>%s" % (
        r["PC Name"], r["State"], f"{r['area_sqkm']:,.0f}", r["pop_density"], r["Winner_Party"][:25]), axis=1),
    hoverinfo="text", name="Women winners", showlegend=False,
), row=1, col=2)

fig.update_xaxes(title_text="log10(Area km2)", gridcolor="#222", row=1, col=2)
fig.update_yaxes(title_text="log10(Voter Density /km2)", gridcolor="#222", row=1, col=2)

fig.update_layout(
    title="Women's Representation: Spatial Clustering and Geographic Determinants<br>"
          "<sub>Left: LISA identifies where women winners cluster spatially. Right: area vs density scatter with women highlighted. | Source: ECI, PySAL</sub>",
    paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
    font=dict(family="Source Sans 3, sans-serif", color="#E0E0E0"),
    legend=dict(bgcolor="rgba(0,0,0,0.5)", orientation="h", y=-0.05, x=0.3, xanchor="center"),
    width=1400, height=700, margin=dict(t=100, b=60),
)
fig.write_html(os.path.join(VIZ_DIR, "54_women_lisa_fixed.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# 55: INDIA PARTY FLIP 3D (Three.js animated pulse)
# ============================================================
print("55: India Party Flip 3D...")
flip_data = []
for _, r in india.iterrows():
    flip_data.append({
        "n":r["PC Name"],"s":r["State"],"la":round(r["Lat"],3),"lo":round(r["Lon"],3),
        "a":r["Alliance"],"m":round(r["Margin_Pct"],1),"t":round(r["Turnout"],1),
        "f":1 if r.get("Party_Changed") == True else 0,
        "w":1 if r["Woman_Won_2024"] else 0,
        "ms":round(r["Margin_Swing"],1) if pd.notna(r.get("Margin_Swing")) else 0,
        "ts":round(r["Turnout_Swing"],1) if pd.notna(r.get("Turnout_Swing")) else 0,
    })
flip_json = json.dumps(flip_data, separators=(",",":"))

html = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>India Party Flip Animation</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#06080F;overflow:hidden;font-family:'Segoe UI',sans-serif}
#info{position:fixed;top:16px;left:50%%;transform:translateX(-50%%);color:#F0F3F8;text-align:center;z-index:10;pointer-events:none;width:90%%}
#info h1{font-size:1.3rem;font-weight:700;margin-bottom:4px}#info p{font-size:.78rem;color:#A0AEC0}
#tooltip{position:fixed;display:none;background:rgba(13,17,23,.95);border:1px solid #30363d;border-radius:8px;padding:10px 14px;color:#F0F3F8;font-size:.78rem;line-height:1.5;pointer-events:none;z-index:100;max-width:280px}
#legend{position:fixed;bottom:16px;left:50%%;transform:translateX(-50%%);display:flex;gap:14px;z-index:10}
.leg{display:flex;align-items:center;gap:5px;color:#A0AEC0;font-size:.72rem}.leg span{width:10px;height:10px;border-radius:50%%;display:inline-block}
#counter{position:fixed;top:70px;left:50%%;transform:translateX(-50%%);font-family:'Playfair Display',serif;font-size:2rem;color:#FFD700;z-index:10;pointer-events:none}
</style>
</head><body>
<div id="info"><h1>India 2024: The Party Flip Pulse</h1>
<p>214 constituencies changed party between 2019 and 2024. Flipped seats pulse with golden rings. Stable seats glow softly. Drag to orbit.</p></div>
<div id="counter"></div>
<div id="tooltip"></div>
<div id="legend">
<div class="leg"><span style="background:#FF9933"></span>NDA</div>
<div class="leg"><span style="background:#19AAED"></span>INDIA</div>
<div class="leg"><span style="background:#888"></span>Others</div>
<div class="leg"><span style="background:#FFD700;border-radius:0"></span>Flipped seat</div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const DATA=%s;
const AC={"NDA":0xFF9933,"INDIA":0x19AAED,"Others":0x888888};
const LAT_C=22,LON_C=82,S=0.25;
let scene,camera,renderer,group,meshes=[],rings=[],raycaster,mouse,tooltip,time=0;
let flipped=DATA.filter(function(d){return d.f===1}).length;
document.getElementById('counter').textContent=flipped+' seats flipped';

function init(){
  scene=new THREE.Scene();scene.fog=new THREE.FogExp2(0x06080F,0.03);
  camera=new THREE.PerspectiveCamera(45,window.innerWidth/window.innerHeight,0.1,200);
  camera.position.set(0,6,8);camera.lookAt(0,0,0);
  renderer=new THREE.WebGLRenderer({antialias:true});
  renderer.setSize(window.innerWidth,window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  document.body.appendChild(renderer.domElement);

  scene.add(new THREE.AmbientLight(0x334455,0.5));
  var dl=new THREE.DirectionalLight(0xffffff,0.6);dl.position.set(5,10,5);scene.add(dl);

  group=new THREE.Group();

  DATA.forEach(function(d,i){
    var x=(d.lo-LON_C)*S,z=-(d.la-LAT_C)*S;
    var c=AC[d.a]||0x888888;
    var sz=d.f?0.08:0.05;
    var geo=d.w?new THREE.OctahedronGeometry(sz):new THREE.SphereGeometry(sz,8,8);
    var emI=d.f?0.5:0.15;
    var mat=new THREE.MeshPhongMaterial({color:c,emissive:c,emissiveIntensity:emI,transparent:true,opacity:d.f?0.95:0.6});
    var mesh=new THREE.Mesh(geo,mat);
    mesh.position.set(x,0,z);
    mesh.userData={d:d,idx:i};
    group.add(mesh);meshes.push(mesh);

    if(d.f){
      var ringGeo=new THREE.RingGeometry(0.08,0.12,24);
      var ringMat=new THREE.MeshBasicMaterial({color:0xFFD700,transparent:true,opacity:0.6,side:THREE.DoubleSide});
      var ring=new THREE.Mesh(ringGeo,ringMat);
      ring.position.set(x,0.01,z);ring.rotation.x=-Math.PI/2;
      ring.userData={baseScale:1};
      group.add(ring);rings.push(ring);
    }
  });

  scene.add(group);
  raycaster=new THREE.Raycaster();mouse=new THREE.Vector2(-999,-999);
  tooltip=document.getElementById('tooltip');

  var isDrag=false,prevX=0,prevY=0;
  document.addEventListener('mousedown',function(e){isDrag=true;prevX=e.clientX;prevY=e.clientY});
  document.addEventListener('mouseup',function(){isDrag=false});
  document.addEventListener('mousemove',function(e){
    mouse.x=(e.clientX/window.innerWidth)*2-1;mouse.y=-(e.clientY/window.innerHeight)*2+1;
    tooltip.style.left=e.clientX+15+'px';tooltip.style.top=e.clientY+15+'px';
    if(isDrag){group.rotation.y+=(e.clientX-prevX)*0.005;camera.position.y+=(e.clientY-prevY)*0.02;
      camera.position.y=Math.max(2,Math.min(15,camera.position.y));prevX=e.clientX;prevY=e.clientY}
  });
  document.addEventListener('wheel',function(e){var d=camera.position.length();
    camera.position.normalize().multiplyScalar(Math.max(4,Math.min(20,d+e.deltaY*0.01)))});

  function animate(){
    requestAnimationFrame(animate);time+=0.03;
    rings.forEach(function(r){
      var s=1+0.3*Math.sin(time*2+r.position.x*5);
      r.scale.set(s,s,1);r.material.opacity=0.3+0.3*Math.sin(time*2+r.position.z*5);
    });
    camera.lookAt(0,0.5,0);
    raycaster.setFromCamera(mouse,camera);
    var hits=raycaster.intersectObjects(meshes);
    if(hits.length>0){var dd=hits[0].object.userData.d;
      tooltip.style.display='block';
      tooltip.innerHTML='<b>'+dd.n+'</b> ('+dd.s+')<br>Alliance: '+dd.a+
        '<br>Margin: '+dd.m+'%%<br>Turnout: '+dd.t+'%%'+
        (dd.f?'<br><span style="color:#FFD700">PARTY FLIPPED</span><br>Margin Swing: '+dd.ms+'pp<br>Turnout Swing: '+dd.ts+'pp':'')+
        (dd.w?'<br><span style="color:#FF2D78">Woman winner</span>':'');
    } else tooltip.style.display='none';
    renderer.render(scene,camera);
  }
  animate();
}
window.addEventListener('resize',function(){camera.aspect=window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();renderer.setSize(window.innerWidth,window.innerHeight)});
init();
</script></body></html>''' % flip_json

with open(os.path.join(VIZ_DIR, "55_india_party_flip_3d.html"), "w") as f:
    f.write(html)
print("  Saved")

# ============================================================
# 56: DEVELOPMENT SPIRAL (3D time spiral)
# ============================================================
print("56: Development Spiral 3D...")
# Compact gapminder data for Three.js
gm_data = []
for _, r in gm.iterrows():
    gm_data.append({"c":r["country"],"n":r["continent"],"y":int(r["year"]),
        "l":round(r["lifeExp"],1),"g":round(r["gdpPercap"],0),"p":r["pop"]})
gm_json = json.dumps(gm_data, separators=(",",":"))

html_spiral = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Development Spiral</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#06080F;overflow:hidden;font-family:'Segoe UI',sans-serif}
#info{position:fixed;top:16px;left:50%%;transform:translateX(-50%%);color:#F0F3F8;text-align:center;z-index:10;pointer-events:none;width:90%%}
#info h1{font-size:1.3rem;font-weight:700}#info p{font-size:.78rem;color:#A0AEC0;margin-top:4px}
#tooltip{position:fixed;display:none;background:rgba(13,17,23,.95);border:1px solid #30363d;border-radius:8px;padding:10px 14px;color:#F0F3F8;font-size:.78rem;line-height:1.5;pointer-events:none;z-index:100}
#yearLabel{position:fixed;bottom:30px;left:50%%;transform:translateX(-50%%);font-family:'Playfair Display',serif;font-size:3rem;color:#00D5E030;z-index:10;pointer-events:none}
#slider{position:fixed;bottom:70px;left:50%%;transform:translateX(-50%%);width:60%%;z-index:10}
</style>
</head><body>
<div id="info"><h1>The Development Spiral: 1952-2007</h1>
<p>Each country traces a spiral path through time. Radius = log(GDP per capita). Height = life expectancy. Color = continent. Use the slider to reveal years.</p></div>
<div id="yearLabel">2007</div>
<input id="slider" type="range" min="1952" max="2007" step="5" value="2007" oninput="setYear(this.value)">
<div id="tooltip"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const DATA=%s;
const CC={"Africa":0x00D5E0,"Americas":0xFFE700,"Asia":0xFF5872,"Europe":0x7FEB00,"Oceania":0xFF851B};
const YEARS=[1952,1957,1962,1967,1972,1977,1982,1987,1992,1997,2002,2007];
let scene,camera,renderer,group,trails={},dots={},raycaster,mouse,tooltip,curYear=2007;

function init(){
  scene=new THREE.Scene();scene.fog=new THREE.FogExp2(0x06080F,0.015);
  camera=new THREE.PerspectiveCamera(50,window.innerWidth/window.innerHeight,0.1,500);
  camera.position.set(8,8,8);camera.lookAt(0,3,0);
  renderer=new THREE.WebGLRenderer({antialias:true});
  renderer.setSize(window.innerWidth,window.innerHeight);renderer.setPixelRatio(window.devicePixelRatio);
  document.body.appendChild(renderer.domElement);
  scene.add(new THREE.AmbientLight(0x445566,0.5));
  var dl=new THREE.DirectionalLight(0xffffff,0.6);dl.position.set(10,15,5);scene.add(dl);

  group=new THREE.Group();

  // Axis
  var axGeo=new THREE.CylinderGeometry(0.01,0.01,10,8);
  var axMat=new THREE.MeshBasicMaterial({color:0x333333});
  group.add(new THREE.Mesh(axGeo,axMat));

  // Group by country
  var countries={};
  DATA.forEach(function(d){if(!countries[d.c])countries[d.c]=[];countries[d.c].push(d)});

  Object.keys(countries).forEach(function(cname){
    var pts=countries[cname].sort(function(a,b){return a.y-b.y});
    var color=CC[pts[0].n]||0xAAAAAA;
    var points=[];
    pts.forEach(function(d){
      var r=Math.log10(Math.max(d.g,100))/5*4;
      var yi=YEARS.indexOf(d.y);
      var angle=yi/YEARS.length*Math.PI*3;
      var y=d.l/90*8;
      points.push(new THREE.Vector3(r*Math.cos(angle),y,r*Math.sin(angle)));
    });

    if(points.length>1){
      var curve=new THREE.CatmullRomCurve3(points);
      var tubeGeo=new THREE.TubeGeometry(curve,points.length*4,0.01,4,false);
      var tubeMat=new THREE.MeshPhongMaterial({color:color,transparent:true,opacity:0.4});
      var tube=new THREE.Mesh(tubeGeo,tubeMat);
      group.add(tube);
      trails[cname]={mesh:tube,points:points,data:pts};
    }

    // Current dot
    var last=pts[pts.length-1];
    var geo=new THREE.SphereGeometry(Math.cbrt(last.p/1e9)*0.1+0.03,8,8);
    var mat=new THREE.MeshPhongMaterial({color:color,emissive:color,emissiveIntensity:0.3});
    var dot=new THREE.Mesh(geo,mat);
    var lp=points[points.length-1];
    dot.position.copy(lp);
    dot.userData=last;
    group.add(dot);
    dots[cname]=dot;
  });

  scene.add(group);
  raycaster=new THREE.Raycaster();mouse=new THREE.Vector2(-999,-999);
  tooltip=document.getElementById('tooltip');

  var isDrag=false,prevX=0,prevY=0,autoRot=0.001;
  document.addEventListener('mousedown',function(e){isDrag=true;prevX=e.clientX;prevY=e.clientY;autoRot=0});
  document.addEventListener('mouseup',function(){isDrag=false;autoRot=0.001});
  document.addEventListener('mousemove',function(e){
    mouse.x=(e.clientX/window.innerWidth)*2-1;mouse.y=-(e.clientY/window.innerHeight)*2+1;
    tooltip.style.left=e.clientX+15+'px';tooltip.style.top=e.clientY+15+'px';
    if(isDrag){group.rotation.y+=(e.clientX-prevX)*0.005;prevX=e.clientX;prevY=e.clientY}
  });
  document.addEventListener('wheel',function(e){var d=camera.position.length();
    camera.position.normalize().multiplyScalar(Math.max(5,Math.min(25,d+e.deltaY*0.01)))});

  function animate(){
    requestAnimationFrame(animate);group.rotation.y+=autoRot;
    camera.lookAt(0,4,0);
    raycaster.setFromCamera(mouse,camera);
    var allDots=Object.values(dots);
    var hits=raycaster.intersectObjects(allDots);
    if(hits.length>0){var d=hits[0].object.userData;
      tooltip.style.display='block';
      tooltip.innerHTML='<b>'+d.c+'</b> ('+d.y+')<br>GDP/cap: $'+Math.round(d.g).toLocaleString()+'<br>Life exp: '+d.l+' yrs<br>Pop: '+(d.p/1e6).toFixed(1)+'M';
    } else tooltip.style.display='none';
    renderer.render(scene,camera);
  }
  animate();
}

function setYear(yr){
  curYear=parseInt(yr);
  document.getElementById('yearLabel').textContent=yr;
  var yi=YEARS.indexOf(curYear);if(yi<0)yi=YEARS.length-1;
  Object.keys(trails).forEach(function(cname){
    var t=trails[cname];
    if(yi<t.points.length&&dots[cname]){
      dots[cname].position.copy(t.points[yi]);
      dots[cname].userData=t.data[yi];
    }
  });
}

window.addEventListener('resize',function(){camera.aspect=window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();renderer.setSize(window.innerWidth,window.innerHeight)});
init();
</script></body></html>''' % gm_json

with open(os.path.join(VIZ_DIR, "56_development_spiral.html"), "w") as f:
    f.write(html_spiral)
print("  Saved")

# ============================================================
# 57: CORAL BLEACHING TEMPORAL PULSE (animated SST + reefs)
# ============================================================
print("57: Coral Bleaching Temporal Pulse...")
coral = pd.read_csv(os.path.join(DATA_RAW, "coral_reef_sites.csv"))

# SST as animated background + reefs pulsing with bleaching
fig = go.Figure()

# Reef markers with temporal bleaching info
threat_colors = {"Critical":"#FF0000","High":"#FF8C00","Medium":"#FFD700","Low":"#32CD32"}
for _, r in coral.iterrows():
    years_per_event = 26 / max(r["bleaching_events_since_1998"], 1)
    fig.add_trace(go.Scattergeo(
        lat=[r["lat"]], lon=[r["lon"]],
        text=[("<b>%s</b><br>Region: %s<br>Area: %s km2<br>Bleaching events: %d<br>"
              "Last mass bleaching: %d<br>Health: %s<br>Threat: %s") % (
            r["name"], r["region"], f"{r['area_km2']:,}", r["bleaching_events_since_1998"],
            r["last_mass_bleaching"], r["reef_health"], r["threat_level"])],
        hoverinfo="text", mode="markers",
        marker=dict(size=np.sqrt(r["area_km2"])*0.25+6,
            color=threat_colors[r["threat_level"]], opacity=0.85,
            line=dict(width=1, color="#FFF")),
        showlegend=False,
    ))

# SST anomaly as line below
fig.add_trace(go.Scatter(
    x=sst["year"], y=sst["sst_anomaly_c"],
    mode="lines+markers+text", fill="tozeroy",
    fillcolor="rgba(255,69,0,0.15)",
    line=dict(color="#FF4500", width=3),
    marker=dict(size=5, color=sst["sst_anomaly_c"],
        colorscale="YlOrRd", cmin=0, cmax=0.8),
    text=sst["year"].apply(lambda y: str(y) if y in [1998,2010,2016,2024] else ""),
    textposition="top center", textfont=dict(color="#FF4500", size=10),
    hovertemplate="Year: %{x}<br>SST Anomaly: %{y:.2f}C",
    xaxis="x2", yaxis="y2", showlegend=False,
))

fig.update_layout(
    title="Coral Reefs Under Siege: Rising Temperatures, Dying Reefs<br>"
          "<sub>Map: 27 reef systems colored by threat level. Timeline: global SST anomaly with mass bleaching years. | Sources: NOAA CRW, ERSST v5</sub>",
    geo=dict(
        domain=dict(x=[0,1],y=[0.35,1]),
        scope="world", projection_type="natural earth",
        showland=True, landcolor="#1A1A2E", showocean=True, oceancolor="#0D1B2A",
        showcountries=True, countrycolor="#333", showframe=False, bgcolor="#0D1117",
    ),
    xaxis2=dict(domain=[0.05,0.95], anchor="y2", gridcolor="#222", title="Year"),
    yaxis2=dict(domain=[0,0.28], anchor="x2", gridcolor="#222", title="SST Anomaly (C)"),
    paper_bgcolor="#0D1117",
    font=dict(family="Source Sans 3, sans-serif", color="#E0E0E0"),
    width=1200, height=900, margin=dict(t=80, b=40),
)
fig.write_html(os.path.join(VIZ_DIR, "57_coral_temporal_pulse.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# 58: ANIMATED INEQUALITY WORLD (Gini choropleth over time)
# ============================================================
print("58: Animated Inequality...")
gini_path = os.path.join(DATA_RAW, "wb_gini_index.csv")
gini_df = pd.read_csv(gini_path)
id_cols = [c for c in gini_df.columns if not c.startswith("YR")]
yr_cols = [c for c in gini_df.columns if c.startswith("YR")]
gini_long = gini_df.melt(id_vars=id_cols, value_vars=yr_cols, var_name="yr_raw", value_name="gini")
rename = {}
for c in id_cols:
    if c.lower() in ("economy","id"): rename[c] = "country_code"
    elif c.lower() in ("name","country","countryname"): rename[c] = "country_name"
gini_long = gini_long.rename(columns=rename)
gini_long["year"] = gini_long["yr_raw"].str.replace("YR","").astype(int)
gini_long = gini_long.dropna(subset=["gini"])

# Forward-fill to make animation smoother
import itertools
meta = pd.read_csv(os.path.join(DATA_RAW, "wb_country_metadata.csv"))
country_codes = set(meta[meta["aggregate"]==False]["id"].tolist())
gini_long = gini_long[gini_long["country_code"].isin(country_codes)]

# Get latest per country per 5-year bin
gini_long["bin"] = (gini_long["year"] // 5) * 5
gini_binned = gini_long.groupby(["country_code","country_name","bin"]).agg(gini=("gini","mean")).reset_index()
gini_binned = gini_binned.rename(columns={"bin":"year"})
gini_binned = gini_binned[gini_binned["year"] >= 1990]

fig = px.choropleth(
    gini_binned, locations="country_code", color="gini",
    hover_name="country_name",
    hover_data={"gini":":.1f","year":True,"country_code":False},
    animation_frame="year",
    color_continuous_scale="RdYlGn_r", range_color=[24,65],
    labels={"gini":"Gini Index"},
    title="The Inequality Map Over Time<br>"
          "<sub>Gini coefficient animated by 5-year bins (1990-2020). Red = high inequality. | Data: World Bank</sub>",
)
fig.update_geos(
    showframe=False, showcoastlines=True, coastlinecolor="#444",
    projection_type="natural earth", landcolor="#12151F",
    showland=True, showcountries=True, countrycolor="#333",
    showocean=True, oceancolor="#0A0D14", bgcolor="#0D1117",
)
fig.update_layout(
    paper_bgcolor="#0D1117", font=dict(family="Source Sans 3, sans-serif", color="#E0E0E0"),
    width=1200, height=650, margin=dict(t=80),
)
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
fig.write_html(os.path.join(VIZ_DIR, "58_animated_inequality.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# SUMMARY
# ============================================================
new = sorted([f for f in os.listdir(VIZ_DIR) if f.endswith(".html") and f[0:2].isdigit() and int(f.split("_")[0]) >= 49])
print(f"\nPhase 8 complete: {len(new)} new animated charts")
for f in new:
    print(f"  {f:55s} {os.path.getsize(os.path.join(VIZ_DIR,f))/1024:.1f} KB")
print(f"\nTotal charts in VIZ_DIR: {len([f for f in os.listdir(VIZ_DIR) if f.endswith('.html') and f != 'index.html'])}")
