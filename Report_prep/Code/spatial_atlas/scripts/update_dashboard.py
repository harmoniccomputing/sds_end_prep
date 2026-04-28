#!/usr/bin/env python3
"""Update the main dashboard to add quad-panel tab, chart index link, and update stats."""

fpath = "/home/claude/rosling_project/visualizations/index.html"
with open(fpath, "r") as f:
    html = f.read()

# 1. Update stats: 80 -> 81 charts, 11 -> 13 themes
html = html.replace('<div class="sv">80</div>', '<div class="sv">81</div>', 1)
html = html.replace('<div class="sv">11</div>', '<div class="sv">13</div>', 1)
html = html.replace('64 interactive visualizations', '81 interactive visualizations')

# 2. Add new tab button for "Synchronized" after the immersive tab
old_tab = '<button class="tb" onclick="sw(\'immersive\')" id="b-immersive"><span class="ti">&#127922;</span><span class="tl">3D Immersive</span><span class="tc">13</span></button>'
new_tabs = old_tab + '\n<button class="tb" onclick="sw(\'sync\')" id="b-sync"><span class="ti">&#128260;</span><span class="tl">Synchronized</span><span class="tc">1</span></button>'
html = html.replace(old_tab, new_tabs)

# 3. Add the synchronized panel before the Sources footer
sync_panel = """<div class="tp" id="p-sync" style="display:none;flex-direction:column"><div class="ph"><div class="pi" style="background:#00D5E022;color:#00D5E0">&#128260;</div><div><h2>Synchronized Multi-View</h2><p class="pd">Four coordinated panels driven by a single timeline. Different chart types, different datasets, one story.</p></div></div><div class="cg2">
<div class="cd" onclick="op('81_quad_panel_sync.html')" style="animation-delay:0.00s"><div class="cs" style="background:#00D5E0"></div><div class="cb"><div class="ct"><span class="cn">81</span><span class="cg">Quad-Panel</span></div><h3>Four Lenses on Global Development</h3><p class="dp">Bubble chart (GDP vs Life Exp) + World choropleth (fertility) + Stacked area (continental population) + Continental trajectory (fertility vs child mortality). All synchronized via single year slider 1990-2023. Play/pause with speed control. Mathematical framework: Preston Curve, Hagerstrand diffusion, demographic transition, Tobler's First Law.</p><div class="ca">Open chart &rarr;</div></div></div>
</div></div>
"""

# Insert before the Sources footer
html = html.replace('<div class="sf"><h3>Sources</h3>', sync_panel + '<div class="sf"><h3>Sources</h3>')

# 4. Add chart index link in the Sources footer area (before closing </div> of sf)
index_link = ' | <b style="color:#FFD700">&#128218; <a href="chart_index.html" style="color:#FFD700">Complete Chart Index (all 81 charts grouped by topic)</a></b>'
html = html.replace('Tropical Underdevelopment</p></div>', 'Tropical Underdevelopment' + index_link + '</p></div>')

with open(fpath, "w") as f:
    f.write(html)

print(f"Dashboard updated: {len(html)/1024:.1f} KB")
print("Added: Synchronized tab, quad-panel card, chart index link")
