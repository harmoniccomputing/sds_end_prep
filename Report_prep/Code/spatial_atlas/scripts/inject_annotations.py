#!/usr/bin/env python3
"""Inject interpretation panels into all 80 chart HTML files."""
import os, re

VIZ_DIR = "visualizations"

# CSS + JS for the collapsible interpretation panel
PANEL_CSS = '''<style>
.interp-toggle{position:fixed;bottom:16px;right:16px;z-index:9999;background:#00D5E0;color:#06080F;border:none;
width:44px;height:44px;border-radius:50%;font-size:1.3rem;cursor:pointer;box-shadow:0 2px 12px rgba(0,213,224,.4);
display:flex;align-items:center;justify-content:center;font-weight:700;transition:transform .2s}
.interp-toggle:hover{transform:scale(1.1)}
.interp-panel{position:fixed;bottom:70px;right:16px;z-index:9998;width:420px;max-height:70vh;overflow-y:auto;
background:rgba(13,17,23,.96);border:1px solid #21293A;border-radius:12px;padding:20px 22px;
color:#E0E0E0;font-family:'Source Sans 3',system-ui,sans-serif;font-size:.82rem;line-height:1.6;
box-shadow:0 8px 32px rgba(0,0,0,.5);display:none;backdrop-filter:blur(8px)}
.interp-panel.show{display:block;animation:fadeUp .3s ease-out}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.interp-panel h3{color:#00D5E0;font-size:1rem;margin:0 0 8px;font-weight:700}
.interp-panel h4{color:#FF5872;font-size:.85rem;margin:12px 0 4px;font-weight:600}
.interp-panel p{margin:0 0 8px;color:#A0AEC0}
.interp-panel .trend{background:#161B26;border-left:3px solid #00D5E0;padding:8px 12px;margin:8px 0;border-radius:0 6px 6px 0}
.interp-panel .trend b{color:#FFD700}
@media(max-width:600px){.interp-panel{width:calc(100vw - 32px);right:16px}}
</style>'''

PANEL_JS = '''<script>
(function(){var b=document.createElement('button');b.className='interp-toggle';b.innerHTML='?';
b.title='Show interpretation';b.onclick=function(){var p=document.getElementById('interp-panel');
p.classList.toggle('show');b.innerHTML=p.classList.contains('show')?'\\u2715':'?'};
document.body.appendChild(b)})();
</script>'''

# All 80 chart annotations
ANNOTATIONS = {
"01": {"title":"Wealth vs Health of Nations",
"show":"Each bubble is a country. X-axis = GDP per capita (PPP, log scale). Y-axis = life expectancy. Bubble size = population. Color = continent. Animation frames step through years 1990-2023.",
"queries":"Does wealth buy health? Which countries break the pattern? How fast is the developing world catching up?",
"trends":"Strong positive correlation: wealthier nations live longer. Sub-Saharan Africa (cyan) clusters bottom-left but moves rightward over decades. China and India (large Asian bubbles) shift dramatically right. The curve flattens above ~$30K, suggesting diminishing returns of wealth on longevity.",
"components":"Log scale on X reveals that the relationship is logarithmic, not linear. Animation slider shows temporal progression. Bubble size makes population-weighted patterns visible (India and China dominate)."},

"02": {"title":"Fertility vs Longevity",
"show":"Each bubble is a country plotted on fertility rate (births per woman) vs life expectancy, animated over time.",
"queries":"Is the world converging toward replacement fertility? Which regions are still in early demographic transition?",
"trends":"A clear negative correlation: higher fertility = lower life expectancy. Over time, most countries migrate toward the lower-right (low fertility, high longevity). Sub-Saharan Africa lags but is accelerating. By 2023, the global cluster is much tighter than 1990.",
"components":"Animation reveals the demographic transition in real-time. Bubble size shows that the world's most populous countries (India, China) have already reached near-replacement fertility."},

"03": {"title":"Child Mortality vs Wealth",
"show":"Under-5 mortality rate (per 1,000 live births) vs GDP per capita, animated 1990-2023. Each bubble is a country.",
"queries":"How strongly does national wealth predict child survival? Where have the biggest improvements occurred?",
"trends":"Dramatic global decline in child mortality. In 1990, many African countries exceeded 200 deaths per 1,000. By 2023, most are below 100. The relationship with GDP is strongly negative (log scale): even modest economic growth translates to significant mortality reduction.",
"components":"Log X-axis compresses the wealth scale to reveal patterns among poorer nations. Animation shows the accelerating pace of improvement since 2000 (Millennium Development Goals era)."},

"04": {"title":"Country Trajectory Traces",
"show":"14 key nations traced on the GDP vs life expectancy plane over their full trajectory. Each line shows one country's development path.",
"queries":"Which countries had the most dramatic transformations? Did any experience reversals? How do Asian tigers compare to African trajectories?",
"trends":"China shows the most dramatic rightward leap. Botswana and South Africa show the HIV/AIDS life expectancy dip (1990s-2000s) before recovery. Rwanda shows a sharp dip (1994 genocide) then rapid recovery. Oil states (Saudi Arabia) move right without proportional life expectancy gains.",
"components":"The traces make temporal direction visible. Scatter points mark specific years. The background grid contextualizes each trajectory against the global distribution."},

"05": {"title":"Continental Trends",
"show":"Three panels showing population-weighted averages for GDP per capita, life expectancy, and fertility rate, by continent, over time.",
"queries":"Are continents converging or diverging? Which dimension shows the most convergence?",
"trends":"Life expectancy is converging (Africa catching up to Europe). GDP per capita is diverging (gap widening). Fertility is converging rapidly (Africa declining toward global norms). Asia's GDP growth is the steepest of any continent.",
"components":"Population weighting means these lines reflect what the average person on each continent experiences, not the average country. Three panels allow simultaneous comparison across dimensions."},

"06": {"title":"Global Income Distribution Shift",
"show":"Population-weighted income distribution showing how global income has shifted from bimodal (two humps: rich and poor) toward unimodal (one middle-income hump) over 1995-2020.",
"queries":"Is the global middle class growing? Is the 'twin peaks' world disappearing?",
"trends":"The rich-world peak (right) and poor-world peak (left) gradually merge into a single broad peak centered around $10K-$15K PPP. This is driven primarily by China and India pulling hundreds of millions into middle-income status.",
"components":"Area charts stack to show population mass. The X-axis (income, log scale) reveals the compression of the bimodal distribution into a unimodal one. Color distinguishes time periods."},

"07": {"title":"Global Reef Bleaching Hotspots",
"show":"27 major coral reef systems plotted on a dark ocean map. Marker size = reef area (km2). Color = threat level (Critical/High/Medium/Low).",
"queries":"Where are the most threatened reefs? Is there a geographic pattern to bleaching? Which reefs are largest?",
"trends":"Critical reefs (red) concentrate in the Caribbean and Southeast Asian Coral Triangle. The Great Barrier Reef and Indo-Pacific systems dominate by area. Equatorial reefs face the highest thermal stress.",
"components":"Size encoding makes the Great Barrier Reef's dominance visible. Color encoding immediately flags the most at-risk systems. Dark ocean basemap provides geographic context."},

"08": {"title":"Ocean SST Anomaly Timeline",
"show":"Global sea surface temperature anomaly from 1980 to 2024, with all four mass bleaching events annotated.",
"queries":"Is ocean warming accelerating? How do bleaching events correlate with temperature spikes?",
"trends":"A clear upward trend with increasing volatility. The 1998 El Nino was the first truly global bleaching event. 2016 and 2024 shattered previous records. The baseline is rising: today's 'normal' would have been anomalous in the 1980s.",
"components":"The filled area below the line emphasizes cumulative warming. Annotations mark mass bleaching events, showing a tightening interval between crises (1998, 2010, 2016, 2024)."},

"09": {"title":"Global Urbanization (Animated Choropleth)",
"show":"Animated world map showing urban population percentage from 1990 to 2022. Color intensity = urbanization level.",
"queries":"Where is urbanization accelerating fastest? Which regions remain predominantly rural?",
"trends":"Asia and Africa show the most dramatic color shifts. China goes from mostly rural (1990) to majority urban (2022). Sub-Saharan Africa remains the least urbanized continent but is changing rapidly.",
"components":"Animation frames step through years. The choropleth color scale (light to dark) makes geographic patterns legible at a glance."},

"10": {"title":"Slum Population",
"show":"World choropleth of the percentage of urban population living in slums.",
"queries":"Where is informal housing most prevalent? Does urbanization without planning lead to slums?",
"trends":"Sub-Saharan Africa and South Asia have the highest slum percentages (60%+ in some countries). Latin American slum rates are declining. East Asian countries have dramatically reduced slum populations.",
"components":"The color gradient reveals the concentration of informal settlement in specific geographic belts. Missing data (grey) often indicates countries that do not report slum statistics."},

"11": {"title":"Extreme Poverty ($1.90/day)",
"show":"Global choropleth of population below the $1.90/day extreme poverty line.",
"queries":"Where is extreme poverty concentrated? Has it been declining?",
"trends":"Sub-Saharan Africa bears the overwhelming burden, with 10+ countries above 40%. South Asia has reduced poverty dramatically. East Asia has nearly eliminated it. The geographic concentration is stark.",
"components":"The YlOrRd color scale makes the severity gradient intuitive (yellow=low, red=high). Country-level resolution reveals within-region variation."},

"12": {"title":"Gini Inequality Index",
"show":"Global choropleth of the Gini coefficient (0=perfect equality, 100=total inequality).",
"queries":"Which regions are most unequal? Is inequality correlated with poverty?",
"trends":"Latin America and Southern Africa are the most unequal regions globally (Gini 50-63). Scandinavian countries are the most equal (Gini 25-30). Inequality and poverty are not the same: some wealthy countries (US, Gini ~41) are quite unequal.",
"components":"The color scale runs from green (equal) to red (unequal). Missing data is significant: many countries do not regularly measure inequality."},

"13": {"title":"Internet Usage (Animated Choropleth)",
"show":"Animated world map of internet users as % of population, from 2000 to 2022.",
"queries":"How fast did the digital revolution spread? Which countries are still offline?",
"trends":"In 2000, most of the world is below 10%. By 2022, Europe and the Americas are at 80-95%. Africa shows the most dramatic change in the 2010-2022 period (mobile internet leapfrogging). The digital divide persists but is narrowing.",
"components":"Animation is crucial here: the temporal progression from dark (offline) to bright (connected) is the story itself. Step through slowly to see the wave propagate from North to South."},

"14": {"title":"Electricity Access",
"show":"Choropleth of the percentage of population with access to electricity.",
"queries":"Where do people still live without electricity? Is energy poverty geographic?",
"trends":"Sub-Saharan Africa stands out starkly: multiple countries below 20% access. South Asia has made dramatic progress (India went from 60% to 99%+ in two decades). The equatorial belt in Africa remains the darkest zone.",
"components":"The single snapshot (latest year) hides the dramatic improvements in South and East Asia. Hover for exact figures per country."},

"15": {"title":"Mobile Phone Subscriptions",
"show":"Choropleth of mobile subscriptions per 100 people.",
"queries":"Did mobile leapfrog fixed-line infrastructure? Which countries have >100 subscriptions per person?",
"trends":"Many African and Asian countries exceed 100 (people have multiple SIMs). The mobile revolution is the most evenly distributed technology in history. Even the poorest countries show 50+ subscriptions per 100.",
"components":"Values above 100 indicate multiple subscriptions per person, common in countries with competing networks or dual-SIM phones."},

"16": {"title":"GDP per Capita (PPP)",
"show":"Global choropleth of GDP per capita in purchasing power parity dollars.",
"queries":"Where is global wealth concentrated? How wide is the gap between richest and poorest?",
"trends":"The North-South wealth divide is stark. Gulf states and Singapore/Hong Kong rival or exceed Western Europe. The gap between the poorest African nations (<$1,000) and the richest ($100K+) spans two orders of magnitude.",
"components":"PPP adjustment makes cross-country comparison meaningful by accounting for local price levels."},

"17": {"title":"Trade Openness",
"show":"Choropleth of total trade (exports + imports) as percentage of GDP.",
"queries":"Which economies are most trade-dependent? Is openness correlated with wealth?",
"trends":"Small, wealthy nations (Singapore, Luxembourg, Hong Kong) show extreme openness (>200% of GDP). Large economies (US, Brazil, Japan) show lower ratios despite high absolute trade volumes. Island nations and trade hubs are the most open.",
"components":"Trade as % of GDP normalizes for economy size. Very high values indicate entrepot economies (goods pass through rather than being consumed domestically)."},

"18": {"title":"Remittances (% of GDP)",
"show":"Choropleth of personal remittances received as percentage of GDP.",
"queries":"Which economies are most dependent on diaspora? Does remittance dependency indicate development challenges?",
"trends":"Small, low-income nations show the highest dependency: Tonga (40%+), Nepal (25%+), Tajikistan, El Salvador. These are economies where a significant fraction of the working-age population has migrated abroad. India receives the most in absolute terms but it is a small GDP fraction.",
"components":"Percentage of GDP reveals structural dependency that absolute dollar figures would hide."},

"19": {"title":"Forest Cover",
"show":"Choropleth of forest area as percentage of total land area.",
"queries":"Where are the world's remaining forests? Which biomes are most forested?",
"trends":"The Amazon Basin (Brazil, Peru, Colombia) and Congo Basin dominate. Scandinavian countries and Southeast Asia also show high coverage. The Sahel, Middle East, and Central Asian steppes have minimal forest.",
"components":"This is a snapshot of current cover, not deforestation rate. Countries with high cover but rapid loss (e.g., Indonesia) may appear green but face acute threats."},

"20": {"title":"Renewable Energy",
"show":"Choropleth of renewable energy as percentage of total final energy consumption.",
"queries":"Which countries lead in renewables? Is high renewable share always a sign of progress?",
"trends":"Sub-Saharan Africa shows high renewable percentages, but this reflects biomass (wood, charcoal) dependence, not modern renewables. Nordic countries show high shares from hydropower. Major economies (US, China) have lower percentages despite large absolute renewable capacity.",
"components":"The distinction between traditional biomass and modern renewables (solar, wind, hydro) is crucial for interpretation. High % in poor countries often means energy poverty, not clean energy progress."},

"21": {"title":"Freshwater Stress",
"show":"Choropleth of freshwater withdrawals as percentage of available renewable water resources. Over 100% = unsustainable.",
"queries":"Which regions face water crises? Is water stress geographic or economic?",
"trends":"The Middle East and North Africa (MENA) region is the most stressed globally, with several countries exceeding 100% (mining fossil groundwater). The subtropical arid belt (20-35 degrees latitude) shows a clear clustering of stress.",
"components":"Values above 100% indicate unsustainable extraction from non-renewable sources. This is a red alert: these countries are depleting their water capital."},

"22": {"title":"Nations Bubble Map",
"show":"Countries plotted at their geographic coordinates as bubbles. Size = population. Hover for GDP and life expectancy.",
"queries":"How does the geographic distribution of population map onto the globe?",
"trends":"Asia dominates with the two largest bubbles (India, China). Africa's bubble count is high but individual bubbles are smaller. Europe has many medium bubbles. The Americas are spread across a vast longitude range.",
"components":"The geographic placement makes this a population density proxy. Hover data adds the economic and health dimensions without cluttering the visual."},

"23": {"title":"Latitude-Wealth Gradient",
"show":"Scatter plot of GDP per capita (log scale) vs absolute latitude (distance from equator).",
"queries":"Is there a tropical poverty trap? Does geography determine economic destiny?",
"trends":"A strong positive correlation: countries further from the equator tend to be wealthier. This supports the 'geography hypothesis' (Sachs, 2001) and 'institutions hypothesis' (Acemoglu et al., 2001). Notable exceptions: Singapore (1 degree latitude, very wealthy), Gulf states.",
"components":"Absolute latitude removes hemisphere effects. Log GDP reveals the exponential nature of the wealth gap. Color by continent shows that the pattern holds within continents, not just between them."},

"24": {"title":"Megacity Distance vs Life Expectancy",
"show":"Distance to nearest megacity (>10M population) vs life expectancy for each country.",
"queries":"Does proximity to major economic hubs correlate with health outcomes?",
"trends":"Countries near megacities (low distance) show higher life expectancy on average. Remote countries (high distance) cluster at lower life expectancy. This reflects the 'connectivity premium': proximity to centers of economic activity, medical infrastructure, and trade routes.",
"components":"Distance is computed as haversine distance from capital to the nearest of 20 megacities. The scatter reveals that geographic isolation compounds economic disadvantage."},

"25": {"title":"Climate Zones and Child Survival",
"show":"Under-5 mortality vs absolute latitude, colored by climate zone (Tropical, Subtropical, Temperate, Subarctic).",
"queries":"Does climate zone predict child survival? Is the tropical disease burden visible in mortality data?",
"trends":"Tropical countries (red/orange) cluster at high mortality. Temperate/Subarctic countries (blue/green) cluster at low mortality. The transition zone (Subtropical) shows the most variance, suggesting other factors (governance, healthcare) matter more within the tropics.",
"components":"Climate zone classification adds a categorical dimension to the latitude gradient. The color grouping makes within-zone variation visible."},

"26": {"title":"The Cost of Conflict",
"show":"Dual-panel scatter: UCDP conflict intensity (0-10 scale) vs GDP per capita (left) and vs life expectancy (right).",
"queries":"How much does armed conflict cost in economic and human terms?",
"trends":"Conflict-affected countries cluster at low GDP and low life expectancy. Even moderate conflict intensity (3-5) is associated with dramatically worse outcomes. The relationship is not just correlation: conflict destroys infrastructure, displaces populations, and diverts resources.",
"components":"The dual panel allows simultaneous assessment of economic and health costs. Conflict intensity from UCDP/PRIO provides a credible, standardized measure."},

"27": {"title":"The Sea Access Premium",
"show":"Box plots comparing GDP per capita distributions for landlocked vs coastal countries, by continent.",
"queries":"Do landlocked countries face a systematic economic penalty? Does it vary by continent?",
"trends":"Landlocked countries have lower median GDP on every continent. The penalty is largest in Africa (where 16 landlocked nations face infrastructure and trade barriers) and smallest in Europe (where strong institutions and EU integration partly compensate).",
"components":"Box plots show median, quartiles, and outliers. Continental faceting prevents the global pattern from masking regional variation."},

"28": {"title":"The Digital-Geographic Divide",
"show":"Internet usage (%) vs absolute latitude, colored by income group.",
"queries":"Is the digital divide geographic or economic? Can latitude predict connectivity?",
"trends":"Income group explains most of the variance, but latitude adds explanatory power: even within the same income group, higher-latitude countries tend to have slightly higher internet penetration (possibly due to infrastructure density).",
"components":"Color by income group disentangles the latitude effect from the wealth effect. The scatter reveals that the digital divide parallels the broader development gradient."},

"29": {"title":"Fertility Rates by Climate Zone",
"show":"Violin plots of fertility rate distributions across four climate zones: Tropical, Subtropical, Temperate, Subarctic.",
"queries":"Does climate zone predict fertility patterns? How wide is the within-zone variance?",
"trends":"Tropical countries show the widest distribution and highest median (3-5 births/woman). Temperate countries cluster tightly at replacement level (1.2-1.8). The violin shape reveals that even within the tropics, there is significant variation (some tropical countries have sub-replacement fertility).",
"components":"Violin width = density of countries at that fertility level. Wider sections = more countries at that value. Individual points are visible for outliers."},

"30": {"title":"Urbanization vs Clean Energy",
"show":"Scatter of urban population percentage vs renewable energy share.",
"queries":"Does urbanization drive renewable energy adoption, or reduce it?",
"trends":"Counterintuitively, the most urbanized countries often show lower renewable percentages (because urban energy consumption is dominated by fossil fuels and grid electricity). Highly rural countries show high renewable percentages (biomass dependence). The pattern reverses for wealthy nations investing in modern renewables.",
"components":"The scatter reveals a non-linear relationship that challenges simplistic 'cities = green' narratives."},

"31": {"title":"The Arid Belt: Water Stress by Latitude",
"show":"Freshwater withdrawals (% of renewable resources) vs absolute latitude.",
"queries":"Is there a specific latitude band where water stress concentrates?",
"trends":"The 20-35 degree latitude band (subtropical deserts) shows dramatic water stress clustering. Countries near the equator (0-10 degrees) generally have abundant rainfall. High-latitude countries (>50 degrees) have lower stress due to lower evapotranspiration.",
"components":"The highlighted arid belt zone makes the geographic pattern immediately legible. Outliers (e.g., Israel at high stress despite technology) reveal the limits of geography."},

"32": {"title":"Healthcare Access by Latitude",
"show":"Physicians per 1,000 population vs distance from the equator.",
"queries":"Is healthcare workforce distribution geographic? Where are the healthcare deserts?",
"trends":"A strong positive correlation: countries further from the equator have more physicians per capita. Sub-Saharan Africa (near equator) has severe physician shortages (<0.5 per 1,000). Former Soviet states show high physician density due to historical centralized healthcare systems.",
"components":"The scatter reveals that the healthcare workforce mirrors the broader development gradient. Exceptions (Cuba: near equator, high physician density) highlight the role of policy."},

"33": {"title":"Education vs Global Connectivity",
"show":"Primary school completion rate vs distance to nearest megacity.",
"queries":"Does geographic isolation predict educational outcomes?",
"trends":"Countries near megacities show higher completion rates on average. Remote countries (far from economic hubs) tend to have lower educational attainment. The relationship is modest: many other factors (government investment, cultural norms) mediate.",
"components":"Distance to megacity serves as a proxy for 'global connectivity' rather than just geographic isolation."},

"34": {"title":"Trade Across the East-West Axis",
"show":"Trade openness (exports+imports as % GDP) vs longitude.",
"queries":"Is there an East-West pattern in trade integration?",
"trends":"The highest trade openness concentrates around 0-30 degrees East (European trade hubs) and 100-120 degrees East (East Asian export economies). The Americas (negative longitude) show moderate openness. The pattern reflects the two major trade blocs: EU and East Asian supply chains.",
"components":"Longitude as an axis is unusual in economic analysis, making this a novel perspective on global trade geography."},

"35": {"title":"Forest Cover and Maternal Health",
"show":"Maternal mortality ratio vs forest cover percentage.",
"queries":"Is there a correlation between environmental and health outcomes?",
"trends":"Countries with very high forest cover (Congo Basin, Amazon) show high maternal mortality, likely reflecting rural remoteness and limited healthcare access. The relationship is U-shaped: countries with moderate forest cover (temperate developed nations) show the lowest mortality.",
"components":"This chart challenges 'green = good' assumptions: high forest cover often means low infrastructure density, which is lethal for maternal health."},

"36": {"title":"Remittance Dependency by Geography",
"show":"Remittances (% of GDP) vs absolute latitude.",
"queries":"Is remittance dependency a geographic phenomenon?",
"trends":"Low-latitude countries show the highest dependency, reflecting the pattern of South-to-North labor migration. The relationship is negative: closer to the equator = higher remittance dependency. This maps onto the broader 'tropical poverty trap' narrative.",
"components":"The geographic pattern suggests that remittance flows partially compensate for the latitude-wealth gradient, transferring wealth from high-latitude destination countries to low-latitude origin countries."},

"37": {"title":"LISA Cluster Map: Electoral Patterns",
"show":"Dual-panel map of Local Indicators of Spatial Association (LISA) for voter turnout (left) and victory margin (right) across 543 Indian parliamentary constituencies.",
"queries":"Is voter turnout spatially clustered? Are competitive races (low margin) concentrated in specific regions?",
"trends":"Turnout shows very strong clustering (Moran's I = 0.64): southern India is a turnout hot spot (High-High, red), while the Hindi belt (UP, Bihar) is a cold spot (Low-Low, blue). Margins show moderate clustering (I = 0.26), with competitive races concentrating in swing states.",
"components":"LISA classifies each constituency into four categories: Hot Spot (high value near high values), Cold Spot (low near low), and two types of spatial outliers. Significance tested at p < 0.05 with 999 permutations. KNN k=8 spatial weights."},

"38": {"title":"Constituency Area vs Electoral Outcomes",
"show":"Dual scatter: constituency area (log km2) vs turnout (left) and vs victory margin (right), colored by alliance.",
"queries":"Do larger constituencies have lower turnout? Is the size of a constituency related to how competitive the race is?",
"trends":"A negative slope for area vs turnout: larger constituencies show systematically lower turnout, likely due to logistical barriers (travel distance to polling stations, sparse infrastructure). Area vs margin shows no strong pattern. Area itself is spatially autocorrelated (I = 0.16).",
"components":"Log scale on area compresses the extreme range (Ladakh: 180,000 km2 vs urban seats: <100 km2). Alliance coloring reveals no systematic partisan difference in the area-turnout relationship."},

"39": {"title":"Moran's I Spatial Lag Scatterplot",
"show":"Dual-panel Moran scatterplot: standardized values (X) vs spatial lag (Y, neighbors' mean) for turnout (left) and margin (right).",
"queries":"How strong is the geographic clustering of electoral behavior? Is India's political geography fundamentally spatial?",
"trends":"Turnout: steep positive slope (I = 0.64) with most points in the HH (red, top-right) and LL (blue, bottom-left) quadrants. This means neighboring constituencies have similar turnout levels. Margin: shallower slope (I = 0.26), indicating moderate but significant clustering of competitive vs safe seats.",
"components":"The gold regression line's slope equals Moran's I. Points in HH/LL quadrants indicate spatial clustering. Points in HL/LH quadrants are spatial outliers (their value differs from their neighbors). Zero lines divide the four quadrants."},

"40": {"title":"Turnout Swing 2019 to 2024",
"show":"Map of turnout change between the 2019 and 2024 Lok Sabha elections. Blue = turnout rose. Red = turnout dropped. Size = magnitude of change.",
"queries":"Where did voter engagement decline between elections? Is disengagement spatially patterned?",
"trends":"National average swing was -1.4 percentage points (turnout fell overall). Red clusters (decline) are visible in parts of UP, Bihar, and Gujarat. Blue clusters (increase) appear in parts of West Bengal and the Northeast. The spatial clustering of disengagement suggests regional, not random, drivers.",
"components":"Diverging color scale (red-blue) centered at zero makes increases and decreases instantly distinguishable. Bubble size encodes magnitude so that large swings stand out."},

"41": {"title":"Center vs Periphery: Distance from Delhi",
"show":"Victory margin vs distance from Delhi (the political center) for each constituency. Color = alliance. Size = electorate.",
"queries":"Does distance from the national capital affect electoral competitiveness? Is there a center-periphery pattern?",
"trends":"No strong linear relationship, but the variance changes: constituencies near Delhi show a wider range of margins (some very safe, some very competitive), while distant constituencies are more uniformly distributed. This suggests that Delhi's political influence is not simply 'distance decay'.",
"components":"Distance in degrees is an approximation but captures the broad North-South and East-West variation. Alliance coloring reveals that NDA (saffron) dominates near Delhi while INDIA (blue) is more prevalent at greater distances."},

"42": {"title":"The Political Cylinder (3D)",
"show":"543 Indian constituencies mapped onto a rotating 3D cylinder. Height = latitude (south at bottom, north at top). Angular position = longitude. Color = winning alliance (NDA saffron, INDIA blue, Others grey). Octahedral shapes = women winners.",
"queries":"Can cylindrical projection reveal the North-South political divide more clearly than a flat map?",
"trends":"The cylinder immediately shows the geographic split: the lower half (south) is predominantly blue (INDIA alliance), the upper half (north) is predominantly saffron (NDA). The transition zone is visible as a mixed band around the middle of the cylinder.",
"components":"Drag to rotate. Scroll to zoom. Hover any node for constituency details. Women winners appear as pink octahedra, making their sparse distribution visible against the dense field of spheres."},

"43": {"title":"Development Globe (3D)",
"show":"196 countries on a slowly rotating 3D sphere with bars extruding outward. Three switchable metrics: GDP per capita, life expectancy, fertility rate. Color = continent.",
"queries":"What does the geography of development look like from space? How do the three metrics produce different global landscapes?",
"trends":"GDP mode: Northern hemisphere bars tower over the South. Life expectancy mode: the pattern is similar but more compressed. Fertility mode: the pattern inverts, with Africa and South Asia showing the tallest bars.",
"components":"Use the metric buttons at the top to switch between variables. Each switch reshapes the entire globe, making the contrast between metrics visceral. Drag to spin. Hover bars for data."},

"44": {"title":"The Double Helix of Indian Democracy (3D)",
"show":"NDA and INDIA alliance constituencies spiral upward in two DNA-like helices. South at bottom, north at top. Node size = victory margin. Tube backbones trace each alliance's geographic path.",
"queries":"Can the bipolar political geography of India be represented as a genetic code?",
"trends":"The NDA strand (saffron) is densely packed in the upper turns (Hindi belt). The INDIA strand (blue) dominates the lower turns (south and east). The two strands interweave in the middle turns (swing states).",
"components":"Drag to rotate. Scroll up/down to traverse the helix. The double-helix metaphor makes the North-South split visceral: two opposing political forces spiral through the same geography."},

"45": {"title":"Continental Development Space (3D)",
"show":"196 countries in a 3D scatter. X = GDP per capita (log). Y = life expectancy. Z = fertility rate. Size = population. Color = continent.",
"queries":"Can three development dimensions be viewed simultaneously? What do the continental clusters look like in 3D?",
"trends":"Africa (cyan) forms a cloud in the high-fertility, low-GDP, low-lifeExp corner. Europe (green) occupies the opposite extreme. Asia (red) spans the widest range. The 3D perspective reveals that the three variables are strongly but not perfectly correlated.",
"components":"Click-drag to rotate. Scroll to zoom. The 3D view shows that some countries break the expected patterns: Gulf states have high GDP but moderate life expectancy and fertility."},

"46": {"title":"Women + Area Hypothesis",
"show":"Three panels: (1) box+strip plots of constituency area by winner gender, (2) population density vs margin with women highlighted, (3) category breakdown (GEN/SC/ST).",
"queries":"Are women winning in larger or smaller constituencies? Is population density a factor?",
"trends":"Women winners (pink) have a lower median area (3,324 km2) than men (4,073 km2). Mann-Whitney U test is significant. Women tend to win in denser, more urban constituencies. SC-reserved seats show the highest women representation at 15.5%.",
"components":"Panel 1 directly tests the area hypothesis. Panel 2 adds the density dimension. Panel 3 breaks it down by reservation category, revealing that SC seats are slightly more favorable for women."},

"47": {"title":"3D Spatial Histogram: India",
"show":"3D bars rising from constituency locations over India. Height = selected metric (electorate ratio, turnout, or margin). Color = alliance. Switchable with buttons.",
"queries":"Can a 3D histogram superimposed on geography reveal patterns that flat maps cannot?",
"trends":"Electorate ratio mode reveals dramatic North-South inequality: northern bars tower (voters are underrepresented) while southern bars are shorter. Turnout mode shows the inverse: southern India has taller bars (higher turnout). The 3D perspective makes both patterns intuitive.",
"components":"Three switchable metrics via buttons. Alliance coloring persists across all modes. Drag to orbit. The geographic footprint anchors the data spatially."},

"48": {"title":"Alliance LISA + Women Bivariate",
"show":"Left: LISA clusters on NDA/INDIA alignment (I = 0.37). Right: state bubble chart of NDA seat share vs women's representation.",
"queries":"Are NDA and INDIA strongholds spatially clustered? Does alliance geography correlate with women's representation?",
"trends":"Left panel: orange = NDA strongholds (Hindi belt), blue = INDIA strongholds (south, east). 110 NDA and 112 INDIA strongholds identified at p < 0.05. Right panel: no strong correlation between alliance dominance and women's representation. Women are underrepresented regardless of which alliance wins.",
"components":"The dual panel tests whether women's outcomes are driven by alliance geography. The 33% reservation target line in the right panel contextualizes how far every state falls short."},

"49": {"title":"GDP Bar Chart Race",
"show":"Animated bar chart racing top 15 nations by GDP per capita from 1992 to 2022. Countries overtake each other in real time.",
"queries":"Which countries have risen fastest? Have any fallen?",
"trends":"Gulf states (Qatar, UAE) and city-states (Singapore, Hong Kong) consistently dominate. Ireland's dramatic rise from mid-table to top 3 reflects its role as a corporate tax haven. Norway climbs on oil wealth. The US remains a steady top-5 presence.",
"components":"Press play and watch bars slide past each other. The percentage labels show both absolute values and relative progress. Color = continent."},

"50": {"title":"India Electoral Swing: 2019 vs 2024",
"show":"Animated geo scatter toggling between the 2019 and 2024 elections. Bubbles morph as margins shift and alliances realign.",
"queries":"How did the political map change between elections? Where were the biggest swings?",
"trends":"The animation reveals NDA contraction in parts of UP and Maharashtra, INDIA gains in West Bengal and the South. Bubble sizes (margin) change dramatically for many constituencies, showing that individual races swung heavily even if the national picture was more stable.",
"components":"Toggle between election years with the animation control. The transition animation (1.5 seconds) makes the shift visible as bubble migration."},

"51": {"title":"The Great Fertility Collapse",
"show":"Year-by-year animated bubble chart of fertility rate vs life expectancy for all countries, 1990-2023 (33 frames).",
"queries":"Is the world converging toward low fertility? Which countries are still in early demographic transition?",
"trends":"The most dramatic visual: watch the entire cloud of bubbles migrate from the upper-left (high fertility, low lifeExp) toward the lower-right (low fertility, high lifeExp). Africa's descent is the most visible ongoing shift. By 2023, only a handful of countries exceed 5 births/woman.",
"components":"Each frame is one year. Bubble size = population (China and India dominate). The animation speed can be adjusted with the play controls. Press play and watch 33 years of demographic transformation unfold."},

"52": {"title":"The Mortality Plunge",
"show":"Animated global choropleth of under-5 mortality (per 1,000 live births) from 1990 to 2022.",
"queries":"Where has child survival improved most? Is the improvement accelerating?",
"trends":"Sub-Saharan Africa starts deep red (200+ per 1,000) and gradually, visibly lightens. South Asia shows the most dramatic improvement (India dropped from 130 to 27). The animation makes the pace of change tangible: faster post-2000 (Millennium Development Goals era) than pre-2000.",
"components":"The YlOrRd color scale makes improvements visible as lightening. The animation slider lets you scrub to specific years. Missing data appears as grey."},

"53": {"title":"Continental Convergence (and Divergence)",
"show":"Dual-panel temporal line chart. Left: life expectancy by continent (converging). Right: GDP per capita by continent (diverging).",
"queries":"Are continents becoming more similar or more different? In which dimensions?",
"trends":"Health convergence: Africa is catching up (life expectancy rose from 50 to 65+ years). Wealth divergence: the gap between Africa and Europe/Americas is widening. Asia's GDP trajectory is the steepest, but it started from a low base. The two panels together tell a story of partial convergence.",
"components":"Population-weighted averages mean these lines reflect what the average person experiences. The contrast between converging (left) and diverging (right) panels is the key insight."},

"54": {"title":"Women's LISA: Spatial Clustering",
"show":"Left: LISA map of women winners (Moran's I = 0.06, p < 0.001). Right: area vs density scatter with women highlighted as pink diamonds.",
"queries":"Do women winners cluster spatially? Is there a geographic pattern to where women win?",
"trends":"Women's spatial autocorrelation is weak (I = 0.06) but statistically significant: there are small clusters where multiple adjacent constituencies elected women. The right panel confirms that women win in a specific zone of the area-density space: smaller, denser constituencies.",
"components":"Left panel uses LISA classification (pink diamonds = women clusters). Right panel provides the analytical complement: area vs density as explanatory variables."},

"55": {"title":"India Party Flip Pulse (3D)",
"show":"214 constituencies that changed party between 2019 and 2024 pulse with golden rings. Stable seats glow softly. 3D view over India.",
"queries":"Where did party control flip? Is party switching spatially clustered?",
"trends":"Flipped seats concentrate in specific corridors: western UP (BJP losses), parts of Maharashtra (alliance reshuffling), and West Bengal (TMC consolidation). The pulsing golden rings make flipped seats impossible to miss against the stable background.",
"components":"The ring animation (sinusoidal scale and opacity) creates a breathing effect. Alliance colors persist for stable seats. Hover for detailed swing data including margin and turnout change."},

"56": {"title":"The Development Spiral (3D)",
"show":"Countries trace spiral paths through time (1952-2007, Gapminder data). Radius = log(GDP per capita). Height = life expectancy. Color = continent. Slider scrubs through years.",
"queries":"What does a country's development trajectory look like as a 3D path through time?",
"trends":"Countries spiral outward (increasing GDP) and upward (increasing life expectancy) over time. African countries show the tightest, lowest spirals. European countries show wide, high spirals. The slider lets you see where each country was at any historical moment.",
"components":"Use the year slider at the bottom to move the position dots along their trajectories. Drag to rotate the spiral. The tube backbones show each country's historical path."},

"57": {"title":"Coral Reefs Under Siege: Temporal Pulse",
"show":"Dual-zone visualization: reef map (top, 27 systems by threat) paired with SST anomaly timeline (bottom, 1980-2024).",
"queries":"How does rising ocean temperature drive coral bleaching? Is the pace accelerating?",
"trends":"The timeline shows accelerating warming with tighter intervals between mass bleaching events (1998, 2010, 2016, 2024). The map shows that reefs in all ocean basins are affected. The dual view makes the causal chain visible: warming (bottom) drives bleaching (top).",
"components":"The top map is a spatial view of reef vulnerability. The bottom timeline adds the temporal dimension. Together they answer both 'where' and 'when'."},

"58": {"title":"Animated Inequality (Gini Over Time)",
"show":"Animated choropleth of the Gini coefficient by 5-year bins from 1990 to 2020.",
"queries":"Is global inequality changing? Are any regions becoming more equal?",
"trends":"Latin America shows gradual improvement (Gini declining from 55-60 to 45-50). Sub-Saharan Africa remains stubbornly high. China's Gini rose sharply (increasing inequality during economic growth). Eastern Europe shows varied trajectories post-Soviet transition.",
"components":"Animation frames are 5-year bins (averaging available data). The RdYlGn_r color scale makes high inequality (red) and low inequality (green) immediately distinguishable."},

"59": {"title":"India Development Terrain (3D)",
"show":"30 Indian states as glowing pillars rising from geographic positions. 8 switchable metrics: HDI, GSDP, literacy, sex ratio, IMR, urbanization, forest cover, food production. Width = state area.",
"queries":"How do India's development indicators vary geographically? Which metric reveals the starkest disparities?",
"trends":"HDI mode: Kerala and Goa tower while Bihar and UP are short. Switching to sex ratio reveals a different geography: Haryana and Punjab shrink (poor sex ratio) while Kerala remains tall. Food production mode shows Punjab and UP dominating.",
"components":"8 metric buttons at top. Each click reshapes the entire terrain. Width encodes state area (UP and Rajasthan are wide). Color morphs from red (low) to green (high). Drag to orbit."},

"60": {"title":"India Food Geography 3D",
"show":"Rice production as green diamonds and wheat production as gold squares, placed at actual state lat/lon, with height = production in million tonnes.",
"queries":"Where does India grow its food? Is there a spatial division between rice and wheat?",
"trends":"Sharp geographic division: rice dominates in the south and east (Bengal, AP, UP eastern parts), wheat dominates in the north (Punjab, UP western parts, MP). The Green Revolution's geographic footprint is visible: Punjab towers in both crops. The 3D perspective makes the spatial separation vivid.",
"components":"Green diamonds = rice, gold squares = wheat. Height = production volume. Geographic placement preserves the actual spatial distribution. Drag to rotate for different perspectives."},

"61": {"title":"Literacy-Gender DNA Helix (3D)",
"show":"Two helical strands: literacy (cyan) and sex ratio (magenta), with states ordered by HDI from bottom to top. Bridges connect the same state across strands.",
"queries":"Do literacy and gender equity move together across Indian states? Where do they diverge?",
"trends":"Kerala (near top): both strands bulge outward (high literacy AND high sex ratio). Bihar (near bottom): both shrink. Haryana creates a dramatic asymmetry: the literacy strand extends normally but the sex ratio strand collapses (OK education, terrible gender ratio). The mismatch is the story.",
"components":"Bridges show co-occurrence. When both strands align (bulge together), literacy and gender equity reinforce each other. When they diverge (one bulges, other shrinks), there is a structural problem."},

"62": {"title":"Constituency Aurora (3D)",
"show":"543 constituencies as breathing particles. Vertical oscillation = turnout-proportional. Glow intensity = margin. Color = alliance. High-margin seats emit vertical beams.",
"queries":"What does Indian democracy look like as a living, breathing organism?",
"trends":"The aurora effect reveals geographic patterns: the southern region breathes with higher amplitude (higher turnout), while the northern region oscillates more gently. Vertical beams (high-margin seats) cluster in certain regions, indicating safe seats.",
"components":"The breathing animation (sinusoidal oscillation per constituency) creates an organic, living visualization. Halos pulse. Beams mark dominance. The overall effect is a living map of democratic intensity."},

"63": {"title":"India Socioeconomic Landscape 3D",
"show":"X = literacy, Y = GSDP per capita, Z = HDI. Size = population. Color = region (South/Central/North/Far North). Drop lines to HDI floor.",
"queries":"How do literacy, wealth, and human development interact across Indian states?",
"trends":"Southern states (red) cluster at high literacy, moderate GSDP, high HDI. Northern states (green/cyan) cluster at lower literacy, lower GSDP, lower HDI. Delhi is an outlier: high GSDP but moderate HDI. Bihar occupies the lowest position on all three axes.",
"components":"Drop lines make the Z-axis (HDI) readable by showing the 'height' above the floor. Rotate to see different projections. The 3D scatter reveals that the three variables are positively correlated but not identical."},

"64": {"title":"Gender-Development Nexus 3D",
"show":"X = sex ratio (F per 1000 M). Y = infant mortality (reversed: lower = better = higher on screen). Z = literacy. Color = sex ratio (red to green).",
"queries":"Can the gender-development relationship be visualized as a 3D space? Where do states cluster?",
"trends":"Kerala sits at the ideal corner: green (high sex ratio), high on screen (low IMR), high literacy. Haryana and Delhi sit at the alarming opposite: red (low sex ratio), low literacy, worse IMR. The 3D perspective makes the gender gap a spatial chasm you can rotate around.",
"components":"Reversed Y-axis (IMR) makes 'up = better' intuitive. Color gradient (red = dangerous sex ratio, green = healthy) adds a fourth dimension. Population sizing shows which states affect the most people."},

"65": {"title":"The Silence Map",
"show":"All 543 constituencies on the India map. Red X markers for the 152 where no woman filed candidacy. Color gradient for others: orange (1 woman) to green (4+ women).",
"queries":"Where in India do women not even appear on the ballot? Is the absence geographic?",
"trends":"152 constituencies (28%) had zero women candidates. The red Xs cluster in parts of UP, Bihar, Rajasthan, and Maharashtra: the Hindi heartland. Southern and northeastern states show more green (more women candidates). Urban constituencies tend to have more women filing.",
"components":"The X symbol makes absences impossible to miss. The four-tier color scheme (red/orange/yellow/green) creates a clear gradient from worst (zero) to best (4+). Hover for detailed candidacy counts."},

"66": {"title":"The Gauntlet: A Woman's Path Through Elections",
"show":"Interactive funnel chart showing the stages of elimination: all candidates, women who filed, women who saved deposit, women who won.",
"queries":"What are a woman's odds at each stage of the electoral process?",
"trends":"~8,360 total candidates. Only 458 (5.5%) were women. Of those, 325 (71%) lost their deposit (got < 1/6 of votes). Only 47 won. The funnel narrows catastrophically at each stage. The deposit forfeiture rate is the single most devastating filter.",
"components":"Funnel width = count at each stage. Percentage labels show both initial (of all candidates) and previous-stage (how many survived this filter). The visual makes the brutal attrition tangible."},

"67": {"title":"Gender Gap in the Electorate",
"show":"Diverging horizontal bar chart: female voters per 1,000 male voters, state by state. Gold dashed line = parity (1000).",
"queries":"In which states are women under-registered as voters? Where do women outnumber men on voter rolls?",
"trends":"Bihar (907), Haryana, J&K have the worst gender gaps in voter registration. Kerala (1,084), Meghalaya, Mizoram, AP, and Goa exceed parity (more women registered than men). The gender gap in the electorate precedes and compounds the gender gap in candidacy.",
"components":"Green bars = above parity. Red bars = below. The gold parity line at 1000 makes the divide immediately legible. The diverging format emphasizes both surplus and deficit."},

"68": {"title":"The Deposit Forfeiture Massacre",
"show":"Strip/jitter plot where every woman candidate is a dot, grouped by outcome: Deposit Forfeited (red), Lost but kept deposit (gold), Won (green).",
"queries":"What does the distribution of women's electoral performance look like? Are most women candidates competitive?",
"trends":"The red column (325 dots) is a wall. Most forfeited women got < 2% of votes, indicating they were marginal or frivolous candidates. The gold column (86 dots) shows women who were competitive but lost. The green column (47 dots) is sparse but shows women who won decisively (20-50% vote share).",
"components":"Each dot is hoverable with the candidate's actual name, party, constituency, and vote count. The jitter prevents overlap. The log Y-axis reveals the distribution across the full range of vote shares."},

"69": {"title":"State Scoreboard: Three Dimensions",
"show":"Triple-panel horizontal bar chart. Left: women elected per state. Center: deposit forfeit rate. Right: voter gender ratio.",
"queries":"Which states are worst for women across multiple dimensions simultaneously?",
"trends":"14 states elected zero women. Kerala elected zero women despite having India's best gender ratio (1,084). Some states with 100% forfeit rates simply had too few women candidates to produce winners. The three panels together reveal that no single metric tells the full story.",
"components":"Each panel uses its own color scale. The side-by-side comparison forces the viewer to consider all three dimensions together. States are sorted by women elected (left panel)."},

"70": {"title":"Women Candidature Terrain 3D",
"show":"Plotly 3D scatter over India. Height = % women candidates per constituency. Color = red (zero) through green (high). Red X markers on the floor for zero-women seats.",
"queries":"What does the geography of women's exclusion look like in 3D?",
"trends":"Vast flat red deserts (zero-women zones in UP, Bihar, Rajasthan) with occasional green peaks (urban constituencies, southern India). The 3D perspective makes the sparsity of women's participation tangible: you can rotate the terrain and see that most of India sits at or near the red floor.",
"components":"Height = percentage, not count. Color reinforces the height encoding for instant readability. Red X markers pinned to z=0 for constituencies where no woman ran. Drag to orbit for different perspectives."},

"71": {"title":"Delimitation Simulator",
"show":"Animated scatter: current seats (X) vs population-proportional new seats (Y), slider from 543 to 1000 total seats. Color = region.",
"queries":"If India's 543 seats were redistributed purely by population, who gains and who loses? How does increasing total seats affect the outcome?",
"trends":"Southern states (red) consistently lose seats under proportional reallocation because they controlled population growth. Northern states (green/yellow) gain because their populations grew faster. The gold diagonal = no change. Points above the diagonal = states that gain seats; below = states that lose.",
"components":"Drag the slider from 543 to 1000 to see how the scatter changes. More total seats slightly reduces the proportional shift but does not eliminate it. The animation makes the zero-sum nature of delimitation visible."},

"72": {"title":"Fiscal Returns: Rs per Rs 100 Paid",
"show":"Diverging bar chart showing how much each state gets back from the central government for every Rs 100 it pays in taxes.",
"queries":"Which states are net contributors to India's federal fisc? Which are net recipients? Is the pattern geographic?",
"trends":"Southern states (TN: Rs 29.7, MH: Rs 27.8, KA: Rs 37.3) get back far less than they pay. Northern states (Bihar: Rs 142.5, UP: Rs 118.3) and northeastern states (Arunachal: Rs 510.3) are massive net recipients. The 'double whammy': southern states lose seats in delimitation AND subsidize northern states fiscally.",
"components":"The gold break-even line at Rs 100 divides contributors (red, left) from recipients (green, right). Source: 15th Finance Commission recommendations."},

"73": {"title":"Women's Reservation Simulator",
"show":"Animated scatter: states plotted with Y = effective women % in parliament, slider from 0% to 100% reservation quota.",
"queries":"What would India's parliament look like with different levels of women's reservation?",
"trends":"At 0%: current reality (8.7% women). At 33% (the actual Reservation Bill): ~180 guaranteed women seats. At 50%: ~272 seats. At 100%: all 543. The animation shows every state's bubble rising uniformly as the quota increases. But the starting positions vary: states with existing women winners start higher.",
"components":"Bubble size = population. Color = region. The slider makes the counterfactual concrete: 'what if we had set the quota to X%?' Each click of the play button shows the next level."},

"74": {"title":"Moran's I Criteria Explorer",
"show":"Two curves: Moran's I as the weight shifts between (a) area vs population, and (b) women voters vs fiscal returns.",
"queries":"Which delimitation criteria produces the most equitable spatial distribution? Should area or population drive seat allocation?",
"trends":"The red curve (area vs population) shows that area-weighted allocation produces higher Moran's I (more clustering, less equitable). Population-weighted is slightly better. The cyan curve (women voters vs fiscal returns) explores alternative criteria. The gold zero line marks the ideal: no clustering.",
"components":"Lower Moran's I = more equitable dispersion. Negative I would mean perfect anti-clustering (ideal but unrealistic). The intersection of each curve with the zero line indicates the optimal weight balance."},

"75": {"title":"The Punishment Value (3D)",
"show":"3D scatter: X = fiscal return (Rs per 100 paid), Y = female voter %, Z = Lok Sabha seats. Color = punishment value (1 - 0.35 * fiscal / 100).",
"queries":"Which states face the worst combination of fiscal penalty, gender gap, and representational deficit?",
"trends":"Tamil Nadu and Maharashtra sit in the deep red zone: they pay the most tax (low fiscal return), have moderate female voter percentages, and face seat reductions under delimitation. Northeast states sit in the green zone: massive fiscal transfers compensate for small size. The 3D makes the triple burden tangible.",
"components":"Punishment value formula: 1 - 0.35 * (fiscal return / 100). A value near 1 means the state is severely punished. Near 0 or negative means the state receives generous transfers. Size = population."},

"76": {"title":"Representation Inequality",
"show":"Animated bar chart: electors per seat (millions) for each state, slider from 543 to 1000 total seats.",
"queries":"How unequal is voter representation? Does increasing total seats fix it?",
"trends":"At 543 seats: massive inequality. UP has ~2.4M voters per seat while Sikkim has ~0.4M. A vote in Sikkim is worth 6 times a vote in UP. As total seats increase toward 1000, the bars equalize because proportional allocation converges toward equal representation. Perfect equity = all bars the same height.",
"components":"The animation makes the convergence visible. Color = region. The tallest bars (most underrepresented) are in the most populous states (UP, Bihar, Maharashtra)."},

"77": {"title":"The Fiscal Spine",
"show":"States connected south-to-north by latitude on the India map. Node size = Lok Sabha seats. Color = fiscal return (red = contributor, green = recipient).",
"queries":"Is there a geographic spine of fiscal inequality running through India?",
"trends":"The spine traces a clear gradient: red nodes (contributors) at the southern end, green nodes (recipients) at the northern end. The transition happens roughly at the Vindhya range latitude. The largest nodes (most seats) are in the middle and north.",
"components":"The connecting line emphasizes the sequential, latitudinal nature of the fiscal gradient. Size encoding shows that the largest democratic weights (most seats) coincide with net recipient status."},

"78": {"title":"Democratic Real Estate Treemap",
"show":"Hierarchical treemap: Region > State. Area = Lok Sabha seats. Color = fiscal return (red = contributor, green = recipient).",
"queries":"How is India's democratic 'real estate' distributed? Do net contributors have proportional representation?",
"trends":"Central and East regions occupy the largest rectangles (UP, Bihar, MP = many seats). Southern region, despite paying the most tax (red), has a smaller combined area. The treemap makes the imbalance tangible: red rectangles (contributors) are smaller than green rectangles (recipients).",
"components":"Click a region to drill into state-level detail. Color intensity encodes fiscal return magnitude. Hover for detailed stats including women elected and population."},

"79": {"title":"Fiscal Returns vs Women's Representation",
"show":"Animated bubble plot: X = fiscal return (Rs per 100), Y = effective women %. Slider from 0% to 100% reservation. Color = region. Size = population.",
"queries":"Does the fiscal penalty faced by southern states correlate with their women's representation?",
"trends":"At 0% reservation: southern states (left, low fiscal return) have low women representation, similar to northern states (right, high fiscal return). As reservation increases, all bubbles rise uniformly. The fiscal position does not predict women's representation. The x-axis spread (fiscal return from Rs 15 to Rs 510) dwarfs the y-axis variation.",
"components":"Linear X-axis (fixed from earlier log-scale bug). The animation reveals that reservation is the only lever that reliably increases women's representation across all fiscal categories."},

"80": {"title":"Constituency Clustering: Women Candidates",
"show":"Every constituency color-coded by % women candidates on a continuous red-to-green scale. Size = total candidates.",
"queries":"Is there spatial clustering in where women contest? Can we see geographic exclusion zones?",
"trends":"Red zones (0% women) cluster in central UP, rural Bihar, and parts of Rajasthan and Maharashtra. Green pockets (15-30% women) appear in urban areas (Delhi, Mumbai, Bangalore constituencies) and parts of southern India. The clustering is not random: it follows social, cultural, and party-structural lines.",
"components":"Continuous color scale (unlike the binary Silence Map) reveals the gradient from complete exclusion to relative inclusion. Hover for exact percentages per constituency. Size encoding shows that larger candidate fields do not necessarily mean more women."},
}

def inject_panel(filepath, annotation):
    with open(filepath, "r") as f:
        html = f.read()
    
    # Skip if already annotated
    if "interp-panel" in html:
        return False
    
    panel_html = f'''
<div id="interp-panel" class="interp-panel">
<h3>{annotation["title"]}</h3>
<h4>What This Shows</h4>
<p>{annotation["show"]}</p>
<h4>Questions It Answers</h4>
<p>{annotation["queries"]}</p>
<h4>Key Trends</h4>
<div class="trend">{annotation["trends"]}</div>
<h4>Reading the Components</h4>
<p>{annotation["components"]}</p>
</div>
'''
    
    injection = PANEL_CSS + panel_html + PANEL_JS
    
    # Insert before </body>
    if "</body>" in html:
        html = html.replace("</body>", injection + "\n</body>")
    else:
        html += injection
    
    with open(filepath, "w") as f:
        f.write(html)
    return True

# Process all charts
count = 0
for filename in sorted(os.listdir(VIZ_DIR)):
    if not filename.endswith(".html") or filename == "index.html":
        continue
    num = filename.split("_")[0]
    if num not in ANNOTATIONS:
        continue
    filepath = os.path.join(VIZ_DIR, filename)
    if inject_panel(filepath, ANNOTATIONS[num]):
        count += 1

print(f"Annotated {count} charts out of {len(ANNOTATIONS)} defined")
print(f"Total HTML files: {len([f for f in os.listdir(VIZ_DIR) if f.endswith('.html') and f != 'index.html'])}")
