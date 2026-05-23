import os
import re

files = [f for f in os.listdir(".") if f.endswith(".html") and f != "index.html" and f != "competitor_map.html"]

keywords = [
    r'\bhead spa\b',
    r'\bvip pods?\b',
    r'\bprivate pods?\b',
    r'\bstarlight\b',
    r'\brelaxation suites?\b',
    r'\bspa poc\b',
    r'\bscalp spa\b'
]

print("=== OLD MODEL TERMINOLOGY DETECTED ===")
for f in sorted(files):
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
        
    found = []
    for kw in keywords:
        matches = re.findall(kw, content, re.IGNORECASE)
        if matches:
            found.append(f"{kw.replace(r'\\b', '')} ({len(matches)}x)")
            
    if found:
        print(f"{f}: {', '.join(found)}")
