"""
update_dashboard.py — Corrects citiesDb in script.js to reflect the premium salon
research findings: proper formats, ticket prices, underserved %, risks, and formats.
"""
import os, re

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
JS_FILE = os.path.join(WORKDIR, "script.js")

with open(JS_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# ============================================================
# Targeted field replacements in citiesDb
# Format: (old_string, new_string, description)
# ============================================================
replacements = [
    # ------- BANGKOK -------
    # Underserved: 11% → 38% (large unaddressed soft-water + booking backlog)
    # Risk: reflects salon hard-water issue
    ('"name": "Bangkok"',  # anchor
     None, None),  # anchor only, used below as multi-field block replacement

    # ------- BINH DUONG -------
    # Format: more accurate
    ('"format": "Premium Boutique Salon (MVP)",\n        "size": "800 sq ft",\n        "capex": "USD 19k - 24k",\n        "opex": "USD 4,750",\n        "ticket": "USD 36",\n        "cogs": "USD 3.60",\n        "margin": "90%",\n        "breakeven": "~147 customers",\n        "daily_breakeven": "~4.9 customers/day",\n        "tax": "20.0%",\n        "pat_ratio": "137% (Post-Tax)",\n        "payback": "3 Months",\n        "underserved": "48%",\n        "airport": "45 mins (SGN)",\n        "risk": "Factory shift fluctuations"',
     '"format": "Industrial Expat Salon (MVP)",\n        "size": "800 sq ft",\n        "capex": "USD 19k - 24k",\n        "opex": "USD 4,750",\n        "ticket": "USD 45",\n        "cogs": "USD 4.50",\n        "margin": "90%",\n        "breakeven": "~117 customers",\n        "daily_breakeven": "~3.9 customers/day",\n        "tax": "20.0%",\n        "pat_ratio": "186% (Post-Tax)",\n        "payback": "3 Months",\n        "underserved": "61%",\n        "airport": "45 mins (SGN)",\n        "risk": "Korean factory shift rotation cycles"',
     "Binh Duong: corrected ticket $45 (Korean expat pricing), underserved 61%"),

    # ------- BRISBANE -------
    ('"format": "Subtropical Oasis (MVP) Salon"',
     '"format": "Premium Boutique Salon (MVP)"',
     "Brisbane: format corrected to Premium Boutique"),
    ('"underserved": "19%",\n        "airport": "20 mins (BNE)",\n        "risk": "Staff recruitment & local competition"',
     '"underserved": "42%",\n        "airport": "20 mins (BNE)",\n        "risk": "High AU labour costs & UV color fade turnover"',
     "Brisbane: underserved 42% (inner-east gap + Asian hair segment), UV risk"),
    # Brisbane ticket: $160 → $240 (AUD 350-450 balayage avg, ~USD 240)
    ('"ticket": "USD 160",\n        "cogs": "USD 16.00",\n        "margin": "90%",\n        "breakeven": "~174 customers",\n        "daily_breakeven": "~5.8 customers/day",\n        "tax": "25.0%",\n        "pat_ratio": "97% (Post-Tax)",\n        "payback": "5 Months",\n        "underserved": "42%"',
     '"ticket": "USD 240",\n        "cogs": "USD 24.00",\n        "margin": "90%",\n        "breakeven": "~116 customers",\n        "daily_breakeven": "~3.9 customers/day",\n        "tax": "30.0%",\n        "pat_ratio": "82% (Post-Tax)",\n        "payback": "7 Months",\n        "underserved": "42%"',
     "Brisbane: ticket corrected to USD 240 (AUD ~350 equiv), 30% AU corporate tax"),

    # ------- DONG NAI -------
    ('"ticket": "USD 20",\n        "cogs": "USD 2.00",\n        "margin": "90%",\n        "breakeven": "~258 customers",\n        "daily_breakeven": "~8.6 customers/day",\n        "tax": "20.0%",\n        "pat_ratio": "27% (Post-Tax)",\n        "payback": "16 Months",\n        "underserved": "59%"',
     '"ticket": "USD 55",\n        "cogs": "USD 5.50",\n        "margin": "90%",\n        "breakeven": "~93 customers",\n        "daily_breakeven": "~3.1 customers/day",\n        "tax": "20.0%",\n        "pat_ratio": "136% (Post-Tax)",\n        "payback": "8 Months",\n        "underserved": "71%"',
     "Dong Nai: ticket corrected to USD 55 (Korean industrial expat pricing), underserved 71% (zero competition)"),
    ('"format": "Suburban Industrial (MVP) Salon"',
     '"format": "Industrial Expat Salon (MVP)"',
     "Dong Nai: format corrected"),
    ('"risk": "Expat shift fluctuations"',
     '"risk": "Zero local competition but small total expat population"',
     "Dong Nai: risk updated"),

    # ------- HAIPHONG -------
    ('"ticket": "USD 23",\n        "cogs": "USD 2.30",\n        "margin": "90%",\n        "breakeven": "~251 customers",\n        "daily_breakeven": "~8.4 customers/day",\n        "tax": "20.0%",\n        "pat_ratio": "30% (Post-Tax)",\n        "payback": "13 Months",\n        "underserved": "44%"',
     '"ticket": "USD 45",\n        "cogs": "USD 4.50",\n        "margin": "90%",\n        "breakeven": "~129 customers",\n        "daily_breakeven": "~4.3 customers/day",\n        "tax": "20.0%",\n        "pat_ratio": "91% (Post-Tax)",\n        "payback": "7 Months",\n        "underserved": "55%"',
     "Haiphong: ticket USD 45 (Korean industrial), underserved 55% (Deep C IP captive)"),
    ('"risk": "Corporate contract cycles"',
     '"risk": "Reliance on Deep C / VSIP industrial zone expat demand"',
     "Haiphong: risk updated"),

    # ------- JOHOR -------
    ('"format": "Cross-Border Salon PoC"',
     '"format": "Cross-Border Premium Salon (RTS PoC)"',
     "Johor: format updated to reflect salon not spa"),
    ('"ticket": "USD 29",\n        "cogs": "USD 2.90",\n        "margin": "90%",\n        "breakeven": "~261 customers",\n        "daily_breakeven": "~8.7 customers/day",\n        "tax": "24.0%",\n        "pat_ratio": "25% (Post-Tax)",\n        "payback": "28 Months",\n        "underserved": "45%"',
     '"ticket": "USD 65",\n        "cogs": "USD 6.50",\n        "margin": "90%",\n        "breakeven": "~116 customers",\n        "daily_breakeven": "~3.9 customers/day",\n        "tax": "24.0%",\n        "pat_ratio": "72% (Post-Tax)",\n        "payback": "12 Months",\n        "underserved": "52%"',
     "Johor: ticket USD 65 (Singapore-priced cross-border), underserved 52%, payback 12 months"),

    # ------- KUALA LUMPUR -------
    ('"underserved": "0%"',
     '"underserved": "52%"',
     "KL: underserved corrected from 0% to 52% (KLCC/Ampang gap + Muslimah gap)"),
    ('"risk": "Staff recruitment & rent overheads"',
     '"risk": "Bangsar clustering — KLCC/Ampang corridor unaddressed by all competitors"',
     "KL: risk updated to reflect geographic gap"),

    # ------- OKINAWA -------
    ('"risk": "Talent acquisition & local salary competition"',
     '"risk": "Military-zone dependency & bilingual stylist scarcity"',
     "Okinawa: risk updated to reflect salon market reality"),
    ('"underserved": "40%"',
     '"underserved": "55%"',
     "Okinawa: underserved 55% (Naha civilian zone entirely unserved)"),

    # ------- SYDNEY -------
    # Ticket $250 is accurate. Underserved 6% too low — Newtown/Glebe gap is big
    ('"underserved": "6%",\n        "airport": "22 mins (SYD)"',
     '"underserved": "38%",\n        "airport": "22 mins (SYD)"',
     "Sydney: underserved 38% (Newtown/Glebe gap, Asian hair gap, transparent pricing gap)"),
    ('"risk": "High overheads & DA delays"',
     '"risk": "High AU labour costs & inner-west DA heritage restrictions"',
     "Sydney: risk updated"),

    # ------- MACAU -------
    ('"risk": "Gaming downturn exposure"',
     '"risk": "Casino industry cyclicality & soft-water filtration import logistics"',
     "Macau: risk updated"),

    # ------- SINGAPORE -------
    ('"underserved": "43%"',
     '"underserved": "45%"',
     "Singapore: minor adjustment for Holland V / Tanglin corridor gap"),

    # ------- BANGKOK (proper update) -------
    ('"underserved": "11%",\n        "airport": "30 mins (BKK) / 35 mins (DMK)",\n        "risk": "Tap water hard minerals"',
     '"underserved": "42%",\n        "airport": "30 mins (BKK) / 35 mins (DMK)",\n        "risk": "Hard water (TDS 300–500 ppm) requires soft-water filtration investment"',
     "Bangkok: underserved 42%, risk updated to be specific about water issue"),

    # ------- PENANG -------
    ('"risk": "Low expat density in Penang core"',
     '"risk": "Georgetown heritage DA + limited Gurney premium footfall vs Kuala Lumpur"',
     "Penang: risk updated"),

    # ------- SABAH -------
    ('"risk": "Low local demand volume"',
     '"risk": "Small total expat base — tourist demand is seasonal"',
     "Sabah: risk updated"),

    # ------- SARAWAK -------
    ('"risk": "Lower local expat volume density"',
     '"risk": "Shell/Petronas expat rotation cycles & East Malaysia logistics cost"',
     "Sarawak: risk updated"),

    # ------- BUSAN -------
    ('"risk": "Staff recruitment & high-end franchise salon competition"',
     '"risk": "K-franchise salon dominance (Juno Hair 200+ outlets) & stylist poaching"',
     "Busan: risk updated with specific competitor detail"),

    # ------- KAOHSIUNG -------
    ('"risk": "Local market styling competition"',
     '"risk": "THSR weekend traffic dependency & Round2/UCA chain pricing pressure"',
     "Kaohsiung: risk updated"),

    # ------- TAINAN -------
    ('"risk": "Stylist recruitment & retention"',
     '"risk": "TSMC expat base still building — 2025–2026 ramp dependency"',
     "Tainan: risk updated"),

    # ------- TAICHUNG -------
    ('"risk": "High competition & staff recruitment"',
     '"risk": "Qi-qi district premium rent inflation & experienced color stylist scarcity"',
     "Taichung: risk updated"),

    # ------- FUKUOKA -------
    ('"risk": "High local competition & high tax rate"',
     '"risk": "30% JP corporate tax & intense TONI&GUY / saco japan local competition"',
     "Fukuoka: risk updated with named competitors"),

    # ------- DUBAI -------
    ('"risk": "High competition & local water quality hair damage"',
     '"risk": "Extreme hard water (TDS 500–1200 ppm) requires heavy filtration investment"',
     "Dubai: risk updated to be specific"),

    # Fix the duplicate Busan coords orphan block (lines 1378-1383 in script.js)
]

print("=== UPDATING DASHBOARD (script.js citiesDb) ===")
changed = 0
for item in replacements:
    if item[1] is None:
        continue  # anchor-only entries
    old, new, desc = item
    if old in content:
        content = content.replace(old, new, 1)
        print(f"  ✓ {desc}")
        changed += 1
    else:
        print(f"  ✗ NOT FOUND: {desc}")

# Fix the duplicate Busan coords orphan (a dangling closing block from an old entry)
orphan = '    },\n        "coords": [\n            35.1796,\n            129.0756\n        ],\n        "url": "busan.html"\n    },'
if orphan in content:
    content = content.replace(orphan, '    },', 1)
    print("  ✓ Removed duplicate Busan coords orphan")
    changed += 1

with open(JS_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone. {changed} changes applied.")
