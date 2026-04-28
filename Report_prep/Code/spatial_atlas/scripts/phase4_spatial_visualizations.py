"""
Phase 4: Spatial Visualizations
================================
Creates geospatial choropleth maps and point maps across 6 themes:
  1. Corals - reef bleaching hotspots, SST anomalies
  2. People - urbanization, population density, slum populations
  3. Poverty - headcount ratios, Gini inequality
  4. Usage of Items - internet, mobile, electricity access
  5. Money - GDP, trade openness, remittances
  6. Environment - forest cover, renewables, CO2, freshwater stress

Data Sources:
  World Bank Open Data: https://data.worldbank.org/
  NOAA Coral Reef Watch: https://coralreefwatch.noaa.gov/
  NOAA ERSST v5: https://www.ncei.noaa.gov/products/extended-reconstructed-sst
  Gapminder: https://www.gapminder.org/data/
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os, json

DATA_RAW = "/home/claude/rosling_project/data/raw"
DATA_PROC = "/home/claude/rosling_project/data/processed"
VIZ_DIR = "/home/claude/rosling_project/visualizations"
os.makedirs(VIZ_DIR, exist_ok=True)

# ============================================================
# UTILITY: Extract latest value per country from WB CSV
# ============================================================
def load_wb_latest(filename, value_name, year_min=2015):
    """Load a WB CSV, reshape to long, return latest value per country."""
    fpath = os.path.join(DATA_RAW, filename)
    if not os.path.exists(fpath):
        print(f"  WARNING: {filename} not found")
        return pd.DataFrame()
    df = pd.read_csv(fpath)
    id_cols = [c for c in df.columns if not c.startswith("YR")]
    yr_cols = [c for c in df.columns if c.startswith("YR")]
    df_long = df.melt(id_vars=id_cols, value_vars=yr_cols,
                      var_name="yr_raw", value_name=value_name)
    df_long["year"] = df_long["yr_raw"].str.replace("YR","").astype(int)
    # Rename
    rename = {}
    for c in id_cols:
        if c.lower() in ("economy","id","countrycode"): rename[c] = "country_code"
        elif c.lower() in ("name","countryname","country"): rename[c] = "country_name"
    df_long = df_long.rename(columns=rename)
    df_long = df_long.dropna(subset=[value_name])
    df_long = df_long[df_long["year"] >= year_min]
    # Get latest per country
    idx = df_long.groupby("country_code")["year"].idxmax()
    latest = df_long.loc[idx, ["country_code","country_name","year",value_name]].copy()
    latest = latest.rename(columns={"year": f"{value_name}_year"})
    return latest

# Load country metadata for filtering aggregates
meta = pd.read_csv(os.path.join(DATA_RAW, "wb_country_metadata.csv"))
country_codes = set(meta[meta["aggregate"]==False]["id"].tolist())

# Common layout template
LAYOUT_TEMPLATE = dict(
    font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif", size=12),
    paper_bgcolor="#FFFFFF",
    margin=dict(t=80, b=20, l=20, r=20),
    width=1200,
    height=650,
)

GEO_TEMPLATE = dict(
    showframe=False,
    showcoastlines=True,
    coastlinecolor="#888888",
    projection_type="natural earth",
    landcolor="#F0F0F0",
    showland=True,
    showcountries=True,
    countrycolor="#CCCCCC",
    showocean=True,
    oceancolor="#E8F4FD",
)

# ============================================================
# 1. CORALS: Global Reef Bleaching Map
# ============================================================
print("=" * 60)
print("SPATIAL VIZ 1: Coral Reef Bleaching Hotspots")
print("=" * 60)

coral = pd.read_csv(os.path.join(DATA_RAW, "coral_reef_sites.csv"))
sst = pd.read_csv(os.path.join(DATA_RAW, "global_sst_anomaly.csv"))

threat_colors = {"Critical": "#FF0000", "High": "#FF8C00", "Medium": "#FFD700", "Low": "#32CD32"}
coral["color"] = coral["threat_level"].map(threat_colors)
coral["size_display"] = np.sqrt(coral["area_km2"]) * 0.3

fig_coral = go.Figure()

for threat in ["Critical", "High", "Medium", "Low"]:
    subset = coral[coral["threat_level"] == threat]
    fig_coral.add_trace(go.Scattergeo(
        lat=subset["lat"],
        lon=subset["lon"],
        text=subset.apply(
            lambda r: f"<b>{r['name']}</b><br>"
                      f"Region: {r['region']}<br>"
                      f"Area: {r['area_km2']:,} km2<br>"
                      f"Bleaching events since 1998: {r['bleaching_events_since_1998']}<br>"
                      f"Health: {r['reef_health']}<br>"
                      f"Threat: {r['threat_level']}",
            axis=1
        ),
        hoverinfo="text",
        mode="markers",
        marker=dict(
            size=subset["size_display"],
            color=threat_colors[threat],
            opacity=0.8,
            line=dict(width=1, color="#333"),
            sizemin=6,
        ),
        name=f"{threat} threat",
    ))

fig_coral.update_layout(
    title="Global Coral Reef Bleaching Hotspots<br>"
          "<sub>Bubble size = reef area | Color = threat level | "
          "Sources: NOAA CRW, ICRI, Reef Check</sub>",
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="#555555",
        projection_type="natural earth",
        landcolor="#2A2A2A",
        showland=True,
        showcountries=True,
        countrycolor="#444444",
        showocean=True,
        oceancolor="#1A3A5C",
        bgcolor="#1A1A2E",
        showlakes=True,
        lakecolor="#1A3A5C",
    ),
    paper_bgcolor="#1A1A2E",
    font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif", color="white"),
    legend=dict(
        title="Threat Level",
        bgcolor="rgba(0,0,0,0.5)",
        font=dict(color="white"),
    ),
    width=1200, height=650,
    margin=dict(t=80, b=20, l=20, r=20),
)

fig_coral.write_html(os.path.join(VIZ_DIR, "07_coral_bleaching_map.html"), include_plotlyjs="cdn")
print("  Saved: 07_coral_bleaching_map.html")

# SST Anomaly timeline (context for coral bleaching)
fig_sst = go.Figure()
fig_sst.add_trace(go.Scatter(
    x=sst["year"], y=sst["sst_anomaly_c"],
    mode="lines+markers",
    fill="tozeroy",
    fillcolor="rgba(255,69,0,0.2)",
    line=dict(color="#FF4500", width=2.5),
    marker=dict(size=4),
    hovertemplate="Year: %{x}<br>SST Anomaly: %{y:.2f} C<extra></extra>",
))

# Annotate major bleaching events
events = [
    (1998, 0.34, "1998 El Nino\nFirst global bleaching"),
    (2010, 0.30, "2010\nSecond global\nbleaching"),
    (2016, 0.42, "2015-16\nThird global\nbleaching"),
    (2024, 0.74, "2024\nFourth global\nbleaching"),
]
for yr, val, label in events:
    fig_sst.add_annotation(
        x=yr, y=val + 0.06, text=label, showarrow=True,
        arrowhead=2, arrowsize=1, arrowcolor="#FF4500",
        font=dict(size=9, color="#FF4500"),
        align="center",
    )

fig_sst.update_layout(
    title="Global Ocean Surface Temperature Anomaly (1980-2024)<br>"
          "<sub>Baseline: 1901-2000 average | Source: NOAA ERSST v5</sub>",
    xaxis=dict(title="Year", gridcolor="#E0E0E0"),
    yaxis=dict(title="Temperature Anomaly (degrees C)", gridcolor="#E0E0E0",
               zeroline=True, zerolinecolor="#888", zerolinewidth=1),
    plot_bgcolor="#FAFAFA",
    **LAYOUT_TEMPLATE,
)
fig_sst.write_html(os.path.join(VIZ_DIR, "08_ocean_sst_anomaly.html"), include_plotlyjs="cdn")
print("  Saved: 08_ocean_sst_anomaly.html")

# ============================================================
# 2. PEOPLE: Urbanization Choropleth (Animated)
# ============================================================
print("\n" + "=" * 60)
print("SPATIAL VIZ 2: People - Urbanization & Slum Population")
print("=" * 60)

# Animated urbanization choropleth
urban_path = os.path.join(DATA_RAW, "wb_urban_population_pct.csv")
df_urb = pd.read_csv(urban_path)
id_cols = [c for c in df_urb.columns if not c.startswith("YR")]
yr_cols = [c for c in df_urb.columns if c.startswith("YR")]
df_urb_long = df_urb.melt(id_vars=id_cols, value_vars=yr_cols,
                           var_name="yr_raw", value_name="urban_pct")
rename = {}
for c in id_cols:
    if c.lower() in ("economy","id"): rename[c] = "country_code"
    elif c.lower() in ("name","country","countryname"): rename[c] = "country_name"
df_urb_long = df_urb_long.rename(columns=rename)
df_urb_long["year"] = df_urb_long["yr_raw"].str.replace("YR","").astype(int)
df_urb_long = df_urb_long.dropna(subset=["urban_pct"])
df_urb_long = df_urb_long[df_urb_long["country_code"].isin(country_codes)]
# Sample every 5 years for animation
df_urb_anim = df_urb_long[df_urb_long["year"].isin([1990,1995,2000,2005,2010,2015,2020,2022])]

fig_urban = px.choropleth(
    df_urb_anim,
    locations="country_code",
    color="urban_pct",
    hover_name="country_name",
    hover_data={"urban_pct": ":.1f", "year": True, "country_code": False},
    animation_frame="year",
    color_continuous_scale="YlOrRd",
    range_color=[10, 100],
    labels={"urban_pct": "Urban Population (%)"},
    title="Global Urbanization (1990-2022)<br>"
          "<sub>Urban population as % of total | Source: World Bank (SP.URB.TOTL.IN.ZS)</sub>",
)
fig_urban.update_geos(**GEO_TEMPLATE)
fig_urban.update_layout(**LAYOUT_TEMPLATE)
fig_urban.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 800
fig_urban.write_html(os.path.join(VIZ_DIR, "09_urbanization_choropleth.html"), include_plotlyjs="cdn")
print("  Saved: 09_urbanization_choropleth.html")

# Slum population map (latest)
slum = load_wb_latest("wb_slum_population_pct.csv", "slum_pct", year_min=2010)
slum = slum[slum["country_code"].isin(country_codes)]
if len(slum) > 0:
    fig_slum = px.choropleth(
        slum,
        locations="country_code",
        color="slum_pct",
        hover_name="country_name",
        hover_data={"slum_pct": ":.1f", "slum_pct_year": True, "country_code": False},
        color_continuous_scale="Reds",
        range_color=[0, 80],
        labels={"slum_pct": "Slum Population (%)", "slum_pct_year": "Data Year"},
        title="Urban Slum Population (% of urban population)<br>"
              "<sub>Latest available data (2014-2020) | Source: World Bank (EN.POP.SLUM.UR.ZS)</sub>",
    )
    fig_slum.update_geos(**GEO_TEMPLATE)
    fig_slum.update_layout(**LAYOUT_TEMPLATE)
    fig_slum.write_html(os.path.join(VIZ_DIR, "10_slum_population_map.html"), include_plotlyjs="cdn")
    print("  Saved: 10_slum_population_map.html")

# ============================================================
# 3. POVERTY: Extreme Poverty & Inequality Maps
# ============================================================
print("\n" + "=" * 60)
print("SPATIAL VIZ 3: Poverty - Extreme Poverty & Gini Inequality")
print("=" * 60)

pov = load_wb_latest("wb_poverty_headcount_190.csv", "poverty_pct", year_min=2010)
pov = pov[pov["country_code"].isin(country_codes)]
if len(pov) > 0:
    fig_pov = px.choropleth(
        pov,
        locations="country_code",
        color="poverty_pct",
        hover_name="country_name",
        hover_data={"poverty_pct": ":.1f", "poverty_pct_year": True, "country_code": False},
        color_continuous_scale="Inferno_r",
        range_color=[0, 70],
        labels={"poverty_pct": "Population below $1.90/day (%)", "poverty_pct_year": "Data Year"},
        title="Extreme Poverty: Living Below $1.90/day<br>"
              "<sub>Latest available data | Source: World Bank (SI.POV.DDAY)</sub>",
    )
    fig_pov.update_geos(**GEO_TEMPLATE)
    fig_pov.update_layout(**LAYOUT_TEMPLATE)
    fig_pov.write_html(os.path.join(VIZ_DIR, "11_extreme_poverty_map.html"), include_plotlyjs="cdn")
    print("  Saved: 11_extreme_poverty_map.html")

gini = load_wb_latest("wb_gini_index.csv", "gini", year_min=2010)
gini = gini[gini["country_code"].isin(country_codes)]
if len(gini) > 0:
    fig_gini = px.choropleth(
        gini,
        locations="country_code",
        color="gini",
        hover_name="country_name",
        hover_data={"gini": ":.1f", "gini_year": True, "country_code": False},
        color_continuous_scale="RdYlGn_r",
        range_color=[24, 65],
        labels={"gini": "Gini Index", "gini_year": "Data Year"},
        title="Income Inequality: Gini Index by Country<br>"
              "<sub>0 = perfect equality, 100 = perfect inequality | Source: World Bank (SI.POV.GINI)</sub>",
    )
    fig_gini.update_geos(**GEO_TEMPLATE)
    fig_gini.update_layout(**LAYOUT_TEMPLATE)
    fig_gini.write_html(os.path.join(VIZ_DIR, "12_gini_inequality_map.html"), include_plotlyjs="cdn")
    print("  Saved: 12_gini_inequality_map.html")

# ============================================================
# 4. USAGE OF ITEMS: Internet, Mobile, Electricity Access
# ============================================================
print("\n" + "=" * 60)
print("SPATIAL VIZ 4: Usage - Internet, Mobile, Electricity")
print("=" * 60)

# Animated internet usage choropleth
inet_path = os.path.join(DATA_RAW, "wb_internet_users_pct.csv")
df_inet = pd.read_csv(inet_path)
id_cols_i = [c for c in df_inet.columns if not c.startswith("YR")]
yr_cols_i = [c for c in df_inet.columns if c.startswith("YR")]
df_inet_long = df_inet.melt(id_vars=id_cols_i, value_vars=yr_cols_i,
                             var_name="yr_raw", value_name="internet_pct")
rename_i = {}
for c in id_cols_i:
    if c.lower() in ("economy","id"): rename_i[c] = "country_code"
    elif c.lower() in ("name","country","countryname"): rename_i[c] = "country_name"
df_inet_long = df_inet_long.rename(columns=rename_i)
df_inet_long["year"] = df_inet_long["yr_raw"].str.replace("YR","").astype(int)
df_inet_long = df_inet_long.dropna(subset=["internet_pct"])
df_inet_long = df_inet_long[df_inet_long["country_code"].isin(country_codes)]
df_inet_anim = df_inet_long[df_inet_long["year"].isin([2000,2005,2010,2015,2020,2022])]

fig_inet = px.choropleth(
    df_inet_anim,
    locations="country_code",
    color="internet_pct",
    hover_name="country_name",
    hover_data={"internet_pct": ":.1f", "year": True, "country_code": False},
    animation_frame="year",
    color_continuous_scale="Viridis",
    range_color=[0, 100],
    labels={"internet_pct": "Internet Users (% of population)"},
    title="The Digital Divide: Internet Usage (2000-2022)<br>"
          "<sub>Source: World Bank (IT.NET.USER.ZS)</sub>",
)
fig_inet.update_geos(**GEO_TEMPLATE)
fig_inet.update_layout(**LAYOUT_TEMPLATE)
fig_inet.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 800
fig_inet.write_html(os.path.join(VIZ_DIR, "13_internet_usage_choropleth.html"), include_plotlyjs="cdn")
print("  Saved: 13_internet_usage_choropleth.html")

# Electricity access
elec = load_wb_latest("wb_electricity_access_pct.csv", "elec_pct", year_min=2015)
elec = elec[elec["country_code"].isin(country_codes)]
if len(elec) > 0:
    fig_elec = px.choropleth(
        elec,
        locations="country_code",
        color="elec_pct",
        hover_name="country_name",
        hover_data={"elec_pct": ":.1f", "elec_pct_year": True, "country_code": False},
        color_continuous_scale="YlGnBu",
        range_color=[0, 100],
        labels={"elec_pct": "Electricity Access (%)", "elec_pct_year": "Data Year"},
        title="Access to Electricity (% of population)<br>"
              "<sub>Source: World Bank (EG.ELC.ACCS.ZS)</sub>",
    )
    fig_elec.update_geos(**GEO_TEMPLATE)
    fig_elec.update_layout(**LAYOUT_TEMPLATE)
    fig_elec.write_html(os.path.join(VIZ_DIR, "14_electricity_access_map.html"), include_plotlyjs="cdn")
    print("  Saved: 14_electricity_access_map.html")

# Mobile subscriptions
mobile = load_wb_latest("wb_mobile_subscriptions_per100.csv", "mobile_per100", year_min=2015)
mobile = mobile[mobile["country_code"].isin(country_codes)]
if len(mobile) > 0:
    fig_mobile = px.choropleth(
        mobile,
        locations="country_code",
        color="mobile_per100",
        hover_name="country_name",
        hover_data={"mobile_per100": ":.0f", "mobile_per100_year": True, "country_code": False},
        color_continuous_scale="Purples",
        range_color=[0, 200],
        labels={"mobile_per100": "Mobile subscriptions per 100 people", "mobile_per100_year": "Data Year"},
        title="Mobile Phone Subscriptions (per 100 people)<br>"
              "<sub>Source: World Bank (IT.CEL.SETS.P2)</sub>",
    )
    fig_mobile.update_geos(**GEO_TEMPLATE)
    fig_mobile.update_layout(**LAYOUT_TEMPLATE)
    fig_mobile.write_html(os.path.join(VIZ_DIR, "15_mobile_subscriptions_map.html"), include_plotlyjs="cdn")
    print("  Saved: 15_mobile_subscriptions_map.html")

# ============================================================
# 5. MONEY: GDP Choropleth, Trade, Remittances
# ============================================================
print("\n" + "=" * 60)
print("SPATIAL VIZ 5: Money - GDP, Trade Openness, Remittances")
print("=" * 60)

gdp = load_wb_latest("wb_gdp_per_capita_ppp.csv", "gdp_pc", year_min=2018)
gdp = gdp[gdp["country_code"].isin(country_codes)]
if len(gdp) > 0:
    gdp["gdp_pc_log"] = np.log10(gdp["gdp_pc"].clip(lower=100))
    fig_gdp = px.choropleth(
        gdp,
        locations="country_code",
        color="gdp_pc",
        hover_name="country_name",
        hover_data={"gdp_pc": ":,.0f", "gdp_pc_year": True, "country_code": False},
        color_continuous_scale="Plasma",
        range_color=[500, 80000],
        labels={"gdp_pc": "GDP per capita (PPP, 2017 $)", "gdp_pc_year": "Data Year"},
        title="Global Wealth: GDP per Capita (PPP)<br>"
              "<sub>Constant 2017 international dollars | Source: World Bank (NY.GDP.PCAP.PP.KD)</sub>",
    )
    fig_gdp.update_geos(**GEO_TEMPLATE)
    fig_gdp.update_layout(**LAYOUT_TEMPLATE)
    fig_gdp.write_html(os.path.join(VIZ_DIR, "16_gdp_per_capita_map.html"), include_plotlyjs="cdn")
    print("  Saved: 16_gdp_per_capita_map.html")

trade = load_wb_latest("wb_trade_pct_gdp.csv", "trade_pct", year_min=2015)
trade = trade[trade["country_code"].isin(country_codes)]
if len(trade) > 0:
    fig_trade = px.choropleth(
        trade,
        locations="country_code",
        color="trade_pct",
        hover_name="country_name",
        hover_data={"trade_pct": ":.1f", "trade_pct_year": True, "country_code": False},
        color_continuous_scale="Tealgrn",
        range_color=[0, 200],
        labels={"trade_pct": "Trade (% of GDP)", "trade_pct_year": "Data Year"},
        title="Trade Openness: Exports + Imports as % of GDP<br>"
              "<sub>Source: World Bank (NE.TRD.GNFS.ZS)</sub>",
    )
    fig_trade.update_geos(**GEO_TEMPLATE)
    fig_trade.update_layout(**LAYOUT_TEMPLATE)
    fig_trade.write_html(os.path.join(VIZ_DIR, "17_trade_openness_map.html"), include_plotlyjs="cdn")
    print("  Saved: 17_trade_openness_map.html")

remit = load_wb_latest("wb_remittances_pct_gdp.csv", "remit_pct", year_min=2015)
remit = remit[remit["country_code"].isin(country_codes)]
if len(remit) > 0:
    fig_remit = px.choropleth(
        remit,
        locations="country_code",
        color="remit_pct",
        hover_name="country_name",
        hover_data={"remit_pct": ":.1f", "remit_pct_year": True, "country_code": False},
        color_continuous_scale="Oranges",
        range_color=[0, 40],
        labels={"remit_pct": "Remittances (% of GDP)", "remit_pct_year": "Data Year"},
        title="Personal Remittances Received (% of GDP)<br>"
              "<sub>Source: World Bank (BX.TRF.PWKR.DT.GD.ZS)</sub>",
    )
    fig_remit.update_geos(**GEO_TEMPLATE)
    fig_remit.update_layout(**LAYOUT_TEMPLATE)
    fig_remit.write_html(os.path.join(VIZ_DIR, "18_remittances_map.html"), include_plotlyjs="cdn")
    print("  Saved: 18_remittances_map.html")

# ============================================================
# 6. ENVIRONMENT: Forest Cover, Renewables, CO2, Water Stress
# ============================================================
print("\n" + "=" * 60)
print("SPATIAL VIZ 6: Environment - Forest, CO2, Renewables, Water")
print("=" * 60)

forest = load_wb_latest("wb_forest_area_pct.csv", "forest_pct", year_min=2015)
forest = forest[forest["country_code"].isin(country_codes)]
if len(forest) > 0:
    fig_forest = px.choropleth(
        forest,
        locations="country_code",
        color="forest_pct",
        hover_name="country_name",
        hover_data={"forest_pct": ":.1f", "forest_pct_year": True, "country_code": False},
        color_continuous_scale="Greens",
        range_color=[0, 80],
        labels={"forest_pct": "Forest Area (% of land)", "forest_pct_year": "Data Year"},
        title="Forest Cover (% of land area)<br>"
              "<sub>Source: World Bank (AG.LND.FRST.ZS) / FAO</sub>",
    )
    fig_forest.update_geos(**GEO_TEMPLATE)
    fig_forest.update_layout(**LAYOUT_TEMPLATE)
    fig_forest.write_html(os.path.join(VIZ_DIR, "19_forest_cover_map.html"), include_plotlyjs="cdn")
    print("  Saved: 19_forest_cover_map.html")

renew = load_wb_latest("wb_renewable_energy_pct.csv", "renew_pct", year_min=2015)
renew = renew[renew["country_code"].isin(country_codes)]
if len(renew) > 0:
    fig_renew = px.choropleth(
        renew,
        locations="country_code",
        color="renew_pct",
        hover_name="country_name",
        hover_data={"renew_pct": ":.1f", "renew_pct_year": True, "country_code": False},
        color_continuous_scale="Emrld",
        range_color=[0, 95],
        labels={"renew_pct": "Renewable Energy (% of total)", "renew_pct_year": "Data Year"},
        title="Renewable Energy Consumption (% of total energy)<br>"
              "<sub>Source: World Bank (EG.FEC.RNEW.ZS)</sub>",
    )
    fig_renew.update_geos(**GEO_TEMPLATE)
    fig_renew.update_layout(**LAYOUT_TEMPLATE)
    fig_renew.write_html(os.path.join(VIZ_DIR, "20_renewable_energy_map.html"), include_plotlyjs="cdn")
    print("  Saved: 20_renewable_energy_map.html")

water = load_wb_latest("wb_freshwater_withdrawals_pct.csv", "water_stress", year_min=2005)
water = water[water["country_code"].isin(country_codes)]
if len(water) > 0:
    fig_water = px.choropleth(
        water,
        locations="country_code",
        color="water_stress",
        hover_name="country_name",
        hover_data={"water_stress": ":.1f", "water_stress_year": True, "country_code": False},
        color_continuous_scale="Blues_r",
        range_color=[0, 150],
        labels={"water_stress": "Freshwater Withdrawal (% of resources)", "water_stress_year": "Data Year"},
        title="Freshwater Stress: Annual Withdrawals (% of internal resources)<br>"
              "<sub>Over 100% = unsustainable | Source: World Bank (ER.H2O.FWTL.ZS)</sub>",
    )
    fig_water.update_geos(**GEO_TEMPLATE)
    fig_water.update_layout(**LAYOUT_TEMPLATE)
    fig_water.write_html(os.path.join(VIZ_DIR, "21_water_stress_map.html"), include_plotlyjs="cdn")
    print("  Saved: 21_water_stress_map.html")

# ============================================================
# BONUS: Multi-indicator spatial scatter (GDP vs Life Exp on map)
# ============================================================
print("\n" + "=" * 60)
print("SPATIAL VIZ BONUS: Bubble Map - GDP, LifeExp, Population")
print("=" * 60)

rosling = pd.read_csv(os.path.join(DATA_PROC, "rosling_ready.csv"))
latest_yr = rosling["year"].max()
r_latest = rosling[rosling["year"] == latest_yr].copy()
r_latest = r_latest.dropna(subset=["latitude","longitude","gdp_per_capita","life_expectancy","population"])
r_latest["pop_millions"] = r_latest["population"] / 1e6
r_latest["bubble_size"] = np.sqrt(r_latest["population"]) / 500

continent_colors_map = {
    "Africa": "#00D5E0", "Americas": "#FFE700",
    "Asia": "#FF5872", "Europe": "#7FEB00", "Other": "#AAAAAA"
}

fig_bubble_map = go.Figure()
for cont, color in continent_colors_map.items():
    subset = r_latest[r_latest["continent"] == cont]
    if len(subset) == 0:
        continue
    fig_bubble_map.add_trace(go.Scattergeo(
        lat=subset["latitude"].astype(float),
        lon=subset["longitude"].astype(float),
        text=subset.apply(
            lambda r: f"<b>{r['country_name']}</b><br>"
                      f"GDP/cap: ${r['gdp_per_capita']:,.0f}<br>"
                      f"Life Exp: {r['life_expectancy']:.1f} yrs<br>"
                      f"Pop: {r['pop_millions']:.1f}M",
            axis=1
        ),
        hoverinfo="text",
        mode="markers",
        marker=dict(
            size=subset["bubble_size"],
            color=color,
            opacity=0.7,
            line=dict(width=0.5, color="#333"),
            sizemin=4,
        ),
        name=cont,
    ))

fig_bubble_map.update_layout(
    title=f"Nations on the Map: GDP, Health & Population ({latest_yr})<br>"
          "<sub>Bubble size = population | Hover for details | Source: World Bank</sub>",
    geo=dict(**GEO_TEMPLATE),
    legend=dict(title="Continent", orientation="h", yanchor="bottom", y=-0.05, xanchor="center", x=0.5),
    **LAYOUT_TEMPLATE,
)
fig_bubble_map.write_html(os.path.join(VIZ_DIR, "22_bubble_map_gdp_health.html"), include_plotlyjs="cdn")
print("  Saved: 22_bubble_map_gdp_health.html")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("PHASE 4 COMPLETE: Spatial Visualization Summary")
print("=" * 60)
viz_files = sorted([f for f in os.listdir(VIZ_DIR) if f.endswith(".html")])
for f in viz_files:
    fpath = os.path.join(VIZ_DIR, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  {f:55s} {size_kb:8.1f} KB")
print(f"\nTotal: {len(viz_files)} visualizations")
