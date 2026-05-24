import json
import os
import re

folder = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

# Read city_data.json
with open(os.path.join(folder, "city_data.json"), "r", encoding="utf-8") as f:
    cities_data = json.load(f)

print(f"{'City':<22} {'Excel Gap %':<12} {'Cand A Gap %':<12}")
print("-" * 50)

def parse_javascript_objects(array_str):
    blocks = re.findall(r"\{([^}]+)\}", array_str, re.DOTALL)
    objects = []
    for b in blocks:
        obj = {}
        # Parse name
        name_match = re.search(r"name\s*:\s*([\"'`])(.*?)\1", b)
        if name_match: obj["name"] = name_match.group(2)
        
        # Parse catchment
        catch_match = re.search(r"catchment\s*:\s*(\d+)", b)
        if catch_match: obj["catchment"] = int(catch_match.group(1))
        
        # Parse premiumTargetPct
        target_match = re.search(r"premiumTargetPct\s*:\s*(\d+)", b)
        if target_match: obj["premiumTargetPct"] = int(target_match.group(1))
        
        # Parse competitorCapacity
        cap_match = re.search(r"competitorCapacity\s*:\s*(\d+)", b)
        if cap_match: obj["competitorCapacity"] = int(cap_match.group(1))
        
        objects.append(obj)
    return objects

for city in cities_data:
    name = city["name"]
    url = city["url"]
    path = os.path.join(folder, url)
    excel_gap = city["underserved_raw"]
    
    cand_gap = "N/A"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        cands_match = re.search(r"(?:const|let)\s+candidates\s*=\s*(\[.*?\]);", content, re.DOTALL)
        if cands_match:
            cands = parse_javascript_objects(cands_match.group(1))
            if cands:
                cand_a = cands[0]
                catchment = cand_a.get("catchment", 0)
                pct = cand_a.get("premiumTargetPct", 0)
                cap = cand_a.get("competitorCapacity", 0)
                
                target_demand = round(catchment * (pct / 100))
                gap = max(0, target_demand - cap)
                if target_demand > 0:
                    cand_gap = round((gap / target_demand) * 100)
                
    print(f"{name:<22} {excel_gap:<12} {cand_gap:<12}")
