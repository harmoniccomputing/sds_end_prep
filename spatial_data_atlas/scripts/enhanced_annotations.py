#!/usr/bin/env python3
"""Enhanced interpretation panels for all 80 charts with deep policy analysis."""
import os, re, json

VIZ_DIR = "visualizations"

PANEL_CSS = '''<style>
.interp-toggle{position:fixed;bottom:16px;right:16px;z-index:9999;background:#00D5E0;color:#06080F;border:none;
width:44px;height:44px;border-radius:50%;font-size:1.3rem;cursor:pointer;box-shadow:0 2px 12px rgba(0,213,224,.4);
display:flex;align-items:center;justify-content:center;font-weight:700;transition:transform .2s}
.interp-toggle:hover{transform:scale(1.1)}
.interp-panel{position:fixed;bottom:70px;right:16px;z-index:9998;width:460px;max-height:75vh;overflow-y:auto;
background:rgba(13,17,23,.97);border:1px solid #21293A;border-radius:12px;padding:22px 24px;
color:#E0E0E0;font-family:'Source Sans 3',system-ui,sans-serif;font-size:.8rem;line-height:1.65;
box-shadow:0 8px 32px rgba(0,0,0,.5);display:none;backdrop-filter:blur(8px)}
.interp-panel.show{display:block;animation:fadeUp .3s ease-out}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.interp-panel h3{color:#00D5E0;font-size:1.05rem;margin:0 0 10px;font-weight:700;border-bottom:1px solid #21293A;padding-bottom:8px}
.interp-panel h4{color:#FF5872;font-size:.82rem;margin:14px 0 5px;font-weight:700;letter-spacing:.02em}
.interp-panel p{margin:0 0 8px;color:#B0BEC5}
.interp-panel .box{background:#161B26;border-left:3px solid #00D5E0;padding:10px 14px;margin:8px 0;border-radius:0 6px 6px 0}
.interp-panel .box.warn{border-left-color:#FF5872}
.interp-panel .box.gold{border-left-color:#FFD700}
.interp-panel .metric{display:inline-block;background:#1C2333;padding:2px 8px;border-radius:4px;color:#00D5E0;font-weight:600;font-size:.75rem;margin:1px 2px}
.interp-panel .label-list{margin:6px 0;padding-left:0}
.interp-panel .label-item{margin:4px 0;padding:4px 0 4px 12px;border-left:2px solid #2D3748}
.interp-panel .label-item b{color:#FFD700}
@media(max-width:600px){.interp-panel{width:calc(100vw - 32px);right:16px;font-size:.75rem}}
</style>'''

PANEL_JS = '''<script>
(function(){var b=document.createElement('button');b.className='interp-toggle';b.innerHTML='?';
b.title='Interpretation guide';b.onclick=function(){var p=document.getElementById('interp-panel');
p.classList.toggle('show');b.innerHTML=p.classList.contains('show')?'\\u2715':'?'};
document.body.appendChild(b)})();
</script>'''

# Load all annotations from JSON to keep the script manageable
ANNOTATIONS = {}

# I'll define them inline but structured
def A(num, title, sections):
    ANNOTATIONS[num] = {"title": title, "sections": sections}

# Helper to build section HTML
def build_html(ann):
    h = f'<h3>{ann["title"]}</h3>'
    for sec in ann["sections"]:
        h += f'<h4>{sec["heading"]}</h4>'
        if sec.get("box"):
            cls = "box " + sec.get("box_type", "")
            h += f'<div class="{cls.strip()}">{sec["content"]}</div>'
        else:
            h += f'<p>{sec["content"]}</p>'
    return h

# ---- CHART 01-06: GLOBAL DEVELOPMENT ----
A("01","Wealth vs Health of Nations",[
{"heading":"What This Chart Shows","content":"Each bubble represents one country. The <span class='metric'>X-axis</span> shows GDP per capita in PPP dollars on a logarithmic scale (each gridline represents a 10x increase in income). The <span class='metric'>Y-axis</span> shows life expectancy at birth in years. <span class='metric'>Bubble size</span> encodes total population. <span class='metric'>Color</span> distinguishes continents. The <span class='metric'>animation slider</span> steps through years 1990 to 2023."},
{"heading":"Understanding the Labels","content":"<div class='label-list'><div class='label-item'><b>GDP per Capita (PPP $)</b>: Total economic output divided by population, adjusted for local purchasing power. A value of $10,000 means a person could buy goods equivalent to $10,000 in the United States. The log scale is used because the relationship between income and health is logarithmic: the first $5,000 of income buys far more life expectancy than going from $50,000 to $55,000.</div><div class='label-item'><b>Life Expectancy</b>: The average number of years a newborn is expected to live under current mortality conditions. Values below 60 indicate severe health crises. Above 80 is typical of wealthy nations.</div><div class='label-item'><b>Population (bubble size)</b>: Larger bubbles = more people affected by that country's conditions.</div></div>"},
{"heading":"Interpreting the Trends","box":True,"content":"The strong upward curve confirms the <b>Preston Curve</b> (1975): national income strongly predicts population health, but with diminishing returns. Moving from $1,000 to $5,000 GDP adds roughly 15 years of life expectancy. Moving from $50,000 to $100,000 adds perhaps 1-2 years. This flattening means that beyond a threshold, <b>health policy and social infrastructure matter more than raw wealth</b>."},
{"heading":"What Movement Means","content":"When a bubble moves <b>rightward</b> over time, the country is getting richer. <b>Upward</b> movement means improving health. The ideal trajectory is upper-right. Countries moving <b>leftward</b> (rare) are experiencing economic contraction. Countries moving <b>downward</b> (very rare: HIV-era Botswana, conflict zones) are experiencing health catastrophes."},
{"heading":"Policy Implications","box":True,"box_type":"warn","content":"For countries in the steep part of the curve ($1K-$10K), <b>economic growth is the most powerful health intervention</b>. For countries on the flat part (>$30K), further GDP growth yields minimal health gains; <b>targeted healthcare investment, inequality reduction, and public health infrastructure</b> become more cost-effective. Sub-Saharan African nations clustered in the bottom-left face a compounding trap: poor health reduces economic productivity, which perpetuates poor health."},
])

A("02","Fertility vs Longevity",[
{"heading":"What This Chart Shows","content":"Countries plotted on <span class='metric'>fertility rate</span> (births per woman, X-axis) vs <span class='metric'>life expectancy</span> (Y-axis), animated over time 1990-2023."},
{"heading":"Understanding the Variables","content":"<div class='label-list'><div class='label-item'><b>Fertility Rate</b>: The average number of children a woman would bear over her lifetime at current age-specific birth rates. Values above 2.1 mean population growth (above replacement). Below 2.1 means eventual population decline without immigration.</div><div class='label-item'><b>Replacement level (2.1)</b>: The fertility rate at which a population exactly replaces itself. The 0.1 above 2.0 accounts for child mortality.</div></div>"},
{"heading":"Interpreting the Trends","box":True,"content":"The global pattern shows the <b>Demographic Transition</b>: societies move from high fertility + low life expectancy (upper-left) to low fertility + high life expectancy (lower-right). This transition is driven by: (1) declining child mortality (parents need fewer births to ensure surviving children), (2) women's education and workforce participation, (3) access to contraception, (4) urbanization (children become economic costs rather than assets). By 2023, most of the world has completed or is mid-transition. <b>Sub-Saharan Africa is the final frontier</b>."},
{"heading":"Policy Implications","box":True,"box_type":"warn","content":"Countries still in the upper-left face a <b>youth bulge</b>: large young populations needing education, jobs, and services. If harnessed (investing in education and job creation), this becomes a <b>demographic dividend</b> that accelerates growth. If neglected, it becomes a source of instability. Countries in the lower-right face <b>aging populations</b>: rising dependency ratios, pension pressure, and potential labor shortages. Japan (fertility 1.2) and South Korea (0.7) represent the extreme of this challenge."},
])

A("03","Child Mortality vs Wealth",[
{"heading":"What This Chart Shows","content":"<span class='metric'>Under-5 mortality rate</span> (deaths per 1,000 live births, Y-axis) vs <span class='metric'>GDP per capita</span> (PPP $, log X-axis), animated 1990-2023."},
{"heading":"Understanding the Variables","content":"<div class='label-list'><div class='label-item'><b>Under-5 Mortality</b>: The probability that a newborn will die before reaching age 5, expressed per 1,000 live births. A value of 100 means 1 in 10 children dies. Below 10 is the norm in wealthy nations.</div><div class='label-item'><b>The log scale on GDP</b>: Compresses the wealth axis so that both $500 and $50,000 countries are visible. This is essential because the poorest countries have the most to gain from analysis.</div></div>"},
{"heading":"Interpreting the Trends","box":True,"content":"The global mortality decline is one of humanity's greatest achievements. In 1990, many countries exceeded 200 per 1,000 (1 in 5 children died). By 2023, no country exceeds 120. The decline was driven by: <b>oral rehydration therapy</b> (treating diarrhea), <b>vaccination campaigns</b> (measles, polio), <b>insecticide-treated bed nets</b> (malaria), and <b>improved nutrition</b>. The animation shows this decline accelerating post-2000, coinciding with the Millennium Development Goals."},
{"heading":"Policy Implications","box":True,"box_type":"warn","content":"The steep negative slope means <b>every dollar of GDP growth in poor countries translates to children's lives saved</b>. But the curve is not destiny: countries like Bangladesh and Rwanda achieve mortality rates far below what their GDP would predict, proving that <b>targeted public health investment can override economic constraints</b>. Policymakers in high-mortality countries should prioritize primary healthcare, clean water, and childhood vaccination over expensive tertiary care."},
])

# I'll generate simplified but still rich annotations for charts 04-80
# to keep within size limits while covering all requirements

SIMPLIFIED = {
"04": ("Country Trajectory Traces",
"14 key nations traced on GDP vs life expectancy over decades.",
"Each line is one country's development path. <b>Rightward</b> = getting richer. <b>Upward</b> = healthier. <b>Dips</b> indicate crises: Botswana's HIV dip (1990s), Rwanda's genocide (1994).",
"<b>GDP per Capita (PPP)</b>: economic output per person. <b>Life Expectancy</b>: years at birth. Traces show temporal direction of development.",
"China shows the most dramatic rightward leap (economic liberalization). Countries with HIV epidemics show downward loops before recovery. <b>Policy lesson</b>: development is not monotonic; crises can reverse decades of progress. Health system resilience determines recovery speed."),

"05": ("Continental Trends",
"Three panels: GDP, life expectancy, and fertility by continent over time, population-weighted.",
"<b>Population weighting</b> means each line reflects what the average person on that continent experiences, not the average country. This makes China and India dominate Asian averages.",
"<b>Convergence</b>: when lines come together over time (health is converging). <b>Divergence</b>: when lines spread apart (wealth is diverging). <b>Policy lesson</b>: global health interventions are succeeding, but economic growth remains unequally distributed. Africa needs both continued health investment and economic development strategies.",
"Life expectancy convergence means health interventions (vaccines, primary care) are the most globally equitable force in development. GDP divergence means the market alone will not close the wealth gap."),

"06": ("Income Distribution Shift",
"Population-weighted income distribution showing the shift from bimodal (two humps) to unimodal (one hump) over 1995-2020.",
"The <b>bimodal pattern</b> (two peaks) represented Rosling's 'developed vs developing' world. Its disappearance proves his thesis: there is no longer a binary division. The merge is driven by China and India pulling ~2.5 billion people into middle income.",
"<b>X-axis (log income)</b>: each gridline is a 10x increase. <b>Area under curve</b>: proportional to population at that income level. <b>Policy lesson</b>: global poverty reduction is real but incomplete. The remaining left tail (extreme poor) is increasingly concentrated in Sub-Saharan Africa and conflict zones.",
""),

"07": ("Reef Bleaching Hotspots",
"27 major reef systems on a dark ocean map. Size = area. Color = threat level (Critical/High/Medium/Low).",
"<b>Threat levels</b>: Critical = reef has lost >50% coral cover. High = significant recent bleaching. Medium = some stress. Low = relatively intact. Thermal stress from warming oceans causes coral to expel symbiotic algae (bleaching).",
"<b>Size</b> encodes reef area in km2. <b>Color</b>: red = critical, orange = high, yellow = medium, green = low. <b>Policy implications</b>: Marine Protected Areas (MPAs) can reduce local stressors (pollution, overfishing) but cannot prevent thermal bleaching from global warming. The Paris Agreement's 1.5C target is effectively a reef survival threshold; exceeding it means losing most tropical reefs by 2050.",
""),

"08": ("Ocean SST Anomaly",
"Global sea surface temperature anomaly 1980-2024 with mass bleaching events annotated.",
"<b>SST Anomaly</b>: deviation from the 1971-2000 baseline average. Positive values = warmer than historical normal. The upward trend is unambiguous: the baseline itself is rising. Annotated events (1998, 2010, 2016, 2024) mark mass coral bleaching.",
"The tightening interval between crises (18 years, then 12, then 6, then 8) shows <b>accelerating frequency</b>. <b>Policy implications</b>: reef management must shift from 'protect and recover' to 'adapt and triage'. Some reefs will not survive; resources should focus on the most genetically resilient populations.",
""),

"09": ("Urbanization (Animated)",
"Animated world choropleth of urban population % from 1990 to 2022. Darker color = more urbanized.",
"<b>Urban population %</b>: fraction of total population living in areas classified as urban by national statistical offices. Increasing values mean people are moving from rural to urban areas. China went from ~26% to ~64% in this period.",
"<b>Policy implications</b>: rapid urbanization without infrastructure investment leads to slums, pollution, and inequality. Countries entering the 30-50% urban range (current Africa) face a critical window: invest now in transit, housing, and sanitation, or lock in decades of informal settlement.",
""),

"10": ("Slum Population",
"Choropleth of % urban population in slums.",
"<b>Slum</b> (UN-Habitat definition): housing lacking one or more of: durable structure, sufficient living area, access to improved water, access to improved sanitation, security of tenure. Values above 50% mean most urban residents lack basic housing.",
"Sub-Saharan Africa and South Asia bear the highest burden. <b>Policy implications</b>: slum upgrading programs (providing water, sanitation, land tenure to existing settlements) are far more cost-effective than demolition and relocation. Nairobi, Mumbai, and Lagos demonstrate both successful upgrading and failed eviction approaches.",
""),

"11": ("Extreme Poverty ($1.90/day)",
"Choropleth of population below the international poverty line ($1.90/day PPP).",
"<b>$1.90/day (PPP)</b>: the World Bank's extreme poverty line, representing the minimum needed for basic survival. This is adjusted for local purchasing power. Values above 40% mean nearly half the population cannot afford basic food and shelter.",
"The geographic concentration in Sub-Saharan Africa and parts of South Asia reflects the compound effect of conflict, governance failures, geographic disadvantage, and disease burden. <b>Policy implications</b>: targeted cash transfer programs, agricultural investment, and conflict resolution are the three most effective poverty reduction tools in these contexts.",
""),

"12": ("Gini Inequality",
"Choropleth of the Gini coefficient (0 = perfect equality, 100 = one person has everything).",
"<b>Gini coefficient</b>: measures income distribution. Calculated as the ratio of the area between the Lorenz curve and the line of equality to the total area under the line of equality. A Gini of 30 (Scandinavia) means relatively equal distribution. A Gini of 60+ (South Africa, Brazil) means extreme concentration of wealth.",
"<b>Increasing Gini</b> = growing inequality (the rich getting disproportionately richer). <b>Decreasing Gini</b> = more equal distribution. <b>Policy implications</b>: high inequality correlates with social instability, lower trust, and worse health outcomes (Wilkinson & Pickett, 2009). Progressive taxation, universal education, and social safety nets are the primary tools for Gini reduction.",
""),
}

# Build the remaining charts with shorter but still comprehensive annotations
# Charts 13-36, 37-48, 49-58, 59-64, 65-80

REMAINING = {
"13":("Internet (Animated)","Animated choropleth of internet users %, 2000-2022.","<b>Internet users %</b>: individuals who accessed the internet in the last 3 months. Rising values = digital inclusion. The spread was North-to-South, rich-to-poor. <b>Policy</b>: digital literacy programs and infrastructure investment (fiber, mobile towers) in underserved areas yield outsized returns in education, healthcare access, and economic participation."),
"14":("Electricity Access","Choropleth of % population with electricity.","<b>Electricity access</b>: % of population with a connection. Sub-Saharan Africa has the lowest rates. <b>Policy</b>: off-grid solar systems can leapfrog centralized grids in remote areas. Energy poverty directly limits education (no light for studying), healthcare (no refrigeration for vaccines), and economic activity."),
"15":("Mobile Subscriptions","Choropleth of mobile subscriptions per 100 people.","Values >100 mean people have multiple SIM cards (common with competing networks). Mobile is the most equitably distributed technology globally. <b>Policy</b>: mobile money (M-Pesa model) and mobile health platforms can deliver financial and health services to unbanked and underserved populations."),
"16":("GDP per Capita","Choropleth of GDP per capita in PPP dollars.","<b>PPP adjustment</b> accounts for local price differences. $1,000 in India buys more than $1,000 in Switzerland. <b>Policy</b>: GDP per capita is the most commonly used proxy for standard of living but misses inequality, environmental degradation, and unpaid labor."),
"17":("Trade Openness","Choropleth of trade (exports+imports) as % of GDP.","High values indicate trade-dependent economies. Small wealthy nations (Singapore >300%) are entrepot economies. Large economies (US ~25%) have lower ratios despite massive absolute trade. <b>Policy</b>: trade openness correlates with growth but also vulnerability to global shocks."),
"18":("Remittances","Choropleth of remittances as % of GDP.","<b>Remittances</b>: money sent home by workers abroad. High dependency (>20% of GDP) indicates structural reliance on migration. <b>Policy</b>: remittances are a vital lifeline but create dependency. Investing remittance flows into productive local assets (not just consumption) is key to long-term development."),
"19":("Forest Cover","Choropleth of forest area as % of land.","Forest cover affects carbon sequestration, biodiversity, and local rainfall. Declining cover = deforestation. <b>Policy</b>: REDD+ programs pay countries to preserve forests. The Amazon and Congo basins are globally significant carbon sinks whose loss would accelerate climate change."),
"20":("Renewable Energy","Choropleth of renewable energy % of consumption.","High values in poor countries often reflect <b>traditional biomass</b> (wood, charcoal) not modern renewables. In rich countries, high values indicate wind/solar/hydro investment. <b>Policy</b>: the distinction between 'good' renewables (modern, clean) and 'bad' renewables (biomass causing deforestation and indoor air pollution) is critical."),
"21":("Freshwater Stress","Choropleth of water withdrawals as % of renewable resources. >100% = unsustainable.","Values >100% mean the country is extracting <b>fossil groundwater</b> that does not replenish. The 20-35 degree latitude band (subtropical deserts) faces the worst stress. <b>Policy</b>: water pricing, drip irrigation, desalination, and wastewater recycling are the primary tools. Countries like Israel demonstrate that technology can overcome natural scarcity."),
"22":("Nations Bubble Map","Countries as bubbles at their geographic coordinates. Size = population.","A geographic population density proxy. <b>Policy</b>: the spatial distribution of humanity shows where infrastructure investment affects the most people. Asia's concentration means interventions there have the highest population-weighted impact."),
"23":("Latitude-Wealth Gradient","GDP (log) vs absolute latitude.","Tests the <b>geography hypothesis</b> (Sachs 2001): tropical countries are systematically poorer due to disease burden, agricultural productivity, and historical colonization patterns. <b>Policy</b>: if geography is destiny, tropical nations need compensating investment in healthcare, infrastructure, and institutions."),
"24":("Megacity Distance vs Life Expectancy","Distance to nearest megacity (>10M) vs life expectancy.","Tests the <b>connectivity premium</b>: proximity to economic hubs correlates with better health. Remote countries lack access to trade, medical supply chains, and knowledge transfer. <b>Policy</b>: transportation infrastructure and telemedicine can reduce the isolation penalty."),
"25":("Climate vs Child Mortality","Under-5 mortality vs latitude by climate zone.","Tropical countries face higher mortality due to malaria, diarrheal diseases, and lower agricultural productivity. <b>Policy</b>: climate-specific health interventions (bed nets for malaria zones, oral rehydration for hot climates) can break the climate-mortality link."),
"26":("Cost of Conflict","Conflict intensity vs GDP and life expectancy.","<b>UCDP conflict intensity</b> (0-10): standardized measure of armed violence. Even moderate conflict (3-5) is associated with 10-15 years lower life expectancy. <b>Policy</b>: conflict prevention and resolution yield enormous development dividends. Every dollar spent on peacekeeping saves an estimated $10-16 in post-conflict reconstruction."),
"27":("Sea Access Premium","GDP distributions: landlocked vs coastal by continent.","<b>Landlocked</b> countries face higher transport costs (15-20% of export value vs 5-8% for coastal). <b>Policy</b>: regional transit agreements, railway investment, and customs harmonization can reduce the landlocked penalty. Botswana demonstrates that good governance can partially overcome geographic disadvantage."),
"28":("Digital-Geographic Divide","Internet usage vs latitude, colored by income.","The digital divide parallels the development gradient but income group explains most variance. <b>Policy</b>: universal broadband policies should target the intersection of low latitude and low income for maximum impact."),
"29":("Fertility by Climate Zone","Fertility distributions across 4 climate zones.","Tropical zones show the widest distribution and highest median. <b>Policy</b>: the fertility-climate link operates through women's education, healthcare access, and agricultural livelihoods, all of which can be intervened upon regardless of climate."),
"30":("Urbanization vs Renewables","Urban % vs renewable energy share.","A counterintuitive negative relationship. Highly urbanized = more fossil fuel dependent (grid electricity). Rural = more biomass (counted as 'renewable'). <b>Policy</b>: urban clean energy transitions require grid-scale solar and wind investment, not biomass."),
"31":("Arid Belt Water Stress","Water withdrawals vs latitude.","The 20-35 degree band concentrates water stress. <b>Policy</b>: agricultural water efficiency (drip irrigation can reduce water use by 30-50%), water recycling, and demand management are more sustainable than supply-side solutions (dams, desalination)."),
"32":("Healthcare by Latitude","Physicians per 1,000 vs latitude.","Fewer doctors near the equator reflects both brain drain (physicians emigrate to wealthy countries) and training capacity gaps. <b>Policy</b>: community health worker programs, telemedicine, and retention bonuses for rural physicians can partially compensate for shortages."),
"33":("Education vs Connectivity","Primary completion vs distance to megacity.","Remote countries have lower school completion. <b>Policy</b>: distance learning, mobile education platforms, and teacher incentive programs for remote postings can reduce the isolation penalty."),
"34":("Trade East-West","Trade openness vs longitude.","Peaks at 0-30E (Europe) and 100-120E (East Asia) reflect the two major trade blocs. <b>Policy</b>: countries between these peaks (Central Asia, Middle East) can leverage their position as trade corridors."),
"35":("Forest vs Maternal Health","Maternal mortality vs forest cover.","High forest cover often means rural remoteness and poor healthcare access. <b>Policy</b>: forested countries need skilled birth attendants and emergency obstetric care in remote areas. The environmental-health tradeoff demands targeted, not one-size-fits-all, solutions."),
"36":("Remittance Geography","Remittances vs latitude.","Low-latitude countries depend most on remittances, reflecting South-to-North migration. <b>Policy</b>: reducing remittance transfer costs (currently 5-10%) would immediately increase family incomes in recipient countries. The World Bank target is 3%."),
"37":("LISA Cluster Map","LISA analysis of turnout and margin across 543 constituencies. <b>Moran's I</b> measures spatial autocorrelation: the tendency for nearby areas to have similar values. I=0 means random. I>0 means clustering. I<0 means dispersion. Turnout I=0.64 indicates <b>very strong</b> spatial clustering.","<b>LISA</b> (Local Indicators of Spatial Association, Anselin 1995) decomposes the global Moran's I into per-location contributions. <b>Hot Spots (HH)</b>: high turnout near high turnout (red). <b>Cold Spots (LL)</b>: low turnout near low turnout (blue). <b>Outliers (HL/LH)</b>: a high-turnout constituency surrounded by low-turnout neighbors. <b>Computed using</b>: KNN k=8 spatial weights, row-standardized, 999 conditional permutations for significance at p<0.05.","<b>Policy</b>: Cold spots (UP/Bihar) need voter mobilization infrastructure: more polling stations, voter awareness campaigns, transportation to remote booths. Hot spots (Kerala/Tamil Nadu) demonstrate that political culture and civic engagement can be cultivated. The spatial pattern suggests that voter engagement is <b>contagious</b>: neighboring constituencies influence each other."),
"38":("Area vs Outcomes","Constituency area (log km2) vs turnout and margin. <b>Log transformation</b> is used because area spans 4 orders of magnitude (29 km2 to 180,000 km2). Without log, small urban seats would be invisible.","A <b>negative slope</b> for area vs turnout means larger constituencies have lower voter participation. This is intuitive: voters in Ladakh (180K km2) face far greater logistical barriers than voters in urban Mumbai. <b>Policy</b>: larger constituencies need more polling stations per voter, mobile polling booths, and postal ballot facilitation. The trendline slope quantifies the 'size penalty' on democratic participation."),
"39":("Moran's I Scatterplot","<b>Moran's I Scatterplot</b>: X-axis = standardized value (how far a constituency deviates from the mean). Y-axis = spatial lag (the average of its neighbors' values). The <b>slope of the gold regression line = Moran's I</b>. <b>Four quadrants</b>: HH (top-right, both high), LL (bottom-left, both low), HL (bottom-right, outlier high among low), LH (top-left, outlier low among high).","Points in HH/LL quadrants indicate <b>spatial clustering</b>: the constituency and its neighbors are similar. Points in HL/LH are <b>spatial outliers</b>: the constituency differs from its neighborhood. <b>Policy</b>: outlier constituencies are interesting because they suggest local factors (a charismatic candidate, a local issue) can override regional trends."),
"40":("Turnout Swing","Change in voter turnout between 2019 and 2024. <b>Red</b> = turnout dropped (voter disengagement). <b>Blue</b> = turnout rose (increased participation). National average: -1.4 percentage points.","<b>Negative swing</b> = fewer voters participated in 2024 than 2019 in that constituency. This could indicate voter fatigue, anti-incumbency apathy, or logistical barriers. <b>Positive swing</b> = mobilization succeeded. <b>Policy</b>: constituencies with large negative swings need investigation: was it weather, security issues, voter suppression, or genuine disaffection? Targeted Get-Out-The-Vote campaigns should focus on these areas."),
"41":("Center vs Periphery","Margin vs distance from Delhi (degrees). Tests Rokkan's (1970) <b>core-periphery model</b>: whether the political center (Delhi) exerts systematic influence on electoral outcomes.","No strong linear relationship, but <b>variance changes</b>: near Delhi, margins range widely (safe NDA seats and competitive ones); far from Delhi, the distribution is more uniform. <b>Policy</b>: the lack of a strong distance effect is actually good news: it means Indian democracy is not simply radiating outward from a single center."),
"42":("Political Cylinder (3D)","543 constituencies on a rotating cylinder. <b>Latitude maps to height</b> (south at bottom, north at top). <b>Longitude maps to angle</b>. <b>Color = alliance</b>. This is a <b>cylindrical projection</b> that unrolls India's geography onto a 3D surface.","The cylinder reveals the North-South political divide more dramatically than a flat map. The lower half (south) is predominantly blue (INDIA alliance). The upper half (north) is predominantly saffron (NDA). <b>Policy</b>: India's political geography is fundamentally spatial. Any party seeking national power must bridge this divide."),
"43":("Development Globe (3D)","Countries as bars on a rotating sphere. <b>Bar height = selected metric</b>. Three switchable metrics via buttons. <b>Policy</b>: the globe perspective shows that development challenges cluster geographically: Sub-Saharan Africa's bars are consistently shortest for GDP and life expectancy, tallest for fertility."),
"44":("Double Helix (3D)","NDA and INDIA alliance constituencies spiral in a DNA-like double helix. <b>Node size = victory margin</b>. The metaphor: India's democracy has two intertwined strands of political identity, geographically encoded.","<b>Policy</b>: the helix structure suggests that India's political divide is not a clean line but an interwoven structure. States in the middle turns (Maharashtra, Karnataka) are genuinely contested."),
"45":("Continental Development Space (3D)","196 countries in 3D: <b>X = GDP (log)</b>, <b>Y = Life Expectancy</b>, <b>Z = Fertility</b>. Three variables shown simultaneously without information loss from 2D projection.","Africa (cyan) clusters in the high-Z (high fertility), low-X (low GDP), low-Y (low life expectancy) corner. Europe (green) occupies the opposite corner. <b>Policy</b>: the 3D view reveals that countries breaking the expected pattern (Gulf states: high GDP, moderate life expectancy, low fertility) have distinctive policy environments worth studying."),
"46":("Women + Area Hypothesis","Three panels testing whether women win in larger or smaller constituencies. <b>Mann-Whitney U test</b>: a non-parametric test comparing two distributions without assuming normality. If p < 0.05, the distributions are significantly different.","Women win in slightly <b>smaller, denser</b> constituencies (median 3,324 vs 4,073 km2). <b>Policy</b>: women's campaigns may benefit from constituency-level characteristics (urban, higher media access, shorter travel distances). Parties nominating women should consider geographic favorability."),
"47":("3D Spatial Histogram","3D bars over India's footprint. <b>Height = selected metric</b> (electorate ratio, turnout, or margin). This is the 'spatial histogram' concept: superimposing quantitative data onto geographic space.","<b>Policy</b>: in electorate ratio mode, the dramatic North-South inequality is immediately visible. Northern constituencies have 2x the national average electorate, meaning votes there are worth half as much. This is the core delimitation argument."),
"48":("Alliance LISA + Women","Left: LISA on NDA/INDIA alignment (I=0.37). Right: state bubble chart of NDA share vs women %. <b>NDA coded as +1, INDIA as -1</b>. LISA identifies where these alignments cluster spatially.","110 NDA strongholds and 112 INDIA strongholds identified at p<0.05. <b>Key finding</b>: women's representation does NOT correlate with alliance dominance. Both NDA and INDIA strongholds have similarly poor women's representation. <b>Policy</b>: women's reservation cannot be left to partisan goodwill; it requires structural mandates like the 33% Reservation Bill."),
"49":("GDP Bar Chart Race","Top 15 nations by GDP per capita racing 1992-2022. <b>Press play</b> to watch countries overtake each other.","Ireland's dramatic rise reflects corporate tax haven status (GDP is inflated by multinational profits booked there). Qatar and Singapore reflect resource/trade wealth concentrated in tiny populations. <b>Policy</b>: per-capita GDP rankings can be misleading. Median household income is a better welfare measure."),
"50":("Electoral Swing 2019 vs 2024","Animated geo scatter toggling between elections. <b>Bubbles morph</b> as margins and positions change.","<b>Policy</b>: constituencies where margins swung by >10 points deserve investigation. Were swings driven by candidate quality, anti-incumbency, alliance realignment, or structural demographic shifts?"),
"51":("Fertility Collapse","Year-by-year animation 1990-2023 of fertility vs life expectancy. 33 frames showing the entire world converging.","This is the single most important demographic chart of our era. <b>Policy</b>: the remaining high-fertility countries (mostly West/Central Africa) will contribute most of humanity's future population growth. Investment in girls' education in these countries is the single most effective intervention for global demographic transition."),
"52":("Mortality Plunge","Animated choropleth of under-5 mortality 1990-2022.","Watch Sub-Saharan Africa gradually lighten. <b>Policy</b>: the acceleration post-2000 (MDG era) proves that coordinated international development goals work. The SDG era must continue this momentum."),
"53":("Continental Convergence","Life expectancy converging (left), GDP diverging (right).","<b>Convergence</b> = lines coming together. <b>Divergence</b> = lines spreading apart. <b>Policy</b>: health convergence proves that targeted interventions (vaccines, primary care) can overcome economic inequality. GDP divergence proves that market forces alone will not equalize wealth."),
"54":("Women's LISA","LISA on women winners (I=0.06). Right: area vs density scatter.","Weak but significant clustering (I=0.06, p<0.001) means women winners are <b>slightly</b> more likely to cluster spatially than random. <b>Policy</b>: parties could strategically nominate women in clusters where adjacent constituencies have elected women, leveraging the 'neighborhood effect'."),
"55":("Party Flip Pulse (3D)","214 flipped constituencies pulse with golden rings. <b>Pulsing animation</b> = sinusoidal scale oscillation to draw attention to change.","<b>Policy</b>: flipped seats represent the most dynamic part of Indian democracy. Understanding what drove flips (anti-incumbency, alliance changes, candidate factors) informs campaign strategy."),
"56":("Development Spiral (3D)","Countries trace spiral paths through time. <b>Radius = log(GDP)</b>. <b>Height = life expectancy</b>. Slider scrubs through years.","The spiral is a spacetime trajectory. Countries that spiral outward and upward are developing. Countries that spiral inward or downward are regressing. <b>Policy</b>: the slider reveals when each country's development accelerated or stalled, correlating with specific policy eras."),
"57":("Coral Temporal Pulse","Reef map (top) + SST timeline (bottom). Dual-zone visualization linking cause (warming) and effect (bleaching).","The tightening interval between mass bleaching events (18, 12, 6, 8 years) shows <b>accelerating frequency</b>. <b>Policy</b>: the Paris Agreement's 1.5C target is effectively a reef survival threshold. Current trajectories (2.5-3C by 2100) mean losing 70-90% of tropical reefs."),
"58":("Animated Inequality","Gini coefficient animated by 5-year bins 1990-2020.","<b>Policy</b>: Latin America's declining Gini reflects successful conditional cash transfer programs (Bolsa Familia, Oportunidades). China's rising Gini reflects the inequality cost of rapid market-driven growth. Policy choices, not just economic forces, determine inequality trajectories."),
"59":("India Development Terrain (3D)","30 states as pillars. 8 switchable metrics. <b>Width = state area</b>. <b>Color gradient</b>: red (low) to green (high).","Switching metrics reveals that <b>no state excels on all dimensions</b>. Kerala leads in HDI and sex ratio but not GSDP. Gujarat leads in GSDP but not HDI. <b>Policy</b>: balanced development requires investment across all dimensions simultaneously, not just GDP growth."),
"60":("India Food Geography 3D","Rice (green) and wheat (gold) in 3D. <b>Height = production in million tonnes</b>.","The sharp rice-wheat divide follows the monsoon boundary. <b>Policy</b>: food security planning must account for this spatial specialization. Climate change threatens wheat in Punjab (heat stress) and rice in Bengal (sea level rise). Crop diversification is an insurance policy."),
"61":("Literacy-Gender Helix (3D)","Two helical strands: literacy (cyan) vs sex ratio (magenta), ordered by HDI.","Where strands align (Kerala: both bulge), education and gender equity reinforce each other. Where they diverge (Haryana: literacy OK, sex ratio terrible), there is a structural problem. <b>Policy</b>: Haryana's mismatch proves that education alone does not guarantee gender equity. Deep cultural interventions (against sex-selective practices) are required."),
"62":("Constituency Aurora (3D)","543 particles breathing with turnout, glowing with margin. Alliance-colored.","The breathing animation encodes democratic <b>vitality</b>: high-amplitude oscillation = high turnout = engaged electorate. Low amplitude = disengaged. <b>Policy</b>: the aurora metaphor makes democratic health feel organic and alive, not abstract."),
"63":("India Socioeconomic 3D","X=Literacy, Y=GSDP, Z=HDI. <b>Drop lines</b> to the HDI floor show each state's 'height' above minimum.","The 3D scatter reveals that literacy, GSDP, and HDI are positively correlated but <b>not identical</b>. Delhi has high GSDP but moderate HDI (inequality reduces the average). <b>Policy</b>: HDI is a better welfare measure than GSDP because it incorporates health and education."),
"64":("Gender-Development Nexus 3D","X=Sex Ratio, Y=IMR (reversed: lower=better=higher), Z=Literacy. <b>Color = sex ratio</b> (red=dangerous, green=healthy).","<b>Reversed Y-axis</b> makes 'up = better' intuitive for IMR. Kerala sits at the ideal corner (green, high, right). <b>Policy</b>: states in the red zone (Haryana, Punjab, Delhi) need enforcement of the PCPNDT Act (Pre-Conception and Pre-Natal Diagnostic Techniques Act) against sex-selective abortion, plus cultural change programs."),
"65":("The Silence Map","152 constituencies (28%) with zero women candidates, marked with red X.","<b>Policy</b>: the clustering of zero-women constituencies in the Hindi heartland reflects party gatekeeping (parties do not nominate women), social barriers (women face violence and intimidation when running), and structural factors (larger, rural constituencies with conservative social norms). The Women's Reservation Bill (33%) would force parties to nominate women in these very seats."),
"66":("The Gauntlet","Funnel chart: 8,360 candidates to 458 women to 133 deposit-saved to 47 winners.","<b>Deposit forfeiture</b>: candidates who receive less than 1/6 of total votes lose their security deposit. 71% of women candidates forfeited. This suggests many women are fielded as token candidates by fringe parties with no real campaign support. <b>Policy</b>: parties must provide genuine campaign infrastructure (funding, media, organization) to women candidates, not just symbolic nominations."),
"67":("Gender Gap in Electorate","Female voters per 1,000 male. <b>Parity = 1000</b>. Green = above parity. Red = below.","Bihar (907) has 93 fewer women registered per 1,000 men. This means ~4 million women are 'missing' from Bihar's voter rolls. <b>Policy</b>: voter registration drives targeting women, especially in states below 950, could add millions of women to the democratic process. Mobile registration units and women's self-help group partnerships are effective."),
"68":("Deposit Forfeiture Massacre","Every woman candidate as a dot. 325 red (forfeited), 86 gold (lost, kept deposit), 47 green (won).","The red wall of 325 dots is the story. Most forfeited women got <2% of votes, indicating they were not competitive. <b>Policy</b>: the data suggests that most women run without real party backing. A 'candidate quality' intervention (training, funding, mentorship for women candidates) would likely move dots from red to gold, and some from gold to green."),
"69":("State Scoreboard","Three panels: women elected, forfeit rate, gender ratio.","14 states elected zero women. Kerala elected zero women despite having the best gender ratio (1,084). This paradox means that voter registration parity does NOT automatically translate to women winning. The pipeline breaks at the <b>nomination stage</b> (parties not selecting women), not the voting stage. <b>Policy</b>: mandatory party-level quotas for women candidates are more effective than voter-level interventions."),
"70":("Women Candidature 3D","Height = % women candidates. Red X on floor = zero women.","The 3D terrain makes the sparsity tangible: most of India is a flat red desert with occasional green peaks. <b>Policy</b>: the spatial pattern suggests that women's candidature is not randomly distributed but concentrated in specific socio-geographic niches (urban, southern, educated). Breaking out of these niches requires party-level structural reform."),
"71":("Delimitation Simulator","Slider 543 to 1000 seats. <b>Webster method</b>: proportional allocation where each state gets seats proportional to its population, with remainders allocated to states with the largest fractional entitlement.","<b>Gold diagonal = no change</b>. Points above = states gaining seats. Points below = states losing. Southern states (red dots) consistently fall below because they controlled population growth. <b>Policy</b>: the delimitation debate is zero-sum. Increasing total seats (to 700 or 1000) reduces but does not eliminate the proportional shift away from the South. An alternative: weight criteria (area, literacy, fiscal contribution) alongside population."),
"72":("Fiscal Returns","For every Rs 100 in tax, how much does each state get back. <b>Gold line = break-even</b> (Rs 100).","Tamil Nadu gets Rs 29.7 (net contributor of Rs 70.3 per Rs 100). Bihar gets Rs 142.5 (net recipient of Rs 42.5). <b>Policy</b>: the 15th Finance Commission formula weights: population (15%), area (15%), forest cover (10%), demographic performance (12.5%), income distance (45%), tax effort (2.5%). Southern states argue that demographic performance (low fertility) should have higher weight, rewarding population control."),
"73":("Reservation Simulator","Slider 0-100% women's reservation.","At 33% (the actual bill): ~180 guaranteed women seats. Current reality: 47 seats (8.7%). The gap between 47 and 180 quantifies the structural deficit. <b>Policy</b>: reservation is the only proven mechanism for rapid representation increase. Gradual 'cultural change' approaches have produced only marginal improvement over 75 years of Indian democracy."),
"74":("Moran Criteria Explorer","Two curves showing how Moran's I changes as the weight between two delimitation criteria shifts. <b>Lower I = more equitable dispersion</b>. <b>Negative I = anti-clustering (ideal)</b>.","If using only area for seat allocation, Moran's I is higher (more clustering, less fair). Population-based allocation is slightly more equitable. Using fiscal returns or women voter percentages as criteria produces different I values. <b>Policy</b>: the optimal delimitation formula minimizes spatial clustering (approaches I=0 or negative), ensuring that no geographic region is systematically over or underrepresented."),
"75":("Punishment Value (3D)","<b>Punishment value formula</b>: 1 - 0.35 x (fiscal return / 100). If a state gets Rs 29.7 back, its punishment value is 1 - 0.35 x 0.297 = 0.896 (severely punished). If it gets Rs 142.5, the value is 1 - 0.35 x 1.425 = 0.501 (mildly punished). If it gets Rs 510, the value is negative (net beneficiary).","Tamil Nadu (0.90) and Maharashtra (0.90) face the worst triple burden: high taxes, low fiscal return, AND seat losses under delimitation. <b>Policy</b>: the 35% factor in the formula represents the estimated women's share of tax contribution. Earmarking this fraction for women's welfare programs in contributor states would partially compensate for the fiscal penalty."),
"76":("Representation Inequality","Electors per seat (millions) by state. Slider 543 to 1000. <b>Perfect equity = all bars the same height</b>.","At 543: UP has ~2.4M voters per seat, Sikkim has ~0.4M. A vote in Sikkim is worth <b>6 times</b> a vote in UP. This is the most fundamental democratic inequality in India. <b>Policy</b>: increasing total seats toward 1000 reduces inequality because proportional allocation converges toward equal representation. The question is political: who benefits and who loses."),
"77":("Fiscal Spine","States connected south-to-north. Size = seats. Color = fiscal return.","The spine traces India's fiscal gradient: red (contributors) at the southern end, green (recipients) at the northern end. <b>Policy</b>: the spatial autocorrelation in fiscal inequality mirrors the political divide. Southern contributor states vote INDIA alliance; northern recipient states vote NDA. Fiscal federalism is thus inseparable from electoral geography."),
"78":("Treemap","Region > State. Area = seats. Color = fiscal return.","Central and East regions (green, large rectangles) receive the most fiscal transfers AND have the most seats. Southern region (red, smaller rectangles) pays the most AND has fewer seats. <b>Policy</b>: the treemap visualizes the 'double whammy': fiscal penalty + representational penalty. Addressing either without the other leaves the structural imbalance intact."),
"79":("Fiscal-Gender Bubble","Fiscal return vs women % with reservation slider.","As reservation increases (drag slider), all bubbles rise uniformly. But the X-axis spread (fiscal return) does NOT change. <b>Key insight</b>: reservation fixes the gender gap but does NOT fix the fiscal gap. The two problems require separate policy interventions."),
"80":("Constituency Clustering","Every constituency color-coded by % women candidates.","Red zones cluster in central UP, rural Bihar, and parts of Rajasthan. Green pockets in urban/southern areas. <b>Policy</b>: the clustering confirms that women's exclusion is not random but geographically patterned. Interventions (party quotas, campaign funding, safety infrastructure) should be spatially targeted at the red zones."),
}

# Build annotations for charts 04-80
for num, data in SIMPLIFIED.items():
    if len(data) == 5:
        title, show, trends, labels, policy = data
        A(num, title, [
            {"heading":"What This Chart Shows","content":show},
            {"heading":"Understanding the Labels and Metrics","content":labels},
            {"heading":"Interpreting the Trends","box":True,"content":trends},
            {"heading":"Policy Implications","box":True,"box_type":"warn","content":policy},
        ])
    elif len(data) == 4:
        title, show, labels, policy = data
        A(num, title, [
            {"heading":"What This Chart Shows","content":show},
            {"heading":"Understanding the Labels and Metrics","content":labels},
            {"heading":"Policy Implications","box":True,"box_type":"warn","content":policy},
        ])

for num, data in REMAINING.items():
    if len(data) == 3:
        title, content1, content2 = data
        A(num, title, [
            {"heading":"What This Shows and How to Read It","content":content1},
            {"heading":"Interpretation, Trends, and Policy","box":True,"content":content2},
        ])
    elif len(data) == 4:
        title, content1, content2, content3 = data
        secs = [{"heading":"What This Shows","content":content1},
                {"heading":"Labels, Metrics, and Calculations","content":content2}]
        if content3:
            secs.append({"heading":"Interpretation and Policy","box":True,"content":content3})
        A(num, title, secs)

# Inject into all charts
def inject_panel(filepath, annotation):
    with open(filepath, "r") as f:
        html = f.read()
    if "interp-panel" in html:
        return False
    
    panel_html = '<div id="interp-panel" class="interp-panel">'
    panel_html += build_html(annotation)
    panel_html += '</div>'
    
    injection = PANEL_CSS + panel_html + PANEL_JS
    if "</body>" in html:
        html = html.replace("</body>", injection + "\n</body>")
    else:
        html += injection
    
    with open(filepath, "w") as f:
        f.write(html)
    return True

count = 0
for filename in sorted(os.listdir(VIZ_DIR)):
    if not filename.endswith(".html") or filename == "index.html":
        continue
    num = filename.split("_")[0]
    if num not in ANNOTATIONS:
        print(f"  WARNING: No annotation for {filename}")
        continue
    if inject_panel(os.path.join(VIZ_DIR, filename), ANNOTATIONS[num]):
        count += 1

print(f"\nAnnotated {count}/{len(ANNOTATIONS)} charts")
missing = set(ANNOTATIONS.keys()) - set(f.split("_")[0] for f in os.listdir(VIZ_DIR) if f.endswith(".html") and f != "index.html")
if missing:
    print(f"Missing files for: {missing}")
