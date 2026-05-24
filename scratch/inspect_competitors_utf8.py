import os
import re
import json
import sys

folder = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
files = [f for f in os.listdir(folder) if f.endswith(".html") and f != "index.html" and f != "competitor_map.html"]

output_path = os.path.join(folder, "scratch", "competitors.txt")

with open(output_path, "w", encoding="utf-8") as out:
    out.write("=== COMPETITOR DATA PER PAGE ===\n")
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
            if not names:
                # Try single quotes
                names = re.findall(r"name:\s*'(.*?)'", array_content)
                comments = re.findall(r"comment:\s*'(.*?)'", array_content)
            
            out.write(f"\n--- {file} ---\n")
            for name, comm in zip(names, comments):
                out.write(f"  * {name}: {comm}\n")
        else:
            out.write(f"\n--- {file} --- NO COMPETITORS ARRAY FOUND\n")

print(f"Competitor data written successfully to {output_path}")
