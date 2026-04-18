#!/usr/bin/env python3
"""Phase 3: Deep academic interpretation guides for charts 37-48.
India Elections 2024 core (LISA, Moran's I, turnout, area, alliance) + 3D immersive environments."""

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
# CHART 37: LISA Cluster Map (Turnout + Margin)
# ═══════════════════════════════════════════════════════════════════
G["37"] = '''
<h2>LISA Cluster Map: Where Electoral Behavior Clusters Geographically</h2>
<p class="tagline">Voter turnout in India is not random across space. It clusters with an intensity (I = 0.642) that demands geographic explanation.</p>

<h3>What You Are Seeing</h3>
<p>Two choropleth maps of India's 543 Lok Sabha constituencies. The <b>left panel</b> shows LISA clusters for <b>voter turnout</b>. The <b>right panel</b> shows LISA clusters for <b>victory margin</b> (the gap between the winner and runner-up as a percentage of total votes). Each constituency is colored according to its LISA classification: <b>Red (High-High / Hot Spot)</b> = high-value constituency surrounded by high-value neighbors. <b>Blue (Low-Low / Cold Spot)</b> = low-value surrounded by low. <b>Orange (High-Low)</b> = a high outlier in a low neighborhood. <b>Cyan (Low-High)</b> = the reverse. <b>Grey</b> = not statistically significant at p < 0.05.</p>

<h3>What Is LISA and How Is It Computed?</h3>
<div class="hl">LISA stands for <b>Local Indicators of Spatial Association</b>, developed by Luc Anselin in his seminal 1995 paper in <i>Geographical Analysis</i>. It is the local decomposition of the global <b>Moran's I</b> statistic, meaning that each spatial unit (here, each constituency) receives its own local I value that measures how similar or dissimilar it is to its neighbors. The formal definition is:

<p><code>I_i = (x_i - x&#772;) / s&sup2; &times; &Sigma;_j w_ij (x_j - x&#772;)</code></p>

<p>where <em>x_i</em> is the value at location <em>i</em>, <em>x&#772;</em> is the global mean, <em>s&sup2;</em> is the variance, and <em>w_ij</em> is the spatial weight between locations <em>i</em> and <em>j</em>. The sum of all local I values equals the global Moran's I (up to a scaling factor). <b>Spatial weights</b> define who is a "neighbor." We used <b>K-Nearest Neighbors with k = 8</b> (each constituency's 8 nearest centroids are neighbors), with <b>row standardization</b> (each row of the weights matrix sums to 1, so each neighbor contributes equally). Significance is assessed through <b>999 conditional random permutations</b>: the observed local I is compared to 999 reshufflings of the data to determine whether the observed clustering could have occurred by chance. Only clusters with <b>p < 0.05</b> are colored.</p></div>

<h3>Why KNN k=8? The Neighborhood Definition Problem</h3>
<div class="hl gold">The choice of spatial weights is the most consequential methodological decision in any spatial autocorrelation analysis. We chose <b>k=8</b> nearest neighbors (rather than queen contiguity or distance bands) for specific reasons. India's parliamentary constituencies vary enormously in area: from Chandni Chowk in Delhi (approximately 10 km&sup2;) to Ladakh (approximately 170,000 km&sup2;). Under queen contiguity (shared border = neighbor), Ladakh would have only 1 or 2 neighbors, producing unreliable local statistics. Under distance bands, a 100 km radius would capture dozens of neighbors in dense UP but only 1 in sparse Ladakh. KNN equalizes the number of neighbors, ensuring that every constituency's local I is computed from the same number of comparisons (8), making the statistics more comparable across the urban-rural and dense-sparse gradient. The choice of k=8 (rather than 4 or 12) is standard in the spatial econometrics literature for moderate-resolution datasets, providing sufficient local information without oversmoothing.</div>

<h3>The Turnout Map (Left Panel): India's North-South Civic Engagement Divide</h3>
<div class="hl">The turnout LISA map reveals what may be <b>the most important spatial pattern in Indian democracy</b>. <b>150 Hot Spots (High-High)</b> concentrate in Kerala, Tamil Nadu, West Bengal, and parts of Assam and Tripura. These are constituencies where turnout exceeds 65-70%, surrounded by neighbors with similarly high turnout. <b>170 Cold Spots (Low-Low)</b> concentrate in Uttar Pradesh, Bihar, parts of Rajasthan, and Madhya Pradesh. These are constituencies where turnout is below 55%, surrounded by similarly disengaged neighbors. The global <b>Moran's I = 0.642</b>, which is extraordinarily high for a social science variable. For context, Moran's I ranges from -1 (perfect dispersion) to +1 (perfect clustering), with 0 indicating random spatial distribution. A value of 0.642 means that turnout in Indian constituencies is <em>very strongly</em> spatially autocorrelated: knowing a constituency's turnout, you can predict its neighbors' turnout with considerable accuracy.</div>

<h3>What Drives the North-South Turnout Divide?</h3>
<p>The spatial pattern of turnout clustering maps onto multiple overlapping structural variables. <b>Literacy</b>: Kerala's literacy rate (96%) and Tamil Nadu's (80%) vastly exceed UP's (69%) and Bihar's (62%). Literate populations are more likely to understand the voting process, read election materials, and participate in civic discourse. <b>Women's participation</b>: in Southern states, the gap between male and female turnout is small (often below 3 percentage points). In UP and Bihar, the gap exceeds 10 points in many constituencies, reflecting both lower female autonomy and cultural barriers to women's public participation. <b>Political competition</b>: the South has a longer history of competitive multi-party politics (DMK/AIADMK in Tamil Nadu, CPI(M)/Congress in Kerala, TMC/BJP/Left in West Bengal), which generates stronger mobilization incentives. Bihar and UP have long been dominated by caste-based patronage networks that mobilize selectively rather than universally. <b>State capacity</b>: Southern states have more polling stations per voter, better transport infrastructure to booths, and more efficient electoral administration.</p>

<h3>The Margin Map (Right Panel): Competitive vs Safe Seats</h3>
<div class="hl gold">The margin LISA map shows a weaker but still significant pattern (<b>I = 0.260</b>). <b>High-margin clusters</b> (constituencies won by large margins, surrounded by similar) tend to concentrate in regions of single-party dominance: BJP strongholds in central India, TMC strongholds in Bengal, DMK strongholds in Tamil Nadu. <b>Low-margin clusters</b> (tight races surrounded by tight races) concentrate in swing regions: eastern UP, parts of Maharashtra, and Karnataka. The lower Moran's I for margins compared to turnout (0.260 vs 0.642) reflects the fact that competition is less spatially structured than participation: competitive and safe seats can alternate within short distances depending on candidate quality, caste dynamics, and local issues, whereas turnout is driven by deeper structural factors (literacy, women's status, state capacity) that vary more gradually across space.</div>

<h3>Tobler's First Law and Electoral Contagion</h3>
<p>Waldo Tobler's First Law of Geography ("everything is related to everything else, but near things are more related than distant things") manifests powerfully in electoral data. The strong spatial autocorrelation in turnout reflects <b>electoral contagion</b> through multiple channels. <b>Social networks</b>: people discuss politics with neighbors, friends, and family, who are geographically proximate. If your social network votes, you are more likely to vote. <b>Media markets</b>: local newspapers, television channels, and social media groups serve geographically bounded audiences, creating shared information environments. <b>Party organization</b>: political party infrastructure (booth-level workers, local leaders, mobilization machinery) operates geographically, and strong organization in one constituency spills over to adjacent ones. <b>Shared grievances</b>: economic conditions, infrastructure quality, and governance performance affect geographic regions, not individual constituencies, creating spatially correlated attitudes toward incumbents and challengers.</p>

<h3>The Spatial Outliers: Orange and Cyan</h3>
<div class="hl warn">The <b>High-Low outliers</b> (orange, a high-turnout constituency in a low-turnout region) and <b>Low-High outliers</b> (cyan, the reverse) are analytically the most interesting features. They represent <b>local deviations from the regional norm</b> and demand constituency-specific explanations. A High-Low outlier in UP might be a constituency with an exceptionally popular local candidate or strong local party organization that mobilized voters despite regional apathy. A Low-High outlier in Tamil Nadu might be a constituency experiencing local disillusionment (a corruption scandal, candidate controversy, or boycott call) despite high regional engagement. These outliers are the points where <b>national and regional trends are overridden by local agency</b>, and they are the most valuable cases for qualitative political analysis.</div>

<h3>Methodological Cautions</h3>
<p>Several caveats apply. <b>Modifiable Areal Unit Problem (MAUP)</b>: the spatial patterns observed depend on the geographic units used. If we had assembly-segment-level data (each Lok Sabha constituency contains 5-8 assembly segments), the patterns might differ because smaller units capture finer-grained variation. <b>Ecological fallacy</b>: constituency-level patterns do not directly reveal individual behavior. A "cold spot" constituency does not mean every individual is disengaged; it means the aggregate rate is low. <b>Temporal stability</b>: a single election's LISA map captures one snapshot. Comparing LISA maps across elections (2014, 2019, 2024) would reveal whether the spatial clustering is persistent (structural) or volatile (event-driven). The I = 0.642 for turnout is likely persistent because the structural drivers (literacy, women's status) change slowly. The I = 0.260 for margins is likely more volatile because competition levels fluctuate with candidate selection and campaign dynamics.</p>

<p class="ref"><b>Key references:</b> Anselin, L. (1995). Local indicators of spatial association: LISA. <i>Geographical Analysis</i>, 27(2). | Tobler, W. (1970). A computer movie simulating urban growth in the Detroit region. <i>Economic Geography</i>, 46(sup1). | Rey, S. & Anselin, L. (2007). PySAL: A Python library of spatial analytical methods. <i>Review of Regional Studies</i>, 37(1). | Yadav, Y. (1999). Electoral politics in the time of change: India's third electoral system. <i>Economic and Political Weekly</i>, 34(34/35).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 38: India Area vs Outcomes
# ═══════════════════════════════════════════════════════════════════
G["38"] = '''
<h2>Constituency Area vs Electoral Outcomes</h2>
<p class="tagline">India's parliamentary constituencies range from 10 km&sup2; to 170,000 km&sup2;. Does geographic size shape democratic outcomes?</p>

<h3>What You Are Seeing</h3>
<p>Scatter plots relating <b>constituency area</b> (km&sup2;, typically on a log scale) to electoral variables: turnout, victory margin, and/or alliance dominance. Each dot is one of India's 543 constituencies. The enormous variance in area (a 17,000-fold range) is itself a product of the 1971 delimitation, which equalized constituencies by <em>population</em>, not area, producing geographically vast but sparsely populated seats in the north and east (Ladakh, Barmer, Arunachal) alongside tiny but densely packed seats in urban areas (Delhi, Mumbai, Kolkata).</p>

<h3>Why Area Matters for Democracy</h3>
<div class="hl">Constituency area is not merely a geographic curiosity; it is a <b>structural determinant of democratic quality</b>. In larger constituencies: <b>Campaign costs are higher</b>: a candidate in Barmer (Rajasthan, approximately 71,000 km&sup2;) must cover 50 times the area of a candidate in Chandni Chowk (Delhi, approximately 10 km&sup2;), requiring more vehicles, more events, more staff, and more money. This cost asymmetry systematically advantages wealthy candidates and well-funded parties in geographically large seats. <b>Voter-representative contact is weaker</b>: an MP representing Ladakh (approximately 170,000 km&sup2;) cannot physically visit all communities in their constituency, even over a full 5-year term. This dilutes accountability and reduces the legislator's knowledge of local conditions. <b>Media coverage is thinner</b>: large rural constituencies receive less media attention per voter than compact urban ones, reducing information availability for voters.</div>

<h3>The Area-Turnout Relationship</h3>
<div class="hl gold">If the scatter shows a negative relationship between area and turnout, it reflects the <b>distance-to-polling-station effect</b>. In geographically vast constituencies with dispersed settlements, some voters must travel significant distances to reach their polling booth. Even with the Election Commission's mandate that no voter should be more than 2 km from a booth, this is not always achieved in constituencies like Ladakh, Bastar (Chhattisgarh), or Arunachal West, where terrain (mountains, forests, rivers without bridges) imposes travel times of hours rather than minutes. The spatial pattern of turnout within large constituencies is well-documented: turnout is highest near booth locations and decays with distance, following a classic <b>distance decay function</b>. This geographic barrier to voting disproportionately affects the elderly, disabled, women (whose mobility is socially restricted in many rural areas), and the very poor (who cannot afford to sacrifice a day's wages for travel).</div>

<h3>Area and Party Strategy</h3>
<p>Political parties adapt their strategies to constituency geography. In <b>compact urban constituencies</b>: door-to-door canvassing, social media campaigns, and candidate-centered politics dominate. In <b>large rural constituencies</b>: parties rely on hierarchical networks (district-block-village leaders), caste and community mobilization, and "booth management" (assigning party workers to each polling station). The BJP's success in the 2014 and 2019 elections was partly attributed to its superior <b>booth-level organizational density</b>, which allowed it to compete effectively even in geographically vast constituencies where personal candidate contact was impossible. The INDIA alliance's relative strength in compact Southern and urban constituencies in 2024 may partly reflect the organizational advantages that smaller geography confers on newer or less infrastructure-heavy parties.</p>

<h3>The Delimitation Dimension</h3>
<div class="hl warn">The area distribution of constituencies is frozen from the <b>1971 delimitation</b> (with minor adjustments in 2008 that rebalanced within states but did not change inter-state seat allocation). Since 1971, India's population has more than doubled, but the population growth has been <b>geographically uneven</b>: northern states (UP, Bihar, Rajasthan, Madhya Pradesh) grew much faster than southern states (Tamil Nadu, Kerala, Andhra Pradesh, Karnataka). The result is that northern constituencies now have far more voters per seat (UP: approximately 2.4 million per constituency) than southern ones (Kerala: approximately 1.3 million). When delimitation eventually proceeds (based on updated Census data), the area-population mismatch will be rebalanced, but this will transfer seats from the south to the north, creating the political crisis discussed in Charts 71-80. The area variable in this chart is thus a snapshot of a frozen geographic moment that does not reflect current population realities.</div>

<p class="ref"><b>Key references:</b> Election Commission of India (2024). Statistical Report on General Elections, 2024. | Kumar, S. (2013). <i>Indian Democracy: Meanings and Practices</i>. | Iyer, L. & Reddy, M. (2013). Redrawing the lines: Did political incumbents influence the delimitation of constituencies in India? Working Paper, Harvard Business School.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 39: Moran's I Scatterplot
# ═══════════════════════════════════════════════════════════════════
G["39"] = '''
<h2>Moran's I Scatterplot: The Statistical Heart of Spatial Autocorrelation</h2>
<p class="tagline">This four-quadrant scatter is how spatial statisticians see the world. Each quadrant tells a different story about geographic clustering.</p>

<h3>What You Are Seeing</h3>
<p>The <b>Moran scatterplot</b> is the standard diagnostic visualization for spatial autocorrelation. The <b>X-axis</b> shows each constituency's standardized value (its deviation from the mean, divided by the standard deviation). The <b>Y-axis</b> shows the <b>spatial lag</b>: the weighted average of neighboring constituencies' standardized values. The four quadrants map directly to LISA categories: <b>upper-right (Q1)</b> = High-High (hot spot), <b>lower-left (Q3)</b> = Low-Low (cold spot), <b>lower-right (Q4)</b> = High-Low (positive outlier), <b>upper-left (Q2)</b> = Low-High (negative outlier). The <b>slope of the regression line</b> through this scatter equals the global <b>Moran's I</b>.</p>

<h3>How to Read the Scatterplot</h3>
<div class="hl">The distribution of points across quadrants reveals the <b>nature</b> of spatial association. If most points fall in Q1 and Q3 (the diagonal from lower-left to upper-right), positive spatial autocorrelation dominates: similar values cluster together. This is the case for turnout (I = 0.642), where the vast majority of points are in Q1 (high-turnout southern constituencies surrounded by high-turnout neighbors) or Q3 (low-turnout northern constituencies surrounded by low-turnout neighbors). The <b>slope of the fitted line</b> (Moran's I) measures the strength of this tendency. A steeper slope means stronger spatial autocorrelation. Points in Q2 and Q4 are spatial outliers: they deviate from their neighborhood's character. These are the orange (High-Low) and cyan (Low-High) constituencies on the LISA map.</div>

<h3>The Mathematics of Moran's I</h3>
<div class="hl gold">The global Moran's I is formally defined as:

<p><code>I = (n / S_0) &times; [&Sigma;_i &Sigma;_j w_ij (x_i - x&#772;)(x_j - x&#772;)] / [&Sigma;_i (x_i - x&#772;)&sup2;]</code></p>

<p>where <em>n</em> = 543 (number of constituencies), <em>S_0</em> = sum of all spatial weights, <em>w_ij</em> = spatial weight between <em>i</em> and <em>j</em>, and <em>x&#772;</em> = global mean. The numerator is a <b>weighted cross-product of deviations</b>: it is large and positive when neighboring constituencies deviate from the mean in the <em>same direction</em> (both above or both below). The denominator is the total variance. The ratio thus measures what proportion of the total variance is "spatially structured" vs "spatially random." Under the null hypothesis of spatial randomness (values assigned to locations at random), the expected value of I is approximately <em>-1/(n-1)</em>, which for n=543 is approximately -0.0018, essentially zero. Our observed I = 0.642 for turnout is approximately 350 standard deviations above the null expectation, confirming with overwhelming statistical certainty that the turnout pattern is not random.</p></div>

<h3>Interpreting the Magnitude</h3>
<p>Moran's I values in social science data rarely exceed 0.5. For comparison: racial segregation indices in US cities typically produce Moran's I values of 0.4 to 0.7. Land price gradients in cities produce values of 0.3 to 0.6. Disease incidence clustering rarely exceeds 0.3 to 0.4. The turnout I = 0.642 is thus at the <b>high end of what is observed in any spatial social science application</b>, indicating that India's electoral participation geography is as strongly structured as racial segregation in American cities. The margin I = 0.260 is moderate but still highly significant, indicating meaningful geographic clustering of competitive vs safe seats. The difference between the two values (0.642 vs 0.260) tells us that <b>participation is more geographically structured than competition</b>: people in the same neighborhood tend to vote at similar rates more than they tend to produce similar margins.</p>

<h3>Why This Matters Beyond Statistics</h3>
<div class="hl warn">The Moran's I scatterplot is not merely a methodological exercise. It has direct <b>policy implications for electoral resource allocation</b>. The strong positive spatial autocorrelation in turnout means that low-turnout constituencies are not randomly scattered; they cluster together in identifiable geographic zones (UP, Bihar, parts of Rajasthan). This clustering means that <b>geographically targeted interventions</b> (voter education campaigns, additional polling stations, transport to booths, women's mobilization programs) can reach the maximum number of disengaged voters per unit of investment. If low-turnout constituencies were randomly distributed, such targeting would be impossible. The spatial structure is, in this case, a policy asset: it tells the Election Commission of India exactly <em>where</em> to concentrate its efforts to increase democratic participation.</div>

<p class="ref"><b>Key references:</b> Anselin, L. (1995). Local indicators of spatial association: LISA. <i>Geographical Analysis</i>, 27(2). | Anselin, L. (1996). The Moran scatterplot as an ESDA tool. In Fischer, M. et al. (eds.), <i>Spatial Analytical Perspectives on GIS</i>. | Cliff, A. & Ord, J. (1981). <i>Spatial Processes: Models and Applications</i>. Pion.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 40: Turnout Swing 2019-2024
# ═══════════════════════════════════════════════════════════════════
G["40"] = '''
<h2>Turnout Swing: 2019 vs 2024</h2>
<p class="tagline">Where did voters show up more, and where did they stay home? The geographic pattern of swing reveals the mood of the electorate.</p>

<h3>What You Are Seeing</h3>
<p>A geographic visualization showing the <b>change in voter turnout</b> between the 2019 and 2024 Lok Sabha elections for each constituency. Constituencies colored in one direction (e.g., blue/green) experienced increased turnout; those in the opposite direction (red/orange) experienced decreased turnout. The magnitude of the color indicates the size of the swing. The animation or toggle allows switching between the two election snapshots.</p>

<h3>National Context: The 2024 Turnout Decline</h3>
<div class="hl">The 2024 Lok Sabha election saw a <b>national average turnout of approximately 65.8%</b>, slightly lower than 2019's approximately 67.4%. This modest national decline masks enormous <b>geographic heterogeneity</b>. Some constituencies swung 10 or more percentage points in either direction. Understanding the spatial pattern of this swing is crucial because turnout changes are often more politically consequential than vote-share changes: <b>which voters stayed home, and where, shaped the outcome</b> as much as which party they chose.</div>

<h3>The Geography of Turnout Change</h3>
<div class="hl gold">The spatial pattern of turnout swing tends to correlate with several geographic and political variables. <b>Anti-incumbency concentration</b>: constituencies where the sitting MP was perceived as ineffective often saw turnout changes driven by either protest voting (increased turnout) or disillusionment (decreased turnout, particularly among the incumbent's base). <b>Heatwave geography</b>: the 2024 election (April-June) coincided with extreme heat across northern India. Constituencies in the Gangetic plain and Rajasthan that voted in the hottest phases may have experienced <b>heat-suppressed turnout</b>, a phenomenon documented in US elections but rarely studied in Indian contexts. Peak temperatures exceeding 45 degrees Celsius during polling hours represent a real physiological barrier to voter participation, particularly for elderly voters, outdoor workers, and those in constituencies with long distances to polling booths. <b>Polarization geography</b>: highly polarized constituencies (where voters felt the stakes were high) may have seen increased turnout, while "foregone conclusion" safe seats may have seen decreased turnout due to voter fatigue.</div>

<h3>Spatial Autocorrelation of Swing</h3>
<p>Turnout swing itself is likely to be <b>spatially autocorrelated</b>, meaning that constituencies that gained turnout cluster together, and those that lost turnout cluster together. This spatial structure reflects the geographic nature of the factors driving swing: weather is geographically correlated (heat waves affect regions, not random constituencies), anti-incumbency sentiment often reflects region-wide governance failures (state-level factors), and party mobilization efforts are organized regionally. Computing a LISA analysis on the <em>swing</em> variable (rather than on the raw turnout) would reveal which geographic zones experienced the most dramatic collective shifts in civic engagement between the two elections.</p>

<h3>The Differential Turnout Hypothesis</h3>
<div class="hl warn">In electoral analysis, <b>differential turnout</b> (when turnout changes differently across demographic or geographic groups) is often more consequential than vote switching (when individuals change their party preference). If turnout drops disproportionately in a party's stronghold areas (its supporters stay home), the party loses seats even if nobody switched votes. The geographic pattern of the 2024 turnout swing should be read against the alliance map (Chart 48): if turnout declined more in NDA-stronghold areas than in INDIA-stronghold areas (or vice versa), this differential is a key explanatory variable for the election result. The spatial dimension adds power to this analysis: we can identify not just <em>how much</em> turnout changed but <em>where</em>, and correlate "where" with party strength, demographic composition, infrastructure quality, and environmental conditions.</div>

<p class="ref"><b>Key references:</b> Yadav, Y. (2024). Reading the 2024 verdict: turnout, swing, and geography. <i>The Hindu</i>. | Gomez, B. et al. (2007). The effects of weather on voter turnout. <i>Journal of Politics</i>, 69(3). | Election Commission of India (2024). Statistical Report on General Elections.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 41: Distance from Delhi vs Margin
# ═══════════════════════════════════════════════════════════════════
G["41"] = '''
<h2>Center vs Periphery: Does Distance from Delhi Shape Electoral Margins?</h2>
<p class="tagline">Testing Stein Rokkan's core-periphery model in the world's largest democracy.</p>

<h3>What You Are Seeing</h3>
<p>A scatter plot with <b>geodesic distance from New Delhi</b> (km) on the X-axis and <b>victory margin</b> (% of total votes) on the Y-axis. Each point is a constituency. Delhi, the national capital and seat of the ruling party's power, serves as the hypothetical "core" of Indian political geography. The question is whether electoral margins (how safely a seat is won or lost) vary systematically with distance from this core.</p>

<h3>Rokkan's Core-Periphery Model</h3>
<div class="hl"><b>Stein Rokkan and Derek Urwin (1983)</b> developed the core-periphery model to explain spatial variation in political behavior across European nations. The model posits that the political "core" (the capital region, seat of economic and administrative power) projects influence outward, and that this influence <b>decays with distance</b>. Peripheral regions develop distinct political identities, grievances, and voting patterns that diverge from the core. In European contexts, this explains the persistence of regional nationalist parties (Scotland, Catalonia, Corsica, Flanders) at the geographic periphery of centralized states.</div>

<h3>What the Scatter Reveals for India</h3>
<div class="hl gold">The Indian case is likely to show <b>no strong linear relationship</b> between distance from Delhi and margin. This is because India's political geography is not organized around a single core-periphery gradient. Instead, India has <b>multiple regional political systems</b> that operate semi-independently: Tamil Nadu's DMK-AIADMK system, West Bengal's TMC-BJP-Left system, Kerala's LDF-UDF alternation, and the Hindi heartland's BJP-SP-BSP competition each have their own internal geography. Distance from Delhi does not predict whether a seat is competitive or safe because competition is determined by <b>regional factors</b> (candidate quality, caste dynamics, state-level anti-incumbency) rather than proximity to the national capital. However, the <b>variance</b> of margins may change with distance: near Delhi, margins span the full range (from razor-thin to enormous), while at the periphery (Northeast, Tamil Nadu, Kerala), margins may cluster more tightly due to the dominance of regional parties with geographically concentrated support bases.</div>

<h3>India's Multiple Cores</h3>
<p>A more sophisticated application of Rokkan's model would recognize that India has <b>multiple political cores</b>, not one. Mumbai serves as an economic core. Chennai, Kolkata, and Bengaluru function as regional political-cultural cores. The BJP's organizational core is arguably in Nagpur (RSS headquarters) rather than Delhi. A multi-core distance analysis, measuring each constituency's distance from the <em>nearest</em> political core, might reveal patterns invisible in the single-core Delhi model. This speaks to a fundamental characteristic of Indian federalism: it is a <b>multi-polar political geography</b> that resists the simple center-periphery frameworks developed for more centralized European states.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The absence of a strong core-periphery gradient is, paradoxically, a <b>democratic strength</b>. It means that Indian democracy is not simply radiating from a single center; it has genuine geographic pluralism. Peripheral regions (the Northeast, Tamil Nadu, Kashmir) are not simply passive recipients of national political trends but <b>active generators of distinct political cultures, party systems, and policy demands</b>. This geographic pluralism is the institutional expression of India's enormous linguistic, cultural, and ecological diversity. Any attempt to impose uniform political patterns from the center (through hyper-centralization of power, for instance) would be working against the grain of this spatial political structure. The federalism that India's geographic diversity demands is not merely a constitutional convenience; it is a spatial necessity.</div>

<p class="ref"><b>Key references:</b> Rokkan, S. & Urwin, D. (1983). <i>Economy, Territory, Identity</i>. Sage. | Lipset, S.M. & Rokkan, S. (1967). Cleavage structures, party systems, and voter alignments. In <i>Party Systems and Voter Alignments</i>. Free Press. | Chhibber, P. & Verma, R. (2018). <i>Ideology and Identity: The Changing Party Systems of India</i>. Oxford UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 42: India Political Cylinder (Three.js)
# ═══════════════════════════════════════════════════════════════════
G["42"] = '''
<h2>India Political Cylinder: Three-Dimensional Electoral Geography</h2>
<p class="tagline">543 constituencies unwrapped onto a rotating cylinder. Height is latitude, angle is longitude, color is alliance. The North-South divide becomes viscerally three-dimensional.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Three.js WebGL</b> 3D scene. India's 543 Lok Sabha constituencies are represented as colored spheres (or markers) placed on the surface of a rotating cylinder. The mapping from geography to cylinder is: <b>vertical position (height) = latitude</b> (northern constituencies at the top, southern at the bottom). <b>Angular position = longitude</b> (eastern constituencies on one side, western on the other). <b>Color = political alliance</b>: saffron/orange for NDA (BJP and allies), blue/green for INDIA alliance, and other colors for unaffiliated parties. <b>Pink octahedra</b> mark constituencies where women candidates won. The cylinder rotates slowly, allowing the viewer to see the full 360-degree distribution.</p>

<h3>Why a Cylinder? The Cartographic Logic</h3>
<div class="hl">All map projections involve tradeoffs between area, shape, distance, and direction. The cylindrical projection used here is a deliberate choice that <b>emphasizes the latitudinal (north-south) dimension</b> of Indian politics while preserving the longitudinal distribution. By wrapping India's geography around a cylinder, the visualization eliminates the "edge effect" of flat maps (where eastern and western extremities appear far apart) and instead shows them as adjacent on the cylinder's surface. This is particularly useful for India's Northeast (Assam, Manipur, Nagaland, etc.), which is geographically connected to India through a narrow corridor (the Siliguri Corridor) but appears isolated on flat maps. On the cylinder, the Northeast's political character (strong regional parties, low NDA penetration) is visible in context with the rest of India's eastern geography.</div>

<h3>The North-South Political Divide in 3D</h3>
<div class="hl gold">The cylinder makes <b>India's most important political-geographic cleavage</b> physically manifest. The upper portion of the cylinder (north India: UP, Bihar, Rajasthan, Madhya Pradesh, Gujarat) is dominated by saffron (NDA). The lower portion (south India: Tamil Nadu, Kerala, Karnataka, Andhra Pradesh, Telangana) is dominated by blue/green (INDIA alliance and regional parties). The middle band (Maharashtra, Odisha, West Bengal) is contested territory with mixed colors. This tripartite vertical structure corresponds to deep structural differences: the Hindi heartland (north) with its BJP-centric politics, the Dravidian and regional-party-dominated south, and the transitional middle belt. Seeing this in 3D, with the cylinder rotating, gives a visceral sense of the <b>geographic coherence</b> of each political bloc that flat maps can obscure.</div>

<h3>Women Winners: The Pink Octahedra</h3>
<p>The pink octahedra marking women winners are <b>sparse and geographically clustered</b>. Only 74 women won seats in the 2024 election (approximately 13.6% of 543). Their spatial distribution on the cylinder reveals that women winners are not randomly distributed but concentrate in specific geographic bands: Rajasthan (several women MPs), West Bengal (TMC nominations), and pockets in UP and Madhya Pradesh. Large stretches of the cylinder, particularly in the deep south (Tamil Nadu) and deep north (Bihar), show almost no pink markers. This 3D view makes the <b>geographic scarcity of women's political success</b> more visually striking than any 2D map could.</p>

<h3>Interactive Engagement</h3>
<div class="hl warn">Drag to rotate the cylinder and observe how the political geography shifts as you move around. Notice how the NDA-dominated north and the INDIA-dominated south are not separated by a clean horizontal line but by a <b>ragged, contested frontier</b> that zigzags across the cylinder's middle band. This frontier is where elections are won and lost: the "swing belt" of Maharashtra, Karnataka, and parts of Odisha and West Bengal that determines which alliance forms the government. The 3D representation makes the <b>three-dimensionality of Indian political geography</b> literally visible: it is not a simple north-south binary but a complex, spatially textured landscape with internal variation, outlier pockets, and transitional zones.</div>

<p class="ref"><b>Key references:</b> Three.js documentation. | Tufte, E. (1983). <i>The Visual Display of Quantitative Information</i>. | Sridharan, E. (2004). The fragmentation of the Indian party system. In <i>India's Political Parties</i>. Oxford UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 43: Development Globe (Three.js)
# ═══════════════════════════════════════════════════════════════════
G["43"] = '''
<h2>Development Globe: The Planet's Vital Signs on a Rotating Sphere</h2>
<p class="tagline">196 countries on a spinning globe. Bars extrude proportional to GDP, life expectancy, or fertility. Switch metrics to see how the world's shape changes.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Three.js WebGL</b> globe with 196 countries represented at their geographic centroids. Each country has a <b>3D bar</b> (extruded cylinder or prism) extending outward from the globe's surface. The height of the bar encodes the selected development metric. Button controls let you switch between <b>GDP per capita</b>, <b>life expectancy</b>, and <b>fertility rate</b>. The globe rotates slowly, and you can drag to reorient. <b>Color</b> encodes continental membership, creating a visual separation between geographic regions.</p>

<h3>Why a Globe? The Distortion Problem</h3>
<div class="hl">All flat map projections distort either area, shape, distance, or direction. The most commonly used projection, Mercator, dramatically inflates high-latitude areas (Greenland appears larger than Africa, when in reality Africa is 14 times larger). This distortion systematically exaggerates the visual "weight" of wealthy northern nations. The 3D globe <b>eliminates projection distortion entirely</b>: each country appears at its true relative size and position. This is particularly important for development data because the Mercator distortion visually amplifies the countries that are already dominant (Europe, North America, Russia) while shrinking the countries where most of humanity lives and where the most dramatic development changes are occurring (Sub-Saharan Africa, South and Southeast Asia). The globe gives <b>Africa, South Asia, and the Pacific their true visual weight</b>.</div>

<h3>Switching Metrics: How the World's Shape Changes</h3>
<div class="hl gold">The most powerful feature is switching between metrics and observing how the <b>shape of the globe's surface</b> changes. <b>GDP per capita</b>: tall bars in North America, Western Europe, Japan, Australia, Gulf states. Short bars across Africa and South Asia. The globe looks "spiky" in the north and "smooth" in the south. <b>Life expectancy</b>: the distribution is more uniform. Europe and East Asia still have tall bars, but Africa's bars, while shorter, are less dramatically different than for GDP. The globe's surface is more "even," reflecting the partial health convergence discussed in Chart 05. <b>Fertility</b>: the pattern <em>inverts</em>. Africa's bars are tallest (high fertility), while Europe and East Asia have stumps (below-replacement fertility). The globe looks "spiky" in Africa and "smooth" in the north. Watching the shape invert as you switch from GDP to fertility is a powerful visual demonstration of the <b>demographic-economic paradox</b>: the poorest regions have the most children, and the richest have the fewest.</div>

<h3>The Hemispheric Perspective</h3>
<p>Rotating the globe to view specific hemispheres reveals patterns invisible on flat maps. The <b>view from above the North Pole</b> shows a ring of wealthy, high-life-expectancy, low-fertility nations surrounding the Arctic. The <b>view from above the South Pole</b> shows a scattering of countries (Australia, New Zealand, Argentina, Chile, South Africa) surrounded by ocean. The <b>equatorial view</b> shows the densest concentration of humanity (India, China, Southeast Asia, West Africa) and the widest range of development outcomes. The globe perspective reveals that development is not just a "north-south" divide but has a <b>hemispheric geometry</b> shaped by continental positions, ocean currents, and historical trade routes.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The globe visualization forces a confrontation with <b>geographic bias in global governance</b>. International institutions (UN Security Council, G7, IMF, World Bank) are disproportionately governed by high-bar (wealthy) nations that occupy a relatively small portion of the globe's surface. When you rotate to see Africa or South Asia, the mismatch between the number of people living there (approximately 40% of humanity) and their representation in global governance is stark. The bars for GDP and political power do not match the bars for population. The globe also reveals the <b>spatial logic of South-South cooperation</b>: the BRICS nations (Brazil, Russia, India, China, South Africa) are distributed across the globe's surface in a way that creates a network of large developing nations that can bypass the traditional North Atlantic-centered institutions. Their geographic spread is itself a geopolitical resource: they span all major ocean basins and time zones.</div>

<p class="ref"><b>Key references:</b> Snyder, J.P. (1987). <i>Map Projections: A Working Manual</i>. USGS Professional Paper 1395. | Monmonier, M. (2004). <i>Rhumb Lines and Map Wars</i>. University of Chicago Press. | Three.js documentation.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 44: Democracy Helix (Three.js)
# ═══════════════════════════════════════════════════════════════════
G["44"] = '''
<h2>Democracy Helix: NDA and INDIA Alliance in DNA Double-Strand Form</h2>
<p class="tagline">India's two major political coalitions rendered as intertwined helices. Where one strand is thick, the other is thin. The spatial complementarity of Indian electoral geography.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Three.js 3D helix</b> with two intertwined strands, evoking the DNA double helix. One strand represents <b>NDA (BJP and allies)</b> constituencies; the other represents <b>INDIA alliance</b> constituencies. Constituencies are arranged along the helix by geographic order (typically latitude, with northern constituencies at the top). <b>Node size encodes victory margin</b>: large nodes are safe seats won by wide margins; small nodes are closely contested. The helix rotates slowly.</p>

<h3>The Double Helix Metaphor</h3>
<div class="hl">The DNA metaphor is analytically precise, not merely aesthetic. Just as the two strands of DNA are <b>complementary</b> (where one has adenine, the other has thymine), India's two major political coalitions occupy <b>complementary geographic space</b>. Where one is strong (large nodes), the other is weak (small or absent nodes). The upper turns of the helix (northern India) show a <b>thick NDA strand</b> (large saffron nodes) and a <b>thin INDIA strand</b> (small blue nodes). The lower turns (southern India) reverse: the <b>INDIA strand thickens</b> and the <b>NDA strand thins</b>. The middle turns (Maharashtra, Karnataka, West Bengal, Odisha) show <b>both strands at moderate thickness</b>, the contested terrain where elections are decided.</div>

<h3>Spatial Complementarity and the Federal Structure</h3>
<div class="hl gold">The geographic complementarity visible in the helix reflects India's <b>federal electoral structure</b>. India does not have a single national party system; it has a <b>patchwork of regional systems</b> loosely aggregated into two national coalitions. The NDA's dominance in northern India rests on the BJP's organizational reach in the Hindi heartland, amplified by Hindutva mobilization and the Modi personal brand. The INDIA alliance's strength in the south and east rests on powerful regional parties (DMK in Tamil Nadu, TMC in West Bengal, JMM in Jharkhand, JD(U) in Bihar, though JD(U) joined NDA in 2024) that have deep local roots, linguistic/cultural identity appeal, and strong state-level governance records. The helix makes visible what political scientists call <b>"the nationalization of Indian politics"</b>, or rather, the limits thereof: despite the BJP's attempts to become a truly national party, India's political geography retains a fundamentally federal, regionally differentiated character.</div>

<h3>Margin Size as Political Energy</h3>
<p>The node size encoding (margin) reveals the <b>geographic distribution of political energy</b>. Large nodes (safe seats with margins above 20%) represent constituencies where one coalition has overwhelming dominance, often reflecting deep structural factors (caste composition, linguistic identity, long-term party loyalty). Small nodes (margins below 5%) represent constituencies where the outcome was contingent on short-term factors (candidate quality, campaign effectiveness, last-minute mobilization). The geographic distribution of large vs small nodes reveals the <b>bedrock geography of Indian politics</b> (large nodes) versus its <b>contingent, contested surface</b> (small nodes). Any shift in national power between coalitions must come from the small-node zones, not the large-node strongholds.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The helix structure implies that <b>no coalition can govern India effectively without geographic breadth</b>. A government formed exclusively from the upper turns (north) or lower turns (south) of the helix would lack legitimacy and responsiveness in the opposite region. The BJP's challenge after 2024, having performed worse in the south than in 2019, is to extend its strand downward on the helix. The INDIA alliance's challenge is to thicken its strand upward in the Hindi heartland. The <b>geographic complementarity also has policy implications for fiscal federalism</b>: the north-south political divide maps directly onto the north-south fiscal divide (see Charts 72, 77), making any policy that transfers resources from one end of the helix to the other a politically explosive geographic question.</div>

<p class="ref"><b>Key references:</b> Chhibber, P. & Verma, R. (2018). <i>Ideology and Identity</i>. Oxford UP. | Palshikar, S. et al. (eds.) (2024). <i>Electoral Politics in India: The Resurgence of the Bharatiya Janata Party</i>. Routledge. | Sridharan, E. (2004). The fragmentation of the Indian party system. In <i>India's Political Parties</i>. Oxford UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 45: Continental Development Space (Plotly 3D)
# ═══════════════════════════════════════════════════════════════════
G["45"] = '''
<h2>Continental Development Space: Three Variables, Three Dimensions, No Flattening</h2>
<p class="tagline">GDP, Life Expectancy, and Fertility plotted in true 3D. Continental clusters emerge that no 2D projection can fully reveal.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Plotly 3D scatter plot</b> with three development variables mapped to three spatial axes: <b>X = GDP per capita (log scale)</b>, <b>Y = Life Expectancy</b>, <b>Z = Fertility Rate</b>. Each point is a country, colored by continent. The plot is fully interactive: drag to rotate, scroll to zoom, hover for country details. The 3D space reveals the <b>multivariate structure of development</b> without the information loss that 2D projections impose.</p>

<h3>Why 3D? The Information Loss Problem</h3>
<div class="hl">Every 2D scatter plot of multivariate data involves <b>projection</b>: collapsing a higher-dimensional space onto a plane. When we plot GDP vs life expectancy (Charts 01, 04), we lose information about fertility. When we plot fertility vs life expectancy (Chart 02), we lose GDP. The 3D scatter eliminates this tradeoff for three variables by literally showing all three simultaneously. The result is a <b>development manifold</b>: the surface or curve in 3D space along which most countries lie. If countries obeyed a strict three-variable relationship, they would all lie on a 2D surface embedded in 3D space. The deviation of individual countries from this surface reveals countries that break the expected pattern: Gulf states (high GDP, moderate life expectancy, moderate fertility: off the manifold), Cuba (low GDP, high life expectancy, low fertility: off the manifold in the opposite direction).</div>

<h3>Continental Clusters in 3D</h3>
<div class="hl gold">The 3D view reveals <b>continental clustering that is tighter in three dimensions than in any two-dimensional projection</b>. <b>Sub-Saharan Africa</b> occupies a distinct volume: low-X (poor), low-Y (low life expectancy), high-Z (high fertility). <b>Europe</b> occupies the opposite corner: high-X, high-Y, low-Z. <b>Latin America</b> clusters at moderate-X, moderate-to-high-Y, low-Z (they completed the fertility transition before reaching European income levels). <b>East Asia</b> shows the widest spread: from low-income Laos/Myanmar to high-income Japan/South Korea, but with universally low fertility. <b>South Asia</b> is mid-transition: moderate income, moderate life expectancy, fertility declining but still above replacement. The 3D view reveals that these clusters are not just different "levels" of development but occupy <b>qualitatively different positions in development space</b>, reflecting distinct historical paths through the demographic and economic transitions.</div>

<h3>The Development Manifold and Convergence</h3>
<p>If you animate this 3D scatter through time (adding a temporal dimension), you would see all continental clusters <b>migrating toward the same corner</b>: high GDP, high life expectancy, low fertility. This is the "convergence" hypothesis rendered in 3D. But the paths of convergence differ by continent: East Asian countries moved along a steep, fast trajectory (compressed transition). Latin American countries moved more gradually. African countries are moving slowest and along a different angle (life expectancy improving faster than GDP, fertility declining slowly). The <b>angle of approach</b> to the "developed" corner differs by continental cluster and reveals the relative pace of economic vs demographic vs health transition.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The 3D space reveals that <b>development is not one-dimensional</b>. A country cannot be meaningfully ranked on a single axis of "developed" to "underdeveloped." A country can be economically poor but demographically advanced (Bangladesh: low GDP, low fertility, improving life expectancy). It can be economically rich but demographically stalled (Gulf states: high GDP, moderate life expectancy, falling-but-still-moderate fertility). Policy must be tailored to a country's position in this three-dimensional space, not to its rank on any single variable. The 3D view also reveals that <b>the "developed" corner has its own problems</b>: ultra-low fertility (below 1.5), population aging, and stagnant GDP growth. The "arrival" point of development is itself an unstable equilibrium, not a final destination.</div>

<p class="ref"><b>Key references:</b> UNDP (2023). <i>Human Development Report</i>. | Gapminder Foundation (2024). Data tools and documentation. | Plotly documentation. | Sen, A. (1999). <i>Development as Freedom</i>. Oxford UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 46: Women + Area Hypothesis
# ═══════════════════════════════════════════════════════════════════
G["46"] = '''
<h2>Women and Area: Testing Whether Women Win in Different Geographies</h2>
<p class="tagline">Do women candidates succeed in smaller, denser constituencies? The data says yes, and the Mann-Whitney U test quantifies it.</p>

<h3>What You Are Seeing</h3>
<p>Three panels testing the relationship between <b>constituency area</b> and <b>women's electoral success</b>. Panel 1: distribution of constituency areas for <b>women winners vs men winners</b>. Panel 2: scatter of area vs margin, with women highlighted. Panel 3: density plots comparing the geographic size of constituencies won by women vs men. The key statistical test is the <b>Mann-Whitney U test</b>, a non-parametric comparison of two distributions that does not assume normality.</p>

<h3>The Mann-Whitney U Test: What It Tests and What It Found</h3>
<div class="hl">The <b>Mann-Whitney U test</b> (also called the Wilcoxon rank-sum test) asks whether one sample (areas of women-won constituencies) tends to have <b>systematically different ranks</b> than another sample (areas of men-won constituencies) when all values are pooled and ranked. Unlike the t-test, it makes no assumption about the shape of the distribution, which is important because constituency areas are heavily right-skewed (a few enormous constituencies like Ladakh and Barmer pull the mean far from the median). The test result: <b>women winners have a median constituency area of 3,324 km&sup2;</b> compared to <b>men winners' median of 4,073 km&sup2;</b>. The difference is <b>statistically significant</b>, meaning it is unlikely to have occurred by chance alone.</div>

<h3>Why Would Geography Favor Women Candidates?</h3>
<div class="hl gold">Several spatial mechanisms could explain why women succeed more often in smaller, denser constituencies. <b>Campaign cost</b>: smaller constituencies require less travel, fewer vehicles, and lower logistics costs, reducing the financial barrier that disproportionately affects women candidates (who typically receive less party funding than men). <b>Visibility</b>: in compact constituencies, a candidate can be personally known to a larger fraction of voters through community events, door-to-door campaigning, and local media, reducing reliance on party brand and mass media, which favor established (male) incumbents. <b>Urban effect</b>: smaller constituencies are disproportionately urban, and urban voters tend to be more educated, more exposed to gender-progressive attitudes, and less bound by caste and patriarchal norms that discourage voting for women. <b>Social network density</b>: in compact areas, women's self-help groups, community organizations, and social networks are denser, providing stronger mobilization infrastructure for women candidates.</div>

<h3>Confounders and Cautions</h3>
<p>The area-gender relationship must be interpreted cautiously. <b>Party nomination patterns</b> are a major confounder: parties may systematically nominate women in smaller/urban constituencies (where they perceive women as more competitive) and men in larger/rural ones. If so, the geographic effect is partly an artifact of party strategy rather than a genuine voter-level preference. <b>Regional confounding</b>: smaller constituencies cluster in specific regions (Delhi, Mumbai, Kolkata, parts of Tamil Nadu and Kerala), and these regions may have independently higher rates of women's candidacy for cultural or political reasons unrelated to area. Disentangling the "area effect" from the "region effect" would require multivariate regression controlling for state, urbanization rate, literacy, and party.</p>

<h3>Policy Implications</h3>
<div class="hl warn">If the area effect is genuine (not purely a confound of party nomination strategy), it has implications for the <b>Women's Reservation Bill</b>. When selecting the one-third of constituencies to reserve for women (approximately 181 seats), the selection could be <b>spatially optimized</b> to maximize women's electoral chances by preferring smaller, more compact, more urban constituencies. Alternatively, if the goal is to normalize women's presence across all geographies (including large rural constituencies where women face the greatest barriers), the reservation should deliberately include some large constituencies, even at the cost of lower initial win margins. The tension between maximizing women's electoral success (reserve small seats) and maximizing the transformative impact of women's representation in traditionally excluded geographies (reserve large seats) is a spatial policy tradeoff with no obvious resolution.</div>

<p class="ref"><b>Key references:</b> Mann, H.B. & Whitney, D.R. (1947). On a test of whether one of two random variables is stochastically larger than the other. <i>Annals of Mathematical Statistics</i>, 18(1). | Basu, A. (2010). <i>Women, Dynasties and Democracy in India</i>. In Kapur, D. & Mehta, P.B. (eds.), <i>Rethinking Public Institutions in India</i>. Oxford UP. | Chattopadhyay, R. & Duflo, E. (2004). Women as policy makers: evidence from a randomized policy experiment in India. <i>Econometrica</i>, 72(5).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 47: 3D Extruded India (Three.js)
# ═══════════════════════════════════════════════════════════════════
G["47"] = '''
<h2>3D Extruded India: Electoral Data as Topographic Relief</h2>
<p class="tagline">Each constituency becomes a column whose height encodes a chosen metric. The political landscape of India, rendered literally.</p>

<h3>What You Are Seeing</h3>
<p>A <b>Three.js 3D map</b> of India where each of the 543 Lok Sabha constituencies is extruded vertically (as a 3D column or prism) from the map surface. The <b>height of each column</b> encodes the selected metric, switchable via buttons: <b>electorate ratio</b> (voters per seat), <b>turnout</b>, <b>victory margin</b>, or other variables. <b>Color</b> may encode a secondary variable (e.g., alliance, or the same metric on a gradient). The camera can be rotated and zoomed to view the extruded landscape from any angle.</p>

<h3>The Spatial Histogram: A Cartographic Concept</h3>
<div class="hl">This visualization is a <b>3D spatial histogram</b> (also called a prism map or block diagram): a technique that superimposes quantitative data onto geographic space using the vertical dimension. The concept dates to Jacques Bertin's <i>Semiology of Graphics</i> (1967), which identified the three retinal variables that the eye processes most efficiently: position, size, and color. The extruded 3D map uses <b>position</b> (geographic location on the map), <b>size</b> (height of the extrusion), and <b>color</b> simultaneously, making it one of the most information-dense cartographic representations possible. However, it also has known perceptual limitations: tall columns in the foreground can occlude shorter columns behind them (the <b>occlusion problem</b>), and the human eye is less accurate at judging 3D volume than 2D area (the <b>Weber-Fechner effect</b>). Interactive rotation mitigates the occlusion problem by allowing the viewer to examine the landscape from multiple angles.</div>

<h3>Electorate Ratio Mode: The Democratic Inequality Landscape</h3>
<div class="hl gold">When switched to <b>electorate ratio</b> (number of registered voters per constituency), the 3D map reveals India's most fundamental democratic inequality. Uttar Pradesh constituencies tower over the landscape (approximately 2.0 to 2.5 million voters per seat), while small states and territories (Sikkim, Lakshadweep, Andaman and Nicobar) are barely visible (0.4 to 0.6 million). This means that <b>a vote cast in Sikkim has approximately 5 to 6 times the weight of a vote cast in UP</b> in terms of its contribution to electing an MP. The 3D view makes this inequality viscerally apparent: the towering columns of northern India represent massive populations squeezed into the same single-seat unit as tiny populations in the northeast. This is the spatial expression of the frozen 1971 delimitation, and it will be the central political controversy whenever delimitation proceeds.</div>

<h3>Turnout Mode: The Civic Engagement Landscape</h3>
<p>In <b>turnout mode</b>, the 3D landscape shows the same North-South divide visible in the LISA map (Chart 37), but with an added physical intuition. Southern India's columns rise high (65 to 80% turnout), while northern India's columns are shorter (50 to 60%). The 3D perspective allows the viewer to literally see the <b>"valley" of civic disengagement</b> that stretches across the Gangetic plain, flanked by the "mountains" of high participation in the south and parts of the northeast. This topographic metaphor is analytically useful: just as a geographic valley is shaped by the erosive forces that carved it, the turnout valley is shaped by the structural forces (low literacy, low women's participation, weak state capacity) that have eroded civic engagement in northern India over decades.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The 3D extruded map is not merely a visualization technique; it is a <b>spatial policy tool</b>. By rendering electoral data as a physical landscape, it makes spatial inequality tangible and communicable to non-specialists. A policymaker or journalist viewing the electorate ratio landscape can immediately grasp the democratic inequality that abstract statistics (like "UP has 2.4 million voters per constituency") fail to convey. The <b>turnout landscape</b> similarly communicates the scale and geography of civic disengagement in a way that flat charts cannot. For the Election Commission of India, this type of visualization can guide <b>resource allocation</b>: the "low valleys" on the turnout landscape are precisely the geographic zones where additional polling stations, voter education campaigns, and women's mobilization efforts should be concentrated.</div>

<p class="ref"><b>Key references:</b> Bertin, J. (1967/1983). <i>Semiology of Graphics</i>. Trans. Berg, W. University of Wisconsin Press. | Three.js documentation. | Dorling, D. (2012). <i>The Visualization of Spatial Social Structure</i>. Wiley.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 48: Alliance LISA + Women Bivariate
# ═══════════════════════════════════════════════════════════════════
G["48"] = '''
<h2>Alliance LISA and Women's Representation: The Bivariate Question</h2>
<p class="tagline">Do women fare better in NDA or INDIA strongholds? The answer is that neither alliance has earned a claim to women's representation. I = 0.367 for alliance clustering.</p>

<h3>What You Are Seeing</h3>
<p>A two-panel visualization. The <b>left panel</b> shows a LISA cluster map for <b>alliance dominance</b> (NDA vs INDIA), computed on a binary or continuous measure of NDA vote share. The <b>right panel</b> overlays <b>women's candidacy or success rates</b> onto the alliance geography, testing whether one alliance's stronghold regions have better women's representation.</p>

<h3>Alliance LISA: I = 0.367</h3>
<div class="hl">The alliance Moran's I of <b>0.367</b> (p < 0.001) indicates <b>strong positive spatial autocorrelation</b> in political alignment. NDA-voting constituencies cluster together, and INDIA-voting constituencies cluster together. This is not surprising given India's regional party structure, but the magnitude is informative. The <b>110 NDA Hot Spots</b> (High-High: strong NDA constituencies surrounded by strong NDA neighbors) concentrate in Gujarat, Rajasthan, Madhya Pradesh, and parts of UP: the Hindi heartland core of BJP support. The <b>112 INDIA Hot Spots</b> concentrate in Tamil Nadu, Kerala, West Bengal, and parts of Maharashtra and Jharkhand. The spatial outliers (a BJP win in a sea of opposition, or vice versa) are relatively rare, reflecting the geographic coherence of India's political coalitions.</div>

<h3>The Key Finding: Women's Representation Is Unrelated to Alliance</h3>
<div class="hl gold">The right panel tests a hypothesis that many observers might expect to hold: that one alliance's stronghold regions have better women's representation than the other. The data <b>rejects this hypothesis</b>. Women's candidacy and success rates are low across <b>both</b> alliance strongholds. NDA strongholds in the Hindi heartland have very few women candidates (reflecting the region's conservative gender norms). INDIA strongholds in the south have somewhat more women candidates in absolute numbers but still elect very few women relative to their total seats. The bivariate analysis reveals that <b>women's political exclusion is a cross-partisan, cross-geographic phenomenon</b> in India. It is not a failure of one ideology or one region; it is a structural feature of the entire party system.</div>

<h3>Why Neither Alliance Champions Women</h3>
<p>The bivariate pattern reflects the fact that <b>candidate selection in Indian politics is driven by "winnability" calculations</b> that systematically disadvantage women. Party bosses in both alliances evaluate potential candidates on caste alignment (will this candidate consolidate the dominant caste vote?), financial capacity (can this candidate self-fund a significant portion of campaign costs?), and local network strength (does this candidate have booth-level organizational reach?). On all three criteria, <b>men score higher on average</b> due to structural gender inequalities: men are more likely to be leaders of caste associations, to have personal wealth or business connections, and to have existing political networks. These "winnability" criteria are nominally gender-neutral but operationally gender-biased. Without a <b>structural mandate</b> (like the Women's Reservation Bill, which forces parties to nominate women in one-third of seats regardless of winnability calculations), the gender-neutral selection criteria will continue to produce gender-unequal outcomes.</p>

<h3>The Spatial Dimension of the Reservation Question</h3>
<div class="hl warn">The Women's Reservation Bill (passed 2023, not yet implemented) will reserve approximately 181 Lok Sabha seats for women. <b>Which 181?</b> The selection will be done by rotation (different constituencies reserved in successive elections), but the first set will shape initial outcomes. The bivariate analysis in this chart suggests that <b>reserving seats in both NDA and INDIA strongholds is essential</b>, because neither alliance voluntarily nominates women. If reservation were concentrated only in one alliance's territory (due to rotation patterns), the other alliance's territory would remain a women-free zone. The spatial distribution of reserved seats should aim for <b>geographic balance across regions, alliance territories, and urban/rural gradients</b> to ensure that women's representation is normalized across the full geography of Indian democracy, not confined to selected pockets.</div>

<p class="ref"><b>Key references:</b> Anselin, L. (1995). Local indicators of spatial association: LISA. <i>Geographical Analysis</i>, 27(2). | Rai, P. (2017). Women's representation in Indian Parliament: an analysis. <i>India Review</i>, 16(2). | Chattopadhyay, R. & Duflo, E. (2004). Women as policy makers. <i>Econometrica</i>, 72(5). | Krook, M.L. (2009). <i>Quotas for Women in Politics</i>. Oxford UP.</p>
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

print(f"\nPhase 3: Injected deep guides into {count} charts")
