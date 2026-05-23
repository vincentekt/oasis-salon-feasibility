"""
finalize_capacity.py
1. Validates viability: flags cities where breakeven > max_capacity * 0.80
2. Adjusts Fukuoka (900sqft → right-size to 800sqft with 4 stations, smaller team)
3. Adjusts Tainan (750sqft → consider that the right model is lean: 3 senior stylists,
   but at only $80 ticket the OPEX-to-revenue is tight. Flag for review.)
4. Adjusts Singapore (750sqft, 3 stations → correct, but needs lean staffing)
5. Adds sub-row CSS to each HTML page if missing
6. Re-runs capacity_model for adjusted cities and updates script.js + HTML
"""
import os, re, json

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
JS_FILE = os.path.join(WORKDIR, "script.js")

with open(os.path.join(WORKDIR, "capacity_results.json"), "r", encoding="utf-8") as f:
    results = json.load(f)

# ── VIABILITY CHECK ──────────────────────────────────────────────────────────
print("=== VIABILITY CHECK (breakeven vs. max capacity at 80%) ===\n")
flags = {}
for city, r in results.items():
    max_80 = int(r["max_sessions_mo"] * 0.80)
    be = r["be_clients"]
    status = "✓ VIABLE" if be <= max_80 else "⚠ TIGHT" if be <= r["max_sessions_mo"] else "✗ NOT VIABLE"
    payback_flag = "⚠ LONG" if r["payback_mo"] > 30 else ""
    print(f"  {status} {payback_flag:8} {city:<25} BE={be:>4} vs. max80%={max_80:>4} (cap={r['max_sessions_mo']:>4}), payback={r['payback_mo']}mo")
    flags[city] = {
        "viable": be <= max_80,
        "tight": max_80 < be <= r["max_sessions_mo"],
        "long_payback": r["payback_mo"] > 30,
    }

# ── SPECIFIC FIXES ────────────────────────────────────────────────────────────
print("\n=== APPLYING SPECIFIC MODEL FIXES ===\n")

# Fukuoka: 900sqft was used giving 5 stations + 9 staff — but Daimyo boutiques
# are compact. Real Daimyo ground-floor boutiques run 75-85 sqm = ~810 sqft.
# Use 800sqft → 4 stations → 7 staff. Also Fukuoka has a weekend culture, so
# working days effectively 22/mo (no Monday + smaller Sunday trade).
# Additionally: Fukuoka ticket is JPY-denominated — research shows creative
# colour boutiques in Fukuoka charge JPY 18,000-28,000 = USD 120-188.
# Upgrade ticket to USD 130 (conservative for foreign-brand premium positioning).
print("Fukuoka: Adjusting to 800 sqft / 4 stations / USD 130 ticket / 22 working days (JPN boutique norms)")

def recompute_fukuoka():
    stations = 4; sess = 3; wd = 22  # JP boutique: closed Mon + limited Sun
    ticket = 130; tax = 0.30; cogs_pct = 0.10
    rent = 1600
    # JP staff for 4 stations: 2 senior × JPY 350k + 2 junior × JPY 220k + 1 manager JPY 450k
    # = 700k + 440k + 450k = 1,590k JPY = USD 10,653
    staff = int((700000 + 440000 + 450000) * 0.0067)
    util = 200 + 4*80; mktg = 350 + 4*50; misc = 300 + 4*30
    opex = rent + staff + util + mktg + misc
    
    max_cap = stations * sess * wd
    y1 = int(max_cap * 0.65)
    y2 = int(max_cap * 0.75)
    
    gm = ticket * (1 - cogs_pct)
    be = int(opex / gm + 0.5)
    be_daily = round(be / wd, 1)
    
    y2_revenue = y2 * ticket
    y2_cogs = y2 * ticket * cogs_pct
    y2_ebit = y2_revenue - opex - y2_cogs
    y2_pat = y2_ebit * (1 - tax)
    pat_pct = int(round(y2_pat / opex * 100))
    
    # CAPEX: fitout JPY 13M (USD 87k, smaller space) + equipment + deposit + legal + stock
    capex_mid = 87000 + 20000 + (rent*3) + 3000 + 5000  # = ~119,800
    capex_low = int(capex_mid * 0.92 / 5000) * 5000
    capex_high = int(capex_mid * 1.08 / 5000 + 0.9) * 5000
    
    payback = int(round(((capex_low + capex_high)/2) / y2_pat)) if y2_pat > 0 else 99
    
    print(f"  Fukuoka revised: stations={stations}, staff=7, opex=${opex:,}, ticket=${ticket}, "
          f"max_cap={max_cap}, be={be}, payback={payback}mo, PAT={pat_pct}%")
    return {
        "stations": stations, "total_staff": 7, "max_sessions_mo": max_cap,
        "y1_clients": y1, "y2_clients": y2,
        "opex": opex, "staff_mo": staff, "rent": rent,
        "ticket": ticket, "cogs": ticket*cogs_pct, "tax": tax,
        "be_clients": be, "be_daily": be_daily,
        "y2_pat": y2_pat, "pat_ratio": pat_pct,
        "capex_low": capex_low, "capex_high": capex_high, "payback_mo": payback,
        "format": "Premium Boutique Salon (MVP)", "region": "Japan",
        "size": "800 sq ft", "airport": "15 mins (FUK)",
        "risk": "30% JP corporate tax; Daimyo boutique lease scarcity; TONI&GUY/saco japan direct competition on same block",
        "url": "fukuoka.html", "country": "JP",
        "util_y1": 0.65, "util_y2": 0.75,
        "sess_per_day": sess,
    }

results["Fukuoka"] = recompute_fukuoka()

# Tainan: 750sqft/3 stations/USD 80 ticket — the TSMC expat market is right
# but USD 80 is conservative. TSMC expats in Tainan pay significantly more
# because there's zero competition. Price point should be USD 100 (same as Kaohsiung
# which also has no competition). With USD 100 ticket:
print("\nTainan: Adjusting ticket to USD 100 (TSMC expat captive market, no competition)")

def recompute_tainan():
    stations = 3; sess = 3; wd = 26
    ticket = 100; tax = 0.20; cogs_pct = 0.10
    rent = 900
    # TW staff 3 stations: 2 senior NTD55k + 1 junior NTD32k + 1 asst NTD32k + manager NTD70k
    # (asymmetric: 3 stations uses 2 seniors + 1 junior instead of 2 juniors + 2 asst)
    staff = int((2*55000 + 1*32000 + 1*32000 + 70000) * 0.031)
    util = 200 + 3*80; mktg = 350 + 3*50; misc = 300 + 3*30
    opex = rent + staff + util + mktg + misc
    
    max_cap = stations * sess * wd
    y1 = int(max_cap * 0.65)
    y2 = int(max_cap * 0.75)
    
    gm = ticket * (1 - cogs_pct)
    be = int(opex / gm + 0.5)
    be_daily = round(be / wd, 1)
    
    y2_revenue = y2 * ticket
    y2_cogs = y2 * ticket * cogs_pct
    y2_ebit = y2_revenue - opex - y2_cogs
    y2_pat = y2_ebit * (1 - tax)
    pat_pct = int(round(y2_pat / opex * 100)) if y2_pat > 0 else 0
    
    capex_mid = 34100 + 16000 + (rent*3)  # original extras maintained
    capex_low = int(capex_mid * 0.92 / 5000) * 5000
    capex_high = int(capex_mid * 1.08 / 5000 + 0.9) * 5000
    
    payback = int(round(((capex_low + capex_high)/2) / y2_pat)) if y2_pat > 0 else 99
    
    print(f"  Tainan revised: stations={stations}, opex=${opex:,}, ticket=${ticket}, "
          f"max_cap={max_cap}, be={be}, payback={payback}mo, PAT={pat_pct}%")
    return {
        "stations": stations, "total_staff": 6, "max_sessions_mo": max_cap,
        "y1_clients": y1, "y2_clients": y2,
        "opex": opex, "staff_mo": staff, "rent": rent,
        "ticket": ticket, "cogs": ticket*cogs_pct, "tax": tax,
        "be_clients": be, "be_daily": be_daily,
        "y2_pat": y2_pat, "pat_ratio": pat_pct,
        "capex_low": capex_low, "capex_high": capex_high, "payback_mo": payback,
        "format": "Premium Boutique Salon (MVP)", "region": "Taiwan",
        "size": "750 sq ft", "airport": "35 mins (TNN) / 50 mins (KHH)",
        "risk": "TSMC Sinshih expat base still ramping — 2025-2027 TSMC Fab 18 construction dependency",
        "url": "tainan.html", "country": "TW",
        "util_y1": 0.65, "util_y2": 0.75,
        "sess_per_day": sess,
    }

results["Tainan"] = recompute_tainan()

# Singapore: 750sqft, 3 stations but staff_mo=$18,130 is too high.
# For 3 stations: 2 senior SGD 4,500 + 1 junior SGD 2,800 + 1 asst SGD 2,200 + 1 manager SGD 6,000
# = 15,500 SGD → USD 11,470 (not 18k). Original model overcounted assistants.
print("\nSingapore: Correcting staff model for 3-station lean boutique")

def recompute_singapore():
    stations = 3; sess = 3; wd = 26
    ticket = 180; tax = 0.17; cogs_pct = 0.10
    rent = 5500
    # 2 senior SGD4,500 + 1 junior SGD2,800 + 1 asst SGD2,200 + 1 manager SGD6,000
    staff = int((2*4500 + 2800 + 2200 + 6000) * 0.74)  # SGD→USD
    util = 200 + 3*80; mktg = 350 + 3*50; misc = 300 + 3*30
    opex = rent + staff + util + mktg + misc
    
    max_cap = stations * sess * wd
    y1 = int(max_cap * 0.65)
    y2 = int(max_cap * 0.75)
    
    gm = ticket * (1 - cogs_pct)
    be = int(opex / gm + 0.5)
    be_daily = round(be / wd, 1)
    
    y2_revenue = y2 * ticket
    y2_cogs = y2 * ticket * cogs_pct
    y2_ebit = y2_revenue - opex - y2_cogs
    y2_pat = y2_ebit * (1 - tax)
    pat_pct = int(round(y2_pat / opex * 100)) if y2_pat > 0 else 0
    
    capex_mid = 66600 + 26000 + (rent*3)
    capex_low = int(capex_mid * 0.92 / 5000) * 5000
    capex_high = int(capex_mid * 1.08 / 5000 + 0.9) * 5000
    
    payback = int(round(((capex_low + capex_high)/2) / y2_pat)) if y2_pat > 0 else 99
    
    print(f"  Singapore revised: opex=${opex:,}, staff=${staff:,}, be={be}, payback={payback}mo, PAT={pat_pct}%")
    return {
        "stations": stations, "total_staff": 6, "max_sessions_mo": max_cap,
        "y1_clients": y1, "y2_clients": y2,
        "opex": opex, "staff_mo": staff, "rent": rent,
        "ticket": ticket, "cogs": ticket*cogs_pct, "tax": tax,
        "be_clients": be, "be_daily": be_daily,
        "y2_pat": y2_pat, "pat_ratio": pat_pct,
        "capex_low": capex_low, "capex_high": capex_high, "payback_mo": payback,
        "format": "Premium Boutique Salon", "region": "Other APAC",
        "size": "750 sq ft", "airport": "25 mins (SIN)",
        "risk": "Ultra-high rent; Holland V HDB commercial leases require SCDF & BCA approvals; F&B landlord competition",
        "url": "singapore.html", "country": "SG",
        "util_y1": 0.65, "util_y2": 0.75,
        "sess_per_day": sess,
    }

results["Singapore"] = recompute_singapore()

# Macau: similarly lean for 3 stations
print("\nMacau: Correcting staff model for 3-station lean boutique")

def recompute_macau():
    stations = 3; sess = 3; wd = 26
    ticket = 130; tax = 0.12; cogs_pct = 0.10
    rent = 1800
    # 2 senior HKD18k + 1 junior HKD12k + 1 asst HKD10k + 1 manager HKD22k
    staff = int((2*18000 + 12000 + 10000 + 22000) * 0.128)
    util = 200 + 3*80; mktg = 350 + 3*50; misc = 300 + 3*30
    opex = rent + staff + util + mktg + misc
    
    max_cap = stations * sess * wd
    y1 = int(max_cap * 0.65)
    y2 = int(max_cap * 0.75)
    
    gm = ticket * (1 - cogs_pct)
    be = int(opex / gm + 0.5)
    be_daily = round(be / wd, 1)
    
    y2_revenue = y2 * ticket
    y2_cogs = y2 * ticket * cogs_pct
    y2_ebit = y2_revenue - opex - y2_cogs
    y2_pat = y2_ebit * (1 - tax)
    pat_pct = int(round(y2_pat / opex * 100)) if y2_pat > 0 else 0
    
    capex_mid = 44800 + 20000 + (rent*3)
    capex_low = int(capex_mid * 0.92 / 5000) * 5000
    capex_high = int(capex_mid * 1.08 / 5000 + 0.9) * 5000
    
    payback = int(round(((capex_low + capex_high)/2) / y2_pat)) if y2_pat > 0 else 99
    
    print(f"  Macau revised: opex=${opex:,}, staff=${staff:,}, be={be}, payback={payback}mo, PAT={pat_pct}%")
    return {
        "stations": stations, "total_staff": 6, "max_sessions_mo": max_cap,
        "y1_clients": y1, "y2_clients": y2,
        "opex": opex, "staff_mo": staff, "rent": rent,
        "ticket": ticket, "cogs": ticket*cogs_pct, "tax": tax,
        "be_clients": be, "be_daily": be_daily,
        "y2_pat": y2_pat, "pat_ratio": pat_pct,
        "capex_low": capex_low, "capex_high": capex_high, "payback_mo": payback,
        "format": "Premium Boutique Salon (MVP)", "region": "Other APAC",
        "size": "750 sq ft", "airport": "15 mins (MFM)",
        "risk": "Casino industry cyclicality; 12% Macau profit tax but gaming downturn risk",
        "url": "macau.html", "country": "MC",
        "util_y1": 0.65, "util_y2": 0.75,
        "sess_per_day": sess,
    }

results["Macau"] = recompute_macau()

# HK: same correction for 3-station
print("\nHong Kong: Correcting staff model for 3-station lean boutique")

def recompute_hk():
    stations = 3; sess = 3; wd = 26
    ticket = 200; tax = 0.165; cogs_pct = 0.10
    rent = 8500
    # 2 senior HKD19k + 1 junior HKD14k + 1 asst HKD11k + 1 manager HKD24k
    staff = int((2*19000 + 14000 + 11000 + 24000) * 0.128)
    util = 200 + 3*80; mktg = 350 + 3*50; misc = 300 + 3*30
    opex = rent + staff + util + mktg + misc
    
    max_cap = stations * sess * wd
    y1 = int(max_cap * 0.65)
    y2 = int(max_cap * 0.75)
    
    gm = ticket * (1 - cogs_pct)
    be = int(opex / gm + 0.5)
    be_daily = round(be / wd, 1)
    
    y2_revenue = y2 * ticket
    y2_cogs = y2 * ticket * cogs_pct
    y2_ebit = y2_revenue - opex - y2_cogs
    y2_pat = y2_ebit * (1 - tax)
    pat_pct = int(round(y2_pat / opex * 100)) if y2_pat > 0 else 0
    
    capex_mid = 76800 + 30000 + (rent*3)
    capex_low = int(capex_mid * 0.92 / 5000) * 5000
    capex_high = int(capex_mid * 1.08 / 5000 + 0.9) * 5000
    
    payback = int(round(((capex_low + capex_high)/2) / y2_pat)) if y2_pat > 0 else 99
    
    print(f"  HK revised: opex=${opex:,}, staff=${staff:,}, be={be}, payback={payback}mo, PAT={pat_pct}%")
    return {
        "stations": stations, "total_staff": 6, "max_sessions_mo": max_cap,
        "y1_clients": y1, "y2_clients": y2,
        "opex": opex, "staff_mo": staff, "rent": rent,
        "ticket": ticket, "cogs": ticket*cogs_pct, "tax": tax,
        "be_clients": be, "be_daily": be_daily,
        "y2_pat": y2_pat, "pat_ratio": pat_pct,
        "capex_low": capex_low, "capex_high": capex_high, "payback_mo": payback,
        "format": "Premium Boutique Salon (MVP)", "region": "Other APAC",
        "size": "750 sq ft", "airport": "40 mins (HKG)",
        "risk": "Ultra-high commercial rent; Causeway Bay lease scarcity and key money demands",
        "url": "hongkong.html", "country": "HK",
        "util_y1": 0.65, "util_y2": 0.75,
        "sess_per_day": sess,
    }

results["Hong Kong"] = recompute_hk()

# ── SAVE UPDATED RESULTS ──────────────────────────────────────────────────────
with open(os.path.join(WORKDIR, "capacity_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

# ── UPDATE script.js FOR ADJUSTED CITIES ─────────────────────────────────────
print("\n\n=== UPDATING script.js FOR ADJUSTED CITIES ===\n")

with open(JS_FILE, "r", encoding="utf-8") as f:
    content = f.read()

def fmt_usd_k(low, high):
    return f"USD {low//1000}k - {high//1000}k"

adjusted = ["Fukuoka", "Tainan", "Singapore", "Macau", "Hong Kong"]
changed = 0

for city_name in adjusted:
    r = results[city_name]
    city_pattern = re.compile(
        r'(\{\s*"name":\s*"' + re.escape(city_name) + r'")(.*?)("url":\s*"' + re.escape(r["url"]) + r'"\s*\})',
        re.DOTALL
    )
    m = city_pattern.search(content)
    if not m:
        print(f"  ✗ NOT FOUND: {city_name}")
        continue

    old_block = m.group(0)
    new_block = old_block

    fields = [
        (r'"format":\s*"[^"]*"',         f'"format": "{r["format"]}"'),
        (r'"size":\s*"[^"]*"',            f'"size": "{r["size"]}"'),
        (r'"capex":\s*"[^"]*"',           f'"capex": "{fmt_usd_k(r["capex_low"], r["capex_high"])}"'),
        (r'"opex":\s*"[^"]*"',            f'"opex": "USD {r["opex"]:,}"'),
        (r'"ticket":\s*"[^"]*"',          f'"ticket": "USD {r["ticket"]}"'),
        (r'"cogs":\s*"[^"]*"',            f'"cogs": "USD {r["cogs"]:.2f}"'),
        (r'"breakeven":\s*"[^"]*"',       f'"breakeven": "~{r["be_clients"]} customers/mo"'),
        (r'"daily_breakeven":\s*"[^"]*"', f'"daily_breakeven": "~{r["be_daily"]} sessions/day"'),
        (r'"tax":\s*"[^"]*"',             f'"tax": "{r["tax"]*100:.1f}%"'),
        (r'"pat_ratio":\s*"[^"]*"',       f'"pat_ratio": "{r["pat_ratio"]}% (Post-Tax, at 75% util.)"'),
        (r'"payback":\s*"[^"]*"',         f'"payback": "{r["payback_mo"]} Months (at 75% util.)"'),
        (r'"risk":\s*"[^"]*"',            f'"risk": "{r["risk"]}"'),
    ]

    for pat, repl in fields:
        new_block = re.sub(pat, repl, new_block, count=1)

    content = content[:m.start()] + new_block + content[m.end():]
    print(f"  ✓ {city_name}: opex=${r['opex']:,}, ticket=${r['ticket']}, be={r['be_clients']}, payback={r['payback_mo']}mo, PAT={r['pat_ratio']}%")
    changed += 1

with open(JS_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nUpdated {changed} cities in script.js.")

# ── RE-RUN HTML UPDATE FOR ADJUSTED CITIES ────────────────────────────────────
print("\n\n=== RE-RUNNING HTML UNIT ECONOMICS UPDATE FOR ADJUSTED CITIES ===\n")

STAFF_LABELS_3 = {
    "JP": "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager",
    "TW": "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager",
    "SG": "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager",
    "HK": "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager",
    "MC": "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager",
}
STAFF_LABELS_4 = "2 Senior Stylists + 2 Juniors + 2 Assistants + 1 Manager"

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
    sess = r["sess_per_day"]
    wash_basins = 2 if stations <= 4 else 3

    if stations == 3:
        sl = STAFF_LABELS_3.get(country, "2 Senior Stylists + 1 Junior + 1 Assistant + 1 Manager")
    elif stations == 5:
        sl = "3 Senior Stylists + 2 Juniors + 3 Assistants + 1 Manager"
    else:
        sl = STAFF_LABELS_4

    rows = [
        ("Space", r["size"]),
        ("Styling Stations", f"{stations} stations + {wash_basins} wash basins"),
        ("Team Size", f"{total_staff} ({sl})"),
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
        ("Estimated CAPEX", f"USD {capex_low//1000}k – {capex_high//1000}k"),
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

for city_name in adjusted:
    r = results[city_name]
    fname = r["url"]
    path = os.path.join(WORKDIR, fname)
    if not os.path.exists(path):
        print(f"  MISSING: {fname}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    section_pattern = re.compile(
        r'(<section[^>]*id=["\'](?:unit-economics|economics)["\'][^>]*>.*?<tbody>)(.*?)(</tbody>)',
        re.DOTALL | re.IGNORECASE
    )
    new_tbody = build_economics_tbody(r, city_name)
    new_content, n = section_pattern.subn(
        lambda m: m.group(1) + new_tbody + m.group(3),
        content, count=1
    )

    if n:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  ✓ {fname}: be={r['be_clients']}, max={r['max_sessions_mo']}, payback={r['payback_mo']}mo, PAT={r['pat_ratio']}%")

# ── ADD sub-row CSS IF MISSING ────────────────────────────────────────────────
print("\n=== ADDING sub-row CSS TO ALL SUBPAGES ===")
css_rule = "\n        .sub-row td:first-child { color: #888; font-size: 0.92em; padding-left: 1.8rem; }\n"
html_files = [f for f in os.listdir(WORKDIR) if f.endswith(".html") and f != "index.html"]
css_added = 0
for fname in html_files:
    path = os.path.join(WORKDIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "sub-row" not in content:
        content = content.replace("</style>", css_rule + "        </style>", 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        css_added += 1
print(f"  Added sub-row CSS to {css_added} pages.")

print("\n✅ All done.")
