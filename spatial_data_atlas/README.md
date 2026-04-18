# Spatial & Geographical Data Visualization Atlas

## Quick Start

```bash
# Option 1: Run the server
./run_atlas.sh
# Opens at http://localhost:8000

# Option 2: Specify a port
./run_atlas.sh 3000

# Option 3: Just open the file directly
open visualizations/index.html
```

## Contents

- **89 interactive charts** (75 Plotly.js + 9 Three.js + 5 new Three.js WebGL)
- **14 thematic tabs**: Global Development, Animated Temporal, Corals & Oceans, People, Poverty, Technology, Money & Trade, Environment, Geo-Variables, India Elections, Delimitation & Fiscal, 3D Immersive, Synchronized, Spatial Deep Dive
- **Guided tour** (20 stops): `guided_tour.html`
- **Chart index**: `chart_index.html`
- **Sitemap**: `sitemap.html`

## New Charts (85-89): Spatial Deep Dive

| # | Name | Engine | Description |
|---|---|---|---|
| 85 | Moran Eruption Plane | Three.js WebGL | 512 constituencies as 3D columns above/below I=0 cutting plane. Smoke particles. Variable dropdowns. |
| 86 | Women's Field of Silence | Three.js WebGL | Women's exclusion as 3D tower field. Red = zero women (119 PCs). Gold = woman won. I = 0.113. |
| 87 | Delimitation Freeze | Three.js WebGL | Paired 3D bars: current vs proportional seats. 53-year distortion. Fiscal returns. |
| 88 | Electoral Terrain | Three.js WebGL | Turnout as 3D landscape. Red peaks (HH), blue valleys (LL). Mean plane at 65.8%. |
| 89 | Women's Gauntlet | Three.js WebGL | Three-tier pipeline: contested, retained, elected. Falling attrition particles. |

## Data Sources

- Election Commission of India (2024, 2019)
- World Bank Open Data (1990-2023)
- Gapminder Foundation
- NOAA ERSST v5, Coral Reef Watch
- DataMeet (GeoJSON boundaries)
- Census of India 2011
- RBI Handbook of Statistics

## Spatial Methods

- Moran's I (Global): PySAL esda.moran.Moran
- LISA (Local): PySAL esda.moran.Moran_Local
- Spatial Weights: PySAL libpysal.weights.KNN (k=8)
- 999 permutations, alpha = 0.05

## Authors

Vishakha Agrawal, Malini Krishnan
Lab for Spatial Informatics, IIIT Hyderabad
Advisors: Kuldeep Kurte, K.S. Rajan
