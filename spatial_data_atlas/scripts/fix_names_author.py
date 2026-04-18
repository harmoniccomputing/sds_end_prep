#!/usr/bin/env python3
"""
1. Remove person names from descriptive text (keep only in citations/references)
2. Add 'Vishakha Agrawal' as author across all pages
"""
import os, re

VIS = "/home/claude/rosling_project/visualizations"

changes = []

# ===== FIX 1: guided_tour.html =====
fpath = os.path.join(VIS, "guided_tour.html")
with open(fpath, "r") as f:
    content = f.read()

# Fix tour stop 1 title and desc
content = content.replace(
    'title: "The Rosling Classic: Wealth vs Health"',
    'title: "The Animated Classic: Wealth vs Health"'
)
content = content.replace(
    "This is the visualization that changed how the world sees data, first animated by Hans Rosling in 2006. Each bubble is a nation.",
    "This is the visualization that changed how the world sees data. Each bubble is a nation."
)

# Add author to splash
content = content.replace(
    '<div class="splash-eyebrow">Lab for Spatial Informatics, IIIT Hyderabad</div>',
    '<div class="splash-eyebrow">By Vishakha Agrawal | Lab for Spatial Informatics, IIIT Hyderabad</div>'
)

with open(fpath, "w") as f:
    f.write(content)
changes.append("guided_tour.html: fixed title, removed name from desc, added author")

# ===== FIX 2: 06_income_distribution_shift.html =====
fpath = os.path.join(VIS, "06_income_distribution_shift.html")
with open(fpath, "r") as f:
    content = f.read()

content = content.replace(
    "Hans Rosling famously used this chart to argue that the \"developing world\" is a misleading concept: there is no longer a discrete cluster of poor nations separated from a discrete cluster of rich ones.",
    "This shift demonstrates that the \"developing world\" is a misleading concept: there is no longer a discrete cluster of poor nations separated from a discrete cluster of rich ones."
)

with open(fpath, "w") as f:
    f.write(content)
changes.append("06: removed Hans Rosling from description text")

# ===== FIX 3: 49_gdp_bar_race.html =====
fpath = os.path.join(VIS, "49_gdp_bar_race.html")
with open(fpath, "r") as f:
    content = f.read()

content = content.replace(
    "Hans Rosling repeatedly cautioned against the \"race\" metaphor for development: countries are not competing for a fixed prize but navigating distinct structural transformations at different speeds.",
    "Development researchers have cautioned against the \"race\" metaphor: countries are not competing for a fixed prize but navigating distinct structural transformations at different speeds."
)

with open(fpath, "w") as f:
    f.write(content)
changes.append("49: removed Hans Rosling from description text")

# ===== FIX 4: Add author to ALL chart pages =====
# Insert <meta name="author"> and a small footer credit line
author_meta = '<meta name="author" content="Vishakha Agrawal">'

for fname in sorted(os.listdir(VIS)):
    if not fname.endswith(".html"):
        continue
    fpath = os.path.join(VIS, fname)
    with open(fpath, "r") as f:
        content = f.read()
    
    modified = False
    
    # Add meta author tag if not present
    if 'name="author"' not in content:
        if "<head>" in content:
            content = content.replace("<head>", f"<head>\n{author_meta}", 1)
            modified = True
        elif "<head" in content:
            # head tag with attributes
            idx = content.find(">", content.find("<head"))
            if idx > 0:
                content = content[:idx+1] + f"\n{author_meta}" + content[idx+1:]
                modified = True
        elif "<title>" in content.lower():
            # No explicit head, insert before title
            ti = content.lower().find("<title>")
            content = content[:ti] + f"{author_meta}\n" + content[ti:]
            modified = True
    
    if modified:
        with open(fpath, "w") as f:
            f.write(content)

changes.append(f"All HTML: added <meta author='Vishakha Agrawal'>")

# ===== FIX 5: Add author to dashboard header =====
fpath = os.path.join(VIS, "index.html")
with open(fpath, "r") as f:
    content = f.read()

if "Vishakha Agrawal" not in content:
    content = content.replace(
        '<p class="af">Lab for Spatial Informatics, IIIT Hyderabad</p>',
        '<p class="af">By Vishakha Agrawal | Lab for Spatial Informatics, IIIT Hyderabad</p>'
    )
    with open(fpath, "w") as f:
        f.write(content)
    changes.append("index.html: added author to header")

# ===== FIX 6: Add author to chart_index.html =====
fpath = os.path.join(VIS, "chart_index.html")
with open(fpath, "r") as f:
    content = f.read()

if "Vishakha Agrawal" not in content:
    content = content.replace(
        "Lab for Spatial Informatics, IIIT Hyderabad. All",
        "By Vishakha Agrawal | Lab for Spatial Informatics, IIIT Hyderabad. All"
    )
    with open(fpath, "w") as f:
        f.write(content)
    changes.append("chart_index.html: added author")

# ===== VERIFY: No remaining non-citation name references =====
print("CHANGES MADE:")
for c in changes:
    print(f"  {c}")

print("\nVERIFICATION: Checking for remaining non-citation name references...")

problem_files = []
for fname in sorted(os.listdir(VIS)):
    if not fname.endswith(".html"):
        continue
    fpath = os.path.join(VIS, fname)
    with open(fpath, "r") as f:
        content = f.read()
    
    # Find "Hans Rosling" outside of reference blocks
    lines = content.split("\n")
    for i, line in enumerate(lines):
        lower = line.lower()
        # Skip reference/citation lines
        if any(x in lower for x in ['class="ref"', 'key ref', 'references:', 'bibliography']):
            continue
        # Check for "Hans Rosling" (the problematic casual usage)
        if "Hans Rosling" in line:
            problem_files.append((fname, i+1, "Hans Rosling in non-ref context"))

if problem_files:
    print("  REMAINING ISSUES:")
    for f, line, issue in problem_files:
        print(f"    {f}:{line} - {issue}")
else:
    print("  All non-citation name references removed: OK")

# Check author presence
author_count = 0
for fname in sorted(os.listdir(VIS)):
    if not fname.endswith(".html"):
        continue
    with open(os.path.join(VIS, fname), "r") as f:
        if 'Vishakha Agrawal' in f.read():
            author_count += 1

html_count = sum(1 for f in os.listdir(VIS) if f.endswith(".html"))
print(f"\n  Author 'Vishakha Agrawal' present in: {author_count}/{html_count} HTML files")
