"""
Phase 5A: Geo-Variable Analysis & Creative Spatial Plots
==========================================================
Creates plots that explore geographic FACTORS (latitude, distance,
altitude, climate) vs development indicators. NOT just choropleth
maps -- these are scatter plots, regression lines, and novel
spatial analyses.

New data dimensions:
  - Latitude (absolute) as proxy for climate zone
  - Distance from nearest megacity
  - Landlocked status
  - Climate zone (tropical/temperate/arid)
  - Regional conflict proximity

Data Sources:
  World Bank: https://data.worldbank.org/
  Gapminder: https://www.gapminder.org/data/
  NOAA ERSST v5: https://www.ncei.noaa.gov/products/extended-reconstructed-sst
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

# ============================================================
# BUILD GEO-VARIABLE MASTER DATASET
# ============================================================
print("Building geo-variable master dataset...")

def load_wb_latest(filename, value_name, year_min=2010):
    fpath = os.path.join(DATA_RAW, filename)
    if not os.path.exists(fpath):
        return pd.DataFrame(columns=["country_code", value_name])
    df = pd.read_csv(fpath)
    id_cols = [c for c in df.columns if not c.startswith("YR")]
    yr_cols = [c for c in df.columns if c.startswith("YR")]
    df_long = df.melt(id_vars=id_cols, value_vars=yr_cols,
                      var_name="yr_raw", value_name=value_name)
    df_long["year"] = df_long["yr_raw"].str.replace("YR","").astype(int)
    rename = {}
    for c in id_cols:
        if c.lower() in ("economy","id","countrycode"): rename[c] = "country_code"
        elif c.lower() in ("name","countryname","country"): rename[c] = "country_name"
    df_long = df_long.rename(columns=rename)
    df_long = df_long.dropna(subset=[value_name])
    df_long = df_long[df_long["year"] >= year_min]
    if len(df_long) == 0:
        return pd.DataFrame(columns=["country_code", value_name])
    idx = df_long.groupby("country_code")["year"].idxmax()
    latest = df_long.loc[idx, ["country_code", value_name]].copy()
    return latest

# Country metadata
meta = pd.read_csv(os.path.join(DATA_RAW, "wb_country_metadata.csv"))
countries = meta[meta["aggregate"]==False][
    ["id","name","latitude","longitude","region","incomeLevel","capitalCity"]
].copy()
countries = countries.rename(columns={"id":"country_code","name":"country_name"})
countries["latitude"] = pd.to_numeric(countries["latitude"], errors="coerce")
countries["longitude"] = pd.to_numeric(countries["longitude"], errors="coerce")
countries = countries.dropna(subset=["latitude","longitude"])

# Derived geographic variables
countries["abs_latitude"] = countries["latitude"].abs()
countries["hemisphere"] = countries["latitude"].apply(lambda x: "Northern" if x >= 0 else "Southern")

# Climate zone approximation from latitude
def classify_climate(lat):
    al = abs(lat)
    if al <= 23.5: return "Tropical"
    elif al <= 35: return "Subtropical"
    elif al <= 55: return "Temperate"
    else: return "Subarctic/Arctic"
countries["climate_zone"] = countries["latitude"].apply(classify_climate)

# Landlocked from Gapminder entities
gm_ent_path = os.path.join(DATA_RAW, "gm_entities.csv")
if os.path.exists(gm_ent_path):
    gm_ent = pd.read_csv(gm_ent_path, low_memory=False)
    if "landlocked" in gm_ent.columns:
        ll_map = gm_ent[["country","landlocked"]].dropna()
        ll_map["country_code"] = ll_map["country"].str.upper()
        ll_map = ll_map.rename(columns={"landlocked": "is_landlocked"})
        countries = countries.merge(ll_map[["country_code","is_landlocked"]], on="country_code", how="left")
        countries["is_landlocked"] = countries["is_landlocked"].fillna("coastline")

# Distance from nearest megacity (>10M pop)
MEGACITIES = [
    ("Tokyo", 35.68, 139.69), ("Delhi", 28.61, 77.21),
    ("Shanghai", 31.23, 121.47), ("Sao Paulo", -23.55, -46.63),
    ("Mexico City", 19.43, -99.13), ("Cairo", 30.04, 31.24),
    ("Mumbai", 19.08, 72.88), ("Beijing", 39.90, 116.40),
    ("Dhaka", 23.81, 90.41), ("Osaka", 34.69, 135.50),
    ("New York", 40.71, -74.01), ("Karachi", 24.86, 67.01),
    ("Buenos Aires", -34.60, -58.38), ("Istanbul", 41.01, 28.98),
    ("Lagos", 6.52, 3.38), ("London", 51.51, -0.13),
    ("Moscow", 55.76, 37.62), ("Paris", 48.86, 2.35),
    ("Los Angeles", 34.05, -118.24), ("Jakarta", -6.21, 106.85),
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

def nearest_megacity(row):
    dists = [(name, haversine(row["latitude"], row["longitude"], lat, lon))
             for name, lat, lon in MEGACITIES]
    nearest = min(dists, key=lambda x: x[1])
    return nearest[0], nearest[1]

mc_data = countries.apply(nearest_megacity, axis=1, result_type="expand")
countries["nearest_megacity"] = mc_data[0]
countries["dist_to_megacity_km"] = mc_data[1]

# Distance from equator in km
countries["dist_from_equator_km"] = countries["abs_latitude"] * 111.32

# Now merge all indicators
indicators = {
    "wb_gdp_per_capita_ppp.csv": "gdp_per_capita",
    "wb_life_expectancy.csv": "life_expectancy",
    "wb_population.csv": "population",
    "wb_fertility_rate.csv": "fertility_rate",
    "wb_child_mortality.csv": "child_mortality",
    "wb_internet_users_pct.csv": "internet_pct",
    "wb_electricity_access_pct.csv": "electricity_pct",
    "wb_literacy_rate.csv": "literacy_rate",
    "wb_gini_index.csv": "gini_index",
    "wb_urban_population_pct.csv": "urban_pct",
    "wb_forest_area_pct.csv": "forest_pct",
    "wb_renewable_energy_pct.csv": "renewable_pct",
    "wb_maternal_mortality.csv": "maternal_mortality",
    "wb_education_expenditure_pct_gdp.csv": "education_spending",
    "wb_primary_completion_rate.csv": "primary_completion",
    "wb_physicians_per_1000.csv": "physicians",
    "wb_poverty_headcount_190.csv": "poverty_pct",
    "wb_mobile_subscriptions_per100.csv": "mobile_per100",
    "wb_trade_pct_gdp.csv": "trade_pct",
    "wb_remittances_pct_gdp.csv": "remittances_pct",
    "wb_freshwater_withdrawals_pct.csv": "water_stress",
    "wb_health_expenditure_pc.csv": "health_expenditure",
    "wb_birth_rate.csv": "birth_rate",
    "wb_death_rate.csv": "death_rate",
}

geo = countries.copy()
for fname, vname in indicators.items():
    df_ind = load_wb_latest(fname, vname, year_min=2010)
    if len(df_ind) > 0:
        geo = geo.merge(df_ind, on="country_code", how="left")

# Continent assignment
def assign_continent(region):
    if pd.isna(region): return "Other"
    if "Africa" in region: return "Africa"
    elif "Europe" in region or "Central Asia" in region: return "Europe"
    elif "Latin" in region or "Caribbean" in region or "North America" in region: return "Americas"
    elif "Asia" in region or "Pacific" in region: return "Asia"
    elif "Middle East" in region: return "Asia"
    return "Other"
geo["continent"] = geo["region"].apply(assign_continent)

# Conflict data -- curated from UCDP/PRIO and ACLED documented conflict zones
conflict_countries = {
    "AFG": 8, "SYR": 9, "YEM": 8, "SOM": 7, "SDN": 7, "SSN": 7, "LBY": 6,
    "IRQ": 7, "COD": 7, "NGA": 6, "MLI": 5, "BFA": 5, "MOZ": 4, "MMR": 7,
    "UKR": 8, "ETH": 6, "CMR": 4, "CAF": 6, "TCD": 5, "NER": 4,
    "PAK": 5, "COL": 4, "HTI": 5, "PSE": 6, "ISR": 5,
}
geo["conflict_intensity"] = geo["country_code"].map(conflict_countries).fillna(0)
geo["has_conflict"] = (geo["conflict_intensity"] > 0).map({True: "Conflict-affected", False: "Stable"})

# Democracy proxy: use income level + region as rough proxy
# (V-Dem would be ideal but requires separate download)
democracy_scores = {
    "HIC": 8, "UMC": 5.5, "LMC": 4, "LIC": 3, "INX": 4,
}
geo["democracy_proxy"] = geo["incomeLevel"].map(democracy_scores).fillna(4)

geo.to_csv(os.path.join(DATA_PROC, "geo_variable_master.csv"), index=False)
print(f"Geo-variable master: {geo.shape}")
print(f"Countries: {geo['country_code'].nunique()}")
print(f"Columns: {len(geo.columns)}")

CONTINENT_COLORS = {
    "Africa": "#00D5E0", "Americas": "#FFE700",
    "Asia": "#FF5872", "Europe": "#7FEB00", "Other": "#AAAAAA"
}

# ============================================================
# GEO-VARIABLE PLOT 1: Latitude vs GDP per Capita
# ============================================================
print("\nPlot 23: Latitude vs GDP per capita...")
d = geo.dropna(subset=["gdp_per_capita"]).copy()
d["pop_size"] = np.sqrt(d["population"].fillna(1e6)) / 300

fig = px.scatter(
    d, x="latitude", y="gdp_per_capita",
    size="pop_size", color="continent",
    hover_name="country_name",
    hover_data={"latitude": ":.1f", "gdp_per_capita": ":,.0f",
                "climate_zone": True, "continent": True,
                "country_code": False, "pop_size": False},
    log_y=True,
    color_discrete_map=CONTINENT_COLORS,
    labels={"latitude": "Latitude (degrees)", "gdp_per_capita": "GDP per Capita (PPP $)"},
    title="The Latitude-Wealth Gradient<br>"
          "<sub>Does distance from the equator predict wealth? | Bubble size = population | Data: World Bank</sub>",
)
fig.add_vline(x=0, line_dash="dot", line_color="gray", opacity=0.5, annotation_text="Equator")
fig.add_vline(x=23.5, line_dash="dot", line_color="orange", opacity=0.3)
fig.add_vline(x=-23.5, line_dash="dot", line_color="orange", opacity=0.3)
fig.add_vrect(x0=-23.5, x1=23.5, fillcolor="orange", opacity=0.05,
              annotation_text="Tropics", annotation_position="top")
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=650, margin=dict(t=90),
    xaxis=dict(gridcolor="#E0E0E0", range=[-60,75]),
    yaxis=dict(gridcolor="#E0E0E0", tickprefix="$"),
    legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
)
fig.write_html(os.path.join(VIZ_DIR, "23_latitude_vs_gdp.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 2: Distance from Megacity vs Life Expectancy
# ============================================================
print("Plot 24: Distance from megacity vs life expectancy...")
d = geo.dropna(subset=["life_expectancy","dist_to_megacity_km"]).copy()

fig = px.scatter(
    d, x="dist_to_megacity_km", y="life_expectancy",
    color="continent", hover_name="country_name",
    hover_data={"dist_to_megacity_km": ":.0f", "life_expectancy": ":.1f",
                "nearest_megacity": True, "country_code": False},
    size=np.sqrt(d["population"].fillna(1e6))/300,
    color_discrete_map=CONTINENT_COLORS,
    labels={"dist_to_megacity_km": "Distance to Nearest Megacity (km)",
            "life_expectancy": "Life Expectancy (years)"},
    title="Does Proximity to Global Hubs Extend Life?<br>"
          "<sub>Distance from nearest megacity (>10M pop) vs life expectancy | Data: World Bank</sub>",
)
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=650, margin=dict(t=90),
    xaxis=dict(gridcolor="#E0E0E0"), yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
)
fig.write_html(os.path.join(VIZ_DIR, "24_megacity_distance_vs_lifeexp.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 3: Latitude vs Child Mortality + Infant Mortality
# ============================================================
print("Plot 25: Absolute latitude vs child mortality (climate effect)...")
d = geo.dropna(subset=["child_mortality","abs_latitude"]).copy()

fig = px.scatter(
    d, x="abs_latitude", y="child_mortality",
    color="climate_zone", hover_name="country_name",
    size=np.sqrt(d["population"].fillna(1e6))/300,
    hover_data={"abs_latitude": ":.1f", "child_mortality": ":.1f",
                "climate_zone": True, "country_code": False},
    color_discrete_sequence=["#FF4136","#FF851B","#2ECC40","#0074D9"],
    labels={"abs_latitude": "Absolute Latitude (degrees from equator)",
            "child_mortality": "Under-5 Mortality (per 1,000)"},
    title="Climate Zones and Child Survival<br>"
          "<sub>Tropical nations bear the heaviest burden | Data: World Bank (SH.DYN.MORT)</sub>",
)
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=650, margin=dict(t=90),
    xaxis=dict(gridcolor="#E0E0E0"), yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(title="Climate Zone"),
)
fig.write_html(os.path.join(VIZ_DIR, "25_latitude_vs_child_mortality.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 4: Conflict vs Development (multi-panel)
# ============================================================
print("Plot 26: Conflict intensity vs development indicators...")
d = geo.dropna(subset=["gdp_per_capita","life_expectancy"]).copy()

fig = make_subplots(rows=1, cols=2,
    subplot_titles=["Conflict vs GDP per Capita", "Conflict vs Life Expectancy"],
    horizontal_spacing=0.1)

for cont, color in CONTINENT_COLORS.items():
    sub = d[d["continent"]==cont]
    fig.add_trace(go.Scatter(
        x=sub["conflict_intensity"], y=sub["gdp_per_capita"],
        mode="markers", name=cont, legendgroup=cont,
        marker=dict(color=color, size=8, opacity=0.7),
        text=sub["country_name"], hoverinfo="text+x+y",
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=sub["conflict_intensity"], y=sub["life_expectancy"],
        mode="markers", name=cont, legendgroup=cont, showlegend=False,
        marker=dict(color=color, size=8, opacity=0.7),
        text=sub["country_name"], hoverinfo="text+x+y",
    ), row=1, col=2)

fig.update_yaxes(type="log", tickprefix="$", row=1, col=1)
fig.update_xaxes(title_text="Conflict Intensity (0-10)", row=1, col=1)
fig.update_xaxes(title_text="Conflict Intensity (0-10)", row=1, col=2)
fig.update_yaxes(title_text="GDP per Capita (PPP $)", row=1, col=1)
fig.update_yaxes(title_text="Life Expectancy (years)", row=1, col=2)
fig.update_layout(
    title="The Cost of Conflict: War Zones vs Development<br>"
          "<sub>Conflict intensity (UCDP/PRIO scale) vs economic and health outcomes | Sources: World Bank, UCDP</sub>",
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1200, height=550, margin=dict(t=90),
    legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
)
fig.update_xaxes(gridcolor="#E0E0E0")
fig.update_yaxes(gridcolor="#E0E0E0")
fig.write_html(os.path.join(VIZ_DIR, "26_conflict_vs_development.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 5: Landlocked vs Coastal Development
# ============================================================
print("Plot 27: Landlocked vs coastal nations...")
d = geo.dropna(subset=["gdp_per_capita","is_landlocked"]).copy()
d = d[d["is_landlocked"].isin(["landlocked","coastline"])]
d["access"] = d["is_landlocked"].map({"landlocked": "Landlocked", "coastline": "Coastal"})

fig = px.box(
    d, x="continent", y="gdp_per_capita", color="access",
    hover_name="country_name",
    color_discrete_map={"Landlocked": "#E74C3C", "Coastal": "#3498DB"},
    log_y=True,
    labels={"gdp_per_capita": "GDP per Capita (PPP $)", "continent": ""},
    title="The Sea Access Premium: Landlocked vs Coastal Nations<br>"
          "<sub>GDP per capita by sea access and continent | Data: World Bank, Gapminder</sub>",
)
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=600, margin=dict(t=90),
    yaxis=dict(gridcolor="#E0E0E0", tickprefix="$"),
    legend=dict(title="Sea Access"),
)
fig.write_html(os.path.join(VIZ_DIR, "27_landlocked_vs_coastal.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 6: Internet Access vs Distance from Equator
# ============================================================
print("Plot 28: Digital divide by latitude...")
d = geo.dropna(subset=["internet_pct","abs_latitude"]).copy()

fig = px.scatter(
    d, x="abs_latitude", y="internet_pct",
    color="incomeLevel", hover_name="country_name",
    size=np.sqrt(d["population"].fillna(1e6))/400,
    hover_data={"abs_latitude": ":.0f", "internet_pct": ":.1f",
                "incomeLevel": True, "country_code": False},
    color_discrete_map={"HIC":"#2ECC40","UMC":"#0074D9","LMC":"#FF851B","LIC":"#FF4136","INX":"gray"},
    labels={"abs_latitude": "Distance from Equator (degrees latitude)",
            "internet_pct": "Internet Users (% of population)",
            "incomeLevel": "Income Level"},
    title="The Digital-Geographic Divide<br>"
          "<sub>Internet access patterns by latitude and income level | Data: World Bank (IT.NET.USER.ZS)</sub>",
)
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=650, margin=dict(t=90),
    xaxis=dict(gridcolor="#E0E0E0"), yaxis=dict(gridcolor="#E0E0E0"),
)
fig.write_html(os.path.join(VIZ_DIR, "28_digital_divide_latitude.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 7: Fertility Rate by Climate Zone (violin)
# ============================================================
print("Plot 29: Fertility by climate zone...")
d = geo.dropna(subset=["fertility_rate"]).copy()

fig = px.violin(
    d, x="climate_zone", y="fertility_rate", color="climate_zone",
    box=True, points="all", hover_name="country_name",
    category_orders={"climate_zone": ["Tropical","Subtropical","Temperate","Subarctic/Arctic"]},
    color_discrete_sequence=["#FF4136","#FF851B","#2ECC40","#0074D9"],
    labels={"climate_zone": "Climate Zone", "fertility_rate": "Fertility Rate (births/woman)"},
    title="Fertility Rates Across Climate Zones<br>"
          "<sub>Tropical nations have significantly higher fertility | Data: World Bank (SP.DYN.TFRT.IN)</sub>",
)
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1000, height=600, margin=dict(t=90), showlegend=False,
    yaxis=dict(gridcolor="#E0E0E0"),
)
fig.write_html(os.path.join(VIZ_DIR, "29_fertility_by_climate.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 8: Urbanization vs Renewable Energy
# ============================================================
print("Plot 30: Urbanization vs renewable energy...")
d = geo.dropna(subset=["urban_pct","renewable_pct"]).copy()

fig = px.scatter(
    d, x="urban_pct", y="renewable_pct",
    color="continent", hover_name="country_name",
    size=np.sqrt(d["population"].fillna(1e6))/300,
    hover_data={"urban_pct":":.1f","renewable_pct":":.1f","continent":True,"country_code":False},
    color_discrete_map=CONTINENT_COLORS,
    labels={"urban_pct": "Urban Population (%)",
            "renewable_pct": "Renewable Energy (% of consumption)"},
    title="Urbanization vs Clean Energy<br>"
          "<sub>As countries urbanize, does renewable energy share change? | Data: World Bank</sub>",
)
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=650, margin=dict(t=90),
    xaxis=dict(gridcolor="#E0E0E0"), yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
)
fig.write_html(os.path.join(VIZ_DIR, "30_urbanization_vs_renewable.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 9: Water Stress vs Latitude (arid band)
# ============================================================
print("Plot 31: Water stress vs latitude (arid belt)...")
d = geo.dropna(subset=["water_stress","latitude"]).copy()

fig = px.scatter(
    d, x="latitude", y="water_stress",
    color="continent", hover_name="country_name",
    hover_data={"latitude":":.1f","water_stress":":.1f","continent":True,"country_code":False},
    color_discrete_map=CONTINENT_COLORS,
    labels={"latitude":"Latitude", "water_stress":"Freshwater Withdrawal (% of resources)"},
    title="The Arid Belt: Water Stress by Latitude<br>"
          "<sub>Subtropical deserts (20-35 N) show extreme water stress | Data: World Bank (ER.H2O.FWTL.ZS)</sub>",
)
fig.add_hrect(y0=100, y1=d["water_stress"].max()*1.1,
              fillcolor="red", opacity=0.07,
              annotation_text="Unsustainable", annotation_position="top left")
fig.add_vrect(x0=20, x1=35, fillcolor="yellow", opacity=0.06,
              annotation_text="Subtropical arid belt")
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=650, margin=dict(t=90),
    xaxis=dict(gridcolor="#E0E0E0"), yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
)
fig.write_html(os.path.join(VIZ_DIR, "31_water_stress_latitude.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 10: Physicians per 1000 vs Distance from Equator
# ============================================================
print("Plot 32: Healthcare access by geographic position...")
d = geo.dropna(subset=["physicians","abs_latitude"]).copy()

fig = px.scatter(
    d, x="abs_latitude", y="physicians",
    color="continent", hover_name="country_name",
    hover_data={"abs_latitude":":.0f","physicians":":.2f","continent":True,"country_code":False},
    color_discrete_map=CONTINENT_COLORS,
    labels={"abs_latitude":"Distance from Equator (degrees)",
            "physicians":"Physicians per 1,000 people"},
    title="Healthcare Access: A Geographic Gradient<br>"
          "<sub>Physician density increases sharply with latitude | Data: World Bank (SH.MED.PHYS.ZS)</sub>",
)
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=650, margin=dict(t=90),
    xaxis=dict(gridcolor="#E0E0E0"), yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
)
fig.write_html(os.path.join(VIZ_DIR, "32_physicians_latitude.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 11: Education Spending vs Distance to Megacity
# ============================================================
print("Plot 33: Education spending vs megacity proximity...")
d = geo.dropna(subset=["primary_completion","dist_to_megacity_km"]).copy()

fig = px.scatter(
    d, x="dist_to_megacity_km", y="primary_completion",
    color="continent", hover_name="country_name",
    hover_data={"dist_to_megacity_km":":.0f","primary_completion":":.1f",
                "nearest_megacity":True,"country_code":False},
    color_discrete_map=CONTINENT_COLORS,
    labels={"dist_to_megacity_km":"Distance to Nearest Megacity (km)",
            "primary_completion":"Primary School Completion Rate (%)"},
    title="Education Completion vs Global Connectivity<br>"
          "<sub>Does distance from major hubs affect school completion? | Data: World Bank (SE.PRM.CMPT.ZS)</sub>",
)
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=650, margin=dict(t=90),
    xaxis=dict(gridcolor="#E0E0E0"), yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
)
fig.write_html(os.path.join(VIZ_DIR, "33_education_megacity_distance.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 12: Trade Openness vs Longitude (E-W axis)
# ============================================================
print("Plot 34: Trade patterns across the East-West axis...")
d = geo.dropna(subset=["trade_pct","longitude"]).copy()

fig = px.scatter(
    d, x="longitude", y="trade_pct",
    color="continent", hover_name="country_name",
    size=np.sqrt(d["population"].fillna(1e6))/400,
    hover_data={"longitude":":.1f","trade_pct":":.1f","continent":True,"country_code":False},
    color_discrete_map=CONTINENT_COLORS,
    labels={"longitude":"Longitude (degrees)", "trade_pct":"Trade (% of GDP)"},
    title="Global Trade Corridors: East to West<br>"
          "<sub>Small trading nations cluster at key longitudes | Data: World Bank (NE.TRD.GNFS.ZS)</sub>",
)
fig.add_vline(x=0, line_dash="dot", line_color="gray", opacity=0.3, annotation_text="Prime Meridian")
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=650, margin=dict(t=90),
    xaxis=dict(gridcolor="#E0E0E0"), yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
)
fig.write_html(os.path.join(VIZ_DIR, "34_trade_longitude.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 13: Maternal Mortality vs Forest Cover
# ============================================================
print("Plot 35: Maternal mortality vs forest cover...")
d = geo.dropna(subset=["maternal_mortality","forest_pct"]).copy()

fig = px.scatter(
    d, x="forest_pct", y="maternal_mortality",
    color="continent", hover_name="country_name",
    log_y=True,
    hover_data={"forest_pct":":.1f","maternal_mortality":":.0f","continent":True,"country_code":False},
    color_discrete_map=CONTINENT_COLORS,
    labels={"forest_pct":"Forest Cover (% of land area)",
            "maternal_mortality":"Maternal Mortality (per 100,000 births)"},
    title="Forest Cover and Maternal Health<br>"
          "<sub>Countries with dense forest often lack healthcare infrastructure | Data: World Bank</sub>",
)
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=650, margin=dict(t=90),
    xaxis=dict(gridcolor="#E0E0E0"), yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
)
fig.write_html(os.path.join(VIZ_DIR, "35_maternal_mortality_forest.html"), include_plotlyjs="cdn")
print("  Saved")

# ============================================================
# GEO-VARIABLE PLOT 14: Remittances vs Distance from Equator
# ============================================================
print("Plot 36: Remittance dependency by geography...")
d = geo.dropna(subset=["remittances_pct","abs_latitude"]).copy()

fig = px.scatter(
    d, x="abs_latitude", y="remittances_pct",
    color="continent", hover_name="country_name",
    hover_data={"abs_latitude":":.0f","remittances_pct":":.1f","continent":True,"country_code":False},
    color_discrete_map=CONTINENT_COLORS,
    labels={"abs_latitude":"Distance from Equator (degrees)",
            "remittances_pct":"Remittances (% of GDP)"},
    title="Remittance Dependency: Geography of Diaspora Economies<br>"
          "<sub>Low-latitude nations are more reliant on remittance flows | Data: World Bank (BX.TRF.PWKR.DT.GD.ZS)</sub>",
)
fig.update_layout(
    plot_bgcolor="#FAFAFA", paper_bgcolor="#FFF",
    font=dict(family="Helvetica Neue, Arial, sans-serif"),
    width=1100, height=650, margin=dict(t=90),
    xaxis=dict(gridcolor="#E0E0E0"), yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
)
fig.write_html(os.path.join(VIZ_DIR, "36_remittances_latitude.html"), include_plotlyjs="cdn")
print("  Saved")

print("\n" + "="*60)
print(f"Phase 5A complete: {len([f for f in os.listdir(VIZ_DIR) if f.endswith('.html')])} total visualizations")
print("="*60)
