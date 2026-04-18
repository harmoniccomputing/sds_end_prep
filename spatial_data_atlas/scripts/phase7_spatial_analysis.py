#!/usr/bin/env python3
"""
Phase 7: TA Hypotheses - Women+Area, 3D Extruded Map, State LISA
Sources: ECI via OpenCity.in, DataMeet, PySAL/esda
"""
import os, json
import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from libpysal.weights import KNN
from esda.moran import Moran, Moran_Local

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW = os.path.join(SCRIPT_DIR, "data", "raw")
VIZ_DIR = os.path.join(SCRIPT_DIR, "visualizations")

print("="*60)
print("Phase 7: TA Hypotheses")
print("="*60)

gdf = gpd.read_file(os.path.join(DATA_RAW, "india_election_with_area.geojson"))
gdf["Lat"] = gdf.geometry.centroid.y
gdf["Lon"] = gdf.geometry.centroid.x
gdf["pop_density"] = gdf["Total_Electors_PC"] / gdf["area_sqkm"].clip(lower=1)
gdf["log_area"] = np.log10(gdf["area_sqkm"].clip(lower=10))
print(f"  {len(gdf)} constituencies loaded")

# ============================================================
# 46: WOMEN + AREA + DENSITY HYPOTHESIS
# ============================================================
print("\nPlot 46: Women + Area + Density Hypothesis...")

fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=[
        "Are Women Winning in Larger Constituencies?",
        "Women vs Population Density",
        "Women by Reservation Category + Area",
    ],
    horizontal_spacing=0.06,
)

# Panel 1: Area distribution by gender of winner (box + strip)
for gender, color, label in [(True, "#FF2D78", "Women"), (False, "#3B82F6", "Men")]:
    sub = gdf[gdf["Woman_Won_2024"] == gender]
    fig.add_trace(go.Box(
        y=sub["log_area"], name=label,
        marker_color=color, boxmean=True,
        boxpoints="all", jitter=0.4, pointpos=0,
        marker=dict(size=4, opacity=0.5),
        text=sub.apply(lambda r: "%s (%s)<br>Area: %s km2<br>%s" % (
            r["PC Name"], r["State"], f"{r['area_sqkm']:,.0f}", r["Winner_Party"][:25]
        ), axis=1),
        hoverinfo="text",
    ), row=1, col=1)

# Panel 2: Density scatter - women as highlighted diamonds
men = gdf[~gdf["Woman_Won_2024"]]
women = gdf[gdf["Woman_Won_2024"]]
fig.add_trace(go.Scatter(
    x=np.log10(men["pop_density"].clip(lower=1)),
    y=men["Margin_Pct"], mode="markers",
    marker=dict(color="#334155", size=5, opacity=0.3),
    text=men.apply(lambda r: "%s (%s)<br>Density: %d voters/km2<br>Margin: %.1f%%" % (
        r["PC Name"], r["State"], r["pop_density"], r["Margin_Pct"]), axis=1),
    hoverinfo="text", name="Men winners", showlegend=False,
), row=1, col=2)
fig.add_trace(go.Scatter(
    x=np.log10(women["pop_density"].clip(lower=1)),
    y=women["Margin_Pct"], mode="markers",
    marker=dict(color="#FF2D78", size=10, symbol="diamond",
                line=dict(width=1, color="#FFF"), opacity=0.9),
    text=women.apply(lambda r: "%s (%s)<br>Density: %d voters/km2<br>Margin: %.1f%%<br>%s" % (
        r["PC Name"], r["State"], r["pop_density"], r["Margin_Pct"], r["Winner_Party"][:25]), axis=1),
    hoverinfo="text", name="Women winners", showlegend=False,
), row=1, col=2)

# Panel 3: Category stacked - area on y, category on x, women highlighted
cat_colors = {"GEN": "#636EE6", "SC": "#3ABEFF", "ST": "#2ECC71"}
for cat, color in cat_colors.items():
    sub = gdf[gdf["pc_category"] == cat]
    w_sub = sub[sub["Woman_Won_2024"]]
    m_sub = sub[~sub["Woman_Won_2024"]]
    fig.add_trace(go.Scatter(
        x=[cat] * len(m_sub), y=m_sub["log_area"], mode="markers",
        marker=dict(color=color, size=5, opacity=0.3),
        text=m_sub.apply(lambda r: "%s (%s)<br>%s km2" % (r["PC Name"], r["State"], f"{r['area_sqkm']:,.0f}"), axis=1),
        hoverinfo="text", name=cat + " (men)", showlegend=False,
    ), row=1, col=3)
    fig.add_trace(go.Scatter(
        x=[cat] * len(w_sub), y=w_sub["log_area"], mode="markers",
        marker=dict(color="#FF2D78", size=10, symbol="diamond",
                    line=dict(width=1, color="#FFF"), opacity=0.9),
        text=w_sub.apply(lambda r: "%s (%s)<br>%s km2<br>WOMAN WINNER" % (r["PC Name"], r["State"], f"{r['area_sqkm']:,.0f}"), axis=1),
        hoverinfo="text", name=cat + " (women)", showlegend=False,
    ), row=1, col=3)

# Annotations with test results
from scipy import stats
w_areas = gdf[gdf["Woman_Won_2024"]]["area_sqkm"].values
m_areas = gdf[~gdf["Woman_Won_2024"]]["area_sqkm"].values
u_stat, u_p = stats.mannwhitneyu(w_areas, m_areas, alternative="two-sided")

fig.update_yaxes(title_text="log10(Area km2)", gridcolor="#222", row=1, col=1)
fig.update_yaxes(title_text="Victory Margin (%)", gridcolor="#222", row=1, col=2)
fig.update_xaxes(title_text="log10(Voter Density)", gridcolor="#222", row=1, col=2)
fig.update_yaxes(title_text="log10(Area km2)", gridcolor="#222", row=1, col=3)

fig.update_layout(
    title="TA Hypothesis: Are Women Winning in Larger or Denser Constituencies?<br>"
          "<sub>Women median area: 3,324 km2 vs Men: 4,073 km2. Mann-Whitney U p=%.3f. "
          "Women win in slightly smaller, denser seats. Pink diamonds = women winners. | Source: ECI, DataMeet</sub>" % u_p,
    plot_bgcolor="#0D1117", paper_bgcolor="#0D1117",
    font=dict(family="Source Sans 3, sans-serif", color="#E0E0E0"),
    width=1500, height=550, margin=dict(t=100),
    showlegend=False,
)
fig.write_html(os.path.join(VIZ_DIR, "46_women_area_hypothesis.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# 47: 3D EXTRUDED INDIA MAP (bars rising from constituencies)
# ============================================================
print("Plot 47: 3D Extruded India Map...")

# Prepare compact data for Three.js
ext_data = []
for _, r in gdf.iterrows():
    ext_data.append({
        "n": r["PC Name"], "s": r["State"],
        "la": round(r["Lat"], 3), "lo": round(r["Lon"], 3),
        "t": round(r["Turnout"], 1),
        "e": round(r["Electorate_Ratio"], 2),
        "a": r["Alliance"],
        "m": round(r["Margin_Pct"], 1),
        "w": 1 if r["Woman_Won_2024"] else 0,
        "ar": round(r["area_sqkm"], 0),
    })
ext_json = json.dumps(ext_data, separators=(",", ":"))

html_3d_map = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>3D Extruded India Map</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#06080F;overflow:hidden;font-family:'Segoe UI',sans-serif}
#info{position:fixed;top:16px;left:50%%;transform:translateX(-50%%);color:#F0F3F8;text-align:center;z-index:10;pointer-events:none;width:90%%}
#info h1{font-size:1.3rem;font-weight:700;margin-bottom:4px}
#info p{font-size:.78rem;color:#A0AEC0}
#tooltip{position:fixed;display:none;background:rgba(13,17,23,.95);border:1px solid #30363d;border-radius:8px;padding:10px 14px;color:#F0F3F8;font-size:.78rem;line-height:1.5;pointer-events:none;z-index:100;max-width:280px}
#metric{position:fixed;top:72px;left:50%%;transform:translateX(-50%%);z-index:10;display:flex;gap:6px}
#metric button{background:#161B26;border:1px solid #30363d;color:#A0AEC0;padding:5px 12px;border-radius:6px;cursor:pointer;font-size:.78rem;transition:all .2s}
#metric button.active{background:#00D5E0;color:#06080F;border-color:#00D5E0}
#legend{position:fixed;bottom:16px;left:50%%;transform:translateX(-50%%);display:flex;gap:14px;z-index:10}
.leg{display:flex;align-items:center;gap:5px;color:#A0AEC0;font-size:.72rem}
.leg span{width:10px;height:10px;border-radius:50%%;display:inline-block}
</style>
</head><body>
<div id="info"><h1>3D Extruded India: Spatial Histogram</h1>
<p>Bar height = selected metric. Color = alliance. Superimposed 3D histogram over the geographic footprint of India. Drag to orbit, scroll to zoom.</p></div>
<div id="metric">
<button class="active" onclick="setM('e')">Electorate Ratio</button>
<button onclick="setM('t')">Turnout</button>
<button onclick="setM('m')">Victory Margin</button>
</div>
<div id="tooltip"></div>
<div id="legend">
<div class="leg"><span style="background:#FF9933"></span>NDA</div>
<div class="leg"><span style="background:#19AAED"></span>INDIA</div>
<div class="leg"><span style="background:#888"></span>Others</div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const DATA=%s;
const AC={"NDA":0xFF9933,"INDIA":0x19AAED,"Others":0x888888};
let scene,camera,renderer,group,bars=[],raycaster,mouse,tooltip,curMetric='e';
const LAT_C=22,LON_C=82,SCALE=0.25;

function latLon2XZ(la,lo){return[(lo-LON_C)*SCALE,-(la-LAT_C)*SCALE]}

function barH(d,m){
  if(m==='e') return d.e*1.5;
  if(m==='t') return d.t/100*2;
  if(m==='m') return Math.min(d.m/50,2)*1.5;
  return 1;
}

function init(){
  scene=new THREE.Scene();
  scene.fog=new THREE.FogExp2(0x06080F,0.04);
  camera=new THREE.PerspectiveCamera(45,window.innerWidth/window.innerHeight,0.1,200);
  camera.position.set(0,8,8);camera.lookAt(0,0,0);
  renderer=new THREE.WebGLRenderer({antialias:true});
  renderer.setSize(window.innerWidth,window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  document.body.appendChild(renderer.domElement);

  scene.add(new THREE.AmbientLight(0x334455,0.6));
  var dl=new THREE.DirectionalLight(0xffffff,0.7);dl.position.set(5,10,5);scene.add(dl);
  var pl=new THREE.PointLight(0x00D5E0,0.3,30);pl.position.set(-3,5,3);scene.add(pl);

  group=new THREE.Group();

  // Ground plane (India footprint approximation)
  var gnd=new THREE.PlaneGeometry(10,8);
  var gmat=new THREE.MeshPhongMaterial({color:0x0A0F1A,transparent:true,opacity:0.5});
  var gmesh=new THREE.Mesh(gnd,gmat);gmesh.rotation.x=-Math.PI/2;gmesh.position.y=-0.01;
  group.add(gmesh);

  // Bars
  DATA.forEach(function(d,i){
    var xz=latLon2XZ(d.la,d.lo);
    var h=barH(d,curMetric);
    var geo=new THREE.BoxGeometry(0.06,h,0.06);
    var c=AC[d.a]||0x888888;
    var mat=new THREE.MeshPhongMaterial({color:c,emissive:c,emissiveIntensity:0.15,transparent:true,opacity:0.85});
    var bar=new THREE.Mesh(geo,mat);
    bar.position.set(xz[0],h/2,xz[1]);
    bar.userData={d:d,idx:i,xz:xz};
    group.add(bar);
    bars.push(bar);
  });

  scene.add(group);
  raycaster=new THREE.Raycaster();
  mouse=new THREE.Vector2(-999,-999);
  tooltip=document.getElementById('tooltip');

  var isDrag=false,prevX=0,prevY=0;
  document.addEventListener('mousedown',function(e){isDrag=true;prevX=e.clientX;prevY=e.clientY});
  document.addEventListener('mouseup',function(){isDrag=false});
  document.addEventListener('mousemove',function(e){
    mouse.x=(e.clientX/window.innerWidth)*2-1;
    mouse.y=-(e.clientY/window.innerHeight)*2+1;
    tooltip.style.left=e.clientX+15+'px';tooltip.style.top=e.clientY+15+'px';
    if(isDrag){
      group.rotation.y+=(e.clientX-prevX)*0.005;
      camera.position.y+=((e.clientY-prevY)*0.03);
      camera.position.y=Math.max(2,Math.min(20,camera.position.y));
      prevX=e.clientX;prevY=e.clientY;
    }
  });
  document.addEventListener('wheel',function(e){
    var d=camera.position.length();
    var s=Math.max(5,Math.min(25,d+e.deltaY*0.01));
    camera.position.normalize().multiplyScalar(s);
  });

  function animate(){
    requestAnimationFrame(animate);
    camera.lookAt(0,1,0);
    raycaster.setFromCamera(mouse,camera);
    var hits=raycaster.intersectObjects(bars);
    if(hits.length>0){
      var dd=hits[0].object.userData.d;
      tooltip.style.display='block';
      tooltip.innerHTML='<b>'+dd.n+'</b> ('+dd.s+')<br>Alliance: '+dd.a+'<br>Electorate Ratio: '+dd.e+'x<br>Turnout: '+dd.t+'%%<br>Margin: '+dd.m+'%%<br>Area: '+dd.ar.toLocaleString()+' km2'+(dd.w?'<br><span style="color:#FF2D78">Woman winner</span>':'');
    } else {tooltip.style.display='none'}
    renderer.render(scene,camera);
  }
  animate();
}

function setM(m){
  curMetric=m;
  document.querySelectorAll('#metric button').forEach(function(b){b.classList.remove('active')});
  event.target.classList.add('active');
  bars.forEach(function(bar){
    var d=bar.userData.d;
    var h=barH(d,m);
    bar.geometry.dispose();
    bar.geometry=new THREE.BoxGeometry(0.06,h,0.06);
    bar.position.y=h/2;
  });
}

window.addEventListener('resize',function(){
  camera.aspect=window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth,window.innerHeight);
});
init();
</script></body></html>''' % ext_json

with open(os.path.join(VIZ_DIR, "47_3d_extruded_india.html"), "w") as f:
    f.write(html_3d_map)
print("  Saved")

# ============================================================
# 48: STATE-LEVEL NDA SHARE LISA + BIVARIATE
# ============================================================
print("Plot 48: State-level NDA share LISA...")

# Compute state-level aggregates
state_data = gdf.groupby("State").agg(
    nda_seats=("Alliance", lambda x: (x == "NDA").sum()),
    india_seats=("Alliance", lambda x: (x == "INDIA").sum()),
    total_seats=("PC Name", "count"),
    women_seats=("Woman_Won_2024", "sum"),
    avg_turnout=("Turnout", "mean"),
    avg_margin=("Margin_Pct", "mean"),
    avg_area=("area_sqkm", "mean"),
    avg_lat=("Lat", "mean"),
    avg_lon=("Lon", "mean"),
).reset_index()
state_data["nda_pct"] = state_data["nda_seats"] / state_data["total_seats"] * 100
state_data["women_pct"] = state_data["women_seats"] / state_data["total_seats"] * 100

# For per-constituency LISA of NDA share, we compute per-constituency NDA=1/INDIA=-1
gdf["nda_val"] = gdf["Alliance"].map({"NDA": 1, "INDIA": -1, "Others": 0}).astype(float)

w = KNN.from_dataframe(gdf, k=8)
w.transform = "r"

# LISA on NDA vote (per constituency)
lisa_nda = Moran_Local(gdf["nda_val"].values, w, seed=42)
mi_nda = Moran(gdf["nda_val"].values, w)
print(f"  NDA spatial autocorrelation: I={mi_nda.I:.3f} p={mi_nda.p_sim:.3f}")

mean_nda = gdf["nda_val"].mean()
gdf["LISA_NDA"] = "Not Significant"
for i in range(len(gdf)):
    if lisa_nda.p_sim[i] <= 0.05:
        hi = gdf["nda_val"].iloc[i] > mean_nda
        pos = lisa_nda.Is[i] > 0
        if hi and pos: gdf.loc[gdf.index[i], "LISA_NDA"] = "NDA Stronghold"
        elif not hi and pos: gdf.loc[gdf.index[i], "LISA_NDA"] = "INDIA Stronghold"
        elif hi and not pos: gdf.loc[gdf.index[i], "LISA_NDA"] = "NDA Outlier"
        else: gdf.loc[gdf.index[i], "LISA_NDA"] = "INDIA Outlier"

print(f"  LISA NDA: {gdf['LISA_NDA'].value_counts().to_dict()}")

# Build the visualization
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=[
        "Alliance LISA: NDA vs INDIA Spatial Clustering (I=%.3f)" % mi_nda.I,
        "State-level: NDA Share vs Women Representation",
    ],
    specs=[[{"type": "scattergeo"}, {"type": "xy"}]],
    horizontal_spacing=0.06,
)

# Panel 1: LISA map
LC = {
    "NDA Stronghold": "#FF6600",
    "INDIA Stronghold": "#0088DD",
    "NDA Outlier": "#FFB366",
    "INDIA Outlier": "#66BBEE",
    "Not Significant": "#1E2233",
}
geo_cfg = dict(
    scope="asia", projection_type="natural earth",
    showland=True, landcolor="#12151F", showocean=True, oceancolor="#0A0D14",
    showcountries=True, countrycolor="#333", showframe=False,
    lonaxis=dict(range=[67, 98]), lataxis=dict(range=[6, 37]), bgcolor="#0D1117",
)
for label, color in LC.items():
    sub = gdf[gdf["LISA_NDA"] == label]
    if len(sub) == 0: continue
    sz = 4 if "Not" in label else 10
    fig.add_trace(go.Scattergeo(
        lat=sub["Lat"], lon=sub["Lon"],
        text=sub.apply(lambda r: "<b>%s</b> (%s)<br>Alliance: %s<br>Cluster: %s<br>Margin: %.1f%%" % (
            r["PC Name"], r["State"], r["Alliance"], r["LISA_NDA"], r["Margin_Pct"]), axis=1),
        hoverinfo="text", mode="markers",
        marker=dict(size=sz, color=color,
                    opacity=0.9 if "Not" not in label else 0.15,
                    line=dict(width=0.8 if "Not" not in label else 0, color="#FFF")),
        name=label, legendgroup=label,
    ), row=1, col=1)

fig.update_geos(**geo_cfg, row=1, col=1)

# Panel 2: State bubble chart - NDA % vs Women %
sd = state_data[state_data["total_seats"] >= 2].copy()
fig.add_trace(go.Scatter(
    x=sd["nda_pct"], y=sd["women_pct"],
    mode="markers+text",
    marker=dict(
        size=sd["total_seats"] * 1.2,
        color=sd["nda_pct"],
        colorscale=[[0, "#19AAED"], [0.5, "#888"], [1, "#FF9933"]],
        cmin=0, cmax=100,
        line=dict(width=1, color="#444"),
        opacity=0.8,
    ),
    text=sd.apply(lambda r: r["State"][:12] if r["total_seats"] >= 8 else "", axis=1),
    textposition="top center",
    textfont=dict(size=8, color="#A0AEC0"),
    hovertext=sd.apply(lambda r: "<b>%s</b><br>Seats: %d<br>NDA: %d (%.0f%%)<br>INDIA: %d<br>Women: %d (%.0f%%)" % (
        r["State"], r["total_seats"], r["nda_seats"], r["nda_pct"],
        r["india_seats"], r["women_seats"], r["women_pct"]), axis=1),
    hoverinfo="text", showlegend=False,
), row=1, col=2)

# 33% target line (manual shape since mixed subplots don't support add_hline)
fig.add_shape(type="line", x0=-5, x1=105, y0=33, y1=33,
    line=dict(color="#FFD700", width=1, dash="dash"),
    xref="x2", yref="y2")
fig.add_annotation(x=100, y=35, text="33% target", font=dict(color="#FFD700", size=10),
    showarrow=False, xref="x2", yref="y2")

fig.update_xaxes(title_text="NDA Seat Share (%)", gridcolor="#222", range=[-5, 105], row=1, col=2)
fig.update_yaxes(title_text="Women Winners (%)", gridcolor="#222", row=1, col=2)

fig.update_layout(
    title="Alliance Geography and Women's Representation<br>"
          "<sub>Left: LISA clusters show NDA strongholds (orange) and INDIA strongholds (blue). "
          "Right: State bubble chart, size=total seats, color=NDA share. | Source: ECI, PySAL</sub>",
    paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
    font=dict(family="Source Sans 3, sans-serif", color="#E0E0E0"),
    legend=dict(bgcolor="rgba(0,0,0,0.5)", font=dict(size=10),
                orientation="h", y=-0.08, x=0.3, xanchor="center"),
    width=1500, height=700, margin=dict(t=100, b=60),
)
fig.write_html(os.path.join(VIZ_DIR, "48_alliance_lisa_women.html"), include_plotlyjs="cdn")
print("  Saved")

print(f"\nPhase 7 complete: 3 new charts")
for f in ["46_women_area_hypothesis.html", "47_3d_extruded_india.html", "48_alliance_lisa_women.html"]:
    fp = os.path.join(VIZ_DIR, f)
    if os.path.exists(fp):
        print(f"  {f:55s} {os.path.getsize(fp)/1024:.1f} KB")
