"""
excel_to_json.py
================
Reads salon_data.xlsx (Cities + Country sheets) and:
  1. Replicates all Model-sheet formulas in Python (mirrors Excel exactly)
  2. Outputs city_data.json   — consumed by the frontend
  3. Patches script.js        — regenerates the citiesDb block

Run this after any change to salon_data.xlsx.
Usage:
    python excel_to_json.py
    # Optional: python excel_to_json.py --dry-run   (print only, no file writes)
"""

import os, re, json, sys, math
import openpyxl

WORKDIR   = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
XLSX_FILE = os.path.join(WORKDIR, "salon_data.xlsx")
JSON_FILE = os.path.join(WORKDIR, "city_data.json")
JS_FILE   = os.path.join(WORKDIR, "script.js")

DRY_RUN = "--dry-run" in sys.argv

# ── LOAD EXCEL ────────────────────────────────────────────────────────────────
print(f"Reading {XLSX_FILE}...")
wb = openpyxl.load_workbook(XLSX_FILE, data_only=True)

# ── COUNTRY PARAMS (Country sheet, rows 4-14, cols A-H) ──────────────────────
ws_c = wb["Country"]
country_params = {}
for row in ws_c.iter_rows(min_row=4, max_row=20, values_only=True):
    if not row[0]:
        continue
    # Skip non-data rows (e.g. instruction text bled into the sheet)
    try:
        tax_check = float(row[2])
    except (TypeError, ValueError):
        continue
    code = str(row[0]).strip()
    if len(code) > 3:   # safety: country codes are 2-3 chars max
        continue
    country_params[code] = {
        "name":    row[1],
        "tax":     float(row[2]) if row[2] else 0.20,
        "currency":row[3],
        "senior":  float(row[4]) if row[4] else 1500,
        "junior":  float(row[5]) if row[5] else 900,
        "asst":    float(row[6]) if row[6] else 700,
        "manager": float(row[7]) if row[7] else 1800,
    }
print(f"  Loaded {len(country_params)} country records: {list(country_params.keys())}")

# ── CITY INPUTS (Cities sheet, rows 5+, cols A-P) ────────────────────────────
ws_i = wb["Cities"]
city_inputs = []
for row in ws_i.iter_rows(min_row=5, max_row=50, values_only=True):
    if not row[0]:
        continue
    city_inputs.append({
        "name":     str(row[0]).strip(),
        "url":      str(row[1]).strip(),
        "region":   str(row[2]).strip(),
        "country":  str(row[3]).strip(),
        "sqft":     int(row[4]) if row[4] else 800,
        "sess":     int(row[5]) if row[5] else 3,
        "wd":       int(row[6]) if row[6] else 26,
        "ticket":   float(row[7]) if row[7] else 100,
        "cogs_pct": float(row[8]) if row[8] else 0.10,
        "rent":     float(row[9]) if row[9] else 2000,
        "fitout":   float(row[10]) if row[10] else 50000,
        "equip":    float(row[11]) if row[11] else 20000,
        "other":    float(row[12]) if row[12] else 5000,
        "dep_mo":   int(row[13]) if row[13] else 3,
        "util_y1":  float(row[14]) if row[14] else 0.65,
        "util_y2":  float(row[15]) if row[15] else 0.75,
    })
print(f"  Loaded {len(city_inputs)} cities")

# ── MIRRORED MODEL FORMULAS ───────────────────────────────────────────────────
def compute_model(city, cp):
    """Mirrors the Excel Model sheet formulas exactly."""
    sqft    = city["sqft"]
    sess    = city["sess"]
    wd      = city["wd"]
    ticket  = city["ticket"]
    cogs_p  = city["cogs_pct"]
    rent    = city["rent"]
    fitout  = city["fitout"]
    equip   = city["equip"]
    other   = city["other"]
    dep_mo  = city["dep_mo"]
    util_y1 = city["util_y1"]
    util_y2 = city["util_y2"]
    
    # Country rates
    tax     = cp["tax"]
    senior  = cp["senior"]
    junior  = cp["junior"]
    asst    = cp["asst"]
    manager = cp["manager"]
    
    # === SPACE → STAFF ===
    # Stations = IF(sqft<=750,3, IF(sqft<=850,4, 5))
    if sqft <= 750:
        stations = 3
    elif sqft <= 850:
        stations = 4
    else:
        stations = 5
    
    # Wash basins
    wash_basins = 2 if stations <= 4 else 3
    
    # Seniors = IF(stations<=4, 2, 3)
    seniors = 2 if stations <= 4 else 3
    
    # Juniors = stations - seniors
    juniors = stations - seniors
    
    # Assistants = CEILING(stations/2, 1)
    assistants = math.ceil(stations / 2)
    
    # Total Staff = seniors + juniors + assistants + 1 (manager)
    total_staff = seniors + juniors + assistants + 1
    
    # === COUNTRY LOOKUP ===
    # Staff cost = seniors×senior + juniors×junior + assistants×asst + manager
    staff_cost = seniors * senior + juniors * junior + assistants * asst + manager
    
    # === OPEX ===
    utilities  = 200 + stations * 80
    mktg_misc  = 350 + stations * 50 + 300 + stations * 30  # = 650 + stations*80
    total_opex = rent + staff_cost + utilities + mktg_misc
    
    # === CAPACITY ===
    max_cap = stations * sess * wd
    y1_clients = int(max_cap * util_y1)
    y2_clients = int(max_cap * util_y2)
    
    # === UNIT ECONOMICS ===
    cogs_per_session = ticket * cogs_p
    gm_per_session   = ticket - cogs_per_session
    
    # Breakeven = CEILING(opex / gm_per_session, 1)
    breakeven = math.ceil(total_opex / gm_per_session)
    breakeven_daily = round(breakeven / wd, 1)
    
    # Y2 Monthly PAT = (y2_clients × ticket × (1-cogs%) - opex) × (1-tax)
    y2_ebit = y2_clients * ticket * (1 - cogs_p) - total_opex
    y2_pat  = y2_ebit * (1 - tax)
    pat_ratio = round(y2_pat / total_opex * 100) if total_opex > 0 else 0
    
    # === CAPEX ===
    capex_base = fitout + equip + other + rent * dep_mo
    capex_low  = math.floor(capex_base * 0.92 / 5000) * 5000
    capex_high = math.ceil( capex_base * 1.08 / 5000) * 5000
    capex_mid  = (capex_low + capex_high) / 2
    
    # Payback = CEILING(capex_mid / y2_pat, 1) — or 999 if unprofitable
    payback = math.ceil(capex_mid / y2_pat) if y2_pat > 0 else 999
    
    # Viable? = breakeven < 80% of max capacity
    viable = breakeven < max_cap * 0.8
    
    return {
        # Staff
        "stations":      stations,
        "wash_basins":   wash_basins,
        "seniors":       seniors,
        "juniors":       juniors,
        "assistants":    assistants,
        "total_staff":   total_staff,
        # Rates
        "tax":           round(tax, 4),
        # Costs
        "rent":          round(rent),
        "staff_cost":    round(staff_cost),
        "utilities":     round(utilities),
        "mktg_misc":     round(mktg_misc),
        "total_opex":    round(total_opex),
        # Capacity
        "max_cap":       max_cap,
        "y1_clients":    y1_clients,
        "y2_clients":    y2_clients,
        # Economics
        "ticket":        round(ticket, 2),
        "cogs_pct":      round(cogs_p, 4),
        "cogs_session":  round(cogs_per_session, 2),
        "gm_session":    round(gm_per_session, 2),
        "breakeven":     breakeven,
        "be_daily":      breakeven_daily,
        "y2_pat":        round(y2_pat, 2),
        "pat_ratio":     pat_ratio,
        # CAPEX
        "capex_low":     int(capex_low),
        "capex_high":    int(capex_high),
        "capex_mid":     int(capex_mid),
        "payback_mo":    payback,
        # Status
        "viable":        viable,
        "size":          f"{sqft} sq ft",
        "util_y1":       util_y1,
        "util_y2":       util_y2,
        "sess_per_day":  sess,
        "working_days":  wd,
    }

# ── RUN MODEL FOR ALL CITIES ──────────────────────────────────────────────────
print("\nComputing model for all cities:")
print(f"{'City':<22} {'Sta':>4} {'Staff':>6} {'OPEX':>9} {'MaxCap':>7} {'BE':>6} {'Y2 PAT':>9} {'PAT%':>6} {'CAPEX':>14} {'Payback':>8} {'OK?':>6}")
print("-" * 100)

results = {}
for city in city_inputs:
    name = city["name"]
    cp   = country_params.get(city["country"])
    if not cp:
        print(f"  ⚠ Missing country: {city['country']} for {name}")
        continue
    m = compute_model(city, cp)
    results[name] = {**city, **m}
    print(f"{name:<22} {m['stations']:>4} {m['total_staff']:>6} ${m['total_opex']:>8,} "
          f"{m['max_cap']:>7} {m['breakeven']:>6} ${m['y2_pat']:>8,.0f} {m['pat_ratio']:>5}% "
          f"USD{m['capex_low']//1000:>4}k-{m['capex_high']//1000}k {m['payback_mo']:>6}mo "
          f"{'✓' if m['viable'] else '⚠':>6}")

# ── BUILD JSON FOR FRONTEND ────────────────────────────────────────────────────
print(f"\nBuilding city_data.json...")

# Build extra metadata from capacity_results.json (airport, risk, format, etc.)
# to preserve fields not in the Excel (we'll keep those in JSON or add to Excel later)
extra_meta = {}
cr_path = os.path.join(WORKDIR, "capacity_results.json")
if os.path.exists(cr_path):
    with open(cr_path, "r", encoding="utf-8") as f:
        cap_results = json.load(f)
    for cname, cdata in cap_results.items():
        extra_meta[cname] = {
            "airport": cdata.get("airport", ""),
            "risk":    cdata.get("risk", ""),
            "format":  cdata.get("format", ""),
            "region":  cdata.get("region", ""),
        }

def fmt_usd(v):
    return f"USD {int(round(v)):,}"

def fmt_capex(low, high):
    return f"USD {low//1000}k - {high//1000}k"

def staff_label(seniors, juniors, assistants):
    parts = []
    if seniors > 0:
        parts.append(f"{seniors} Senior Stylist{'s' if seniors > 1 else ''}")
    if juniors > 0:
        parts.append(f"{juniors} Junior Stylist{'s' if juniors > 1 else ''}")
    if assistants > 0:
        parts.append(f"{assistants} Assistant{'s' if assistants > 1 else ''}")
    parts.append("1 Manager")
    return " + ".join(parts)

cities_json = []
for city in city_inputs:
    name = city["name"]
    if name not in results:
        continue
    r  = results[name]
    ex = extra_meta.get(name, {})

    entry = {
        "name":         name,
        "url":          city["url"],
        "region":       ex.get("region", city["region"]),
        "format":       ex.get("format", "Premium Boutique Salon"),
        "size":         r["size"],
        "airport":      ex.get("airport", ""),
        # Financial inputs
        "ticket":       f"USD {r['ticket']:.0f}",
        "cogs":         f"USD {r['cogs_session']:.2f}",
        "margin":       "90%",
        "rent_mo":      fmt_usd(r["rent"]),
        # Staff
        "stations":     r["stations"],
        "wash_basins":  r["wash_basins"],
        "total_staff":  r["total_staff"],
        "staff_label":  staff_label(r["seniors"], r["juniors"], r["assistants"]),
        "staff_cost_mo":fmt_usd(r["staff_cost"]),
        # Capacity
        "max_capacity": f"{r['max_cap']} sessions/month",
        "y1_clients":   r["y1_clients"],
        "y2_clients":   r["y2_clients"],
        "util_y1":      f"{int(r['util_y1']*100)}%",
        "util_y2":      f"{int(r['util_y2']*100)}%",
        # OPEX
        "opex":         fmt_usd(r["total_opex"]),
        "opex_raw":     r["total_opex"],
        # Economics
        "breakeven":    f"~{r['breakeven']} customers/mo",
        "daily_breakeven": f"~{r['be_daily']} sessions/day",
        "tax":          f"{r['tax']*100:.1f}%",
        "pat_ratio":    f"{r['pat_ratio']}% (Post-Tax, at 75% util.)",
        "y2_pat":       fmt_usd(r["y2_pat"]),
        # CAPEX
        "capex":        fmt_capex(r["capex_low"], r["capex_high"]),
        "capex_low":    r["capex_low"],
        "capex_high":   r["capex_high"],
        "payback":      f"{r['payback_mo']} Months (at 75% util.)",
        # Risk & flags
        "risk":         ex.get("risk", ""),
        "viable":       r["viable"],
        "country":      city["country"],
    }
    cities_json.append(entry)

if not DRY_RUN:
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(cities_json, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Written: {JSON_FILE} ({len(cities_json)} cities)")
else:
    print(f"  [DRY RUN] Would write {len(cities_json)} cities to {JSON_FILE}")

# ── PATCH script.js ─────────────────────────────────────────────────────────
print(f"\nPatching script.js...")

with open(JS_FILE, "r", encoding="utf-8") as f:
    js_content = f.read()

# Build fields to update per city in the citiesDb
changed = 0
for entry in cities_json:
    name = entry["name"]
    url  = entry["url"]

    city_pattern = re.compile(
        r'(\{\s*"name":\s*"' + re.escape(name) + r'")(.*?)("url":\s*"' + re.escape(url) + r'"\s*\})',
        re.DOTALL
    )
    m = city_pattern.search(js_content)
    if not m:
        print(f"  ✗ NOT FOUND in script.js: {name}")
        continue

    old_block = m.group(0)
    new_block = old_block

    fields = [
        (r'"format":\s*"[^"]*"',          f'"format": "{entry["format"]}"'),
        (r'"size":\s*"[^"]*"',             f'"size": "{entry["size"]}"'),
        (r'"capex":\s*"[^"]*"',            f'"capex": "{entry["capex"]}"'),
        (r'"opex":\s*"[^"]*"',             f'"opex": "{entry["opex"]}"'),
        (r'"ticket":\s*"[^"]*"',           f'"ticket": "{entry["ticket"]}"'),
        (r'"cogs":\s*"[^"]*"',             f'"cogs": "{entry["cogs"]}"'),
        (r'"margin":\s*"[^"]*"',           f'"margin": "90%"'),
        (r'"breakeven":\s*"[^"]*"',        f'"breakeven": "{entry["breakeven"]}"'),
        (r'"daily_breakeven":\s*"[^"]*"',  f'"daily_breakeven": "{entry["daily_breakeven"]}"'),
        (r'"tax":\s*"[^"]*"',              f'"tax": "{entry["tax"]}"'),
        (r'"pat_ratio":\s*"[^"]*"',        f'"pat_ratio": "{entry["pat_ratio"]}"'),
        (r'"payback":\s*"[^"]*"',          f'"payback": "{entry["payback"]}"'),
        (r'"risk":\s*"[^"]*"',             f'"risk": "{entry["risk"]}"'),
    ]
    for pat, repl in fields:
        new_block = re.sub(pat, repl, new_block, count=1)

    js_content = js_content[:m.start()] + new_block + js_content[m.end():]
    changed += 1

if not DRY_RUN:
    with open(JS_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"  ✓ Updated {changed}/27 city blocks in script.js")
else:
    print(f"  [DRY RUN] Would update {changed}/27 city blocks in script.js")

# ── SUMMARY TABLE ─────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("FINAL MODEL SUMMARY")
print("=" * 80)
print(f"{'City':<22} {'CAPEX':>16} {'OPEX':>10} {'Ticket':>8} {'BE':>6} {'PAT%':>6} {'Payback':>8}")
print("-" * 80)
for entry in cities_json:
    name = entry["name"]
    r    = results[name]
    print(f"{name:<22} USD{r['capex_low']//1000:>4}k-{r['capex_high']//1000}k "
          f"${r['total_opex']:>9,} ${r['ticket']:>7.0f} {r['breakeven']:>6} "
          f"{r['pat_ratio']:>5}% {r['payback_mo']:>6}mo")

print(f"\n✅ Done. {len(cities_json)} cities processed.")
print(f"   Files updated: city_data.json, script.js")
print(f"   Next: git add -A && git commit -m 'Update financials from Excel' && git push")
