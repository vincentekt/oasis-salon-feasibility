import os, re

folder = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
with open(os.path.join(folder, "bangkok.html"), "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r'<section id="location-study".*?</section>', html, re.DOTALL)
if m:
    print(m.group()[:5000])
else:
    # Try candidates section
    m2 = re.search(r'<section id="candidates".*?</section>', html, re.DOTALL)
    if m2:
        print(m2.group()[:5000])
    else:
        # Show all section ids
        ids = re.findall(r'<section id="([^"]+)"', html)
        print("Section IDs found:", ids)
