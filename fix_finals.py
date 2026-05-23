"""Fix the final 8 remnant lines across specific files."""
import os

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

fixes = {
    "binhduong.html": [
        ("Low-cost local hair washes and standard beauty salons, but zero specialized acoustic Japanese head spas.",
         "Low-cost local hair salons and standard beauty shops, but zero premium boutique styling studios with soft-water filtration and specialized technical coloring."),
    ],
    "danang.html": [
        ("Dozens of low-cost traditional shampoo parlors, but zero specialized acoustic Japanese head spas.",
         "Dozens of low-cost traditional shampoo parlors, but zero premium boutique styling salons with international coloring techniques and soft-water filtration."),
    ],
    "hanoi.html": [
        ("Intense competition in low-cost hair washes, but zero high-end head spas with proper styling stations and specialized scalp care technology.",
         "Intense competition from low-cost local hair salons, but no premium ground-floor boutique salons with specialist balayage/highlights expertise, demineralized water filtration, and private styling bays."),
    ],
    "johor.html": [
        ("JB has plenty of massage parlors (foot/body) and standard hair salons, but lacks premium, specialized head spas focusing on custom track lighting quiet sensory relaxation.",
         "JB has plenty of budget hair salons and beauty chains, but lacks premium ground-floor boutique salons specializing in advanced technical coloring, balayage, and soft-water hair therapy with a high-end studio aesthetic."),
    ],
    "penang.html": [
        ("<td>Scientific Scalp Scan</td>", "<td>Hair Health Consultation</td>"),
    ],
    "sabah.html": [
        ("<td>Scientific Scalp Scan</td>", "<td>Hair Health Consultation</td>"),
    ],
    "sarawak.html": [
        ("<td>Scientific Scalp Scan</td>", "<td>Hair Health Consultation</td>"),
    ],
    "taipei.html": [
        ("<td>Consultation & Scalp Scan</td>", "<td>Styling Consultation & Hair Assessment</td>"),
    ],
}

for fname, replacements in fixes.items():
    path = os.path.join(WORKDIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fixed: {fname}")

print("\nAll final remnants patched.")
