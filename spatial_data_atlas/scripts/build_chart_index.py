#!/usr/bin/env python3
"""
Build a comprehensive grouped index page for all charts in the atlas.
Groups by topic, with clear titles, descriptions, and bottomline spatial messages.
Also updates the main dashboard to link to this index and to the new quad-panel chart.
"""

# Each entry: (number, filename, title, description, bottomline, group)
CHARTS = [
    # === GLOBAL DEVELOPMENT DYNAMICS ===
    (1, "01_gdp_vs_life_expectancy.html", "GDP vs Life Expectancy",
     "Animated bubble chart showing the Preston Curve across 199 countries (1990-2023). Bubble size = population, color = continent.",
     "Richer countries live longer, but the relationship is logarithmic: the first $5,000 matters enormously; the next $50,000 barely moves the needle.",
     "Global Development Dynamics"),
    
    (2, "02_fertility_vs_life_expectancy.html", "Fertility vs Life Expectancy",
     "Animated bubble chart tracing the demographic transition: as life expectancy rises, fertility falls. 1990-2023.",
     "The world has converged dramatically: in 1990, fertility ranged from 1.2 to 7.5; by 2023, most countries cluster between 1.5 and 4.0.",
     "Global Development Dynamics"),
    
    (3, "03_child_mortality_vs_gdp.html", "Child Mortality vs GDP",
     "Animated scatter showing the inverse relationship between wealth and under-5 mortality. Log-scale GDP axis.",
     "Child mortality has halved globally since 1990, but the poorest countries still lose 10x more children than the richest.",
     "Global Development Dynamics"),
    
    (4, "04_country_trajectories.html", "Country Development Trajectories",
     "Spaghetti plot tracing individual country paths through GDP-health space over three decades.",
     "Most trajectories move right and up (richer and healthier), but conflict zones (Syria, Yemen) show dramatic reversals.",
     "Global Development Dynamics"),
    
    (5, "05_continental_trends.html", "Continental Development Trends",
     "Area/line chart comparing continental averages across key development indicators over time.",
     "Asia's rise is the dominant story: its average GDP per capita tripled in 30 years, driven by China and India.",
     "Global Development Dynamics"),
    
    (6, "06_income_distribution_shift.html", "Income Distribution Shift",
     "Animated histogram showing how the global income distribution has changed shape from 1990 to 2023.",
     "The bimodal 'twin peaks' distribution of 1990 (rich vs poor) has collapsed into a single peak centered at middle income.",
     "Global Development Dynamics"),

    # === ANIMATED TEMPORAL ===
    (49, "49_gdp_bar_race.html", "GDP Bar Chart Race",
     "Animated bar race showing the top 15 countries by GDP per capita (PPP) racing from 1992 to 2022.",
     "Ireland's meteoric rise is partly a statistical artifact of corporate tax haven effects; Qatar's lead reflects hydrocarbon wealth divided by a tiny citizen population.",
     "Animated Temporal"),
    
    (50, "50_india_electoral_swing.html", "India Electoral Swing Animation",
     "Animated map showing constituency-level electoral swings across Indian states, with victory margins evolving over time.",
     "Electoral swings are spatially clustered: neighboring constituencies tend to swing in the same direction, following regional political waves.",
     "Animated Temporal"),
    
    (51, "51_fertility_collapse.html", "Fertility Rate Collapse",
     "Animated chart showing the dramatic decline of fertility rates worldwide, with countries transitioning from high to low fertility.",
     "Bangladesh's fertility dropped from 6.2 to 2.0 in one generation without reaching high income, disproving the 'wealth causes low fertility' hypothesis.",
     "Animated Temporal"),
    
    (52, "52_mortality_plunge.html", "Child Mortality Plunge",
     "Animated visualization of the global decline in under-5 mortality rates from 1990 onward.",
     "Sub-Saharan Africa saw the steepest absolute declines after 2005, driven by anti-malaria bed nets and oral rehydration therapy.",
     "Animated Temporal"),
    
    (53, "53_convergence_race.html", "Economic Convergence Race",
     "Animated comparison showing whether poor countries are catching up to rich ones in GDP per capita.",
     "Conditional convergence is real (poor countries grow faster IF they have good institutions), but unconditional convergence remains elusive for the poorest.",
     "Animated Temporal"),
    
    (54, "54_women_lisa_fixed.html", "Women LISA Spatial Animation",
     "Animated Local Indicators of Spatial Association for women's candidature patterns across Indian constituencies.",
     "Spatial clustering of women's political exclusion is persistent: the same 'silence zones' appear year after year.",
     "Animated Temporal"),

    # === CORALS & OCEANS ===
    (7, "07_coral_bleaching_map.html", "Coral Bleaching Risk Map",
     "Choropleth map showing global coral reef bleaching severity, colored by thermal stress index.",
     "Bleaching severity follows equatorial SST anomalies, with the Coral Triangle (Indonesia, Philippines) most at risk due to narrow thermal tolerance.",
     "Corals & Oceans"),
    
    (8, "08_ocean_sst_anomaly.html", "Ocean SST Anomaly Map",
     "World map of sea surface temperature anomalies relative to long-term baseline.",
     "The spatial pattern of warming is not uniform: Arctic amplification is 2-3x the global average, and eastern boundary upwelling zones warm slower.",
     "Corals & Oceans"),
    
    (57, "57_coral_temporal_pulse.html", "Coral Bleaching Temporal Pulse",
     "Animated time series showing the pulse-like nature of mass bleaching events tied to El Nino cycles.",
     "The three global mass bleaching events (1998, 2010, 2015-16) all coincided with El Nino warm phases, but rising baseline SST makes each event worse.",
     "Corals & Oceans"),

    # === PEOPLE ===
    (9, "09_urbanization_choropleth.html", "Global Urbanization Rates",
     "Choropleth map of urban population percentage by country.",
     "Urbanization is the single strongest spatial predictor of development outcomes: countries over 60% urban almost universally have life expectancy above 70.",
     "People"),
    
    (10, "10_slum_population_map.html", "Slum Population Distribution",
     "Map showing the percentage of urban population living in slum conditions by country.",
     "90% of the world's slum dwellers live in three regions: sub-Saharan Africa, South Asia, and East Asia, revealing urbanization without adequate infrastructure.",
     "People"),
    
    (58, "58_animated_inequality.html", "Animated Global Inequality",
     "Animated visualization of the Gini coefficient evolution across countries over time.",
     "Latin America has been reducing inequality since 2000, while several Asian economies have seen rising inequality accompanying rapid growth.",
     "People"),

    # === POVERTY ===
    (11, "11_extreme_poverty_map.html", "Extreme Poverty ($2.15/day)",
     "Choropleth showing the percentage of population living below $2.15/day (2017 PPP).",
     "Extreme poverty has shifted from a global phenomenon (35% in 1990) to a geographically concentrated one: 70% of the extreme poor now live in sub-Saharan Africa.",
     "Poverty"),
    
    (12, "12_gini_inequality_map.html", "GINI Inequality Map",
     "World map colored by Gini coefficient, measuring income inequality within each country.",
     "South Africa (Gini ~63) and the Nordic countries (Gini ~25-28) represent the extremes: geography interacts with colonial history and institutional design.",
     "Poverty"),

    # === TECHNOLOGY ===
    (13, "13_internet_usage_choropleth.html", "Internet Penetration Rates",
     "Choropleth of internet users as percentage of population.",
     "The digital divide mirrors the development divide: sub-Saharan Africa averages 30% penetration vs 90%+ in Europe, creating a spatial information asymmetry.",
     "Technology"),
    
    (14, "14_electricity_access_map.html", "Electricity Access Map",
     "Map showing percentage of population with access to electricity.",
     "600 million Africans still lack electricity access; the spatial pattern follows the rural-urban divide more than the income divide.",
     "Technology"),
    
    (15, "15_mobile_subscriptions_map.html", "Mobile Phone Subscriptions",
     "Choropleth of mobile subscriptions per 100 people by country.",
     "Mobile leapfrogging: Africa skipped landlines entirely, and mobile money (M-Pesa in Kenya) demonstrates how technology diffusion follows spatial network effects.",
     "Technology"),

    # === MONEY & TRADE ===
    (16, "16_gdp_per_capita_map.html", "GDP per Capita World Map",
     "Choropleth of GDP per capita (PPP) across all countries.",
     "The North-South gradient is unmistakable: the 30 richest countries by GDP/capita are overwhelmingly in the Northern Hemisphere above 30 degrees latitude.",
     "Money & Trade"),
    
    (17, "17_trade_openness_map.html", "Trade Openness Index",
     "Map of trade openness (exports + imports as % of GDP) by country.",
     "Small countries and geographically central countries trade more; landlocked nations average 20% lower trade openness than coastal ones.",
     "Money & Trade"),
    
    (18, "18_remittances_map.html", "Remittances as % of GDP",
     "Choropleth showing how dependent each country's economy is on diaspora remittances.",
     "Tajikistan, Tonga, and Nepal receive 20-30% of GDP from remittances, revealing migration as a spatial economic strategy.",
     "Money & Trade"),

    # === ENVIRONMENT ===
    (19, "19_forest_cover_map.html", "Forest Cover Percentage",
     "World map of forest area as percentage of total land area.",
     "Deforestation follows the forest transition curve: poor countries lose forests (agriculture expansion), middle-income countries stabilize, and rich countries regain cover.",
     "Environment"),
    
    (20, "20_renewable_energy_map.html", "Renewable Energy Share",
     "Choropleth of renewable energy as percentage of total energy consumption.",
     "Geography determines renewable potential: Iceland (100% renewable from geothermal/hydro) vs Saudi Arabia (<1%): energy transition is a spatial problem.",
     "Environment"),
    
    (21, "21_water_stress_map.html", "Water Stress Index",
     "Map of water stress levels by country, from low to extremely high.",
     "Water stress follows latitude and aridity bands: the MENA region (Middle East & North Africa) has the highest stress, but rapidly urbanizing South Asia is catching up.",
     "Environment"),

    # === GEO-VARIABLE ANALYSIS ===
    (22, "22_bubble_map_gdp_health.html", "GDP-Health Bubble Map",
     "Proportional symbol map overlaying GDP and health outcomes on geographic coordinates.",
     "Spatial clustering of prosperity is visible at continental scale: European and East Asian clusters vs. African and South Asian low-GDP zones.",
     "Geo-Variable Analysis"),
    
    (23, "23_latitude_vs_gdp.html", "Latitude vs GDP per Capita",
     "Scatter plot testing the 'latitude hypothesis' (temperate climates produce richer economies).",
     "The correlation is r=0.45 for Northern Hemisphere but near zero for Southern Hemisphere, suggesting colonial history, not climate, drives the pattern.",
     "Geo-Variable Analysis"),
    
    (24, "24_megacity_distance_vs_lifeexp.html", "Distance from Megacity vs Life Expectancy",
     "Scatter plot of each country's distance from the nearest megacity vs. life expectancy.",
     "Countries far from megacities (Pacific islands, Central Africa) have lower life expectancy, supporting the 'proximity to urban knowledge centers' hypothesis.",
     "Geo-Variable Analysis"),
    
    (25, "25_latitude_vs_child_mortality.html", "Latitude vs Child Mortality",
     "Scatter showing how absolute latitude correlates with under-5 mortality.",
     "Tropical countries (0-15 degrees latitude) have 5x higher child mortality than temperate ones, but this reflects disease ecology and institutional history.",
     "Geo-Variable Analysis"),
    
    (26, "26_conflict_vs_development.html", "Conflict Intensity vs Development",
     "Scatter of armed conflict intensity vs. Human Development Index.",
     "Conflict is spatially contagious: countries neighboring conflict zones show 0.05-0.15 lower HDI, a geographic spillover effect.",
     "Geo-Variable Analysis"),
    
    (27, "27_landlocked_vs_coastal.html", "Landlocked vs Coastal Nations",
     "Box/bar comparison of development indicators between landlocked and coastal countries.",
     "Landlocked developing countries have 40% lower trade volumes and 0.1 lower HDI on average: geography as destiny through transport cost friction.",
     "Geo-Variable Analysis"),
    
    (28, "28_digital_divide_latitude.html", "Digital Divide by Latitude",
     "Scatter of internet penetration vs. latitude, testing geographic digital inequality.",
     "Internet access follows the same latitude gradient as GDP, but mobile leapfrogging is narrowing the gap faster than income convergence.",
     "Geo-Variable Analysis"),
    
    (29, "29_fertility_by_climate.html", "Fertility Rate by Climate Zone",
     "Scatter/box plot of total fertility rate grouped by Koppen climate classification.",
     "Tropical Af/Am climates average TFR of 4.2 vs. 1.6 for temperate Cfb climates; the link is indirect through urbanization, education, and agricultural mode.",
     "Geo-Variable Analysis"),
    
    (30, "30_urbanization_vs_renewable.html", "Urbanization vs Renewable Energy",
     "Scatter of urbanization rate vs. renewable energy share across countries.",
     "The relationship is non-linear: very rural countries use biomass (counted as 'renewable'), highly urban countries invest in solar/wind, mid-range countries use fossil fuels.",
     "Geo-Variable Analysis"),
    
    (31, "31_water_stress_latitude.html", "Water Stress by Latitude",
     "Scatter showing how water stress varies with latitude (proxy for aridity).",
     "The 20-35 degree latitude band (subtropical high-pressure zone) is the global water stress hotspot, aligning with the Hadley cell descending limb.",
     "Geo-Variable Analysis"),
    
    (32, "32_physicians_latitude.html", "Physicians per 1000 by Latitude",
     "Scatter of physician density vs. latitude across countries.",
     "Cuba (latitude 22) is a striking outlier with physician density rivaling Northern Europe, demonstrating that state policy can override geographic determinism.",
     "Geo-Variable Analysis"),
    
    (33, "33_education_megacity_distance.html", "Education vs Distance from Megacities",
     "Scatter exploring whether proximity to urban knowledge centers predicts education levels.",
     "Mean years of schooling drops by 0.8 years per 1000 km distance from the nearest megacity, reflecting knowledge diffusion decay with distance.",
     "Geo-Variable Analysis"),
    
    (34, "34_trade_longitude.html", "Trade Openness by Longitude",
     "Scatter of trade openness vs. longitude, testing whether East-West position affects trade integration.",
     "The 'Eurasian trade belt' (30-120 degrees East) shows highest openness, reflecting proximity to global shipping lanes and historical Silk Road connectivity.",
     "Geo-Variable Analysis"),
    
    (35, "35_maternal_mortality_forest.html", "Maternal Mortality vs Forest Cover",
     "Scatter testing the unexpected link between forest cover and maternal health outcomes.",
     "Dense forest cover correlates with higher maternal mortality (r=0.5), not because forests are harmful, but because they proxy for remoteness and poor road access.",
     "Geo-Variable Analysis"),
    
    (36, "36_remittances_latitude.html", "Remittances Dependency by Latitude",
     "Scatter of remittance-to-GDP ratio vs. latitude.",
     "The highest remittance dependency (20-30% of GDP) clusters at 10-30 degrees latitude, reflecting the migration corridor from tropics to temperate labor markets.",
     "Geo-Variable Analysis"),

    # === INDIA ELECTIONS 2024 ===
    (37, "37_india_lisa_clusters.html", "LISA Clusters (Voter Turnout)",
     "Local Indicators of Spatial Association map showing spatial clustering of voter turnout across 543 constituencies.",
     "Turnout Moran's I = 0.642: voter participation is highly spatially autocorrelated, with High-High clusters in the South and Low-Low clusters in parts of UP/Bihar.",
     "India Elections 2024"),
    
    (38, "38_india_area_outcomes.html", "Constituency Area vs Electoral Outcomes",
     "Scatter plot testing whether constituency size (km2) predicts victory margin or turnout.",
     "Larger constituencies have lower turnout (r = -0.3), suggesting that geographic spread creates barriers to electoral participation.",
     "India Elections 2024"),
    
    (39, "39_india_moran_scatterplot.html", "Moran Scatterplot (Spatial Autocorrelation)",
     "Classic Moran scatterplot with spatial lag on Y and original value on X, showing quadrant classification.",
     "The positive slope (I = 0.643) confirms strong spatial autocorrelation in turnout, rejecting the null hypothesis of spatial randomness at p < 0.001.",
     "India Elections 2024"),
    
    (40, "40_india_turnout_swing.html", "Turnout vs Swing Analysis",
     "Scatter of voter turnout vs. victory margin swing, exploring whether participation affects competitiveness.",
     "High-turnout constituencies tend to have narrower margins, suggesting mobilization of marginal voters in competitive seats.",
     "India Elections 2024"),
    
    (41, "41_india_distance_delhi_margin.html", "Distance from Delhi vs Victory Margin",
     "Scatter testing the 'Delhi distance' hypothesis: does distance from the capital predict electoral margin?",
     "There is a weak positive correlation: constituencies farther from Delhi tend to have higher margins, consistent with the 'incumbency gradient' model.",
     "India Elections 2024"),
    
    (46, "46_women_area_hypothesis.html", "Women Candidates vs Constituency Area",
     "Scatter testing whether larger (rural) constituencies field fewer women candidates.",
     "The relationship is negative but weak: constituency size is not the primary determinant of women's exclusion. Party gatekeeping matters more.",
     "India Elections 2024"),
    
    (48, "48_alliance_lisa_women.html", "Alliance LISA & Women Analysis",
     "Multi-panel analysis combining alliance-level LISA clustering with women's candidature spatial patterns.",
     "NDA and INDIA alliance dominance zones show distinct spatial signatures, and women's candidature clusters independently of alliance patterns.",
     "India Elections 2024"),
    
    (65, "65_silence_map.html", "The Silence Map (Zero Women Constituencies)",
     "Choropleth highlighting 152/543 constituencies (28%) where not a single woman contested the 2024 election.",
     "28% of Indian constituencies had zero women candidates: these 'silence zones' cluster in specific states (UP, Bihar, Maharashtra) revealing structural patriarchal exclusion.",
     "India Elections 2024"),
    
    (66, "66_the_gauntlet.html", "The Gauntlet (Women Candidate Funnel)",
     "Funnel chart tracing women's journey from candidature (458) through deposit retention (133) to victory (74).",
     "71% of women candidates lost their deposit (325/458), compared to ~55% for men: the electoral system is a filter that disproportionately eliminates women.",
     "India Elections 2024"),
    
    (67, "67_gender_gap_electorate.html", "Gender Gap in Electorate",
     "Bar and scatter analysis of the male-female voter gap across Indian states.",
     "Kerala has more female voters than male (1,084 per 1,000), while Bihar lags at 907: the gender gap in electoral participation is a spatial phenomenon.",
     "India Elections 2024"),
    
    (68, "68_deposit_forfeiture.html", "Deposit Forfeiture Analysis",
     "Scatter analyzing which factors predict whether women candidates lose their deposit (< 1/6 of votes).",
     "Women in reserved (SC/ST) constituencies are less likely to forfeit deposits, suggesting reservations provide a structural pathway.",
     "India Elections 2024"),
    
    (69, "69_state_scoreboard.html", "State Gender Scoreboard",
     "Heatmap ranking Indian states on multiple dimensions of women's political representation.",
     "No state scores high on all dimensions simultaneously: even 'progressive' states like Kerala excel on voter turnout but lag on candidature.",
     "India Elections 2024"),

    # === DELIMITATION & FISCAL ===
    (71, "71_delimitation_simulator.html", "Delimitation Seat Reallocation Simulator",
     "Interactive simulator showing how seat redistribution based on 2024 population would reshape Parliament (543 seats).",
     "Population-based delimitation would transfer ~80 seats from the South to UP/Bihar/MP, punishing states that controlled population growth.",
     "Delimitation & Fiscal"),
    
    (72, "72_fiscal_returns.html", "Fiscal Returns by State",
     "Scatter showing how much each state gets back per rupee contributed to the central exchequer.",
     "Southern states (Karnataka, Tamil Nadu) contribute more than they receive; northern states receive 2-3x what they contribute: a fiscal spatial transfer.",
     "Delimitation & Fiscal"),
    
    (73, "73_reservation_simulator.html", "Reservation Impact Simulator",
     "Interactive tool simulating how different reservation policies would change women's representation.",
     "A 33% women's reservation would guarantee 181 women MPs vs. the current 74: policy can override the structural barriers the Gauntlet chart reveals.",
     "Delimitation & Fiscal"),
    
    (74, "74_moran_criteria_explorer.html", "Multi-Criteria Moran Explorer",
     "Interactive tool allowing users to explore Moran's I for different variables (turnout, margin, women candidates).",
     "Turnout (I=0.642) is far more spatially autocorrelated than women's candidature (I=0.062), suggesting different spatial processes drive each.",
     "Delimitation & Fiscal"),
    
    (75, "75_punishment_value_3d.html", "Demographic Punishment Value (3D)",
     "3D surface showing the interaction between population growth rate, fertility rate, and seat reallocation impact.",
     "States that reduced TFR the most (Kerala, Tamil Nadu) face the largest seat losses under delimitation: a perverse spatial incentive.",
     "Delimitation & Fiscal"),
    
    (76, "76_representation_inequality.html", "Representation Inequality (Lorenz Curve)",
     "Lorenz curve and equality analysis for the distribution of parliamentary seats relative to population.",
     "The current frozen delimitation creates a representation Gini of ~0.15: some voters are worth 3x others in seat-to-population ratio.",
     "Delimitation & Fiscal"),
    
    (77, "77_fiscal_spine.html", "Fiscal Spine Chart",
     "Spine (diverging bar) chart comparing state contributions vs. receipts from the central fiscal pool.",
     "The 15th Finance Commission formula allocates 45% weight to population, directly linking fiscal transfers to the same spatial demographic patterns.",
     "Delimitation & Fiscal"),
    
    (78, "78_representation_treemap.html", "Representation Treemap",
     "Treemap showing seat allocation by state, sized by population and colored by seats-per-million ratio.",
     "Uttar Pradesh (80 seats for 240M people) vs Goa (2 seats for 1.5M): the per-capita representation varies 8-fold across India.",
     "Delimitation & Fiscal"),
    
    (79, "79_fiscal_gender_bubble.html", "Fiscal-Gender Nexus Bubble Chart",
     "Bubble chart overlaying fiscal dependency, women's candidature rate, and development index by state.",
     "States receiving the most fiscal transfers (Bihar, UP) are also those with the lowest women's candidature rates: fiscal and gender inequality are spatially co-located.",
     "Delimitation & Fiscal"),
    
    (80, "80_constituency_clustering.html", "Constituency Clustering (k-Means)",
     "k-Means clustering of 543 constituencies using turnout, margin, area, women candidates, and alliance data.",
     "Five natural clusters emerge: 'competitive urban', 'safe rural NDA', 'high-turnout South', 'low-participation mega-constituencies', and 'women-inclusive competitive'.",
     "Delimitation & Fiscal"),

    # === 3D IMMERSIVE ===
    (42, "42_india_political_cylinder.html", "India Political Cylinder (3D)",
     "Cylindrical 3D projection mapping constituencies onto a cylinder with height = turnout, color = winning party.",
     "The cylinder reveals vertical striations (party dominance bands) that are invisible in flat maps: geography and politics wrap around each other.",
     "3D Immersive Visualizations"),
    
    (43, "43_development_globe.html", "Development Globe (3D)",
     "Interactive 3D globe with countries extruded by GDP per capita and colored by life expectancy.",
     "Spinning the globe reveals the stark contrast between the 'Northern ridge' of prosperity and the 'Southern plain' of low GDP: the world is literally uneven.",
     "3D Immersive Visualizations"),
    
    (44, "44_democracy_helix.html", "Democracy-Development Double Helix (3D)",
     "3D helix tracing the co-evolution of democracy scores and development indicators across decades.",
     "Democracy and development spiral upward together but with significant lag: democratic transitions often precede economic growth by 5-10 years.",
     "3D Immersive Visualizations"),
    
    (45, "45_continental_dev_space.html", "Continental Development Hyperspace (3D)",
     "3D scatter plotting countries in GDP-health-education space, colored by continent.",
     "Continents form distinct clouds in 3D development space, with Africa and Europe as well-separated clusters and Asia spanning the entire range.",
     "3D Immersive Visualizations"),
    
    (47, "47_3d_extruded_india.html", "3D Extruded India Map",
     "India map with constituencies extruded by victory margin and colored by winning alliance.",
     "The NDA 'mountain range' across the Hindi belt vs. the INDIA alliance 'plateau' in the South creates a topographic metaphor for India's political geography.",
     "3D Immersive Visualizations"),
    
    (55, "55_india_party_flip_3d.html", "India Party Flip (3D)",
     "3D visualization showing constituencies that flipped between alliances, with height encoding margin change.",
     "Flip constituencies are geographically clustered at alliance boundary zones, not randomly distributed: spatial contagion in electoral change.",
     "3D Immersive Visualizations"),
    
    (56, "56_development_spiral.html", "Development Spiral (3D)",
     "3D spiral tracing the global development trajectory through GDP-health-time space.",
     "The spiral accelerates after 2000 (faster GDP growth) but shows a kink in 2020 (COVID): development is not a smooth upward path.",
     "3D Immersive Visualizations"),
    
    (59, "59_india_dev_terrain.html", "India Development Terrain (3D)",
     "3D terrain surface mapping Indian states by development indicators, creating a literal 'development landscape'.",
     "Kerala and Goa are 'peaks' while Bihar and Jharkhand are 'valleys': development in India has a physical topology.",
     "3D Immersive Visualizations"),
    
    (60, "60_india_food_geography_3d.html", "India Food Geography (3D)",
     "3D visualization of India's food production landscape, mapping crop yield and food security spatially.",
     "The Indo-Gangetic plain is India's food backbone, but the Green Revolution's spatial concentration created mono-cropping risks in Punjab/Haryana.",
     "3D Immersive Visualizations"),
    
    (61, "61_literacy_gender_helix.html", "Literacy-Gender Double Helix (3D)",
     "3D helix tracing the co-evolution of male and female literacy rates across Indian states.",
     "The gender literacy gap has narrowed from 25 to 14 percentage points since 2001, but spatial variation persists: 6 pts in Kerala vs 23 pts in Rajasthan.",
     "3D Immersive Visualizations"),
    
    (62, "62_constituency_aurora.html", "Constituency Aurora (3D)",
     "Artistic 3D aurora visualization of constituency-level data, mapping electoral energy as light patterns.",
     "The 'aurora' intensity reveals hidden patterns in electoral engagement that are lost in conventional cartographic representations.",
     "3D Immersive Visualizations"),
    
    (63, "63_india_socioeconomic_3d.html", "India Socioeconomic Landscape (3D)",
     "3D surface mapping multiple socioeconomic indicators across Indian states.",
     "The 3D surface reveals that GDP, education, and health do not perfectly covary: some states are 'ridges' on one dimension but 'valleys' on another.",
     "3D Immersive Visualizations"),
    
    (64, "64_gender_development_3d.html", "Gender-Development 3D Surface",
     "3D surface showing the interaction between gender indicators and development metrics across India.",
     "The surface has a 'gender plateau' where improvements in women's indicators plateau below a certain development threshold, suggesting structural barriers.",
     "3D Immersive Visualizations"),
    
    (70, "70_women_candidature_3d.html", "Women Candidature 3D Landscape",
     "3D visualization of women's political candidature patterns mapped onto India's geographic coordinates.",
     "The 3D landscape reveals that women's candidature is not uniformly low: it has spatial 'hotspots' (Kerala, West Bengal) surrounded by 'deserts' (UP, Bihar).",
     "3D Immersive Visualizations"),

    # === SYNCHRONIZED MULTI-PANEL ===
    (81, "81_quad_panel_sync.html", "Four Lenses: Synchronized Quad-Panel Animation",
     "Four different chart types (bubble, choropleth, stacked area, continental trajectory) showing four datasets animated by a single year slider (1990-2023).",
     "The synchronized view reveals that COVID-19 was a mortality shock visible in the bubble chart but invisible in the fertility map: different data structures tell different stories about the same event.",
     "Synchronized Multi-View"),
]

# Group them
from collections import OrderedDict
groups = OrderedDict()
for num, fname, title, desc, bottomline, group in CHARTS:
    if group not in groups:
        groups[group] = []
    groups[group].append((num, fname, title, desc, bottomline))

# Group icons/colors
GROUP_STYLE = {
    "Global Development Dynamics": ("#00D5E0", "globe-icon"),
    "Animated Temporal": ("#FF5872", "clock-icon"),
    "Corals & Oceans": ("#0099CC", "wave-icon"),
    "People": ("#B088F9", "people-icon"),
    "Poverty": ("#FF8C00", "coin-icon"),
    "Technology": ("#7CFC00", "bolt-icon"),
    "Money & Trade": ("#FFD700", "dollar-icon"),
    "Environment": ("#2ECC71", "leaf-icon"),
    "Geo-Variable Analysis": ("#00D5E0", "axes-icon"),
    "India Elections 2024": ("#FF5872", "vote-icon"),
    "Delimitation & Fiscal": ("#FFD700", "balance-icon"),
    "3D Immersive Visualizations": ("#B088F9", "cube-icon"),
    "Synchronized Multi-View": ("#00D5E0", "sync-icon"),
}

# Build HTML
cards_html = ""
for group_name, charts in groups.items():
    color = GROUP_STYLE.get(group_name, ("#00D5E0",))[0]
    cards_html += f"""
    <div class="group-section">
        <h2 class="group-title" style="border-color:{color}"><span class="group-dot" style="background:{color}"></span>{group_name} <span class="group-count">({len(charts)} charts)</span></h2>
        <div class="cards-grid">
    """
    for num, fname, title, desc, bottomline in charts:
        cards_html += f"""
        <a href="{fname}" class="card" style="--accent:{color}">
            <div class="card-num">#{num:02d}</div>
            <div class="card-title">{title}</div>
            <div class="card-desc">{desc}</div>
            <div class="card-bottom"><span class="bottom-label">Takeaway:</span> {bottomline}</div>
        </a>
        """
    cards_html += "</div></div>"

index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Complete Chart Index | Spatial Data Visualization Atlas</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@300;400;600;700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#080B13;color:#c0c8d4;font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif;overflow-x:hidden}}
.page-header{{text-align:center;padding:40px 20px 20px}}
.page-header h1{{font-family:'Playfair Display',Georgia,serif;color:#F0F4F8;font-size:2.2rem;margin-bottom:8px}}
.page-header p{{color:#7B8CA3;font-size:.95rem;max-width:800px;margin:0 auto}}
.stats-bar{{display:flex;justify-content:center;gap:30px;padding:14px 20px;margin-bottom:10px}}
.stat{{text-align:center}}
.stat-num{{font-family:'Playfair Display',Georgia,serif;color:#FFD700;font-size:1.8rem;font-weight:700}}
.stat-label{{color:#5a6a7a;font-size:.78rem;text-transform:uppercase;letter-spacing:.05em}}
.back-link{{text-align:center;margin-bottom:24px}}
.back-link a{{color:#00D5E0;text-decoration:none;font-size:.9rem;border:1px solid #1a2233;padding:6px 18px;border-radius:4px;transition:all .2s}}
.back-link a:hover{{background:#00D5E0;color:#080B13}}
.content{{max-width:1200px;margin:0 auto;padding:0 20px 60px}}
.group-section{{margin-bottom:36px}}
.group-title{{font-family:'Playfair Display',Georgia,serif;color:#F0F4F8;font-size:1.25rem;padding:10px 0 8px;margin-bottom:14px;border-bottom:2px solid;display:flex;align-items:center;gap:10px}}
.group-dot{{width:10px;height:10px;border-radius:50%;display:inline-block}}
.group-count{{color:#5a6a7a;font-size:.8rem;font-weight:400}}
.cards-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:12px}}
.card{{display:block;background:#0D1117;border:1px solid #1a2233;border-radius:8px;padding:16px 18px;text-decoration:none;transition:all .25s;border-left:3px solid var(--accent)}}
.card:hover{{background:#111822;border-color:var(--accent);transform:translateY(-2px);box-shadow:0 4px 20px rgba(0,0,0,.4)}}
.card-num{{color:var(--accent);font-size:.72rem;font-weight:700;font-family:'Playfair Display',Georgia,serif;margin-bottom:2px;opacity:.7}}
.card-title{{color:#F0F4F8;font-size:.95rem;font-weight:700;margin-bottom:6px;font-family:'Playfair Display',Georgia,serif}}
.card-desc{{color:#7B8CA3;font-size:.78rem;line-height:1.6;margin-bottom:8px}}
.card-bottom{{background:#0a0e16;border-radius:4px;padding:8px 10px;font-size:.76rem;line-height:1.5;color:#9aa8b8}}
.bottom-label{{color:var(--accent);font-weight:700;text-transform:uppercase;font-size:.68rem;letter-spacing:.03em}}
.search-bar{{text-align:center;margin-bottom:24px}}
.search-bar input{{background:#0D1117;border:1px solid #1a2233;color:#F0F4F8;padding:10px 20px;border-radius:6px;width:400px;max-width:80vw;font-size:.9rem;font-family:inherit}}
.search-bar input:focus{{outline:none;border-color:#00D5E0}}
@media(max-width:700px){{.cards-grid{{grid-template-columns:1fr}}.stats-bar{{flex-wrap:wrap;gap:16px}}}}
</style>
</head>
<body>
<div class="page-header">
<h1>Complete Chart Index</h1>
<p>Spatial &amp; Geographical Data Visualization Atlas, Lab for Spatial Informatics, IIIT Hyderabad. All {len(CHARTS)} visualizations grouped by topic.</p>
</div>
<div class="stats-bar">
<div class="stat"><div class="stat-num">{len(CHARTS)}</div><div class="stat-label">Charts</div></div>
<div class="stat"><div class="stat-num">{len(groups)}</div><div class="stat-label">Topic Groups</div></div>
<div class="stat"><div class="stat-num">199</div><div class="stat-label">Countries</div></div>
<div class="stat"><div class="stat-num">543</div><div class="stat-label">India Constituencies</div></div>
<div class="stat"><div class="stat-num">1990-2023</div><div class="stat-label">Time Span</div></div>
</div>
<div class="back-link"><a href="index.html">&larr; Back to Dashboard</a></div>
<div class="search-bar">
<input type="text" id="searchInput" placeholder="Search charts by title, topic, or keyword..." oninput="filterCards(this.value)">
</div>
<div class="content" id="content">
{cards_html}
</div>
<script>
function filterCards(q) {{
    q = q.toLowerCase().trim();
    document.querySelectorAll('.card').forEach(card => {{
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(q) ? '' : 'none';
    }});
    document.querySelectorAll('.group-section').forEach(section => {{
        const visibleCards = section.querySelectorAll('.card[style=""], .card:not([style])');
        let anyVisible = false;
        section.querySelectorAll('.card').forEach(c => {{
            if (c.style.display !== 'none') anyVisible = true;
        }});
        section.style.display = anyVisible ? '' : 'none';
    }});
}}
</script>
</body>
</html>"""

outpath = "/home/claude/rosling_project/visualizations/chart_index.html"
with open(outpath, "w") as f:
    f.write(index_html)
print(f"Written: {outpath} ({len(index_html)/1024:.1f} KB)")
print(f"Total charts indexed: {len(CHARTS)}")
print(f"Groups: {list(groups.keys())}")
