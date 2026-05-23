import os
import re

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
files = [f for f in os.listdir(WORKDIR) if f.endswith(".html") and f != "index.html" and f != "competitor_map.html"]

replacements = {
    # Positioning and USP
    "upscale, high-visibility upstairs or ground floor units": "upscale, high-visibility ground floor retail storefronts",
    "upstairs or ground floor units": "ground floor retail storefronts",
    '"Your signature look. Expert styling, premium care."': '"Your signature look. Expert styling, soft-water hair care."',
    "Japanese head spa viral videos on TikTok/IG have primed the market demand without sufficient high-end supply.": "Surging demand for premium chemical coloring (balayage, highlights) and professional international styling among high-income locals and expat communities.",
    "Acoustic isolation, microscopic scanning, Japanese CO2 water systems": "Precision hair coloring chemistry, custom styling bays, multi-stage soft-water filtration systems",
    "Standard local hair shops. Loud, lack premium private pods.": "Traditional local salons. Lack specialized soft-water filtration, open crowded layouts, and Western styling expertise.",
    "Noisy open layouts, basic wash beds, no private VIP pods": "Crowded open layouts, lack soft-water systems, basic hair coloring techniques",
    "Japanese head spa viral videos": "Premium hair styling and coloring demand",
    "private VIP pods": "styling stations",
    "soundproofed VIP pods": "semi-private styling bays",
    "private pods": "styling stations",
    "VIP pods": "styling stations",
    "VIP treatment pods": "styling stations",
    "VIP treatment rooms": "styling bays",
    "VIP rooms": "styling bays",
    "Treatment Rooms (3)": "Styling Station Bays (4)",
    "Treatment Rooms": "Styling Station Bays",
    "starlight projection ceilings": "custom track lighting",
    "starlight projection ceiling": "custom track lighting",
    "starlight ceilings": "professional vanity track lighting",
    "starlight projection": "modern vanity lighting",
    "starlight": "custom track lighting",
    
    # Layout and Equipment
    "3 Japanese Takara Belmont wash beds, dark aesthetics": "4 premium styling stations, professional vanity setup",
    "4 Private VIP Pods (400 sqft): Soundproofed walls, starlight projection ceilings, Japanese wash beds.": "4 Boutique Styling Stations (400 sqft): Semi-private bays, professional vanity track lighting, styling chair.",
    "4 VIP Beds (OEM), 800 sq ft": "4 Styling Stations, 2 Backwash Beds, 800 sq ft",
    "4 VIP Beds (OEM)": "4 Styling Chairs, 2 Wash Beds",
    "4 VIP Beds": "4 Styling Chairs",
    "Yume Beds": "Styling Chairs",
    "Yume beds": "styling chairs",
    "wash beds": "styling chairs",
    "wash bed": "styling chair",
    "water filtration units": "carbonated hair rinse systems",
    "filtration units": "soft-water systems",
    
    # Staffing
    "Store Manager / Lead": "Salon Director / Master Stylist",
    "Store Manager": "Salon Director",
    "Senior Therapist": "Senior Hair Stylist",
    "3 Therapists:": "3 Stylist Assistants:",
    "therapists": "stylists",
    "therapist": "stylist",
    "Therapist": "Stylist",
    
    # Service Menu
    "Express Reset": "Express Cut & Blowout",
    "Signature Head Spa": "Precision Cut & Scalp Treatment",
    "Scalp Detox Focus": "Luxury Hair Botox & Rejuvenation",
    "Ultimate Zen": "Signature Balayage & Highlights",
    "Executive Reset": "Executive Cut & Blowout",
    "VSIP Industrial Reset": "VSIP Stylist Cut & Blowout",
    "Hard Water Detox": "International Color & Custom Style",
    "Viral Scalp Facial": "Viral Balayage / Accent Highlights",
    "Oxygen Mist Scalp Reset": "Custom Color & Blowout",
    "mist systems": "soft-water systems",
    
    # Diagnostic / Cams
    "micro-camera analytics": "technical hair consultation",
    "micro-camera scan": "hair health assessment",
    "micro-camera": "hair consultation",
    "scalp scan": "hair consultation",
    "scalp micro-camera scan": "hair health consultation",
    "microscope scanning": "hair consultation",
    "microscopic scanning": "hair consultation",
    "scalp analyzer camera": "styling consultant desk",
    "scalp analyzer": "styling consultant desk"
}

print("=== RUNNING BASELINE SALON PIVOTER ===")
updated_count = 0
for file in sorted(files):
    path = os.path.join(WORKDIR, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    original = content
    for old, new in replacements.items():
        # Match case-insensitively or match exact case to be safe
        content = content.replace(old, new)
        # Also handle lower/title variations if needed
        content = content.replace(old.lower(), new.lower())
        content = content.replace(old.capitalize(), new.capitalize())
        
    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated baseline in: {file}")
        updated_count += 1

print(f"\nCompleted baseline pivoting in {updated_count} files.")
