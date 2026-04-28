#!/usr/bin/env python3
"""Phase 2: Deep academic interpretation guides for charts 16-36.
Covers Money & Trade, Environment, Nations Bubble Map, and all 14 Geo-Variable Analysis charts."""

import os, re

VIZ_DIR = "visualizations"

GUIDE_CSS = '''<!--ATLAS-GUIDE-START-->
<style>
.guide{position:relative;z-index:1;background:#080B13;padding:40px 5% 60px;color:#C8D0DA;
font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif;font-size:.84rem;line-height:1.8;border-top:2px solid #151d2e}
.guide-inner{max-width:1100px;margin:0 auto}
.guide h2{color:#00D5E0;font-size:1.2rem;font-weight:700;margin:0 0 4px;font-family:'Playfair Display',Georgia,serif}
.guide .tagline{color:#FF5872;font-size:.93rem;font-weight:600;margin:0 0 18px;font-style:italic}
.guide h3{color:#FFD700;font-size:.88rem;font-weight:700;margin:26px 0 6px;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid #1a2233;padding-bottom:4px}
.guide p{margin:0 0 11px;color:#B8C4D0;text-align:justify}
.guide .hl{background:#0f1520;border-left:3px solid #00D5E0;padding:12px 16px;margin:12px 0;border-radius:0 6px 6px 0}
.guide .warn{border-left-color:#FF5872}
.guide .gold{border-left-color:#FFD700}
.guide b{color:#E8ECF0}.guide em{color:#FFD700;font-style:normal}
.guide code{background:#1C2333;padding:1px 5px;border-radius:3px;font-size:.76rem;color:#00D5E0}
.guide .ref{font-size:.76rem;color:#7B8CA3;margin-top:20px;border-top:1px solid #1a2233;padding-top:10px}
.guide .two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:12px 0}
@media(max-width:900px){.guide .two-col{grid-template-columns:1fr}}
</style>'''

GUIDE_END = '<!--ATLAS-GUIDE-END-->'

G = {}

# ═══════════════════════════════════════════════════════════════════
# CHART 16: GDP per Capita Map
# ═══════════════════════════════════════════════════════════════════
G["16"] = '''
<h2>GDP per Capita: The Wealth Surface of the Planet</h2>
<p class="tagline">National income per person remains the most powerful single predictor of human welfare, despite everything it fails to measure.</p>

<h3>What You Are Seeing</h3>
<p>A choropleth map of GDP per capita in Purchasing Power Parity (PPP) international dollars. PPP adjustment corrects for differences in local price levels: a dollar in India buys more goods and services than a dollar in Norway, so PPP adjusts upward for low-price countries and downward for high-price ones. This makes cross-country comparisons more meaningful than market-exchange-rate GDP. The color gradient runs from deep red (lowest GDP per capita, typically below $2,000) through yellow to green (highest, above $50,000).</p>

<h3>The Geography of Wealth: Why It Looks Like This</h3>
<div class="hl">The spatial pattern of global GDP per capita is strikingly persistent. The broad contours visible today, wealthy temperate-zone nations flanking the North Atlantic and North Pacific, with a belt of poverty across the tropics, would be recognizable to an observer in 1900, or even 1800. This persistence has generated one of the most contentious debates in social science: <b>is geography destiny?</b> Three competing schools offer spatial explanations for why the wealth map looks the way it does. <b>Jeffrey Sachs (2001)</b> argues for direct geographic causation: tropical disease burden, low agricultural productivity in tropical soils, distance from navigable waterways, and landlockedness directly constrain economic growth. <b>Daron Acemoglu and James Robinson (2001, 2012)</b> argue that geography matters only indirectly, through its effect on institutions: European colonizers established extractive institutions in tropical disease-ridden colonies (where settlers died quickly) and inclusive institutions in temperate colonies (where settlers survived and demanded property rights and rule of law). The "reversal of fortune" among colonized nations (rich pre-colonial civilizations like the Aztec and Mughal empires became poor, while sparsely populated temperate colonies like the US and Australia became rich) supports the institutional channel. <b>Jared Diamond (1997)</b> takes the longest view, arguing that the east-west orientation of Eurasia facilitated crop and technology diffusion (because climate zones run east-west), while the north-south orientation of the Americas and Africa impeded it.</div>

<h3>The Middle-Income Trap as a Spatial Phenomenon</h3>
<div class="hl gold">Many countries that escaped deep poverty in the late 20th century appear "stuck" in the middle-income range ($5,000 to $15,000 per capita). Economists call this the <b>middle-income trap</b>. It has a spatial expression: countries in this band (much of Latin America, Southeast Asia, North Africa, Turkey, South Africa) cluster geographically, suggesting shared structural constraints. The trap arises when the strategies that propel low-income growth (cheap labor manufacturing, commodity exports, urbanization) are exhausted before the strategies needed for high-income growth (innovation, advanced services, institutional quality) are developed. The geographic clustering of trapped countries suggests that <b>regional factors</b>, including shared trade dependencies, parallel demographic trajectories, similar colonial institutional legacies, and neighborhood effects in institutional quality, play a role. East Asia's "flying geese" model (Japan, then South Korea, then Taiwan, then China, then Vietnam) represents the most successful regional escape from the trap, driven partly by geographic proximity enabling supply-chain integration.</div>

<h3>What GDP per Capita Misses</h3>
<p>GDP per capita is an average that conceals distribution. Qatar's GDP per capita (approximately $80,000) is among the world's highest, but this wealth is concentrated among citizens who comprise only 12% of the resident population; migrant workers (88%) live in conditions closer to those of low-income countries. Similarly, Equatorial Guinea has a GDP per capita above $15,000 (oil wealth) but a life expectancy of 59 years (because the oil income is captured by a tiny elite). The <b>Inequality-adjusted Human Development Index (IHDI)</b> corrects for this by discounting average achievements by the degree of inequality. Countries like the US and Saudi Arabia drop dramatically in IHDI rankings compared to HDI, while egalitarian countries like Norway and Japan barely change. The spatial map of IHDI would look notably different from the GDP map, with several resource-rich but unequal nations appearing much poorer in welfare terms.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The persistence of the geographic wealth pattern implies that <b>structural transformation is required, not just incremental growth</b>. For tropical nations caught in the Sachs poverty trap: investment in disease control (malaria eradication would free up 1.3% of GDP annually in affected nations), climate-resilient agriculture, and transport infrastructure connecting landlocked regions to global markets. For middle-income trapped nations: educational investment in STEM and innovation capacity, institutional reform (rule of law, property rights, anti-corruption), and regional trade integration to create the market scale needed for industrial upgrading. For wealthy nations: the challenge has shifted from growth to sustainability and inclusion, ensuring that aggregate wealth translates into broad-based welfare rather than elite capture. The geographic pattern is not immutable: South Korea was poorer than Ghana in 1960 and is now 15 times richer. But changing geographic destiny requires deliberate, sustained institutional transformation over decades.</div>

<p class="ref"><b>Key references:</b> Sachs, J. (2001). Tropical underdevelopment. NBER Working Paper 8119. | Acemoglu, D. & Robinson, J. (2012). <i>Why Nations Fail</i>. Crown Business. | Diamond, J. (1997). <i>Guns, Germs, and Steel</i>. W.W. Norton. | Gill, I. & Kharas, H. (2015). The middle-income trap turns ten. World Bank Policy Research Working Paper 7403.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 17: Trade Openness
# ═══════════════════════════════════════════════════════════════════
G["17"] = '''
<h2>Trade Openness: How Geography Shapes Economic Integration</h2>
<p class="tagline">Trade as a share of GDP reveals which nations are economic islands and which are embedded in global flows.</p>

<h3>What You Are Seeing</h3>
<p>A choropleth showing trade openness, defined as <b>(Exports + Imports) / GDP x 100</b>. This measures the degree to which a country's economy is integrated with global markets. Values range from below 30% (relatively closed economies like Brazil, the US, Japan) to above 300% (entrepot economies like Singapore and Hong Kong, where goods flow through for re-export).</p>

<h3>Why Size and Geography Determine Trade Openness</h3>
<div class="hl">The single strongest predictor of trade openness is <b>country size</b>. Large countries (US, China, Brazil, India) have low trade-to-GDP ratios because they possess large internal markets that absorb domestic production. Small countries (Singapore, Luxembourg, Belgium, Netherlands) have high ratios because their domestic markets are too small to absorb or produce the full range of goods they consume. This is not merely a statistical artifact; it reflects a deep economic logic formalized in <b>gravity models of trade</b> (Tinbergen, 1962): bilateral trade between two countries is proportional to the product of their economic sizes and inversely proportional to the distance between them. Geographic distance remains the strongest friction in international trade: doubling the distance between two countries reduces bilateral trade by approximately 50% (the "distance puzzle" that persists even in an era of cheap shipping and digital communication).</div>

<h3>The Spatial Structure of Trade Networks</h3>
<div class="hl gold">Global trade is not a uniform web; it is organized into <b>regional blocs</b> with dense intra-bloc connections and sparser inter-bloc links. Three mega-blocs dominate. <b>The European Single Market</b>: the EU's elimination of tariffs and harmonization of regulations created the densest trade network on Earth. Belgium's trade openness (above 160%) is incomprehensible outside this context: Belgium functions as a logistics hub within the European network. <b>The East Asian production network</b>: centered on China, with supply chains linking Japan, South Korea, Taiwan, and ASEAN nations in a tightly integrated manufacturing ecosystem. Components cross borders multiple times before final assembly, inflating trade-to-GDP ratios for all participants. <b>The NAFTA/USMCA zone</b>: US-Mexico-Canada, with particularly deep integration in automotive and agricultural supply chains. The geographic proximity of these trading partners is not coincidental: the gravity model predicts that trade intensity falls rapidly with distance, and the world's three densest trade blocs are also three of its most geographically compact regional groupings.</div>

<h3>Landlocked Countries: The Geography of Trade Exclusion</h3>
<p>The map reveals a systematic penalty for <b>landlocked countries</b>. Nations without a coastline (Bolivia, Paraguay, Ethiopia, Uganda, Central Asian states) consistently show lower trade openness than their coastal neighbors. Paul Collier (2007) estimated that being landlocked reduces trade volumes by approximately 50% and GDP growth by approximately 1.5 percentage points per year. The mechanism is straightforward: international trade is overwhelmingly waterborne (approximately 80% of global trade by volume moves by ship). Landlocked countries must transit through neighboring countries to reach ports, adding transport costs, border delays, and political risk. The spatial concentration of landlocked nations in Africa (16 out of 54) and Central Asia helps explain these regions' lower integration with global trade networks. The African Continental Free Trade Area (AfCFTA) aims to partially offset this by creating a continental market where landlocked nations can trade with neighbors rather than relying on distant overseas markets.</p>

<h3>Trade Openness and Vulnerability</h3>
<div class="hl warn">High trade openness is not unambiguously beneficial. It creates <b>exposure to external shocks</b>. Small, highly open economies (Singapore, Ireland, Belgium) experienced sharper GDP contractions during the 2008-2009 global financial crisis than larger, more closed economies (India, Brazil). Commodity-dependent small economies (Zambia with copper, Botswana with diamonds) are particularly vulnerable because their trade openness is concentrated in a single product whose price they do not control. The COVID-19 pandemic revealed another dimension of vulnerability: highly trade-open economies experienced more severe supply chain disruptions. The policy debate between "openness for efficiency" and "resilience through diversification" is fundamentally a spatial question: how much should a nation's economic geography be oriented outward (toward global supply chains) versus inward (toward domestic and regional self-sufficiency)?</div>

<p class="ref"><b>Key references:</b> Tinbergen, J. (1962). <i>Shaping the World Economy</i>. Twentieth Century Fund. | Collier, P. (2007). <i>The Bottom Billion</i>. Oxford UP. | Disdier, A.C. & Head, K. (2008). The puzzling persistence of the distance effect on bilateral trade. <i>Review of Economics and Statistics</i>, 90(1). | WTO (2023). <i>World Trade Report</i>.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 18: Remittances
# ═══════════════════════════════════════════════════════════════════
G["18"] = '''
<h2>Remittances: The Geography of Diaspora Capital</h2>
<p class="tagline">Migrants send more money home than all foreign aid combined. This map shows where that money flows.</p>

<h3>What You Are Seeing</h3>
<p>A choropleth showing personal remittances received as a percentage of GDP. Remittances are cross-border transfers from migrant workers to family members in their home countries. Countries colored darkest receive the most remittances relative to their economy. Values range from near zero (wealthy nations that are net senders) to above 30% (Tonga, Nepal, Tajikistan, where remittances are the single largest source of national income).</p>

<h3>The Spatial Logic of Remittance Corridors</h3>
<div class="hl">Global remittance flows are structured along <b>migration corridors</b> that follow geographic, linguistic, and colonial pathways. The largest corridors include: <b>US to Mexico/Central America</b> ($60 billion annually), reflecting geographic proximity and historical labor migration patterns. <b>Gulf States to South/Southeast Asia</b> ($100+ billion), reflecting the oil economy's demand for construction and service labor. <b>Europe to North Africa and Eastern Europe</b>, reflecting colonial ties (France to Morocco/Algeria/Tunisia) and EU labor mobility (Romania/Poland to Germany/UK). <b>Russia to Central Asia</b> (Tajikistan, Kyrgyzstan, Uzbekistan), a legacy of Soviet-era geographic integration. These corridors are not random: they follow the <b>gravity model of migration</b>, where migration flows are proportional to economic differentials and inversely proportional to geographic and cultural distance.</div>

<h3>Remittances vs Foreign Aid: The Spatial Comparison</h3>
<div class="hl gold">In 2023, global remittances to low- and middle-income countries exceeded $650 billion, roughly three times the total of Official Development Assistance (ODA, approximately $200 billion). Unlike aid, which is channeled through government institutions and often subject to political conditionality, remittances flow directly to households and communities. The <b>spatial distribution of remittances</b> is therefore fundamentally different from the spatial distribution of aid. Aid is concentrated in countries prioritized by donor geopolitics (historically, strategic allies of Western nations). Remittances are concentrated in countries with large diasporas, regardless of geopolitical alignment. This means that countries like the Philippines, Mexico, Egypt, and Pakistan receive enormous financial flows that are invisible in aid statistics but dwarf aid in their economic impact. The spatial targeting of remittances is also more granular than aid: remittances reach specific households in specific villages, creating micro-geographic patterns of development impact that no donor program can replicate.</div>

<h3>The "Left Behind" Communities</h3>
<p>Remittance dependence has a distinctive spatial footprint within sending countries. The regions that send the most migrants are typically <b>economically marginal but socially connected</b>: they have enough education and social networks to facilitate migration but not enough local economic opportunity to retain their working-age population. In Mexico, the states of Michoacan, Zacatecas, and Guanajuato send the most migrants and receive the most remittances. In the Philippines, the Visayas and rural Luzon. In Kerala, India, the Muslim-majority districts of Malappuram and Kozhikode send disproportionate numbers of workers to the Gulf. These "left behind" communities develop a distinctive economic structure: consumption-driven (remittances fund housing, education, healthcare), labor-scarce (working-age adults are abroad), and highly dependent on external conditions they cannot control (oil prices in the Gulf, immigration policy in the US or Europe).</p>

<h3>The Dutch Disease Risk</h3>
<div class="hl warn">Countries where remittances exceed 15 to 20% of GDP face a version of <b>Dutch Disease</b>: the inflow of foreign currency appreciates the real exchange rate, making the country's exports less competitive and its imports cheaper. This hollows out the tradeable sector (manufacturing, agriculture for export) while inflating the non-tradeable sector (construction, services, real estate). Tajikistan (remittances approximately 30% of GDP) and Nepal (approximately 25%) exhibit classic symptoms: booming construction sectors funded by Gulf remittances, declining agricultural output, and extreme vulnerability to any disruption in the migration corridor (as occurred when Gulf countries reduced foreign worker visas during COVID-19 and post-2020 Saudization policies). The spatial irony is that remittance dependence can transform productive agricultural landscapes into dormitory communities where the primary economic activity is waiting for monthly transfers.</div>

<p class="ref"><b>Key references:</b> World Bank (2023). <i>Migration and Development Brief</i>. | Ratha, D. (2003). Workers' remittances: An important and stable source of external development finance. <i>Global Development Finance</i>. | Acosta, P. et al. (2009). Remittances and the Dutch Disease. <i>Journal of International Economics</i>, 79(1). | Adams, R. & Page, J. (2005). Do international migration and remittances reduce poverty in developing countries? <i>World Development</i>, 33(10).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 19: Forest Cover
# ═══════════════════════════════════════════════════════════════════
G["19"] = '''
<h2>Forest Cover: The Shrinking Green Canopy</h2>
<p class="tagline">Forests cover 31% of Earth's land. Their spatial distribution is the result of climate, history, economics, and governance.</p>

<h3>What You Are Seeing</h3>
<p>A choropleth of forest area as a percentage of total land area for each country. Deep green indicates heavily forested nations (Suriname 97%, Gabon 91%, Finland 73%). Yellow to red indicates deforested or naturally treeless nations (Libya, Egypt, and the Gulf states have below 1%). The map encodes one of the most consequential environmental variables: the planet's terrestrial carbon sink, biodiversity reservoir, and hydrological regulator.</p>

<h3>Three Forest Geographies</h3>
<div class="hl">The world's forests fall into three geographic and ecological zones with very different dynamics. <b>Boreal forests</b> (Russia, Canada, Scandinavia) comprise the largest forest biome by area. They are relatively stable because the land they occupy has low agricultural value (short growing seasons, poor soils). Their primary threat is climate change itself: warming is accelerating wildfire frequency (Canada's 2023 fire season burned 18.5 million hectares, 7 times the annual average) and enabling northward expansion of bark beetles. <b>Temperate forests</b> (Europe, eastern US, China, Japan) are actually <em>expanding</em> through a process called the <b>forest transition</b>: as countries industrialize and urbanize, marginal farmland is abandoned and reverts to forest. Europe has more forest today than in 1900. <b>Tropical forests</b> (Amazon, Congo Basin, Southeast Asia, Indo-Malaya) are where the crisis is concentrated. Tropical deforestation accounts for approximately 95% of global net forest loss and approximately 10% of annual carbon emissions.</div>

<h3>The Forest Transition Curve: A Spatial-Temporal Model</h3>
<div class="hl gold">Alexander Mather (1992) proposed the <b>forest transition model</b>: countries follow a U-shaped curve where forest cover first declines during agricultural expansion, reaches a minimum during peak land clearance, and then recovers during industrialization as agriculture intensifies on less land and marginal land reverts to forest. The spatial pattern on this map captures countries at different points on this curve. <b>Left (declining)</b>: Brazil, Indonesia, DRC, Myanmar, currently in the deforestation phase. <b>Bottom (minimum)</b>: Haiti (2% forest cover), El Salvador, Philippines, countries that have already lost most of their forest. <b>Right (recovering)</b>: France, China, India, Vietnam, Costa Rica, countries where deliberate reforestation programs or natural regeneration have reversed the decline. The spatial pattern of the forest transition correlates with economic development: the poorest countries are typically in the declining phase (converting forest to farmland for survival), while middle-income and wealthy countries have passed the minimum and begun recovery.</div>

<h3>The Spatial Externalities of Deforestation</h3>
<p>Deforestation is not a local event; it has <b>spatial externalities</b> that extend far beyond the cleared area. Tropical forests generate approximately 30 to 50% of their own rainfall through evapotranspiration (the "flying rivers" phenomenon). Deforestation in the Amazon reduces rainfall not only locally but across the entire basin and potentially as far as the Argentine Pampas, threatening agriculture thousands of kilometers away. Research by Antonio Nobre (2014) estimated that the Amazon recycles approximately 20 trillion liters of water per day through transpiration, more than the Amazon River itself discharges into the Atlantic. Deforestation in the Congo Basin similarly affects rainfall patterns across East Africa. These <b>teleconnections</b> mean that forest loss in one country can reduce agricultural productivity in another, creating cross-border environmental externalities that no national policy can address alone.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The spatial concentration of deforestation in a relatively small number of countries (Brazil, DRC, Indonesia, and Bolivia account for over 50% of global tropical forest loss) means that <b>targeted policy interventions in a handful of nations could dramatically alter the global trajectory</b>. The most effective interventions documented to date include: <b>Brazil's DETER system</b> (satellite-based deforestation detection enabling rapid enforcement, which reduced Amazon deforestation by 80% between 2004 and 2012 before enforcement weakened); <b>Costa Rica's Payment for Ecosystem Services (PES)</b> program (paying landowners $64/hectare/year to maintain forest, which reversed deforestation and doubled forest cover from 26% to 52% over three decades); and <b>Indonesia's moratorium on new palm oil and logging concessions</b> (partially effective but undermined by enforcement gaps). The REDD+ mechanism (Reducing Emissions from Deforestation and Forest Degradation) attempts to create a global market for the carbon storage services that tropical forests provide, but has been hampered by monitoring challenges, tenure disputes, and insufficient pricing of carbon. The fundamental spatial policy question is whether the global benefits of tropical forests (carbon storage, biodiversity, hydrological regulation) can be monetized at a level sufficient to outbid the alternative land uses (cattle ranching, palm oil, soy) that drive deforestation.</div>

<p class="ref"><b>Key references:</b> Mather, A. (1992). The forest transition. <i>Area</i>, 24(4). | Nobre, A. (2014). <i>The Future Climate of Amazonia</i>. INPE. | Hansen, M. et al. (2013). High-resolution global maps of 21st-century forest cover change. <i>Science</i>, 342(6160). | Engel, S. et al. (2008). Designing payments for environmental services in theory and practice. <i>Ecological Economics</i>, 65(4).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 20: Renewable Energy
# ═══════════════════════════════════════════════════════════════════
G["20"] = '''
<h2>Renewable Energy Share: The Geography of the Energy Transition</h2>
<p class="tagline">Which nations run on renewables, and why? The answer is written in their topography, latitude, and political economy.</p>

<h3>What You Are Seeing</h3>
<p>A choropleth showing renewable energy as a percentage of total final energy consumption. This includes hydropower, solar, wind, geothermal, and biomass. Countries range from near-zero (oil-producing Gulf states where cheap fossil fuel eliminates the economic incentive for renewables) to near-100% (Iceland, which runs almost entirely on geothermal and hydropower). The spatial pattern is strikingly different from the maps of wealth or development, because renewable potential depends on <b>physical geography</b>, not economic geography.</p>

<h3>Geography Determines Renewable Potential</h3>
<div class="hl">Each renewable technology has a distinct geographic signature. <b>Hydropower</b> requires elevation gradients and reliable precipitation, favoring mountainous countries with high rainfall (Norway, Brazil, DRC, Nepal, Bhutan). Countries that appear bright green on this map often owe their status primarily to hydro: Brazil's Itaipu dam alone generates 75 TWh/year. <b>Solar</b> potential is a function of latitude and cloud cover: the Sahara, Arabian Peninsula, Australian outback, and Indian desert receive 5 to 7 kWh/m2/day of irradiance, roughly double that of Northern Europe. <b>Wind</b> potential concentrates along coastlines, mountain ridgelines, and specific atmospheric convergence zones: the North Sea, Patagonia, the US Great Plains, and the Horn of Africa are among the world's best wind resources. <b>Geothermal</b> is the most spatially restricted, available only along tectonic plate boundaries: Iceland, Kenya's Rift Valley, the Philippines, Indonesia, and parts of Central America. This geographic specificity means that <b>the optimal energy mix is fundamentally a spatial variable</b>: no single renewable technology is universally best.</div>

<h3>The Nordic Paradox</h3>
<div class="hl gold">The Nordic countries illustrate how geography creates renewable advantage. <b>Norway</b> (98% renewable electricity) benefits from abundant hydropower potential in its fjord-cut, glacier-fed topography. <b>Iceland</b> (100% renewable electricity) sits on the Mid-Atlantic Ridge, giving it virtually unlimited geothermal energy. <b>Denmark</b>, lacking mountains and volcanoes, invested instead in <b>wind power</b>, exploiting its flat, windy North Sea coastline to become the world leader in wind energy technology. <b>Sweden and Finland</b> combine hydro, wind, and biomass (from their vast forests). The paradox is that these nations, located at high latitudes with limited solar resource, have achieved some of the world's highest renewable shares, not despite their geography but because of it. The lesson is that <b>renewable energy strategy must be adapted to geographic endowment</b>, not copied from other countries' templates.</div>

<h3>The Fossil Fuel Lock-in: Geographic and Political Economy</h3>
<p>Countries that appear red on this map (low renewable share) are predominantly <b>fossil fuel producers</b> (Saudi Arabia, Russia, Qatar, Kuwait, Iraq) or <b>fossil fuel dependent developing nations</b> (South Africa with its abundant coal). The explanation is partly geographic (nations with large fossil fuel reserves have cheap energy that makes renewables uncompetitive without policy intervention) and partly political economy (fossil fuel rents create powerful constituencies, the so-called "petrostate" phenomenon, that resist energy transition). The <b>resource curse</b> extends to energy policy: oil-rich nations not only suffer Dutch Disease and institutional degradation but also develop an energy infrastructure path dependency that makes transition exceptionally difficult. The spatial irony is that many of the best solar and wind resources on Earth are located in fossil fuel-rich nations (Saudi Arabia, Libya, Algeria) that have the least incentive to develop them.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The geographic specificity of renewable potential implies that <b>international cooperation and grid interconnection</b> are essential for an efficient global energy transition. No single country has optimal resources for all renewables, but most regions collectively do. The European supergrid concept (connecting Saharan solar, North Sea wind, Nordic hydro, and Icelandic geothermal via HVDC transmission) exemplifies this spatial logic. Africa's potential is even more dramatic: the continent has enough solar resource to power itself 10,000 times over, enough hydro in the Congo Basin to supply all of Sub-Saharan Africa, and excellent wind along its eastern and western coastlines. The constraint is not geographic potential but <b>infrastructure</b> (transmission lines), <b>finance</b> (upfront capital for renewable installation), and <b>governance</b> (regulatory frameworks that attract investment). The spatial mismatch between where renewable energy is abundant and where energy demand is concentrated is the central challenge of the 21st-century energy system.</div>

<p class="ref"><b>Key references:</b> IRENA (2023). <i>Renewable Energy Statistics</i>. | Jacobson, M. & Delucchi, M. (2011). Providing all global energy with wind, water, and solar power. <i>Energy Policy</i>, 39(3-4). | Ross, M. (2012). <i>The Oil Curse</i>. Princeton UP. | Edenhofer, O. et al. (2014). <i>Climate Change 2014: Mitigation of Climate Change</i>. IPCC WGIII.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 21: Water Stress
# ═══════════════════════════════════════════════════════════════════
G["21"] = '''
<h2>Water Stress: The Coming Geography of Scarcity</h2>
<p class="tagline">Water stress is the ratio of demand to supply. When it exceeds 40%, a society is in crisis. Geography determines who is there first.</p>

<h3>What You Are Seeing</h3>
<p>A choropleth of freshwater withdrawal as a percentage of available renewable freshwater resources (the Falkenmark Water Stress Indicator). Values below 10% indicate abundance. 10 to 20% is "stress." 20 to 40% is "scarcity." Above 40% is "absolute scarcity," where allocation conflicts become acute and ecosystems are degraded. Countries in the Middle East and North Africa routinely exceed 80%, meaning they withdraw nearly all available renewable water and increasingly rely on non-renewable groundwater, desalination, or virtual water imports.</p>

<h3>The Hydrogeography of Stress</h3>
<div class="hl">Water stress is fundamentally a <b>spatial mismatch</b> between where precipitation falls and where people live and farm. The global distribution of renewable freshwater is staggeringly uneven: Brazil has 12% of the world's freshwater for 3% of its population. The Middle East has 1% of freshwater for 5% of the world's population. This mismatch is governed by the <b>Hadley circulation</b>: the atmospheric circulation cell that creates a band of low precipitation around 20 to 30 degrees latitude (the "arid belt" containing the Sahara, Arabian, Thar, Gobi, Sonoran, and Namib deserts). Most of the world's water-stressed nations lie within or adjacent to this belt. The spatial pattern of water stress is therefore, at its most fundamental level, a consequence of planetary atmospheric physics. The exceptions are countries that are water-stressed despite receiving moderate rainfall because their water is consumed by <b>irrigated agriculture</b> (India, Pakistan, Uzbekistan) or because rapid urbanization concentrates demand (cities like Mexico City and Cape Town that have experienced near-catastrophic shortages).</div>

<h3>Virtual Water and the Spatial Redistribution of Water</h3>
<div class="hl gold">The concept of <b>virtual water</b> (Tony Allan, 1993) transformed the understanding of water stress as a spatial phenomenon. Virtual water is the water embedded in traded goods: producing 1 kg of wheat requires approximately 1,300 liters of water; 1 kg of beef requires approximately 15,000 liters. When a water-scarce country imports grain instead of growing it domestically, it is effectively importing the water used to grow that grain. The global virtual water trade, estimated at approximately 2,300 billion cubic meters annually, represents a massive spatial redistribution of water from water-rich regions (North America, South America, Australia, Southeast Asia) to water-scarce regions (Middle East, North Africa, East Asia). Without this virtual water trade, many water-stressed nations would face absolute water crises. The spatial implication is that <b>water security is inseparable from food trade security</b>: any disruption to global grain markets (as occurred in 2007-2008 and 2022 due to the Ukraine conflict) is simultaneously a water crisis for import-dependent arid nations.</div>

<h3>Groundwater Mining: The Invisible Spatial Crisis</h3>
<p>Many countries that appear manageable on this map are in fact mining <b>non-renewable groundwater</b> at unsustainable rates. India pumps more groundwater than any other country (approximately 250 km3/year), depleting aquifers that took millennia to fill. The <b>Ogallala Aquifer</b> under the US Great Plains is dropping approximately 30 cm per year, threatening the grain belt that feeds a significant fraction of the world. Saudi Arabia exhausted most of its non-renewable fossil water by the 2010s after using it to grow wheat in the desert (a policy since abandoned). NASA's GRACE satellite mission revealed that the world's 37 largest aquifer systems are being depleted faster than they recharge, with the most critical overdrafts in the Indo-Gangetic Basin, the Arabian Aquifer System, and the Murzuk-Djado Basin in North Africa. This invisible depletion does not appear in surface water stress indicators but represents a <b>slow-motion spatial catastrophe</b> that will surface within decades.</p>

<h3>Policy Implications</h3>
<div class="hl warn">Water stress will be the <b>defining geographic constraint of the 21st century</b>. The World Resources Institute projects that by 2040, 33 countries will face "extremely high" water stress, up from 17 in 2020. The spatial overlap between water stress, high population growth, and political instability (the Sahel, Horn of Africa, Middle East) creates a <b>nexus of risk</b> that is often cited as a root cause of conflict (the Syrian civil war was preceded by the worst drought in the Fertile Crescent's recorded history, which displaced 1.5 million farmers to cities). Policy responses must be geographically differentiated: for arid urban areas, water recycling and desalination (Israel recycles 85% of its wastewater, the global leader); for irrigated agriculture, drip irrigation and crop switching (replacing thirsty rice with millets in water-stressed Indian states); for transboundary rivers (which account for 60% of global freshwater flow), international water-sharing agreements that anticipate climate-driven changes in flow patterns.</div>

<p class="ref"><b>Key references:</b> Allan, T. (1993). <i>Fortunately there are substitutes for water: otherwise our hydropolitical futures would be impossible</i>. ODA conference. | Falkenmark, M. (1989). The massive water scarcity now threatening Africa. <i>Ambio</i>, 18(2). | Richey, A. et al. (2015). Quantifying renewable groundwater stress with GRACE. <i>Water Resources Research</i>, 51(7). | Gleick, P. (2014). Water, drought, climate change, and conflict in Syria. <i>Weather, Climate, and Society</i>, 6(3).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 22: Nations Bubble Map
# ═══════════════════════════════════════════════════════════════════
G["22"] = '''
<h2>Nations Bubble Map: Population, Wealth, and Health on a Single Canvas</h2>
<p class="tagline">Every country as a bubble on its actual geographic position. Size is population. Color is income. Vertical offset is life expectancy.</p>

<h3>What You Are Seeing</h3>
<p>Each country is plotted at its geographic centroid with <b>bubble size proportional to population</b>, <b>color encoding GDP per capita</b> (red = low, green = high), and <b>vertical position slightly adjusted by life expectancy</b>. This is a cartogram-scatter hybrid: it preserves geographic context while overlaying multivariate information. The visual effect is a world map where the largest circles (India, China, US, Indonesia, Brazil, Nigeria) dominate, and color reveals the wealth gradient from the "green" North Atlantic to the "red" Sahel.</p>

<h3>Why Centroids Distort and Reveal</h3>
<div class="hl">Using geographic centroids introduces a deliberate distortion: <b>large countries are represented as single points</b>, erasing internal variation. Russia's centroid is in Siberia, far from its population center (Moscow). China's centroid is in its western interior, far from its economic center (the eastern seaboard). Brazil's is in the cerrado, far from Sao Paulo. This distortion is analytically useful because it highlights <b>how misleading national averages are for geographically vast nations</b>. The color of China's bubble represents a GDP per capita that ranges from $5,000 in Gansu to $30,000 in Shanghai. The color of India's bubble averages Goa ($12,000) with Bihar ($1,500). The bubble map is thus simultaneously informative (revealing global patterns) and cautionary (reminding us that "countries" are abstractions that mask enormous internal spatial heterogeneity).</div>

<h3>The Visual Weight of Population</h3>
<div class="hl gold">The bubble size encoding forces the viewer to confront <b>population concentration</b>. India and China together contain approximately 36% of humanity. Their bubbles dwarf everything else. Nigeria, the world's seventh most populous country (220 million), is often overlooked in development discussions but its bubble is larger than any European nation. Indonesia (275 million) anchors Southeast Asia. Pakistan (230 million) is larger than all but three countries. These visual weights matter for policy: <b>global development outcomes are disproportionately determined by what happens in approximately 10 countries</b>. If India, China, Nigeria, Indonesia, Pakistan, Bangladesh, Brazil, Ethiopia, DRC, and the Philippines achieve their development goals, global poverty will be nearly eliminated. If they do not, no amount of progress elsewhere will compensate.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The geographic clustering of large, poor populations in South Asia and Sub-Saharan Africa implies that <b>international development policy should be concentrated, not diffused</b>. The current aid architecture distributes relatively small amounts across many countries. The bubble map suggests that <b>transformative impact requires massive, sustained investment in a small number of high-population, low-income nations</b>, particularly India, Nigeria, DRC, Ethiopia, and Bangladesh. The geographic proximity of these priority nations also suggests opportunities for <b>regional approaches</b>: South Asian integration (India-Bangladesh-Nepal-Sri Lanka) and West African integration (Nigeria-Ghana-Senegal-Cote d'Ivoire) could create markets of scale comparable to China's, potentially replicating the agglomeration effects that drove East Asian development.</div>

<p class="ref"><b>Key references:</b> Dorling, D. (2012). <i>The Visualization of Spatial Social Structure</i>. Wiley. | Gastner, M. & Newman, M. (2004). Diffusion-based method for producing density-equalizing maps. <i>PNAS</i>, 101(20). | World Bank (2023). <i>World Development Indicators</i>.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHARTS 23-36: GEO-VARIABLE ANALYSIS (14 charts)
# ═══════════════════════════════════════════════════════════════════

G["23"] = '''
<h2>Latitude vs GDP: The Geographic Gradient of Wealth</h2>
<p class="tagline">Are nations richer at higher latitudes? The data says yes, but the causal story is fiercely debated.</p>

<h3>What You Are Seeing</h3>
<p>A scatter plot with <b>absolute latitude</b> (distance from the equator in degrees) on the X-axis and <b>GDP per capita (PPP, log scale)</b> on the Y-axis. Each point is a country. The upward slope, if visible, indicates that countries farther from the equator tend to be wealthier. A trend line or LOESS curve summarizes the relationship.</p>

<h3>The Latitude-Wealth Gradient: Three Hypotheses</h3>
<div class="hl">The positive correlation between latitude and wealth is one of the most robust empirical regularities in economic geography. Three competing (and potentially complementary) hypotheses explain it. <b>The Disease Hypothesis (Sachs, Gallup, Mellinger, 1999)</b>: tropical latitudes have higher burdens of infectious disease (malaria, dengue, yellow fever, trypanosomiasis) because the warm, humid climate supports year-round vector reproduction. This disease burden reduces labor productivity, increases healthcare costs, and deters foreign investment. Malaria alone reduces GDP growth by an estimated 1.3% per year in affected nations. <b>The Agricultural Hypothesis (Diamond, 1997; Landes, 1998)</b>: temperate soils (particularly the chernozem/black earth belt of the Northern Hemisphere at 45 to 55 degrees latitude) are more fertile and better suited to the staple cereals (wheat, barley, oats) that supported European agricultural surpluses. Tropical soils, leached by heavy rainfall, have lower nutrient content and are more vulnerable to degradation. <b>The Institutional Hypothesis (Acemoglu, Johnson, Robinson, 2001)</b>: latitude matters because it determined the type of colonial institutions established. In tropical colonies, high European settler mortality (from malaria and yellow fever) led to extractive institutions (designed to transfer resources to the metropole). In temperate colonies, settlers survived and demanded inclusive institutions (property rights, representative government). These institutional differences persist centuries later and explain the latitude-wealth gradient better than direct geographic effects.</div>

<h3>The Exceptions Are Instructive</h3>
<div class="hl gold">The scatter plot contains revealing outliers. <b>Singapore</b> (latitude 1.3 degrees N, GDP $65,000) is the most dramatic exception: a tropical island with no natural resources and extraordinarily high income, achieved through institutional quality, trade orientation, and human capital investment. Its existence severely challenges any purely geographic determinism. <b>Qatar, UAE, Kuwait</b> are wealthy tropical/subtropical nations, but their wealth derives from hydrocarbon extraction rather than broad-based economic productivity. <b>Mongolia and Kyrgyzstan</b> are high-latitude but poor, demonstrating that latitude alone is insufficient; landlockedness, small domestic markets, and post-Soviet institutional disruption matter independently. <b>Botswana</b> (tropical, relatively wealthy for Africa) shows that good governance can partially overcome latitude disadvantage. These exceptions collectively suggest that <b>latitude is a predisposing factor, not a determining one</b>: it creates a gradient of difficulty, but institutional choices can override geographic constraints.</div>

<h3>Spatial Autocorrelation in the Residuals</h3>
<p>If we were to compute the residuals of a latitude-GDP regression (the deviation of each country from its predicted GDP based on latitude alone), those residuals would themselves be <b>spatially autocorrelated</b>. Countries that outperform their latitude cluster together (East Asian tigers, Gulf states, Nordic countries), and countries that underperform cluster together (Sub-Saharan Africa, Central America). This spatial clustering in the residuals suggests that <b>neighborhood effects</b>, including trade networks, institutional diffusion, regional integration, and shared colonial histories, explain a significant portion of the variation beyond what latitude alone captures. In econometric terms, Ordinary Least Squares regression on this data violates the independence assumption because of spatial autocorrelation, necessitating spatial regression models (spatial lag or spatial error) for valid inference.</p>

<h3>Policy Implications</h3>
<div class="hl warn">If the latitude-wealth gradient were purely geographic (disease, soil, climate), then policy interventions targeting these geographic constraints (malaria eradication, agricultural technology, climate adaptation) would be the priority. If it is primarily institutional, then governance reform, anti-corruption measures, and legal system development are the priority. The evidence suggests <b>both channels operate simultaneously</b>: geographic constraints create a baseline of difficulty that bad institutions amplify and good institutions can (partially) overcome. For tropical nations, this implies a dual strategy: invest in geographic mitigation (disease control, soil management, climate-resilient agriculture) while simultaneously building the institutional quality needed to attract investment and enable structural transformation. The spatial clustering of successful tropical nations (Singapore, Botswana, Costa Rica, Mauritius) suggests that "best practice" institutional models can be adapted for tropical contexts, though not simply copied from temperate-zone templates.</div>

<p class="ref"><b>Key references:</b> Gallup, J., Sachs, J. & Mellinger, A. (1999). Geography and economic development. <i>International Regional Science Review</i>, 22(2). | Acemoglu, D., Johnson, S. & Robinson, J. (2001). The colonial origins of comparative development. <i>AER</i>, 91(5). | Diamond, J. (1997). <i>Guns, Germs, and Steel</i>. Norton. | Bloom, D. & Sachs, J. (1998). Geography, demography, and economic growth in Africa. <i>Brookings Papers on Economic Activity</i>, 2.</p>
'''

G["24"] = '''
<h2>Megacity Distance vs Life Expectancy</h2>
<p class="tagline">Does proximity to a global city improve health outcomes? Testing the spatial diffusion of medical infrastructure.</p>

<h3>What You Are Seeing</h3>
<p>Each country is plotted with its <b>distance to the nearest megacity (population above 10 million)</b> on the X-axis and <b>life expectancy</b> on the Y-axis. The hypothesis is that proximity to large urban agglomerations, which concentrate medical infrastructure, pharmaceutical supply chains, and specialist expertise, improves health outcomes through spatial spillover effects.</p>

<h3>The Central Place Theory Connection</h3>
<div class="hl">Walter Christaller's <b>Central Place Theory</b> (1933) predicts that specialized services (including tertiary healthcare) concentrate in higher-order urban centers and are accessed by populations within their hinterlands. Megacities serve as apex central places for healthcare: they house the region's best hospitals, attract specialist physicians, host pharmaceutical distributors, and serve as nodes for medical knowledge diffusion. Countries closer to megacities benefit from these <b>agglomeration externalities</b> even if their own healthcare systems are weak, through medical tourism, emergency evacuation networks, supply chain proximity, and training opportunities for health workers. The relationship is strongest for <b>conditions requiring specialist care</b> (cancer, cardiac surgery, trauma) rather than primary care conditions (diarrhea, respiratory infections) which can be treated locally.</div>

<h3>The Scatter Pattern</h3>
<div class="hl gold">The scatter likely shows a weak but visible negative relationship: countries far from any megacity (remote Pacific islands, landlocked Sahel states, Central Asian nations) tend to have somewhat lower life expectancy, controlling for income. But the relationship is heavily confounded by income: megacities concentrate in wealthy regions, so distance from megacities correlates with distance from wealthy countries. The most interesting observations are the <b>residuals</b>: countries that have much higher or lower life expectancy than their megacity distance would predict. Countries near megacities but with low life expectancy (e.g., nations neighboring Lagos or Karachi, where megacity proximity does not translate into health spillovers because the megacity itself lacks world-class healthcare) are particularly informative. They suggest that the quality, not just the proximity, of the nearest megacity matters.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The spatial decay of healthcare access from urban centers is one of the most persistent inequities in global health. WHO data shows that <b>physician density in rural areas is typically 3 to 10 times lower than in urban areas</b>, even in the same country. Telemedicine, mobile health clinics, and community health worker programs represent spatial strategies for extending healthcare reach beyond urban agglomerations. The rise of <b>medical hubs</b> in middle-income countries (Thailand, India, Turkey for medical tourism) creates new spatial nodes that can serve surrounding regions. For policy, the implication is that <b>strategic investment in regional healthcare hubs</b> (second-tier cities, not just national capitals) can reduce the distance penalty and improve health equity across geographic space.</div>

<p class="ref"><b>Key references:</b> Christaller, W. (1933). <i>Central Places in Southern Germany</i>. | Krugman, P. (1991). Increasing returns and economic geography. <i>Journal of Political Economy</i>, 99(3). | WHO (2023). <i>World Health Statistics</i>.</p>
'''

G["25"] = '''
<h2>Latitude vs Child Mortality: The Tropical Penalty on Children</h2>
<p class="tagline">The relationship between distance from the equator and child survival is among the starkest in all of development geography.</p>

<h3>What You Are Seeing</h3>
<p>A scatter of <b>absolute latitude</b> (X-axis) vs <b>under-5 mortality rate per 1,000 live births</b> (Y-axis). If the correlation is negative (downward slope), it means that countries closer to the equator have higher child mortality, which is the expected pattern based on tropical disease burden, agricultural constraints, and institutional legacies.</p>

<h3>Why Children Die More in the Tropics</h3>
<div class="hl">The tropical child mortality penalty is driven by a specific set of <b>geographically mediated diseases</b>. <b>Malaria</b> kills approximately 600,000 people per year, the vast majority children under 5 in Sub-Saharan Africa. The Anopheles mosquito's range is almost perfectly bounded by the tropics. <b>Diarrheal diseases</b> are more prevalent in tropical environments where water sources are contaminated year-round (in temperate zones, winter freezing interrupts pathogen cycles). <b>Acute respiratory infections</b> are exacerbated by indoor cooking smoke from biomass fuels, which is more common in tropical rural areas. <b>Malnutrition</b> is more prevalent because tropical soils support lower-calorie crop yields and because parasitic infections (hookworm, schistosomiasis) reduce nutrient absorption. The cumulative effect is that a child born in the tropical belt faces 10 to 50 times the mortality risk of a child born in the temperate zone, a geographic gradient in life chances that is among the most extreme of any measurable human outcome.</div>

<h3>The Residuals: Tropical Successes and Temperate Failures</h3>
<div class="hl gold">Countries that lie far below the trend line (lower child mortality than their latitude predicts) are among the most important case studies in development policy. <b>Sri Lanka</b> (latitude 7 degrees N, U5MR approximately 7 per 1,000) has child mortality comparable to upper-middle-income countries, achieved through universal free healthcare, high female literacy, and comprehensive vaccination since the 1950s. <b>Cuba</b> (latitude 22 degrees N, U5MR approximately 5) has the lowest child mortality in Latin America, driven by a primary-care-centered health system with community doctors in every neighborhood. <b>Rwanda</b> (latitude 2 degrees S, U5MR approximately 35, down from 230 in 1990) demonstrates the most dramatic recent tropical improvement, driven by community health workers (one per 400 people) and near-universal health insurance through the Mutuelle de Sante scheme. These cases prove that the tropical penalty is not immutable: it can be overcome by deliberate, sustained public health investment.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The geographic specificity of child mortality causes implies geographically specific solutions. For the malaria belt (roughly 15 degrees S to 20 degrees N in Africa): insecticide-treated bed nets, indoor residual spraying, seasonal malaria chemoprevention, and the new RTS,S vaccine (approved by WHO in 2021). For tropical diarrheal disease zones: water treatment at point of use, improved sanitation (particularly ending open defecation), and oral rehydration salts in every household. For tropical malnutrition hotspots: zinc supplementation, vitamin A supplementation, exclusive breastfeeding promotion, and nutritional support for pregnant and lactating women. The <b>cost-effectiveness of these interventions is extraordinary</b>: GiveWell estimates that distributing bed nets saves a child's life for approximately $4,500. No intervention in wealthy countries comes close to this cost-per-life-saved ratio. The geographic concentration of child mortality in the tropics thus represents the single largest opportunity for life-saving at scale in the world today.</div>

<p class="ref"><b>Key references:</b> UNICEF (2023). <i>Levels & Trends in Child Mortality</i>. | Sachs, J. & Malaney, P. (2002). The economic and social burden of malaria. <i>Nature</i>, 415(6872). | Binkin, N. et al. (2011). Scaling up integrated management of childhood illness. <i>Health Policy and Planning</i>, 26(suppl 1). | GiveWell (2024). Cost-effectiveness analysis of malaria interventions.</p>
'''

G["26"] = '''
<h2>Conflict vs Development: The Spatial Trap of Violence</h2>
<p class="tagline">Armed conflict and underdevelopment are spatially co-located. Untangling which causes which is one of the hardest problems in social science.</p>

<h3>What You Are Seeing</h3>
<p>A scatter or map showing the relationship between <b>conflict intensity</b> (measured by battle-related deaths per capita or conflict years in the last two decades) and <b>development indicators</b> (GDP per capita, life expectancy, or a composite). The pattern typically shows a strong negative relationship: countries with more conflict have worse development outcomes.</p>

<h3>The Conflict Trap: Circular Causation</h3>
<div class="hl">Paul Collier and colleagues (2003) documented what they called the <b>conflict trap</b>: low income increases the risk of civil war (by approximately 2 percentage points for each halving of GDP per capita), and civil war reduces income (by approximately 2.3% per year of conflict). This creates a self-reinforcing cycle that is extremely difficult to escape. The spatial expression of this trap is visible in the map: a contiguous band of conflict-affected states stretches across the Sahel (Mali, Burkina Faso, Niger, Nigeria, Chad), through the Horn of Africa (Somalia, South Sudan, Ethiopia, Eritrea), and into the Great Lakes region (DRC, Burundi). A second cluster covers parts of the Middle East (Syria, Iraq, Yemen, Afghanistan). These conflict clusters are not independent events; they represent <b>spatial contagion</b>: conflict in one country generates refugee flows, arms proliferation, and ethnic mobilization that destabilize neighbors.</div>

<h3>Geography as a Conflict Determinant</h3>
<div class="hl gold">Geographic variables are among the strongest predictors of civil war onset. <b>Mountainous terrain</b> provides cover for insurgent groups and makes state control of territory more difficult (Fearon and Laitin, 2003). <b>Lootable natural resources</b>, including alluvial diamonds (Sierra Leone, DRC), coltan (DRC), timber (Liberia, Cambodia), and opium (Afghanistan), when geographically located in peripheral regions beyond effective state control, finance rebel movements and prolong conflicts. <b>Ethnic homeland geography</b>: when ethnic groups with historical grievances occupy compact, defensible territories (Kurds, Tamils, Tigrayans), secessionist conflict is more likely. <b>Distance from the capital</b>: regions far from the national capital tend to receive less public investment and have weaker state presence, creating the marginalization that fuels rebellion. The <b>center-periphery model</b> (Rokkan and Urwin, 1983) describes how states project power outward from their capitals, with the quality of governance decaying with distance.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The spatial nature of the conflict trap implies that <b>conflict prevention and development must be pursued simultaneously and regionally</b>. Investing in development in a single country while its neighbors are in conflict is often futile (refugee inflows, cross-border armed groups, trade disruption). The most effective approaches combine <b>regional security frameworks</b> (the African Union's Peace and Security Council, ECOWAS's intervention capacity) with <b>development investment targeted at conflict-prone geographic zones</b>. Within countries, the center-periphery pattern suggests that <b>decentralization of fiscal resources and public services to peripheral regions</b> can reduce the marginalization grievances that fuel rebellion. The spatial analysis also reveals that <b>natural resource governance is critical</b>: transparent resource revenue management (as in Botswana's diamond sector) can prevent the "resource curse" that fuels conflict in otherwise similar geographic settings.</div>

<p class="ref"><b>Key references:</b> Collier, P. et al. (2003). Breaking the conflict trap. World Bank Policy Research Report. | Fearon, J. & Laitin, D. (2003). Ethnicity, insurgency, and civil war. <i>APSR</i>, 97(1). | Rokkan, S. & Urwin, D. (1983). <i>Economy, Territory, Identity</i>. Sage. | Lujala, P. et al. (2005). A diamond curse? <i>Journal of Conflict Resolution</i>, 49(4).</p>
'''

G["27"] = '''
<h2>Landlocked vs Coastal: Sea Access as Economic Destiny</h2>
<p class="tagline">Being landlocked reduces GDP growth by approximately 1.5% per year. This chart quantifies the most persistent geographic handicap in development.</p>

<h3>What You Are Seeing</h3>
<p>A comparison of development outcomes (GDP per capita, trade openness, growth rates) between <b>landlocked countries</b> (no direct ocean access) and <b>coastal countries</b>. The comparison may take the form of box plots, bar charts, or scatter plots distinguishing the two groups. The gap is stark: of the world's 44 landlocked developing countries, not one has achieved high-income status (Botswana and Kazakhstan come closest, both relying on mineral extraction).</p>

<h3>The Mechanisms of Landlocked Disadvantage</h3>
<div class="hl">The landlocked penalty operates through multiple spatial channels. <b>Transport costs</b>: landlocked countries face overland transport costs 50 to 100% higher than coastal nations for the same volume of goods. The World Bank estimates that transport costs consume 15 to 20% of the value of exports for landlocked African nations, compared to 5 to 8% for coastal ones. <b>Transit dependency</b>: landlocked countries are economically hostage to the policies, infrastructure quality, and political stability of their transit neighbors. Uganda's exports must pass through Kenya; Malawi's through Mozambique. Any disruption (border closures, port congestion, conflict) in the transit country chokes the landlocked nation's economy. <b>Market access</b>: the gravity model predicts that trade diminishes with distance, and landlocked countries are effectively more "distant" from global markets even if they are physically close, because overland distance is more costly per kilometer than sea distance. <b>Port access asymmetry</b>: 80% of world trade by volume moves by ship. Without a port, landlocked countries cannot participate directly in maritime trade, which is the backbone of global commerce.</div>

<h3>The Geographic Distribution of Landlockedness</h3>
<div class="hl gold"><b>Africa has 16 landlocked countries</b> (the most of any continent), compared to 12 in Asia (mostly Central Asia), 2 in South America (Bolivia, Paraguay), and 0 in East/Southeast Asia. This geographic distribution is partly a legacy of the Berlin Conference (1884-1885), which partitioned Africa into colonial territories with little regard for economic viability, creating landlocked entities that had no independent access to global markets. Central Asian landlockedness is a legacy of the Soviet Union, which integrated these regions via internal rail networks that became international borders after 1991. The contrast with East and Southeast Asia is instructive: Japan, South Korea, Taiwan, China, Vietnam, Thailand, Malaysia, Singapore, Indonesia, and the Philippines all have extensive coastlines. Their export-led development model was facilitated by geographic access to global shipping lanes. The absence of any landlocked country in East Asia's "miracle" economies is not coincidental.</div>

<h3>Can the Penalty Be Overcome?</h3>
<p>Historical examples of successfully overcoming landlockedness are rare but instructive. <b>Switzerland and Austria</b> are wealthy landlocked nations, but they benefit from being surrounded by wealthy, well-infrastructured neighbors with predictable transit policies. Their example is not transferable to developing landlocked countries surrounded by poor, unstable neighbors. <b>Ethiopia</b> is attempting to overcome its landlockedness through a new railway to Djibouti's port (Chinese-financed, opened 2018) and negotiations for port access in Somaliland. <b>Rwanda</b> has pursued a "knowledge economy" strategy (ICT services, financial services, conference tourism) that is less transport-cost-sensitive than manufacturing. These strategies suggest that while the penalty cannot be eliminated, it can be mitigated through <b>strategic infrastructure investment</b>, <b>transit corridor agreements</b>, and <b>economic diversification toward less weight-intensive sectors</b>.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The international community has recognized landlockedness as a structural disadvantage through the <b>Vienna Programme of Action for Landlocked Developing Countries (2014-2024)</b>. Key recommendations include: investment in <b>multimodal transport corridors</b> connecting landlocked nations to ports (the Dar es Salaam corridor for East African landlocked states, the Maputo corridor for Southern Africa); <b>one-stop border posts</b> to reduce transit delays; <b>harmonized customs procedures</b> across transit countries; and <b>special trade preferences</b> that compensate for transport cost disadvantages. At the national level, landlocked countries should prioritize sectors where transport costs are a smaller share of product value: services (ICT, tourism, finance), high-value agriculture (horticulture, spices, coffee), and mineral processing (adding value before export to reduce cost-per-unit-value of transport).</div>

<p class="ref"><b>Key references:</b> Collier, P. (2007). <i>The Bottom Billion</i>. Oxford UP, ch. 4. | Limao, N. & Venables, A.J. (2001). Infrastructure, geographical disadvantage, transport costs, and trade. <i>World Bank Economic Review</i>, 15(3). | Faye, M. et al. (2004). The challenges facing landlocked developing countries. <i>Journal of Human Development</i>, 5(1). | UN-OHRLLS (2014). Vienna Programme of Action.</p>
'''

G["28"] = '''
<h2>Digital Divide by Latitude: Connectivity and the Geographic Gradient</h2>
<p class="tagline">Internet access decreases toward the equator. The digital divide is, in part, a latitude divide.</p>

<h3>What You Are Seeing</h3>
<p>A scatter of <b>absolute latitude</b> vs <b>internet users per 100 people</b>. The upward slope indicates that countries farther from the equator tend to have higher internet penetration. This relationship is partially mediated by income (high-latitude countries are wealthier, and wealthier countries have more internet) but also has independent geographic components related to infrastructure, urbanization patterns, and education levels.</p>

<h3>The Infrastructure Geography of Connectivity</h3>
<div class="hl">The digital divide has a <b>physical infrastructure layer</b> that is inherently geographic. <b>Submarine cables</b> connect continents along routes determined by ocean floor topography, distance, and demand. The North Atlantic cable system (connecting the US and Europe) carries far more bandwidth than the cables connecting Africa to the rest of the world. <b>Terrestrial fiber networks</b> follow population density: dense coastal and urban populations justify infrastructure investment that sparse interior populations do not. <b>Cell tower density</b> is an economic function of subscribers per tower, which is higher in urban areas. The result is that the same Hagerstrandian diffusion pattern visible in physical technologies (railways, electricity) reproduces in digital technologies: core regions connect first, peripheries last. Latitude correlates with this pattern because the high-latitude regions of North America and Europe were the earliest adopters and infrastructure investors.</div>

<h3>Education as a Mediating Variable</h3>
<div class="hl gold">The latitude-internet relationship is partly mediated by <b>education</b>. High-latitude countries invest more in education (a consequence of their higher income), and education drives both the demand for internet (literate populations use digital services) and the supply (educated workforces build and maintain digital infrastructure). The relationship between latitude, education, and connectivity is thus a <b>causal chain</b>: latitude (via climate and institutional legacy) predicts income; income predicts educational investment; education predicts digital adoption. But there are important exceptions: <b>India</b> (low latitude, moderate income, rapidly growing connectivity, particularly in urban areas) and <b>China</b> (mid-latitude, enormous digital economy despite government restrictions) demonstrate that the latitude gradient is not deterministic. <b>Kenya and Rwanda</b> in tropical Africa have achieved digital connectivity rates far above their income peers, driven by mobile money ecosystems and deliberate government policy.</div>

<h3>Policy Implications</h3>
<div class="hl warn">Closing the digital divide requires geographically differentiated strategies. For remote, low-density tropical regions: <b>satellite broadband</b> (LEO constellations) may be the only cost-effective option, bypassing the need for terrestrial infrastructure entirely. For mid-density peri-urban areas: <b>community networks</b> and <b>TV white space</b> (using unused television spectrum for broadband) can extend coverage at low cost. For urban areas in developing countries where the barrier is affordability rather than infrastructure: <b>zero-rating</b> (free access to essential services like Wikipedia, government portals, and health information) and <b>device subsidies</b> (smartphone prices have dropped below $50 in some markets) can rapidly expand adoption. The geographic dimension matters because a single national broadband strategy will inevitably underserve the most remote populations; spatially targeted policies are essential.</div>

<p class="ref"><b>Key references:</b> Hilbert, M. (2016). The bad news is that the digital access divide is here to stay. <i>Telecommunications Policy</i>, 40(6). | ITU (2023). <i>Measuring Digital Development</i>. | World Bank (2016). <i>World Development Report: Digital Dividends</i>.</p>
'''

G["29"] = '''
<h2>Fertility by Climate Zone: How Temperature Shapes Reproductive Behavior</h2>
<p class="tagline">Tropical countries have higher fertility rates. Climate, agriculture, and cultural evolution intertwine to explain why.</p>

<h3>What You Are Seeing</h3>
<p>A visualization relating <b>climate classification</b> (tropical, arid, temperate, continental, polar) or <b>average temperature</b> to <b>total fertility rate</b>. The pattern shows higher fertility in warmer climates and lower fertility in cooler climates, with considerable scatter.</p>

<h3>Causal Pathways: Climate to Fertility</h3>
<div class="hl">The climate-fertility correlation is not a direct physiological effect (human fertility is not significantly affected by ambient temperature). Instead, it operates through at least four indirect pathways. <b>(1) Agricultural systems</b>: tropical subsistence agriculture (particularly shifting cultivation and pastoralism) relies more heavily on family labor, creating economic incentives for large families. Temperate cereal farming is more amenable to mechanization, reducing the labor demand for children. <b>(2) Child mortality</b>: tropical disease burden creates higher child mortality, which, as discussed in Chart 25, drives higher fertility as a compensation mechanism. <b>(3) Urbanization</b>: temperate-zone countries urbanized earlier, and urban living reduces fertility through the mechanisms discussed in Chart 02 (children as cost centers rather than labor assets). <b>(4) Education and women's status</b>: the historical accumulation of educational investment in temperate-zone countries (partly a wealth effect, partly institutional) has raised women's education and autonomy, the strongest proximate determinant of fertility decline.</div>

<h3>The Anthropological Dimension</h3>
<div class="hl gold">Anthropological research adds nuance to the economic model. In many tropical African societies, <b>lineage systems</b> (extended family networks that collectively raise and invest in children) diffuse the cost of childbearing across a wider group, reducing the "per-child cost" to individual parents and sustaining higher fertility norms. John Caldwell's (1982) <b>wealth flow theory</b> argued that in traditional societies, the net flow of resources is from children to parents (children's labor benefits parents), while in modern societies, the flow reverses (parents invest in children's education and welfare). The climate-fertility correlation thus reflects, in part, the geographic distribution of these fundamentally different family economic systems. The transition from one to the other, which Caldwell called the "great divide," proceeds along geographic and economic lines that broadly track the tropical-temperate gradient.</div>

<h3>Policy Implications</h3>
<div class="hl warn">Understanding the climate-fertility pathway implies that <b>fertility reduction in tropical countries requires addressing the underlying geographic and economic conditions</b>, not simply providing contraception (though contraceptive access is necessary). The most effective interventions target the <b>mediating variables</b>: reducing child mortality (so parents feel confident in smaller families), expanding girls' education (so women have alternatives to early childbearing), promoting urbanization with economic opportunity (so the cost-benefit calculus of children shifts), and strengthening social safety nets (so elderly parents do not depend on large numbers of children for old-age security). Countries that have addressed these mediating variables in tropical settings (Bangladesh, Thailand, Costa Rica) have achieved dramatic fertility declines despite their climate zone.</div>

<p class="ref"><b>Key references:</b> Caldwell, J. (1982). <i>Theory of Fertility Decline</i>. Academic Press. | Bongaarts, J. (2017). Africa's unique fertility transition. <i>Population and Development Review</i>, 43(S1). | Bloom, D. et al. (2003). The demographic dividend: A new perspective on the economic consequences of population change. RAND Corporation.</p>
'''

G["30"] = '''
<h2>Urbanization vs Renewable Energy: The Spatial Energy Paradox</h2>
<p class="tagline">More urbanized countries use less renewable energy. Why cities and renewables are in tension.</p>

<h3>What You Are Seeing</h3>
<p>A scatter of <b>urbanization rate</b> (% of population in cities) vs <b>renewable energy share</b> (% of total energy). The expected negative relationship, if present, reflects a paradox: cities are dense and efficient, which should favor renewables, but in practice highly urbanized countries often have <b>lower</b> renewable shares because their economies are powered by fossil-fueled industry and transport.</p>

<h3>The Paradox Explained</h3>
<div class="hl">The negative relationship arises from two confounding factors. First, <b>countries with high renewable shares are often poor and rural</b>, and their "renewable energy" is predominantly <b>traditional biomass</b> (wood, charcoal, dung) used for cooking and heating. This is not modern renewable energy; it is the energy of pre-industrial poverty. Burning biomass indoors causes approximately 3.2 million premature deaths per year (WHO) and is not sustainable at scale. Second, <b>highly urbanized countries have energy-intensive industrial economies</b> powered by fossil fuels, giving them high total energy consumption with a small renewable share. The urbanization-renewables scatter is thus misleading if taken at face value: it conflates traditional biomass with modern renewables and does not control for income.</div>

<h3>The Spatial Energy Transition in Cities</h3>
<div class="hl gold">Cities are simultaneously the <b>largest consumers of energy</b> (approximately 75% of global energy) and the <b>most promising sites for energy transition</b>. Urban density enables district heating, public transit, and efficient building design that reduce per-capita energy demand. Rooftop solar in cities can be deployed without land use competition. Electric vehicle charging networks are most cost-effective in dense urban areas. The spatial structure of cities, particularly their compactness and transit orientation, is a primary determinant of their energy efficiency. Studies of US cities (Newman and Kenworthy, 1999) showed a strong inverse relationship between urban density and per-capita transport energy use: compact cities like New York consume one-fifth the transport energy per capita of sprawling cities like Houston.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The energy transition must be spatially differentiated. <b>For rural developing countries</b>: transition from traditional biomass to modern renewables (clean cookstoves, solar home systems, mini-grids). <b>For urban developing countries</b>: invest in public transit and compact urban form to prevent lock-in to car-dependent sprawl. <b>For wealthy urbanized countries</b>: retrofit existing cities with building-scale renewables, electrify transport, and deploy smart grids that manage urban demand peaks. The spatial pattern on this chart will <em>reverse</em> as the global energy transition proceeds: highly urbanized countries will achieve higher modern renewable shares because their concentrated demand can be efficiently served by solar, wind, and grid storage. The policy priority is ensuring that the rural poor do not remain trapped on traditional biomass while the urban wealthy transition to modern clean energy.</div>

<p class="ref"><b>Key references:</b> Newman, P. & Kenworthy, J. (1999). <i>Sustainability and Cities</i>. Island Press. | IEA (2023). <i>Energy Technology Perspectives</i>. | WHO (2023). Household air pollution and health fact sheet.</p>
'''

G["31"] = '''
<h2>Water Stress by Latitude: The Arid Belt and Beyond</h2>
<p class="tagline">The geography of water scarcity follows atmospheric physics: the Hadley Cell creates a band of dryness that shapes civilizations.</p>

<h3>What You Are Seeing</h3>
<p>A scatter of <b>absolute latitude</b> vs <b>water stress index</b>. The pattern should show a peak in water stress at approximately 20 to 35 degrees latitude (the subtropical dry belt), with lower stress at both the equator (abundant tropical rainfall) and high latitudes (lower evapotranspiration). The arid belt countries (Middle East, North Africa, Central Asia, parts of Australia) cluster at high stress regardless of income.</p>

<h3>Atmospheric Physics Determines the Baseline</h3>
<div class="hl">The <b>Hadley Cell</b> is the large-scale atmospheric circulation between the equator and approximately 30 degrees latitude. At the equator, intense solar heating causes moist air to rise, cool, and release precipitation (creating the tropical rainforests). This dry air then descends at approximately 20 to 30 degrees latitude, warming as it falls and creating the world's great deserts: the Sahara, Arabian, Sonoran, Namib, Kalahari, Thar, and Australian deserts. This <b>subsidence zone</b> is the primary determinant of the water stress pattern visible in this chart. Countries within the subsidence zone (Egypt, Libya, Saudi Arabia, Iraq, Iran, Pakistan, northern Mexico, Australia) face a permanent, physics-determined water deficit that no amount of economic development can eliminate. They can only adapt through water-saving technologies, desalination, or virtual water imports.</div>

<h3>Climate Change and the Expanding Arid Belt</h3>
<div class="hl warn">Climate models consistently project that the Hadley Cell will <b>expand poleward</b> under greenhouse warming, pushing the arid belt toward the mid-latitudes. This means that regions currently at the edge of the dry zone (the Mediterranean, California, parts of Australia, South Africa's Western Cape) will experience increasing aridity. The Mediterranean is projected to lose 10 to 30% of its precipitation by 2100 under moderate warming scenarios. This has profound spatial implications: agricultural zones that have sustained civilizations for millennia (the Fertile Crescent, the Nile Valley, the Mediterranean basin) are becoming drier, potentially triggering large-scale migration from newly arid regions to regions that remain habitable. The Syrian drought of 2006-2010, which displaced 1.5 million people and contributed to the subsequent civil war, may be a preview of this dynamic.</div>

<p class="ref"><b>Key references:</b> Held, I. & Soden, B. (2006). Robust responses of the hydrological cycle to global warming. <i>Journal of Climate</i>, 19(21). | Gleick, P. (2014). Water, drought, climate change, and conflict in Syria. <i>Weather, Climate, and Society</i>, 6(3). | Falkenmark, M. (1989). The massive water scarcity now threatening Africa. <i>Ambio</i>, 18(2).</p>
'''

G["32"] = '''
<h2>Physicians per 1,000 by Latitude: The Healthcare Desert</h2>
<p class="tagline">The global distribution of doctors follows wealth, not disease burden. The sickest regions have the fewest healers.</p>

<h3>What You Are Seeing</h3>
<p>A scatter of <b>absolute latitude</b> vs <b>physicians per 1,000 population</b>. The upward slope reflects the concentration of medical professionals in wealthy, high-latitude countries. Values range from below 0.1 (Sub-Saharan Africa, where a single doctor may serve 10,000 or more patients) to above 4.0 (Cuba, Austria, Greece).</p>

<h3>The Inverse Care Law as a Global Spatial Phenomenon</h3>
<div class="hl">Julian Tudor Hart's <b>Inverse Care Law</b> (1971) stated that "the availability of good medical care tends to vary inversely with the need for it in the population served." Originally describing inequality within the UK's National Health Service, this law operates globally with devastating spatial precision. Sub-Saharan Africa carries approximately 24% of the global disease burden but has only 3% of the world's health workers. The WHO estimates a global shortfall of 18 million health workers, with the deficit concentrated almost entirely in low-income tropical countries. The spatial mismatch between disease burden and healthcare capacity is the single most important structural barrier to health equity on the planet.</div>

<h3>The Brain Drain: A Spatial Flow of Human Capital</h3>
<div class="hl gold">The doctor shortage in low-income countries is exacerbated by <b>medical brain drain</b>: physicians trained in poor countries migrate to wealthy ones. Approximately 25% of doctors practicing in the UK and 23% in the US received their primary medical training in a developing country. Ethiopia, with a population of 120 million, has approximately 5,000 doctors total, while the Chicago metropolitan area (population 9 million) has approximately 30,000. This spatial flow of medical talent from the Global South to the Global North represents a massive implicit subsidy: the training cost of each emigrating doctor (estimated at $50,000 to $100,000) is borne by poor countries, while the service benefits accrue to rich ones. The WHO's Global Code of Practice on International Recruitment of Health Personnel (2010) attempts to address this, but remains voluntary and largely unenforceable.</div>

<h3>Policy Implications</h3>
<div class="hl warn"><b>Task-shifting</b> (training community health workers, nurses, and clinical officers to perform tasks traditionally restricted to doctors) is the most promising spatial strategy for closing the care gap. Ethiopia's Health Extension Worker program (38,000 workers covering 80% of the rural population) and Rwanda's community health model demonstrate that even with extreme doctor shortages, basic health outcomes can be dramatically improved by deploying lower-cadre workers into underserved communities. <b>Telemedicine</b> offers another spatial solution: connecting rural patients to urban specialists via mobile technology. For physician retention: domestic medical schools must be expanded, rural service requirements instituted, and compensation structured to reward underserved-area practice. The geographic concentration of the physician shortage in a limited number of countries means that targeted medical education investment in Sub-Saharan Africa could have outsized global impact.</div>

<p class="ref"><b>Key references:</b> Hart, J.T. (1971). The inverse care law. <i>The Lancet</i>, 297(7696). | WHO (2023). <i>World Health Statistics</i>. | Bhutta, Z. et al. (2010). Global experience of community health workers for delivery of health-related MDGs. <i>The Lancet</i>, 375(9722).</p>
'''

G["33"] = '''
<h2>Education and Megacity Distance: Knowledge Diffusion from Urban Centers</h2>
<p class="tagline">Educational attainment diminishes with distance from major urban centers, reflecting the spatial decay of institutional capacity.</p>

<h3>What You Are Seeing</h3>
<p>A scatter of <b>distance to nearest megacity</b> (X-axis) vs <b>mean years of schooling or school enrollment rate</b> (Y-axis). The expected negative relationship reflects the concentration of educational infrastructure (universities, teacher training colleges, publishing, educational technology) in major urban centers, with quality and access decaying with distance.</p>

<h3>Why Distance Matters for Education</h3>
<div class="hl">The spatial pattern of educational achievement reflects multiple overlapping geographic processes. <b>Teacher deployment</b>: qualified teachers prefer urban postings (better pay, amenities, career opportunities), creating chronic rural teacher shortages. In Malawi, the student-teacher ratio in urban areas is approximately 40:1; in rural areas, approximately 100:1. <b>Infrastructure</b>: schools in remote areas are more likely to lack electricity (preventing computer use), libraries, laboratories, and even basic supplies. <b>Opportunity cost</b>: in remote agricultural communities, children's labor has higher economic value, reducing school attendance during planting and harvest seasons. <b>Language of instruction</b>: in linguistically diverse countries, children in remote areas are more likely to be instructed in a non-native language (the capital's dominant language), reducing comprehension and increasing dropout rates. These factors compound: distance from urban centers is a proxy for the simultaneous absence of multiple educational inputs.</div>

<h3>Digital Technology as Distance-Destroyer</h3>
<div class="hl gold">The most promising development in spatial educational equity is <b>mobile-based and satellite-delivered education</b>. Programs like Khan Academy (available on basic smartphones), Eneza Education (SMS-based tutoring in Kenya), and India's SWAYAM platform (MOOCs broadcast via satellite) represent attempts to compress the distance penalty in education. Early evidence is mixed: technology can deliver content but cannot replace the human relationship between teacher and student that is critical for learning, especially for younger children. The spatial implication is that technology can complement but not substitute for investment in <b>rural educational infrastructure and teacher deployment</b>. The countries that have achieved the best rural educational outcomes (Vietnam, Cuba, Sri Lanka) did so primarily through aggressive teacher deployment and community school construction, not technology.</div>

<h3>Policy Implications</h3>
<div class="hl warn">Reducing the distance penalty in education requires spatially targeted interventions: <b>rural teacher incentives</b> (salary bonuses, housing, career advancement for rural service), <b>boarding school networks</b> for remote secondary education, <b>mother-tongue early education</b> followed by gradual transition to the national language, and <b>satellite/mobile learning platforms</b> for supplementary instruction. The evidence from multiple countries suggests that <b>the first priority should be ensuring a qualified teacher in every classroom</b>, which requires training institutions located in or near rural communities (not concentrated in the capital), followed by infrastructure investment and, only then, technology.</div>

<p class="ref"><b>Key references:</b> UNESCO (2023). <i>Global Education Monitoring Report</i>. | Muralidharan, K. & Sundararaman, V. (2011). Teacher performance pay: experimental evidence from India. <i>Journal of Political Economy</i>, 119(1). | Kremer, M. et al. (2013). The challenge of education and learning in the developing world. <i>Science</i>, 340(6130).</p>
'''

G["34"] = '''
<h2>Trade Openness by Longitude: East-West Patterns in Global Commerce</h2>
<p class="tagline">Does longitude predict trade integration? Testing Jared Diamond's east-west axis hypothesis in the modern economy.</p>

<h3>What You Are Seeing</h3>
<p>A scatter of <b>longitude</b> (X-axis, from 180W to 180E) vs <b>trade openness</b> (exports + imports as % of GDP). The hypothesis, drawn loosely from Diamond's <i>Guns, Germs, and Steel</i>, is that the east-west continental axis of Eurasia facilitated trade historically (same climate zone, easier crop and technology diffusion) and may still produce geographic patterns in modern trade integration.</p>

<h3>The East-West Axis in Trade History</h3>
<div class="hl">Diamond's (1997) argument was about prehistoric crop diffusion, but the east-west axis has modern trade implications. <b>Eurasia's east-west orientation</b> meant that the Silk Road, the world's most important pre-modern trade route, connected civilizations across 8,000 km without requiring major changes in latitude (and thus climate, growing conditions, and disease environment). The <b>Americas' north-south orientation</b> created barriers to trade: the Isthmus of Panama was a geographic bottleneck, and the temperature/climate transitions from the Andes to the Amazon impeded overland commerce. In the modern era, the <b>major shipping lanes</b> still run primarily east-west (trans-Pacific, trans-Atlantic, Europe-Asia via Suez), and countries located along these lanes tend to have higher trade openness than those off the main routes.</div>

<h3>What the Scatter Shows</h3>
<div class="hl gold">The scatter likely shows <b>clusters rather than a continuous gradient</b>. The <b>European cluster</b> (0 to 30 degrees E) shows consistently high trade openness, reflecting EU integration. The <b>East Asian cluster</b> (100 to 140 degrees E) shows high openness due to export-oriented manufacturing. The <b>Americas</b> (60 to 120 degrees W) show lower openness for large countries (US, Brazil) but higher for Caribbean and Central American entrepots. <b>Central/West Africa</b> (0 to 20 degrees E) shows low openness despite being in the same longitude range as Europe, demonstrating that longitude alone is not deterministic. The scatter suggests that modern trade openness is shaped more by <b>regional trade agreements</b>, <b>institutional quality</b>, and <b>colonial trading relationships</b> than by raw longitude.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The spatial structure of global trade favors countries located along major maritime routes. Landlocked and geographically remote nations face structural disadvantages that regional trade agreements (AfCFTA, RCEP, EU single market) can partially offset by creating nearby markets. The east-west axis hypothesis reminds us that <b>geography creates corridors of easy exchange</b> and that deliberate infrastructure investment (railways, highways, ports) can create new corridors where geography did not provide natural ones. The Belt and Road Initiative is, in spatial terms, an attempt to recreate and expand the Silk Road's east-west connectivity using modern infrastructure.</div>

<p class="ref"><b>Key references:</b> Diamond, J. (1997). <i>Guns, Germs, and Steel</i>. Norton. | Disdier, A.C. & Head, K. (2008). The puzzling persistence of the distance effect on bilateral trade. <i>Review of Economics and Statistics</i>, 90(1). | WTO (2023). <i>World Trade Report</i>.</p>
'''

G["35"] = '''
<h2>Maternal Mortality and Forest Cover: An Unexpected Spatial Correlation</h2>
<p class="tagline">Countries with more forest have lower maternal mortality. Is this ecology, economy, or spurious correlation?</p>

<h3>What You Are Seeing</h3>
<p>A scatter of <b>forest cover (%)</b> vs <b>maternal mortality ratio</b> (deaths per 100,000 live births). The expected negative relationship (more forest = lower maternal mortality) is surprising because there is no obvious direct causal link between tree cover and maternal health.</p>

<h3>Unpacking the Correlation</h3>
<div class="hl">This is a classic example of a <b>confounded spatial correlation</b> that requires careful interpretation. The correlation likely arises from several indirect pathways. <b>Income confounding</b>: wealthier countries have both more forest (they have passed the forest transition minimum and are regaining forest) and lower maternal mortality (they can afford obstetric care). <b>Governance quality</b>: countries with strong governance protect both forests (through environmental regulation) and maternal health (through healthcare investment). <b>Geographic coincidence</b>: some of the world's most forested countries (Scandinavian nations, Japan, Canada, Bhutan, Papua New Guinea) happen to have low maternal mortality for reasons unrelated to forest cover. Meanwhile, deforested countries (Haiti, Sahel nations) tend to be desperately poor with collapsed health systems. The correlation is <b>ecologically fallacious</b> if interpreted as forest cover directly causing better maternal health.</div>

<h3>The Genuine Ecological Connection</h3>
<div class="hl gold">However, there are <em>some</em> plausible direct mechanisms. Forests regulate local climate and water availability, supporting agricultural productivity and food security, which affect maternal nutrition. Forests provide <b>traditional medicinal resources</b> that, in many rural communities, supplement or substitute for formal obstetric care. Deforestation causes soil erosion and flooding, which destroys infrastructure (including roads to hospitals) and contaminates water supplies, increasing infection risk during childbirth. In the Amazon, research has linked deforestation to increased malaria incidence (by creating sun-exposed puddles where Anopheles mosquitoes breed), which is a leading cause of maternal morbidity. These ecological pathways are real but small compared to the dominant confounders of income and governance.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The lesson is methodological as much as substantive: <b>spatial correlations are not causal evidence</b>. Planting trees will not reduce maternal mortality; investing in skilled birth attendants, emergency obstetric care, and antenatal nutrition will. The correlation does, however, point to a deeper truth: <b>environmental health and human health are spatially co-determined</b>. Countries that destroy their natural environment (deforestation, water pollution, soil degradation) tend to have worse human health outcomes, not because nature directly heals people but because the same governance failures, poverty traps, and institutional weaknesses that drive environmental destruction also drive health system collapse. Addressing both requires systemic interventions that improve governance, institutions, and investment capacity, not sector-specific interventions targeting forests or maternal health in isolation.</div>

<p class="ref"><b>Key references:</b> Mather, A. (1992). The forest transition. <i>Area</i>, 24(4). | Myers, S. et al. (2013). Human health impacts of ecosystem alteration. <i>PNAS</i>, 110(47). | MacDonald, A. & Mordecai, E. (2019). Amazon deforestation drives malaria transmission. <i>PNAS</i>, 116(44).</p>
'''

G["36"] = '''
<h2>Remittances by Latitude: Migration Flows and the Global Labor Market</h2>
<p class="tagline">Remittance dependence peaks in the low-latitude, low-income belt where emigration is highest.</p>

<h3>What You Are Seeing</h3>
<p>A scatter of <b>absolute latitude</b> vs <b>personal remittances received (% of GDP)</b>. The expected negative relationship (lower latitude = higher remittance dependence) reflects the fact that low-latitude countries tend to be poorer and have higher emigration rates to wealthier, higher-latitude destinations.</p>

<h3>The Spatial Structure of Global Labor Migration</h3>
<div class="hl">Global labor migration flows follow a clear <b>south-to-north gradient</b> (or, more precisely, from low-latitude to high-latitude). The major corridors are: <b>Latin America to North America</b> (Mexico, Central America, Colombia to the US), <b>South Asia to the Gulf</b> (India, Pakistan, Bangladesh, Nepal to Saudi Arabia, UAE, Qatar), <b>Southeast Asia to East Asia</b> (Philippines, Indonesia, Myanmar to Japan, South Korea, Taiwan), <b>Sub-Saharan Africa to Europe</b> (West Africa to France, UK, Italy; East Africa to UK, Scandinavia), and <b>Central Asia to Russia</b> (Tajikistan, Uzbekistan, Kyrgyzstan to Moscow). These flows are driven by wage differentials that follow the latitude-wealth gradient: a construction worker in Qatar earns 5 to 10 times what they would earn in Bangladesh for identical work. The spatial logic is that labor migrates toward capital, and capital concentrates at higher latitudes.</div>

<h3>The Gender Geography of Remittances</h3>
<div class="hl gold">Migration corridors have distinct <b>gender profiles</b>. The Gulf corridor is predominantly male (construction, driving, manual labor), meaning that women in source communities (Kerala, Bihar, Nepal) manage households on remittance income while their husbands are abroad. This has complex spatial consequences: it empowers women economically (they control household spending) but also increases their labor burden and can disrupt family structures. The Philippines corridor is more gender-balanced (healthcare workers, domestic workers), with Filipina women comprising approximately 60% of overseas workers. The European corridor from Eastern Europe is predominantly female (care work, domestic labor). The gender geography of migration thus creates distinct spatial patterns of social transformation in source communities depending on which gender emigrates.</div>

<h3>Policy Implications</h3>
<div class="hl warn">Remittance flows represent a <b>market-driven form of international redistribution</b> that dwarfs official development assistance. Policy can enhance their development impact through: <b>reducing transfer costs</b> (global average remittance cost is approximately 6%, but corridors to Sub-Saharan Africa average approximately 8%; the UN SDG target is below 3%); <b>channeling remittances toward productive investment</b> (diaspora bonds, matched savings programs, remittance-backed microfinance); and <b>protecting migrant workers' rights</b> in destination countries (wage theft and exploitation in the Gulf construction sector are well-documented). The spatial concentration of remittance dependence in specific countries means that policy changes in a small number of destination countries (US, Saudi Arabia, UAE, Russia) can have outsized impacts on the economies of dozens of source countries.</div>

<p class="ref"><b>Key references:</b> World Bank (2023). <i>Migration and Development Brief</i>. | Ratha, D. (2003). Workers' remittances: An important and stable source of external development finance. | Clemens, M. (2011). Economics and emigration: Trillion-dollar bills on the sidewalk? <i>Journal of Economic Perspectives</i>, 25(3).</p>
'''


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


# Process
count = 0
for filename in sorted(os.listdir(VIZ_DIR)):
    if not filename.endswith(".html") or filename == "index.html":
        continue
    num = filename.split("_")[0]
    if num in G:
        if inject_guide(os.path.join(VIZ_DIR, filename), G[num]):
            count += 1
            print(f"  Injected: {filename}")
        else:
            print(f"  SKIPPED (already has guide): {filename}")

print(f"\nPhase 2: Injected deep guides into {count} charts")
