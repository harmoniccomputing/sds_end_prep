#!/usr/bin/env python3
"""Inject always-visible interpretation guides below all 80 charts."""
import os, re

VIZ_DIR = "visualizations"

# Universal CSS for the guide panel - always visible, fixed at bottom
GUIDE_CSS = '''<!--ATLAS-GUIDE-START-->
<style>
.guide{position:fixed;bottom:0;left:0;right:0;z-index:900;max-height:38vh;overflow-y:auto;
background:linear-gradient(180deg,rgba(6,8,15,.0),rgba(6,8,15,.98) 8%);
padding:32px 5% 20px;color:#C8D0DA;font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif;
font-size:.82rem;line-height:1.7;border-top:1px solid #1a2233}
.guide::-webkit-scrollbar{width:6px}.guide::-webkit-scrollbar-thumb{background:#2D3748;border-radius:3px}
.guide-inner{max-width:1200px;margin:0 auto;columns:2;column-gap:36px;column-rule:1px solid #1a2233}
@media(max-width:900px){.guide-inner{columns:1}}
.guide h2{color:#00D5E0;font-size:1rem;font-weight:700;margin:0 0 6px;column-span:all;
font-family:'Playfair Display',serif;letter-spacing:-.01em}
.guide h3{color:#FF5872;font-size:.78rem;font-weight:700;margin:10px 0 3px;text-transform:uppercase;letter-spacing:.04em}
.guide p{margin:0 0 7px;break-inside:avoid}
.guide .hl{background:#111825;border-left:3px solid #00D5E0;padding:8px 12px;margin:6px 0;
border-radius:0 5px 5px 0;break-inside:avoid;font-size:.79rem}
.guide .warn{border-left-color:#FF5872}
.guide .gold{border-left-color:#FFD700}
.guide b{color:#E8ECF0}.guide em{color:#FFD700;font-style:normal}
.guide code{background:#1C2333;padding:1px 5px;border-radius:3px;font-size:.75rem;color:#00D5E0}
</style>'''

GUIDE_END = '<!--ATLAS-GUIDE-END-->'

# Comprehensive annotations for all 80 charts
G = {}

G["01"] = '''<h2>Wealth vs Health of Nations</h2>
<h3>What You Are Seeing</h3>
<p>Each bubble is one country in one year. The <b>horizontal axis</b> shows GDP per capita in Purchasing Power Parity (PPP) dollars on a <em>logarithmic scale</em>: each major gridline represents a tenfold increase in national income. The <b>vertical axis</b> shows life expectancy at birth in years. <b>Bubble size</b> encodes total population, making India and China visually dominant. <b>Color</b> distinguishes continents. The <b>animation slider</b> at the bottom steps through years 1990 to 2023, letting you watch three decades of development unfold.</p>
<h3>Why the Log Scale Matters</h3>
<p>The logarithmic transformation on the X-axis is not cosmetic. The relationship between income and health follows the <b>Preston Curve</b> (Samuel Preston, 1975): life expectancy rises steeply at low incomes, then flattens. Going from $1,000 to $5,000 GDP per capita adds roughly 15 years of life expectancy (through basic sanitation, nutrition, and primary healthcare). Going from $50,000 to $100,000 adds perhaps 1-2 years. The log scale makes this non-linear relationship appear as a straighter line, revealing the diminishing returns that are the central insight.</p>
<h3>What the Trends Mean</h3>
<div class="hl">As you press play and watch bubbles migrate rightward (richer) and upward (healthier), you are witnessing the single most important fact about the modern world: <b>global health has improved dramatically and nearly universally</b>. Sub-Saharan African nations (cyan) start in the bottom-left in 1990 but shift visibly rightward by 2023. China's bubble (large, pink) makes a dramatic rightward leap. Countries that move <b>downward</b> (rare) have experienced catastrophic health crises: Botswana and South Africa dipped during the HIV/AIDS epidemic of the 1990s-2000s before antiretroviral therapy restored life expectancy.</div>
<h3>Policy Implications</h3>
<div class="hl warn">For countries on the <b>steep part</b> of the curve ($1K-$10K GDP), economic growth is the most powerful health intervention available: growth funds hospitals, trains doctors, builds water systems. For countries on the <b>flat part</b> (above ~$30K), further GDP growth yields minimal health gains; <b>targeted investments</b> in healthcare equity, mental health, lifestyle disease prevention, and social infrastructure become more cost-effective. The policymaker's question changes from "how do we grow?" to "how do we distribute and apply what we have?" Sub-Saharan nations face a compounding trap: poor health reduces economic productivity, which perpetuates poor health. Breaking this cycle requires simultaneous investment in health <em>and</em> economic infrastructure.</div>'''

G["02"] = '''<h2>Fertility vs Longevity: The Demographic Transition in Motion</h2>
<h3>Reading the Axes</h3>
<p><b>X-axis: Fertility Rate</b> (births per woman over her lifetime at current rates). Values above <em>2.1</em> indicate population growth (above replacement level). Below 2.1 means eventual population decline without immigration. The 0.1 above 2.0 accounts for child mortality. <b>Y-axis: Life Expectancy</b> at birth in years.</p>
<h3>The Demographic Transition</h3>
<div class="hl">This chart visualizes humanity's most consequential transformation. Societies move from <b>high fertility + low life expectancy</b> (upper-left) to <b>low fertility + high life expectancy</b> (lower-right). This shift is driven by: (1) declining child mortality (parents need fewer births to ensure surviving children), (2) women's education and workforce participation, (3) contraceptive access, (4) urbanization (children shift from economic assets to costs). By 2023, most of the world has completed or is mid-transition. <b>Sub-Saharan Africa is the final frontier</b>, and its trajectory will determine whether world population peaks at 9 billion or 11 billion.</div>
<h3>Policy Implications</h3>
<div class="hl warn">Countries in the <b>upper-left</b> (high fertility, low lifeExp) face a <em>youth bulge</em>: enormous young populations needing education, jobs, and services. If harnessed through education and job creation, this becomes a <em>demographic dividend</em> that accelerates growth (as happened in East Asia, 1970-2000). If neglected, it becomes a source of instability. Countries in the <b>lower-right</b> (low fertility, high lifeExp) face aging populations: pension pressure, labor shortages, and rising dependency ratios. Japan (fertility 1.2) and South Korea (0.7) represent the extreme of this challenge. <b>The single most cost-effective intervention</b> for countries still in early transition is girls' secondary education, which reliably reduces fertility by 0.5-1.0 children per woman.</div>'''

G["37"] = '''<h2>LISA Cluster Map: Where Electoral Behavior Clusters Geographically</h2>
<h3>What Is LISA?</h3>
<p><b>LISA</b> stands for Local Indicators of Spatial Association, developed by Luc Anselin (1995). It answers a specific question: <em>is the value at a given location significantly similar to or different from its neighbors?</em> The method computes a local version of <b>Moran's I statistic</b> for each spatial unit (here, each of India's 543 parliamentary constituencies).</p>
<h3>How Moran's I Is Calculated</h3>
<div class="hl"><b>Moran's I</b> = (n / sum of all weights) x (sum of weighted cross-products of deviations from mean) / (sum of squared deviations). Formally: <code>I = (n/W) x [sum_i sum_j w_ij(x_i - x_bar)(x_j - x_bar)] / [sum_i (x_i - x_bar)^2]</code>. Here, <em>n</em> = 543 constituencies, <em>x_i</em> = the variable value at constituency <em>i</em>, <em>w_ij</em> = the spatial weight between constituencies <em>i</em> and <em>j</em> (1 if neighbors, 0 otherwise), and <em>x_bar</em> = the overall mean. <b>I = 0</b> means no spatial pattern (random). <b>I > 0</b> means clustering (similar values near each other). <b>I < 0</b> means dispersion (dissimilar values near each other). For turnout, <b>I = 0.642</b>: extremely strong positive spatial autocorrelation.</div>
<h3>What the Spatial Weights Mean</h3>
<p>We used <b>KNN k=8</b>: each constituency's 8 nearest neighbors (by centroid distance) are considered its spatial neighbors. Weights are <em>row-standardized</em> (each row sums to 1), so each neighbor contributes equally. Significance is tested with <b>999 conditional permutations</b>: the observed local I is compared against 999 random reshufflings of the data. Only clusters with <b>p < 0.05</b> (fewer than 5% chance of occurring randomly) are colored.</p>
<h3>Reading the Colors</h3>
<p><b>Red (High-High / Hot Spot)</b>: a constituency with HIGH turnout surrounded by neighbors with HIGH turnout. <b>Blue (Low-Low / Cold Spot)</b>: LOW turnout surrounded by LOW turnout. <b>Orange (High-Low)</b>: a high-turnout outlier surrounded by low-turnout neighbors. <b>Cyan (Low-High)</b>: the reverse. <b>Grey</b>: not statistically significant.</p>
<h3>What the Patterns Reveal</h3>
<div class="hl">The left panel (turnout) reveals a <b>sharp North-South divide</b>: 150 Hot Spots concentrate in Kerala, Tamil Nadu, and West Bengal (high civic engagement), while 170 Cold Spots concentrate in Uttar Pradesh and Bihar (low participation). This is not random: it reflects deep structural differences in <b>literacy, political mobilization, women's participation, and democratic culture</b>. Tobler's First Law of Geography applies: "near things are more related than distant things." Voter behavior is contagious through social networks that are geographically bounded.</div>
<h3>Policy Implications</h3>
<div class="hl warn"><b>Cold spot constituencies</b> (UP/Bihar) need: more polling stations per voter, voter awareness campaigns in local languages, transportation infrastructure to remote booths, and women-specific mobilization (women's turnout is even lower in these areas). <b>Hot spot regions</b> (Kerala, Tamil Nadu) demonstrate that high civic engagement can be cultivated through sustained investment in literacy, political competition, and local governance. The spatial clustering means that <b>interventions in one constituency can spill over to neighbors</b>, suggesting that area-based rather than constituency-by-constituency approaches may be more efficient.</div>'''

G["65"] = '''<h2>The Silence Map: 152 Constituencies Where No Woman Even Ran</h2>
<h3>What You Are Seeing</h3>
<p>Every one of India's 543 Lok Sabha constituencies is plotted on this map. <b>Red X markers</b> (large, impossible to miss) mark the 152 constituencies where <em>not a single woman filed her candidacy</em> in the 2024 general election. <b>Orange dots</b> = exactly 1 woman candidate. <b>Yellow</b> = 2-3 women. <b>Green</b> = 4 or more women candidates. Data source: Election Commission of India, 2024.</p>
<h3>What the Numbers Mean</h3>
<div class="hl"><b>152 out of 543 = 28% of Indian democracy had zero female voice on the ballot.</b> This is not about women losing elections. This is about women not even being present as an option for voters. In these constituencies, every single candidate was male. The question is not "why don't women win?" but "why don't women even run?" The answer lies in <b>party gatekeeping</b> (parties nominate men), <b>social barriers</b> (harassment, family opposition, financial constraints), and <b>structural factors</b> (larger, rural constituencies with conservative norms make campaigning harder for women).</div>
<h3>The Spatial Pattern</h3>
<div class="hl gold">The red Xs are <b>not randomly distributed</b>. They cluster heavily in the <em>Hindi heartland</em>: central Uttar Pradesh, rural Bihar, parts of Rajasthan and Maharashtra. Southern and northeastern states show more green (more women candidates). Urban constituencies tend to have more women filing. This geographic pattern mirrors India's <b>gender development index</b>: the same states with the worst sex ratios, lowest female literacy, and highest rates of child marriage are the ones where women cannot even enter the political arena.</div>
<h3>Policy Implications</h3>
<div class="hl warn">The <b>Women's Reservation Bill (33%)</b>, passed in 2023 but not yet implemented, would reserve approximately 181 constituencies for women candidates. This would force parties to nominate women in exactly the kind of constituencies currently showing red Xs. Without this structural mandate, 75 years of Indian democracy have produced only incremental improvement: from about 5% women MPs in the 1950s to about 8.7% today. The spatial clustering suggests that <b>cultural change alone is insufficient</b>. The bill's implementation would be the single most impactful intervention for women's political representation in India. Additionally, parties should be required to provide genuine campaign infrastructure (funding, media, organization) to women candidates, not just symbolic nominations.</div>'''

G["72"] = '''<h2>Fiscal Returns: The Tax Inequality Map of India</h2>
<h3>What You Are Seeing</h3>
<p>A diverging horizontal bar chart showing, for each major Indian state, <b>how many rupees it gets back from the central government for every Rs 100 it pays in taxes</b>. The <b>gold dashed line at Rs 100</b> marks break-even: to its left, states are <em>net contributors</em> (paying more than they receive). To its right, states are <em>net recipients</em>.</p>
<h3>How Fiscal Transfers Work</h3>
<p>India's fiscal architecture routes tax revenue through the central government, which then distributes it back to states through the <b>Finance Commission</b> formula. The 15th Finance Commission uses these criteria with weights: <em>Population (15%)</em>, <em>Area (15%)</em>, <em>Forest cover (10%)</em>, <em>Demographic performance (12.5%)</em>, <em>Income distance (45%)</em>, <em>Tax effort (2.5%)</em>. The <b>income distance</b> criterion (45% weight) means poorer states receive more, which is the largest driver of the redistribution pattern.</p>
<h3>What the Bars Mean</h3>
<div class="hl"><b>Tamil Nadu: Rs 29.7</b> means Tamilians pay Rs 100 in taxes but their state receives only Rs 29.7 in central transfers. The "missing" Rs 70.3 subsidizes other states. <b>Bihar: Rs 142.5</b> means Bihar receives Rs 42.5 more per Rs 100 than its population pays in taxes. <b>Delhi: Rs 15.2</b> is the most extreme contributor, reflecting its high income and tax base relative to its small population.</div>
<h3>The "Double Whammy" Problem</h3>
<div class="hl warn">Southern states (Tamil Nadu, Karnataka, Kerala, Maharashtra) face a <b>compounding penalty</b>: they invested in education, healthcare, and family planning, which <em>reduced their population growth</em>. Under population-based delimitation, they will <em>lose Lok Sabha seats</em>. Simultaneously, because they are economically successful (partly <em>because</em> of lower population growth), they <em>subsidize northern states fiscally</em>. They are punished twice for the same good behavior. Northern states (UP, Bihar), which did not invest as heavily in population control, gain both more seats AND more fiscal transfers. This creates a <b>perverse incentive</b> against demographic responsibility.</div>
<h3>Policy Debate</h3>
<div class="hl gold">The core tension: fiscal redistribution from rich to poor states is a feature of all federal democracies (Germany, US, Australia all do this). The question is <b>how much weight</b> should go to population vs other criteria. Southern states argue that <em>demographic performance</em> (currently 12.5% weight) should be increased to reward population control, and that <em>literacy</em> and <em>human development</em> should be added as criteria. The Finance Commission could also consider earmarking a portion of transfers for women's welfare (see Chart 75: Punishment Value), which would partially compensate contributor states that have invested in women's development.</div>'''

G["71"] = '''<h2>Delimitation Simulator: What If India Had More Seats?</h2>
<h3>How to Use This Chart</h3>
<p><b>Drag the slider</b> from 543 (current) to 1000 total Lok Sabha seats. Each frame shows what would happen if seats were redistributed purely proportional to state population using the <b>Webster/Sainte-Lague method</b> (a proportional allocation algorithm where each state gets seats proportional to its population, with remainders allocated to states with the largest fractional entitlement).</p>
<h3>Reading the Scatter</h3>
<p><b>X-axis</b> = current seats (out of 543). <b>Y-axis</b> = new proportional seats. The <b>gold diagonal line</b> = no change. Points <em>above</em> the diagonal = states that <b>gain</b> seats under proportional reallocation. Points <em>below</em> = states that <b>lose</b>. <b>Color = region</b>: South (red), North (green), Central (yellow), East (cyan), West (orange), Northeast (purple). <b>Size</b> = magnitude of change.</p>
<h3>What the Animation Reveals</h3>
<div class="hl">As you drag rightward (more total seats), all points move upward (every state gets more seats in absolute terms), but <b>the relative position does not change</b>. Southern states (red) consistently sit below the diagonal because their population growth was lower than the national average (thanks to successful family planning). Northern states (green/yellow) consistently sit above. At 543 seats: UP goes from 80 to ~91 proportionally. Tamil Nadu drops from 39 to ~31. At 1000 seats: the shift is diluted but not eliminated.</div>
<h3>Policy Implications</h3>
<div class="hl warn"><b>Increasing total seats to 700 or 1000 reduces the proportional pain</b> for southern states because they still gain seats in absolute terms (just fewer than northern states). But the fundamental demographic imbalance remains. Alternative approaches: (1) <b>weight criteria beyond population</b> (area, literacy, fiscal contribution), (2) <b>freeze the current ratio</b> indefinitely (as India did from 1976-2026), (3) <b>create compensating mechanisms</b> in the Rajya Sabha or Finance Commission. Each approach has tradeoffs between democratic equality (one person, one vote) and federalism (protecting smaller/responsible states).</div>'''

# Generate remaining charts with efficient but thorough annotations
BATCH = {
"03":"Under-5 mortality vs GDP. <b>Under-5 mortality</b>: probability of dying before age 5, per 1,000 live births. Values >100 = 1 in 10 children dies. The dramatic global decline (many countries from 200+ to below 50 between 1990-2023) is driven by oral rehydration therapy, vaccines, bed nets, and nutrition. <b>Log X-axis</b> compresses the wealth scale to reveal patterns among poorer nations. <b>Policy</b>: every dollar of GDP growth in poor countries saves children's lives. But countries like Bangladesh prove that <b>targeted public health investment can override economic constraints</b>: focus on primary care, clean water, and vaccination over expensive tertiary hospitals.",
"04":"14 nations traced on GDP vs life expectancy. Each line = one country's development path over decades. <b>Rightward</b> = getting richer. <b>Upward</b> = healthier. China shows the most dramatic leap (economic liberalization). Botswana/South Africa show HIV/AIDS dips before ARV recovery. Rwanda shows a sharp 1994 dip (genocide) then rapid recovery. <b>Policy</b>: development is not monotonic; crises reverse progress. Health system resilience determines recovery speed.",
"05":"Three panels: GDP, life expectancy, fertility by continent over time. <b>Population-weighted</b> means lines reflect what the average <em>person</em> (not country) experiences. Key finding: life expectancy is <b>converging</b> (Africa catching up). GDP is <b>diverging</b> (gap widening). Fertility is converging. <b>Policy</b>: health interventions are the most globally equitable force; markets alone will not close the wealth gap.",
"06":"Population-weighted income distribution shifting from bimodal (two humps: rich world + poor world) toward unimodal (one middle-income hump), 1995-2020. The merge is driven by China and India pulling ~2.5 billion people into middle income. <b>X-axis is log income</b>: each gridline = 10x increase. <b>Area under curve</b> = population at that income. The remaining left tail (extreme poor) is increasingly concentrated in Sub-Saharan Africa.",
"07":"27 reef systems on dark ocean. <b>Size = reef area (km2)</b>. <b>Color = threat level</b>: Critical (>50% coral lost), High (significant recent bleaching), Medium, Low. Thermal stress from warming oceans causes coral to expel symbiotic algae (bleaching). <b>Policy</b>: Marine Protected Areas reduce local stressors but cannot prevent thermal bleaching. The Paris Agreement's 1.5C target is effectively a <b>reef survival threshold</b>.",
"08":"Global SST anomaly 1980-2024 with mass bleaching events. <b>SST Anomaly</b> = deviation from 1971-2000 baseline. Positive = warmer. The tightening interval between crises (1998, 2010, 2016, 2024: 18, 12, 6, 8 years) shows <b>accelerating frequency</b>. <b>Policy</b>: reef management must shift from 'protect and recover' to 'adapt and triage' as some systems will not survive.",
"09":"Animated world choropleth: urban population % (1990-2022). <b>Increasing color intensity</b> = more urbanized. China went from ~26% to ~64%. <b>Policy</b>: countries entering the 30-50% range (current Africa) face a critical window: invest now in transit, housing, and sanitation, or lock in decades of slums.",
"10":"% urban population in slums. <b>Slum</b> (UN-Habitat): housing lacking durable structure, sufficient space, water, sanitation, or tenure security. Values >50% = most urban residents lack basic housing. <b>Policy</b>: upgrading existing settlements (water, sanitation, tenure) is far more cost-effective than demolition.",
"11":"Population below $1.90/day (PPP). This line represents minimum survival needs. Values >40% = nearly half the population in extreme deprivation. <b>Policy</b>: cash transfers, agricultural investment, and conflict resolution are the three most effective poverty reduction tools.",
"12":"<b>Gini coefficient</b> (0-100): measures income concentration. Calculated from the Lorenz curve (plotting cumulative income share vs cumulative population share). Gini 30 (Scandinavia) = relatively equal. Gini 60+ (South Africa) = extreme concentration. <b>Policy</b>: high inequality correlates with social instability, worse health outcomes. Progressive taxation and universal education are primary tools.",
"13":"Internet users %, animated 2000-2022. <b>Increasing values</b> = digital inclusion. The spread was North-to-South, rich-to-poor. <b>Policy</b>: digital literacy programs and mobile infrastructure in underserved areas yield outsized returns in education, healthcare, and economic participation.",
"14":"% population with electricity. Sub-Saharan Africa has the lowest rates. <b>Policy</b>: off-grid solar leapfrogs centralized grids in remote areas. Energy poverty limits education (no light), healthcare (no refrigeration), and economic activity.",
"15":"Mobile subscriptions per 100. Values >100 = multiple SIMs per person. Mobile is the most equitably distributed technology globally. <b>Policy</b>: mobile money (M-Pesa) and mobile health platforms deliver financial/health services to unbanked populations.",
"16":"GDP per capita in PPP dollars. <b>PPP adjustment</b> accounts for local price differences ($1,000 in India buys more than in Switzerland). <b>Policy</b>: GDP/cap is the standard welfare proxy but misses inequality, environment, and unpaid labor.",
"17":"Trade (exports+imports) as % of GDP. High values = trade-dependent. Small nations (Singapore >300%) are entrepot economies. Large economies (US ~25%) have lower ratios. <b>Policy</b>: openness correlates with growth but also vulnerability to global shocks.",
"18":"Remittances as % of GDP. High dependency (>20%) indicates structural reliance on migration. <b>Policy</b>: reducing transfer costs (currently 5-10%, target 3%) would immediately increase family incomes. Invest remittances into productive assets, not just consumption.",
"19":"Forest area as % of land. Amazon, Congo basins dominate. <b>Policy</b>: REDD+ programs pay to preserve forests. These basins are globally significant carbon sinks whose loss would accelerate climate change.",
"20":"Renewable energy % of consumption. High values in poor countries often = traditional <b>biomass</b> (wood, charcoal), not modern renewables. <b>Policy</b>: the distinction between 'good' renewables (solar/wind) and 'bad' renewables (biomass causing deforestation/indoor pollution) is critical.",
"21":"Water withdrawals as % of renewable resources. <b>>100% = unsustainable</b>: extracting fossil groundwater. The 20-35 degree latitude band (MENA, Central Asia) faces the worst stress. <b>Policy</b>: water pricing, drip irrigation (reduces use 30-50%), desalination, and wastewater recycling.",
"22":"Countries at geographic coords as bubbles. Size = population. <b>Policy</b>: the spatial distribution shows where infrastructure investment affects the most people. Asia's concentration means interventions there have highest population-weighted impact.",
"23":"GDP (log) vs absolute latitude. Tests the <b>geography hypothesis</b> (Sachs 2001): tropical countries are poorer due to disease burden, agricultural productivity, and colonial history. Strong positive correlation. <b>Policy</b>: tropical nations need compensating investment in healthcare and institutions.",
"24":"Distance to nearest megacity (>10M) vs life expectancy. Tests the <b>connectivity premium</b>: proximity to economic hubs correlates with health. <b>Policy</b>: transportation and telemedicine can reduce isolation penalties.",
"25":"Under-5 mortality vs latitude by climate zone. Tropical countries face higher mortality (malaria, diarrheal diseases). <b>Policy</b>: climate-specific health interventions (bed nets, oral rehydration) can break the climate-mortality link.",
"26":"UCDP conflict intensity (0-10) vs GDP and life expectancy. Even moderate conflict (3-5) costs 10-15 years of life expectancy. <b>Policy</b>: every $1 on peacekeeping saves ~$10-16 in reconstruction. Conflict prevention yields enormous development dividends.",
"27":"GDP distributions: landlocked vs coastal, by continent. Landlocked countries face 15-20% higher transport costs. <b>Policy</b>: regional transit agreements, railways, and customs harmonization reduce the penalty. Botswana shows good governance partially overcomes geography.",
"28":"Internet vs latitude, colored by income. Income group explains most variance, but latitude adds explanatory power. <b>Policy</b>: universal broadband should target the intersection of low latitude and low income.",
"29":"Fertility distributions across 4 climate zones (violin plots). Tropical zones show widest distribution, highest median. <b>Violin width</b> = density of countries at that fertility level. <b>Policy</b>: the fertility-climate link operates through women's education and healthcare, which can be intervened upon regardless of climate.",
"30":"Urban % vs renewable energy share. Counterintuitively negative: highly urbanized = more fossil fuel dependent. Rural = more biomass ('renewable'). <b>Policy</b>: urban clean energy transitions require grid-scale solar/wind, not biomass.",
"31":"Water withdrawals vs latitude. The 20-35 degree band = subtropical deserts with extreme stress. <b>Policy</b>: agricultural water efficiency, demand management, and wastewater recycling are more sustainable than supply-side solutions.",
"32":"Physicians per 1,000 vs latitude. Fewer doctors near equator (brain drain + training gaps). <b>Policy</b>: community health workers, telemedicine, and retention bonuses for rural physicians can compensate.",
"33":"Primary completion vs distance to megacity. Remote countries have lower completion. <b>Policy</b>: distance learning, mobile education, and teacher incentives for remote postings.",
"34":"Trade openness vs longitude. Peaks at 0-30E (Europe) and 100-120E (East Asia), the two major trade blocs. <b>Policy</b>: countries between peaks (Central Asia, Middle East) can leverage their position as trade corridors.",
"35":"Maternal mortality vs forest cover. High forest = rural remoteness, poor healthcare access. <b>Policy</b>: forested countries need skilled birth attendants in remote areas. High forest cover is not inherently protective for health.",
"36":"Remittances vs latitude. Low-latitude countries depend most on remittances (South-to-North migration). <b>Policy</b>: remittance flows partially compensate for the latitude-wealth gradient.",
"38":"Constituency area (log km2) vs turnout and margin. <b>Log transformation</b> handles the 4-order-of-magnitude range (29 km2 to 180,000 km2). <b>Negative slope</b> for area vs turnout: larger constituencies have lower participation (logistical barriers). Area is itself spatially autocorrelated (I=0.16). <b>Policy</b>: larger constituencies need more polling stations, mobile booths, and postal ballots.",
"39":"<b>Moran's I Scatterplot</b>: X = standardized value (deviation from mean), Y = spatial lag (neighbors' average). <b>Slope = Moran's I</b>. Four quadrants: HH (top-right, high near high), LL (bottom-left, low near low), HL/LH (outliers). Points in HH/LL = spatial clustering. HL/LH = local factors overriding regional trends. <b>Policy</b>: outlier constituencies merit investigation as models.",
"40":"Turnout change 2019 to 2024. <b>Red = dropped</b> (disengagement). <b>Blue = rose</b> (mobilization). National avg: -1.4pp. <b>Policy</b>: constituencies with large negative swings need investigation: weather, security, suppression, or genuine disaffection? Targeted Get-Out-The-Vote campaigns should focus here.",
"41":"Margin vs distance from Delhi. Tests Rokkan's (1970) <b>core-periphery model</b>. No strong linear effect, but variance changes: near Delhi margins range widely, far away they are more uniform. <b>Policy</b>: Indian democracy is not simply radiating from a single center.",
"42":"543 constituencies on rotating 3D cylinder. <b>Height = latitude</b>, <b>angle = longitude</b>, <b>color = alliance</b>. The cylindrical projection reveals the North-South political divide more dramatically than flat maps. <b>Pink octahedra = women winners</b>. <b>Policy</b>: any party seeking national power must bridge this spatial divide.",
"43":"196 countries on rotating sphere. Bars extrude proportional to selected metric (GDP/lifeExp/fertility). Switch with buttons. <b>Policy</b>: the globe perspective reveals that development challenges cluster by hemisphere, requiring geographically targeted international cooperation.",
"44":"NDA and INDIA alliance constituencies spiral in DNA double helix. <b>Node size = margin</b>. NDA strand dense in upper turns (north), INDIA in lower turns (south). <b>Policy</b>: India's political geography is encoded in a dual structure, not a simple divide.",
"45":"196 countries in 3D: X=GDP(log), Y=Life Expectancy, Z=Fertility. <b>Three variables simultaneously</b> without 2D projection information loss. Africa clusters at high-Z/low-X/low-Y. Europe at the opposite. <b>Policy</b>: the 3D view reveals countries that break expected patterns (Gulf states, Singapore).",
"46":"Three panels testing if women win in larger/smaller constituencies. <b>Mann-Whitney U test</b>: non-parametric comparison of two distributions. Women win in slightly smaller, denser seats (median 3,324 vs 4,073 km2). <b>Policy</b>: parties should consider geographic favorability when nominating women.",
"47":"3D bars over India. Height = metric (electorate ratio/turnout/margin), switchable. <b>Spatial histogram</b>: quantitative data superimposed on geography. <b>Policy</b>: electorate ratio mode reveals North-South inequality; northern votes are worth less.",
"48":"Left: LISA on NDA/INDIA (I=0.37). Right: NDA share vs women %. <b>Key finding</b>: women's representation does NOT correlate with alliance dominance. Both strongholds have poor women's representation. <b>Policy</b>: reservation mandates are needed; partisan goodwill is insufficient.",
"49":"Top 15 GDP per capita bar race, 1992-2022. Ireland's rise = corporate tax haven. Qatar = resource wealth in tiny population. <b>Policy</b>: per-capita GDP rankings can be misleading; median household income is a better welfare measure.",
"50":"Animated geo scatter toggling 2019 vs 2024 elections. Bubbles morph as margins shift. <b>Policy</b>: constituencies with >10pp swings deserve investigation: candidate quality, anti-incumbency, or structural demographic shifts?",
"51":"Year-by-year animation of fertility vs life expectancy, 1990-2023. <b>The single most important demographic chart</b>: watch the entire world converge. <b>Policy</b>: remaining high-fertility countries (West/Central Africa) need girls' education investment, the most effective intervention for demographic transition.",
"52":"Animated choropleth of under-5 mortality 1990-2022. Watch Africa gradually lighten. Acceleration post-2000 coincides with Millennium Development Goals. <b>Policy</b>: coordinated international goals work. SDG era must continue.",
"53":"Left: life expectancy converging. Right: GDP diverging. <b>Convergence</b> = lines coming together. <b>Divergence</b> = spreading apart. <b>Policy</b>: health interventions overcome inequality; markets alone do not equalize wealth.",
"54":"LISA on women winners (I=0.06, weak but significant). Right: area vs density with women highlighted. Women cluster slightly. <b>Policy</b>: parties could strategically nominate women in clusters where neighbors elected women, leveraging the neighborhood effect.",
"55":"214 flipped constituencies pulse with golden rings. <b>Pulsing = sinusoidal animation</b> drawing attention to change. <b>Policy</b>: flipped seats = the dynamic part of democracy. Understanding what drove flips informs strategy.",
"56":"Countries trace spiral paths through time (1952-2007). <b>Radius = log(GDP)</b>, <b>height = life expectancy</b>. Slider scrubs years. Countries spiraling outward+upward = developing. Inward/downward = regressing. <b>Policy</b>: the slider reveals when development accelerated or stalled, correlating with policy eras.",
"57":"Reef map (top) + SST timeline (bottom). Links cause (warming) and effect (bleaching). Tightening intervals between crises show <b>accelerating frequency</b>. <b>Policy</b>: the Paris 1.5C target is a reef survival threshold. Current trajectories (2.5-3C by 2100) = 70-90% reef loss.",
"58":"Gini animated by 5-year bins, 1990-2020. Latin America's declining Gini = successful conditional cash transfers (Bolsa Familia). China's rising Gini = inequality cost of rapid growth. <b>Policy</b>: policy choices, not just market forces, determine inequality trajectories.",
"59":"30 Indian states as 3D pillars. 8 switchable metrics. <b>Width = area</b>. <b>Color: red(low) to green(high)</b>. Switching reveals that <b>no state excels on all dimensions</b>. Kerala leads HDI but not GSDP. <b>Policy</b>: balanced development requires investment across all dimensions simultaneously.",
"60":"Rice (green diamonds) and wheat (gold squares) at state lat/lon, height = production (MT). Sharp geographic division follows the monsoon boundary. <b>Policy</b>: climate change threatens wheat in Punjab (heat) and rice in Bengal (sea level). Crop diversification is insurance.",
"61":"Two helical strands: literacy (cyan) vs sex ratio (magenta), ordered by HDI. Where both bulge (Kerala) = education and gender equity reinforce each other. Where they diverge (Haryana: literacy OK, sex ratio terrible) = structural problem. <b>Policy</b>: education alone does not guarantee gender equity; cultural interventions against sex-selective practices are required.",
"62":"543 constituencies as breathing particles. Oscillation amplitude = turnout. Glow = margin. Beams = high-margin seats. <b>Policy</b>: the aurora makes democratic health feel organic. High-amplitude regions have engaged electorates.",
"63":"X=Literacy, Y=GSDP, Z=HDI. <b>Drop lines</b> show HDI height. Southern states cluster high. Delhi is an outlier: high GSDP but moderate HDI (inequality reduces average). <b>Policy</b>: HDI is a better welfare measure than GSDP.",
"64":"X=Sex Ratio, Y=IMR (reversed: lower=better=higher), Z=Literacy. Color=sex ratio (red=dangerous, green=healthy). Kerala at ideal corner. Haryana at alarming opposite. <b>Policy</b>: states in red need PCPNDT Act enforcement against sex-selective abortion, plus cultural change programs.",
"66":"Funnel: 8,360 candidates to 458 women to 133 deposit-saved to 47 winners. <b>Deposit forfeiture</b>: candidates getting <1/6 of votes lose their security deposit. 71% of women candidates forfeited. <b>Policy</b>: parties must provide real campaign infrastructure to women candidates, not symbolic nominations.",
"67":"Female voters per 1,000 male by state. <b>Parity = 1000</b>. Green = above. Red = below. Bihar (907) = ~4 million 'missing' women from voter rolls. <b>Policy</b>: voter registration drives targeting women, especially in states below 950, could add millions to the democratic process.",
"68":"Every woman candidate plotted. 325 red (forfeited), 86 gold (lost, saved deposit), 47 green (won). The red wall of 325 dots = women fielded without real party backing. <b>Policy</b>: candidate training, funding, and mentorship for women would move dots from red to gold.",
"69":"Triple panel: women elected, forfeit rate, gender ratio. 14 states elected zero women. Kerala elected zero women despite best gender ratio (1,084). <b>Policy</b>: voter parity does NOT translate to women winning. The pipeline breaks at party <b>nomination</b>, not voting. Mandatory party-level quotas are needed.",
"70":"3D: height = % women candidates. Red X on floor = zero women. Most of India = flat red desert with rare green peaks. <b>Policy</b>: women's candidature is concentrated in specific niches (urban, southern). Breaking out requires party structural reform.",
"73":"Slider 0-100% women's reservation. At 33% (actual bill): ~180 seats. Current: 47 (8.7%). <b>Policy</b>: reservation is the only proven mechanism for rapid representation increase. 75 years of 'gradual change' produced only marginal improvement.",
"74":"Two curves: Moran's I vs weight between criteria. <b>Lower I = more equitable dispersion</b>. Area-weighted allocation = higher I (more clustering, less fair). <b>Policy</b>: optimal delimitation formula minimizes spatial clustering, meaning no region is systematically over/underrepresented.",
"75":"3D: fiscal return x female voter % x seats. <b>Punishment value</b> = 1 - 0.35 x (fiscal_return/100). TN (0.90) and MH (0.90): worst triple burden (high taxes, low return, seat losses). <b>Policy</b>: earmarking 35% of transfers (estimated women's tax share) for women's welfare partially compensates contributor states.",
"76":"Electors per seat by state. Slider 543-1000. At 543: UP has ~2.4M/seat, Sikkim ~0.4M. A Sikkim vote is worth <b>6x</b> a UP vote. Increasing seats toward 1000 equalizes. <b>Policy</b>: this is the most fundamental democratic inequality in India.",
"77":"States connected south-to-north. Size = seats. Color = fiscal return. Red (contributors) at southern end, green (recipients) at northern end. <b>Policy</b>: the fiscal gradient mirrors the political divide. Fiscal federalism is inseparable from electoral geography.",
"78":"Treemap: Region > State. Area = seats. Color = fiscal return. Central/East regions (green, large) receive most transfers AND have most seats. South (red, small) pays most AND has fewer seats. <b>Policy</b>: the 'double whammy' visualized spatially.",
"79":"Fiscal return vs women % with reservation slider. As reservation rises, all bubbles rise, but the X-axis (fiscal) does NOT change. <b>Policy</b>: reservation fixes the gender gap but NOT the fiscal gap. The two problems require separate interventions.",
"80":"Every constituency color-coded by % women candidates. Red zones cluster in UP, Bihar, Rajasthan. Green in urban/southern areas. <b>Policy</b>: women's exclusion is geographically patterned. Interventions should be spatially targeted at red zones.",
}

def inject_guide(filepath, content_html):
    with open(filepath, "r") as f:
        html = f.read()
    if 'ATLAS-GUIDE-START' in html:
        return False
    
    guide_block = GUIDE_CSS + '\n<div class="guide"><div class="guide-inner">\n'
    guide_block += content_html
    guide_block += '\n</div></div>\n' + GUIDE_END + '\n'
    
    if "</body>" in html:
        html = html.replace("</body>", guide_block + "</body>")
    else:
        html += guide_block
    
    with open(filepath, "w") as f:
        f.write(html)
    return True

# Process all charts
count = 0
for filename in sorted(os.listdir(VIZ_DIR)):
    if not filename.endswith(".html") or filename == "index.html":
        continue
    num = filename.split("_")[0]
    
    content = None
    if num in G:
        content = G[num]
    elif num in BATCH:
        # Wrap batch content in standard structure
        title = filename.split("_", 1)[1].replace(".html", "").replace("_", " ").title()
        content = f'<h2>{title}</h2>\n<p>{BATCH[num]}</p>'
    
    if content:
        if inject_guide(os.path.join(VIZ_DIR, filename), content):
            count += 1
    else:
        print(f"  NO ANNOTATION: {filename}")

print(f"\nInjected guides into {count} charts")
