"""
Phase 3: Hans Rosling Visualization Engine
=============================================
Generates all signature Rosling/Gapminder visualizations using Plotly.

Visualizations:
  1. Animated Bubble Chart: GDP per capita vs Life Expectancy (THE classic)
  2. Animated Bubble Chart: Fertility Rate vs Life Expectancy
  3. Child Mortality vs GDP per capita
  4. Income vs Health Expenditure
  5. Population Treemap by Region
  6. Trajectory traces for selected countries

All charts are saved as interactive HTML files.

Data Sources:
  - World Bank Open Data (https://data.worldbank.org/)
  - Gapminder (https://www.gapminder.org/data/)
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json

# ============================================================
# CONFIGURATION
# ============================================================
DATA_PROC = "/home/claude/rosling_project/data/processed"
VIZ_DIR = "/home/claude/rosling_project/visualizations"
os.makedirs(VIZ_DIR, exist_ok=True)

# Rosling-inspired color palette by continent
CONTINENT_COLORS = {
    "Africa": "#00D5E0",
    "Americas": "#FFE700",
    "Asia": "#FF5872",
    "Europe": "#7FEB00",
    "Other": "#AAAAAA",
}

# Countries to highlight in trajectory plots
HIGHLIGHT_COUNTRIES = [
    "CHN", "IND", "USA", "BRA", "NGA", "JPN", "DEU",
    "GBR", "ZAF", "IDN", "BGD", "RUS", "MEX", "ETH",
]

# ============================================================
# LOAD DATA
# ============================================================
print("Loading processed data...")
df = pd.read_csv(os.path.join(DATA_PROC, "rosling_ready.csv"))
print(f"  Shape: {df.shape}")
print(f"  Countries: {df['country_code'].nunique()}")
print(f"  Years: {df['year'].min()} - {df['year'].max()}")

# Ensure clean data for animations
df = df.sort_values(["country_code", "year"])

# Log-transform GDP for better visual spread (Rosling uses log scale)
df["gdp_log"] = np.log10(df["gdp_per_capita"].clip(lower=100))

# Population in millions for readable hover text
df["pop_millions"] = df["population"] / 1e6

# ============================================================
# VIZ 1: THE CLASSIC - GDP vs Life Expectancy (Animated)
# ============================================================
print("\nGenerating Viz 1: GDP vs Life Expectancy (animated bubble)...")

fig1 = px.scatter(
    df,
    x="gdp_per_capita",
    y="life_expectancy",
    size="population",
    color="continent",
    hover_name="country_name",
    hover_data={
        "gdp_per_capita": ":,.0f",
        "life_expectancy": ":.1f",
        "population": ":,.0f",
        "continent": True,
        "country_code": False,
        "year": False,
        "pop_millions": False,
        "gdp_log": False,
    },
    animation_frame="year",
    animation_group="country_code",
    log_x=True,
    size_max=80,
    color_discrete_map=CONTINENT_COLORS,
    range_x=[200, 150000],
    range_y=[20, 90],
    labels={
        "gdp_per_capita": "GDP per Capita (PPP, constant 2017 $)",
        "life_expectancy": "Life Expectancy (years)",
        "population": "Population",
        "continent": "Continent",
    },
    title="Wealth vs Health of Nations (1990-2023)<br><sub>Inspired by Hans Rosling's Gapminder | Data: World Bank</sub>",
)

fig1.update_layout(
    font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif"),
    plot_bgcolor="#FAFAFA",
    paper_bgcolor="#FFFFFF",
    xaxis=dict(
        gridcolor="#E0E0E0",
        tickprefix="$",
        tickvals=[500, 1000, 2000, 5000, 10000, 20000, 50000, 100000],
        ticktext=["500", "1K", "2K", "5K", "10K", "20K", "50K", "100K"],
    ),
    yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(
        title="Continent",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
    ),
    width=1100,
    height=700,
    margin=dict(t=100),
)

# Slow down animation
fig1.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
fig1.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 300

fig1_path = os.path.join(VIZ_DIR, "01_gdp_vs_life_expectancy.html")
fig1.write_html(fig1_path, include_plotlyjs="cdn")
print(f"  Saved: {fig1_path}")

# ============================================================
# VIZ 2: Fertility Rate vs Life Expectancy (Animated)
# ============================================================
print("Generating Viz 2: Fertility vs Life Expectancy (animated bubble)...")

df2 = df.dropna(subset=["fertility_rate"]).copy()

fig2 = px.scatter(
    df2,
    x="fertility_rate",
    y="life_expectancy",
    size="population",
    color="continent",
    hover_name="country_name",
    hover_data={
        "fertility_rate": ":.2f",
        "life_expectancy": ":.1f",
        "population": ":,.0f",
        "continent": True,
        "country_code": False,
        "year": False,
        "pop_millions": False,
        "gdp_log": False,
        "gdp_per_capita": False,
    },
    animation_frame="year",
    animation_group="country_code",
    size_max=80,
    color_discrete_map=CONTINENT_COLORS,
    range_x=[0.5, 9],
    range_y=[20, 90],
    labels={
        "fertility_rate": "Fertility Rate (births per woman)",
        "life_expectancy": "Life Expectancy (years)",
        "population": "Population",
        "continent": "Continent",
    },
    title="Fertility vs Longevity (1990-2023)<br><sub>Inspired by Hans Rosling's Gapminder | Data: World Bank</sub>",
)

fig2.update_layout(
    font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif"),
    plot_bgcolor="#FAFAFA",
    paper_bgcolor="#FFFFFF",
    xaxis=dict(gridcolor="#E0E0E0", dtick=1),
    yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(
        title="Continent",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
    ),
    width=1100,
    height=700,
    margin=dict(t=100),
)

fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
fig2.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 300

fig2_path = os.path.join(VIZ_DIR, "02_fertility_vs_life_expectancy.html")
fig2.write_html(fig2_path, include_plotlyjs="cdn")
print(f"  Saved: {fig2_path}")

# ============================================================
# VIZ 3: Child Mortality vs GDP (Animated)
# ============================================================
print("Generating Viz 3: Child Mortality vs GDP (animated bubble)...")

df3 = df.dropna(subset=["child_mortality"]).copy()

fig3 = px.scatter(
    df3,
    x="gdp_per_capita",
    y="child_mortality",
    size="population",
    color="continent",
    hover_name="country_name",
    hover_data={
        "gdp_per_capita": ":,.0f",
        "child_mortality": ":.1f",
        "population": ":,.0f",
        "continent": True,
        "country_code": False,
        "year": False,
        "pop_millions": False,
        "gdp_log": False,
    },
    animation_frame="year",
    animation_group="country_code",
    log_x=True,
    size_max=80,
    color_discrete_map=CONTINENT_COLORS,
    range_x=[200, 150000],
    range_y=[0, 350],
    labels={
        "gdp_per_capita": "GDP per Capita (PPP, constant 2017 $)",
        "child_mortality": "Under-5 Mortality Rate (per 1,000 live births)",
        "population": "Population",
        "continent": "Continent",
    },
    title="Child Mortality vs Wealth (1990-2023)<br><sub>Inspired by Hans Rosling's Gapminder | Data: World Bank</sub>",
)

fig3.update_layout(
    font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif"),
    plot_bgcolor="#FAFAFA",
    paper_bgcolor="#FFFFFF",
    xaxis=dict(
        gridcolor="#E0E0E0",
        tickprefix="$",
        tickvals=[500, 1000, 2000, 5000, 10000, 20000, 50000, 100000],
        ticktext=["500", "1K", "2K", "5K", "10K", "20K", "50K", "100K"],
    ),
    yaxis=dict(gridcolor="#E0E0E0"),
    legend=dict(
        title="Continent",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
    ),
    width=1100,
    height=700,
    margin=dict(t=100),
)

fig3.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
fig3.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 300

fig3_path = os.path.join(VIZ_DIR, "03_child_mortality_vs_gdp.html")
fig3.write_html(fig3_path, include_plotlyjs="cdn")
print(f"  Saved: {fig3_path}")

# ============================================================
# VIZ 4: Country Trajectories (GDP vs Life Expectancy over time)
# ============================================================
print("Generating Viz 4: Country trajectory traces...")

df_traj = df[df["country_code"].isin(HIGHLIGHT_COUNTRIES)].copy()

fig4 = go.Figure()

for cc in HIGHLIGHT_COUNTRIES:
    cdata = df_traj[df_traj["country_code"] == cc].sort_values("year")
    if len(cdata) == 0:
        continue
    continent = cdata["continent"].iloc[0]
    name = cdata["country_name"].iloc[0]
    color = CONTINENT_COLORS.get(continent, "#888")

    # Trail line
    fig4.add_trace(go.Scatter(
        x=cdata["gdp_per_capita"],
        y=cdata["life_expectancy"],
        mode="lines",
        line=dict(color=color, width=1.5),
        opacity=0.5,
        showlegend=False,
        hoverinfo="skip",
    ))

    # Start point
    fig4.add_trace(go.Scatter(
        x=[cdata["gdp_per_capita"].iloc[0]],
        y=[cdata["life_expectancy"].iloc[0]],
        mode="markers",
        marker=dict(color=color, size=6, symbol="circle-open"),
        showlegend=False,
        hovertext=f"{name} ({cdata['year'].iloc[0]})",
        hoverinfo="text",
    ))

    # End point (current)
    fig4.add_trace(go.Scatter(
        x=[cdata["gdp_per_capita"].iloc[-1]],
        y=[cdata["life_expectancy"].iloc[-1]],
        mode="markers+text",
        marker=dict(
            color=color,
            size=np.sqrt(cdata["population"].iloc[-1] / 1e6) * 1.5,
            sizemin=8,
        ),
        text=[name],
        textposition="top center",
        textfont=dict(size=10, color=color),
        showlegend=False,
        hovertext=f"{name} ({cdata['year'].iloc[-1]})<br>"
                  f"GDP/cap: ${cdata['gdp_per_capita'].iloc[-1]:,.0f}<br>"
                  f"Life Exp: {cdata['life_expectancy'].iloc[-1]:.1f}",
        hoverinfo="text",
    ))

fig4.update_layout(
    title="Country Trajectories: Wealth vs Health (1990-2023)<br>"
          "<sub>Each trail shows a country's path over time | Data: World Bank</sub>",
    xaxis=dict(
        title="GDP per Capita (PPP, constant 2017 $, log scale)",
        type="log",
        gridcolor="#E0E0E0",
        range=[np.log10(300), np.log10(150000)],
        tickprefix="$",
        tickvals=[500, 1000, 2000, 5000, 10000, 20000, 50000, 100000],
        ticktext=["500", "1K", "2K", "5K", "10K", "20K", "50K", "100K"],
    ),
    yaxis=dict(
        title="Life Expectancy (years)",
        gridcolor="#E0E0E0",
        range=[30, 90],
    ),
    font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif"),
    plot_bgcolor="#FAFAFA",
    paper_bgcolor="#FFFFFF",
    width=1100,
    height=700,
    margin=dict(t=100),
)

fig4_path = os.path.join(VIZ_DIR, "04_country_trajectories.html")
fig4.write_html(fig4_path, include_plotlyjs="cdn")
print(f"  Saved: {fig4_path}")

# ============================================================
# VIZ 5: Continental Trends (Small Multiples)
# ============================================================
print("Generating Viz 5: Continental trend lines...")

# Compute continent-level weighted averages per year
continent_stats = []
for (continent, year), grp in df.groupby(["continent", "year"]):
    pop = grp["population"].sum()
    if pop > 0 and grp["gdp_per_capita"].notna().any() and grp["life_expectancy"].notna().any():
        # Population-weighted means
        gdp_wt = np.average(
            grp["gdp_per_capita"].dropna(),
            weights=grp.loc[grp["gdp_per_capita"].notna(), "population"]
        )
        le_wt = np.average(
            grp["life_expectancy"].dropna(),
            weights=grp.loc[grp["life_expectancy"].notna(), "population"]
        )
        fert_vals = grp.dropna(subset=["fertility_rate"])
        fert_wt = np.average(fert_vals["fertility_rate"], weights=fert_vals["population"]) if len(fert_vals) > 0 else np.nan

        continent_stats.append({
            "continent": continent,
            "year": year,
            "population": pop,
            "gdp_per_capita_wt": gdp_wt,
            "life_expectancy_wt": le_wt,
            "fertility_rate_wt": fert_wt,
        })

cs = pd.DataFrame(continent_stats)
cs = cs[cs["continent"] != "Other"]

fig5 = make_subplots(
    rows=1, cols=3,
    subplot_titles=[
        "GDP per Capita (PPP)",
        "Life Expectancy",
        "Fertility Rate",
    ],
    horizontal_spacing=0.08,
)

for continent in ["Africa", "Americas", "Asia", "Europe"]:
    cdata = cs[cs["continent"] == continent].sort_values("year")
    color = CONTINENT_COLORS[continent]

    fig5.add_trace(go.Scatter(
        x=cdata["year"], y=cdata["gdp_per_capita_wt"],
        name=continent, mode="lines", line=dict(color=color, width=2.5),
        legendgroup=continent, showlegend=True,
    ), row=1, col=1)

    fig5.add_trace(go.Scatter(
        x=cdata["year"], y=cdata["life_expectancy_wt"],
        name=continent, mode="lines", line=dict(color=color, width=2.5),
        legendgroup=continent, showlegend=False,
    ), row=1, col=2)

    fig5.add_trace(go.Scatter(
        x=cdata["year"], y=cdata["fertility_rate_wt"],
        name=continent, mode="lines", line=dict(color=color, width=2.5),
        legendgroup=continent, showlegend=False,
    ), row=1, col=3)

fig5.update_layout(
    title="Continental Trends (Population-Weighted Averages, 1990-2023)<br>"
          "<sub>Data: World Bank | Visualization inspired by Hans Rosling's Gapminder</sub>",
    font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif"),
    plot_bgcolor="#FAFAFA",
    paper_bgcolor="#FFFFFF",
    legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="center", x=0.5),
    width=1400,
    height=500,
    margin=dict(t=120),
)

fig5.update_xaxes(gridcolor="#E0E0E0")
fig5.update_yaxes(gridcolor="#E0E0E0")
fig5.update_yaxes(tickprefix="$", row=1, col=1)

fig5_path = os.path.join(VIZ_DIR, "05_continental_trends.html")
fig5.write_html(fig5_path, include_plotlyjs="cdn")
print(f"  Saved: {fig5_path}")

# ============================================================
# VIZ 6: Income Distribution Shift (Stacked Area / Ridge)
# ============================================================
print("Generating Viz 6: Income distribution shift...")

# Show how GDP per capita distribution has shifted over decades
selected_years = [1995, 2000, 2005, 2010, 2015, 2020]

fig6 = go.Figure()
yr_colors = px.colors.sequential.Viridis

for i, yr in enumerate(selected_years):
    yr_data = df[df["year"] == yr].dropna(subset=["gdp_per_capita", "population"])
    if len(yr_data) == 0:
        continue
    # Sort by GDP
    yr_data = yr_data.sort_values("gdp_per_capita")
    # Create weighted histogram-like representation
    log_gdp = np.log10(yr_data["gdp_per_capita"].values)
    weights = yr_data["population"].values

    bins = np.linspace(2, 5.2, 50)  # log10(100) to log10(150000)
    hist, edges = np.histogram(log_gdp, bins=bins, weights=weights)
    hist = hist / hist.sum()  # normalize
    centers = (edges[:-1] + edges[1:]) / 2

    color_idx = int(i * (len(yr_colors) - 1) / max(len(selected_years) - 1, 1))
    fig6.add_trace(go.Scatter(
        x=10 ** centers,
        y=hist,
        name=str(yr),
        mode="lines",
        fill="tozeroy",
        line=dict(width=2),
        opacity=0.6,
    ))

fig6.update_layout(
    title="Global Income Distribution Shift (Population-Weighted)<br>"
          "<sub>How the world's income distribution has evolved | Data: World Bank</sub>",
    xaxis=dict(
        title="GDP per Capita (PPP, constant 2017 $)",
        type="log",
        gridcolor="#E0E0E0",
        tickprefix="$",
        tickvals=[100, 500, 1000, 5000, 10000, 50000, 100000],
        ticktext=["100", "500", "1K", "5K", "10K", "50K", "100K"],
    ),
    yaxis=dict(
        title="Share of World Population",
        gridcolor="#E0E0E0",
        tickformat=".1%",
    ),
    font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif"),
    plot_bgcolor="#FAFAFA",
    paper_bgcolor="#FFFFFF",
    width=1100,
    height=600,
    margin=dict(t=100),
)

fig6_path = os.path.join(VIZ_DIR, "06_income_distribution_shift.html")
fig6.write_html(fig6_path, include_plotlyjs="cdn")
print(f"  Saved: {fig6_path}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("PHASE 3 COMPLETE: Visualization Summary")
print("=" * 60)
viz_files = sorted(os.listdir(VIZ_DIR))
for f in viz_files:
    fpath = os.path.join(VIZ_DIR, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  {f:50s} {size_kb:8.1f} KB")
print(f"\nTotal: {len(viz_files)} visualizations generated")
