#!/usr/bin/env python3
"""Phase 4: Deep academic interpretation guides for charts 49-64.
Animated Temporal (bar race, swing, fertility collapse, mortality plunge, convergence, inequality)
+ remaining 3D Immersive (spiral, terrain, food geography, helices, aurora, socioeconomic)
+ Women LISA + Coral Temporal."""

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
# CHART 49: GDP Bar Chart Race (1992-2022)
# ═══════════════════════════════════════════════════════════════════
G["49"] = '''
<h2>GDP Bar Chart Race: Thirty Years of Global Economic Reshuffling</h2>
<p class="tagline">Watch the world's economic hierarchy rearrange itself in real time. The bar chart race is not just entertainment; it encodes the speed and direction of structural economic change.</p>

<h3>What You Are Seeing</h3>
<p>An animated horizontal bar chart showing the <b>top 15 countries by GDP per capita (PPP)</b>, racing from 1992 to 2022. Each bar's length is proportional to GDP per capita. Countries enter and exit the top 15 as their relative position changes. The animation speed reveals the <b>velocity</b> of economic change: fast-moving bars indicate rapid growth or decline.</p>

<h3>The Stories Embedded in the Animation</h3>
<div class="hl"><b>Ireland's ascent</b> is the most dramatic single-country story. In 1992, Ireland was a mid-ranking European economy (GDP per capita around $15,000). By 2022, it had soared to the top 5 globally (above $100,000 on some measures). This "Celtic Tiger" phenomenon is partly real (EU membership, education investment, English-language advantage) and partly statistical artifact: Ireland's status as a <b>corporate tax haven</b> (12.5% rate) means that multinational profits are booked in Ireland, inflating GDP far beyond the actual economic activity occurring on Irish soil. The Central Statistics Office of Ireland itself created "Modified GNI" (GNI*) to strip out these distortions, which reduces Ireland's apparent income by approximately 40%. The bar chart race thus embeds a <b>cautionary tale about GDP as a welfare measure</b>: Ireland's bars are racing upward, but Irish households are not 3 times richer than German households.</div>

<div class="hl gold"><b>Qatar and Gulf states</b> appear at or near the top throughout. Their extreme per-capita GDP reflects the combination of enormous hydrocarbon revenues and tiny citizen populations (Qatar has approximately 300,000 citizens among 2.8 million residents; only citizens are in the denominator for some calculations). <b>Singapore's</b> steady climb reflects genuine productivity-driven growth: a city-state with no natural resources that built its wealth through education, institutions, trade facilitation, and strategic positioning at the nexus of Pacific and Indian Ocean shipping. <b>China</b> does not appear in the top 15 for per-capita GDP (it would rank approximately 70th globally), but its absolute GDP trajectory, from 10th largest in 1992 to 2nd by 2010 to near-parity with the US by 2022 in PPP terms, is the most consequential economic shift of the era.</div>

<h3>What Bar Chart Races Reveal and Conceal</h3>
<p>The bar chart race format is optimized for showing <b>rank changes and velocity</b>, which makes it compelling as a narrative device. However, it has analytical limitations. It shows only the top N countries, obscuring the far larger changes happening at the bottom and middle of the distribution (the billions of people in China and India who moved out of poverty are invisible in a "top 15" race). It uses per-capita GDP, which, as the Ireland and Qatar examples show, can be severely misleading. And the racing animation can create a false impression of competition: countries are not actually "racing" against each other; their growth trajectories are determined by internal structural factors, not relative positioning. The spatial dimension is absent from the bar chart race format itself, but the viewer should mentally map each bar to its geographic location: the dominance of small European and Gulf states at the top reflects the statistical bias of per-capita measures toward small-population, high-income nations.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The bar chart race inadvertently illustrates the <b>limitations of GDP as a policy target</b>. Ireland "winning" the race is meaningless for Irish welfare when the victory is driven by accounting flows of multinational profits. Qatar's top position coexists with labor conditions for migrant workers that the International Labour Organization has repeatedly criticized. The race format privileges <b>growth speed</b>, but sustainable development requires balancing growth with equity, environmental sustainability, and institutional quality. Hans Rosling repeatedly cautioned against the "race" metaphor for development: countries are not competing for a fixed prize but navigating distinct structural transformations at different speeds. A more useful framing is whether countries are moving in the <b>right direction</b> for their populations, regardless of their rank relative to others.</div>

<p class="ref"><b>Key references:</b> Barro, R. & Sala-i-Martin, X. (2003). <i>Economic Growth</i>. MIT Press. | FitzGerald, J. (2018). National accounts for a global economy: the case of Ireland. <i>Quarterly Economic Commentary</i>, ESRI. | Stiglitz, J., Sen, A. & Fitoussi, J.P. (2009). <i>Report by the Commission on the Measurement of Economic Performance and Social Progress</i>.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 50: India Electoral Swing 2019 vs 2024
# ═══════════════════════════════════════════════════════════════════
G["50"] = '''
<h2>India Electoral Swing: 2019 vs 2024</h2>
<p class="tagline">Animated geographic scatter toggling between two elections. Watch margins morph as the electorate's mood shifts across geographic space.</p>

<h3>What You Are Seeing</h3>
<p>An animated geographic visualization that toggles or morphs between the <b>2019 and 2024 Lok Sabha election results</b>. Each constituency is plotted at its geographic position, with <b>bubble size encoding victory margin</b> and <b>color encoding the winning alliance</b>. The animation transitions between the two snapshots, allowing the viewer to see which constituencies <b>swung</b> (changed alliance), which <b>tightened</b> (margin narrowed), and which <b>stayed stable</b>.</p>

<h3>The Geography of Swing</h3>
<div class="hl">Electoral swing has a <b>spatial structure</b> that reflects the geographic organization of Indian politics. The 2024 election saw the BJP lose approximately 60 seats compared to 2019, but these losses were not geographically random. They concentrated in specific zones. <b>UP and Bihar</b>: the Samajwadi Party (SP) and RJD recovered significant ground, reclaiming constituencies that the BJP had won in 2019 on the strength of the Modi wave. The geographic pattern of SP recovery follows caste geography: Yadav and Muslim-plurality constituencies swung back. <b>Maharashtra</b>: the three-way split between Shiv Sena factions and NCP factions created geographic fragmentation, with swing patterns following factional loyalty lines. <b>The South</b>: relatively stable, as regional party dominance (DMK in TN, TMC in WB) persisted with minor adjustments. The animation makes visible the key insight that <b>Indian elections are won and lost in specific geographic zones, not uniformly across the country</b>.</div>

<h3>Swing as a Spatial Diffusion Process</h3>
<div class="hl gold">Electoral swing can be modeled as a <b>spatial diffusion process</b>. When a party gains (or loses) support, the change tends to radiate outward from epicenters rather than occurring uniformly. In 2024, the SP's resurgence in UP appears to have diffused from its traditional strongholds (eastern UP, Yadav-majority belts) outward into adjacent constituencies. The BJP's decline in these areas followed a complementary pattern: losses were most severe near SP epicenters and diminished with distance. This spatial diffusion pattern has implications for campaign strategy: parties should identify <b>swing epicenters</b> early and either reinforce them (if favorable) or contain them (if unfavorable). The geographic diffusion metaphor, borrowed from epidemiology and innovation studies, treats political momentum as something that <b>spreads through spatial proximity</b>, which makes sense given that the mechanisms of political change (word of mouth, local media, community meetings, rally attendance) are all geographically bounded.</div>

<h3>Constituencies with Greater than 10 Percentage Point Swings</h3>
<p>Constituencies that experienced swing greater than 10 percentage points deserve individual investigation because they represent <b>dramatic local shifts</b> that override national trends. Such large swings are typically driven by: <b>candidate quality change</b> (a popular local leader replacing a weak incumbent or vice versa), <b>caste arithmetic shift</b> (a change in ticket allocation that consolidates or fragments a caste coalition), <b>local issues</b> (a major infrastructure failure, corruption scandal, or natural disaster), or <b>organizational collapse/surge</b> (a party's local machinery either disintegrating or being rebuilt). Mapping these high-swing constituencies geographically reveals whether they cluster (suggesting a regional wave driven by a common cause) or scatter (suggesting constituency-specific factors).</p>

<h3>Policy Implications</h3>
<div class="hl warn">For democratic health, the <b>spatial pattern of swing matters more than the national aggregate</b>. If swing is concentrated in a few states while the rest of the country is static, it means that a national mandate is being determined by <b>localized mood shifts</b>, not a genuine nationwide verdict. This geographic concentration of swing is a structural feature of India's first-past-the-post system with regional parties: a 5% swing in UP (80 seats) can change 30 to 40 seats, while the same swing in Tamil Nadu (39 seats) might change 2 to 3 due to DMK dominance. The <b>geographic asymmetry of electoral sensitivity</b> means that some regions have disproportionate influence over national outcomes, raising questions about whether India's seat allocation and party system give adequate weight to all geographic voices.</div>

<p class="ref"><b>Key references:</b> Yadav, Y. & Palshikar, S. (2009). Between fortuna and virtu: explaining the results of 2009. <i>Economic and Political Weekly</i>, 44(39). | Butler, D. & Stokes, D. (1969). <i>Political Change in Britain</i>. Macmillan. (Foundational swing analysis.) | Election Commission of India (2024). Statistical Report.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 51: Fertility Collapse (Animated Bubble)
# ═══════════════════════════════════════════════════════════════════
G["51"] = '''
<h2>The Global Fertility Collapse: Year-by-Year Animation</h2>
<p class="tagline">Watch the entire world converge toward below-replacement fertility. This animation is the demographic event of the millennium.</p>

<h3>What You Are Seeing</h3>
<p>An animated bubble chart stepping through years 1990 to 2023, plotting <b>fertility rate</b> (X-axis) against <b>life expectancy</b> (Y-axis). Bubble size = population, color = continent. The animation reveals a <b>global convergence</b>: virtually every country's bubble moves leftward (declining fertility) and upward (improving life expectancy) over the period.</p>

<h3>The Speed of Convergence</h3>
<div class="hl">The most remarkable feature of this animation is the <b>compression of the fertility distribution</b>. In 1990, the world's fertility rates ranged from approximately 1.3 (Italy, Spain) to 8.0 (Niger, Mali). By 2023, the range had narrowed to approximately 0.7 (South Korea) to 6.5 (Niger). The global mean TFR fell from 3.4 to 2.3, crossing the <b>replacement threshold of 2.1</b> in approximately 2015. This means that, for the first time in the history of Homo sapiens, the average woman on Earth is having fewer children than needed to replace the current population. If this trend continues (and no reversal has ever been observed in any country that has completed the demographic transition), <b>the human population will peak and begin declining</b>, probably between 2080 and 2100, at somewhere between 9 and 10.5 billion.</div>

<h3>The Spatial Pattern of Convergence</h3>
<div class="hl gold">The animation reveals that convergence is not uniform. <b>East Asian bubbles</b> (China, South Korea, Japan, Thailand) moved leftward fastest, often overshooting replacement to reach ultra-low levels (below 1.5). This compressed transition, completed in two to three decades rather than the century that Europe took, is sometimes called the <b>"East Asian fertility shock."</b> Its spatial clustering suggests shared cultural factors (Confucian emphasis on education quality over quantity, intense labor market competition, high cost of urban living in mega-dense cities like Seoul, Tokyo, Shanghai) overlaid on common policy drivers (aggressive family planning programs in the 1960s-1980s). <b>South Asian bubbles</b> (India, Bangladesh) moved leftward steadily, reaching near-replacement by 2023. <b>Sub-Saharan African bubbles</b> moved leftward most slowly and remain the rightmost cluster, with most countries still above TFR 4.0. The spatial gap between Africa and the rest of the world in fertility is widening even as the absolute levels decline.</div>

<h3>The Ultra-Low Fertility Crisis</h3>
<p>The left side of this animation reveals a crisis as consequential as the right side. Countries with TFR below 1.5 (South Korea 0.7, Japan 1.2, Italy 1.2, Spain 1.2, China 1.0, and increasingly Germany, Poland, and Canada) face <b>population aging at a pace never before experienced</b>. Japan already has more people over 65 than under 15. South Korea's working-age population will halve by 2070 at current rates. China's will shrink by 200 million by 2050. The economic consequences are profound: shrinking labor forces, rising dependency ratios, pension system insolvency, and declining domestic demand. No policy intervention has reliably reversed ultra-low fertility: pronatalist subsidies (baby bonuses, parental leave, childcare provision) in France, Sweden, and Hungary have at best nudged TFR upward by 0.2 to 0.3, far short of reaching replacement. The spatial clustering of ultra-low fertility in East Asia and Southern Europe suggests shared structural drivers: extreme housing costs in dense cities, long working hours, gender inequality in household labor (women bear a "double burden" of work and childcare), and cultural shifts toward individualism and delayed family formation.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The animation's key message for policymakers is that <b>the world's demographic future is being written in two geographic zones simultaneously</b>. In Sub-Saharan Africa: accelerating the fertility transition through girls' education, contraceptive access, and child mortality reduction is critical to preventing a population peak above 11 billion. In East Asia and Europe: mitigating the consequences of ultra-low fertility through immigration policy, automation, retirement age adjustment, and childcare infrastructure is critical to preventing economic stagnation. These two challenges are <b>geographically complementary</b>: the young populations of Africa could, through managed migration, partially offset the aging of Europe and East Asia, while remittances from migrants could accelerate development in Africa. The spatial logic of the demographic transition thus points toward <b>international migration as the great equilibrating mechanism</b> of the 21st century, if political systems can accommodate it.</div>

<p class="ref"><b>Key references:</b> Lutz, W. et al. (2001). The end of world population growth. <i>Nature</i>, 412(6846). | Sobotka, T. (2017). Post-transitional fertility: the role of childbearing postponement in fuelling the shift to low and unstable fertility levels. <i>Journal of Biosocial Science</i>, 49(S1). | McDonald, P. (2000). Gender equity in theories of fertility transition. <i>Population and Development Review</i>, 26(3). | UN DESA (2022). <i>World Population Prospects</i>.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 52: Child Mortality Plunge (Animated Choropleth)
# ═══════════════════════════════════════════════════════════════════
G["52"] = '''
<h2>The Child Mortality Plunge: Animated Choropleth 1990-2022</h2>
<p class="tagline">Watch Africa gradually lighten as millions of children survive who would not have thirty years earlier. This is the best news on Earth.</p>

<h3>What You Are Seeing</h3>
<p>An animated choropleth map stepping through years from 1990 to 2022, showing <b>under-5 mortality rate</b> (deaths per 1,000 live births) for each country. Dark red indicates catastrophic child mortality (above 200). The animation reveals a global wave of improvement, with countries progressively lightening (lower mortality) from green-to-yellow as decades pass.</p>

<h3>The Three Waves of Improvement</h3>
<div class="hl">The animation reveals child mortality decline as a <b>spatial wave</b> that swept across the world in three phases. <b>Wave 1 (1990s)</b>: Latin America, East Asia, and parts of the Middle East lightened rapidly, driven by expanded vaccination programs, oral rehydration therapy scale-up, and economic growth. <b>Wave 2 (2000-2010)</b>: South Asia (particularly India and Bangladesh) began dramatic improvement, and parts of East Africa (Kenya, Tanzania, Rwanda) followed. This wave was catalyzed by the Millennium Development Goals and the associated funding mechanisms (GAVI, Global Fund, PEPFAR). <b>Wave 3 (2010-2022)</b>: West and Central Africa, the last holdout, began significant decline, though levels remain the world's highest. The spatial sequencing of these waves follows the geography of development capacity: countries with stronger health systems and governance improved first; the most fragile states improved last.</div>

<h3>The Acceleration After 2000</h3>
<div class="hl gold">The animation shows a visible <b>acceleration in the rate of improvement</b> around the year 2000. This coincides with the adoption of the MDGs and the creation of dedicated global health funding mechanisms. Between 1990 and 2000, global under-5 deaths fell from approximately 12.6 million to 9.9 million per year (a 21% decline in a decade). Between 2000 and 2015, they fell to 5.9 million (a 40% decline, nearly double the previous rate). This acceleration demonstrates that <b>coordinated international goal-setting with measurable targets and dedicated financing works</b>. The geographic pattern of acceleration also reveals which countries were most responsive to external support: Ethiopia, Rwanda, Bangladesh, and Malawi showed the steepest declines, driven by community health worker programs, vaccination campaigns, and insecticide-treated bed net distribution, all funded or supported by international mechanisms.</div>

<h3>The Remaining Dark Spots</h3>
<p>Even in the final frame (2022), a handful of countries remain stubbornly dark: <b>Nigeria, Chad, Central African Republic, Somalia, South Sudan, Mali, Sierra Leone</b>. These represent the <b>hardest cases</b>: countries where conflict, state fragility, geographic remoteness, and extreme poverty combine to prevent the health gains achieved elsewhere. Nigeria alone accounts for approximately 15% of global child deaths despite having approximately 3% of the world's population. The spatial concentration of remaining child mortality in a shrinking number of countries means that the global challenge has shifted from "everywhere" (in 1990) to <b>a specific, identifiable set of fragile and conflict-affected states</b> where conventional development approaches (building clinics, training health workers) are insufficient because the underlying governance and security conditions do not permit their functioning.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The animation contains both the best news and the hardest remaining challenge in global development. The best news: <b>humanity has cut child mortality by more than half in a single generation</b>, saving millions of lives through technologies that cost pennies per dose. The hard challenge: the remaining deaths are geographically and structurally concentrated in environments where <b>standard health system approaches fail</b>. Reaching the last mile requires innovation: community health workers deployed in conflict zones, mobile health clinics, drone delivery of vaccines to remote areas, and ultimately, political solutions to the conflicts and governance failures that prevent health system functioning. The spatial targeting is clear: approximately 10 countries account for over 60% of remaining child deaths, and within those countries, specific subnational regions (northern Nigeria, southern Somalia, eastern DRC) account for a disproportionate share. <b>Global child survival is now a precision geographic targeting problem, not a knowledge or technology problem.</b></div>

<p class="ref"><b>Key references:</b> UNICEF (2023). <i>Levels & Trends in Child Mortality</i>. | Lozano, R. et al. (2011). Progress towards Millennium Development Goals 4 and 5. <i>The Lancet</i>, 378(9797). | Victora, C. et al. (2003). Applying an equity lens to child health and mortality. <i>The Lancet</i>, 362(9379).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 53: Continental Convergence Race
# ═══════════════════════════════════════════════════════════════════
G["53"] = '''
<h2>Continental Convergence Race: Health Converges, Wealth Diverges</h2>
<p class="tagline">Two panels. Left: life expectancy lines converging. Right: GDP lines diverging. The central paradox of modern development visualized.</p>

<h3>What You Are Seeing</h3>
<p>A dual-panel animated line chart. <b>Left panel</b>: continental mean life expectancy over time, with each continent's line color-coded. The lines <b>converge</b>, meaning the gap between the highest (Europe) and lowest (Africa) narrows over time. <b>Right panel</b>: continental mean GDP per capita over time. The lines <b>diverge</b>, meaning the gap between richest and poorest continents widens, or at best stagnates.</p>

<h3>The Convergence Paradox Explained</h3>
<div class="hl">This chart visualizes what development economists call the <b>convergence-divergence paradox</b>. The mechanisms that drive health convergence are fundamentally different from those that drive (or fail to drive) economic convergence. <b>Health knowledge is a global public good</b>: once a vaccine is invented, it can be manufactured and distributed worldwide at declining marginal cost. Technologies like oral rehydration salts, insecticide-treated bed nets, and antiretroviral drugs have been successfully transferred from invention in wealthy countries to deployment in poor countries within 5 to 15 years. The result is that the steepest health improvements occur in countries starting from the lowest base, producing convergence. <b>Economic productivity, by contrast, depends on institutional infrastructure</b> (rule of law, property rights, contract enforcement, anti-corruption), <b>human capital</b> (education quality, not just years of schooling), and <b>physical capital</b> (factories, ports, electricity grids) that are expensive to build, slow to accumulate, and resistant to cross-border transfer. The result is that wealthy countries can sustain compound productivity growth while poor countries struggle to generate the institutional foundations for any growth at all.</div>

<h3>The Spatial Dimension of Convergence</h3>
<div class="hl gold">The convergence-divergence asymmetry has a <b>spatial expression</b>. Health convergence is geographically <em>broad</em>: almost every country on Earth has improved its life expectancy since 1990, including the poorest and most conflict-affected (with exceptions like Syria during active war). This broad-based improvement creates a spatially <em>smoother</em> health surface across the globe. Economic divergence is geographically <em>concentrated</em>: a small number of rapidly growing economies (China, India, Vietnam, Bangladesh) have narrowed the gap with wealthy nations, while a large number of stagnant or declining economies (much of Sub-Saharan Africa, parts of Central America, post-conflict states) have fallen further behind. The spatial pattern of economic growth is <b>lumpy</b>: it concentrates in geographic clusters (East Asian manufacturing corridor, Indian IT corridor) while leaving vast areas untouched.</div>

<h3>Will Economic Convergence Follow?</h3>
<p>Neoclassical growth theory (Solow, 1956) predicts that poor countries should grow faster than rich ones (due to higher marginal returns on capital), leading to eventual convergence. Empirically, this <b>conditional convergence</b> holds only among countries with similar institutions and human capital (EU countries converge, OECD countries converge, East Asian tigers converge). Among all countries unconditionally, there is <b>no convergence in GDP per capita</b>. The gap between the richest and poorest countries has widened, not narrowed, since 1960. The spatial implication is stark: without dramatic institutional change, the geographic wealth map of the world in 2050 will look essentially the same as it does today, even as the health map continues to equalize. The world is becoming more <b>equally healthy but equally unequally wealthy</b>.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The dual-panel format forces a policy question: <b>if health can converge, why can't wealth?</b> The answer points to the different policy instruments required. Health convergence was driven by <b>specific, deliverable, scalable technologies</b> (vaccines, drugs, devices) deployed through <b>purpose-built international mechanisms</b> (WHO, GAVI, Global Fund). Economic convergence would require equivalent breakthroughs in <b>institutional quality, governance, and human capital</b>, which are inherently harder to "deliver" from outside. The most promising economic analogue to health technology transfer is <b>regional economic integration</b>: by creating large, rule-governed markets (EU, ASEAN, AfCFTA), poor countries can access the trade, investment, and institutional diffusion that drove East Asian convergence. But integration requires the same institutional foundations that make convergence difficult in the first place, creating a chicken-and-egg problem that spatial economic theory has not resolved.</div>

<p class="ref"><b>Key references:</b> Solow, R. (1956). A contribution to the theory of economic growth. <i>Quarterly Journal of Economics</i>, 70(1). | Pritchett, L. (1997). Divergence, big time. <i>Journal of Economic Perspectives</i>, 11(3). | Deaton, A. (2004). Health in an age of globalization. NBER Working Paper 10669. | Barro, R. & Sala-i-Martin, X. (1992). Convergence. <i>Journal of Political Economy</i>, 100(2).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 54: Women LISA Fixed
# ═══════════════════════════════════════════════════════════════════
G["54"] = '''
<h2>Women Winners LISA: Weak but Significant Spatial Clustering</h2>
<p class="tagline">Moran's I = 0.062 for women's election victories. Weak clustering, but statistically significant. What does weak spatial autocorrelation mean in this context?</p>

<h3>What You Are Seeing</h3>
<p>Two panels. <b>Left</b>: a LISA cluster map for a binary or continuous measure of women's electoral success across India's 543 constituencies. <b>Right</b>: a scatter of constituency area vs population density with women winners highlighted. The LISA analysis tests whether constituencies that elected women cluster geographically or are randomly distributed.</p>

<h3>Interpreting Weak Spatial Autocorrelation</h3>
<div class="hl">The Moran's I of <b>0.062</b> is <b>statistically significant</b> (p < 0.001, confirmed by 999 permutations) but <b>substantively weak</b>. This means that while women's electoral success is not perfectly random across space (there is a slight tendency for women-won constituencies to neighbor other women-won constituencies), the spatial signal is very faint compared to variables like turnout (I = 0.642) or alliance dominance (I = 0.367). The weakness of the clustering tells an important story: <b>women's success in Indian elections is primarily determined by constituency-specific factors</b> (party nomination decisions, individual candidate quality, local caste dynamics) rather than by broad regional or geographic patterns. Unlike turnout, which is shaped by deep structural factors that vary gradually across geographic space (literacy, culture, state capacity), women's candidacy is shaped by <b>discrete party-level decisions</b> that can place a woman candidate in one constituency while ignoring the neighboring one.</div>

<h3>The Small Clusters That Do Exist</h3>
<div class="hl gold">Despite the weak overall signal, the LISA map does reveal a few <b>small spatial clusters of women's success</b>. Rajasthan shows a cluster of 3 to 4 adjacent constituencies that elected women, likely reflecting both the BJP's nominations (Rajasthan had relatively more women nominees from BJP in 2024) and the state's reservation-in-panchayats legacy (three-tier local government reservation for women since 1993 created a pipeline of experienced women politicians who subsequently contested Lok Sabha seats). West Bengal shows another small cluster, reflecting the TMC's relatively higher rate of women nominations. These micro-clusters suggest a <b>neighborhood demonstration effect</b>: when a woman wins in one constituency, parties in neighboring constituencies may be more willing to nominate women, having seen that a woman candidate can succeed locally. This "spatial learning" hypothesis is plausible but cannot be confirmed from a single election's cross-sectional data; it would require multi-election panel analysis.</div>

<h3>The Right Panel: Area and Density</h3>
<p>The area-density scatter with women highlighted reinforces the findings from Chart 46: women winners concentrate in the <b>moderate-area, moderate-to-high-density</b> portion of the scatter. They are underrepresented in the extreme tails: the very largest, most remote constituencies (where campaign costs and cultural barriers are highest) and, surprisingly, some of the very smallest urban constituencies (where competition for tickets is fiercest and party power brokers, typically men, are most entrenched). The "sweet spot" for women candidates appears to be mid-sized constituencies with moderate urbanization, where barriers are lower than in deep rural areas but party gatekeeping is less intense than in premium urban seats.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The weak spatial autocorrelation of women's success, combined with the strong spatial autocorrelation of women's <em>exclusion</em> (see Chart 65: the 152 zero-women constituencies cluster geographically), yields a precise policy insight: <b>the problem is not that women cannot win where they run; it is that they do not run in geographically clustered exclusion zones</b>. The parties' nomination decisions, not voter preferences, are the binding constraint. The spatial learning hypothesis suggests that the Women's Reservation Bill could create a <b>positive spatial diffusion effect</b>: by forcing women's candidacy in currently excluded zones, it may normalize women's political presence in neighboring constituencies, creating a geographic cascade that extends beyond the reserved seats themselves. This is exactly the mechanism observed in panchayat-level reservation in Rajasthan and West Bengal: exposure to women leaders in reserved positions increased voter willingness to support women in unreserved positions in adjacent areas (Beaman et al., 2012).</div>

<p class="ref"><b>Key references:</b> Anselin, L. (1995). LISA. <i>Geographical Analysis</i>, 27(2). | Beaman, L. et al. (2012). Female leadership raises aspirations and educational attainment for girls. <i>Science</i>, 335(6068). | Chattopadhyay, R. & Duflo, E. (2004). Women as policy makers. <i>Econometrica</i>, 72(5).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 55: Party Flip Pulse (Three.js)
# ═══════════════════════════════════════════════════════════════════
G["55"] = '''
<h2>Party Flip Pulse: The Geography of Electoral Change in 3D</h2>
<p class="tagline">214 constituencies changed hands between 2019 and 2024. Each one pulses with a golden ring. The geography of political change, made kinetic.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Three.js 3D visualization</b> of India with all 543 constituencies rendered. Constituencies that <b>flipped</b> (changed their winning party/alliance between 2019 and 2024) are highlighted with <b>pulsing golden rings</b> using a sinusoidal animation. Non-flipped constituencies remain static. The pulsing draws the eye to the <b>dynamic geography of Indian democracy</b>: the places where voters changed their minds.</p>

<h3>What the Spatial Pattern of Flips Reveals</h3>
<div class="hl">The 214 flipped constituencies are not randomly distributed. They cluster in <b>contested geographic zones</b> where neither alliance has structural dominance. Key flip zones include: <b>Eastern UP</b> (SP recapturing seats from BJP, driven by OBC consolidation and Muslim-Yadav alliance revival), <b>Maharashtra</b> (fragmentation between rival Sena and NCP factions creating unpredictable local outcomes), <b>Rajasthan</b> (anti-incumbency against the BJP state government in 2024), and <b>parts of Karnataka and Telangana</b> (Congress/INDIA alliance gains on development platforms). The geographic clustering of flips confirms that Indian electoral change is <b>regionally structured</b>: national swings manifest as geographic waves that wash through specific zones while leaving others untouched.</div>

<h3>The Pulsing Metaphor</h3>
<div class="hl gold">The sinusoidal pulse is not merely decorative. It encodes a conceptual insight: <b>flipped constituencies are the "living" tissue of democracy</b>. They are where voters exercised genuine choice, where campaign dynamics mattered, where democracy functioned as a mechanism of accountability. Static (non-flipped) constituencies, particularly those won by the same party in multiple consecutive elections by large margins, represent the <b>"ossified" geography of Indian politics</b>: safe seats where neither party makes serious efforts because the outcome is predetermined by structural factors (caste composition, regional party dominance). A healthy democracy should have more pulse and less stasis. The ratio of flipped to stable constituencies (214/543 = 39% in 2024) is a rough measure of <b>democratic competitiveness</b>, and its geographic distribution reveals where that competitiveness is concentrated.</div>

<h3>Policy Implications</h3>
<div class="hl warn">For political strategists, the flip map identifies the <b>geographic battleground</b> for the next election. For democratic reformers, the concentration of flips in specific zones while other zones remain static raises concerns about <b>geographic democratic inequality</b>: voters in safe-seat regions effectively have less influence over government formation than voters in swing zones. Electoral reforms that could increase geographic competitiveness include: <b>proportional representation elements</b> (which would make every vote matter regardless of geographic location), <b>ranked-choice voting</b> (which would encourage parties to appeal beyond their base), and <b>delimitation reform</b> that considers competitiveness as a factor in constituency design alongside population equality.</div>

<p class="ref"><b>Key references:</b> Three.js documentation. | Sridharan, E. (2014). India's watershed election. <i>Journal of Democracy</i>, 25(4). | Yadav, Y. (1999). Electoral politics in the time of change. <i>Economic and Political Weekly</i>, 34(34/35).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 56: Development Spiral (Three.js)
# ═══════════════════════════════════════════════════════════════════
G["56"] = '''
<h2>Development Spiral: Countries Traced Through Time in 3D</h2>
<p class="tagline">Each country traces a spiral path: radius = log(GDP), height = life expectancy. Outward and upward = developing. Scrub the slider to watch history unfold.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Three.js 3D spiral</b> visualization where each country traces a helical path through time (1952 to 2007, from the Gapminder classic dataset). The mapping is: <b>angular position = time</b> (each year advances the spiral by a fixed angle), <b>radius = log(GDP per capita)</b> (richer countries are farther from the center), <b>height = life expectancy</b>. The year slider scrubs through time, revealing each country's trajectory. Countries spiraling outward and upward are developing. Countries spiraling inward or downward are regressing.</p>

<h3>Why a Spiral? The Temporal-Spatial Encoding</h3>
<div class="hl">The spiral encoding solves a fundamental problem in temporal data visualization: <b>showing both trajectory and current state simultaneously</b>. In a standard 2D scatter (GDP vs life expectancy), each country is a single point with no visible history. Adding animation shows history one year at a time, but the viewer cannot see the full trajectory at once. The 3D spiral shows the <b>entire trajectory</b> as a visible path in space. A country that developed steadily (constant growth + constant life expectancy improvement) traces a smooth, gradually expanding upward spiral. A country that experienced a crisis (GDP collapse or life expectancy decline) shows a <b>kink, reversal, or inward loop</b> in its spiral. These visual signatures of historical events are immediately identifiable without needing to know the specific years.</div>

<h3>Reading the Spirals: Key Country Signatures</h3>
<div class="hl gold"><b>China's spiral</b> is the most dramatic: starting tight and low (poor, moderate life expectancy) in 1952, it shows a notable <b>downward kink</b> during 1959-1961 (the Great Leap Forward famine, which reduced life expectancy by approximately 20 years in the worst-affected provinces), then recovers and begins a steady outward-upward expansion from the 1970s onward, accelerating dramatically after the 1978 economic reforms. <b>Botswana's spiral</b> shows a stunning outward expansion (diamond-fueled growth) with an equally stunning <b>downward plunge</b> in the 1990s-2000s (HIV/AIDS), followed by recovery. <b>Rwanda's spiral</b> shows a catastrophic collapse in 1994 (genocide) followed by one of the steepest recovery trajectories of any country. <b>Japan's spiral</b> is almost perfectly smooth and gradually expanding, the geometric signature of sustained, stable development. Each spiral is a <b>visual biography of a nation's development experience</b>, with crises, recoveries, and steady-state periods all legible from the shape alone.</div>

<h3>The Spatial Organization of Spirals</h3>
<p>If countries are arranged on the spiral axis by <b>geographic proximity</b> (nearby countries near each other), the visualization reveals spatial autocorrelation in development trajectories: neighboring countries tend to have similar spiral shapes because they share trade networks, colonial histories, disease environments, and institutional legacies. African spirals tend to be tight (low GDP) with height (life expectancy) gains only in recent decades. European spirals are wide and high throughout. The visual similarity of spirals within geographic clusters is itself a manifestation of Tobler's First Law: near things (countries) are more related (in development trajectory) than distant things.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The spiral visualization makes <b>development reversals viscerally visible</b> in a way that static charts cannot. The downward kinks (China's famine, Botswana's HIV crisis, Rwanda's genocide) are not mere data points; they are human catastrophes rendered as geometric anomalies in an otherwise smooth upward path. The policy lesson is that <b>development is fragile</b>: decades of progress can be reversed by a single catastrophic event (pandemic, famine, genocide, economic crisis). Resilience, the capacity to withstand shocks without losing developmental gains, is as important as growth. Countries whose spirals show smooth, steady expansion (Japan, Norway, Australia) share a common feature: <b>strong institutions that buffer against shocks</b> (democratic governance, social safety nets, diversified economies, rule of law). Building these institutions is the policy equivalent of <b>smoothing the spiral</b>.</div>

<p class="ref"><b>Key references:</b> Gapminder Foundation (2024). Classic dataset documentation. | Rosling, H. (2018). <i>Factfulness</i>. Flatiron Books. | Three.js documentation.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 57: Coral Temporal Pulse
# ═══════════════════════════════════════════════════════════════════
G["57"] = '''
<h2>Coral Temporal Pulse: Bleaching Frequency as a Climate Clock</h2>
<p class="tagline">The interval between mass bleaching events is shortening. Reefs that once had decades to recover now have years. This timeline charts the acceleration.</p>

<h3>What You Are Seeing</h3>
<p>A dual-panel visualization. <b>Top</b>: a map of reef locations colored by bleaching history. <b>Bottom</b>: a timeline of global and regional sea surface temperature (SST) anomaly, with <b>vertical markers</b> indicating documented mass bleaching events. The tightening interval between markers is the chart's central message: the time between crises is shrinking.</p>

<h3>The Acceleration of Bleaching</h3>
<div class="hl">The first recorded global mass bleaching event was in <b>1998</b>, driven by a powerful El Nino. The second was in <b>2010</b> (12-year gap). The third was <b>2015-2016</b> (5-year gap). The fourth was confirmed in <b>2024</b> (8-year gap). But between these global events, regional bleaching episodes have become <b>nearly annual</b> in the most vulnerable reef systems: the Great Barrier Reef experienced mass bleaching in 2016, 2017, 2020, 2022, and 2024. The Caribbean has experienced regional bleaching in most years since 2014. The accelerating frequency is a direct consequence of the ratcheting SST baseline discussed in Chart 08: as background warming raises the "floor" temperature, ever-smaller El Nino or seasonal heat events push reefs past their bleaching threshold. The interval between mass events is now <b>shorter than the 5 to 10 years that most coral species require for full recovery</b>, meaning reefs enter each new bleaching event in an already weakened state.</div>

<h3>The Spatial Pattern of Temporal Acceleration</h3>
<div class="hl gold">Not all reefs are experiencing the same acceleration. The <b>most rapid tightening of bleaching intervals</b> is in the western Pacific warm pool (Great Barrier Reef, Coral Triangle) and the western Indian Ocean (Maldives, Chagos, East Africa). These regions sit in the warmest tropical waters and have the narrowest thermal tolerance windows. <b>Higher-latitude reefs</b> (Japan's Okinawa, Australia's Lord Howe Island, Bermuda) are bleaching less frequently because their wider seasonal temperature range gives them a broader thermal envelope. <b>Upwelling regions</b> (eastern Pacific, parts of East Africa) experience intermittent cooling that interrupts the warming trend, providing periodic relief. The spatial pattern of temporal acceleration thus overlays the static vulnerability map (Chart 07) with a dynamic dimension: <b>where</b> reefs are located determines not just their current bleaching risk but <b>how fast</b> that risk is increasing.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The tightening interval has a critical policy implication: <b>the window for reef conservation through local management is closing</b>. Local stressors (pollution, overfishing, sedimentation) weaken reef resilience, making thermal bleaching more lethal. Reducing local stressors can buy time for reefs to survive bleaching events. But if the interval between events shrinks below the recovery period, no amount of local management can save reefs from thermal-driven decline. The only intervention that addresses the root cause is <b>global emissions reduction</b> to slow and eventually halt ocean warming. The spatial targeting of conservation should prioritize <b>climate refugia</b>: reef locations where oceanographic conditions (upwelling, deep water proximity, high-latitude location) provide natural thermal buffering and where local management can maintain the resilience needed to survive the coming decades of warming until (and if) global emissions peak and begin to decline.</div>

<p class="ref"><b>Key references:</b> Hughes, T. et al. (2018). Spatial and temporal patterns of mass bleaching. <i>Science</i>, 359(6371). | NOAA CRW (2024). Coral bleaching alert system. | Hoegh-Guldberg, O. et al. (2019). The human imperative of stabilizing global climate change at 1.5C. <i>Science</i>, 365(6459).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 58: Animated Inequality (Gini Choropleth)
# ═══════════════════════════════════════════════════════════════════
G["58"] = '''
<h2>Animated Inequality: The Gini Coefficient Through Time</h2>
<p class="tagline">Inequality is not static. Watch Latin America's Gini decline through conditional cash transfers, while China's rises with uneven growth.</p>

<h3>What You Are Seeing</h3>
<p>An animated choropleth stepping through 5-year bins (1990, 1995, 2000, 2005, 2010, 2015, 2020), showing each country's <b>Gini coefficient</b> for income inequality. Countries darken (more unequal) or lighten (more equal) as the decades pass. The animation reveals that inequality is <b>not a fixed characteristic of countries</b>: it responds to policy choices, economic shocks, and structural transformations.</p>

<h3>Latin America: The Declining Gini</h3>
<div class="hl">The most visible region-wide trend in the animation is <b>Latin America lightening</b> from the 2000s onward. Brazil's Gini fell from 0.59 in 1990 to approximately 0.49 by 2020. Mexico, Argentina, Peru, and Ecuador showed similar declines. The primary drivers were: <b>conditional cash transfer (CCT) programs</b> (Brazil's Bolsa Familia, Mexico's Oportunidades/Prospera), which directly redistribute income to poor households conditional on children's school attendance and health checkups; <b>commodity-driven wage growth</b> (the 2000s commodity boom raised wages for low-skilled workers in mining, agriculture, and construction); <b>minimum wage increases</b> (Brazil raised its minimum wage by 100% in real terms between 2002 and 2014); and <b>educational expansion</b> (more years of schooling compressed the education premium, reducing skill-based inequality). The spatial clustering of inequality decline across Latin America suggests <b>policy diffusion</b>: the success of Bolsa Familia in Brazil inspired similar CCT programs across the continent, creating a regional wave of redistribution.</div>

<h3>China: The Rising Gini</h3>
<div class="hl gold">China's Gini rose dramatically from approximately 0.32 in 1990 to approximately 0.47 by 2010, before stabilizing. This increase is the <b>inequality cost of rapid, geographically uneven growth</b>. China's economic transformation was spatially concentrated: Special Economic Zones on the eastern seaboard (Shenzhen, Shanghai, Guangzhou) boomed while interior provinces lagged. Urban incomes soared while rural incomes grew more slowly. The coastal-interior, urban-rural double divide created a spatial pattern of inequality that is literally visible from satellite imagery: glittering megacities alongside villages that still lack running water. China's post-2010 stabilization reflects deliberate policy: the "Go West" campaign (investing in interior provinces), expansion of the <em>dibao</em> (minimum livelihood guarantee), and targeted poverty alleviation programs that reached 100 million people. The Chinese trajectory demonstrates that inequality is <b>a policy variable, not an inevitable consequence of growth</b>.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The animation demonstrates that <b>inequality trajectories are determined by policy choices, not by immutable structural forces</b>. The same decade (2000s) saw inequality declining in Latin America (due to redistribution policies) and rising in China (due to geographically concentrated growth). Countries can choose which trajectory to follow. The spatial dimension adds nuance: inequality is not just a national average but has <b>geographic expression</b>. Within-country spatial inequality (rich coast vs poor interior, prosperous capital vs stagnant provinces) is often more visible and politically salient than interpersonal inequality captured by the Gini. Policies that target <b>place-based disadvantage</b> (investing in lagging regions, building infrastructure in remote areas, decentralizing economic opportunity from primate cities to secondary towns) can reduce both spatial and interpersonal inequality simultaneously.</div>

<p class="ref"><b>Key references:</b> Lustig, N. et al. (2013). The decline in inequality in Latin America. <i>World Development</i>, 44. | Ravallion, M. & Chen, S. (2007). China's (uneven) progress against poverty. <i>Journal of Development Economics</i>, 82(1). | Piketty, T. (2014). <i>Capital in the Twenty-First Century</i>. Harvard UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 59: India Development Terrain (Three.js)
# ═══════════════════════════════════════════════════════════════════
G["59"] = '''
<h2>India Development Terrain: 30 States as 3D Pillars</h2>
<p class="tagline">Eight switchable metrics. No state excels on all dimensions. The terrain of Indian development is as uneven as the subcontinent's physical topography.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Three.js 3D visualization</b> of India's 30 major states, each represented as a rectangular pillar at its geographic location. <b>Height = the selected metric value</b>, switchable via buttons: HDI, GSDP per capita, literacy rate, sex ratio, infant mortality rate, urbanization, electrification, and women's political representation. <b>Width approximates state area</b>. <b>Color gradient</b>: red (low/poor) to green (high/good). The camera can be rotated to view the development landscape from any angle.</p>

<h3>The Multidimensional Poverty of Single Metrics</h3>
<div class="hl">Switching between metrics reveals that <b>no Indian state excels on all dimensions simultaneously</b>. <b>Kerala</b> leads on HDI, literacy (96%), and sex ratio (1,084 females per 1,000 males) but has only moderate GSDP per capita (reflecting limited industrialization). <b>Goa</b> has the highest GSDP per capita but is tiny in population and area. <b>Maharashtra</b> has a large economy but deep internal inequality (Mumbai's wealth coexists with vidarbha's farmer suicides). <b>Bihar</b> ranks last or near-last on almost every metric: lowest GSDP per capita, lowest literacy, worst sex ratio (907), highest infant mortality, lowest urbanization. The 3D terrain makes this multidimensional variation viscerally apparent: switching metrics creates a <b>radically different landscape each time</b>, demonstrating that "development" is not a single dimension but a multi-faceted construct that can be advanced unevenly.</div>

<h3>The North-South Gradient Across Metrics</h3>
<div class="hl gold">While the specific rankings change with each metric, a <b>broad north-south gradient persists across most dimensions</b>. Southern states (Kerala, Tamil Nadu, Karnataka, Andhra Pradesh, Telangana) and western states (Maharashtra, Gujarat, Goa) consistently have taller pillars (better outcomes) than northern and eastern states (UP, Bihar, Jharkhand, Madhya Pradesh, Chhattisgarh). This north-south development gradient is India's most fundamental spatial inequality and has deep historical roots: the South's linguistic states reorganization (1956) created governance units aligned with cultural-linguistic communities, enabling more effective public service delivery. The South's longer history of anti-caste social reform movements (Periyar in Tamil Nadu, Narayan Guru in Kerala) created more egalitarian social structures. And the South's earlier demographic transition (lower fertility, higher women's education) generated a demographic dividend that northern states have not yet captured.</div>

<h3>Amartya Sen's Capability Approach in 3D</h3>
<p>The switchable-metric design embodies Amartya Sen's <b>capability approach</b> (1999), which argues that development should be measured not by a single aggregate (GDP) but by the <b>set of capabilities</b> (freedoms, opportunities, functionings) that people have. Each metric represents a different capability: GSDP per capita measures material command over resources; literacy measures the capability to read, learn, and participate in the knowledge economy; sex ratio measures whether women have the basic capability of being born and surviving; infant mortality measures children's capability to live. The 3D terrain, by requiring the viewer to switch between metrics rather than looking at a single composite, forces engagement with the <b>disaggregated, multidimensional nature of human development</b>.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The terrain's most important policy implication is that <b>states need different interventions depending on which metric is selected</b>. Bihar does not need the same policy package as Kerala. Bihar needs basic infrastructure (electricity, roads, schools, hospitals), demographic transition support (girls' education, contraceptive access), and governance reform. Kerala needs economic diversification (manufacturing, IT services), job creation for its highly educated population, and health system reform to address the emerging burden of non-communicable diseases associated with an aging population. The 3D terrain makes clear that <b>"one India" development policy is a fiction</b>: the subcontinent's internal variation is as large as the variation between rich and poor countries globally, and requires correspondingly differentiated strategies.</div>

<p class="ref"><b>Key references:</b> Sen, A. (1999). <i>Development as Freedom</i>. Oxford UP. | Dreze, J. & Sen, A. (2013). <i>An Uncertain Glory: India and Its Contradictions</i>. Princeton UP. | NITI Aayog (2023). SDG India Index and Dashboard. | Three.js documentation.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 60: India Food Geography 3D (Plotly 3D)
# ═══════════════════════════════════════════════════════════════════
G["60"] = '''
<h2>India Food Geography: Rice and Wheat in Three Dimensions</h2>
<p class="tagline">Green diamonds for rice. Gold squares for wheat. Height = production in million tonnes. India's food geography mirrors its monsoon geography.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Plotly 3D scatter</b> with Indian states plotted at their geographic coordinates (latitude, longitude). <b>Green diamonds</b> represent <b>rice production</b> and <b>gold squares</b> represent <b>wheat production</b>, both extruded vertically with <b>height proportional to production in million tonnes</b>. The visualization reveals the <b>sharp geographic division</b> between India's two staple cereals.</p>

<h3>The Monsoon Boundary as Food System Determinant</h3>
<div class="hl">India's rice-wheat divide is determined by <b>monsoon geography</b>. Rice requires <b>standing water during growth</b> (paddy cultivation) and thrives in areas with over 1,200 mm annual rainfall: the eastern Indo-Gangetic plain (West Bengal, Bihar, Assam), the western coast (Kerala, Karnataka), and the eastern coast (Andhra Pradesh, Odisha, Tamil Nadu). Wheat requires <b>cool, dry winters</b> for grain filling and thrives in areas with winter irrigation and temperatures below 20 degrees Celsius: Punjab, Haryana, western UP, Madhya Pradesh, and Rajasthan. The geographic boundary between the rice zone and the wheat zone runs roughly along the <b>80 degree East longitude line</b> through the Gangetic plain, shifting with local topography and irrigation infrastructure. This food geography is one of the oldest spatial patterns in Indian civilization: the rice cultures of the east and south and the wheat cultures of the north and west have shaped cuisine, culture, agricultural practice, and even political economy for millennia.</div>

<h3>The Green Revolution's Spatial Footprint</h3>
<div class="hl gold">The Green Revolution (1960s-1970s) transformed India's food geography by <b>concentrating production gains in specific regions</b>. The high-yielding wheat varieties developed by Norman Borlaug were adopted fastest in Punjab and Haryana, which had existing canal irrigation infrastructure (built during British colonial rule) and relatively large landholdings suitable for mechanization. The result was a dramatic concentration of wheat surplus in the Punjab-Haryana belt: these two states, covering less than 3% of India's area, produce approximately 30% of India's wheat and contribute a disproportionate share to the central procurement system (which purchases grain at minimum support prices for the public distribution system). Rice Green Revolution gains were more geographically diffuse but concentrated in the river deltas of the south and east. This geographic concentration of food production creates <b>spatial vulnerability</b>: any climate, water, or political disruption affecting Punjab threatens national food security.</div>

<h3>Climate Change and the Future of Indian Food Geography</h3>
<div class="hl warn">Climate projections pose severe threats to this food geography. <b>Wheat in Punjab-Haryana</b> faces rising temperatures that shorten the grain-filling period: studies project 3 to 17% yield decline per degree Celsius of warming, with the most severe impacts in the already-warm Indo-Gangetic plain. <b>Rice in West Bengal and Bangladesh</b> faces sea-level rise and increased cyclone intensity that threaten delta agriculture. <b>Groundwater depletion</b> in Punjab (water table dropping approximately 0.5 to 1 meter per year) threatens the irrigation that makes intensive agriculture possible. The spatial response will require <b>crop diversification</b> (shifting from water-intensive rice-wheat monoculture to drought-resistant millets, pulses, and oilseeds), <b>geographic diversification</b> (developing new production zones in currently underexploited regions like the Deccan plateau), and <b>variety adaptation</b> (heat-tolerant wheat varieties, salinity-tolerant rice varieties for coastal areas). India's food security in the 21st century depends on <b>reorganizing the spatial structure of its agriculture</b> in response to a changing climate.</div>

<p class="ref"><b>Key references:</b> Jha, D.K. & Jha, G.K. (2014). India's food production geography. <i>Economic and Political Weekly</i>, 49(52). | Lobell, D. et al. (2012). Extreme heat effects on wheat senescence in India. <i>Nature Climate Change</i>, 2(3). | Rodell, M. et al. (2009). Satellite-based estimates of groundwater depletion in India. <i>Nature</i>, 460(7258).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 61: Literacy-Gender Helix (Three.js)
# ═══════════════════════════════════════════════════════════════════
G["61"] = '''
<h2>Literacy-Gender Helix: Two Intertwined Strands of Human Development</h2>
<p class="tagline">Cyan for literacy, magenta for sex ratio. Where both strands bulge, development flourishes. Where they diverge, structural pathology is exposed.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Three.js double helix</b> with Indian states arranged along the vertical axis by <b>Human Development Index (HDI)</b>. Two intertwined strands encode: <b>cyan strand = literacy rate</b> (bulging outward = higher literacy) and <b>magenta strand = sex ratio</b> (bulging outward = more balanced, i.e., closer to or above 1,000 females per 1,000 males). The helix rotates, allowing the viewer to see the relative thickness of each strand at each state's position.</p>

<h3>Where the Strands Align: The Kerala Model</h3>
<div class="hl"><b>Kerala</b> appears at or near the top of the helix (high HDI), with <b>both strands bulging</b>: literacy at 96% and sex ratio at 1,084 (one of the few Indian states where women outnumber men, as in most biologically normal populations). This alignment is not coincidental: <b>female literacy and gender equity are mutually reinforcing</b>. Educated women are more likely to be in the workforce, more likely to have voice in household decisions, more likely to resist sex-selective practices, and more likely to invest in daughters' education. Kerala's social reform movements (starting in the 19th century with leaders like Narayan Guru and Ayyankali) simultaneously attacked caste discrimination and gender discrimination, creating a virtuous cycle that is visible in the helix as twin bulges.</div>

<h3>Where the Strands Diverge: The Haryana Paradox</h3>
<div class="hl gold"><b>Haryana</b> presents the helix's most instructive divergence: <b>moderate literacy</b> (approximately 76%) but <b>catastrophic sex ratio</b> (879 females per 1,000 males in 2011, among India's worst). This divergence demolishes the simplistic assumption that education automatically produces gender equity. Haryana's economy is relatively prosperous (high GSDP per capita due to proximity to Delhi and industrial development), and its education rates are above the national average. Yet the deep-rooted patriarchal norms of the Jat community (predominant in Haryana), combined with the economics of dowry (marrying a daughter is expensive, making daughters "costly"), have perpetuated sex-selective abortion even among educated, relatively wealthy families. The Haryana case demonstrates that <b>economic development and basic education are necessary but not sufficient for gender equity</b>: cultural transformation, legal enforcement (the PCPNDT Act against sex-selective abortion), and direct policy interventions are required independently.</div>

<h3>Bihar: Both Strands Thin</h3>
<p><b>Bihar</b> appears near the bottom of the helix (low HDI) with <b>both strands thin</b>: literacy at approximately 62% (India's lowest) and sex ratio at 907 (among the worst). Bihar represents the <b>compounding trap</b>: low literacy reduces economic productivity, which limits investment in girls' education, which perpetuates low sex ratios, which reduces the workforce, which limits economic growth. The geographic clustering of such states (Bihar, Jharkhand, UP, Madhya Pradesh) in north-central India creates a <b>spatial development deficit</b> that affects approximately 500 million people and that no national average can obscure.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The helix reveals three distinct policy challenges requiring different interventions. For <b>"both strands bulging" states</b> (Kerala, Goa): maintain gains, address emerging challenges (aging, unemployment, non-communicable diseases). For <b>"literacy high, sex ratio low" states</b> (Haryana, Punjab, Delhi): the binding constraint is not education but <b>cultural norms around son preference</b>. Interventions include strict PCPNDT Act enforcement, cash transfer programs conditional on keeping daughters (Beti Bachao Beti Padhao), and public campaigns that revalue daughters. For <b>"both strands thin" states</b> (Bihar, Jharkhand, UP): the priority is <b>basic education infrastructure</b>, particularly for girls, combined with economic development that increases the opportunity cost of early marriage and childbearing. The helix makes clear that <b>there is no single "women's empowerment" policy</b>; the appropriate intervention depends on which strand is thin and why.</div>

<p class="ref"><b>Key references:</b> Dreze, J. & Sen, A. (2013). <i>An Uncertain Glory</i>. Princeton UP. | Bhat, P.N. & Zavier, A.J. (2007). Factors influencing the use of prenatal diagnostic techniques and sex ratio at birth in India. <i>Economic and Political Weekly</i>, 42(24). | Census of India (2011). Sex ratio data.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 62: Constituency Aurora (Three.js)
# ═══════════════════════════════════════════════════════════════════
G["62"] = '''
<h2>Constituency Aurora: India's Democratic Energy Field</h2>
<p class="tagline">543 constituencies as breathing particles. Oscillation amplitude = turnout. Glow = margin. The aurora makes democratic health feel organic.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Three.js particle system</b> representing India's 543 Lok Sabha constituencies as floating, breathing points of light. Each particle's <b>oscillation amplitude</b> (how much it moves up and down) encodes <b>turnout</b>: high-turnout constituencies breathe deeply, low-turnout ones barely move. <b>Glow intensity</b> encodes <b>victory margin</b>: high-margin seats glow brightly, tight races shimmer faintly. <b>Beam effects</b> highlight the highest-margin seats. The overall effect is an aurora or star field where democratic vitality manifests as motion and light.</p>

<h3>The Aesthetic as Analytic</h3>
<div class="hl">This visualization deliberately breaks from the cartographic tradition (maps, choropleths, scatter plots) to represent democracy as a <b>living system</b>. The breathing metaphor is analytically appropriate: democracy is not a static structure but a dynamic process that requires continuous energy (voter participation) to function. Constituencies that "breathe deeply" (high turnout) are the healthy tissue of the democratic organism. Those that barely move (low turnout) represent democratic atrophy. The spatial distribution of breathing amplitude maps onto the same North-South divide visible in the LISA analysis (Chart 37): southern constituencies breathe deeply while northern ones are comparatively still. But the aurora format adds an <b>emotional and intuitive dimension</b> that analytical charts lack: the viewer <em>feels</em> the vitality differential rather than merely reading it from numbers.</div>

<h3>What the Glow Reveals</h3>
<div class="hl gold">The glow encoding (margin) adds a second layer. Paradoxically, <b>the "brightest" (highest-margin) constituencies are often the least democratically healthy</b>: a margin of 30 or 40 percentage points means that one party dominates so completely that meaningful electoral competition has ceased. These bright, still particles (high margin, often moderate turnout) are the safe seats where democracy has ossified. The most <b>democratically vital</b> constituencies are those that both breathe deeply (high turnout) <em>and</em> glow faintly (tight margins): these are the competitive, engaged constituencies where every vote matters and the outcome is genuinely uncertain. The aurora visualization makes this two-dimensional assessment of democratic health (participation x competition) visually intuitive.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The aurora format, by making democratic vitality visible and visceral, could serve as a <b>communication tool for electoral reform advocacy</b>. Showing citizens and policymakers a "breathing map" of democracy, where vast regions are barely alive, communicates the urgency of participation enhancement more effectively than statistical reports. The visualization also suggests a metric: the <b>average breathing depth</b> (national mean turnout weighted by competition) could serve as a summary "democratic health index" that captures both participation and competition in a single measure. Tracking this index across elections would reveal whether Indian democracy is becoming more or less vital over time.</div>

<p class="ref"><b>Key references:</b> Three.js documentation. | Dahl, R. (1971). <i>Polyarchy: Participation and Opposition</i>. Yale UP. | Norris, P. (2014). <i>Why Electoral Integrity Matters</i>. Cambridge UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 63: India Socioeconomic 3D (Plotly)
# ═══════════════════════════════════════════════════════════════════
G["63"] = '''
<h2>India Socioeconomic 3D: Literacy, GSDP, and HDI in Space</h2>
<p class="tagline">X = Literacy, Y = GSDP per capita, Z = HDI. Drop lines show each state's position in three-dimensional development space.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Plotly 3D scatter</b> with India's states plotted in three-dimensional development space: <b>X = literacy rate</b>, <b>Y = Gross State Domestic Product per capita</b>, <b>Z = Human Development Index</b>. <b>Drop lines</b> from each point to the XY-plane show how HDI (the vertical dimension) relates to the two input variables. Color may encode a fourth variable (region or sex ratio). The plot is interactive: rotate, zoom, and hover for state details.</p>

<h3>The Development Manifold in Indian State Space</h3>
<div class="hl">If development outcomes were determined by a simple linear combination of literacy and income, all states would lie on a flat plane in this 3D space. The deviations from the plane reveal states that <b>over- or under-achieve</b> their expected HDI given their literacy and GSDP. <b>Kerala</b> sits notably high on the Z-axis (HDI) relative to its Y-axis position (GSDP per capita), demonstrating that human development can outpace economic development when social investment is prioritized. <b>Delhi</b> and <b>Goa</b> have high Y (GSDP) but only moderately high Z (HDI), because income inequality within these territories means that high average income does not translate into universal human development. <b>Bihar</b> and <b>Jharkhand</b> sit in the low corner on all three axes: they are poor, illiterate, and underdeveloped in multidimensional terms.</div>

<h3>The Cluster Structure</h3>
<div class="hl gold">The 3D scatter reveals a <b>three-cluster structure</b> in Indian state development. <b>Cluster 1 (high-high-high)</b>: Kerala, Goa, Delhi, Himachal Pradesh, Tamil Nadu. These states combine relatively high literacy, moderate-to-high GSDP, and high HDI. <b>Cluster 2 (moderate-moderate-moderate)</b>: Maharashtra, Karnataka, Gujarat, West Bengal, Andhra Pradesh. These are India's "middle-income" states with development on multiple fronts but significant internal inequality. <b>Cluster 3 (low-low-low)</b>: Bihar, UP, Jharkhand, MP, Chhattisgarh, Odisha. These are India's "development deficit" states where all three dimensions are below national average. The spatial clustering (Clusters 1 and 2 in the south and west, Cluster 3 in the north and east) reinforces the north-south gradient discussed throughout this atlas, now visible in three-dimensional development space.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The 3D scatter reveals that <b>moving from Cluster 3 to Cluster 2 requires simultaneous investment in all three dimensions</b>: literacy alone will not increase GSDP (without jobs to absorb the literate workforce), GSDP alone will not increase HDI (without public investment in health and education), and HDI cannot improve without both economic resources and human capital. The states trapped in Cluster 3 need a <b>Big Push</b> (Rosenstein-Rodan, 1943): coordinated, large-scale, simultaneous investment across multiple sectors that creates the complementarities needed for self-sustaining development. Piecemeal interventions (a literacy campaign here, an industrial park there) are unlikely to move states across cluster boundaries because the dimensions are <b>complementary</b>, not independent.</div>

<p class="ref"><b>Key references:</b> Sen, A. (1999). <i>Development as Freedom</i>. Oxford UP. | UNDP (2023). <i>Human Development Report</i>. | Rosenstein-Rodan, P. (1943). Problems of industrialisation of Eastern and South-Eastern Europe. <i>Economic Journal</i>, 53(210-211). | Plotly documentation.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 64: Gender-Development Nexus (Plotly 3D)
# ═══════════════════════════════════════════════════════════════════
G["64"] = '''
<h2>Gender-Development Nexus: Sex Ratio, IMR, and Literacy in 3D</h2>
<p class="tagline">X = Sex Ratio, Y = Infant Mortality Rate (reversed), Z = Literacy. Color = sex ratio danger level. Kerala at the ideal corner. Haryana at the alarming opposite.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Plotly 3D scatter</b> mapping India's states across three gender-development variables: <b>X = Sex Ratio</b> (females per 1,000 males; higher is healthier), <b>Y = Infant Mortality Rate</b> (reversed so that lower IMR = higher position, i.e., better = up), <b>Z = Literacy Rate</b>. <b>Color gradient</b>: red = dangerously low sex ratio (below 930), yellow = moderate, green = healthy (above 1,000). The "ideal corner" of this space is upper-right-far (high sex ratio, low IMR, high literacy). The "crisis corner" is lower-left-near (low sex ratio, high IMR, low literacy).</p>

<h3>The Gender-Development Nexus</h3>
<div class="hl">This 3D scatter reveals that gender outcomes and development outcomes are <b>not independent dimensions but deeply correlated</b>. States in the "ideal corner" (Kerala, Tamil Nadu, Goa) have high sex ratios, low infant mortality, <em>and</em> high literacy because these outcomes share common determinants: <b>women's education</b> (educated women are less likely to accept sex-selective abortion, more likely to seek prenatal and postnatal care for infants, and contribute to overall literacy rates), <b>healthcare infrastructure</b> (reduces IMR and enables safe childbirth regardless of infant sex), and <b>social norms</b> (cultures that value daughters invest in their education and health). States in the "crisis corner" (Bihar, UP, Rajasthan, MP) have low sex ratios, high IMR, <em>and</em> low literacy because the same structural factors (patriarchal norms, underfunded services, low women's agency) drive all three outcomes in the same negative direction.</div>

<h3>The Haryana-Kerala Axis</h3>
<div class="hl gold">The most instructive comparison in the scatter is between <b>Haryana</b> and <b>Kerala</b>. Haryana (sex ratio 879, moderate literacy 76%, moderate IMR) sits in a peculiar position: it is <b>richer</b> than Kerala in per-capita income (reflecting proximity to Delhi and industrial development) but <b>far worse</b> on gender indicators. This Haryana-Kerala axis demonstrates that <b>economic development without social transformation can worsen gender outcomes</b>. In Haryana, rising incomes funded access to ultrasound technology, which was used for sex-selective abortion (leading to the worst sex ratios in India). In Kerala, rising incomes (though more modest) were channeled through a social framework that valued daughters equally, producing one of the world's healthiest sex ratios. The 3D scatter makes this divergence spatially visible: Haryana and Kerala occupy very different positions in gender-development space despite similar economic levels, demonstrating that <b>the path to the ideal corner is through social equity, not just economic growth</b>.</div>

<h3>The PCPNDT Act and Spatial Enforcement</h3>
<p>The <b>Pre-Conception and Pre-Natal Diagnostic Techniques (PCPNDT) Act</b>, which prohibits sex determination during pregnancy and sex-selective abortion, has been law since 1994 but its <b>enforcement varies dramatically across space</b>. States with strong enforcement (Maharashtra, which pioneered the act; Punjab, after intense civil society pressure) have seen sex ratios improve. States with weak enforcement (parts of UP, Rajasthan, and Gujarat) show minimal improvement. The geographic pattern of PCPNDT enforcement effectiveness maps onto the same cluster structure visible in this 3D scatter: states already near the ideal corner have the institutional capacity to enforce the law, while states in the crisis corner lack the governance infrastructure (registrar capacity, judiciary responsiveness, medical regulation) to make the law effective.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The 3D nexus reveals that <b>gender equality is not a standalone policy domain but is embedded in the broader development trajectory</b>. States cannot improve their sex ratio without also improving female literacy (which changes norms around son preference) and reducing infant mortality (which reduces the perceived "need" for sons as insurance against child death). Conversely, reducing infant mortality is harder when sex-selective practices eliminate female infants before they can be counted in mortality statistics. The <b>interdependence of these dimensions implies that siloed interventions (a sex ratio campaign without education reform, or a literacy program without healthcare) will be less effective than integrated, multi-dimensional strategies</b> that move states diagonally toward the ideal corner rather than along a single axis. The Women's Reservation Bill, by inserting women into political decision-making positions, could catalyze movement on all three dimensions simultaneously, as evidence from panchayat-level reservation suggests (Chattopadhyay and Duflo, 2004).</div>

<p class="ref"><b>Key references:</b> Sen, A. (1990). More than 100 million women are missing. <i>New York Review of Books</i>, 37(20). | Bhat, P.N. & Zavier, A.J. (2007). Factors influencing prenatal diagnostic techniques and sex ratio at birth in India. <i>EPW</i>, 42(24). | Chattopadhyay, R. & Duflo, E. (2004). Women as policy makers. <i>Econometrica</i>, 72(5). | Census of India (2011). State-level sex ratio data.</p>
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

print(f"\nPhase 4: Injected deep guides into {count} charts")
