#!/usr/bin/env python3
"""
Phase 6: India Lok Sabha 2024 - Spatial Autocorrelation Analysis
Uses PySAL/esda for Moran's I and LISA.
Sources: ECI via OpenCity.in, DataMeet shapefiles
"""
import os, json
import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from libpysal.weights import KNN
from esda.moran import Moran, Moran_Local

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW = os.path.join(SCRIPT_DIR, "data", "raw")
VIZ_DIR = os.path.join(SCRIPT_DIR, "visualizations")

print("="*60)
print("Phase 6: Spatial Autocorrelation Analysis")
print("="*60)

gdf = gpd.read_file(os.path.join(DATA_RAW, "india_election_with_area.geojson"))
gdf["Lat"] = gdf.geometry.centroid.y
gdf["Lon"] = gdf.geometry.centroid.x
print(f"  {len(gdf)} constituencies with geometry and area")

# Spatial weights
w = KNN.from_dataframe(gdf, k=8)
w.transform = "r"

turnout_vals = gdf["Turnout"].fillna(gdf["Turnout"].median()).values
margin_vals = gdf["Margin_Pct"].fillna(gdf["Margin_Pct"].median()).values
area_vals = gdf["area_sqkm"].values

mi_turn = Moran(turnout_vals, w)
mi_marg = Moran(margin_vals, w)
mi_area = Moran(area_vals, w)
print(f"  Turnout I={mi_turn.I:.4f} p={mi_turn.p_sim:.4f}")
print(f"  Margin  I={mi_marg.I:.4f} p={mi_marg.p_sim:.4f}")
print(f"  Area    I={mi_area.I:.4f} p={mi_area.p_sim:.4f}")

lisa_turn = Moran_Local(turnout_vals, w, seed=42)
lisa_marg = Moran_Local(margin_vals, w, seed=42)

def classify_lisa(lisa, vals, sig=0.05):
    m = np.mean(vals)
    out = []
    for i in range(len(vals)):
        if lisa.p_sim[i] > sig:
            out.append("Not Significant")
        else:
            hi = vals[i] > m
            pos = lisa.Is[i] > 0
            if hi and pos: out.append("High-High (Hot Spot)")
            elif not hi and pos: out.append("Low-Low (Cold Spot)")
            elif hi and not pos: out.append("High-Low (Outlier)")
            else: out.append("Low-High (Outlier)")
    return out

gdf["LISA_Turn"] = classify_lisa(lisa_turn, turnout_vals)
gdf["LISA_Marg"] = classify_lisa(lisa_marg, margin_vals)
gdf["LISA_Turn_I"] = lisa_turn.Is
gdf["LISA_Turn_p"] = lisa_turn.p_sim
gdf["LISA_Marg_I"] = lisa_marg.Is
gdf["LISA_Marg_p"] = lisa_marg.p_sim

# Standardized values and spatial lags for Moran scatter
for var, vals_arr, prefix in [("Turnout", turnout_vals, "Turn"), ("Margin_Pct", margin_vals, "Marg")]:
    std = (vals_arr - np.mean(vals_arr)) / np.std(vals_arr)
    W_full = w.full()[0]
    lag = np.dot(W_full, std)
    gdf[f"{prefix}_std"] = std
    gdf[f"{prefix}_lag"] = lag

print(f"  LISA Turnout: {pd.Series(gdf['LISA_Turn']).value_counts().to_dict()}")

# ============================================================
# 37: LISA CLUSTER MAP
# ============================================================
print("\nPlot 37: LISA Cluster Map...")
LC = {
    "High-High (Hot Spot)":"#D7191C","Low-Low (Cold Spot)":"#2C7BB6",
    "High-Low (Outlier)":"#FD8D3C","Low-High (Outlier)":"#ABD9E9",
    "Not Significant":"#1E2233",
}
geo_cfg = dict(
    scope="asia",projection_type="natural earth",
    showland=True,landcolor="#12151F",showocean=True,oceancolor="#0A0D14",
    showcountries=True,countrycolor="#333",showframe=False,
    lonaxis=dict(range=[67,98]),lataxis=dict(range=[6,37]),bgcolor="#0D1117",
)

fig = make_subplots(rows=1,cols=2,
    subplot_titles=[
        f"Turnout Clusters (Moran's I={mi_turn.I:.3f}, p={mi_turn.p_sim:.3f})",
        f"Margin Clusters (Moran's I={mi_marg.I:.3f}, p={mi_marg.p_sim:.3f})",
    ],
    specs=[[{"type":"scattergeo"},{"type":"scattergeo"}]],
    horizontal_spacing=0.02)

for lisa_col, col_idx in [("LISA_Turn",1),("LISA_Marg",2)]:
    i_col = f"{lisa_col}_I"
    p_col = f"{lisa_col}_p"
    for label, color in LC.items():
        sub = gdf[gdf[lisa_col]==label]
        if len(sub)==0: continue
        sz = 4 if "Not" in label else 10
        fig.add_trace(go.Scattergeo(
            lat=sub["Lat"],lon=sub["Lon"],
            text=sub.apply(lambda r: (
                f"<b>{r['PC Name']}</b> ({r['State']})<br>"
                f"Cluster: {r[lisa_col]}<br>"
                f"Turnout: {r['Turnout']:.1f}% | Margin: {r['Margin_Pct']:.1f}%<br>"
                f"Area: {r['area_sqkm']:,.0f} km2<br>"
                f"Local I: {r[i_col]:.3f}, p={r[p_col]:.3f}"
            ),axis=1),
            hoverinfo="text",mode="markers",
            marker=dict(size=sz,color=color,
                opacity=0.9 if "Not" not in label else 0.2,
                line=dict(width=0.8 if "Not" not in label else 0,color="#FFF")),
            name=label,legendgroup=label,showlegend=(col_idx==1),
        ),row=1,col=col_idx)

fig.update_geos(**geo_cfg,row=1,col=1)
fig.update_geos(**geo_cfg,row=1,col=2)
fig.update_layout(
    title="LISA Cluster Map: Where Do Electoral Patterns Cluster Spatially?<br>"
          "<sub>Red Hot Spots = high values near high values. Blue Cold Spots = low near low. Orange/Cyan = spatial outliers. KNN k=8. | Source: ECI</sub>",
    paper_bgcolor="#0D1117",font=dict(family="Source Sans 3, sans-serif",color="#E0E0E0"),
    legend=dict(bgcolor="rgba(0,0,0,0.5)",font=dict(size=11),orientation="h",y=-0.05,x=0.5,xanchor="center"),
    width=1400,height=700,margin=dict(t=100,b=60))
fig.write_html(os.path.join(VIZ_DIR,"37_india_lisa_clusters.html"),include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# 38: AREA vs ELECTORAL OUTCOMES
# ============================================================
print("Plot 38: Area vs Electoral Outcomes...")
AC = {"NDA":"#FF9933","INDIA":"#19AAED","Others":"#888"}

fig = make_subplots(rows=1,cols=2,
    subplot_titles=["Constituency Area vs Turnout","Constituency Area vs Victory Margin"],
    horizontal_spacing=0.08)

for alliance,color in AC.items():
    sub = gdf[gdf["Alliance"]==alliance]
    for col_idx, y_var, y_label in [(1,"Turnout","Turnout (%)"),(2,"Margin_Pct","Victory Margin (%)")]:
        fig.add_trace(go.Scatter(
            x=np.log10(sub["area_sqkm"].clip(lower=10)),
            y=sub[y_var],mode="markers",
            marker=dict(color=color,size=7,opacity=0.7,line=dict(width=0.5,color="#333")),
            text=sub.apply(lambda r: (
                f"<b>{r['PC Name']}</b> ({r['State']})<br>"
                f"Area: {r['area_sqkm']:,.0f} km2<br>"
                f"Turnout: {r['Turnout']:.1f}% | Margin: {r['Margin_Pct']:.1f}%<br>"
                f"Alliance: {r['Alliance']} | {r['Winner_Party'][:25]}"
            ),axis=1),
            hoverinfo="text",
            name=alliance,legendgroup=alliance,showlegend=(col_idx==1),
        ),row=1,col=col_idx)

# Trend line for turnout
from numpy.polynomial import polynomial as P
xlog = np.log10(gdf["area_sqkm"].clip(lower=10).values)
yt = gdf["Turnout"].values
mask = np.isfinite(xlog) & np.isfinite(yt)
c = P.polyfit(xlog[mask],yt[mask],1)
xf = np.linspace(xlog[mask].min(),xlog[mask].max(),50)
fig.add_trace(go.Scatter(x=xf,y=P.polyval(xf,c),mode="lines",
    line=dict(color="#FFD700",width=2,dash="dash"),showlegend=False),row=1,col=1)

fig.update_xaxes(title_text="log10(Area km2)",gridcolor="#222",row=1,col=1)
fig.update_xaxes(title_text="log10(Area km2)",gridcolor="#222",row=1,col=2)
fig.update_yaxes(title_text="Turnout (%)",gridcolor="#222",row=1,col=1)
fig.update_yaxes(title_text="Victory Margin (%)",gridcolor="#222",row=1,col=2)
fig.update_layout(
    title="Does Size Matter? Constituency Area vs Electoral Outcomes<br>"
          f"<sub>Area Moran's I={mi_area.I:.3f} (p={mi_area.p_sim:.3f}): constituency sizes are spatially clustered. Larger seats show lower turnout. | Source: ECI, DataMeet</sub>",
    plot_bgcolor="#0D1117",paper_bgcolor="#0D1117",
    font=dict(family="Source Sans 3, sans-serif",color="#E0E0E0"),
    legend=dict(bgcolor="rgba(0,0,0,0.5)",orientation="h",y=1.08,x=0.5,xanchor="center"),
    width=1300,height=600,margin=dict(t=100))
fig.write_html(os.path.join(VIZ_DIR,"38_india_area_outcomes.html"),include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# 39: MORAN'S I SCATTERPLOT
# ============================================================
print("Plot 39: Moran's I Scatterplot...")

QC = {"HH":"#D7191C","LL":"#2C7BB6","HL":"#FD8D3C","LH":"#ABD9E9"}
QL = {"HH":"HH (Hot Spot)","LL":"LL (Cold Spot)","HL":"HL (Outlier)","LH":"LH (Outlier)"}

def quad(x,y):
    if x>0 and y>0: return "HH"
    elif x<0 and y<0: return "LL"
    elif x>0 and y<0: return "HL"
    else: return "LH"

gdf["MQ_T"] = [quad(x,y) for x,y in zip(gdf["Turn_std"],gdf["Turn_lag"])]
gdf["MQ_M"] = [quad(x,y) for x,y in zip(gdf["Marg_std"],gdf["Marg_lag"])]

fig = make_subplots(rows=1,cols=2,
    subplot_titles=[
        f"Turnout (I={mi_turn.I:.3f})",
        f"Victory Margin (I={mi_marg.I:.3f})",
    ],horizontal_spacing=0.08)

for q,color in QC.items():
    for col_idx,std_col,lag_col,mq_col,var_name in [
        (1,"Turn_std","Turn_lag","MQ_T","Turnout"),
        (2,"Marg_std","Marg_lag","MQ_M","Margin_Pct")]:
        sub = gdf[gdf[mq_col]==q]
        fig.add_trace(go.Scatter(
            x=sub[std_col],y=sub[lag_col],mode="markers",
            marker=dict(color=color,size=6,opacity=0.7),
            text=sub.apply(lambda r: (
                f"<b>{r['PC Name']}</b> ({r['State']})<br>"
                f"Turnout: {r['Turnout']:.1f}% | Margin: {r['Margin_Pct']:.1f}%<br>"
                f"Quadrant: {QL[r[mq_col]]}"
            ),axis=1),
            hoverinfo="text",
            name=QL[q],legendgroup=q,showlegend=(col_idx==1),
        ),row=1,col=col_idx)

xr = np.linspace(-3.5,3.5,50)
fig.add_trace(go.Scatter(x=xr,y=mi_turn.I*xr,mode="lines",
    line=dict(color="#FFD700",width=2,dash="dash"),showlegend=False,
    hoverinfo="skip"),row=1,col=1)
fig.add_trace(go.Scatter(x=xr,y=mi_marg.I*xr,mode="lines",
    line=dict(color="#FFD700",width=2,dash="dash"),showlegend=False,
    hoverinfo="skip"),row=1,col=2)

for c in [1,2]:
    fig.add_hline(y=0,line_color="#444",line_width=0.5,row=1,col=c)
    fig.add_vline(x=0,line_color="#444",line_width=0.5,row=1,col=c)

fig.update_xaxes(title_text="Standardized Value",gridcolor="#222",row=1,col=1)
fig.update_xaxes(title_text="Standardized Value",gridcolor="#222",row=1,col=2)
fig.update_yaxes(title_text="Spatial Lag (neighbors' mean)",gridcolor="#222",row=1,col=1)
fig.update_yaxes(title_text="Spatial Lag (neighbors' mean)",gridcolor="#222",row=1,col=2)

fig.update_layout(
    title="Moran's I Scatterplot: Spatial Clustering in Indian Elections<br>"
          "<sub>Slope = Moran's I. HH/LL quadrants = spatial clustering. HL/LH = outliers. Gold line = regression (spatial autocorrelation). KNN k=8. | Source: ECI</sub>",
    plot_bgcolor="#0D1117",paper_bgcolor="#0D1117",
    font=dict(family="Source Sans 3, sans-serif",color="#E0E0E0"),
    legend=dict(bgcolor="rgba(0,0,0,0.5)",orientation="h",y=-0.08,x=0.5,xanchor="center"),
    width=1300,height=600,margin=dict(t=100,b=60))
fig.write_html(os.path.join(VIZ_DIR,"39_india_moran_scatterplot.html"),include_plotlyjs="cdn")
print("  Saved")

print(f"\nPhase 6 complete: 3 new spatial autocorrelation charts")
