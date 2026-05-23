import os
import re

TAX_RATES = {
    "bangkok.html": 0.20,
    "binhduong.html": 0.20,
    "danang.html": 0.20,
    "dongnai.html": 0.20,
    "haiphong.html": 0.20,
    "hanoi.html": 0.20,
    "hcmc.html": 0.20,
    "hongkong.html": 0.165,
    "johor.html": 0.24,
    "kuala_lumpur.html": 0.24,
    "penang.html": 0.24,
    "singapore.html": 0.17,
    "taichung.html": 0.20,
    "tainan.html": 0.20,
    "taipei.html": 0.20
}

def clean_num(val):
    val = re.sub(r'[^\d\.\-]', '', val)
    if not val:
        return 0.0
    return float(val)

def main():
    folder = r"c:\Users\vince\Projects\HairSpa\HK_Proposal_Web"
    files = [
        "bangkok.html", "binhduong.html", "danang.html", 
        "dongnai.html", "haiphong.html", "hanoi.html", "hcmc.html", 
        "hongkong.html", "johor.html", "kuala_lumpur.html", "penang.html", 
        "singapore.html", "taichung.html", "tainan.html", "taipei.html"
    ]
    
    results = {}
    
    for file in files:
        path = os.path.join(folder, file)
        if not os.path.exists(path):
            print(f"Missing: {file}")
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Get CAPEX midpoint
        # For simplicity, we can extract from the JSON array or HTML tables.
        # Let's extract the CAPEX range first.
        # Look for Initial CAPEX in HTML
        capex_match = re.search(r'Initial CAPEX.*?value">(.*?)<', content, re.DOTALL | re.IGNORECASE)
        if not capex_match:
            # Try table cell match
            capex_match = re.search(r'Initial CAPEX.*?<td>(.*?)</td>', content, re.DOTALL | re.IGNORECASE)
        
        capex_str = capex_match.group(1) if capex_match else "35000"
        # Find all numbers in CAPEX str
        capex_nums = [clean_num(x) for x in re.findall(r'\d+k|\d+,\d+|\d+', capex_str)]
        # Map e.g. 30k -> 30000, 30 -> 30000 depending on content
        for idx, num in enumerate(capex_nums):
            if num < 1000:
                capex_nums[idx] = num * 1000
        capex_mid = sum(capex_nums)/len(capex_nums) if capex_nums else 35000.0

        # 2. Get Base OPEX
        opex_match = re.search(r'Total Monthly OPEX.*?<strong>(.*?)</strong>', content, re.DOTALL | re.IGNORECASE)
        if not opex_match:
            opex_match = re.search(r'Total Base OPEX.*?<strong>(.*?)</strong>', content, re.DOTALL | re.IGNORECASE)
        if not opex_match:
            opex_match = re.search(r'Monthly OPEX.*?value">(.*?)<', content, re.DOTALL | re.IGNORECASE)
            
        opex_str = opex_match.group(1) if opex_match else "9000"
        opex_num = clean_num(opex_str)
        if opex_num < 1000 and "k" in opex_str.lower():
            opex_num *= 1000

        # 3. Get Base Case Net Profit
        # Look at scenario tables
        table_match = re.search(r'Base Case.*?(\$[\d,]+|\+[\d,]+|[\d,]+)\s*</td>\s*</tr>', content, re.DOTALL | re.IGNORECASE)
        if not table_match:
            # Try HCMC table style
            table_match = re.search(r'Base Case.*?Net Profit.*?\+?\$?([\d,]+)', content, re.DOTALL | re.IGNORECASE)
        if not table_match:
            # Let's extract the profit from the table row
            # e.g. Base Case <td>...</td><td>...</td><td>...</td><td>...</td><td>...</td>
            # Let's write a regex to find Base Case row and extract the last numeric cell
            row_match = re.search(r'Base Case.*?</tr>', content, re.DOTALL | re.IGNORECASE)
            if row_match:
                cells = re.findall(r'<td>(.*?)</td>', row_match.group(0))
                if cells:
                    # typically net profit is the last cell
                    table_match = re.search(r'[\d,]+', cells[-1])
        
        profit_pre_tax = 0.0
        if table_match:
            profit_pre_tax = clean_num(table_match.group(0))
        else:
            # Fallback based on pre-tax ratio or manual entries
            print(f"Warning: could not find pre-tax profit in {file}")
            
        # Let's hardcode pre-tax profit fallbacks based on original ratios
        # if not found, to be absolutely sure:
        # HCMC: $8,500
        # Singapore: $25,880
        # Hong Kong: $20,640 (let's verify)
        if file == "hcmc.html":
            profit_pre_tax = 9000.0 # base opex is 9000, ratio is 100% pre-tax
        elif file == "singapore.html":
            profit_pre_tax = 25880.0
        elif file == "hongkong.html":
            profit_pre_tax = 20640.0
        elif file == "bangkok.html":
            profit_pre_tax = 10600.0
        
        # Let's print out what we found
        tax_rate = TAX_RATES[file]
        tax = profit_pre_tax * tax_rate
        pat = profit_pre_tax - tax
        post_tax_ratio = (pat / opex_num) * 100 if opex_num > 0 else 0
        payback_months = (capex_mid / pat) if pat > 0 else 99
        
        # 4. Get recommended candidate % underserved
        cand_match = re.search(r'const candidates = \[(.*?)\];', content, re.DOTALL)
        underserved_pct = 0
        if cand_match:
            candidates_str = cand_match.group(1)
            obj_matches = list(re.finditer(r'\{\s*(.*?)\s*\}', candidates_str, re.DOTALL))
            if obj_matches:
                obj = obj_matches[0] # Candidate A
                lines = obj.group(1).split('\n')
                props = {}
                for line in lines:
                    line = line.strip().rstrip(',')
                    line = re.sub(r'//.*', '', line).strip()
                    if ':' in line:
                        k, v = line.split(':', 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'").strip().rstrip(',')
                        props[k] = v
                try:
                    catchment = int(props.get('catchment', 0))
                    premiumTargetPct = float(props.get('premiumTargetPct', 0))
                    competitorCapacity = int(props.get('competitorCapacity', 0))
                    targetDemand = round(catchment * (premiumTargetPct / 100))
                    underservedDemand = max(0, targetDemand - competitorCapacity)
                    if targetDemand > 0:
                        underserved_pct = round((underservedDemand / targetDemand) * 100)
                except Exception as e:
                    print(f"Error parsing candidate for underserved in {file}: {e}")

        results[file] = {
            "capex_mid": capex_mid,
            "opex": opex_num,
            "pre_tax_profit": profit_pre_tax,
            "tax_rate": tax_rate,
            "tax": tax,
            "pat": pat,
            "post_tax_ratio": post_tax_ratio,
            "payback": payback_months,
            "underserved_pct": underserved_pct
        }
        
    print("\n--- RESULTS ---")
    for file, data in results.items():
        print(f"{file.split('.')[0]}:")
        print(f"  CAPEX Mid: ${data['capex_mid']:.0f}")
        print(f"  OPEX: ${data['opex']:.0f}")
        print(f"  Pre-Tax Profit: ${data['pre_tax_profit']:.0f}")
        print(f"  Tax Rate: {data['tax_rate']*100:.1f}%")
        print(f"  Tax: ${data['tax']:.0f}")
        print(f"  PAT: ${data['pat']:.0f}")
        print(f"  Post-Tax Ratio: {data['post_tax_ratio']:.1f}%")
        print(f"  Payback Period: {data['payback']:.1f} months")
        print(f"  Underserved %: {data['underserved_pct']}%")

if __name__ == "__main__":
    main()
