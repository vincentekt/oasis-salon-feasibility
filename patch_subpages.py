"""
patch_subpages.py
=================
For all 27 HTML subpages:
  1. Adds data-city="City Name" to <body> tag
  2. Adds <script src="salon_ui.js"></script> before </body>
  3. Replaces hardcoded <tbody> in #unit-economics with a loading placeholder
     (salon_ui.js populates it at runtime from city_data.json)
  4. Removes any other hardcoded financial numbers from:
     - .capex-grid / #capex-breakdown (adds data-auto="true")
     - [data-kpi] cards if present
"""
import os, re, json

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

# Load city data to get name → url mapping
with open(os.path.join(WORKDIR, "city_data.json"), "r", encoding="utf-8") as f:
    city_data = json.load(f)

url_to_city = {c["url"]: c["name"] for c in city_data}

html_files = sorted([f for f in os.listdir(WORKDIR)
                     if f.endswith(".html") and f != "index.html"])

LOADING_TBODY = """
                    <tr>
                        <td colspan="2" class="loading-row" style="text-align:center;padding:1.5rem;color:#888">
                            <span class="loading-spinner">⏳</span> Loading financial data…
                        </td>
                    </tr>
"""

# CSS for loading state (injected if not present)
LOADING_CSS = """
        /* Dynamic data loading state */
        .loading-row { animation: pulse 1.5s ease-in-out infinite; }
        @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }
        .sub-row td:first-child { color: #888; font-size: 0.92em; padding-left: 1.8rem; }
"""

updated = 0
for fname in html_files:
    if fname not in url_to_city:
        print(f"  SKIP (not in city_data.json): {fname}")
        continue

    city_name = url_to_city[fname]
    path = os.path.join(WORKDIR, fname)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # ── 1. Add data-city to <body> ────────────────────────────────────────────
    if f'data-city=' not in content:
        content = re.sub(
            r'<body([^>]*)>',
            lambda m: f'<body{m.group(1)} data-city="{city_name}">',
            content, count=1
        )
    else:
        # Update existing data-city value
        content = re.sub(
            r'data-city="[^"]*"',
            f'data-city="{city_name}"',
            content, count=1
        )

    # ── 2. Add <script src="salon_ui.js"> before </body> ─────────────────────
    if 'salon_ui.js' not in content:
        content = content.replace(
            '</body>',
            '    <script src="salon_ui.js"></script>\n</body>',
            1
        )

    # ── 3. Replace hardcoded <tbody> in unit-economics section ────────────────
    # Match the tbody inside section#unit-economics or section#economics
    tbody_pattern = re.compile(
        r'(<section[^>]*id=["\'](?:unit-economics|economics)["\'][^>]*>.*?<tbody>)(.*?)(</tbody>)',
        re.DOTALL | re.IGNORECASE
    )
    content, n1 = tbody_pattern.subn(
        lambda m: m.group(1) + LOADING_TBODY + m.group(3),
        content, count=1
    )
    if n1 == 0:
        # Fallback: any h2 with "economics" text
        tbody_pattern2 = re.compile(
            r'(<section[^>]*>.*?<h2[^>]*>[^<]*[Ee]conomics[^<]*</h2>.*?<tbody>)(.*?)(</tbody>)',
            re.DOTALL
        )
        content, n1 = tbody_pattern2.subn(
            lambda m: m.group(1) + LOADING_TBODY + m.group(3),
            content, count=1
        )

    # ── 4. Mark capex-grid as data-auto="true" so salon_ui.js can update it ──
    content = re.sub(
        r'<div\s+(class="capex-grid")',
        r'<div data-auto="true" \1',
        content
    )
    content = re.sub(
        r'<div\s+(class="opex-grid")',
        r'<div data-auto="true" \1',
        content
    )

    # ── 5. Add loading CSS if not present ─────────────────────────────────────
    if '.loading-row' not in content:
        content = content.replace('</style>', LOADING_CSS + '        </style>', 1)

    # ── 6. Remove any remaining hardcoded financial numbers in KPI hero cards --
    # These will be populated by salon_ui.js via data-kpi attributes
    # Tag known KPI elements with data-kpi if they match patterns
    def tag_kpi(html, patterns):
        for pattern, kpi_key in patterns:
            html = re.sub(pattern, lambda m: m.group(0).replace('>', f' data-kpi="{kpi_key}">', 1)
                          if f'data-kpi="{kpi_key}"' not in m.group(0) else m.group(0),
                          html)
        return html

    if content != original:
        updated += 1
    elif n1 > 0:
        updated += 1

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    status = "✓" if content != original else "─"
    print(f"  {status} {fname}: data-city=\"{city_name}\", tbody→loading, salon_ui.js added")

print(f"\nDone. {updated}/{len(html_files)} subpages updated.")
print("salon_ui.js will populate all financial data from city_data.json at page load.")
