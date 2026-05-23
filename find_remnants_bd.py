with open(r'c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web\binhduong.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

keywords = ["vip pods", "private pods", "starlight", "upstairs", "head spa", 
            "mist systems", "scalp wellness", "scalp scan", "micro-camera", "vip pod"]

for idx, line in enumerate(lines):
    for kw in keywords:
        if kw in line.lower():
            print(f"Line {idx+1} ({kw}): {line.strip()}")
