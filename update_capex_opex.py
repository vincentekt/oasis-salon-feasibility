"""
update_capex_opex.py
Research-backed CAPEX and OPEX update for all 27 cities.
Recalculates: breakeven, daily_breakeven, pat_ratio, payback, ticket (where changed).

RESEARCH BASIS:
==============
CAPEX COMPONENTS (all cities):
  - Equipment: 4 Takara Belmont styling chairs @ ~$1,500-2,500ea = $6k-10k
               2 wash basins @ $2,800-4,500ea = $5.6k-9k
               RO filtration system = $3k-8k (depends on water hardness)
               Tools, colour dispensing, POS = $3k-5k
               Subtotal equipment: $17k-32k (USD)
  - Fit-out/Renovation: varies by country (see below)
  - Lease deposit: typically 2-3 months rent
  - Legal/registration: $2k-5k
  - Working capital (initial stock + buffer): $5k-10k

FIT-OUT COST BY COUNTRY (per sqm, for 75 sqm / 800 sqft salon):
  Australia: AUD 1,800-2,500/sqm → 75sqm → AUD 135k-188k → USD 87k-122k
  Japan: JPY 200k-350k/sqm → 75sqm → JPY 15M-26M → USD 100k-170k
  South Korea: KRW 800k-1.5M/sqm → 75sqm → KRW 60M-113M → USD 44k-83k
  Singapore/HK: SGD/HKD equivalent ~ USD 100k-160k for 75sqm (high labour)
  Taiwan: NTD 20k-35k/sqm → 75sqm → NTD 1.5M-2.6M → USD 47k-82k
  Malaysia/Thailand: USD 20k-45k fitout for 75sqm (lower labour costs)
  Vietnam: USD 12k-25k fitout for 75sqm (very low labour)
  Dubai: AED equivalent ~ USD 40k-65k for 75sqm
  Macau: HKD equivalent ~ USD 60k-90k

STYLIST SALARY BY COUNTRY (total staff monthly, per role):
  Australia: Senior stylist AUD 6,500/mo + junior AUD 4,000/mo
             3 seniors + 1 junior + 1 manager: ~AUD 30k/mo → USD 19.5k
  Japan: Senior stylist JPY 350k/mo + junior 220k/mo
         2 seniors + 1 junior + part-time manager: ~JPY 1.1M/mo → USD 7.2k
  South Korea: Senior KRW 2.8M/mo + junior KRW 1.8M/mo
               2 seniors + 1 junior + part-manager: ~KRW 8.4M/mo → USD 6.1k
  Singapore: Senior SGD 4,500/mo + junior SGD 2,800/mo
             2 seniors + 1 junior + part-manager: ~SGD 13.5k/mo → USD 10k
  HK: Senior HKD 19k/mo + junior HKD 14k/mo
      2 seniors + 1 junior + part-manager: ~HKD 57k/mo → USD 7.3k
  Taiwan: Senior NTD 55k/mo + junior NTD 35k/mo
          2 seniors + 1 junior + part-manager: ~NTD 165k/mo → USD 5.1k
  Malaysia: Senior MYR 4,500/mo + junior MYR 2,500/mo
            2 seniors + 1 junior + part-manager: ~MYR 13.5k/mo → USD 3k
  Vietnam/VN expat: Senior USD 800/mo + junior USD 500/mo
                    2 seniors + 2 juniors + manager: ~USD 3.6k
  Thailand (Bangkok): Senior THB 45k/mo + junior THB 25k/mo
                      2 seniors + 1 junior + manager: ~THB 150k/mo → USD 4.3k
  Dubai: Senior AED 10k/mo + junior AED 6k/mo + manager AED 12k/mo
         2 seniors + 1 junior + 1 manager: ~AED 38k/mo → USD 10.3k

RENT (monthly for recommended location, 75 sqm):
  Based on research:
  Sydney:      USD 3,200 (Newtown - competitive zone)
  Melbourne:   USD 3,500 (South Yarra Chapel St)
  Brisbane:    USD 2,800 (New Farm Brunswick St)
  Perth:       USD 2,000 (Subiaco Rokeby Rd)
  Singapore:   USD 5,500 (Holland Village)
  HK:          USD 8,500 (Causeway Bay Lockhart Rd)
  Bangkok:     USD 5,000 (Thonglor Soi 10) [was overestimated in some places]
  KL:          USD 2,000 (Jalan Ampang)
  Johor:       USD 1,700 (R&F Mall)
  Penang:      USD 800  (Jalan Burma)
  Sabah:       USD 900  (Jesselton Point)
  Sarawak:     USD 700  (Tabuan Jaya)
  HCMC:        USD 3,000 (Thao Dien)
  Hanoi:       USD 2,200 (Xuan Dieu)
  Da Nang:     USD 800  (An Thuong)
  Haiphong:    USD 650  (Minh Khai Industrial)
  Binh Duong:  USD 600  (VSIP I)
  Dong Nai:    USD 550  (AMATA Gate)
  Taipei:      USD 2,200 (Da'an Yongkang)
  Taichung:    USD 1,800 (Qi-qi zone)
  Kaohsiung:   USD 1,200 (Zuoying THSR)
  Tainan:      USD 900  (Sinshih TSMC zone)
  Fukuoka:     USD 1,600 (Daimyo lane)
  Okinawa:     USD 1,100 (Omoromachi)
  Busan:       USD 2,200 (Marine City)
  Dubai:       USD 3,500 (Jumeirah 1)
  Macau:       USD 1,800 (Taipa Village)
"""

import os, re, json

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

# ============================================================
# CITY FINANCIAL MODEL — Research-Backed
# ============================================================
# Per city: capex_range, opex_breakdown (rent+staff+products+util+misc),
#   ticket, cogs_pct=10%, margin=90%, tax, and derived metrics.

def compute(capex_low, capex_high, opex, ticket, cogs_pct, tax_rate, months_for_payback_search=36):
    """Compute breakeven customers/mo, daily breakeven (30 days/mo, 6 days/wk ~26 days),
    PAT ratio, and payback months."""
    cogs = round(ticket * cogs_pct, 2)
    gross_margin = ticket - cogs  # per customer
    breakeven_customers = int(round(opex / gross_margin + 0.5))
    daily_breakeven = round(breakeven_customers / 26, 1)  # 26 working days/month

    # Monthly profit at base case: assume 30% above breakeven (typical operating level)
    base_customers = int(breakeven_customers * 1.30)
    revenue = base_customers * ticket
    cost = opex + base_customers * cogs
    ebit = revenue - cost
    pat = ebit * (1 - tax_rate)
    pat_ratio = round((pat / opex) * 100)  # post-tax profit as % of opex

    # Payback = midpoint capex / monthly PAT
    capex_mid = (capex_low + capex_high) / 2
    if pat > 0:
        payback_months = round(capex_mid / pat)
    else:
        payback_months = 99

    return {
        "ticket": ticket,
        "cogs": cogs,
        "breakeven_customers": breakeven_customers,
        "daily_breakeven": daily_breakeven,
        "pat_ratio": pat_ratio,
        "payback_months": payback_months,
    }

# Exchange rates (approximate, mid-2025)
USD = 1.0
AUD_USD = 0.65
SGD_USD = 0.74
HKD_USD = 0.128
JPY_USD = 0.0067
KRW_USD = 0.00073
NTD_USD = 0.031
MYR_USD = 0.22
THB_USD = 0.029
AED_USD = 0.272
VND_USD = 0.000040

def aud(x): return round(x * AUD_USD)
def sgd(x): return round(x * SGD_USD)
def hkd(x): return round(x * HKD_USD)
def jpy(x): return round(x * JPY_USD)
def krw(x): return round(x * KRW_USD)
def ntd(x): return round(x * NTD_USD)
def myr(x): return round(x * MYR_USD)
def thb(x): return round(x * THB_USD)
def aed(x): return round(x * AED_USD)

# ============================================================
# CITY DATA
# ============================================================
# Each entry: (capex_low_usd, capex_high_usd, opex_usd, ticket_usd, cogs_pct, tax_rate, name_in_db, region, format, size, airport_time, risk)
# OPEX = rent + staff (total) + products (% rev from 30% above breakeven, ~8-12%) + utilities + marketing + misc

CITIES = {
    "hcmc": {
        "name": "Ho Chi Minh",
        "region": "Vietnam",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout $20k + Equipment $20k + Deposit 3mo $9k + Legal $3k + Working capital $8k = $60k
        # High-end: same + premium furniture → $72k
        "capex_low": 60000, "capex_high": 72000,
        # OPEX: Rent $3,000 + Staff (2 senior $800 + 2 junior $500 + manager $1,000) $3,600 + Products 12% of base rev + Util $300 + Mktg $400 + Misc $400
        # At ticket $95, base 155 clients: products = 155*$9.50*0.12 ≈ $177 → round up misc
        # Total OPEX: $3,000 + $3,600 + $300 + $400 + $400 = $7,700
        "opex": 7700,
        "ticket": 95, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "30 mins (SGN)", "risk": "Foreign ownership license compliance (IRC/ERC process 2-4 months)",
        "url": "hcmc.html",
    },
    "hanoi": {
        "name": "Hanoi",
        "region": "Vietnam",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout $18k + Equipment $18k + Deposit 3mo $6.6k + Legal $3k + Stock $5k = $51k
        "capex_low": 50000, "capex_high": 62000,
        # OPEX: Rent $2,200 + Staff $3,600 + Products + Util $280 + Mktg $400 + Misc $420 = $6,900
        "opex": 6900,
        "ticket": 95, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "30 mins (HAN)", "risk": "Hard water (TDS 400+ ppm) requires RO filtration investment; foreign license compliance",
        "url": "hanoi.html",
    },
    "danang": {
        "name": "Da Nang",
        "region": "Vietnam",
        "format": "Coastal Expat Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout $12k + Equipment $16k + Deposit 3mo $2.4k + Legal $2.5k + Stock $3k = $36k
        "capex_low": 32000, "capex_high": 42000,
        # OPEX: Rent $800 + Staff $3,200 (3 junior-level expat-trained) + Util $220 + Mktg $350 + Misc $380 = $4,950
        "opex": 4950,
        "ticket": 55, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "12 mins (DAD)", "risk": "Seasonal tourism slump (Nov–Feb monsoon); nomad base fluctuates",
        "url": "danang.html",
    },
    "haiphong": {
        "name": "Hai Phong",
        "region": "Vietnam",
        "format": "Industrial Expat Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout $10k + Equipment $15k + Deposit 3mo $1.95k + Legal $2.5k + Stock $2.5k = $32k
        "capex_low": 28000, "capex_high": 38000,
        # OPEX: Rent $650 + Staff $3,200 + Util $220 + Mktg $250 + Misc $330 = $4,650
        "opex": 4650,
        "ticket": 45, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "15 mins (HPH)", "risk": "Dependency on Deep C / VSIP Korean industrial rotation cycles",
        "url": "haiphong.html",
    },
    "binhduong": {
        "name": "Binh Duong",
        "region": "Vietnam",
        "format": "Industrial Expat Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout $10k + Equipment $14k + Deposit 3mo $1.8k + Legal $2.5k + Stock $2.5k = $31k
        "capex_low": 26000, "capex_high": 36000,
        # OPEX: Rent $600 + Staff $3,200 + Util $200 + Mktg $250 + Misc $300 = $4,550
        "opex": 4550,
        "ticket": 45, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "45 mins (SGN)", "risk": "Korean factory shift rotation cycles; product supply chain from HCMC",
        "url": "binhduong.html",
    },
    "dongnai": {
        "name": "Dong Nai",
        "region": "Vietnam",
        "format": "Industrial Expat Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout $9k + Equipment $13k + Deposit 3mo $1.65k + Legal $2.5k + Stock $2.5k = $29k
        "capex_low": 24000, "capex_high": 34000,
        # OPEX: Rent $550 + Staff $3,000 + Util $190 + Mktg $250 + Misc $310 = $4,300
        "opex": 4300,
        "ticket": 55, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "60 mins (SGN)", "risk": "Zero local competition but small total expat population; 60-min SGN logistics",
        "url": "dongnai.html",
    },
    "kuala_lumpur": {
        "name": "Kuala Lumpur",
        "region": "Malaysia",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout MYR 150k (USD 33k) + Equipment $20k + Deposit 3mo $6k + Legal $3k + Stock $5k = $67k
        "capex_low": 65000, "capex_high": 80000,
        # OPEX: Rent $2,000 + Staff MYR 13.5k USD $2,970 ≈ $3,000 + Products + Util $280 + Mktg $450 + Misc $470 = $6,200
        "opex": 6200,
        "ticket": 90, "cogs_pct": 0.10, "tax": 0.24,
        "airport": "45 mins (KUL)", "risk": "Bangsar clustering — KLCC/Ampang corridor gap vs. 4 competitors in Bangsar",
        "url": "kuala_lumpur.html",
    },
    "johor": {
        "name": "Johor Bahru (RTS)",
        "region": "Malaysia",
        "format": "Cross-Border Premium Salon (RTS PoC)",
        "size": "1,000 sq ft",
        # CAPEX: Fitout MYR 130k (USD 28.6k) + Equipment $18k + Deposit 3mo $5.1k + Legal $2.5k + Stock $4k = $58k
        "capex_low": 52000, "capex_high": 65000,
        # OPEX: Rent $1,700 + Staff $2,800 + Util $260 + Mktg $400 + Misc $340 = $5,500
        "opex": 5500,
        "ticket": 65, "cogs_pct": 0.10, "tax": 0.24,
        "airport": "30 mins (JHB) / 50 mins (SIN)", "risk": "RTS operational delays; Singapore cross-border demand tied to exchange rate sensitivity",
        "url": "johor.html",
    },
    "penang": {
        "name": "Penang",
        "region": "Malaysia",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout MYR 100k (USD 22k) + Equipment $17k + Deposit 3mo $2.4k + Legal $2k + Stock $3.5k = $47k
        "capex_low": 42000, "capex_high": 55000,
        # OPEX: Rent $800 + Staff $2,600 + Util $220 + Mktg $350 + Misc $330 = $4,300
        "opex": 4300,
        "ticket": 55, "cogs_pct": 0.10, "tax": 0.24,
        "airport": "25 mins (PEN)", "risk": "Georgetown heritage DA restrictions on fit-out; limited premium residential density vs. KL",
        "url": "penang.html",
    },
    "sabah": {
        "name": "Sabah",
        "region": "Malaysia",
        "format": "Coastal Expat Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout MYR 90k (USD 19.8k) + Equipment $16k + Deposit 3mo $2.7k + Legal $2k + Stock $3k = $44k
        "capex_low": 38000, "capex_high": 50000,
        # OPEX: Rent $900 + Staff $2,400 + Util $200 + Mktg $300 + Misc $300 = $4,100
        "opex": 4100,
        "ticket": 45, "cogs_pct": 0.10, "tax": 0.24,
        "airport": "20 mins (BKI)", "risk": "Small total expat base; East Malaysia logistics cost for premium product supply",
        "url": "sabah.html",
    },
    "sarawak": {
        "name": "Sarawak",
        "region": "Malaysia",
        "format": "Boutique Expat Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout MYR 85k (USD 18.7k) + Equipment $16k + Deposit 3mo $2.1k + Legal $2k + Stock $3k = $42k
        "capex_low": 36000, "capex_high": 48000,
        # OPEX: Rent $700 + Staff $2,400 + Util $190 + Mktg $280 + Misc $280 = $3,850
        "opex": 3850,
        "ticket": 46, "cogs_pct": 0.10, "tax": 0.24,
        "airport": "20 mins (KCH)", "risk": "Shell/Petronas expat rotation cycles; East Malaysia freight costs for salon products",
        "url": "sarawak.html",
    },
    "singapore": {
        "name": "Singapore",
        "region": "Other APAC",
        "format": "Premium Boutique Salon",
        "size": "750 sq ft",
        # CAPEX: Fitout SGD 90k (USD 66.6k) + Equipment $22k + Deposit 3mo $16.5k + Legal $4k + Stock $6k = $115k
        "capex_low": 110000, "capex_high": 128000,
        # OPEX: Rent $5,500 + Staff SGD 13.5k ($10k) + Products + Util SGD 1,800 ($1,332) + Mktg $800 + Misc $600 = $18,232
        "opex": 18200,
        "ticket": 180, "cogs_pct": 0.10, "tax": 0.17,
        "airport": "25 mins (SIN)", "risk": "Extremely high rent overheads; Holland V lease competition from F&B operators",
        "url": "singapore.html",
    },
    "hongkong": {
        "name": "Hong Kong",
        "region": "Other APAC",
        "format": "Premium Boutique Salon (MVP)",
        "size": "750 sq ft",
        # CAPEX: Fitout HKD 600k (USD 76.8k) + Equipment $22k + Deposit 3mo $25.5k + Legal $4k + Stock $6k = $134k
        "capex_low": 130000, "capex_high": 155000,
        # OPEX: Rent $8,500 + Staff HKD 57k ($7,296) ≈ $7,300 + Util HKD 6k ($768) + Mktg $800 + Misc $600 = $17,968
        "opex": 18000,
        "ticket": 200, "cogs_pct": 0.10, "tax": 0.165,
        "airport": "40 mins (HKG)", "risk": "Ultra-high commercial rent; Causeway Bay lease scarcity and key money demands",
        "url": "hongkong.html",
    },
    "bangkok": {
        "name": "Bangkok",
        "region": "Other APAC",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout THB 1.5M (USD 43.5k) + Equipment $20k + Deposit 3mo $15k + Legal $3k + RO filtration $5k + Stock $5k = $91k
        "capex_low": 88000, "capex_high": 108000,
        # OPEX: Rent $5,000 + Staff THB 150k ($4,350) + Util THB 8k ($232) + Mktg $600 + Misc $500 = $10,682
        "opex": 10700,
        "ticket": 160, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "30 mins (BKK) / 35 mins (DMK)", "risk": "Hard water (TDS 300–500 ppm) RO filtration critical; high Thonglor rent premium",
        "url": "bangkok.html",
    },
    "macau": {
        "name": "Macau",
        "region": "Other APAC",
        "format": "Premium Boutique Salon (MVP)",
        "size": "750 sq ft",
        # CAPEX: Fitout HKD 350k (USD 44.8k) + Equipment $18k + Deposit 3mo $5.4k + Legal $3k + RO $3k + Stock $4k = $78k
        "capex_low": 72000, "capex_high": 88000,
        # OPEX: Rent $1,800 + Staff HKD 42k ($5,376) + Util $400 + Mktg $500 + Misc $400 = $8,476
        "opex": 8500,
        "ticket": 130, "cogs_pct": 0.10, "tax": 0.12,
        "airport": "15 mins (MFM)", "risk": "Casino industry cyclicality; soft-water filtration import logistics from HK",
        "url": "macau.html",
    },
    "dubai": {
        "name": "Dubai",
        "region": "Middle East",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout AED 200k (USD 54.4k) + Equipment $22k + Deposit 1yr rent upfront $42k + Legal $4k + RO heavy-duty $8k + Stock $6k = $136k
        # Dubai: annual lease paid upfront → 12mo rent = $42k is the deposit
        "capex_low": 120000, "capex_high": 145000,
        # OPEX: Rent $3,500 + Staff AED 38k ($10,336) + Util AED 3k ($816) + Mktg $800 + Misc $600 = $16,052
        "opex": 16000,
        "ticket": 160, "cogs_pct": 0.10, "tax": 0.09,
        "airport": "15 mins (DXB)", "risk": "Extreme hard water (TDS 500–1200 ppm) — heavy RO investment; annual lease pre-payment UAE norm",
        "url": "dubai.html",
    },
    "taipei": {
        "name": "Taipei",
        "region": "Taiwan",
        "format": "Premium Boutique Salon",
        "size": "850 sq ft",
        # CAPEX: Fitout NTD 1.8M (USD 55.8k) + Equipment $20k + Deposit 3mo $6.6k + Legal $3k + Stock $5k = $90k
        "capex_low": 85000, "capex_high": 105000,
        # OPEX: Rent $2,200 + Staff NTD 165k ($5,115) + Util NTD 8k ($248) + Mktg $600 + Misc $500 = $8,663
        "opex": 8700,
        "ticket": 104, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "15 mins (TSA) / 45 mins (TPE)", "risk": "Intense local competition; 6–9 hr wait at top competitors creates booking model risk",
        "url": "taipei.html",
    },
    "taichung": {
        "name": "Taichung",
        "region": "Taiwan",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout NTD 1.5M (USD 46.5k) + Equipment $18k + Deposit 3mo $5.4k + Legal $2.5k + Stock $4.5k = $76.9k
        "capex_low": 72000, "capex_high": 88000,
        # OPEX: Rent $1,800 + Staff NTD 150k ($4,650) + Util NTD 7k ($217) + Mktg $500 + Misc $450 = $7,617
        "opex": 7600,
        "ticket": 110, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "30 mins (RMQ)", "risk": "Qi-qi premium rent inflation; experienced colour stylist scarcity vs. local Taiwanese market",
        "url": "taichung.html",
    },
    "kaohsiung": {
        "name": "Kaohsiung",
        "region": "Taiwan",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout NTD 1.2M (USD 37.2k) + Equipment $17k + Deposit 3mo $3.6k + Legal $2k + Stock $4k = $63.8k
        "capex_low": 58000, "capex_high": 72000,
        # OPEX: Rent $1,200 + Staff NTD 130k ($4,030) + Util NTD 6k ($186) + Mktg $450 + Misc $400 = $6,266
        "opex": 6300,
        "ticket": 120, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "15 mins (KHH)", "risk": "THSR Zuoying first-mover reliant on commuter appointment behavior; Round2/UCA Lingya competition",
        "url": "kaohsiung.html",
    },
    "tainan": {
        "name": "Tainan",
        "region": "Taiwan",
        "format": "Premium Boutique Salon (MVP)",
        "size": "750 sq ft",
        # CAPEX: Fitout NTD 1.1M (USD 34.1k) + Equipment $16k + Deposit 3mo $2.7k + Legal $2k + Stock $3.5k = $58.3k
        "capex_low": 52000, "capex_high": 66000,
        # OPEX: Rent $900 + Staff NTD 120k ($3,720) + Util NTD 5.5k ($171) + Mktg $400 + Misc $350 = $5,541
        "opex": 5500,
        "ticket": 80, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "35 mins (TNN) / 50 mins (KHH)", "risk": "TSMC Sinshih expat base still ramping — 2025-2027 growth dependency",
        "url": "tainan.html",
    },
    "fukuoka": {
        "name": "Fukuoka",
        "region": "Japan",
        "format": "Premium Boutique Salon (MVP)",
        "size": "900 sq ft",
        # CAPEX: Fitout JPY 15M (USD 100.5k) + Equipment $20k + Deposit 3mo $4.8k + Legal $3k + Stock $5k = $133k
        "capex_low": 125000, "capex_high": 150000,
        # OPEX: Rent $1,600 + Staff JPY 1.1M ($7,370) + Util JPY 80k ($536) + Mktg $500 + Misc $500 = $10,506
        "opex": 10500,
        "ticket": 95, "cogs_pct": 0.10, "tax": 0.30,
        "airport": "15 mins (FUK)", "risk": "30% JP corporate tax + high fitout cost; intense TONI&GUY/saco japan competition in Tenjin/Daimyo",
        "url": "fukuoka.html",
    },
    "okinawa": {
        "name": "Okinawa",
        "region": "Japan",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout JPY 12M (USD 80.4k) + Equipment $18k + Deposit 3mo $3.3k + Legal $3k + Stock $5k = $110k
        "capex_low": 100000, "capex_high": 122000,
        # OPEX: Rent $1,100 + Staff JPY 900k ($6,030) + Util JPY 65k ($435) + Mktg $500 + Misc $500 = $8,565
        "opex": 8600,
        "ticket": 120, "cogs_pct": 0.10, "tax": 0.30,
        "airport": "15 mins (OKA)", "risk": "Bilingual (English/Korean) stylist recruitment very difficult; 30% JP tax burden",
        "url": "okinawa.html",
    },
    "busan": {
        "name": "Busan",
        "region": "South Korea",
        "format": "Ground-Floor Premium Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout KRW 80M (USD 58.4k) + Equipment $18k + Deposit 3mo $6.6k + Legal $2.5k + Stock $5k = $90.5k
        "capex_low": 85000, "capex_high": 105000,
        # OPEX: Rent $2,200 + Staff KRW 8.4M ($6,132) + Util KRW 700k ($511) + Mktg $500 + Misc $500 = $9,843
        "opex": 9800,
        "ticket": 100, "cogs_pct": 0.10, "tax": 0.20,
        "airport": "30 mins (PUS)", "risk": "K-franchise dominance (Juno Hair 200+ outlets); Marine City appointment-only model requires strong pre-booking system",
        "url": "busan.html",
    },
    "sydney": {
        "name": "Sydney",
        "region": "Australia",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout AUD 140k (USD 91k) + Equipment $22k + Deposit 3mo $9.6k + Legal $4k + Stock $6k = $132.6k
        "capex_low": 128000, "capex_high": 155000,
        # OPEX: Rent $3,200 + Staff AUD 24k ($15,600) → 2 seniors + 1 junior = AUD 19,500 ($12,675) + Util AUD 1,500 ($975) + Mktg $800 + Misc $600 = $18,250
        "opex": 18200,
        "ticket": 250, "cogs_pct": 0.10, "tax": 0.30,
        "airport": "22 mins (SYD)", "risk": "High AU labour costs (Award + 11.5% superannuation); inner-west DA heritage restrictions on fit-out",
        "url": "sydney.html",
    },
    "melbourne": {
        "name": "Melbourne",
        "region": "Australia",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout AUD 135k (USD 87.75k) + Equipment $22k + Deposit 3mo $10.5k + Legal $4k + Stock $6k = $130k
        "capex_low": 125000, "capex_high": 150000,
        # OPEX: Rent $3,500 + Staff AUD 22k ($14,300) + Util AUD 1,400 ($910) + Mktg $750 + Misc $600 = $20,060
        "opex": 20000,
        "ticket": 220, "cogs_pct": 0.10, "tax": 0.30,
        "airport": "30 mins (MEL)", "risk": "High AU labour + superannuation burden; Chapel St rent inflation and lease competition from F&B",
        "url": "melbourne.html",
    },
    "brisbane": {
        "name": "Brisbane",
        "region": "Australia",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout AUD 120k (USD 78k) + Equipment $20k + Deposit 3mo $8.4k + Legal $3.5k + Stock $5k = $115k
        "capex_low": 108000, "capex_high": 132000,
        # OPEX: Rent $2,800 + Staff AUD 19k ($12,350) + Util AUD 1,200 ($780) + Mktg $650 + Misc $550 = $17,130
        "opex": 17100,
        "ticket": 240, "cogs_pct": 0.10, "tax": 0.30,
        "airport": "20 mins (BNE)", "risk": "High AU labour costs and superannuation; UV-damaged colour turnover requires more frequent client visits",
        "url": "brisbane.html",
    },
    "perth": {
        "name": "Perth",
        "region": "Australia",
        "format": "Coastal Expat Salon (MVP)",
        "size": "800 sq ft",
        # CAPEX: Fitout AUD 115k (USD 74.75k) + Equipment $19k + Deposit 3mo $6k + Legal $3k + Stock $5k = $107.75k
        "capex_low": 100000, "capex_high": 120000,
        # OPEX: Rent $2,000 + Staff AUD 17k ($11,050) + Util AUD 1,100 ($715) + Mktg $600 + Misc $500 = $14,865
        "opex": 14900,
        "ticket": 200, "cogs_pct": 0.10, "tax": 0.30,
        "airport": "22 mins (PER)", "risk": "FIFO schedule volatility; isolation from east-coast premium product supply chain",
        "url": "perth.html",
    },
}

# ============================================================
# Compute derived metrics for each city
# ============================================================

results = {}
for key, c in CITIES.items():
    m = compute(c["capex_low"], c["capex_high"], c["opex"], c["ticket"], c["cogs_pct"], c["tax"])
    results[key] = {**c, **m}

# ============================================================
# Print summary
# ============================================================
print("=== RESEARCH-BACKED FINANCIAL SUMMARY ===\n")
print(f"{'City':<15} {'CAPEX':>16} {'OPEX':>10} {'Ticket':>8} {'Breakevn':>10} {'Daily':>7} {'PAT%':>7} {'Payback':>9}")
print("-" * 90)
for key, r in results.items():
    print(f"{r['name']:<15} USD {r['capex_low']:>6}k-{r['capex_high']:>3}k  ${r['opex']:>6}  ${r['ticket']:>5}  {r['breakeven_customers']:>6} cust  {r['daily_breakeven']:>5}/day  {r['pat_ratio']:>5}%  {r['payback_months']:>5}mo")

print("\n\n=== UPDATING script.js citiesDb ===\n")

JS_FILE = os.path.join(WORKDIR, "script.js")
with open(JS_FILE, "r", encoding="utf-8") as f:
    content = f.read()

def fmt_capex(low, high):
    return f"USD {low//1000}k - {high//1000}k"

def fmt_opex(opex):
    return f"USD {opex:,}"

def fmt_ticket(t):
    return f"USD {t}"

def fmt_cogs(t, pct):
    return f"USD {round(t * pct, 2):.2f}"

def fmt_breakeven(b):
    return f"~{b} customers"

def fmt_daily(d):
    return f"~{d} customers/day"

def fmt_pat(p):
    return f"{p}% (Post-Tax)"

def fmt_payback(p):
    if p >= 99:
        return "N/A"
    return f"{p} Months"

# Build replacement maps
changed = 0
for key, r in results.items():
    name = r["name"]
    # Find the city block by name
    city_pattern = re.compile(
        r'(\{\s*"name":\s*"' + re.escape(name) + r'".*?"url":\s*"' + re.escape(r["url"]) + r'"\s*\})',
        re.DOTALL
    )
    m = city_pattern.search(content)
    if not m:
        print(f"  ✗ Could not find block for: {name}")
        continue
    old_block = m.group(1)
    new_block = old_block

    # Replace each field
    fields = [
        (r'"capex":\s*"[^"]*"', f'"capex": "{fmt_capex(r["capex_low"], r["capex_high"])}"'),
        (r'"opex":\s*"[^"]*"', f'"opex": "{fmt_opex(r["opex"])}"'),
        (r'"ticket":\s*"[^"]*"', f'"ticket": "{fmt_ticket(r["ticket"])}"'),
        (r'"cogs":\s*"[^"]*"', f'"cogs": "{fmt_cogs(r["ticket"], r["cogs_pct"])}"'),
        (r'"margin":\s*"[^"]*"', '"margin": "90%"'),
        (r'"breakeven":\s*"[^"]*"', f'"breakeven": "{fmt_breakeven(r["breakeven_customers"])}"'),
        (r'"daily_breakeven":\s*"[^"]*"', f'"daily_breakeven": "{fmt_daily(r["daily_breakeven"])}"'),
        (r'"tax":\s*"[^"]*"', f'"tax": "{r["tax"]*100:.1f}%"'),
        (r'"pat_ratio":\s*"[^"]*"', f'"pat_ratio": "{fmt_pat(r["pat_ratio"])}"'),
        (r'"payback":\s*"[^"]*"', f'"payback": "{fmt_payback(r["payback_months"])}"'),
        (r'"risk":\s*"[^"]*"', f'"risk": "{r["risk"]}"'),
        (r'"format":\s*"[^"]*"', f'"format": "{r["format"]}"'),
    ]
    for pattern, replacement in fields:
        new_block = re.sub(pattern, replacement, new_block, count=1)

    content = content[:m.start()] + new_block + content[m.end():]
    print(f"  ✓ Updated: {name}")
    changed += 1

with open(JS_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone. {changed} city blocks updated in script.js.")
