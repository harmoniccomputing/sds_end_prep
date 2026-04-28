#!/usr/bin/env python3
"""Add proper <title> tags to all charts that are missing them."""
import os, re

VIS_DIR = "/home/claude/rosling_project/visualizations"

TITLES = {
    "01": "GDP vs Life Expectancy (Animated Bubble Chart)",
    "02": "Fertility vs Life Expectancy (Animated Bubble Chart)",
    "03": "Child Mortality vs GDP (Animated Bubble Chart)",
    "04": "Country Development Trajectories",
    "05": "Continental Development Trends",
    "06": "Income Distribution Shift (Animated)",
    "07": "Coral Bleaching Risk Map",
    "08": "Ocean SST Anomaly Map",
    "09": "Global Urbanization Choropleth",
    "10": "Slum Population Distribution",
    "11": "Extreme Poverty Map",
    "12": "GINI Inequality Coefficient Map",
    "13": "Internet Usage Choropleth",
    "14": "Electricity Access Map",
    "15": "Mobile Subscriptions per 100 People",
    "16": "GDP per Capita World Map",
    "17": "Trade Openness Index Map",
    "18": "Remittances as % of GDP",
    "19": "Forest Cover Percentage Map",
    "20": "Renewable Energy Share Map",
    "21": "Water Stress Index Map",
    "22": "GDP-Health Bubble Map",
    "23": "Latitude vs GDP per Capita",
    "24": "Megacity Distance vs Life Expectancy",
    "25": "Latitude vs Child Mortality",
    "26": "Conflict Intensity vs Human Development",
    "27": "Landlocked vs Coastal Nations",
    "28": "Digital Divide by Latitude",
    "29": "Fertility Rate by Climate Zone",
    "30": "Urbanization vs Renewable Energy",
    "31": "Water Stress by Latitude",
    "32": "Physicians per 1000 by Latitude",
    "33": "Education vs Megacity Distance",
    "34": "Trade Openness by Longitude",
    "35": "Maternal Mortality vs Forest Cover",
    "36": "Remittances by Latitude",
    "37": "India Election LISA Clusters (Turnout)",
    "38": "Constituency Area vs Electoral Outcomes",
    "39": "Moran Scatterplot (Spatial Autocorrelation)",
    "40": "Turnout-Swing Spatial Analysis",
    "41": "Distance from Delhi vs Victory Margin",
    "42": "India Political Cylinder (3D)",
    "43": "Development Globe (3D)",
    "44": "Democracy-Development Helix (3D)",
    "45": "Continental Development Space (3D)",
    "46": "Women Candidates vs Area Hypothesis",
    "47": "3D Extruded India Map",
    "48": "Alliance LISA & Women Analysis",
    "49": "GDP Bar Race (1990-2023)",
    "50": "India Electoral Swing Animation",
    "51": "Fertility Rate Collapse (Animated)",
    "52": "Child Mortality Plunge (Animated)",
    "53": "Economic Convergence Race (Animated)",
    "54": "Women LISA Spatial Animation",
    "55": "India Party Flip 3D",
    "56": "Development Spiral (3D)",
    "57": "Coral Bleaching Temporal Pulse (Animated)",
    "58": "Animated Inequality (Gini Over Time)",
    "59": "India Development Terrain (3D)",
    "60": "India Food Geography (3D)",
    "61": "Literacy-Gender Helix (3D)",
    "62": "Constituency Aurora Visualization (3D)",
    "63": "India Socioeconomic Landscape (3D)",
    "64": "Gender-Development 3D Surface",
    "65": "The Silence Map (Zero Women Constituencies)",
    "66": "The Gauntlet (Women Candidate Funnel)",
    "67": "Gender Gap in Electorate",
    "68": "Deposit Forfeiture Analysis",
    "69": "State Gender Scoreboard (Heatmap)",
    "70": "Women Candidature 3D Landscape",
    "71": "Delimitation Simulator",
    "72": "Fiscal Returns by State",
    "73": "Reservation Impact Simulator",
    "74": "Moran Criteria Explorer",
    "75": "Punishment Value 3D Surface",
    "76": "Representation Inequality (Lorenz Curve)",
    "77": "Fiscal Spine Chart",
    "78": "Representation Treemap",
    "79": "Fiscal-Gender Bubble Chart",
    "80": "Constituency Clustering (k-Means)",
}

fixed = 0
for fname in os.listdir(VIS_DIR):
    if not fname.endswith(".html") or fname == "index.html":
        continue
    chart_id = fname.split("_")[0]
    if chart_id not in TITLES:
        continue
    
    fpath = os.path.join(VIS_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "<title>" in content.lower():
        continue
    
    title = TITLES[chart_id]
    # Insert title after <head> or after <html>
    if "<head>" in content:
        content = content.replace("<head>", f"<head>\n<title>{title} | Spatial Atlas</title>", 1)
    elif "<html>" in content:
        content = content.replace("<html>", f"<html>\n<head><title>{title} | Spatial Atlas</title></head>", 1)
    elif "<html" in content:
        # Has attributes on html tag
        idx = content.find(">", content.find("<html"))
        if idx > 0:
            content = content[:idx+1] + f"\n<head><title>{title} | Spatial Atlas</title></head>" + content[idx+1:]
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    fixed += 1

print(f"Fixed {fixed} charts with missing <title> tags")
