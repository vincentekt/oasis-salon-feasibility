import os
import re
import json

folder = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
files = [f for f in os.listdir(folder) if f.endswith(".html") and f != "index.html" and f != "competitor_map.html"]

print("=== COMPETITOR DATA PER PAGE ===")
for file in sorted(files):
    path = os.path.join(folder, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract competitors array
    comp_match = re.search(r'const competitors = \[(.*?)\];', content, re.DOTALL)
    if comp_match:
        array_content = comp_match.group(1).strip()
        # Find names and notes/comments
        names = re.findall(r'name:\s*"(.*?)"', array_content)
        comments = re.findall(r'comment:\s*"(.*?)"', array_content)
        print(f"\n--- {file} ---")
        for name, comm in zip(names, comments):
            print(f"  * {name}: {comm}")
    else:
        print(f"\n--- {file} --- NO COMPETITORS ARRAY FOUND")
