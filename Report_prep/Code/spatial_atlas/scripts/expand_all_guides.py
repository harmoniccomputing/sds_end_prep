#!/usr/bin/env python3
"""Expand all 76 remaining chart guides to benchmark academic depth."""
import os, re, json

VIZ_DIR = "visualizations"

CSS_BLOCK = '''<!--ATLAS-GUIDE-START-->
<style>
.guide{position:relative;z-index:1;background:#080B13;padding:36px 5% 50px;color:#C8D0DA;
font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif;font-size:.84rem;line-height:1.75;border-top:2px solid #151d2e}
.guide-inner{max-width:1100px;margin:0 auto}
.guide h2{color:#00D5E0;font-size:1.15rem;font-weight:700;margin:0 0 4px;font-family:'Playfair Display',Georgia,serif}
.guide .tagline{color:#FF5872;font-size:.92rem;font-weight:600;margin:0 0 16px;font-style:italic}
.guide h3{color:#FFD700;font-size:.88rem;font-weight:700;margin:22px 0 6px;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid #1a2233;padding-bottom:4px}
.guide p{margin:0 0 10px;color:#B8C4D0;text-align:justify}
.guide .hl{background:#0f1520;border-left:3px solid #00D5E0;padding:12px 16px;margin:10px 0;border-radius:0 6px 6px 0}
.guide .warn{border-left-color:#FF5872}.guide .gold{border-left-color:#FFD700}.guide .insight{border-left-color:#B10DC9}
.guide b{color:#E8ECF0}.guide em{color:#FFD700;font-style:normal}
.guide code{background:#1C2333;padding:1px 6px;border-radius:3px;font-size:.76rem;color:#00D5E0}
.guide .cols{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin:10px 0}
@media(max-width:900px){.guide .cols{grid-template-columns:1fr}}
.guide .cols>div{background:#0c1018;border-radius:6px;padding:14px 16px;border:1px solid #151d2e}
.guide .cols h4{color:#00D5E0;font-size:.8rem;margin:0 0 6px;font-weight:700}
</style>
'''

END_BLOCK = '<!--ATLAS-GUIDE-END-->'

def inject(filepath, body):
    html = open(filepath).read()
    if 'ATLAS-GUIDE-START' in html:
        return False
    block = CSS_BLOCK + '<div class="guide"><div class="guide-inner">\n' + body + '\n</div></div>\n' + END_BLOCK + '\n'
    html = html.replace("</body>", block + "</body>") if "</body>" in html else html + block
    open(filepath, 'w').write(html)
    return True

# Load annotation content from external JSON-like structure
# I'll define all 76 guides inline

GUIDES = {}

GUIDES["02"] = '''<h2>Fertility vs Longevity: The Demographic Transition in Motion</h2>
<p class="tagline">The most consequential transformation in human history, compressed into 33 seconds of animation.</p>

<h3>What You Are Seeing</h3>
<p>Each bubble is one country. <b>X-axis: Fertility Rate</b> (total births per woman over her lifetime at current age-specific rates). <b>Y-axis: Life Expectancy</b> at birth. <b>Bubble size</b> = population. <b>Color</b> = continent. The animation slider steps through 1990-2023.</p>

<h3>Understanding the Key Threshold: 2.1</h3>
<div class="hl">The <em>replacement fertility rate</em> is 2.1 births per woman. Below this, a population shrinks without immigration. The 0.1 accounts for child mortality (not every girl born survives to reproductive age). When a country's bubble crosses leftward past the 2.1 line, it has entered a phase of <b>eventual population decline</b>. Japan (1.2), South Korea (0.7), Italy (1.2), and Spain (1.1) are already there. China (1.0) crossed below replacement around 2020, with profound implications for global economic power.</div>

<h3>The Science: Demographic Transition Theory</h3>
<p>The movement from upper-left to lower-right follows the <b>Demographic Transition Model</b> (Thompson 1929, Notestein 1945), the most empirically validated theory in demography. It describes four stages: <b>Stage 1</b> (pre-modern): high birth and death rates, population stable. <b>Stage 2</b> (early transition): death rates fall (sanitation, medicine), birth rates remain high, population explodes. <b>Stage 3</b> (late transition): birth rates fall (urbanization, women's education, contraception), growth slows. <b>Stage 4</b> (post-transition): both rates low, population stable or declining. Most of Sub-Saharan Africa is currently in Stage 2-3. Europe and East Asia are in Stage 4.</p>
<p>The <b>causal mechanisms</b> driving fertility decline are: (1) <b>child survival</b>: when parents are confident their children will survive, they have fewer (Caldwell 1982); (2) <b>women's education</b>: each additional year of female secondary schooling reduces fertility by 0.3-0.5 births (UNESCO 2022); (3) <b>contraceptive access</b>: unmet need for family planning remains ~25% in Sub-Saharan Africa; (4) <b>urbanization</b>: in rural agrarian economies, children are economic assets (farm labor). In cities, children are economic costs (education, housing, food). The rural-to-urban transition is thus a fertility transition.</p>

<h3>Spatial and Geographic Patterns</h3>
<div class="hl gold">The animation reveals a <b>geographic wave of demographic transition</b>. Europe and East Asia completed the transition first (1960s-1990s). Latin America and South Asia followed (1980s-2010s). Sub-Saharan Africa is the last major region to enter, with the transition accelerating post-2000. Within Africa, the spatial pattern is instructive: <b>coastal and southern Africa</b> (South Africa, Kenya, Ghana) are further along than <b>Sahelian and Central Africa</b> (Niger, Chad, DRC, Mali). This follows the broader development gradient visible in Charts 23 (latitude-wealth) and 25 (climate-mortality): the tropical core faces compounding disadvantages.</div>

<h3>Anthropological Significance</h3>
<p>For 99% of human existence, women spent most of their adult lives in a cycle of pregnancy, breastfeeding, and childcare. The fertility decline visible in this animation represents a <b>fundamental change in the human experience of womanhood</b>. In post-transition societies, women spend less than 10% of their adult years bearing and nursing children, freeing time and energy for education, professional work, political participation, and personal development. This is not merely a demographic statistic; it is a transformation of gender relations with implications for every domain of human life.</p>

<h3>Policy Implications</h3>
<div class="hl warn"><b>For high-fertility countries</b> (upper-left): the highest-return investment is <em>girls' secondary education</em>. This reliably reduces fertility, improves maternal and child health, increases household income, and strengthens democratic participation. One year of additional female schooling reduces fertility by 0.3-0.5 births. The cost per year of secondary schooling in Sub-Saharan Africa is approximately $300-500. The return (in reduced population growth, improved health, and increased GDP) is estimated at 10-15x the investment. <b>For low-fertility countries</b> (lower-right): policies include subsidized childcare, parental leave, housing support, and immigration to offset labor shortages. But evidence suggests that once fertility drops below ~1.5, it is very difficult to raise again (the "low-fertility trap" hypothesis, Lutz et al. 2006).</div>'''

GUIDES["03"] = '''<h2>Child Mortality vs Wealth: The Most Important Graph in Global Health</h2>
<p class="tagline">Every dot moving downward represents thousands of children who survived to their fifth birthday.</p>

<h3>What You Are Seeing</h3>
<p><b>Y-axis: Under-5 Mortality Rate</b> (deaths per 1,000 live births before age 5). A value of 200 means 1 in 5 children dies. Below 10 is the developed-world norm. <b>X-axis: GDP per Capita (PPP, log scale)</b>. <b>Bubble size</b> = population. Animation: 1990-2023.</p>

<h3>Understanding the Log Scale</h3>
<div class="hl">The X-axis uses a <b>logarithmic transformation</b>: each gridline represents a 10x increase in income ($100, $1,000, $10,000, $100,000). This is not just a visual convenience. The relationship between income and child mortality is genuinely logarithmic: the <b>first doubling of income</b> (from $500 to $1,000) reduces mortality by roughly 40-50 deaths per 1,000. The <b>tenth doubling</b> (from $50,000 to $100,000) reduces it by perhaps 0.5. A linear scale would compress all low-income countries into an unreadable strip on the left while wasting space on the flat right portion of the curve. The log scale gives equal visual weight to equal <em>proportional</em> changes in income.</div>

<h3>The Mechanisms: Why Wealth Saves Children</h3>
<div class="cols">
<div><h4>Direct Pathways</h4>
<p><b>Nutrition</b>: wealthier families can afford diverse diets with adequate protein, iron, zinc, and vitamin A. Malnutrition underlies 45% of child deaths. <b>Clean water and sanitation</b>: wealthier communities can build and maintain water treatment and sewage systems. Diarrheal disease (caused by contaminated water) kills ~500,000 children/year. <b>Healthcare access</b>: wealthier countries fund hospitals, train doctors, and subsidize medicines. Pneumonia (treatable with $0.50 of antibiotics) kills ~800,000 children/year simply because treatment is not available in time.</p></div>
<div><h4>Indirect Pathways</h4>
<p><b>Maternal education</b>: wealthier societies educate women, who then make better health decisions for their children (handwashing, oral rehydration, vaccination compliance). <b>Infrastructure</b>: roads enable emergency transport to hospitals. Electricity enables vaccine cold chains. Mobile networks enable health information campaigns. <b>Governance</b>: wealthier countries can fund public health systems, regulatory agencies, and disease surveillance.</p></div>
</div>

<h3>The Exceptional Countries</h3>
<div class="hl gold"><b>Bangladesh</b> achieves under-5 mortality of ~27 per 1,000 with a GDP of only ~$8,000, far below what the curve predicts. This is the result of decades of investment in community health workers (BRAC's 100,000-strong cadre), oral rehydration therapy (invented in Dhaka in the 1970s), and aggressive vaccination campaigns. <b>Rwanda</b> achieved similar results post-genocide through a performance-based healthcare financing system that pays clinics per patient treated. <b>Equatorial Guinea</b>, conversely, has high GDP (~$16,000, from oil) but under-5 mortality of ~80, because oil wealth is concentrated among elites and has not been translated into public health investment. These outliers prove that <b>wealth is neither necessary nor sufficient</b> for child survival; it is the <em>allocation</em> of resources that matters.</div>

<h3>The Spatial Pattern of Child Death</h3>
<p>The remaining high-mortality countries cluster in two geographic zones: (1) the <b>Sahel belt</b> (Mali, Niger, Chad, Burkina Faso, Nigeria), where drought, food insecurity, and weak state capacity compound health challenges, and (2) <b>conflict zones</b> (Yemen, Somalia, South Sudan, DRC), where active violence destroys health infrastructure and displaces populations. Both zones are characterized by <b>spatial isolation</b>: long distances between settlements, few paved roads, and limited telecommunications, making it physically difficult to deliver healthcare.</p>

<h3>Policy Implications</h3>
<div class="hl warn">The <b>Millennium Development Goals</b> (2000-2015) set a target of reducing child mortality by two-thirds. The world fell short but made extraordinary progress: under-5 deaths fell from 12.7 million/year (1990) to 5.0 million (2023). The acceleration post-2000 proves that <b>coordinated international goals with funding commitments work</b>. The most cost-effective interventions (per DALY saved) are: (1) childhood vaccination (~$10-15 per DALY), (2) oral rehydration salts + zinc for diarrhea (~$25/DALY), (3) insecticide-treated bed nets for malaria (~$30/DALY), (4) breastfeeding promotion (~$50/DALY). Policymakers in high-mortality countries should fund these in this order before investing in expensive tertiary care.</div>'''

# Save to temp file and continue in next cell due to size
with open('/tmp/guides_02_03.json', 'w') as f:
    json.dump(GUIDES, f)
print(f"Phase 1 built: {len(GUIDES)} guides")
