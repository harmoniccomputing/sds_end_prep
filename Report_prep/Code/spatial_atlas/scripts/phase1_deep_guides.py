#!/usr/bin/env python3
"""Phase 1: Deep academic interpretation guides for charts 01-15.
Covers Global Development Dynamics, Corals & Oceans, People, Poverty, Technology tabs."""

import os, re

VIZ_DIR = "visualizations"

# CSS for the guide panel - flows below chart, generous space
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
# CHART 01: GDP vs Life Expectancy (Wealth vs Health)
# ═══════════════════════════════════════════════════════════════════
G["01"] = '''
<h2>Wealth vs Health of Nations</h2>
<p class="tagline">Does money buy life? The most important scatter plot in the history of public health.</p>

<h3>What You Are Seeing</h3>
<p>Each bubble represents one country in one year. The <b>horizontal axis</b> encodes GDP per capita in Purchasing Power Parity (PPP) international dollars on a <em>logarithmic scale</em>, meaning each major gridline represents a tenfold increase in national income. The <b>vertical axis</b> measures life expectancy at birth in years. <b>Bubble size</b> is proportional to total population, making China and India visually dominant. <b>Color</b> encodes continental membership. The <b>animation slider</b> at the bottom steps through years 1990 to 2023, revealing three decades of development in motion.</p>

<h3>The Preston Curve: Why This Shape Matters</h3>
<p>The concave relationship between income and longevity was first formally documented by Samuel Preston in 1975. His landmark study in <i>Demography</i> showed that life expectancy rises steeply at low income levels and then flattens at higher incomes. The underlying mechanism is not mysterious: at very low GDP per capita ($500 to $5,000), economic growth funds the basics of survival, including clean water infrastructure, primary healthcare clinics, vaccination programs, nutritional adequacy, and sanitation systems. Going from $1,000 to $5,000 GDP per capita typically adds 12 to 18 years of life expectancy. Going from $50,000 to $100,000 adds perhaps 1 to 2 years. The logarithmic X-axis is not a cosmetic choice; it linearizes this fundamentally non-linear relationship, making the diminishing returns visible as a flattening rather than a cramped cluster.</p>

<h3>The Spatial Dimension: Continental Clustering and Outliers</h3>
<div class="hl">The most striking spatial feature is the <b>continental clustering</b>. Sub-Saharan African nations cluster in the lower-left (low wealth, low health). European nations cluster in the upper-right. But the boundaries of these clusters have shifted dramatically between 1990 and 2023. East Asian nations (China, Vietnam, Thailand) have made the most dramatic rightward and upward migration of any continental group, reflecting the region's economic transformation. Meanwhile, certain countries break their continental pattern. <b>Equatorial Guinea</b> (high GDP from oil, but low life expectancy due to extreme inequality and poor governance) sits far to the right of the Preston Curve, a spatial anomaly that reveals how resource extraction wealth without redistribution fails to translate into population health. Conversely, <b>Cuba and Sri Lanka</b> sit above the curve: their life expectancies exceed what their GDP would predict, evidence that targeted public health investment can substitute for aggregate wealth.</div>

<h3>Tobler's First Law in Action</h3>
<p>Waldo Tobler's First Law of Geography states that "everything is related to everything else, but near things are more related than distant things." This chart, though not plotted on a geographic coordinate system, reveals this principle vividly: nations that are geographic neighbors tend to cluster together in GDP-life-expectancy space. West African nations move as a cluster. Scandinavian nations cluster tightly. Central Asian post-Soviet states form their own neighborhood. This spatial autocorrelation of development outcomes is not coincidental. It reflects shared colonial histories, regional trade networks, epidemiological corridors (diseases spread regionally), knowledge diffusion effects, and common ecological and climatic constraints on agriculture and disease burden.</p>

<h3>Temporal Dynamics: What the Animation Reveals</h3>
<div class="hl gold">As you press play and watch bubbles migrate rightward (richer) and upward (healthier), you are witnessing the single most important fact about the modern world: <b>global health has improved dramatically and nearly universally</b>. But the animation also reveals catastrophes. Between roughly 1995 and 2005, several Southern African nations (Botswana, Swaziland, Lesotho, South Africa) experienced a stunning <em>downward</em> movement as HIV/AIDS reduced life expectancy by 10 to 15 years. The subsequent recovery, driven by antiretroviral therapy (ARV) scale-up funded by PEPFAR and the Global Fund, is equally dramatic and represents one of the most successful international health interventions in history. Russia and several post-Soviet states experienced a notable dip in the early 1990s following the collapse of the Soviet Union, reflecting what demographers call a "mortality crisis" driven by alcoholism, cardiovascular disease, and the collapse of the public health system during economic shock therapy.</div>

<h3>The "Big Convergence" Thesis</h3>
<p>Global health economists (notably Dean Jamison et al. in <i>The Lancet</i>, 2013) have argued that we are witnessing a "grand convergence" in global health: the gap in life expectancy between the richest and poorest countries has narrowed substantially. In 1990, the gap between the top and bottom deciles of country life expectancy was approximately 30 years. By 2023, it had narrowed to approximately 20 years. This convergence is driven by dramatic reductions in infectious disease mortality in low-income countries, which account for the steepest part of the Preston Curve. Whether this convergence will continue depends on whether low-income countries can also tackle the "second wave" of non-communicable diseases (diabetes, cardiovascular disease, cancer) that typically surge as incomes rise and diets change.</p>

<h3>Policy Implications: Where You Sit on the Curve Determines What You Need</h3>
<div class="hl warn">For countries on the <b>steep part</b> of the curve ($1K to $10K GDP per capita), economic growth is the most powerful health intervention available. Each percentage point of GDP growth translates into measurable reductions in child mortality, infectious disease burden, and maternal mortality. The policy priority is <b>broad-based growth</b> (not just resource extraction) coupled with basic public health infrastructure. For countries on the <b>flat part</b> (above approximately $30K), further GDP growth yields marginal health gains. Here, the policy frontier shifts to <b>healthcare equity</b> (the US spends more per capita than any nation but has lower life expectancy than many peers due to inequality of access), <b>mental health</b> (which is the leading source of disability in wealthy nations), <b>lifestyle disease prevention</b> (obesity, sedentary behavior, substance use), and <b>environmental determinants</b> (air quality, food systems). The fundamental insight is that the appropriate health strategy is contingent on where a nation sits along the Preston Curve, and no single policy framework applies universally.</div>

<h3>The Spatial Trap</h3>
<div class="hl">Sub-Saharan African nations face a compounding spatial trap. Poor health reduces economic productivity, which perpetuates poverty, which maintains poor health. But the spatial dimension adds a further layer: these nations are geographically clustered together, meaning that disease outbreaks cross borders (Ebola, malaria), skilled workers emigrate to richer regions (brain drain), and trade barriers compound (landlocked nations face even steeper challenges). Breaking this cycle requires <b>simultaneous, regionally coordinated investment</b> in health and economic infrastructure. The African Continental Free Trade Area (AfCFTA, launched 2021) represents one such attempt: by creating a continental market of 1.3 billion people, it aims to generate the internal demand that could fuel the rightward migration of African bubbles on this chart.</div>

<p class="ref"><b>Key references:</b> Preston, S. (1975). The changing relation between mortality and level of economic development. <i>Demography</i>, 12(2). | Deaton, A. (2013). <i>The Great Escape: Health, Wealth, and the Origins of Inequality</i>. Princeton UP. | Jamison, D. et al. (2013). Global health 2035: a world converging within a generation. <i>The Lancet</i>, 382(9908). | Rosling, H. (2018). <i>Factfulness</i>. Flatiron Books.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 02: Fertility vs Life Expectancy
# ═══════════════════════════════════════════════════════════════════
G["02"] = '''
<h2>Fertility vs Longevity: The Demographic Transition in Motion</h2>
<p class="tagline">Humanity's most consequential transformation, playing out across geography and time.</p>

<h3>Reading the Axes</h3>
<p><b>X-axis: Total Fertility Rate (TFR)</b>, defined as the average number of children a woman would bear over her lifetime if she experienced the current age-specific fertility rates at each age. Values above <em>2.1</em> indicate population growth above replacement level. The 0.1 above 2.0 accounts for child mortality before reproductive age. Below 2.1 implies eventual population decline without immigration. <b>Y-axis: Life Expectancy at Birth</b>, the average number of years a newborn would live if subjected to the mortality rates prevailing at the time of their birth throughout their life.</p>

<h3>The Demographic Transition Model</h3>
<p>This chart is the single best visualization of <b>Demographic Transition Theory</b> (Warren Thompson, 1929; Frank Notestein, 1945). The theory describes a universal four-stage process. In <b>Stage 1</b> (pre-industrial), both birth rates and death rates are high, and population grows slowly. In <b>Stage 2</b> (early transition), death rates fall due to improved sanitation and medicine while birth rates remain high, producing rapid population growth. In <b>Stage 3</b> (late transition), birth rates begin to fall as urbanization, education, and contraception take hold. In <b>Stage 4</b> (post-transition), both rates are low, and population stabilizes or begins to decline. Some demographers now add a <b>Stage 5</b> in which fertility falls so far below replacement (TFR below 1.5) that population decline accelerates, as seen in Japan, South Korea, Italy, and increasingly China.</p>

<h3>The Spatial Geography of Transition</h3>
<div class="hl">The demographic transition has a clear <b>spatial diffusion pattern</b>. It began in Northwestern Europe in the late 18th century (France was the first country to experience sustained fertility decline, around 1790). It spread to North America, Australasia, and Southern Europe by the early 20th century. East Asia underwent a compressed, rapid transition from the 1960s to 1990s (South Korea's TFR went from 6.0 in 1960 to 1.6 in 1990). Latin America and South Asia followed from the 1970s onward. <b>Sub-Saharan Africa</b> is the last major world region to enter the transition, with fertility declining from approximately 6.5 in 1990 to approximately 4.5 in 2023. The geographic pattern follows pathways of <b>colonial contact, trade connectivity, educational expansion, and urbanization</b>, confirming that the demographic transition is fundamentally a spatially diffusing phenomenon rather than an independent parallel process.</div>

<h3>Why Fertility Falls: Five Interacting Mechanisms</h3>
<div class="two-col">
<div class="hl"><b>1. Child mortality decline</b>: When parents are confident their children will survive, they have fewer. This is the initiating trigger in most historical transitions. The relationship is so strong that child mortality reduction is sometimes called the "demographic gift" that launches the transition.</div>
<div class="hl"><b>2. Women's education</b>: Each additional year of female secondary education reduces fertility by 0.3 to 0.5 children per woman (World Bank estimates). Education delays marriage, increases contraceptive knowledge, raises the opportunity cost of childbearing, and expands women's agency in reproductive decisions.</div>
<div class="hl"><b>3. Urbanization</b>: In agricultural economies, children are productive assets (farm labor) by age 6 to 8. In urban economies, children are expensive consumption goods requiring years of education before they become economically productive. This economic inversion is the single strongest structural driver of fertility decline.</div>
<div class="hl"><b>4. Contraceptive access</b>: The availability of modern contraception (pills, IUDs, implants) reduces the gap between desired and actual fertility. In many Sub-Saharan African countries, unmet need for contraception exceeds 25%, meaning a quarter of women who want to limit or space births lack access to methods.</div>
</div>
<div class="hl gold"><b>5. Ideational change</b>: As societies globalize, norms about family size, women's roles, and individual autonomy shift. Television and mobile phones accelerate this diffusion. Researchers have shown that exposure to Brazilian telenovelas (which portray small, affluent families) measurably reduced fertility in Brazilian municipalities that received TV signals.</div>

<h3>The Two Population Futures</h3>
<div class="hl warn">Global population projections hinge on one question: <b>how fast will Sub-Saharan Africa complete its transition?</b> The UN's medium projection (10.4 billion by 2100) assumes a gradual decline in African fertility. The low projection (7.3 billion) assumes accelerated decline. The difference, approximately 3 billion people, is almost entirely determined by policy choices in approximately 25 African countries over the next three decades. Nigeria alone could have anywhere from 400 million to 800 million people by 2100 depending on its fertility trajectory. The geopolitical, environmental, and economic implications of this range are staggering. Meanwhile, the countries at the bottom-right of this chart (South Korea TFR 0.7, Japan 1.2, Italy 1.2, Spain 1.2) face the opposite crisis: population aging and shrinkage that threatens pension systems, labor markets, and economic dynamism. <b>There is no precedent in human history for sustained fertility this far below replacement</b>, and no proven policy toolkit for reversing it (pronatalist subsidies in countries like Hungary and Japan have had only marginal effects).</div>

<h3>Anthropological Perspective: The "Quantity-Quality" Tradeoff</h3>
<p>Economist Gary Becker (1960) formalized what anthropologists had long observed: as societies develop, parents substitute <b>quantity of children for quality of investment per child</b>. In pre-transition societies, having many children is rational because each child costs little (no school fees, no healthcare costs beyond folk medicine) and begins contributing labor early. In post-transition societies, each child requires 15 to 25 years of expensive investment (education, healthcare, housing) before becoming economically independent. This shift from "many cheap children" to "few expensive children" is visible in the animation as countries trace a path from upper-left (high fertility, low life expectancy) to lower-right (low fertility, high life expectancy). The path is never reversed: <b>no country that has completed the demographic transition has returned to high fertility</b>.</p>

<p class="ref"><b>Key references:</b> Notestein, F. (1945). Population: The long view. In Schultz, T. (ed.), <i>Food for the World</i>. | Becker, G. (1960). An economic analysis of fertility. In <i>Demographic and Economic Change in Developed Countries</i>. | Caldwell, J. (1982). <i>Theory of Fertility Decline</i>. Academic Press. | La Ferrara, E., Chong, A. & Duryea, S. (2012). Soap operas and fertility: Evidence from Brazil. <i>American Economic Journal: Applied Economics</i>, 4(4).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 03: Child Mortality vs GDP
# ═══════════════════════════════════════════════════════════════════
G["03"] = '''
<h2>Child Mortality vs National Wealth: The Price of Poverty in Children's Lives</h2>
<p class="tagline">Under-5 mortality is the most sensitive barometer of a society's commitment to its most vulnerable members.</p>

<h3>What You Are Seeing</h3>
<p>Each bubble is a country-year. The <b>X-axis</b> shows GDP per capita (PPP) on a logarithmic scale. The <b>Y-axis</b> shows the under-5 mortality rate (U5MR): the probability that a child born in a given year will die before reaching age 5, expressed per 1,000 live births. A value of 100 means 1 in 10 children dies. A value of 200 means 1 in 5. In 1990, several countries (Mali, Sierra Leone, Niger) had U5MR above 300, meaning nearly a third of all children died before their fifth birthday.</p>

<h3>The Steepness of the Left Side</h3>
<div class="hl">The relationship between wealth and child survival is strikingly steep at low incomes and remarkably flat at high incomes. The first $5,000 of GDP per capita reduces under-5 mortality by approximately 150 to 200 per 1,000. The next $45,000 (from $5K to $50K) reduces it by perhaps 20 to 30 more. This asymmetry reflects the underlying causes of child death in poor countries: <b>diarrheal diseases</b> (killed by clean water and oral rehydration salts, costing pennies), <b>pneumonia</b> (killed by antibiotics costing cents), <b>malaria</b> (killed by insecticide-treated bed nets costing $2 each), <b>measles</b> (killed by vaccines costing $0.25 per dose), and <b>neonatal complications</b> (reduced by skilled birth attendants). The interventions that save children's lives in the poorest countries are <em>astonishingly cheap</em>, which is why targeted public health spending can produce results far exceeding what GDP alone would predict.</div>

<h3>Spatial Patterns: The "Belt of Child Death"</h3>
<p>If you could paint each country on a world map according to its position on this chart, a clear geographic pattern would emerge. The highest under-5 mortality rates form a <b>contiguous belt across West and Central Africa</b>, from Guinea-Bissau through Nigeria to Chad and the Central African Republic. This belt corresponds to multiple overlapping geographic disadvantages: tropical climate (malaria, other vector-borne diseases), Sahelian aridity (food insecurity), landlocked geography (limited trade access), and the legacy of extractive colonial institutions. The spatial clustering is not coincidental. Disease vectors (mosquitoes) do not respect borders. Conflict in one country creates refugee flows that overwhelm health systems in neighbors. Skilled health workers emigrate regionally. The "neighborhood effect" in child mortality is strong: a country's U5MR is significantly predicted by the average U5MR of its geographic neighbors, even after controlling for that country's own GDP and health spending.</p>

<h3>The Bangladesh Exception: Geography vs Policy</h3>
<div class="hl gold">Bangladesh deserves special attention. With a GDP per capita of approximately $5,000 (PPP) in 2023, Bangladesh's under-5 mortality rate (28 per 1,000) is lower than that of many countries two or three times richer. This exceptional performance is attributed to: (1) <b>BRAC</b>, the world's largest NGO, which built a parallel primary healthcare system reaching 100 million people; (2) widespread <b>oral rehydration therapy</b> (Bangladesh pioneered ORT in the 1970s at the International Centre for Diarrhoeal Disease Research); (3) <b>community health workers</b> providing door-to-door vaccination and nutrition counseling; (4) high female <b>literacy</b> (73%, far above its income peers in South Asia and Africa). Bangladesh demonstrates that the Preston Curve is not destiny: with the right policies, countries can dramatically outperform their wealth level. The spatial implication is that policy diffusion, not just geographic proximity, matters for health outcomes.</div>

<h3>Temporal Dynamics: The Millennium Development Goals Effect</h3>
<p>The animation reveals a notable acceleration in child mortality reduction after approximately 2000. This coincides with the adoption of the <b>Millennium Development Goals (MDGs)</b>, of which Goal 4 was to reduce under-5 mortality by two-thirds between 1990 and 2015. While the global target was not fully met, the MDG framework catalyzed an unprecedented mobilization of resources: GAVI (the Vaccine Alliance, est. 2000) vaccinated 500 million children; the Global Fund (est. 2002) distributed billions of bed nets; PEPFAR (est. 2003) scaled up HIV treatment for mothers. The result was that global under-5 deaths fell from 12.6 million per year in 1990 to approximately 5.0 million in 2023. This demonstrates that <b>coordinated international goal-setting with measurable targets works</b>, a lesson directly applicable to the Sustainable Development Goals (SDGs) for 2030.</p>

<h3>Policy Implications: The "Low-Hanging Fruit" Paradox</h3>
<div class="hl warn">The steepness of the left side of this chart implies that the <b>most cost-effective life-saving interventions on Earth</b> are concentrated in the poorest countries. GiveWell estimates that distributing insecticide-treated bed nets saves a life for approximately $3,000 to $5,000. Vitamin A supplementation saves a life for approximately $3,500. These are orders of magnitude cheaper than any medical intervention in wealthy countries. The paradox is that global health spending is inversely proportional to need: the US spends approximately $12,000 per person per year on health; countries with the highest child mortality spend $10 to $50. Even small redistributions of global health spending toward the steep part of the curve would save millions of lives. The spatial concentration of child mortality in a relatively small number of countries (Nigeria alone accounts for approximately 15% of global child deaths) means that geographically targeted interventions can have outsized impact.</div>

<p class="ref"><b>Key references:</b> UNICEF (2023). <i>Levels & Trends in Child Mortality</i>. UN Inter-agency Group for Child Mortality Estimation. | Victora, C. et al. (2003). Applying an equity lens to child health and mortality. <i>The Lancet</i>, 362(9379). | GiveWell (2024). Cost-effectiveness estimates for malaria interventions. | Chowdhury, A.M.R. et al. (2013). The Bangladesh paradox. <i>The Lancet</i>, 382(9906).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 04: Country Trajectories
# ═══════════════════════════════════════════════════════════════════
G["04"] = '''
<h2>Country Trajectories: Fourteen Development Paths Through Time</h2>
<p class="tagline">History's arc visualized: each line is a nation's journey through the landscape of wealth and health.</p>

<h3>What You Are Seeing</h3>
<p>Fourteen countries are traced through time (1990 to 2023) across the GDP-per-capita (log scale) vs life-expectancy plane. Each line is a country's path, with markers at key years. Arrows indicate the direction of travel. The selection deliberately spans the full range of development experiences: rapid climbers (China, India, Vietnam), steady advancers (Brazil, Indonesia), crisis survivors (Russia, South Africa), stagnators (Nigeria), and the global frontier (US, Japan, Germany, France, UK).</p>

<h3>Reading the Trajectories</h3>
<div class="hl"><b>China's trajectory</b> is the most dramatic: starting at approximately $1,500 GDP per capita and 69 years life expectancy in 1990, it traces a steep diagonal to approximately $18,000 and 78 years by 2023. This is the fastest large-scale development in human history, moving 800 million people out of extreme poverty. The path briefly flattens during the 2020-2022 COVID period. <b>South Africa's</b> trajectory shows a haunting U-shape in the vertical dimension: life expectancy plummeted from 62 years in 1990 to 52 years around 2005 (HIV/AIDS crisis), then recovered to 65 by 2023 after antiretroviral therapy scale-up. Meanwhile, GDP per capita barely changed, producing a vertical "dip and recovery" that is unique to the HIV-affected nations of Southern Africa.</div>

<h3>Spatial Patterns in Development Paths</h3>
<p>The trajectories reveal <b>spatial clustering of development experiences</b>. European nations (Germany, France, UK) trace nearly identical paths at the upper-right frontier, advancing together. This is not coincidental: EU integration, shared institutions, and economic interdependence mean that European development outcomes are spatially correlated. Similarly, South and Southeast Asian nations (India, Vietnam, Indonesia) show roughly parallel trajectories in the center of the chart, reflecting shared characteristics of the "Asian Development Model" (export-led growth, investment in human capital, demographic dividend exploitation). The divergence of paths within Africa (Nigeria stagnating while Ethiopia, not shown, accelerated) highlights that continental generalizations obscure enormous within-continent variation.</p>

<h3>Regime Changes and Shocks</h3>
<div class="hl gold"><b>Russia</b> shows a dramatic leftward-then-rightward path in the early 1990s: GDP per capita collapsed during the post-Soviet transition (shock therapy, privatization, institutional breakdown), while life expectancy, particularly for men, fell sharply. Russian male life expectancy dropped from 64 to 57 years between 1990 and 1994, driven by cardiovascular disease, alcoholism, violence, and despair. The subsequent recovery under oil-fueled growth (2000s) produced a rightward-upward trajectory. This "reversal and recovery" pattern is shared by other post-Soviet states (Ukraine, Kazakhstan) and illustrates that <b>development is not monotonically progressive</b>: political and economic shocks can set countries back by decades.</div>

<h3>The "Great Escape" and Those Left Behind</h3>
<div class="hl warn">Angus Deaton (Nobel 2015) described the overall pattern as a "Great Escape" from poverty and early death. But the trajectories make clear that the escape is <b>unevenly paced</b>. The gap between China's endpoint and Nigeria's endpoint in 2023 is approximately $16,000 in GDP and 23 years in life expectancy, a chasm that has widened, not narrowed, since 1990. The spatial dimension matters because these divergent trajectories have geopolitical consequences: migration flows, conflict risks, and international aid dependencies all follow the gradient from left-side to right-side nations. The trajectories also reveal the role of <b>geography as destiny vs geography as starting point</b>: tropical, landlocked nations tend to have flatter trajectories, while coastal, temperate nations tend to advance faster, though exceptions (Rwanda, Ethiopia) demonstrate that institutional quality can partially overcome geographic constraints.</div>

<p class="ref"><b>Key references:</b> Deaton, A. (2013). <i>The Great Escape</i>. Princeton UP. | Sachs, J. (2001). Tropical underdevelopment. NBER Working Paper 8119. | Acemoglu, D. & Robinson, J. (2012). <i>Why Nations Fail</i>. Crown Business. | Milanovic, B. (2016). <i>Global Inequality</i>. Harvard UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 05: Continental Trends (3-panel)
# ═══════════════════════════════════════════════════════════════════
G["05"] = '''
<h2>Continental Trends: Three Panels of Global Convergence and Divergence</h2>
<p class="tagline">Do continents converge or diverge? The answer depends on which variable you examine.</p>

<h3>What You Are Seeing</h3>
<p>Three synchronized panels show the trajectory of each continent (represented by its population-weighted mean) across three metrics over 1990 to 2023. <b>Left panel</b>: Life expectancy. <b>Center panel</b>: GDP per capita. <b>Right panel</b>: Fertility rate. Continental means are computed annually, with bubble size proportional to total continental population. The panels together tell a story of partial convergence: continents are becoming more similar in health, but <em>not</em> in wealth.</p>

<h3>The Convergence Asymmetry</h3>
<div class="hl"><b>Life expectancy is converging</b>. In 1990, Africa's mean life expectancy was approximately 51 years and Europe's approximately 73, a gap of 22 years. By 2023, Africa had risen to approximately 64 and Europe to approximately 79, narrowing the gap to 15 years. This convergence was driven by infectious disease reduction (HIV/AIDS treatment, malaria control, childhood vaccination) in Africa. <b>GDP per capita is diverging</b>, or at best, stagnating in relative terms. Europe's mean GDP per capita grew from approximately $25,000 to $42,000 while Africa's grew from approximately $2,500 to $4,000. The absolute gap widened from $22,500 to $38,000. <b>Fertility is converging</b>: every continent's fertility rate moved toward the 1.5 to 2.5 range, with Africa the last holdout above 4.0.</div>

<h3>Why Health Converges But Wealth Does Not</h3>
<div class="hl gold">The asymmetry reveals a fundamental insight about the nature of development knowledge. <b>Medical and public health knowledge is a pure public good</b>: once oral rehydration therapy is invented, it can be deployed anywhere at near-zero marginal cost. Vaccines, antibiotics, insecticides, and contraceptives are all technologies that can be transferred across geography. <b>Economic productivity, by contrast, depends on institutions, infrastructure, human capital, and governance</b>, which are geographically sticky, historically path-dependent, and slow to transfer. You can ship a million doses of vaccine to a country in a week; you cannot ship a functioning legal system, a skilled labor force, or a culture of entrepreneurship. This is why Lant Pritchett (1997) described the pattern as "divergence, big time" for income, while health researchers see "convergence, finally" for life expectancy.</div>

<h3>The African Trajectory: Will the Demographic Dividend Arrive?</h3>
<div class="hl warn">Africa's trajectory on all three panels holds the key to humanity's 21st-century future. If fertility continues to decline (right panel), Africa will enter its <b>demographic dividend</b> period: a window when the working-age population is large relative to dependents, creating an economic boost that fueled East Asia's rise in the 1970s to 1990s. But the dividend is not automatic. It requires massive investment in education, job creation, and infrastructure to absorb the youth bulge productively. If the dividend is captured, Africa's GDP line (center panel) will begin to steepen upward. If not, the youth bulge becomes a source of unemployment, instability, and outward migration. The geographic clustering of high-fertility, low-GDP nations in a contiguous belt across the Sahel means that failure in this region would create spillover effects (refugee flows, conflict diffusion, ecological pressure) that would be felt globally.</div>

<p class="ref"><b>Key references:</b> Pritchett, L. (1997). Divergence, big time. <i>Journal of Economic Perspectives</i>, 11(3). | Bloom, D. & Williamson, J. (1998). Demographic transitions and economic miracles in emerging Asia. <i>World Bank Economic Review</i>, 12(3). | Deaton, A. (2004). Health in an age of globalization. NBER Working Paper 10669.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 06: Income Distribution Shift
# ═══════════════════════════════════════════════════════════════════
G["06"] = '''
<h2>Income Distribution Shift: From Bimodal to Unimodal</h2>
<p class="tagline">The world's income distribution has transformed from two humps to one. The "developing world" no longer exists as a distinct category.</p>

<h3>What You Are Seeing</h3>
<p>A series of global income distribution curves (kernel density estimates) plotted on a logarithmic income axis. Each curve represents a snapshot year. In the earliest year, the distribution is visibly <b>bimodal</b>: two separate humps, one centered around $1,000 to $2,000 (the "poor world") and one around $20,000 to $40,000 (the "rich world"), with a valley between them. Over time, the left hump shrinks and shifts rightward, while the valley fills in, producing a single, broader peak: the <b>unimodal</b> distribution of a more integrated world economy.</p>

<h3>The End of "First World / Third World"</h3>
<div class="hl">The bimodal distribution of the 1970s to 1990s was the statistical basis for the "First World / Third World" dichotomy that dominated 20th-century political and economic discourse. The two humps were real: there were genuinely two clusters of nations with a gap between them. The shift to unimodality reflects the <b>rise of the global middle class</b>, concentrated overwhelmingly in Asia. Between 1990 and 2023, approximately 1.5 billion people crossed from the left hump to the center of the distribution. The primary drivers were <b>China</b> (which alone accounts for approximately 800 million of these transitions) and <b>India, Indonesia, Vietnam, and Bangladesh</b>. Hans Rosling famously used this chart to argue that the "developing world" is a misleading concept: there is no longer a discrete cluster of poor nations separated from a discrete cluster of rich ones. Instead, there is a continuous gradient.</div>

<h3>Spatial Implications of Unimodality</h3>
<div class="hl gold">The shift from bimodality to unimodality has profound spatial consequences. In the bimodal era, global economic geography was essentially an archipelago model: islands of wealth (Western Europe, North America, Japan, Australasia) surrounded by a sea of poverty. Trade, investment, and migration flowed in predictable patterns between the two clusters. In the unimodal era, the economic geography is more of a <b>gradient</b>: wealth varies continuously across space. This creates new spatial patterns. Urban areas in "developing" countries now have income levels comparable to rural areas in "developed" countries. Shanghai's per capita income exceeds that of Mississippi. Nairobi's tech sector generates wealth comparable to mid-tier European cities. The gradient model implies that <b>within-country inequality</b> (urban vs rural, coast vs interior) is now often larger than <b>between-country inequality</b>, which is exactly what Branko Milanovic's work on global inequality has confirmed.</div>

<h3>Who Is Still in the Left Tail?</h3>
<div class="hl warn">While the overall shift is encouraging, the <b>left tail of the distribution has not disappeared</b>. Approximately 700 million people still live below $2.15/day (World Bank extreme poverty line). These individuals are geographically concentrated: roughly half are in Sub-Saharan Africa (Nigeria, DRC, Tanzania, Ethiopia, Madagascar) and much of the remainder in South Asia (India, Bangladesh). The spatial concentration of extreme poverty has actually <em>increased</em> as China and East Asia exited the left tail. In 1990, extreme poverty was distributed across three continents; by 2023, it is predominantly an African and South Asian phenomenon. This geographic concentration means that poverty reduction increasingly requires <b>context-specific, regionally tailored strategies</b> rather than one-size-fits-all global programs. The drivers of poverty in the Sahel (drought, conflict, governance failure) are fundamentally different from those in South Asian river deltas (flooding, density, landlessness).</div>

<p class="ref"><b>Key references:</b> Rosling, H. (2018). <i>Factfulness</i>. Flatiron Books. | Milanovic, B. (2016). <i>Global Inequality: A New Approach for the Age of Globalization</i>. Harvard UP. | Sala-i-Martin, X. (2006). The world distribution of income. <i>Quarterly Journal of Economics</i>, 121(2). | World Bank (2023). <i>Poverty and Shared Prosperity</i>.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 07: Coral Bleaching Hotspots
# ═══════════════════════════════════════════════════════════════════
G["07"] = '''
<h2>Reef Bleaching Hotspots: The Geography of Marine Ecosystem Collapse</h2>
<p class="tagline">Coral reefs occupy 0.1% of the ocean floor but support 25% of all marine species. They are dying in geographically predictable patterns.</p>

<h3>What You Are Seeing</h3>
<p>A world map showing 27 major coral reef systems. Marker size and color encode bleaching severity and frequency. The map reveals that bleaching is not uniformly distributed: it follows specific oceanographic and geographic patterns related to sea surface temperature (SST) anomaly exposure, reef latitude, and ocean circulation systems.</p>

<h3>Why Reefs Bleach: The Thermal Threshold</h3>
<div class="hl">Coral bleaching occurs when water temperatures exceed the coral's thermal tolerance, typically 1 to 2 degrees Celsius above the local long-term maximum monthly mean (MMM). At this point, the coral expels its symbiotic zooxanthellae algae, which provide up to 90% of the coral's energy through photosynthesis. Without these algae, the coral appears white ("bleached") and begins to starve. If temperatures return to normal within approximately 4 to 8 weeks, the coral can recover by reacquiring zooxanthellae. If the thermal stress persists beyond this window, the coral dies. The critical metric used by NOAA's Coral Reef Watch is <b>Degree Heating Weeks (DHW)</b>: the accumulated thermal stress over the previous 12 weeks, measured in degree Celsius-weeks. DHW above 4 triggers significant bleaching. DHW above 8 triggers widespread mortality.</div>

<h3>The Spatial Pattern: Why Some Reefs Survive</h3>
<div class="hl gold">The map reveals that bleaching severity is <b>not uniform across latitude or longitude</b>. Several spatial factors determine vulnerability. <b>Equatorial reefs</b> (within 10 degrees of the equator) experience less seasonal temperature variation, meaning their thermal tolerance window is narrower: even small anomalies push them past their threshold. <b>Eastern boundary current regions</b> (e.g., the coast of East Africa, the eastern Pacific) experience upwelling of cooler deep water, which can buffer against surface warming. <b>High-latitude reefs</b> (subtropical Japan, Bermuda, Lord Howe Island) have wider thermal ranges and may serve as future climate refugia, but they are also among the first to experience novel warm-water conditions as isotherms shift poleward. <b>The Coral Triangle</b> (Indonesia, Philippines, Papua New Guinea), the most biodiverse marine region on Earth, is particularly threatened because its reefs have evolved in relatively stable thermal environments and thus have limited acclimatization capacity.</div>

<h3>Connection to Climate Modes: ENSO and the Indian Ocean Dipole</h3>
<p>Mass bleaching events are strongly associated with <b>El Nino-Southern Oscillation (ENSO)</b> warm phases. The three global-scale mass bleaching events on record (1998, 2010, 2015-2016) all coincided with major El Nino events, which raise SSTs across the tropical Pacific and Indian Oceans. The <b>Indian Ocean Dipole (IOD)</b> modulates bleaching in the western Indian Ocean: positive IOD phases warm the western Indian Ocean, intensifying bleaching risk for East African and Maldivian reefs. The spatial distribution of bleaching in any given year is therefore a function of both long-term warming trend and short-term climate mode oscillation. As background warming raises the baseline SST, El Nino events that were previously survivable become lethal, because the additive thermal stress exceeds the bleaching threshold more frequently.</p>

<h3>Socioeconomic Implications: The Reef as Spatial Infrastructure</h3>
<div class="hl warn">Coral reefs are not just ecological features; they are <b>spatial infrastructure</b> for approximately 500 million people who depend on them for food, income, coastal protection, and cultural identity. Reef fisheries provide the primary protein source for many island nations in the Pacific and Indian Oceans. Reef structures dissipate 97% of wave energy, protecting shorelines from erosion and storm surge (the replacement cost of this natural breakwater has been estimated at $9.9 billion per year globally). Reef tourism generates approximately $36 billion annually. The geographic concentration of reef-dependent communities in Small Island Developing States (SIDS) means that reef loss is an existential threat to national economies with no terrestrial alternative: nations like the Maldives, Kiribati, and Tuvalu have no hinterland to retreat to. The spatial pattern of bleaching thus maps directly onto patterns of climate injustice: the nations least responsible for carbon emissions are the most dependent on reefs and the most vulnerable to their loss.</div>

<p class="ref"><b>Key references:</b> Hughes, T. et al. (2018). Spatial and temporal patterns of mass bleaching of corals in the Anthropocene. <i>Science</i>, 359(6371). | NOAA Coral Reef Watch (2024). SST anomaly and DHW products. | Ferrario, F. et al. (2014). The effectiveness of coral reefs for coastal hazard risk reduction. <i>Nature Communications</i>, 5. | Spalding, M. et al. (2017). Mapping the global value and distribution of coral reef tourism. <i>Marine Policy</i>, 82.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 08: Ocean SST Anomaly
# ═══════════════════════════════════════════════════════════════════
G["08"] = '''
<h2>Ocean Sea Surface Temperature Anomaly: The Warming Signal</h2>
<p class="tagline">The ocean absorbs 90% of the excess heat from greenhouse gases. Its temperature record is the most unambiguous evidence of planetary warming.</p>

<h3>What You Are Seeing</h3>
<p>A time series (1980 to 2024) of global mean sea surface temperature (SST) anomaly relative to a 1971-2000 baseline. The anomaly is the deviation from the long-term average for each month. Positive values (above zero) mean the ocean surface is warmer than the historical average. The trend line reveals the long-term warming signal, while the oscillations around it reflect interannual variability driven primarily by ENSO cycles.</p>

<h3>Reading the Signal and the Noise</h3>
<div class="hl">The <b>trend</b> (the upward-sloping curve) is the climate change signal: a steady increase of approximately 0.12 to 0.15 degrees Celsius per decade, driven by greenhouse gas accumulation. The <b>oscillations</b> around the trend are "noise" in the climate sense, but they are critically important for reefs. <b>Peaks</b> in the anomaly correspond to El Nino events (1998, 2010, 2015-2016, 2023-2024), which temporarily add 0.2 to 0.5 degrees Celsius on top of the warming trend. <b>Troughs</b> correspond to La Nina events, which temporarily cool the tropical Pacific. The critical observation is that <b>each successive El Nino peak occurs at a higher absolute temperature than the last</b>, because the background trend keeps rising. This ratchet effect means that events which caused recoverable bleaching in the 1990s now cause lethal bleaching in the 2020s.</div>

<h3>The Spatial Dimension of Ocean Warming</h3>
<div class="hl gold">Global mean SST obscures enormous <b>spatial heterogeneity</b>. The Arctic Ocean has warmed approximately 3 times faster than the global average (Arctic amplification). The Southern Ocean has warmed more slowly due to deep-water upwelling. The tropical Pacific shows a gradient: the eastern Pacific warms during El Nino and cools during La Nina, while the western Pacific shows a more steady warming trend. The <b>Indian Ocean</b> has warmed more uniformly and rapidly than other tropical oceans, which is why Indian Ocean reefs (Maldives, Chagos, East Africa) are among the most frequently bleached. The <b>North Atlantic</b> experienced a dramatic warming spike in 2023-2024 that exceeded all previous records by a wide margin, triggering alarm among oceanographers because it occurred during La Nina conditions that should have cooled the ocean. Whether this spike represents a regime shift or a transient anomaly is one of the most urgent questions in current climate science.</div>

<h3>Connection to Coral Bleaching Events</h3>
<p>The vertical dashed lines on this chart (if present) correspond to years when mass bleaching events were recorded globally. The correspondence between SST peaks and bleaching events is not perfect, because bleaching depends on <b>local</b> SST anomalies, not the global mean. However, the global mean serves as a proxy for overall thermal stress. The 2023-2024 period is particularly alarming: global SST anomalies reached unprecedented levels (+1.2 degrees Celsius above baseline in some months), and NOAA confirmed the fourth global mass bleaching event in April 2024, affecting reefs in at least 54 countries across all three ocean basins. The geographic scope of this event exceeded all previous episodes.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The <b>Paris Agreement target of 1.5 degrees Celsius</b> global warming is widely regarded as a reef survival threshold. At 1.5 degrees Celsius, models project 70 to 90% loss of tropical coral reefs. At 2.0 degrees Celsius, the loss exceeds 99%. Current national emissions pledges (NDCs), if fully implemented, put the world on a trajectory toward 2.5 to 3.0 degrees Celsius by 2100. The SST anomaly curve on this chart is, in a real sense, a countdown clock for coral reef ecosystems. The spatial implications are stark: the first reefs to be lost permanently will be those in the warmest, most stable tropical waters (equatorial Indian Ocean, Caribbean), while higher-latitude and upwelling-cooled reefs may persist longer as refugia. Conservation strategies must therefore be spatially prioritized, protecting the reefs most likely to survive the coming decades as seed sources for potential future recovery.</div>

<p class="ref"><b>Key references:</b> IPCC (2022). AR6 WGII Chapter 3: Oceans and Coastal Ecosystems. | Cheng, L. et al. (2024). Record-setting ocean warmth continued in 2023. <i>Advances in Atmospheric Sciences</i>. | NOAA CRW (2024). Fourth global coral bleaching event confirmed. | Hoegh-Guldberg, O. et al. (2018). Impacts of 1.5C warming on coral reefs. <i>Science</i>.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 09: Urbanization Choropleth
# ═══════════════════════════════════════════════════════════════════
G["09"] = '''
<h2>Urbanization: The Great Human Migration to Cities</h2>
<p class="tagline">For the first time in history, more than half of humanity lives in cities. This is the spatial story of that threshold crossing.</p>

<h3>What You Are Seeing</h3>
<p>An animated choropleth map showing the percentage of each country's population living in urban areas, from 1990 to 2023. Darker colors indicate higher urbanization. The animation reveals how the global urban frontier has expanded over three decades, with particularly dramatic shifts in East and South Asia and Sub-Saharan Africa.</p>

<h3>The Geography of Urbanization</h3>
<div class="hl">Urbanization follows a clear geographic gradient that reflects economic development stage. <b>High-income countries</b> (Western Europe, North America, Japan, Australia) are already 75 to 95% urban and show little change in the animation because their urban transitions were completed by the mid-20th century. <b>Middle-income countries</b> (China, Brazil, Turkey, Mexico) show the most dramatic darkening over the period, reflecting rapid industrialization-driven rural-to-urban migration. <b>Low-income countries</b> (much of Sub-Saharan Africa, parts of South Asia) remain relatively light but are beginning to darken, representing the early stages of what will be the largest urban transition in history: Africa's urban population is projected to triple from 600 million to 1.5 billion by 2050.</div>

<h3>Spatial Models of Urban Growth</h3>
<p>The patterns visible in this map correspond to well-established spatial models. <b>Zipf's Law</b> predicts that city sizes within a country follow a power-law distribution: the largest city is roughly twice the size of the second largest, three times the third, and so on. Countries undergoing rapid urbanization often violate Zipf's Law by developing a single <b>primate city</b> (e.g., Bangkok in Thailand, Lagos in Nigeria) that absorbs a disproportionate share of urban growth. <b>Central Place Theory</b> (Walter Christaller, 1933) predicts that cities will emerge at regular spatial intervals to serve surrounding hinterlands. In practice, urbanization in developing countries is driven as much by "push" factors (rural poverty, conflict, climate stress) as by "pull" factors (urban employment), producing spatial patterns that deviate significantly from theoretical models.</p>

<h3>The Urban Transition as a Spatial Transformation</h3>
<div class="hl gold">Urbanization is not just a demographic statistic; it is a <b>fundamental reorganization of human spatial relationships</b>. It concentrates human activity, waste production, energy consumption, and economic exchange into dense nodes, while simultaneously emptying rural landscapes. The ecological implications are profound: urban areas occupy approximately 3% of Earth's land surface but consume 75% of its resources and produce 70% of its carbon emissions. The <b>spatial footprint</b> of cities extends far beyond their boundaries through supply chains, commuter sheds, food production zones, and waste disposal networks. A city like Tokyo has an "ecological footprint" approximately 100 times its physical area. Understanding urbanization as a spatial phenomenon, not just a percentage, requires examining these extended networks of resource extraction and waste externalization that link urban cores to distant hinterlands.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The countries currently darkening on this map (Nigeria, India, Bangladesh, DRC, Ethiopia) face a critical policy window. Urban infrastructure built in the next two decades will lock in spatial patterns for a century. <b>Compact, transit-oriented urban growth</b> produces dramatically different outcomes from <b>sprawling, car-dependent growth</b>: lower carbon emissions per capita, lower infrastructure cost per person, better air quality, and stronger economic agglomeration effects. The spatial planning decisions being made today in Abuja, Dhaka, Addis Ababa, and Kinshasa will determine the carbon trajectory, livability, and economic productivity of cities that will house hundreds of millions of people. Historical evidence from East Asia (Singapore, Seoul, Tokyo) shows that strong public transit investment and density planning during the urban transition pays enormous dividends. Historical evidence from the US shows that suburban sprawl creates car dependency, social isolation, and infrastructure maintenance costs that strain public finances for decades.</div>

<p class="ref"><b>Key references:</b> UN-Habitat (2022). <i>World Cities Report</i>. | Christaller, W. (1933). <i>Central Places in Southern Germany</i>. Trans. Baskin, C. (1966). | Seto, K. et al. (2012). Global forecasts of urban expansion. <i>PNAS</i>, 109(40). | Angel, S. (2012). <i>Planet of Cities</i>. Lincoln Institute of Land Policy.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 10: Slum Population
# ═══════════════════════════════════════════════════════════════════
G["10"] = '''
<h2>Slum Population: The Shadow Side of Urbanization</h2>
<p class="tagline">A billion people live in informal settlements. This map shows where urbanization has outrun governance.</p>

<h3>What You Are Seeing</h3>
<p>A choropleth map showing the percentage of urban population living in slum conditions, as defined by UN-Habitat. A household qualifies as a "slum" if it lacks one or more of the following: <b>durable housing</b>, <b>sufficient living area</b> (not more than 3 persons per room), <b>access to improved water</b>, <b>access to improved sanitation</b>, and <b>security of tenure</b>. Countries range from near-zero (Europe, North America) to above 80% (Central African Republic, South Sudan).</p>

<h3>The Geography of Informality</h3>
<div class="hl">Slum prevalence follows a clear geographic pattern that overlaps with, but is not identical to, the poverty map. <b>Sub-Saharan Africa</b> has the highest slum prevalence (approximately 56% of urban residents, representing over 200 million people). <b>South Asia</b> has the largest absolute numbers (approximately 190 million). <b>Latin America</b>, despite higher overall income, still has approximately 21% slum prevalence, concentrated in <em>favelas</em> (Brazil), <em>barriadas</em> (Peru), and <em>villas miseria</em> (Argentina). The spatial distribution of slums is notable: they cluster on <b>marginal land</b> that the formal market does not value, including flood plains (Dhaka's riverside settlements), steep hillsides (Rio's favelas), garbage dumps (Cairo's Zabbaleen settlement), and land adjacent to railways, highways, and industrial zones. This location pattern reflects the intersection of poverty with land market dynamics: the poor settle on land that is either too dangerous, too polluted, or too legally ambiguous for formal development.</div>

<h3>Structural Drivers</h3>
<div class="hl gold">Slums emerge when three conditions coexist: <b>rapid urban population growth</b> (driven by rural-to-urban migration and natural increase), <b>insufficient public investment in housing and infrastructure</b>, and <b>dysfunctional land markets</b> (unclear tenure, prohibitive building codes, corruption in land allocation). The geographic pattern on this map correlates with all three. African and South Asian nations have the fastest urban growth rates, the lowest per-capita infrastructure investment, and the most complex land tenure systems (often a legacy of colonial land administration that created dual formal/informal tenure regimes). The paradox is that slum residents are often <em>more</em> economically productive per unit of capital than formal-sector workers (they build their own houses, create their own water systems, run their own businesses), but they are excluded from the formal economy's benefits (credit, legal protection, public services).</div>

<h3>Health and Environmental Justice</h3>
<p>Slum location on marginal land creates a <b>spatial health penalty</b>. Flood-prone settlements experience periodic waterborne disease outbreaks (cholera, typhoid) when floodwaters mix with open sewage. Hillside settlements are vulnerable to landslides (a 2017 landslide in Freetown, Sierra Leone, killed over 1,000 people in a slum settlement). Settlements near industrial zones suffer elevated rates of respiratory disease, lead poisoning, and cancer. This spatial concentration of health risks in poor communities constitutes an extreme form of <b>environmental injustice</b>: the communities with the least political power and economic resources bear the highest environmental and health burdens.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The dominant policy approaches to slums have shifted over decades. <b>1960s-1970s</b>: slum clearance and relocation (widely recognized as failed, destroying livelihoods and social networks). <b>1980s-1990s</b>: sites-and-services (providing serviced plots for self-built housing). <b>2000s-present</b>: <em>in-situ</em> upgrading (providing water, sanitation, electricity, and tenure security to existing settlements). The spatial dimension is critical: <b>tenure security</b>, which is a spatial-legal concept (the right to remain on a specific piece of land), is the most powerful single intervention. World Bank studies show that granting legal title to slum residents increases their investment in housing quality by 40 to 70% within three years, because people will not invest in improving a structure they fear losing. The geographic concentration of slums in specific countries means that solutions in India, Nigeria, and a handful of other nations could dramatically reduce the global slum population.</div>

<p class="ref"><b>Key references:</b> UN-Habitat (2022). <i>World Cities Report</i>. | Davis, M. (2006). <i>Planet of Slums</i>. Verso. | de Soto, H. (2000). <i>The Mystery of Capital</i>. Basic Books. | Field, E. (2005). Property rights and investment in urban slums. <i>Journal of the European Economic Association</i>, 3(2-3).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 11: Extreme Poverty
# ═══════════════════════════════════════════════════════════════════
G["11"] = '''
<h2>Extreme Poverty: The Shrinking Geography of Deprivation</h2>
<p class="tagline">In 1990, 36% of humanity lived in extreme poverty. By 2023, approximately 8.5%. But the geography of who remains is alarming.</p>

<h3>What You Are Seeing</h3>
<p>A choropleth showing the share of population living below the World Bank's international poverty line ($2.15/day in 2017 PPP), the threshold below which a person cannot reliably afford adequate calories, shelter, and basic necessities. The color gradient runs from green (low poverty) through yellow to deep red (above 50% in extreme poverty).</p>

<h3>The Geographic Concentration of Extreme Poverty</h3>
<div class="hl">The most important spatial fact about extreme poverty in the 2020s is its <b>geographic concentration</b>. In 1990, extreme poverty was distributed across East Asia (40% of China's population), South Asia (50% of India's), and Sub-Saharan Africa (56%). By 2023, East Asian extreme poverty had essentially been eliminated (China: below 0.5%). South Asian poverty had fallen dramatically (India: approximately 10 to 12%). But Sub-Saharan African poverty had fallen only modestly (from 56% to approximately 35%). As a result, Africa's share of the global extreme poor has risen from approximately 15% in 1990 to approximately 60% in 2023, even as the absolute number of poor people globally has fallen. The geography of extreme poverty is <b>Africanizing</b>.</div>

<h3>Why Africa's Poverty Persists: Spatial Explanations</h3>
<div class="hl gold">Several spatial and geographic factors contribute to the persistence of African poverty. <b>Landlocked geography</b>: 16 of Africa's 54 countries are landlocked, compared to 2 in South America and 0 in East/Southeast Asia. Landlocked countries face transport costs 50 to 100% higher than coastal nations, pricing them out of global trade. <b>Tropical disease burden</b>: malaria alone costs African economies an estimated 1.3% of GDP annually, and the geographic distribution of the Anopheles mosquito maps almost perfectly onto the extreme poverty map. <b>Fragmented political geography</b>: Africa has more international borders per unit of land area than any other continent, a legacy of the Berlin Conference of 1884-1885 that drew boundaries with no regard for ethnic, linguistic, or economic communities. These borders create barriers to trade, split ethnic groups across multiple jurisdictions, and generate border conflicts. <b>Arid and semi-arid zones</b>: the Sahel belt (Mauritania to Somalia) overlays extreme poverty with extreme climate vulnerability, creating a poverty-drought-conflict trap.</div>

<h3>The China Comparison</h3>
<p>China's poverty reduction, from approximately 750 million extremely poor people in 1990 to near-zero in 2023, is the largest and fastest in human history. It was driven by a specific spatial strategy: <b>Special Economic Zones (SEZs)</b> in coastal cities attracted foreign manufacturing investment, creating industrial jobs that absorbed surplus rural labor. The geographic structure of this strategy was deliberate: starting at the coast (Shenzhen, Xiamen, Zhuhai), then extending inland along river corridors and rail lines. This "coastal-first" model exploited China's geography (long coastline, major navigable rivers) in ways that landlocked, fragmented African nations cannot easily replicate. This does not mean Africa cannot reduce poverty, but it means that the spatial strategy must be different: regional integration, infrastructure corridors connecting landlocked areas to ports, and investment in agricultural productivity (since 60% of Africans work in agriculture, versus 25% of Chinese in 1990).</p>

<h3>Policy Implications</h3>
<div class="hl warn">The geographic concentration of extreme poverty in approximately 25 countries (mostly in Sub-Saharan Africa plus a few in South Asia) has a policy implication: <b>global poverty is no longer a global problem but a regional one requiring geographically specific solutions</b>. For Sahelian countries: drought-resilient agriculture, pastoralist support, conflict mediation. For Great Lakes region: post-conflict reconstruction, mineral governance (to prevent the "resource curse"), regional trade facilitation. For South Asian pockets: land reform, women's economic inclusion, social protection systems. The SDG goal of eliminating extreme poverty by 2030 will not be met globally, but it is achievable in most non-African regions. The remaining frontier is fundamentally a spatial challenge: reaching the most remote, conflict-affected, climate-vulnerable populations in the most difficult geographies on Earth.</div>

<p class="ref"><b>Key references:</b> World Bank (2023). <i>Poverty and Shared Prosperity</i>. | Ravallion, M. (2016). <i>The Economics of Poverty: History, Measurement, and Policy</i>. Oxford UP. | Collier, P. (2007). <i>The Bottom Billion</i>. Oxford UP. | Gallup, J., Sachs, J. & Mellinger, A. (1999). Geography and economic development. <i>International Regional Science Review</i>, 22(2).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 12: Gini Inequality
# ═══════════════════════════════════════════════════════════════════
G["12"] = '''
<h2>Gini Inequality: The Global Map of Unequal Societies</h2>
<p class="tagline">The Gini coefficient measures how unevenly a nation divides its income. This map reveals that geography shapes inequality as much as policy.</p>

<h3>What You Are Seeing</h3>
<p>A choropleth of the Gini coefficient for income or consumption inequality. The Gini ranges from <b>0</b> (perfect equality: everyone has the same income) to <b>1</b> (perfect inequality: one person has everything). In practice, national Gini values range from approximately 0.24 (Slovakia, Slovenia) to approximately 0.63 (South Africa). Colors range from green (low inequality) through yellow to deep red (high inequality).</p>

<h3>The Geographic Pattern</h3>
<div class="hl">Three distinct geographic zones of inequality emerge. <b>Low inequality (0.24 to 0.32)</b>: concentrated in Northern and Central Europe, particularly the Nordic countries and former Czechoslovakia/Yugoslavia. These nations share a common institutional heritage of strong welfare states, progressive taxation, and corporatist labor-market institutions. <b>Moderate inequality (0.33 to 0.44)</b>: most of Asia, North America, and North Africa. <b>High inequality (0.45 to 0.65)</b>: Latin America and Sub-Saharan Africa form a nearly contiguous band of high inequality stretching from Mexico through Brazil to South Africa, with a few outliers (Botswana, Namibia). This geographic clustering is not coincidental: it reflects shared historical legacies of <b>settler colonialism, plantation economies, and racial stratification</b> that created landed elites and landless masses in patterns that persist centuries later.</div>

<h3>The Latin American and African Inequality Belt</h3>
<div class="hl gold">The concentration of extreme inequality in Latin America and Southern Africa has deep historical-geographic roots. In both regions, colonial powers established <b>extractive economies</b> based on large-scale land grants to European settlers: <em>haciendas</em> and <em>latifundia</em> in Latin America, <em>farms</em> and <em>mines</em> in Southern Africa. These land distributions created a landed aristocracy and a landless peasantry whose descendants still show income differentials of 10:1 or more. In Latin America, the <b>Kuznets Curve</b> prediction (that inequality first rises and then falls with development) has largely held: inequality peaked in the 1990s and declined in the 2000s due to conditional cash transfer programs (Bolsa Familia in Brazil, Oportunidades in Mexico) and commodity-driven wage growth. In Sub-Saharan Africa, particularly South Africa (Gini 0.63), the legacy of apartheid created spatial inequality that is literally visible from satellite imagery: township housing adjacent to gated suburbs.</div>

<h3>Spatial Inequality Within Countries</h3>
<p>The Gini coefficient captures only <b>interpersonal</b> inequality, not <b>spatial</b> inequality (between regions within a country). Yet spatial inequality is often the more politically salient dimension. In India, per-capita income in Goa is approximately 7 times that of Bihar. In China, Shanghai's per-capita income is approximately 4 times that of Gansu. In the US, the ratio between the richest and poorest states (by median household income) is approximately 2:1, but the ratio between the richest and poorest counties is approximately 10:1. Spatial inequality within countries often maps onto ethnic, linguistic, and religious cleavages, making it politically explosive. The "Geography of Discontent" literature (Andres Rodriguez-Pose, 2018) has shown that regions within countries that are economically "left behind" are the same regions that vote for populist, anti-establishment parties.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The geographic clustering of inequality in former colonial economies suggests that <b>land reform</b> remains the single most impactful, and most politically difficult, structural intervention. Countries that carried out significant land reform (South Korea, Taiwan, Japan under US occupation) subsequently achieved both higher growth and lower inequality than their peers that did not. The spatial dimension of inequality also implies that <b>place-based policies</b> (investing in lagging regions) can be more effective than purely interpersonal transfers. The EU's Structural Funds, which channel resources to the poorest regions of Europe, have demonstrably reduced spatial inequality within Europe. Similar regional equalization mechanisms are lacking in most developing countries, where national capitals and coastal cities capture a disproportionate share of investment while interior regions stagnate.</div>

<p class="ref"><b>Key references:</b> Milanovic, B. (2016). <i>Global Inequality</i>. Harvard UP. | Piketty, T. (2014). <i>Capital in the Twenty-First Century</i>. Harvard UP. | Rodriguez-Pose, A. (2018). The revenge of the places that don't matter. <i>Cambridge Journal of Regions, Economy and Society</i>, 11(1). | Acemoglu, D., Johnson, S. & Robinson, J. (2001). The colonial origins of comparative development. <i>American Economic Review</i>, 91(5).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 13: Internet Penetration (animated)
# ═══════════════════════════════════════════════════════════════════
G["13"] = '''
<h2>Internet Penetration: The Digital Frontier's Geographic Advance</h2>
<p class="tagline">In 2000, fewer than 7% of humans had internet access. By 2023, 67%. This map shows how the digital revolution diffused across geography.</p>

<h3>What You Are Seeing</h3>
<p>An animated choropleth showing the percentage of each country's population using the internet, from approximately 2000 to 2023. The animation reveals a classic <b>spatial diffusion pattern</b>: beginning in dense clusters (North America, Scandinavia, East Asia) and radiating outward in waves.</p>

<h3>Spatial Diffusion Theory Applied to Digital Technology</h3>
<div class="hl">The spread of internet access follows Torsten Hagerstrand's (1953) <b>spatial diffusion model</b>. Hagerstrand identified three types of diffusion: <b>expansion diffusion</b> (spreading outward from an origin), <b>hierarchical diffusion</b> (spreading from large cities to smaller ones), and <b>contagious diffusion</b> (spreading to nearby locations). Internet adoption exhibits all three. It began in major cities of wealthy countries (hierarchical), then spread to smaller cities and suburbs within those countries (expansion), then jumped to major cities in developing countries (hierarchical again), and then spread outward to rural areas (contagious). The animation makes this nested diffusion visible: countries do not go from 0% to 100% uniformly. Instead, urban areas darken first, followed by peri-urban zones, with rural areas last.</div>

<h3>The Digital Divide as a Spatial Phenomenon</h3>
<div class="hl gold">The "digital divide" is fundamentally a spatial phenomenon with three dimensions. <b>Between countries</b>: in 2023, internet penetration in Iceland is 99% while in South Sudan it is approximately 8%. <b>Between urban and rural areas within countries</b>: even in India (overall penetration approximately 52%), urban penetration exceeds 80% while rural penetration is approximately 35%. <b>Between genders within geographies</b>: the ITU estimates that in Sub-Saharan Africa, women are 37% less likely to use the internet than men, a gap that is wider in rural areas. These three dimensions intersect: a rural woman in the DRC faces a triple penalty (poor country, rural location, female gender) that compounds to make her among the least connected humans on Earth. The geographic distribution of connectivity thus replicates and amplifies existing spatial inequalities.</div>

<h3>Infrastructure Geography: Why Some Places Connect Faster</h3>
<p>The physical infrastructure of the internet has its own geography. <b>Submarine fiber optic cables</b> follow trade routes, connecting major port cities across oceans. Countries with coastlines and proximity to major cable landing points (Lagos, Mombasa, Djibouti in Africa; Mumbai, Singapore, Hong Kong in Asia) gained broadband access earlier than landlocked nations. <b>Cell towers</b> follow population density and commercial viability: telecom companies invest where revenue potential exceeds infrastructure cost. This means that sparsely populated regions (the Sahel, Central Asian steppe, Amazonia) are the last to receive coverage. <b>Satellite internet</b> (LEO constellations like Starlink) promises to partially overcome this geographic constraint, but at price points that remain prohibitive for the poorest populations.</p>

<h3>Economic and Political Consequences of the Spatial Digital Divide</h3>
<div class="hl warn">The digital divide is not merely an access issue; it is an <b>economic productivity multiplier</b>. The World Bank estimates that a 10% increase in broadband penetration raises GDP growth by 1.2% in developing countries. This means that the geographic pattern of digital connectivity is actively widening economic gaps between connected and unconnected regions. Politically, internet access enables political mobilization and information access: the Arab Spring (2011), India's farmer protests (2020-2021), and numerous other movements relied on digital connectivity. Regions without access are effectively excluded from both digital economic participation and the information ecosystem that shapes modern governance. The geographic pattern of the digital divide thus has implications for political representation, economic opportunity, educational access, and social inclusion.</div>

<p class="ref"><b>Key references:</b> Hagerstrand, T. (1953). <i>Innovation Diffusion as a Spatial Process</i>. Trans. Pred, A. (1967). | ITU (2023). <i>Facts and Figures: The Path to Universal Connectivity</i>. | World Bank (2016). <i>World Development Report: Digital Dividends</i>. | Hilbert, M. (2016). The bad news is that the digital access divide is here to stay. <i>Telecommunications Policy</i>, 40(6).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 14: Electricity Access
# ═══════════════════════════════════════════════════════════════════
G["14"] = '''
<h2>Electricity Access: The Map of Light and Dark</h2>
<p class="tagline">675 million people still lack electricity. Their location on this map tells a story of geographic exclusion.</p>

<h3>What You Are Seeing</h3>
<p>A choropleth showing the percentage of population with access to electricity. Green indicates near-universal access (above 95%). Red indicates large unelectrified populations. The map's most striking feature is the concentration of darkness in Sub-Saharan Africa: approximately 43% of Africans lack electricity, compared to less than 3% in every other major region.</p>

<h3>The Geography of Energy Poverty</h3>
<div class="hl">The map of electricity access is an almost perfect inverse of the nighttime satellite image of Earth. The <b>NASA Black Marble</b> composite shows the planet lit up at night, with obvious bright patches (Europe, East Asia, eastern North America, India's Gangetic plain) and vast dark regions (Sub-Saharan Africa, interior Amazon, Central Asia). This spatial pattern of electrification reflects the economics of grid extension: connecting a household to the electricity grid costs $500 to $2,000 depending on distance from existing infrastructure. In densely populated areas (India, Bangladesh), the cost per household is low because the grid serves many customers per kilometer of line. In sparsely populated regions (much of Africa, where rural population density can be below 10 persons per square kilometer), grid extension is prohibitively expensive relative to expected revenue.</div>

<h3>The Grid vs Off-Grid Revolution</h3>
<div class="hl gold">The traditional model of electrification assumed that every country would replicate the European/American pattern: build large centralized power plants and extend the grid outward. This <b>spatial model</b> (hub-and-spoke grid architecture) worked in densely populated, industrializing economies but fails in the dispersed settlement patterns of rural Africa. The alternative, <b>off-grid solar</b> (solar home systems and mini-grids), represents a fundamentally different spatial model: distributed, modular, and matched to low-density settlement patterns. Since 2010, the cost of solar panels has dropped by 90%, making off-grid solar economically viable for rural Africa for the first time. The geographic suitability is also favorable: Africa has the world's highest average solar irradiance (5 to 7 kWh per square meter per day across most of the continent). The off-grid solar revolution is thus a case where <b>geographic disadvantage (low density, grid distance) can be partially compensated by a different geographic advantage (high solar resource)</b>.</div>

<h3>Electricity and the Development Cascade</h3>
<p>Electricity access is not just one development indicator among many; it is a <b>gateway capability</b> that enables virtually all other development. Without electricity: vaccines cannot be refrigerated, so child mortality remains high. Schools cannot function after dark, so educational attainment is limited. Businesses cannot operate machinery, so productivity stays low. Mobile phones cannot be charged, so digital inclusion is impossible. Water cannot be pumped, so women spend hours daily collecting water instead of participating in the economy. The geographic concentration of electricity poverty in Sub-Saharan Africa thus explains, in part, why this region lags on virtually every other development indicator: the absence of electricity is not a symptom but a <em>cause</em> of multidimensional deprivation.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The <b>SDG 7 target</b> (universal energy access by 2030) will not be met under current trajectories. Achieving it requires doubling the pace of electrification in Sub-Saharan Africa from approximately 15 million new connections per year to 30 million. The spatial strategy should be <b>dual-track</b>: grid extension for urban and peri-urban areas (where it remains the cheapest per-unit option) combined with off-grid solar and mini-grids for rural areas beyond the economic reach of the grid. The World Bank estimates the total investment required at $30 to $55 billion per year, roughly equivalent to the annual global subsidy for fossil fuels. The geographic targeting of this investment should prioritize countries with the largest unelectrified populations (Nigeria, DRC, Ethiopia, Tanzania, Uganda) and the rural regions within those countries where the development impact per connection is highest.</div>

<p class="ref"><b>Key references:</b> IEA (2023). <i>World Energy Outlook</i>: Energy access chapter. | Lighting Global/GOGLA (2023). Off-grid solar market report. | SE4All (2023). <i>Tracking SDG 7: The Energy Progress Report</i>. | Lee, K. et al. (2020). Electrification for "under grid" households in Africa. <i>World Development</i>, 128.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 15: Mobile Phone Subscriptions
# ═══════════════════════════════════════════════════════════════════
G["15"] = '''
<h2>Mobile Phone Subscriptions: The Most Rapid Technology Adoption in Human History</h2>
<p class="tagline">Mobile telephony went from zero to 8 billion subscriptions in 30 years, leapfrogging landline infrastructure entirely in much of the world.</p>

<h3>What You Are Seeing</h3>
<p>A choropleth showing mobile cellular subscriptions per 100 people. Values above 100 indicate that a country has more active SIM cards than people (due to multi-SIM usage, business lines, and data-only devices). Virtually the entire world is above 80 subscriptions per 100 people. The near-universality of this map, compared to the stark inequalities in internet or electricity maps, is the story itself.</p>

<h3>The Leapfrog: Geography as an Accelerant</h3>
<div class="hl">The mobile phone revolution is the most dramatic example of <b>technological leapfrogging</b> in economic history. In the developed world, communications infrastructure evolved sequentially: telegraph (1840s), telephone (1870s), landline networks (20th century), then mobile (1990s). Developing countries, especially in Sub-Saharan Africa, <em>skipped</em> the landline stage entirely. In 2000, Africa had fewer than 2 landlines per 100 people (the lowest teledensity on Earth). By 2023, it had over 80 mobile subscriptions per 100. The geographic reason landlines never penetrated Africa is the same reason that makes mobile attractive: <b>low population density and vast distances make fixed-line infrastructure prohibitively expensive</b>, while <b>cell tower coverage is relatively cheap per unit of area served</b>. A single cell tower can serve a 10 to 30 km radius, reaching scattered villages that would have required hundreds of kilometers of copper wire to connect by landline.</div>

<h3>Mobile Money: A Spatial Financial Revolution</h3>
<div class="hl gold">The most transformative spatial consequence of mobile adoption in the developing world is <b>mobile money</b>. M-Pesa, launched in Kenya in 2007, allowed users to send, receive, and store money via simple SMS-based interfaces on basic feature phones. By 2023, Sub-Saharan Africa had over 800 million registered mobile money accounts processing $700 billion in annual transactions. The spatial significance is profound: mobile money collapses geographic distance in financial transactions. A farmer in rural Uganda can receive payment from a buyer in Kampala instantly, without needing a bank branch (the nearest of which might be 50 km away). Remittances from urban migrants to rural families, which formerly required expensive and slow physical transfer, now flow digitally in seconds. Research by Tavneet Suri and William Jack (2016) found that M-Pesa lifted approximately 194,000 Kenyan households out of extreme poverty, primarily by enabling risk-sharing across geographic distance: when a household experienced a shock (illness, drought), distant relatives could send money immediately.</div>

<h3>From Voice to Data: The Emerging Divide</h3>
<p>While voice and basic SMS mobile coverage is now nearly universal, the next frontier, <b>mobile broadband (3G/4G/5G)</b>, reintroduces geographic inequality. 4G coverage in urban Africa exceeds 80%, but in rural Africa it drops below 30%. 5G is essentially non-existent outside major cities in wealthy nations. This creates a new spatial divide: "connected" (broadband-capable) vs "underconnected" (voice/SMS only). The applications that drive the next wave of economic and social transformation, including video-based education, telemedicine, e-commerce, and precision agriculture, all require broadband speeds that the basic mobile coverage visible on this map does not provide. The geography of mobile broadband availability will thus determine which populations can participate in the digital economy of the 2030s.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The mobile leapfrog suggests a broader lesson about development strategy: <b>geographic constraints that block one technology may be irrelevant for its successor</b>. Africa's low density blocked landlines but barely impeded mobile. Similarly, Africa's limited road network might be partially bypassed by drone delivery (already operational for medical supplies in Rwanda and Ghana). The policy implication is that developing countries should invest in the technologies appropriate to their geography rather than replicating infrastructure patterns from countries with fundamentally different spatial characteristics. For mobile broadband specifically: spectrum policy (allocating low-frequency bands for rural coverage), infrastructure sharing (allowing multiple operators to use the same towers), and Universal Service Funds (taxing profitable urban operations to subsidize rural expansion) are the key policy instruments for closing the remaining spatial gap.</div>

<p class="ref"><b>Key references:</b> Aker, J. & Mbiti, I. (2010). Mobile phones and economic development in Africa. <i>Journal of Economic Perspectives</i>, 24(3). | Suri, T. & Jack, W. (2016). The long-run poverty and gender impacts of mobile money. <i>Science</i>, 354(6317). | GSMA (2023). <i>The Mobile Economy: Sub-Saharan Africa</i>. | ITU (2023). <i>Measuring Digital Development</i>.</p>
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

print(f"\nPhase 1: Injected deep guides into {count} charts")
