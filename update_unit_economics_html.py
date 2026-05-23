"""
update_unit_economics_html.py
Updates the Unit Economics section in each subpage with capacity-driven numbers.
Also fixes staffing: smaller salons (3 stations) don't need as many people.
"""
import os, re, json

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

# Load computed results
with open(os.path.join(WORKDIR, "capacity_results.json"), "r", encoding="utf-8") as f:
    results = json.load(f)

# ── STAFFING LABELS ───────────────────────────────────────────────────────────
STAFF_LABELS = {
    "VN": {
        3: "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager",
        4: "2 Senior Stylists + 2 Juniors + 2 Assistants + 1 Manager",
        5: "3 Senior Stylists + 2 Juniors + 3 Assistants + 1 Manager",
    },
    "MY": {
        3: "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager",
        4: "2 Senior Stylists + 2 Juniors + 2 Assistants + 1 Manager",
        5: "3 Senior Stylists + 2 Juniors + 3 Assistants + 1 Manager",
    },
    "SG": {
        3: "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager",
        4: "2 Senior Stylists + 2 Juniors + 2 Assistants + 1 Manager",
        5: "3 Senior Stylists + 2 Juniors + 3 Assistants + 1 Manager",
    },
    "HK": {
        3: "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager",
        4: "2 Senior Stylists + 2 Juniors + 2 Assistants + 1 Manager",
    },
    "MC": {
        3: "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager",
    },
    "TH": {
        4: "2 Senior Stylists + 2 Juniors + 2 Assistants + 1 Manager",
    },
    "TW": {
        3: "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager",
        4: "2 Senior Stylists + 2 Juniors + 2 Assistants + 1 Manager",
    },
    "JP": {
        4: "2 Senior Stylists + 2 Juniors + 2 Assistants + 1 Manager",
        5: "3 Senior Stylists + 2 Juniors + 3 Assistants + 1 Manager",
    },
    "KR": {
        4: "2 Senior Stylists + 2 Juniors + 2 Assistants + 1 Manager",
    },
    "AU": {
        4: "2 Senior Stylists + 2 Juniors + 2 Assistants + 1 Manager (Part-Time)",
        5: "3 Senior Stylists + 2 Juniors + 3 Assistants + 1 Manager",
    },
    "AE": {
        4: "2 Senior Stylists + 2 Juniors + 2 Assistants + 1 Manager",
    },
}

def get_staff_label(country, stations):
    labels = STAFF_LABELS.get(country, {})
    return labels.get(stations, f"{stations} Stylists + Assistants + 1 Manager")

def get_session_desc(sess_per_day, stations):
    return f"{sess_per_day} sessions/station/day × {stations} stations × 26 days"

def fmt_capex(low, high):
    return f"USD {low//1000}k – {high//1000}k"

def fmt_money(v):
    return f"USD {v:,}"

# ── BUILD HTML TBODY FOR UNIT ECONOMICS TABLE ─────────────────────────────────
# Matches the structure used in subpages: table with rows like
# <tr><td>Label</td><td>Value</td></tr>
# We'll replace the content between markers

def build_economics_tbody(r, city_name):
    stations = r["stations"]
    total_staff = r["total_staff"]
    country = r["country"]
    max_cap = r["max_sessions_mo"]
    y1 = r["y1_clients"]
    y2 = r["y2_clients"]
    be = r["be_clients"]
    be_daily = r["be_daily"]
    opex = r["opex"]
    staff = r["staff_mo"]
    rent = r["rent"]
    ticket = r["ticket"]
    cogs = r["cogs"]
    pat_pct = r["pat_ratio"]
    payback = r["payback_mo"]
    capex_low = r["capex_low"]
    capex_high = r["capex_high"]
    tax_pct = int(r["tax"] * 100)
    util_y1 = int(r["util_y1"] * 100)
    util_y2 = int(r["util_y2"] * 100)
    y2_pat = r["y2_pat"]
    sess_per_day = r["sess_per_day"]

    staff_label = get_staff_label(country, stations)
    session_desc = get_session_desc(sess_per_day, stations)
    wash_basins = 2 if stations <= 4 else 3

    rows = [
        ("Space", r["size"]),
        ("Styling Stations", f"{stations} stations + {wash_basins} wash basins"),
        ("Team Size", f"{total_staff} ({staff_label})"),
        ("Session Capacity", f"{max_cap} sessions/month (max at 100%)"),
        (f"Operating Clients (Year 1 — {util_y1}% util.)", f"{y1} clients/month"),
        (f"Operating Clients (Year 2 — {util_y2}% util.)", f"{y2} clients/month"),
        ("Break-Even Volume", f"~{be} clients/month (~{be_daily} sessions/day)"),
        ("Average Ticket", f"USD {ticket}"),
        ("COGS per Session (10%)", f"USD {cogs:.2f}"),
        ("Gross Margin per Session", f"USD {ticket - cogs:.2f} (90%)"),
        ("Monthly OPEX (Total)", f"USD {opex:,}"),
        ("  → Rent", f"USD {rent:,}"),
        ("  → Staff & Payroll", f"USD {staff:,}"),
        ("  → Utilities + Marketing + Misc", f"USD {opex - rent - staff:,}"),
        (f"Monthly PAT at {util_y2}% Utilization (After {tax_pct}% Tax)", f"USD {y2_pat:,.0f}"),
        ("PAT / OPEX Ratio", f"{pat_pct}%"),
        ("Estimated CAPEX", fmt_capex(capex_low, capex_high)),
        (f"Payback Period (at {util_y2}% utilization)", f"~{payback} months"),
    ]

    tbody = "\n"
    for label, value in rows:
        indent = "                                  "
        is_sub = label.startswith("  →")
        row_class = ' class="sub-row"' if is_sub else ''
        tbody += f'{indent}<tr{row_class}>\n'
        tbody += f'{indent}    <td>{label}</td>\n'
        tbody += f'{indent}    <td><strong>{value}</strong></td>\n'
        tbody += f'{indent}</tr>\n'
    return tbody

# ── PROCESS EACH HTML FILE ────────────────────────────────────────────────────
print("=== UPDATING UNIT ECONOMICS TABLES IN ALL SUBPAGES ===\n")
updated = 0

# URL → city name map
url_to_city = {r["url"]: name for name, r in results.items()}

html_files = [f for f in os.listdir(WORKDIR) if f.endswith(".html") and f != "index.html"]

for fname in sorted(html_files):
    if fname not in url_to_city:
        continue
    city_name = url_to_city[fname]
    r = results[city_name]

    path = os.path.join(WORKDIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find section with id="economics" or id="unit-economics"
    # The section contains a table - replace its tbody
    section_pattern = re.compile(
        r'(<section[^>]*id=["\'](?:unit-economics|economics)["\'][^>]*>.*?<tbody>)(.*?)(</tbody>)',
        re.DOTALL | re.IGNORECASE
    )

    new_tbody = build_economics_tbody(r, city_name)
    new_content, n = section_pattern.subn(
        lambda m: m.group(1) + new_tbody + m.group(3),
        content,
        count=1
    )

    if n == 0:
        # Try alternative: look for the economics data table specifically
        # Some pages may have different section IDs
        alt_pattern = re.compile(
            r'(<section[^>]*>.*?<h2[^>]*>[^<]*[Ee]conomics[^<]*</h2>.*?<tbody>)(.*?)(</tbody>)',
            re.DOTALL
        )
        new_content, n = alt_pattern.subn(
            lambda m: m.group(1) + new_tbody + m.group(3),
            content,
            count=1
        )

    if n == 0:
        print(f"  ✗ NO ECONOMICS TABLE FOUND: {fname}")
        continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  ✓ {fname}: {r['stations']} stations, {r['total_staff']} staff, "
          f"breakeven {r['be_clients']} clients, payback {r['payback_mo']}mo")
    updated += 1

print(f"\nDone. {updated}/{len(html_files)} subpages updated.")
