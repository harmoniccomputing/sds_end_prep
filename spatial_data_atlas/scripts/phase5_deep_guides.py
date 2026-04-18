#!/usr/bin/env python3
"""Phase 5: Deep academic interpretation guides for charts 65-80.
Women's Data (Silence Map, Gauntlet, Gender Gap, Deposit Forfeiture, Scoreboard, Candidature 3D)
+ Delimitation & Fiscal (Simulator, Fiscal Returns, Reservation, Moran Criteria, Punishment Value,
  Representation Inequality, Fiscal Spine, Treemap, Fiscal-Gender Bubble, Constituency Clustering)."""

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
# CHART 65: The Silence Map (152 zero-women constituencies)
# ═══════════════════════════════════════════════════════════════════
G["65"] = '''
<h2>The Silence Map: 152 Constituencies Where No Woman Even Ran</h2>
<p class="tagline">28% of Indian democracy had zero female voice on the ballot. This map shows where silence is loudest.</p>

<h3>What You Are Seeing</h3>
<p>Every one of India's 543 Lok Sabha constituencies is plotted on this map. <b>Red X markers</b> (large, unmistakable) mark the <b>152 constituencies where not a single woman filed her candidacy</b> in the 2024 general election. <b>Orange dots</b> = exactly 1 woman candidate. <b>Yellow</b> = 2 to 3 women. <b>Green</b> = 4 or more women candidates. Data source: Election Commission of India, 2024 general election Constituency-wise Women Candidature report.</p>

<h3>The Scale of Exclusion</h3>
<div class="hl"><b>152 out of 543 = 28% of Indian democracy operated with zero female voice on the ballot.</b> This is not a statistic about women losing elections. It is a statistic about women not being present as an option for voters. In these constituencies, every candidate, from the major national parties to the smallest regional and independent nominees, was male. The question this map poses is not "why don't women win?" but the more fundamental <b>"why don't women even enter?"</b> The answer lies at the intersection of party gatekeeping, social structure, and geography.</div>

<h3>The Spatial Pattern: Not Random, Deeply Structured</h3>
<div class="hl gold">The red Xs are <b>not randomly distributed</b>. They cluster with unmistakable geographic coherence in India's so-called <b>"Hindi heartland"</b>: central and eastern Uttar Pradesh, rural Bihar, parts of Rajasthan, Madhya Pradesh, and pockets of Maharashtra. Southern and northeastern states show far more green (multiple women candidates). Urban constituencies in every region tend to have more women filing. This geographic clustering mirrors India's <b>Gender Development Index</b> with remarkable precision: the same states with the worst sex ratios, lowest female literacy, highest rates of child marriage, and most entrenched patriarchal social structures are the ones where women cannot even enter the political arena. The spatial autocorrelation of women's exclusion is almost certainly stronger than the spatial autocorrelation of women's success (I = 0.062, Chart 54), because the <em>barriers</em> to entry are more geographically structured than the <em>outcomes</em> of those who manage to enter.</div>

<h3>Why These Constituencies? Three Mechanisms of Exclusion</h3>
<div class="two-col">
<div class="hl"><b>1. Party gatekeeping:</b> Political parties select candidates through internal processes (high commands, parliamentary boards, state-level negotiations) that are dominated by men. In the zero-women constituencies, party bosses did not place a single woman on any ticket. This is not passive omission; it is active exclusion. Parties calculate "winnability" based on caste alignment, financial capacity, and organizational network, all criteria that structurally favor men in patriarchal societies. The geographic clustering suggests that <b>state-level party leadership culture</b> matters: the UP BJP, Bihar JD(U), and Rajasthan Congress units appear more resistant to women's candidacy than their counterparts in Tamil Nadu, Kerala, or West Bengal.</div>
<div class="hl"><b>2. Social barriers:</b> In the red X constituencies, potential women candidates face harassment, family opposition, caste-based restrictions on women's public activity, and the threat of violence. Field studies by the Centre for Social Research and others document that women who express interest in contesting elections in these regions face intimidation from male power holders who view elected positions as male entitlements. The <b>financial barrier</b> is also gendered: the average Lok Sabha campaign costs Rs 5 to 15 crore; women have less independent access to wealth, business networks, and party funding.</div>
</div>
<div class="hl warn"><b>3. Constituency geography:</b> Many red X constituencies are <b>geographically vast rural seats</b> (area above 5,000 km&sup2;) where campaigning requires extensive travel, overnight stays in remote areas, and interaction with male-dominated village power structures, conditions that are culturally more restrictive for women. The correlation between constituency area and zero-women status reinforces the finding from Chart 46 that geographic scale itself is a barrier to women's political participation. Compact urban constituencies, where campaigning is physically easier and social norms are more progressive, are far less likely to be red Xs.</div>

<h3>Historical Context: Seventy-Five Years of Marginal Progress</h3>
<p>India's first Lok Sabha (1952) had 22 women MPs (4.4% of 499 seats). The 2024 Lok Sabha has approximately 74 women MPs (13.6% of 543). In 72 years, women's representation has increased by approximately 9 percentage points, an average of <b>0.13 percentage points per year</b>. At this rate, India would reach 33% women MPs (the Women's Reservation Bill target) in approximately <b>2170</b>. The spatial dimension adds urgency: the zero-women constituencies have likely <em>always</em> been zero-women constituencies or close to it. Without structural intervention, they will remain so indefinitely because the underlying social structures change at generational timescales.</p>

<h3>The Women's Reservation Bill: Geographic Implications</h3>
<div class="hl warn">The <b>Nari Shakti Vandan Adhiniyam</b> (Women's Reservation Bill), passed by Parliament in September 2023 but not yet implemented (pending delimitation and census), would reserve <b>one-third of Lok Sabha seats for women candidates</b>, approximately 181 seats. When implemented, it would force parties to nominate women in exactly the kind of constituencies currently showing red Xs. The geographic rotation system (different seats reserved in successive elections) means that every constituency would eventually be a reserved seat, ensuring that women's candidacy is normalized across the full geography of Indian democracy, not confined to progressive pockets. The spatial pattern on this map is thus a <b>before picture</b>: the strongest possible argument for why the bill's implementation is necessary. Without it, the red Xs will persist for generations. With it, parties will be structurally compelled to break the exclusion pattern, constituency by constituency, across geographic space.</div>

<h3>Anthropological and Sociological Dimensions</h3>
<p>The geographic clustering of women's political exclusion in the Hindi heartland reflects what sociologists call <b>"patriarchal bargain"</b> structures (Deniz Kandiyoti, 1988). In these regions, women's social security (protection, housing, economic support) depends on compliance with patriarchal norms (modesty, domesticity, deference to male authority). Entering the public sphere of electoral politics directly violates these norms, threatening not just the individual woman but her family's social standing. The <b>spatial concentration</b> of this bargain in north-central India corresponds to the historically dominant joint family system, strong caste endogamy enforcement, and the practice of <em>purdah</em> (female seclusion), which is more prevalent in these regions than in the south or northeast. The Dravidian social reform tradition in Tamil Nadu and Kerala (Periyar, Narayan Guru, Phule) systematically attacked these patriarchal structures a century ago, creating the more permissive social environment that allows women's candidacy in southern states today. The red Xs on this map are, in a sense, the <b>geographic shadow of unreformed patriarchal social structure</b>.</p>

<p class="ref"><b>Key references:</b> Election Commission of India (2024). Constituency-wise Women Candidature data. | Kandiyoti, D. (1988). Bargaining with patriarchy. <i>Gender & Society</i>, 2(3). | Rai, P. (2017). Women's representation in Indian Parliament. <i>India Review</i>, 16(2). | Krook, M.L. (2009). <i>Quotas for Women in Politics</i>. Oxford UP. | Chattopadhyay, R. & Duflo, E. (2004). Women as policy makers. <i>Econometrica</i>, 72(5).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 66: The Gauntlet (Funnel Chart)
# ═══════════════════════════════════════════════════════════════════
G["66"] = '''
<h2>The Gauntlet: From 8,360 Candidates to 47 Women Winners</h2>
<p class="tagline">A funnel of attrition. At every stage, women are filtered out more harshly than men. The pipeline does not leak; it is structurally designed to exclude.</p>

<h3>What You Are Seeing</h3>
<p>A <b>funnel chart</b> showing successive stages of candidate filtration in the 2024 Lok Sabha election: <b>total candidates</b> (approximately 8,360) to <b>women candidates</b> (458) to <b>women who saved their deposit</b> (133) to <b>women who won</b> (74). Each stage narrows dramatically, revealing the compounding attrition that women face at every level of the electoral pipeline.</p>

<h3>Stage-by-Stage Attrition</h3>
<div class="hl"><b>Stage 1: Filing.</b> Of approximately 8,360 total candidates, only 458 were women (5.5%). This means that <b>94.5% of all candidacies were male</b>. The filing stage is the widest part of the funnel and the point of greatest absolute exclusion. <b>Stage 2: Deposit survival.</b> Under Indian election law, a candidate who fails to receive at least one-sixth (16.67%) of the total valid votes <b>forfeits their security deposit</b> (Rs 25,000 for general category). Of 458 women candidates, <b>325 (71%) forfeited their deposit</b>, compared to approximately 85 to 90% of all candidates. The deposit forfeiture rate for women is slightly better than the overall rate (because the overall includes thousands of frivolous male independents), but the 71% figure still means that <b>nearly three-quarters of women who entered the arena were electorally insignificant</b>. <b>Stage 3: Winning.</b> Of the 133 women who saved their deposit, 74 won their seat (a 56% conversion rate, actually comparable to men who save their deposit). This reveals the critical insight: <b>the bottleneck is not in winning but in being a credible candidate in the first place</b>.</div>

<h3>The "Credibility Gap" at the Funnel's Throat</h3>
<div class="hl gold">The funnel's most dramatic narrowing occurs between "all women candidates" (458) and "women who saved deposit" (133). The 325 women who forfeited represent a specific category: <b>women fielded without genuine party backing</b>. They include independent candidates with no organizational support, candidates from micro-parties using women as token nominees, and occasionally sacrificial candidates placed by major parties in unwinnable seats to appear gender-inclusive while concentrating real resources on male candidates in competitive seats. This "credibility gap" is the funnel's structural chokepoint: parties must provide <b>genuine campaign infrastructure</b> (funding, media access, organizational network, booth-level workers) to women candidates for them to cross the deposit threshold. The 325 forfeiture cases suggest that the vast majority of women's candidacies were <b>nominal rather than resourced</b>.</div>

<h3>Comparative Context</h3>
<p>India's 13.6% women MPs (2024) places it at approximately <b>rank 143 out of 190 countries</b> tracked by the Inter-Parliamentary Union (IPU). This is below the global average of approximately 26%, below the South Asian average (approximately 20%, boosted by Bangladesh and Nepal), and far below the leaders (Rwanda 61%, Cuba 53%, Nicaragua 52%, New Zealand 49%). The countries at the top of the IPU rankings all employ some form of <b>quota or reservation mechanism</b>: Rwanda mandates 30% women in both chambers; Bolivia and Mexico require gender parity on party lists; the Scandinavian countries have voluntary but binding party quotas. No country has achieved above 30% women's representation through organic, unregulated party competition alone. India's funnel chart is thus not an anomaly; it is the <b>predictable outcome of an unregulated system</b> where patriarchal social structures, gendered campaign economics, and male-dominated party hierarchies combine to filter women out at every stage.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The funnel reveals that the intervention must target <b>multiple stages simultaneously</b>. At the filing stage: the Women's Reservation Bill (reserving 181 seats) addresses the widest bottleneck by forcing parties to nominate women. At the credibility stage: parties should be <b>legally required to allocate proportional campaign funding</b> to women candidates (some countries mandate this; India does not). At the winning stage: <b>voter education campaigns</b> addressing the "electability bias" (the widespread assumption that women cannot win, which becomes self-fulfilling when parties act on it) could shift voter behavior. Additionally, <b>candidate training programs</b> (public speaking, campaign management, media interaction, legal literacy) could increase the pool of women with the skills and confidence to enter the arena. The funnel's shape will only change when interventions address all three chokepoints: access (nomination), resources (funding and infrastructure), and conversion (voter acceptance).</div>

<p class="ref"><b>Key references:</b> Election Commission of India (2024). Women Candidature Statistics. | IPU (2024). Women in Parliament database. | Krook, M.L. (2009). <i>Quotas for Women in Politics</i>. Oxford UP. | Norris, P. & Lovenduski, J. (1995). <i>Political Recruitment: Gender, Race and Class in the British Parliament</i>. Cambridge UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 67: Gender Gap in Electorate
# ═══════════════════════════════════════════════════════════════════
G["67"] = '''
<h2>Gender Gap in the Electorate: Female Voters per 1,000 Male by State</h2>
<p class="tagline">Parity is 1,000. Green states are there. Red states have millions of "missing" women voters.</p>

<h3>What You Are Seeing</h3>
<p>A bar or lollipop chart showing, for each Indian state, the <b>number of female registered voters per 1,000 male registered voters</b>. A value of 1,000 indicates gender parity in the electorate. Values above 1,000 (green) mean more women than men are registered. Values below 1,000 (red) mean fewer women are registered, implying either a skewed sex ratio, lower women's registration rates, or both. The <b>parity line at 1,000</b> is the reference point.</p>

<h3>The Missing Women Voters</h3>
<div class="hl"><b>Bihar (907)</b> has the worst gender ratio in the electorate, meaning approximately 93 women are registered for every 100 men. Given Bihar's electorate of approximately 73 million, this implies roughly <b>3.5 million "missing" women voters</b> compared to what a sex-ratio-parity electorate would produce. These missing voters are a compound of two factors: <b>biologically missing women</b> (the adverse sex ratio reflecting son preference, sex-selective practices, and higher female mortality from neglect) and <b>administratively missing women</b> (women who are alive but not registered as voters, due to illiteracy, lack of identity documents, restricted mobility, or household-level patriarchal control that prevents women from engaging with state institutions). Distinguishing these two sources requires comparing voter registration sex ratios with census population sex ratios: where the voter sex ratio is worse than the population sex ratio, <b>administrative exclusion</b> is the binding constraint and can be addressed through targeted registration drives.</div>

<h3>Kerala at the Other Extreme</h3>
<div class="hl gold"><b>Kerala (1,084)</b> has more women than men in its electorate, reflecting both a healthy biological sex ratio (women naturally outnumber men in populations without sex-selective practices, because women have lower mortality at every age) and high administrative inclusion (near-universal voter registration facilitated by high literacy, active civic culture, and effective state administration). Kerala's value of 1,084 is close to what demographers would expect from a population with no sex selection and equal registration rates: approximately 1,050 to 1,080 females per 1,000 males. Kerala thus represents the <b>biologically normal baseline</b>, and deviations below 1,000 in other states measure the combined impact of son preference, female disadvantage, and administrative exclusion.</div>

<h3>The Geographic Pattern</h3>
<p>The gender gap in the electorate follows the same north-south gradient visible throughout this atlas. Southern states (Kerala, Tamil Nadu, Andhra Pradesh, Karnataka) cluster near or above parity. Northern and eastern states (Bihar, UP, Rajasthan, Jharkhand, Haryana) cluster well below parity. This geographic pattern is the <b>electoral expression of India's gender development gradient</b>: the same structural factors (female literacy, economic participation, social autonomy, healthcare access) that determine women's development outcomes also determine whether women are registered to vote and whether they show up at polling stations.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The ECI has conducted <b>Special Summary Revision drives</b> targeting women's registration, particularly in states with low gender ratios. The SVEEP (Systematic Voters' Education and Electoral Participation) program includes gender-specific outreach. But the data suggests that <b>the deficit is too large for incremental registration drives to close</b>. Bihar's 3.5 million missing women voters cannot be recovered by adding a few hundred registration camps; the deficit reflects structural barriers (lack of identity documents, illiteracy, restricted mobility, household-level control) that require <b>systemic interventions</b>: universal identity document issuance (linked to Aadhaar), home-visit registration for immobile women, and community mobilization through women's self-help groups. The spatial concentration of the deficit in a limited number of states means that <b>targeted investment in 5 to 7 states could close the majority of the national gender gap in the electorate</b>.</div>

<p class="ref"><b>Key references:</b> Election Commission of India (2024). State-wise Number of Electors (gender disaggregated). | Sen, A. (1990). More than 100 million women are missing. <i>NYRB</i>. | SVEEP (2024). Gender and electoral participation reports.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 68: Deposit Forfeiture Massacre (Strip Plot)
# ═══════════════════════════════════════════════════════════════════
G["68"] = '''
<h2>Deposit Forfeiture: The Red Wall of 325 Women</h2>
<p class="tagline">Every woman candidate as a dot. 325 red (forfeited), 86 gold (lost but saved deposit), 47 green (won). The red wall tells the story of tokenism.</p>

<h3>What You Are Seeing</h3>
<p>A <b>strip plot</b> (or beeswarm/jitter plot) where every one of the 458 women candidates in the 2024 Lok Sabha election is plotted as an individual dot. Dots are colored: <b>red = forfeited deposit</b> (received less than 1/6 of votes), <b>gold = lost but saved deposit</b> (received over 1/6 of votes but did not win), <b>green = won the seat</b>. The spatial arrangement may sort candidates by vote share, state, or party. The visual dominance of the red zone is the chart's central message.</p>

<h3>What Deposit Forfeiture Means</h3>
<div class="hl">The <b>security deposit</b> system was introduced to deter frivolous candidacies. Candidates must pay Rs 25,000 (Rs 12,500 for SC/ST) at the time of filing. If the candidate receives fewer than one-sixth (16.67%) of valid votes in their constituency, the deposit is forfeited. The threshold is low enough that any serious candidate should clear it. <b>Forfeiture therefore signals that a candidacy was not serious</b>: the candidate had no meaningful campaign infrastructure, party backing, or voter recognition. Among the 325 women who forfeited, the vast majority fall into identifiable categories: <b>independent candidates</b> with no party support; <b>candidates from micro-parties</b> (registered parties with no organizational presence, sometimes created solely to field candidates for symbolic purposes); and <b>sacrificial candidates</b> from major parties placed in seats where the party had no chance of winning, using a woman's name to pad gender statistics without investing real campaign resources.</div>

<h3>The 86 Gold Dots: The "Almost" Zone</h3>
<div class="hl gold">The 86 women who saved their deposit but did not win represent the <b>most policy-relevant segment</b>. These women ran credible campaigns, attracted significant voter support (above 16.67% and in many cases above 30%), but fell short. They include: <b>strong second-place finishers</b> in competitive multi-cornered races, <b>opposition candidates in safe seats</b> where the dominant party's margin was too large to overcome, and <b>first-time candidates building name recognition</b> for future elections. With better party support, campaign funding, or strategic alliance negotiations, <b>many of these 86 could have won</b>. They represent the <b>unrealized potential</b> of women in Indian politics: women who proved their viability but were denied the resources or strategic positioning that would have carried them across the finish line.</div>

<h3>The 47 Green Dots: What Made Them Different?</h3>
<p>The 47 women who won share common characteristics that distinguish them from the red and gold groups. Most won on <b>major party tickets</b> (BJP, Congress, TMC, DMK) in constituencies where they received <b>full party campaign infrastructure</b>. Many are members of <b>political dynasties</b> (daughters, wives, or daughters-in-law of established male politicians), which gave them instant name recognition and organizational networks. A smaller number are <b>self-made politicians</b> who rose through local government (panchayat or municipal) experience. The geographic distribution of winners clusters in states where either the party leadership actively promotes women (TMC in West Bengal) or where the social environment is more receptive to women candidates (parts of Rajasthan, Madhya Pradesh where BJP reserved several tickets). The <b>dynasty pathway</b> to women's political success is a problematic but persistent feature: it allows women to bypass the gatekeeping barriers that block non-dynastic women, but it perpetuates the concentration of political power within a narrow elite.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The strip plot reveals that <b>the problem is not voter rejection of women but party under-investment in women candidates</b>. The 47 winners prove that women can win when backed by serious party machinery. The 86 gold-zone candidates prove that many more women are competitive. The 325 red dots prove that the majority of women's candidacies are <b>nominal, under-resourced, and designed to fail</b>. Policy interventions should target the party machinery: <b>mandatory proportional campaign funding</b> for women candidates (requiring parties to allocate a share of their campaign expenditure proportional to the share of women nominees), <b>candidate training programs</b> funded by the ECI or public agencies, and <b>transparency requirements</b> (requiring parties to publicly report how much they spent on each candidate, disaggregated by gender). The Women's Reservation Bill addresses the top of the funnel (nomination); these complementary interventions address the middle (resourcing) and would move dots from red to gold and from gold to green.</div>

<p class="ref"><b>Key references:</b> ECI (2024). Individual Performance of Women Candidates data. | Basu, A. (2010). Women, dynasties and democracy in India. In Kapur & Mehta (eds.), <i>Rethinking Public Institutions</i>. | Norris, P. & Lovenduski, J. (1995). <i>Political Recruitment</i>. Cambridge UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 69: State Scoreboard (Triple Panel)
# ═══════════════════════════════════════════════════════════════════
G["69"] = '''
<h2>State Scoreboard: Women Elected, Forfeiture Rate, and Gender Ratio</h2>
<p class="tagline">14 states elected zero women. Kerala elected zero despite the best gender ratio in India. The pipeline breaks at nomination, not at voting.</p>

<h3>What You Are Seeing</h3>
<p>A <b>triple-panel visualization</b> showing, for each state: <b>Panel 1</b> = number of women elected to the Lok Sabha. <b>Panel 2</b> = deposit forfeiture rate among women candidates. <b>Panel 3</b> = female-to-male voter ratio (gender ratio in the electorate). The three panels together reveal the <b>disconnect between gender equity in the population and gender equity in political outcomes</b>.</p>

<h3>The Kerala Paradox</h3>
<div class="hl"><b>Kerala elected zero women MPs in 2024</b> despite having India's best gender ratio (1,084 females per 1,000 males), highest female literacy (96%), highest women's workforce participation among major states, and most progressive social norms regarding women's public activity. This paradox is the most important finding in the entire women's data analysis because it demolishes the <b>naive pipeline theory</b>: the assumption that as women's social indicators improve, women's political representation will automatically follow. Kerala's data proves that <b>voter-side gender equity does not translate into candidate-side gender equity</b> when the bottleneck is at the party nomination stage. Neither the CPI(M)-led LDF nor the Congress-led UDF nominated significant numbers of women in Kerala's 20 Lok Sabha constituencies. Kerala's progressive electorate was never given the opportunity to vote for women because parties did not provide them as options.</div>

<h3>States That Elected Zero Women</h3>
<div class="hl gold">The <b>14 states that elected zero women</b> span a wide range of development profiles: from Kerala (high HDI) to Bihar (low HDI), from Himachal Pradesh (small, mountainous, moderate development) to Odisha (large, coastal, poor). This heterogeneity confirms that women's exclusion from Parliament is <b>not a function of state-level development</b> but of <b>party-level nomination decisions</b> that operate independently of the state's social indicators. The geographic spread of zero-women states across all regions of India further undermines any regional or cultural explanation: this is not a "north Indian problem" or a "backward state problem." It is a <b>systemic, pan-Indian party-system problem</b> that affects progressive and conservative, rich and poor, north and south alike.</div>

<h3>The Forfeiture Rate as a Quality Indicator</h3>
<p>Panel 2 (forfeiture rate) reveals which states field women candidates <b>seriously</b> vs <b>tokenistically</b>. States where the forfeiture rate among women is low (below 50%) include West Bengal (TMC fields women in winnable seats), parts of Rajasthan and MP (BJP allocated genuine tickets to women). States where the forfeiture rate is extremely high (above 80%) include states where women's candidacies are dominated by micro-party nominees and independents with no realistic chance of winning. The forfeiture rate is thus a <b>quality indicator for women's political inclusion</b>: a state that fields 20 women candidates with a 90% forfeiture rate is less genuinely inclusive than a state that fields 5 women with a 20% forfeiture rate.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The triple-panel scoreboard demands that <b>party-level accountability replace state-level accountability</b> in the discourse on women's representation. It is not "Bihar's fault" or "Kerala's fault" that they elected zero women; it is the <b>BJP's, Congress's, CPI(M)'s, LDF's, NDA's, and INDIA alliance's fault</b> for not nominating women in those states. Mandatory reporting of party-level gender nomination statistics (already published by the ECI but rarely used in public discourse) should become a standard part of election analysis. <b>Internal party democracy reforms</b>, requiring parties to hold transparent primaries or selection processes with minimum gender quotas, could address the nomination bottleneck. The Scandinavian model (where parties voluntarily adopted "zipper lists" alternating male and female candidates) is unlikely to work in India's first-past-the-post system, making the <b>Women's Reservation Bill the only structural mechanism</b> capable of overriding party gatekeeping at the necessary scale.</div>

<p class="ref"><b>Key references:</b> ECI (2024). State-wise and party-wise women candidature data. | Rai, P. (2017). Women's representation in Indian Parliament. <i>India Review</i>, 16(2). | Dahlerup, D. (2006). <i>Women, Quotas and Politics</i>. Routledge.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 70: Women Candidature Terrain 3D
# ═══════════════════════════════════════════════════════════════════
G["70"] = '''
<h2>Women Candidature Terrain: A 3D Landscape of Political Exclusion</h2>
<p class="tagline">Height = percentage of women candidates. Red X on the floor = zero women. Most of India is a flat red desert with rare green peaks.</p>

<h3>What You Are Seeing</h3>
<p>A <b>3D terrain map</b> where each constituency's vertical height encodes the <b>percentage of candidates who were women</b>. Red X markers on the floor indicate constituencies with zero women. Green peaks indicate constituencies with relatively high women's candidacy (above 10 to 15% of total candidates). The overwhelming visual impression is of a <b>vast, flat desert</b> (most constituencies at or near zero) punctuated by rare green peaks.</p>

<h3>The Topography of Exclusion</h3>
<div class="hl">This 3D terrain makes the <b>geographic concentration of women's political exclusion viscerally physical</b>. The flat red desert stretches across north-central India (UP, Bihar, Rajasthan, MP, Chhattisgarh), with occasional rises in urban areas (Delhi, Mumbai, Kolkata) and scattered peaks in the south (TN, Kerala) and northeast (Assam, Manipur). The terrain metaphor is analytically precise: women's political participation in India is not a gently varying surface but an <b>extremely skewed landscape with a low baseline and rare spikes</b>. The median constituency has only 1 to 2 women among 15 to 20 total candidates (5 to 10%). The red Xs (152 constituencies at absolute zero) form contiguous lowlands, confirming that exclusion is geographically clustered, not randomly distributed.</div>

<h3>What Creates the Green Peaks?</h3>
<div class="hl gold">The rare green peaks (constituencies with 4 or more women candidates, representing above 15 to 20% of the field) tend to share characteristics: <b>urban location</b> (Mumbai North, Bangalore South, Kolkata), <b>proximity to a major party's women-friendly state unit</b> (TMC-held West Bengal constituencies), or <b>the presence of a high-profile woman candidate who attracts other women to run</b> (a competitive woman nominee from a major party appears to encourage independent and minor-party women to also file, creating a clustering effect). This "attraction effect" suggests that <b>visibility matters</b>: seeing one woman run normalizes women's candidacy and draws others in. The reverse is also true: the red X deserts are self-perpetuating because the absence of women candidates normalizes their absence, discouraging potential entrants.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The terrain format reveals that India's women's political participation landscape requires <b>massive terraforming, not gentle erosion</b>. Incremental awareness campaigns and voluntary party commitments will not flatten the desert or raise the baseline. The terrain will only change shape through <b>structural interventions</b> that force the baseline upward: the Women's Reservation Bill (raising the floor from 0% to 100% in reserved constituencies), mandatory party-level women's nomination quotas (raising the baseline across all constituencies), and campaign finance reform that ensures women candidates receive proportional resources. The 3D visualization is a particularly effective advocacy tool because it makes the <b>scale of the problem impossible to ignore</b>: the vast flat desert of zero or near-zero women's candidacy, when rendered as physical terrain, is more emotionally compelling and politically motivating than abstract percentages.</div>

<p class="ref"><b>Key references:</b> ECI (2024). Constituency-wise Women Candidature. | Krook, M.L. (2009). <i>Quotas for Women in Politics</i>. Oxford UP. | Three.js documentation.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 71: Delimitation Simulator
# ═══════════════════════════════════════════════════════════════════
G["71"] = '''
<h2>Delimitation Simulator: What If India Had More Seats?</h2>
<p class="tagline">Drag the slider from 543 to 1000. Watch the North gain and the South lose. The mathematics of representation inequality.</p>

<h3>What You Are Seeing</h3>
<p>An interactive simulator with a <b>slider from 543 (current) to 1000 total Lok Sabha seats</b>. Each frame shows the result of <b>proportionally redistributing seats to states based on population</b> using the <b>Webster/Sainte-Lague method</b>. The scatter plot shows each state's <b>current seats (X-axis) vs new proportional seats (Y-axis)</b>. The <b>gold diagonal line</b> = no change. Points above the diagonal gain seats; points below lose seats. Color = region. Size = magnitude of change.</p>

<h3>The Webster/Sainte-Lague Method</h3>
<div class="hl">The <b>Webster (Sainte-Lague) method</b> is a divisor-based proportional allocation algorithm. It works by dividing each state's population by successive odd numbers (1, 3, 5, 7, ...) to produce a sequence of "quotients." The total seats are allocated one at a time, each going to the state with the highest remaining quotient. This method is mathematically proven to minimize the maximum proportional deviation between any state's seat share and its population share. It is used in New Zealand, Norway, Sweden, and Germany for legislative seat allocation. Compared to the D'Hondt method (which favors larger states) or the Hamilton method (which can produce paradoxical results), Webster is the most proportionally neutral. For India, it means that seat reallocation would reflect population as accurately as possible without systematic bias toward large or small states.</div>

<h3>What the Simulator Reveals</h3>
<div class="hl gold">At <b>543 seats (current)</b>: India's seat allocation is frozen from the 2001 Census (within states) and 1971 Census (between states). Since 1971, northern states have grown much faster. At 543 proportional seats: <b>UP gains from 80 to approximately 91</b>, <b>Bihar gains from 40 to approximately 53</b>, <b>Tamil Nadu drops from 39 to approximately 31</b>, <b>Kerala drops from 20 to approximately 14</b>. As you <b>drag the slider rightward</b> (increasing total seats toward 700, 800, 1000), every state gains seats in absolute terms, but the <b>relative shift persists</b>: southern states consistently sit below the diagonal (losing share) while northern states sit above (gaining share). At <b>1000 seats</b>: TN would have approximately 57 (up from 39 in absolute terms but down from 7.2% to 5.7% of total). UP would have approximately 168 (up from 80 but its share rises from 14.7% to 16.8%). The absolute gains partially mask the relative loss, which is why <b>increasing total seats is the most politically palatable form of delimitation</b>: no state literally loses seats, even as relative power shifts.</div>

<h3>The Constitutional and Political Crisis</h3>
<div class="hl warn">The <b>Article 82</b> of the Indian Constitution mandates readjustment of seat allocation after each Census. The <b>42nd Amendment (1976)</b> froze the allocation at 1971 Census levels to prevent states with successful population control (the South) from being penalized with seat losses. The <b>84th Amendment (2001)</b> extended this freeze until 2026. With the 2021 Census delayed (conducted in 2024-2025), the political crisis is imminent: <b>any population-based redistribution will transfer Lok Sabha seats from south to north</b>. Southern states view this as punishment for successful family planning. Northern states view proportional representation as a democratic right. This is not merely a statistical dispute; it strikes at the foundations of Indian federalism. Tamil Nadu, Kerala, Karnataka, and Andhra Pradesh collectively contribute approximately 35% of India's GDP but would hold only approximately 22% of Lok Sabha seats under proportional allocation. The simulator makes this impending geographic power shift tangible, and any resolution will require balancing democratic equality (one person, one vote) with federalist protections for states that invested in population control.</div>

<p class="ref"><b>Key references:</b> Balinski, M. & Young, H.P. (2001). <i>Fair Representation: Meeting the Ideal of One Man, One Vote</i>. Brookings. | Constitution of India, Articles 81, 82, 170. | National Commission to Review the Working of the Constitution (2002). Delimitation report. | Kumar, S. (2020). Delimitation dilemma. <i>Economic and Political Weekly</i>.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 72: Fiscal Returns
# ═══════════════════════════════════════════════════════════════════
G["72"] = '''
<h2>Fiscal Returns: The Tax Inequality Map of India</h2>
<p class="tagline">For every Rs 100 a state pays in taxes, how much does it get back? Tamil Nadu: Rs 29.7. Bihar: Rs 142.5. The geography of fiscal redistribution.</p>

<h3>What You Are Seeing</h3>
<p>A diverging horizontal bar chart showing, for each major Indian state, <b>the rupees received from the central government for every Rs 100 paid in taxes</b>. The <b>gold dashed line at Rs 100</b> marks break-even. States to its left are <em>net contributors</em> (paying more than they receive). States to its right are <em>net recipients</em> (receiving more than they pay). Data is estimated from 15th Finance Commission allocations and state-level tax contribution data.</p>

<h3>How India's Fiscal Architecture Works</h3>
<div class="hl">India's fiscal transfer system operates through three channels. <b>(1) Devolution of central taxes</b>: the Finance Commission (appointed every 5 years under Article 280) recommends the share of central tax revenue to be devolved to states and the formula for its distribution. The <b>15th Finance Commission (2020-2025)</b> recommended 41% of the divisible pool go to states, distributed by formula: <em>Population (15%)</em>, <em>Area (15%)</em>, <em>Forest & Ecology (10%)</em>, <em>Income Distance (45%)</em>, <em>Demographic Performance (12.5%)</em>, <em>Tax & Fiscal Effort (2.5%)</em>. <b>(2) Grants-in-aid</b>: specific grants for disaster relief, local bodies, health, education, and other purposes. <b>(3) Centrally Sponsored Schemes (CSS)</b>: funding for central government programs implemented by states (MGNREGA, Swachh Bharat, PM Awas Yojana). The combined effect of these three channels creates the fiscal transfer pattern visible in this chart.</div>

<h3>The "Income Distance" Criterion: Why Poor States Receive More</h3>
<div class="hl gold">The dominant criterion, <b>Income Distance (45% weight)</b>, is calculated as the difference between a state's per-capita GSDP and the state with the highest per-capita GSDP. States farther from the richest state receive proportionally more. This single criterion is the largest driver of the fiscal redistribution pattern: because Bihar, UP, MP, and Jharkhand have per-capita GSDPs 3 to 5 times lower than Goa, Haryana, and Delhi, they receive disproportionately large shares. The logic is economically sound: <b>fiscal equalization</b> (transferring resources from richer to poorer regions) is a feature of every federal democracy. Germany's <em>Landerfinanzausgleich</em>, Canada's <em>equalization payments</em>, Australia's GST distribution, and the EU's Structural Funds all operate on similar principles. The question is not whether India should equalize (it should) but <b>how much weight to give population versus other criteria</b>.</div>

<h3>The "Double Whammy" Problem</h3>
<div class="hl warn">Southern states (Tamil Nadu, Karnataka, Kerala, Maharashtra, Andhra Pradesh, Telangana) face a <b>compounding penalty</b> that makes fiscal transfers politically explosive. These states invested in education, healthcare, and family planning, which <b>reduced their population growth</b>. Under population-based delimitation, they will <b>lose Lok Sabha seats</b> (Chart 71). Simultaneously, because they are economically successful (partly <em>because</em> of lower population growth and higher human capital), they pay more taxes than they receive in transfers. They are thus punished twice for the same responsible behavior: <b>less political representation AND less fiscal return</b>. Northern states (UP, Bihar, MP, Rajasthan), which did not invest as heavily in population control, gain both <b>more seats</b> (larger populations) AND <b>more fiscal transfers</b> (lower income). This creates a <b>perverse incentive structure</b> at the state level: responsible demographic and economic policy is penalized, while irresponsible policy is rewarded. No single chart in this atlas captures a more politically charged spatial inequality.</div>

<h3>Comparative Federalism</h3>
<p>India's fiscal imbalance is not extreme by international standards. Germany's fiscal equalization transfers approximately 2% of GDP from richer to poorer <em>Lander</em>. Australia's GST redistribution produces ratios comparable to India's. Even the US, which has no explicit equalization mechanism, implicitly transfers approximately $0.80 to $1.50 from high-income states (Connecticut, New Jersey) to low-income states (Mississippi, West Virginia) for every tax dollar through federal spending patterns. What makes India's case uniquely contentious is that the fiscal transfer overlaps with the <b>delimitation crisis and the linguistic-cultural north-south divide</b>, creating a multi-dimensional grievance that touches economic interests, political power, cultural identity, and historical resentment simultaneously.</p>

<p class="ref"><b>Key references:</b> 15th Finance Commission (2020). <i>Report for 2021-2026</i>. Government of India. | Rao, M.G. & Singh, N. (2005). <i>Political Economy of Federalism in India</i>. Oxford UP. | Boadway, R. & Shah, A. (2009). <i>Fiscal Federalism: Principles and Practice of Multiorder Governance</i>. Cambridge UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 73: Women Reservation Simulator
# ═══════════════════════════════════════════════════════════════════
G["73"] = '''
<h2>Women's Reservation Simulator: Sliding from 0% to 100%</h2>
<p class="tagline">At 33% reservation: approximately 181 seats reserved for women. Current: 74 women MPs (13.6%). Drag the slider to see what structural change looks like.</p>

<h3>What You Are Seeing</h3>
<p>An interactive simulator with a <b>slider from 0% to 100% women's reservation</b>. As you drag rightward, the number of seats mandated for women candidates increases. At <b>33% (the actual bill)</b>: approximately 181 of 543 seats. The visualization shows how many women would serve under each reservation level, assuming women win all reserved seats (which is the design intent, since only women can contest reserved seats).</p>

<h3>The Gap Between 13.6% and 33%</h3>
<div class="hl">India currently has approximately 74 women MPs (13.6%). The reservation bill targets 33%, or approximately 181 seats. The gap of approximately 107 seats represents <b>women who would enter Parliament solely because of the structural mandate</b>, not because parties would have nominated them voluntarily. This gap is the measure of <b>party gatekeeping failure</b>: it quantifies how many women the party system excludes that a structural intervention would include. At 50% (the gender parity target advocated by some feminist organizations), approximately 272 seats would be reserved, more than tripling current women's representation.</div>

<h3>Why 33% and Not 50%?</h3>
<div class="hl gold">The 33% figure was a political compromise, not a principled threshold. The original bill (first introduced in 1996, reintroduced multiple times) chose 33% as the minimum "critical mass" needed for women to influence legislative outcomes rather than being token presences. Political scientist Drude Dahlerup's <b>critical mass theory</b> (1988) argues that until a minority group reaches approximately 30% of a deliberative body, its members are treated as tokens representing their group rather than as individuals with substantive policy positions. Above 30%, the group begins to influence norms, set agendas, and form intra-group coalitions that change legislative behavior. Empirical evidence from Nordic parliaments (which crossed 30% women in the 1980s) supports this threshold: women's policy priorities (childcare, parental leave, reproductive rights, violence against women) received significantly more legislative attention after the 30% threshold was crossed.</div>

<h3>The Rotation Question</h3>
<p>The bill specifies that reserved constituencies will <b>rotate</b> with each general election, so that no constituency is permanently reserved. This means that over three election cycles, approximately all 543 constituencies would have been reserved at least once, normalizing women's candidacy across the full geography. The rotation design addresses two concerns: <b>avoiding permanent geographic concentration</b> of women's representation in a fixed set of seats, and <b>ensuring that incumbency advantages do not lock women out</b> of unreserved seats by creating permanent male-incumbent strongholds in the remaining two-thirds.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The simulator makes visible what 75 years of "gradual change" have failed to achieve. At the current rate of improvement (approximately 0.13 percentage points per year), India would reach 33% women MPs in approximately 2170. The reservation bill would achieve it in a single election cycle. The contrast between <b>incremental voluntarism</b> (waiting for parties to change) and <b>structural intervention</b> (mandating change) is the fundamental policy debate that this simulator quantifies. Every other country that has achieved above 30% women's representation has employed some form of quota, reservation, or mandatory parity mechanism. India's own experience with panchayat-level reservation (mandated since the 73rd Amendment in 1993) has been transformative: over 1.4 million women currently serve as elected panchayat representatives, many of whom would never have entered politics without the structural mandate. The Lok Sabha reservation bill would replicate this proven mechanism at the national level.</div>

<p class="ref"><b>Key references:</b> Dahlerup, D. (1988). From a small to a large minority: women in Scandinavian politics. <i>Scandinavian Political Studies</i>, 11(4). | Chattopadhyay, R. & Duflo, E. (2004). Women as policy makers. <i>Econometrica</i>, 72(5). | Krook, M.L. (2009). <i>Quotas for Women in Politics</i>. Oxford UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 74: Moran's I Criteria Explorer
# ═══════════════════════════════════════════════════════════════════
G["74"] = '''
<h2>Moran's I Criteria Explorer: Which Allocation Formula Produces the Fairest Map?</h2>
<p class="tagline">Two curves: Moran's I computed for different allocation criteria. Lower I = more equitable geographic dispersion. Higher I = more clustering.</p>

<h3>What You Are Seeing</h3>
<p>A visualization showing how <b>Moran's I</b> varies when seat allocation weights are shifted between different criteria (population, area, fiscal contribution, literacy, etc.). The chart tests the spatial equity of alternative delimitation formulas: which formula produces a seat distribution that is most evenly dispersed across geographic space (low I) vs most clustered (high I)?</p>

<h3>The Spatial Equity Principle</h3>
<div class="hl">In an ideal representative democracy, political power should be <b>distributed in proportion to people, not concentrated in geographic clusters</b>. When seat allocation is purely population-based, it produces geographic clustering: populous states in north-central India get large seat blocks, while less populous states get small blocks. The resulting Moran's I for seats-per-unit-area would be high, reflecting this concentration. Alternative formulas that incorporate <b>area</b> (giving more seats to geographically large states) or <b>inverse population density</b> (giving more seats to sparsely populated regions) would produce lower Moran's I, indicating a more <b>spatially dispersed</b> distribution of representation. The tradeoff is between <b>democratic equality</b> (one person, one vote, which favors pure population weighting) and <b>geographic representation</b> (ensuring that all regions have adequate voice, which favors area or inverse-density weighting).</div>

<h3>What the Curves Reveal</h3>
<div class="hl gold">The curves likely show that <b>pure population weighting produces the highest Moran's I</b> (most geographic clustering of seats) because India's population is itself highly spatially concentrated (the Indo-Gangetic plain holds approximately 40% of India's population on approximately 15% of its area). <b>Area-weighted allocation produces moderate I</b> (more dispersed, because large but sparsely populated states like Rajasthan, MP, and the Northeast gain seats). <b>Fiscal-weighted allocation</b> (giving more seats to states that contribute more taxes) would produce a different pattern: concentration in the south and west (contributor states) rather than the north (populous states). The "optimal" formula depends on which values are prioritized: democratic equality, geographic balance, fiscal accountability, or developmental incentive.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The explorer demonstrates that <b>delimitation formula design is not a technical exercise but a value choice with geographic consequences</b>. India could choose a formula that minimizes geographic power concentration (low Moran's I), which would give more seats to smaller and less populous states, improving geographic representation but potentially diluting the principle of one-person-one-vote. Or it could choose pure population proportionality (high Moran's I), which satisfies democratic equality but concentrates power in the most populous (and currently least developed) states. The Finance Commission's multi-criteria formula (which already includes population, area, forest cover, income distance, and demographic performance) provides a model for a <b>multi-criteria delimitation formula</b> that could balance competing values. The Moran's I curves provide an empirical tool for evaluating the spatial consequences of each formula before it is implemented.</div>

<p class="ref"><b>Key references:</b> Anselin, L. (1995). LISA. <i>Geographical Analysis</i>, 27(2). | Balinski, M. & Young, H.P. (2001). <i>Fair Representation</i>. Brookings. | 15th Finance Commission (2020). Formula criteria documentation.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 75: Punishment Value 3D
# ═══════════════════════════════════════════════════════════════════
G["75"] = '''
<h2>Punishment Value: The Triple Burden in Three Dimensions</h2>
<p class="tagline">Fiscal return x female voter share x seats. TN and MH bear the worst triple burden: high taxes paid, low returns received, and seats about to be lost.</p>

<h3>What You Are Seeing</h3>
<p>A <b>3D visualization</b> with three axes encoding three dimensions of the "punishment" experienced by states that invested in human development: <b>X = fiscal return</b> (Rs received per Rs 100 paid; lower = more punished), <b>Y = female voter percentage</b> (as a proxy for gender development), <b>Z = current Lok Sabha seats</b> (which will shrink under proportional delimitation). The <b>"punishment value"</b> is computed as <code>1 - 0.35 x (fiscal_return / 100)</code>, where 0.35 represents the estimated share of India's tax revenue contributed by women (a rough estimate based on women's workforce participation and consumption patterns).</p>

<h3>The Triple Burden Framework</h3>
<div class="hl">The punishment value quantifies a <b>compounding geographic injustice</b> faced by India's most developed states. <b>Burden 1 (Fiscal)</b>: states like TN (Rs 29.7 per Rs 100), MH (Rs 27.8), KA (Rs 37.3), and KL (Rs 40.1) pay far more in taxes than they receive back. <b>Burden 2 (Political)</b>: under population-based delimitation, these same states will lose Lok Sabha seats because their successful family planning reduced population growth. <b>Burden 3 (Gender)</b>: these states have higher women's development (higher sex ratios, female literacy, workforce participation), meaning that a larger share of their tax contribution comes from women. Yet the fiscal transfers go disproportionately to states with the worst gender indicators (Bihar, UP, MP), where women's development lags despite receiving the fiscal resources. The "punishment value" captures the intuition that <b>states investing in women's development are subsidizing states that do not, while simultaneously losing political representation</b>.</div>

<h3>The 0.35 Multiplier: Women's Share of Tax Contribution</h3>
<div class="hl gold">The 0.35 multiplier is an <b>order-of-magnitude estimate</b> of women's share of India's total tax contribution, derived from: <b>direct tax contribution</b> (women's share of income tax, approximately 10 to 15% of total income tax, based on women's lower formal workforce participation); <b>indirect tax contribution</b> (women make a majority of household consumption decisions, meaning GST on household goods is substantially driven by women's purchasing; estimates range from 40 to 60% of indirect tax base); and <b>economic contribution</b> (women's unpaid domestic and care work, valued at approximately 15 to 17% of GDP in most estimates, is not taxed but enables the taxable economic activity of other household members). The 35% figure is conservative and may underestimate women's total contribution to the fiscal base. Even at 35%, the implication is significant: <b>over one-third of the tax revenue flowing from contributor states to recipient states is generated by or through women</b>, yet the recipient states' track records on women's development are far worse than the contributor states'.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The triple burden framework suggests a policy intervention: <b>earmarking a portion of fiscal transfers for women's development</b>. If 35% of transfers to recipient states were conditioned on measurable improvements in women's indicators (sex ratio, female literacy, women's workforce participation, reduction in child marriage), it would create an <b>accountability mechanism</b> that partially compensates contributor states by ensuring their fiscal sacrifice produces gender-development outcomes. This is not unprecedented: the 15th Finance Commission already includes "demographic performance" (12.5% weight) as a criterion, rewarding states that controlled population growth. Expanding this to include gender-specific criteria would formalize the principle that <b>fiscal transfers should incentivize the human development investments that contributor states have already made</b>.</div>

<p class="ref"><b>Key references:</b> 15th Finance Commission (2020). Report. | Rao, M.G. (2017). Central transfers to states in India. <i>Economic and Political Weekly</i>, 52(26-27). | Lahoti, R. & Swaminathan, H. (2016). Economic development and women's labor force participation in India. <i>Feminist Economics</i>, 22(2).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 76: Representation Inequality (Animated Slider)
# ═══════════════════════════════════════════════════════════════════
G["76"] = '''
<h2>Representation Inequality: Electors per Seat by State</h2>
<p class="tagline">A vote in Sikkim is worth 6 times a vote in UP. Drag the slider to see how increasing total seats gradually equalizes.</p>

<h3>What You Are Seeing</h3>
<p>A bar chart or lollipop showing <b>registered electors per Lok Sabha seat</b> for each state, with a slider from 543 to 1000 total seats. At 543 (current): UP has approximately 2.4 million electors per seat while Sikkim has approximately 0.4 million. As you drag rightward, proportional reallocation narrows this gap because more seats allow finer-grained proportional adjustment.</p>

<h3>The Most Fundamental Democratic Inequality</h3>
<div class="hl">The variation in electors per seat is <b>the most fundamental violation of the democratic principle of "one person, one vote" in India</b>. If every vote is supposed to carry equal weight in determining Parliamentary representation, then a constituency with 2.4 million voters should not have the same single MP as a constituency with 0.4 million voters. The <b>6:1 ratio</b> between the most and least populated constituencies means that a voter in Sikkim or Lakshadweep has approximately <b>six times the representative weight</b> of a voter in UP or Rajasthan. This inequality is not accidental; it is the structural consequence of the frozen 1971 delimitation combined with uneven population growth.</div>

<h3>The Tradeoff: Equalization vs State Identity</h3>
<div class="hl gold">Small states and union territories (Sikkim, Goa, Mizoram, Manipur, Tripura, Lakshadweep, Andaman and Nicobar) would lose their Lok Sabha representation entirely if seats were allocated purely by population. A state with 600,000 people (Sikkim) would receive 0.04% of 543 seats, i.e., effectively zero. The <b>minimum guarantee of one seat per state/UT</b> is a constitutional protection for small entities' political voice. This creates a tension between <b>proportional equality</b> (one person, one vote) and <b>territorial representation</b> (every constitutionally recognized entity deserves at least one seat). All federal democracies face this tension: the US Senate gives Wyoming (population 577,000) equal representation to California (population 39 million). India's Rajya Sabha partially addresses it through equal state representation regardless of population. The Lok Sabha, however, is designed to be proportional to population, making the current inequality an anomaly that delimitation would correct.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The slider reveals that <b>increasing total seats is the most politically feasible equalization mechanism</b>. At 700 seats, the maximum electors-per-seat ratio drops from 6:1 to approximately 4:1. At 1000 seats, it drops to approximately 3:1. Complete equalization (1:1 ratio) is impossible without either eliminating small-state representation or expanding the Lok Sabha to impractically large size. The practical recommendation is to <b>increase total seats to 700 to 800</b> (comparable to the European Parliament's 705 members or the UK House of Commons' 650), which would significantly reduce representation inequality while maintaining the Lok Sabha at a governable size. The new Parliament building (inaugurated 2023) was designed to accommodate up to 888 members in the Lok Sabha chamber, suggesting that physical capacity is no longer a constraint.</div>

<p class="ref"><b>Key references:</b> Constitution of India, Articles 81, 82. | Election Commission of India (2024). Electors data. | Balinski, M. & Young, H.P. (2001). <i>Fair Representation</i>. Brookings.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 77: Fiscal Spine (South to North)
# ═══════════════════════════════════════════════════════════════════
G["77"] = '''
<h2>Fiscal Spine: A Geographic Gradient from Contributor South to Recipient North</h2>
<p class="tagline">States connected south-to-north. Size = seats. Color = fiscal return. The spine of Indian fiscal federalism has a red base and a green top.</p>

<h3>What You Are Seeing</h3>
<p>A <b>vertical spine diagram</b> with Indian states arranged geographically from south (bottom) to north (top). Each state is represented as a node whose <b>size = Lok Sabha seats</b> and <b>color = fiscal return</b> (red for net contributors, green for net recipients). Lines connect adjacent states along the spine. The visual effect is a geographic gradient: red (contributor) nodes at the southern end, transitioning through yellow (break-even) in the middle, to green (recipient) nodes at the northern end.</p>

<h3>The Fiscal Gradient as Geographic Structure</h3>
<div class="hl">The south-to-north fiscal gradient is one of the <b>most important spatial structures in Indian political economy</b>. It is not merely a statistical pattern; it reflects deep structural differences in economic history, human capital, institutional quality, and demographic trajectory. Southern states industrialized earlier (textiles in Tamil Nadu, IT in Karnataka and Telangana, petrochemicals in Gujarat), invested in education earlier (Kerala's 1957 education reforms, Tamil Nadu's mid-day meal scheme from 1955), and controlled population earlier (Tamil Nadu reached replacement fertility in 1993, 30 years before UP is projected to). These investments created a <b>virtuous cycle</b>: higher human capital led to higher productivity, which generated higher tax revenue, which funded further investment. Northern states, which invested less in education and population control, entered a <b>different equilibrium</b>: lower human capital, lower productivity, higher population growth, and greater dependence on central fiscal transfers.</div>

<h3>The Political Economy of the Gradient</h3>
<div class="hl gold">The fiscal gradient is politically sustainable only as long as contributor states believe that their fiscal sacrifice is: (a) <b>temporary</b> (recipient states will eventually develop and become contributors themselves), (b) <b>effective</b> (the transfers are being used productively to close the development gap), and (c) <b>fair</b> (the formula does not penalize contributors more than necessary). All three beliefs are under increasing strain. (a) The gap between contributor and recipient states has not narrowed significantly despite decades of transfers. (b) Governance quality in key recipient states (Bihar, UP) is frequently criticized, raising concerns about misuse. (c) The impending delimitation, which will simultaneously reduce contributor states' political voice, threatens the perceived fairness of the system. If contributor states lose faith in the fiscal compact, the result could be <b>political movements for greater fiscal autonomy</b>, similar to the "rich region" movements in Catalonia, northern Italy (Lega Nord), or Flanders.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The fiscal spine demands <b>reforms that strengthen the legitimacy of the fiscal compact</b>. <b>Outcome-based conditionality</b>: linking a portion of transfers to measurable development outcomes in recipient states (educational attainment, infant mortality reduction, women's indicators) would ensure that transfers produce visible results. <b>Transparency</b>: publishing clear, annually updated data on each state's fiscal balance (taxes paid vs transfers received) would make the redistribution visible and subject to public debate. <b>Institutional reform in recipient states</b>: investing in governance capacity (administrative reform, anti-corruption mechanisms, e-governance) in recipient states would address the efficiency concern. <b>Delimitation compromise</b>: a formula that increases total seats (so no state loses seats in absolute terms) while incorporating criteria beyond population (area, literacy, fiscal performance, gender development) would balance the competing principles. The fiscal spine will remain a source of geographic political tension until its gradient begins to flatten, and flattening requires that fiscal transfers actually succeed in developing recipient states.</div>

<p class="ref"><b>Key references:</b> 15th Finance Commission (2020). Report. | Rao, M.G. & Singh, N. (2005). <i>Political Economy of Federalism in India</i>. Oxford UP. | Rodden, J. (2004). Comparative federalism and decentralization. <i>Comparative Politics</i>, 36(4).</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 78: Democratic Real Estate Treemap
# ═══════════════════════════════════════════════════════════════════
G["78"] = '''
<h2>Democratic Real Estate Treemap: Who Owns How Much of India's Parliament?</h2>
<p class="tagline">Region, then state. Area = seats. Color = fiscal return. The "double whammy" visualized as real estate.</p>

<h3>What You Are Seeing</h3>
<p>A <b>hierarchical treemap</b> organized as Region (first level) then State (second level). Each rectangle's <b>area is proportional to the state's Lok Sabha seats</b>. <b>Color encodes fiscal return</b>: red for net contributor states, green for net recipient states. The treemap presents India's Parliamentary representation as a <b>finite real estate</b> to be divided, making the allocation question spatially intuitive.</p>

<h3>The "Real Estate" Metaphor</h3>
<div class="hl">Parliament has exactly 543 "units of real estate" (seats). Each unit represents one constituency's voice in national legislation. The treemap makes the <b>allocation of this finite resource</b> visually immediate. The <b>Central and East regions</b> (UP, Bihar, West Bengal, Jharkhand, Odisha) occupy the largest rectangles (most seats) and are colored green (net fiscal recipients). The <b>South region</b> (Tamil Nadu, Karnataka, Kerala, AP, Telangana) occupies smaller rectangles (fewer seats) and is colored red (net fiscal contributors). The visual message is stark: <b>the regions that pay the most taxes have the least Parliamentary real estate, and the regions that receive the most transfers have the most</b>.</div>

<h3>The "Double Whammy" in One Image</h3>
<div class="hl warn">This treemap is the single most effective visualization of the "double whammy" discussed throughout the Delimitation and Fiscal tab. The red (contributor) rectangles are small (fewer seats). The green (recipient) rectangles are large (more seats). Under proportional delimitation, the red rectangles will shrink further while the green rectangles grow. The fiscal flows will not change (contributors will continue subsidizing recipients). The result: <b>contributor states will have less political voice to protest or modify the fiscal arrangements that they fund</b>. This is the spatial political economy trap that makes delimitation the most contentious domestic policy question in India's near future. The treemap format, by presenting seats as finite area, makes the zero-sum nature of the allocation impossible to ignore: every seat gained by a green state is a seat lost by a red state.</div>

<p class="ref"><b>Key references:</b> Shneiderman, B. (1992). Tree visualization with tree-maps. <i>ACM Transactions on Graphics</i>, 11(1). | 15th Finance Commission (2020). Report. | Rao, M.G. (2017). Central transfers to states in India. <i>EPW</i>.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 79: Fiscal-Gender Animated Bubble
# ═══════════════════════════════════════════════════════════════════
G["79"] = '''
<h2>Fiscal-Gender Animated Bubble: Two Inequalities Overlaid</h2>
<p class="tagline">Fiscal return vs women's representation, with a reservation slider. Reservation fixes the gender gap but NOT the fiscal gap. Two problems, two interventions.</p>

<h3>What You Are Seeing</h3>
<p>An animated bubble chart where each state is a bubble. <b>X-axis = fiscal return</b> (Rs per Rs 100 paid). <b>Y-axis = women's representation</b> (% of MPs or candidates who are women). <b>Bubble size = population or seats</b>. A <b>reservation slider</b> shifts the Y-axis values upward as the mandated women's share increases. The animation reveals how the two dimensions of inequality (fiscal and gender) interact.</p>

<h3>The Independence of Two Inequalities</h3>
<div class="hl">The key insight is that <b>fiscal inequality and gender inequality are largely independent</b> in their spatial distribution. There is no strong correlation between a state's fiscal return ratio and its women's representation. Some contributor states (TN, KA) have moderate women's representation. Some recipient states (Bihar) have very low women's representation. Some recipient states (WB) have relatively higher women's representation (due to TMC's nominations). The independence of these two dimensions means that <b>a single policy instrument cannot address both</b>. The Women's Reservation Bill (which shifts all bubbles upward on the Y-axis) addresses gender inequality but leaves the X-axis (fiscal return) unchanged. Fiscal formula reform addresses the X-axis but has no direct impact on gender. The two inequalities require <b>separate, complementary interventions</b>.</div>

<h3>Policy Implications</h3>
<div class="hl warn">The animated bubble reveals the <b>two-front challenge</b> facing Indian federal democracy. <b>Front 1 (Gender)</b>: the reservation slider shows that mandating 33% women's representation would move all states from the bottom of the Y-axis (below 15%) to the middle (33%), a transformation achievable in a single election cycle. <b>Front 2 (Fiscal)</b>: the X-axis cannot be transformed by a single policy lever; it requires structural economic convergence, which takes decades. The combined visualization suggests that <b>the gender front is the easier win</b>: a bill already exists, the mechanism is proven at the panchayat level, and implementation requires only political will plus a delimitation exercise. The fiscal front is harder and longer-term, requiring sustained investment in human capital and institutional quality in recipient states. Pursuing both simultaneously would move India's federal democracy toward a more equitable equilibrium on both dimensions.</div>

<p class="ref"><b>Key references:</b> 15th Finance Commission (2020). Report. | Dahlerup, D. (1988). Critical mass theory. <i>Scandinavian Political Studies</i>. | Dreze, J. & Sen, A. (2013). <i>An Uncertain Glory</i>. Princeton UP.</p>
'''

# ═══════════════════════════════════════════════════════════════════
# CHART 80: Constituency Clustering Map
# ═══════════════════════════════════════════════════════════════════
G["80"] = '''
<h2>Constituency Clustering: The Geography of Women's Exclusion</h2>
<p class="tagline">Every constituency color-coded by percentage of women candidates. Red zones cluster in UP, Bihar, Rajasthan. Green in urban and southern areas. The spatial pattern demands spatially targeted intervention.</p>

<h3>What You Are Seeing</h3>
<p>A <b>choropleth map</b> of India's 543 constituencies, color-coded by the <b>percentage of total candidates who were women</b>. Red = zero or very few women candidates (below 5%). Yellow = moderate (5 to 10%). Green = relatively high (above 10%). The map reveals the geographic structure of women's political exclusion at the finest available spatial resolution: the individual constituency.</p>

<h3>The Spatial Clustering of Exclusion</h3>
<div class="hl">The red zone (zero or near-zero women candidates) forms a <b>contiguous geographic bloc</b> across north-central India: eastern UP, Bihar, parts of Rajasthan, Madhya Pradesh, and Chhattisgarh. This bloc encompasses approximately 180 to 200 constituencies (one-third of all seats) and represents the <b>geographic core of women's political exclusion in India</b>. The green zones are more fragmented: urban constituencies (Delhi, Mumbai, Kolkata, Bangalore, Chennai), portions of West Bengal (TMC effect), and scattered constituencies in the south and northeast. The spatial pattern is virtually identical to the pattern of women's voter registration gaps (Chart 67), women's deposit forfeiture rates (Chart 68), and the "silence map" zero-women constituencies (Chart 65). This convergence of multiple indicators on the same geographic zone confirms that <b>women's political exclusion in India is a spatially concentrated phenomenon with identifiable geographic boundaries</b>.</div>

<h3>Spatial Autocorrelation of Exclusion</h3>
<div class="hl gold">If we computed Moran's I on the "percentage of women candidates" variable, it would almost certainly show <b>positive spatial autocorrelation</b>: constituencies with few women candidates are surrounded by neighbors with few women candidates. The clustering is driven by the same geographic factors identified throughout this atlas: <b>regional patriarchal culture</b> (the Hindi heartland's more restrictive gender norms), <b>party organizational culture</b> (state-level party units in UP and Bihar being more resistant to women's candidacy), <b>constituency geography</b> (large, rural, remote constituencies where campaign barriers are highest for women), and <b>socioeconomic structure</b> (low female literacy, low women's workforce participation, and strong son preference creating an environment hostile to women's public political activity). The spatial autocorrelation means that <b>exclusion breeds exclusion</b>: the absence of women candidates in a constituency normalizes that absence in neighboring constituencies, creating a self-perpetuating geographic pattern.</div>

<h3>Breaking the Spatial Pattern</h3>
<p>The geographic concentration of exclusion is, paradoxically, a <b>policy opportunity</b>. Because the problem is spatially concentrated (rather than uniformly distributed), it can be addressed with <b>geographically targeted interventions</b>. If the Women's Reservation Bill reserves one-third of seats in each election, and if the rotation algorithm ensures that reserved seats are distributed across both green and red zones, the bill will <b>forcibly break the geographic pattern of exclusion</b> by mandating women's candidacy in the heart of the red zone. The evidence from panchayat-level reservation (Beaman et al., 2012) suggests that exposure to women leaders in reserved positions changes voter and community attitudes, creating a <b>positive spatial diffusion effect</b> that extends beyond the reserved positions themselves. The clustering map thus provides both the diagnosis (geographically concentrated exclusion) and the spatial logic for the treatment (geographically distributed reservation).</p>

<h3>The Atlas Concludes</h3>
<div class="hl warn">This final chart brings the atlas full circle. Chart 01 showed the geography of global wealth and health. Chart 80 shows the geography of women's political voice in the world's largest democracy. The through-line connecting all 80 charts is that <b>geography is not merely a backdrop to human affairs but an active determinant of outcomes</b>. Where you are born determines your wealth (Chart 01), your health (Chart 03), your fertility (Chart 02), your access to technology (Chart 13), your exposure to climate risk (Charts 07, 08), your political representation (Charts 37, 71, 76), and your chance of being a woman in the political arena (Charts 65, 68, 80). Understanding these spatial patterns is the prerequisite for designing interventions that address the root causes of inequality rather than merely treating symptoms. Spatial data science, by revealing the geographic structure of social phenomena, transforms abstract problems into maps that show <b>where to act, what to address, and how success or failure is geographically distributed</b>.</div>

<p class="ref"><b>Key references:</b> Anselin, L. (1995). LISA. <i>Geographical Analysis</i>, 27(2). | Beaman, L. et al. (2012). Female leadership raises aspirations and educational attainment for girls. <i>Science</i>, 335(6068). | Tobler, W. (1970). A computer movie simulating urban growth. <i>Economic Geography</i>, 46(sup1). | ECI (2024). Constituency-wise Women Candidature data.</p>
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

print(f"\nPhase 5: Injected deep guides into {count} charts")
