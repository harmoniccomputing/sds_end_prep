"""
Phase 2: Data Processing Pipeline
===================================
Reshapes World Bank wide-format CSVs into long format,
merges all indicators with country metadata, and produces
a single master dataset ready for visualization.
"""

import pandas as pd
import numpy as np
import os
import json

DATA_RAW = "/home/claude/rosling_project/data/raw"
DATA_PROC = "/home/claude/rosling_project/data/processed"
os.makedirs(DATA_PROC, exist_ok=True)

# ============================================================
# 1. LOAD AND RESHAPE WORLD BANK INDICATORS
# ============================================================
print("=" * 60)
print("1. Reshaping World Bank indicator CSVs (wide -> long)")
print("=" * 60)

WB_FILES = {
    "wb_gdp_per_capita_ppp.csv": "gdp_per_capita",
    "wb_life_expectancy.csv": "life_expectancy",
    "wb_population.csv": "population",
    "wb_fertility_rate.csv": "fertility_rate",
    "wb_child_mortality.csv": "child_mortality",
    "wb_birth_rate.csv": "birth_rate",
    "wb_death_rate.csv": "death_rate",
    "wb_health_expenditure_pc.csv": "health_expenditure",
    "wb_literacy_rate.csv": "literacy_rate",
    "wb_gini_index.csv": "gini_index",
}

indicator_frames = {}

for fname, indicator_name in WB_FILES.items():
    fpath = os.path.join(DATA_RAW, fname)
    if not os.path.exists(fpath):
        print(f"   SKIP (not found): {fname}")
        continue

    df = pd.read_csv(fpath)
    print(f"   Processing {fname} ({df.shape})...", end=" ")

    # Identify year columns (they look like "YR2000" or just numeric)
    id_cols = [c for c in df.columns if not c.startswith("YR")]
    year_cols = [c for c in df.columns if c.startswith("YR")]

    if not year_cols:
        # Try numeric columns
        year_cols = [c for c in df.columns if c.isdigit()]
        id_cols = [c for c in df.columns if not c.isdigit()]

    # Melt to long format
    df_long = df.melt(
        id_vars=id_cols,
        value_vars=year_cols,
        var_name="year_raw",
        value_name=indicator_name,
    )

    # Extract numeric year
    df_long["year"] = df_long["year_raw"].str.replace("YR", "").astype(int)
    df_long = df_long.drop(columns=["year_raw"])

    # Rename id columns for consistency
    rename_map = {}
    for c in id_cols:
        cl = c.lower()
        if cl in ("economy", "id", "countrycode"):
            rename_map[c] = "country_code"
        elif cl in ("name", "countryname", "country"):
            rename_map[c] = "country_name"
    df_long = df_long.rename(columns=rename_map)

    # Keep only relevant columns
    keep_cols = ["country_code", "country_name", "year", indicator_name]
    keep_cols = [c for c in keep_cols if c in df_long.columns]
    df_long = df_long[keep_cols]

    # Drop NaN values for the indicator
    df_long = df_long.dropna(subset=[indicator_name])

    indicator_frames[indicator_name] = df_long
    print(f"long shape = {df_long.shape}")

print()

# ============================================================
# 2. MERGE ALL INDICATORS INTO MASTER DATASET
# ============================================================
print("=" * 60)
print("2. Merging all indicators into master dataset")
print("=" * 60)

# Start with GDP per capita as the base
merge_keys = ["country_code", "year"]
if "country_name" in indicator_frames.get("gdp_per_capita", pd.DataFrame()).columns:
    merge_keys_with_name = ["country_code", "country_name", "year"]
else:
    merge_keys_with_name = merge_keys

master = indicator_frames["gdp_per_capita"].copy()
print(f"   Base (gdp_per_capita): {master.shape}")

for name, df in indicator_frames.items():
    if name == "gdp_per_capita":
        continue
    # Merge on country_code and year only
    df_merge = df.drop(columns=["country_name"], errors="ignore")
    master = master.merge(
        df_merge, on=["country_code", "year"], how="outer"
    )
    print(f"   + {name}: master now {master.shape}")

print()

# ============================================================
# 3. ADD COUNTRY METADATA (region, income level)
# ============================================================
print("=" * 60)
print("3. Adding country metadata (regions, income groups)")
print("=" * 60)

meta_path = os.path.join(DATA_RAW, "wb_country_metadata.csv")
meta = pd.read_csv(meta_path)
print(f"   Metadata shape: {meta.shape}")
print(f"   Metadata columns: {list(meta.columns)}")

# Filter to actual countries (not aggregates)
meta_countries = meta[meta["aggregate"] == False].copy()
print(f"   Countries (non-aggregate): {len(meta_countries)}")

# Merge region and income info
meta_slim = meta_countries[["id", "name", "region", "incomeLevel", "longitude", "latitude"]].copy()
meta_slim = meta_slim.rename(columns={
    "id": "country_code",
    "name": "country_name_meta",
    "region": "region",
    "incomeLevel": "income_level",
})

master = master.merge(meta_slim, on="country_code", how="left")
print(f"   Master after metadata merge: {master.shape}")

# Fill country_name from metadata where missing
if "country_name" in master.columns:
    master["country_name"] = master["country_name"].fillna(master["country_name_meta"])
else:
    master["country_name"] = master["country_name_meta"]
master = master.drop(columns=["country_name_meta"], errors="ignore")

print()

# ============================================================
# 4. ADD GAPMINDER CONTINENT MAPPING
# ============================================================
print("=" * 60)
print("4. Adding Gapminder continent/region mapping")
print("=" * 60)

gm_entities_path = os.path.join(DATA_RAW, "gm_entities.csv")
if os.path.exists(gm_entities_path):
    gm_ent = pd.read_csv(gm_entities_path, low_memory=False)
    print(f"   Gapminder entities: {gm_ent.shape}")
    print(f"   Columns: {list(gm_ent.columns)[:15]}...")

    # Map Gapminder four-region scheme
    if "world_4region" in gm_ent.columns:
        region_map = gm_ent[["country", "name", "world_4region", "world_6region"]].copy()
        region_map = region_map.rename(columns={
            "country": "geo_code",
            "name": "gm_country_name",
            "world_4region": "continent_4",
            "world_6region": "continent_6",
        })
        # Gapminder uses lowercase 3-letter codes, WB uses uppercase
        region_map["country_code"] = region_map["geo_code"].str.upper()
        master = master.merge(
            region_map[["country_code", "continent_4", "continent_6"]],
            on="country_code", how="left"
        )
        print(f"   Added continent_4 and continent_6 columns")
else:
    print("   Gapminder entities not found, skipping")

# Also use the gapminder classic for continent info
gm_classic = pd.read_csv(os.path.join(DATA_RAW, "gapminder_classic.csv"))
classic_continent = gm_classic[["country", "continent"]].drop_duplicates()
# We'll store this separately as a fallback mapping
classic_continent.to_csv(os.path.join(DATA_PROC, "continent_map_classic.csv"), index=False)
print(f"   Classic continent map: {len(classic_continent)} countries")

print()

# ============================================================
# 5. CLEAN AND FINALIZE
# ============================================================
print("=" * 60)
print("5. Cleaning and finalizing master dataset")
print("=" * 60)

# Remove aggregate economies (keep only countries)
agg_codes = meta[meta["aggregate"] == True]["id"].tolist()
before = len(master)
master = master[~master["country_code"].isin(agg_codes)]
print(f"   Removed {before - len(master)} aggregate rows")

# Sort
master = master.sort_values(["country_code", "year"]).reset_index(drop=True)

# Data type fixes
for col in ["longitude", "latitude"]:
    if col in master.columns:
        master[col] = pd.to_numeric(master[col], errors="coerce")

# Summary stats
print(f"\n   MASTER DATASET SUMMARY:")
print(f"   Shape: {master.shape}")
print(f"   Countries: {master['country_code'].nunique()}")
print(f"   Year range: {master['year'].min()} - {master['year'].max()}")
print(f"   Columns: {list(master.columns)}")
print(f"\n   Non-null counts per indicator:")
indicator_cols = [
    "gdp_per_capita", "life_expectancy", "population", "fertility_rate",
    "child_mortality", "birth_rate", "death_rate", "health_expenditure",
    "literacy_rate", "gini_index"
]
for col in indicator_cols:
    if col in master.columns:
        nn = master[col].notna().sum()
        pct = nn / len(master) * 100
        print(f"     {col:30s} {nn:7d} ({pct:5.1f}%)")

# Save master
master_path = os.path.join(DATA_PROC, "master_dataset.csv")
master.to_csv(master_path, index=False)
print(f"\n   Saved: {master_path}")
print(f"   Size: {os.path.getsize(master_path) / 1024 / 1024:.2f} MB")

# ============================================================
# 6. CREATE ROSLING-READY SUBSET (complete cases for key vars)
# ============================================================
print("\n" + "=" * 60)
print("6. Creating Rosling-ready subset (GDP, LifeExp, Pop, Region)")
print("=" * 60)

key_cols = ["gdp_per_capita", "life_expectancy", "population"]
rosling = master.dropna(subset=key_cols).copy()

# Assign a clean continent label using region or continent_4
def assign_continent(row):
    c4 = row.get("continent_4", None)
    if pd.notna(c4):
        mapping = {
            "africa": "Africa",
            "americas": "Americas",
            "asia": "Asia",
            "europe": "Europe",
        }
        return mapping.get(str(c4).lower(), str(c4))
    # Fallback to WB region
    reg = row.get("region", "")
    if pd.isna(reg):
        return "Other"
    reg = str(reg)
    if "Africa" in reg:
        return "Africa"
    elif "Europe" in reg or "Central Asia" in reg:
        return "Europe"
    elif "Latin" in reg or "Caribbean" in reg or "North America" in reg:
        return "Americas"
    elif "Asia" in reg or "Pacific" in reg:
        return "Asia"
    elif "Middle East" in reg:
        return "Asia"
    return "Other"

rosling["continent"] = rosling.apply(assign_continent, axis=1)

rosling_path = os.path.join(DATA_PROC, "rosling_ready.csv")
rosling.to_csv(rosling_path, index=False)

print(f"   Rosling-ready shape: {rosling.shape}")
print(f"   Countries: {rosling['country_code'].nunique()}")
print(f"   Year range: {rosling['year'].min()} - {rosling['year'].max()}")
print(f"   Continent distribution:")
print(rosling["continent"].value_counts().to_string(header=False))
print(f"\n   Saved: {rosling_path}")

print("\n" + "=" * 60)
print("PHASE 2 COMPLETE")
print("=" * 60)
