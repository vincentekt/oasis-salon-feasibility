"""
fix_capex_format.py — Fixes the citiesDb capex display (60000k → 60k)
and also rechecks all PAT ratios which need to be run at a more realistic
operating level (50% above breakeven = 1.5x, not 1.3x).
"""
import os, re

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
JS_FILE = os.path.join(WORKDIR, "script.js")

with open(JS_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Fix: "USD 60000k - 72000k" → "USD 60k - 72k"
def fix_capex(m):
    raw = m.group(0)
    # Extract numbers
    nums = re.findall(r'(\d+)k', raw)
    if not nums:
        return raw
    fixed_nums = []
    for n in nums:
        val = int(n)
        if val > 999:
            fixed_nums.append(str(val // 1000))
        else:
            fixed_nums.append(n)
    result = raw
    for orig, fixed in zip(nums, fixed_nums):
        result = result.replace(orig + 'k', fixed + 'k', 1)
    return result

# Fix capex strings: "USD NNNNNk - NNNNNk"
content = re.sub(r'USD\s+\d+k\s*-\s*\d+k', fix_capex, content)

print("Fixed CAPEX display format.")

# Now let's also recalculate PAT ratios and payback at a more realistic
# operating level. Using 1.5x breakeven (50% above):
# This gives a better representation of steady-state operations.

CITIES_OVERRIDE = {
    # (opex, ticket, cogs_pct, tax, capex_mid)
    "Ho Chi Minh":       (7700,  95,  0.10, 0.20, 66000),
    "Hanoi":             (6900,  95,  0.10, 0.20, 56000),
    "Da Nang":           (4950,  55,  0.10, 0.20, 37000),
    "Hai Phong":         (4650,  45,  0.10, 0.20, 33000),
    "Binh Duong":        (4550,  45,  0.10, 0.20, 31000),
    "Dong Nai":          (4300,  55,  0.10, 0.20, 29000),
    "Kuala Lumpur":      (6200,  90,  0.10, 0.24, 72500),
    "Johor Bahru (RTS)": (5500,  65,  0.10, 0.24, 58500),
    "Penang":            (4300,  55,  0.10, 0.24, 48500),
    "Sabah":             (4100,  45,  0.10, 0.24, 44000),
    "Sarawak":           (3850,  46,  0.10, 0.24, 42000),
    "Singapore":         (18200, 180, 0.10, 0.17, 119000),
    "Hong Kong":         (18000, 200, 0.10, 0.165,142500),
    "Bangkok":           (10700, 160, 0.10, 0.20, 98000),
    "Macau":             (8500,  130, 0.10, 0.12, 80000),
    "Dubai":             (16000, 160, 0.10, 0.09, 132500),
    "Taipei":            (8700,  104, 0.10, 0.20, 95000),
    "Taichung":          (7600,  110, 0.10, 0.20, 80000),
    "Kaohsiung":         (6300,  120, 0.10, 0.20, 65000),
    "Tainan":            (5500,  80,  0.10, 0.20, 59000),
    "Fukuoka":           (10500, 95,  0.10, 0.30, 137500),
    "Okinawa":           (8600,  120, 0.10, 0.30, 111000),
    "Busan":             (9800,  100, 0.10, 0.20, 95000),
    "Sydney":            (18200, 250, 0.10, 0.30, 141500),
    "Melbourne":         (20000, 220, 0.10, 0.30, 137500),
    "Brisbane":          (17100, 240, 0.10, 0.30, 120000),
    "Perth":             (14900, 200, 0.10, 0.30, 110000),
}

print("\nCity PAT ratios at 1.5x breakeven (steady-state operations):")
print(f"{'City':<25} {'Breakeven':>10} {'1.5x clients':>13} {'PAT/mo':>10} {'PAT/OPEX':>10} {'Payback':>9}")
print("-" * 85)

city_overrides = {}
for city, (opex, ticket, cogs_pct, tax, capex_mid) in CITIES_OVERRIDE.items():
    cogs = ticket * cogs_pct
    gm = ticket - cogs
    be = int(opex / gm + 0.5)
    operating_clients = int(be * 1.5)
    revenue = operating_clients * ticket
    total_cost = opex + operating_clients * cogs
    ebit = revenue - total_cost
    pat = ebit * (1 - tax)
    pat_ratio = round((pat / opex) * 100)
    if pat > 0:
        payback = round(capex_mid / pat)
    else:
        payback = 99
    print(f"{city:<25} {be:>9} cust  {operating_clients:>8} cust  ${pat:>8,.0f}  {pat_ratio:>8}%  {payback:>6} mo")
    city_overrides[city] = {"pat_ratio": pat_ratio, "payback": payback, "breakeven": be}

# Apply to script.js
print("\n=== Applying PAT ratio and payback corrections to script.js ===\n")
changed = 0
for city, data in city_overrides.items():
    # Find and replace pat_ratio
    # Pattern: find the city block and update these two fields
    city_pattern = re.compile(
        r'("name":\s*"' + re.escape(city) + r'".*?"pat_ratio":\s*")[^"]*(".*?"payback":\s*")[^"]*(")',
        re.DOTALL
    )
    def make_replacement(d):
        def replacer(m):
            return (m.group(1) + f"{d['pat_ratio']}% (Post-Tax)" +
                    m.group(2) + f"{d['payback']} Months" + m.group(3))
        return replacer
    
    new_content, n = city_pattern.subn(make_replacement(data), content, count=1)
    if n:
        content = new_content
        changed += 1
        # Also fix breakeven
        be_pattern = re.compile(
            r'("name":\s*"' + re.escape(city) + r'".*?"breakeven":\s*")[^"]*(".*?"daily_breakeven":\s*")[^"]*(")',
            re.DOTALL
        )
        daily = round(data['breakeven'] / 26, 1)
        def make_be_repl(b, d):
            def replacer(m):
                return m.group(1) + f"~{b} customers" + m.group(2) + f"~{d} customers/day" + m.group(3)
            return replacer
        content, _ = be_pattern.subn(make_be_repl(data['breakeven'], daily), content, count=1)
        print(f"  ✓ {city}: PAT={data['pat_ratio']}%, Payback={data['payback']}mo, Breakeven={data['breakeven']} clients")
    else:
        print(f"  ✗ NOT FOUND: {city}")

with open(JS_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone. {changed} cities corrected.")
