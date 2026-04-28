"""
Phase 1: Data Acquisition for Hans Rosling Gapminder Replication
================================================================
Downloads all core datasets from verified public sources:
  1. Gapminder Python package (classic 1704-row dataset)
  2. World Bank API via wbgapi (GDP, life expectancy, population, fertility, etc.)
  3. Gapminder GitHub CSV files (income groups, world regions)

Data Sources:
  - Gapminder: https://www.gapminder.org/data/
  - World Bank Open Data: https://data.worldbank.org/
  - Gapminder GitHub: https://github.com/open-numbers/ddf--gapminder--systema_globalis
"""

import os
import pandas as pd
import wbgapi as wb
from gapminder import gapminder
import json
import requests
import time

DATA_RAW = "/home/claude/rosling_project/data/raw"
DATA_PROC = "/home/claude/rosling_project/data/processed"
MANIFEST = {}

# ============================================================
# 1. GAPMINDER PYTHON PACKAGE (classic dataset)
# ============================================================
print("=" * 60)
print("1. Downloading Gapminder classic dataset (Python package)")
print("=" * 60)

gm = gapminder.copy()
print(f"   Shape: {gm.shape}")
print(f"   Columns: {list(gm.columns)}")
print(f"   Countries: {gm['country'].nunique()}")
print(f"   Year range: {gm['year'].min()} to {gm['year'].max()}")
gm.to_csv(os.path.join(DATA_RAW, "gapminder_classic.csv"), index=False)
MANIFEST["gapminder_classic"] = {
    "source": "gapminder Python package (v0.1)",
    "url": "https://pypi.org/project/gapminder/",
    "original_source": "https://www.gapminder.org/data/",
    "rows": len(gm),
    "columns": list(gm.columns),
    "year_range": [int(gm['year'].min()), int(gm['year'].max())],
    "countries": int(gm['country'].nunique()),
}
print("   Saved: gapminder_classic.csv\n")

# ============================================================
# 2. WORLD BANK INDICATORS via wbgapi
# ============================================================
print("=" * 60)
print("2. Downloading World Bank indicators via wbgapi")
print("=" * 60)

# Key indicators used in Rosling's presentations
WB_INDICATORS = {
    "NY.GDP.PCAP.PP.KD": {
        "name": "gdp_per_capita_ppp",
        "description": "GDP per capita, PPP (constant 2017 international $)",
        "wb_page": "https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD",
    },
    "SP.DYN.LE00.IN": {
        "name": "life_expectancy",
        "description": "Life expectancy at birth, total (years)",
        "wb_page": "https://data.worldbank.org/indicator/SP.DYN.LE00.IN",
    },
    "SP.POP.TOTL": {
        "name": "population",
        "description": "Population, total",
        "wb_page": "https://data.worldbank.org/indicator/SP.POP.TOTL",
    },
    "SP.DYN.TFRT.IN": {
        "name": "fertility_rate",
        "description": "Fertility rate, total (births per woman)",
        "wb_page": "https://data.worldbank.org/indicator/SP.DYN.TFRT.IN",
    },
    "SH.DYN.MORT": {
        "name": "child_mortality",
        "description": "Mortality rate, under-5 (per 1,000 live births)",
        "wb_page": "https://data.worldbank.org/indicator/SH.DYN.MORT",
    },
    "EN.ATM.CO2E.PC": {
        "name": "co2_per_capita",
        "description": "CO2 emissions (metric tons per capita)",
        "wb_page": "https://data.worldbank.org/indicator/EN.ATM.CO2E.PC",
    },
    "SI.POV.GINI": {
        "name": "gini_index",
        "description": "Gini index (World Bank estimate)",
        "wb_page": "https://data.worldbank.org/indicator/SI.POV.GINI",
    },
    "SE.ADT.LITR.ZS": {
        "name": "literacy_rate",
        "description": "Literacy rate, adult total (% of people ages 15 and above)",
        "wb_page": "https://data.worldbank.org/indicator/SE.ADT.LITR.ZS",
    },
    "SH.XPD.CHEX.PC.CD": {
        "name": "health_expenditure_pc",
        "description": "Current health expenditure per capita (current US$)",
        "wb_page": "https://data.worldbank.org/indicator/SH.XPD.CHEX.PC.CD",
    },
    "SP.DYN.CBRT.IN": {
        "name": "birth_rate",
        "description": "Birth rate, crude (per 1,000 people)",
        "wb_page": "https://data.worldbank.org/indicator/SP.DYN.CBRT.IN",
    },
    "SP.DYN.CDRT.IN": {
        "name": "death_rate",
        "description": "Death rate, crude (per 1,000 people)",
        "wb_page": "https://data.worldbank.org/indicator/SP.DYN.CDRT.IN",
    },
    "NY.GDP.MKTP.KD.ZG": {
        "name": "gdp_growth",
        "description": "GDP growth (annual %)",
        "wb_page": "https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG",
    },
}

YEAR_RANGE = range(1960, 2024)

for code, info in WB_INDICATORS.items():
    name = info["name"]
    print(f"   Fetching: {name} ({code})...", end=" ")
    try:
        df = wb.data.DataFrame(code, time=YEAR_RANGE, labels=True, columns="time")
        # Reset index to get country info as columns
        df = df.reset_index()
        fname = f"wb_{name}.csv"
        df.to_csv(os.path.join(DATA_RAW, fname), index=False)
        print(f"OK  shape={df.shape}")
        MANIFEST[f"wb_{name}"] = {
            "source": "World Bank Open Data via wbgapi",
            "indicator_code": code,
            "description": info["description"],
            "url": info["wb_page"],
            "api_url": f"https://api.worldbank.org/v2/country/all/indicator/{code}",
            "rows": len(df),
            "year_range": [1960, 2023],
        }
    except Exception as e:
        print(f"FAILED: {e}")
    time.sleep(0.5)  # Be polite to the API

print()

# ============================================================
# 3. WORLD BANK COUNTRY METADATA (regions, income groups)
# ============================================================
print("=" * 60)
print("3. Downloading World Bank country metadata")
print("=" * 60)

try:
    economies = wb.economy.DataFrame()
    economies = economies.reset_index()
    economies.to_csv(os.path.join(DATA_RAW, "wb_country_metadata.csv"), index=False)
    print(f"   Country metadata: {economies.shape}")
    print(f"   Columns: {list(economies.columns)}")
    MANIFEST["wb_country_metadata"] = {
        "source": "World Bank economy metadata via wbgapi",
        "url": "https://data.worldbank.org/country",
        "rows": len(economies),
        "columns": list(economies.columns),
    }
except Exception as e:
    print(f"   FAILED: {e}")

# Also get region definitions
try:
    regions = wb.region.DataFrame()
    regions = regions.reset_index()
    regions.to_csv(os.path.join(DATA_RAW, "wb_regions.csv"), index=False)
    print(f"   Regions: {regions.shape}")
    MANIFEST["wb_regions"] = {
        "source": "World Bank region definitions via wbgapi",
        "url": "https://data.worldbank.org/",
        "rows": len(regions),
    }
except Exception as e:
    print(f"   FAILED: {e}")

# Income level definitions
try:
    incomes = wb.income.DataFrame()
    incomes = incomes.reset_index()
    incomes.to_csv(os.path.join(DATA_RAW, "wb_income_levels.csv"), index=False)
    print(f"   Income levels: {incomes.shape}")
    MANIFEST["wb_income_levels"] = {
        "source": "World Bank income level definitions via wbgapi",
        "url": "https://data.worldbank.org/",
        "rows": len(incomes),
    }
except Exception as e:
    print(f"   FAILED: {e}")

print()

# ============================================================
# 4. GAPMINDER DIRECT DOWNLOADS (supplementary data)
# ============================================================
print("=" * 60)
print("4. Downloading supplementary Gapminder CSVs from GitHub")
print("=" * 60)

GAPMINDER_GITHUB_CSVS = {
    "gm_population": {
        "url": "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--systema_globalis/master/countries-etc-datapoints/ddf--datapoints--population_total--by--geo--time.csv",
        "description": "Gapminder population totals by country and year",
    },
    "gm_life_expectancy": {
        "url": "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--systema_globalis/master/countries-etc-datapoints/ddf--datapoints--life_expectancy_years--by--geo--time.csv",
        "description": "Gapminder life expectancy by country and year",
    },
    "gm_income_per_person": {
        "url": "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--systema_globalis/master/countries-etc-datapoints/ddf--datapoints--income_per_person_gdppercapita_ppp_inflation_adjusted--by--geo--time.csv",
        "description": "Gapminder GDP per capita PPP (inflation adjusted) by country and year",
    },
    "gm_entities": {
        "url": "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--systema_globalis/master/ddf--entities--geo--country.csv",
        "description": "Gapminder country entities with region and income group mappings",
    },
}

for name, info in GAPMINDER_GITHUB_CSVS.items():
    print(f"   Fetching: {name}...", end=" ")
    try:
        r = requests.get(info["url"], timeout=30)
        r.raise_for_status()
        fname = f"{name}.csv"
        fpath = os.path.join(DATA_RAW, fname)
        with open(fpath, "wb") as f:
            f.write(r.content)
        df_check = pd.read_csv(fpath)
        print(f"OK  shape={df_check.shape}")
        MANIFEST[name] = {
            "source": "Gapminder Systema Globalis (GitHub)",
            "url": info["url"],
            "repo": "https://github.com/open-numbers/ddf--gapminder--systema_globalis",
            "description": info["description"],
            "rows": len(df_check),
            "columns": list(df_check.columns),
        }
    except Exception as e:
        print(f"FAILED: {e}")
    time.sleep(0.3)

print()

# ============================================================
# 5. SAVE MANIFEST
# ============================================================
print("=" * 60)
print("5. Saving data manifest")
print("=" * 60)

manifest_path = os.path.join(DATA_RAW, "data_manifest.json")
with open(manifest_path, "w") as f:
    json.dump(MANIFEST, f, indent=2)

print(f"   Manifest saved with {len(MANIFEST)} dataset entries")
print(f"   Location: {manifest_path}")

# Summary
print("\n" + "=" * 60)
print("PHASE 1 COMPLETE: Data Acquisition Summary")
print("=" * 60)
raw_files = os.listdir(DATA_RAW)
print(f"   Total files downloaded: {len(raw_files)}")
for f in sorted(raw_files):
    fpath = os.path.join(DATA_RAW, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"   {f:45s} {size_kb:8.1f} KB")
