import os
import re

folder = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
files = [f for f in os.listdir(folder) if f.endswith(".html") and f != "index.html" and f != "competitor_map.html"]

keywords = [
    "vip pods", "private pods", "starlight", "upstairs", "head spa", 
    "mist systems", "scalp wellness", "scalp scan", "micro-camera"
]

print("=== REMNANT KEYWORD COUNTS ===")
for file in sorted(files):
    path = os.path.join(folder, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().lower()
    
    found = []
    for kw in keywords:
        count = content.count(kw)
        if count > 0:
            found.append(f"{kw}: {count}")
    
    if found:
        print(f"{file}: {', '.join(found)}")
