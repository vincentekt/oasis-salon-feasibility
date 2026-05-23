"""
capacity_model.py
=================
Full capacity-driven financial model for all 27 cities.

Logic chain:
  Space (sqft) → Stations → Staff needed → Max monthly capacity
  → Revenue at 70% utilization → Profit → Payback period

Rules:
  Space → Stations:
    750 sqft: 3 stations + 2 wash basins (SG, HK, Macau — premium city compact)
    800 sqft: 4 stations + 2 wash basins (most cities)
    850 sqft: 4 stations + 2 wash basins (Taipei)
    900 sqft: 5 stations + 2 wash basins (Fukuoka — larger JPN boutique)
   1000 sqft: 5 stations + 3 wash basins (Johor — cross-border volume model)

  Sessions per station per day (avg session duration drives this):
    Ultra-premium colour (AU, SG, HK, Dubai, Macau): 3 sess/station/day (avg 180 min)
    Standard premium (JP, KR, TW, BKK): 3 sess/station/day (avg 150 min)
    Vietnam premium (HCMC, Hanoi): 3 sess/station/day (avg 120 min colour+cut)
    Vietnam/MY industrial expat (DaNang, Haiphong, BinhDuong, DongNai, Penang, Sabah, Sarawak): 
      4 sess/station/day (avg 90-100 min — cut + basic colour for Korean/factory workers)
    Johor (cross-border, mixed): 4 sess/station/day (faster turnover model)

  Working days: 26/month (6 days/week)
  Utilization targets:
    Year 1: 60% (building client base)
    Year 2: 75% (steady state)
    Peak: 85% (fully booked boutique)

  Staff per station (premium model):
    Each station needs 1 dedicated stylist
    + 1 junior/assistant per 2 stations (colour prep, wash, blow-dry)
    + 1 receptionist/manager (all sizes)
    So:
      3 stations: 3 stylists + 2 assistants + 1 manager = 6 total
      4 stations: 4 stylists + 2 assistants + 1 manager = 7 total
      5 stations: 5 stylists + 3 assistants + 1 manager = 9 total

  Stylist cost (monthly, USD, at senior blended rate by country):
    AU:  Senior AUD 6,500 ($4,225), Junior/Asst AUD 3,800 ($2,470), Manager AUD 7,000 ($4,550)
    JP:  Senior JPY 350k ($2,345), Asst JPY 220k ($1,474), Manager JPY 450k ($3,015)
    KR:  Senior KRW 2.8M ($2,044), Asst KRW 1.8M ($1,314), Manager KRW 3.5M ($2,555)
    SG:  Senior SGD 4,500 ($3,330), Asst SGD 2,500 ($1,850), Manager SGD 6,000 ($4,440)
    HK:  Senior HKD 19k ($2,432), Asst HKD 13k ($1,664), Manager HKD 24k ($3,072)
    TW:  Senior NTD 55k ($1,705), Asst NTD 32k ($992), Manager NTD 70k ($2,170)
    MY:  Senior MYR 4,500 ($990), Asst MYR 2,200 ($484), Manager MYR 6,000 ($1,320)
    VN:  Senior USD 800, Asst USD 420, Manager USD 1,100
    TH:  Senior THB 45k ($1,305), Asst THB 22k ($638), Manager THB 60k ($1,740)
    AE:  Senior AED 10k ($2,720), Asst AED 6k ($1,632), Manager AED 14k ($3,808)
    MC:  Senior HKD 18k ($2,304), Asst HKD 12k ($1,536), Manager HKD 22k ($2,816) [Macau]
"""

import os, re

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
JS_FILE = os.path.join(WORKDIR, "script.js")

# ── STAFF COST HELPERS ─────────────────────────────────────────────────────
def staff_cost(country, stations):
    """Return total monthly staff cost in USD."""
    # n_stylists = stations, n_assistants = stations//2 rounded up, n_managers = 1
    ns = stations
    na = (stations + 1) // 2
    nm = 1
    if country == "AU":
        return ns * 4225 + na * 2470 + nm * 4550
    elif country == "JP":
        return ns * 2345 + na * 1474 + nm * 3015
    elif country == "KR":
        return ns * 2044 + na * 1314 + nm * 2555
    elif country == "SG":
        return ns * 3330 + na * 1850 + nm * 4440
    elif country == "HK":
        return ns * 2432 + na * 1664 + nm * 3072
    elif country == "MC":  # Macau
        return ns * 2304 + na * 1536 + nm * 2816
    elif country == "TW":
        return ns * 1705 + na * 992 + nm * 2170
    elif country == "MY":
        return ns * 990 + na * 484 + nm * 1320
    elif country == "VN":
        return ns * 800 + na * 420 + nm * 1100
    elif country == "TH":
        return ns * 1305 + na * 638 + nm * 1740
    elif country == "AE":
        return ns * 2720 + na * 1632 + nm * 3808
    else:
        return ns * 1500 + na * 800 + nm * 2000

# ── CITY DEFINITIONS ──────────────────────────────────────────────────────────
# (sqft, country_code, sessions_per_station_per_day, rent_usd, ticket_usd,
#  cogs_pct, tax_rate, fitout_usd, capex_extra_usd, airport, risk, format, region, url)

CITIES = {
    "Ho Chi Minh": {
        "sqft": 800, "country": "VN", "sess_per_day": 3,
        "rent": 3000, "ticket": 95, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 20000, "extras": 20000,   # equipment + legal + deposit + stock
        "util_rent_deposit_mo": 3,
        "airport": "30 mins (SGN)",
        "risk": "Foreign ownership license compliance (IRC/ERC process 2-4 months)",
        "format": "Premium Boutique Salon (MVP)", "region": "Vietnam", "url": "hcmc.html"
    },
    "Hanoi": {
        "sqft": 800, "country": "VN", "sess_per_day": 3,
        "rent": 2200, "ticket": 95, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 18000, "extras": 19000,
        "util_rent_deposit_mo": 3,
        "airport": "30 mins (HAN)",
        "risk": "Hard water (TDS 400+ ppm) requires RO filtration investment; foreign license compliance",
        "format": "Premium Boutique Salon (MVP)", "region": "Vietnam", "url": "hanoi.html"
    },
    "Da Nang": {
        "sqft": 800, "country": "VN", "sess_per_day": 4,
        "rent": 800, "ticket": 55, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 12000, "extras": 15000,
        "util_rent_deposit_mo": 3,
        "airport": "12 mins (DAD)",
        "risk": "Seasonal tourism slump (Nov-Feb monsoon); nomad base fluctuates with global remote-work trends",
        "format": "Coastal Expat Salon (MVP)", "region": "Vietnam", "url": "danang.html"
    },
    "Hai Phong": {
        "sqft": 800, "country": "VN", "sess_per_day": 4,
        "rent": 650, "ticket": 45, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 10000, "extras": 14000,
        "util_rent_deposit_mo": 3,
        "airport": "15 mins (HPH)",
        "risk": "Dependency on Deep C / VSIP Korean industrial rotation cycles",
        "format": "Industrial Expat Salon (MVP)", "region": "Vietnam", "url": "haiphong.html"
    },
    "Binh Duong": {
        "sqft": 800, "country": "VN", "sess_per_day": 4,
        "rent": 600, "ticket": 45, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 10000, "extras": 13000,
        "util_rent_deposit_mo": 3,
        "airport": "45 mins (SGN)",
        "risk": "Korean factory shift rotation cycles; premium product supply chain from HCMC (60 min)",
        "format": "Industrial Expat Salon (MVP)", "region": "Vietnam", "url": "binhduong.html"
    },
    "Dong Nai": {
        "sqft": 800, "country": "VN", "sess_per_day": 4,
        "rent": 550, "ticket": 55, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 9000, "extras": 12000,
        "util_rent_deposit_mo": 3,
        "airport": "60 mins (SGN)",
        "risk": "Zero local competition but small total expat population; 60-min SGN logistics chain",
        "format": "Industrial Expat Salon (MVP)", "region": "Vietnam", "url": "dongnai.html"
    },
    "Kuala Lumpur": {
        "sqft": 800, "country": "MY", "sess_per_day": 3,
        "rent": 2000, "ticket": 90, "cogs_pct": 0.10, "tax": 0.24,
        "fitout": 33000, "extras": 20000,
        "util_rent_deposit_mo": 3,
        "airport": "45 mins (KUL)",
        "risk": "KLCC/Ampang corridor gap vs. 4 established competitors in Bangsar; Muslimah bay planning needed",
        "format": "Premium Boutique Salon (MVP)", "region": "Malaysia", "url": "kuala_lumpur.html"
    },
    "Johor Bahru (RTS)": {
        "sqft": 1000, "country": "MY", "sess_per_day": 4,
        "rent": 1700, "ticket": 65, "cogs_pct": 0.10, "tax": 0.24,
        "fitout": 28600, "extras": 18000,
        "util_rent_deposit_mo": 3,
        "airport": "30 mins (JHB) / 50 mins (SIN)",
        "risk": "RTS operational delays; SG cross-border demand tied to MYR/SGD exchange rate sensitivity",
        "format": "Cross-Border Premium Salon (RTS PoC)", "region": "Malaysia", "url": "johor.html"
    },
    "Penang": {
        "sqft": 800, "country": "MY", "sess_per_day": 4,
        "rent": 800, "ticket": 55, "cogs_pct": 0.10, "tax": 0.24,
        "fitout": 22000, "extras": 15000,
        "util_rent_deposit_mo": 3,
        "airport": "25 mins (PEN)",
        "risk": "Georgetown heritage DA restrictions on fit-out signage; limited premium residential density vs KL",
        "format": "Premium Boutique Salon (MVP)", "region": "Malaysia", "url": "penang.html"
    },
    "Sabah": {
        "sqft": 800, "country": "MY", "sess_per_day": 4,
        "rent": 900, "ticket": 45, "cogs_pct": 0.10, "tax": 0.24,
        "fitout": 19800, "extras": 14500,
        "util_rent_deposit_mo": 3,
        "airport": "20 mins (BKI)",
        "risk": "Small total expat base; East Malaysia logistics surcharge for premium colour product supply",
        "format": "Coastal Expat Salon (MVP)", "region": "Malaysia", "url": "sabah.html"
    },
    "Sarawak": {
        "sqft": 800, "country": "MY", "sess_per_day": 4,
        "rent": 700, "ticket": 46, "cogs_pct": 0.10, "tax": 0.24,
        "fitout": 18700, "extras": 14000,
        "util_rent_deposit_mo": 3,
        "airport": "20 mins (KCH)",
        "risk": "Shell/Petronas rotation cycles; East Malaysia freight costs for salon products",
        "format": "Boutique Expat Salon (MVP)", "region": "Malaysia", "url": "sarawak.html"
    },
    "Singapore": {
        "sqft": 750, "country": "SG", "sess_per_day": 3,
        "rent": 5500, "ticket": 180, "cogs_pct": 0.10, "tax": 0.17,
        "fitout": 66600, "extras": 26000,
        "util_rent_deposit_mo": 3,
        "airport": "25 mins (SIN)",
        "risk": "Ultra-high rent; Holland V HDB commercial leases require SCDF & BCA approvals; F&B landlord competition",
        "format": "Premium Boutique Salon", "region": "Other APAC", "url": "singapore.html"
    },
    "Hong Kong": {
        "sqft": 750, "country": "HK", "sess_per_day": 3,
        "rent": 8500, "ticket": 200, "cogs_pct": 0.10, "tax": 0.165,
        "fitout": 76800, "extras": 30000,
        "util_rent_deposit_mo": 3,
        "airport": "40 mins (HKG)",
        "risk": "Ultra-high commercial rent; Causeway Bay lease scarcity and key money (premium) demands",
        "format": "Premium Boutique Salon (MVP)", "region": "Other APAC", "url": "hongkong.html"
    },
    "Bangkok": {
        "sqft": 800, "country": "TH", "sess_per_day": 3,
        "rent": 5000, "ticket": 160, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 43500, "extras": 33000,  # incl. RO $5k
        "util_rent_deposit_mo": 3,
        "airport": "30 mins (BKK) / 35 mins (DMK)",
        "risk": "Hard water (TDS 300-500 ppm) — RO filtration essential; very high Thonglor rent premium",
        "format": "Premium Boutique Salon (MVP)", "region": "Other APAC", "url": "bangkok.html"
    },
    "Macau": {
        "sqft": 750, "country": "MC", "sess_per_day": 3,
        "rent": 1800, "ticket": 130, "cogs_pct": 0.10, "tax": 0.12,
        "fitout": 44800, "extras": 20000,
        "util_rent_deposit_mo": 3,
        "airport": "15 mins (MFM)",
        "risk": "Casino industry cyclicality; soft-water filtration import logistics from HK",
        "format": "Premium Boutique Salon (MVP)", "region": "Other APAC", "url": "macau.html"
    },
    "Dubai": {
        "sqft": 800, "country": "AE", "sess_per_day": 3,
        "rent": 3500, "ticket": 160, "cogs_pct": 0.10, "tax": 0.09,
        "fitout": 54400, "extras": 57600,  # incl. annual lease pre-pay $42k + heavy RO $8k + others
        "util_rent_deposit_mo": 12,  # UAE pays annual upfront
        "airport": "15 mins (DXB)",
        "risk": "Extreme hard water (TDS 500-1200 ppm) — heavy RO investment; annual lease pre-payment UAE norm",
        "format": "Premium Boutique Salon (MVP)", "region": "Middle East", "url": "dubai.html"
    },
    "Taipei": {
        "sqft": 850, "country": "TW", "sess_per_day": 3,
        "rent": 2200, "ticket": 104, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 55800, "extras": 24000,
        "util_rent_deposit_mo": 3,
        "airport": "15 mins (TSA) / 45 mins (TPE)",
        "risk": "Intense local competition; 6-9 hr wait at top competitors — booking system must prevent same bottleneck",
        "format": "Premium Boutique Salon", "region": "Taiwan", "url": "taipei.html"
    },
    "Taichung": {
        "sqft": 800, "country": "TW", "sess_per_day": 3,
        "rent": 1800, "ticket": 110, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 46500, "extras": 20000,
        "util_rent_deposit_mo": 3,
        "airport": "30 mins (RMQ)",
        "risk": "Qi-qi premium rent inflation; experienced colour stylist scarcity vs. local Taiwanese market",
        "format": "Premium Boutique Salon (MVP)", "region": "Taiwan", "url": "taichung.html"
    },
    "Kaohsiung": {
        "sqft": 800, "country": "TW", "sess_per_day": 3,
        "rent": 1200, "ticket": 120, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 37200, "extras": 18000,
        "util_rent_deposit_mo": 3,
        "airport": "15 mins (KHH)",
        "risk": "THSR Zuoying first-mover reliant on commuter appointment behavior; Round2/UCA Lingya competition",
        "format": "Premium Boutique Salon (MVP)", "region": "Taiwan", "url": "kaohsiung.html"
    },
    "Tainan": {
        "sqft": 750, "country": "TW", "sess_per_day": 3,
        "rent": 900, "ticket": 80, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 34100, "extras": 16000,
        "util_rent_deposit_mo": 3,
        "airport": "35 mins (TNN) / 50 mins (KHH)",
        "risk": "TSMC Sinshih expat base still ramping — 2025-2027 TSMC fab construction dependency",
        "format": "Premium Boutique Salon (MVP)", "region": "Taiwan", "url": "tainan.html"
    },
    "Fukuoka": {
        "sqft": 900, "country": "JP", "sess_per_day": 3,
        "rent": 1600, "ticket": 95, "cogs_pct": 0.10, "tax": 0.30,
        "fitout": 100500, "extras": 30000,
        "util_rent_deposit_mo": 3,
        "airport": "15 mins (FUK)",
        "risk": "30% JP corporate tax + highest-in-portfolio fitout cost; intense TONI&GUY/saco japan competition",
        "format": "Premium Boutique Salon (MVP)", "region": "Japan", "url": "fukuoka.html"
    },
    "Okinawa": {
        "sqft": 800, "country": "JP", "sess_per_day": 3,
        "rent": 1100, "ticket": 120, "cogs_pct": 0.10, "tax": 0.30,
        "fitout": 80400, "extras": 24000,
        "util_rent_deposit_mo": 3,
        "airport": "15 mins (OKA)",
        "risk": "Bilingual (English/Korean) stylist recruitment extremely difficult in Okinawa; 30% JP tax burden",
        "format": "Premium Boutique Salon (MVP)", "region": "Japan", "url": "okinawa.html"
    },
    "Busan": {
        "sqft": 800, "country": "KR", "sess_per_day": 3,
        "rent": 2200, "ticket": 100, "cogs_pct": 0.10, "tax": 0.20,
        "fitout": 58400, "extras": 24000,
        "util_rent_deposit_mo": 3,
        "airport": "30 mins (PUS)",
        "risk": "K-franchise dominance (Juno Hair 200+ outlets); Marine City appointment-only requires strong pre-booking system",
        "format": "Ground-Floor Premium Salon (MVP)", "region": "South Korea", "url": "busan.html"
    },
    "Sydney": {
        "sqft": 800, "country": "AU", "sess_per_day": 3,
        "rent": 3200, "ticket": 250, "cogs_pct": 0.10, "tax": 0.30,
        "fitout": 91000, "extras": 32000,
        "util_rent_deposit_mo": 3,
        "airport": "22 mins (SYD)",
        "risk": "High AU labour Award rates + 11.5% superannuation; inner-west DA heritage restrictions on fit-out",
        "format": "Premium Boutique Salon (MVP)", "region": "Australia", "url": "sydney.html"
    },
    "Melbourne": {
        "sqft": 800, "country": "AU", "sess_per_day": 3,
        "rent": 3500, "ticket": 220, "cogs_pct": 0.10, "tax": 0.30,
        "fitout": 87750, "extras": 30000,
        "util_rent_deposit_mo": 3,
        "airport": "30 mins (MEL)",
        "risk": "High AU labour + superannuation; Chapel St rent inflation; F&B competition for prime ground-floor leases",
        "format": "Premium Boutique Salon (MVP)", "region": "Australia", "url": "melbourne.html"
    },
    "Brisbane": {
        "sqft": 800, "country": "AU", "sess_per_day": 3,
        "rent": 2800, "ticket": 240, "cogs_pct": 0.10, "tax": 0.30,
        "fitout": 78000, "extras": 26000,
        "util_rent_deposit_mo": 3,
        "airport": "20 mins (BNE)",
        "risk": "High AU labour costs and superannuation; UV-damaged colour turnover requires more frequent client visits",
        "format": "Premium Boutique Salon (MVP)", "region": "Australia", "url": "brisbane.html"
    },
    "Perth": {
        "sqft": 800, "country": "AU", "sess_per_day": 3,
        "rent": 2000, "ticket": 200, "cogs_pct": 0.10, "tax": 0.30,
        "fitout": 74750, "extras": 24000,
        "util_rent_deposit_mo": 3,
        "airport": "22 mins (PER)",
        "risk": "FIFO schedule volatility; isolation from east-coast premium product supply chain",
        "format": "Coastal Expat Salon (MVP)", "region": "Australia", "url": "perth.html"
    },
}

# ── SPACE → STATIONS MAPPING ─────────────────────────────────────────────────
def sqft_to_stations(sqft):
    if sqft <= 750:
        return 3
    elif sqft <= 850:
        return 4
    elif sqft <= 950:
        return 5
    else:
        return 5

# ── WORKING PARAMETERS ────────────────────────────────────────────────────────
WORKING_DAYS = 26   # 6 days/week × ~4.3 weeks
UTIL_Y1 = 0.65      # Year 1 (building clientele)
UTIL_Y2 = 0.75      # Year 2 steady state (used for payback)

# ── COMPUTE MODEL PER CITY ───────────────────────────────────────────────────
print("=" * 110)
print(f"{'City':<22} {'Sqft':>5} {'Sta':>4} {'Stf':>4} {'MaxCap':>7} {'Y1 Cli':>7} {'Y1 Rev':>9} {'OPEX':>8} {'Staff$':>7} {'Tick':>6} {'PAT/mo':>8} {'PAT%':>6} {'CAPEX':>12} {'Payback':>8}")
print("=" * 110)

results = {}

for city_name, c in CITIES.items():
    stations = sqft_to_stations(c["sqft"])
    staff_mo = staff_cost(c["country"], stations)
    assistants = (stations + 1) // 2
    total_staff = stations + assistants + 1  # stylists + assistants + manager

    # Max monthly capacity
    max_sessions_mo = stations * c["sess_per_day"] * WORKING_DAYS
    # Year 1 clients (65% utilization)
    y1_clients = int(max_sessions_mo * UTIL_Y1)
    # Year 2 clients (75% utilization) — used for payback
    y2_clients = int(max_sessions_mo * UTIL_Y2)

    # OPEX breakdown
    ticket = c["ticket"]
    cogs_pct = c["cogs_pct"]
    cogs_per_session = ticket * cogs_pct
    rent = c["rent"]
    util_cost = 200 + int(stations * 80)  # utilities scale with stations (more equipment)
    mktg = 350 + int(stations * 50)
    misc = 300 + int(stations * 30)
    opex_total = int(rent + staff_mo + util_cost + mktg + misc)

    # Revenue and profit
    y2_revenue = y2_clients * ticket
    y2_cogs_total = y2_clients * cogs_per_session
    y2_ebit = y2_revenue - opex_total - y2_cogs_total
    y2_pat = y2_ebit * (1 - c["tax"])
    pat_ratio = int(round((y2_pat / opex_total) * 100)) if y2_pat > 0 else 0

    # Breakeven
    gross_margin_per_client = ticket - cogs_per_session
    be_clients = int(opex_total / gross_margin_per_client + 0.5)
    be_daily = round(be_clients / WORKING_DAYS, 1)

    # CAPEX
    deposit = int(c["rent"] * c["util_rent_deposit_mo"])
    capex = int(c["fitout"] + c["extras"] + deposit)
    # Round to nearest 5k
    capex_low = int(capex * 0.92 / 5000) * 5000
    capex_high = int(capex * 1.08 / 5000 + 0.9) * 5000

    # Payback at Y2 PAT
    payback_mo = int(round(((capex_low + capex_high) / 2) / y2_pat)) if y2_pat > 0 else 99

    print(f"{city_name:<22} {c['sqft']:>5} {stations:>4} {total_staff:>4} {max_sessions_mo:>7} {y1_clients:>7} ${y2_revenue:>8,} ${opex_total:>7,} ${staff_mo:>6,} ${ticket:>5} ${y2_pat:>7,.0f} {pat_ratio:>5}% USD{capex_low//1000:>4}k-{capex_high//1000}k {payback_mo:>6}mo")

    results[city_name] = {
        "stations": stations, "total_staff": total_staff,
        "max_sessions_mo": max_sessions_mo,
        "y1_clients": y1_clients, "y2_clients": y2_clients,
        "opex": opex_total, "staff_mo": int(staff_mo),
        "rent": rent, "ticket": ticket,
        "cogs": cogs_per_session, "tax": c["tax"],
        "be_clients": be_clients, "be_daily": be_daily,
        "y2_pat": y2_pat, "pat_ratio": pat_ratio,
        "capex_low": capex_low, "capex_high": capex_high,
        "payback_mo": payback_mo,
        "format": c["format"], "region": c["region"],
        "size": f"{c['sqft']} sq ft",
        "airport": c["airport"], "risk": c["risk"],
        "url": c["url"],
        "country": c["country"],
        "util_y1": UTIL_Y1, "util_y2": UTIL_Y2,
        "sess_per_day": c["sess_per_day"],
    }

# ── UPDATE script.js ──────────────────────────────────────────────────────────
print("\n\n=== UPDATING script.js citiesDb ===\n")

with open(JS_FILE, "r", encoding="utf-8") as f:
    content = f.read()

def fmt_usd_k(low, high):
    return f"USD {low//1000}k - {high//1000}k"

changed = 0
for city_name, r in results.items():
    db_name = city_name  # matches "name" field in JS

    # Regex: find city block by name + url anchor
    city_pattern = re.compile(
        r'(\{\s*"name":\s*"' + re.escape(db_name) + r'")(.*?)("url":\s*"' + re.escape(r["url"]) + r'"\s*\})',
        re.DOTALL
    )
    m = city_pattern.search(content)
    if not m:
        print(f"  ✗ NOT FOUND: {city_name}")
        continue

    old_block = m.group(0)
    new_block = old_block

    # Field replacements
    fields = [
        (r'"format":\s*"[^"]*"',        f'"format": "{r["format"]}"'),
        (r'"size":\s*"[^"]*"',           f'"size": "{r["size"]}"'),
        (r'"capex":\s*"[^"]*"',          f'"capex": "{fmt_usd_k(r["capex_low"], r["capex_high"])}"'),
        (r'"opex":\s*"[^"]*"',           f'"opex": "USD {r["opex"]:,}"'),
        (r'"ticket":\s*"[^"]*"',         f'"ticket": "USD {r["ticket"]}"'),
        (r'"cogs":\s*"[^"]*"',           f'"cogs": "USD {r["cogs"]:.2f}"'),
        (r'"margin":\s*"[^"]*"',         '"margin": "90%"'),
        (r'"breakeven":\s*"[^"]*"',      f'"breakeven": "~{r["be_clients"]} customers/mo"'),
        (r'"daily_breakeven":\s*"[^"]*"',f'"daily_breakeven": "~{r["be_daily"]} sessions/day"'),
        (r'"tax":\s*"[^"]*"',            f'"tax": "{r["tax"]*100:.1f}%"'),
        (r'"pat_ratio":\s*"[^"]*"',      f'"pat_ratio": "{r["pat_ratio"]}% (Post-Tax, at 75% util.)"'),
        (r'"payback":\s*"[^"]*"',        f'"payback": "{r["payback_mo"]} Months (at 75% util.)"'),
        (r'"risk":\s*"[^"]*"',           f'"risk": "{r["risk"]}"'),
    ]

    for pat, repl in fields:
        new_block = re.sub(pat, repl, new_block, count=1)

    content = content[:m.start()] + new_block + content[m.end():]
    print(f"  ✓ {city_name}: {r['stations']} stations, {r['total_staff']} staff, "
          f"max {r['max_sessions_mo']}/mo, OPEX ${r['opex']:,}, "
          f"payback {r['payback_mo']}mo, PAT {r['pat_ratio']}%")
    changed += 1

with open(JS_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone. {changed}/27 city blocks updated in script.js.")

# ── SAVE RESULTS FOR HTML UPDATE ─────────────────────────────────────────────
import json
with open(os.path.join(WORKDIR, "capacity_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("Saved capacity_results.json for HTML subpage updates.")
