import os, re

folder = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
with open(os.path.join(folder, "bangkok.html"), "r", encoding="utf-8") as f:
    html = f.read()

# Find the script block with map/candidate data
m = re.search(r'const candidates\s*=.*?(?=const |</script>)', html, re.DOTALL)
if m:
    print(m.group()[:6000])
else:
    # Try to find candidates/coords
    m2 = re.search(r'candidates.*?\[.*?\]', html, re.DOTALL)
    if m2:
        print(m2.group()[:3000])
    # Show all JS const declarations
    consts = re.findall(r'const \w+', html)
    print("JS consts:", consts[:30])
