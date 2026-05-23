"""
deep_clean_remnants.py - Second-pass targeted cleanup of all remaining old-model terminology.
Handles context-aware replacements to ensure coherence.
"""
import os
import re

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
files = [f for f in os.listdir(WORKDIR) if f.endswith(".html") and f != "index.html" and f != "competitor_map.html"]

def clean_file(html, fname):
    # ---- HEAD SPA remnants ----
    # Service/menu references
    html = html.replace("integrated Japanese head spa care", "specialized technical coloring and styling care")
    html = html.replace("Japanese head spa/scalp therapy", "specialized scalp-care and styling")
    html = html.replace("Japanese head spa and scalp treatments are secondary", "technical coloring and precision cuts are secondary services")
    html = html.replace("Japanese Carbonated Head Spa & Cut", "Signature Color & Precision Cut")
    html = html.replace("Japanese Carbonated Head Spa", "Premium Color Treatment & Scalp Care")
    html = html.replace("5x Signature Japanese Carbonated Head Spa & Cut", "5x Signature Color & Precision Cut sessions")
    html = html.replace("12x Japanese Carbonated Head Spa & Cut + 10% off all services", "12x Premium Color & Cut sessions + 10% off all services")
    html = html.replace("acoustic head spa station for carbonated mist therapy", "styling station for deep conditioning and blowout")
    html = html.replace("dedicated soundproofed head spa zones", "dedicated private styling consultation zones")
    html = html.replace("Soundproofed shampoo area with premium head spa beds, carbonated mist water generators", "Premium backwash area with luxury recline basins, double-filtration soft-water rinse systems")
    html = html.replace("lacks specialized Japanese head spa/scalp therapy, service is standard open-salon", "lacks soft-water filtration, limited private styling bays")
    html = html.replace("Spacious luxury layout, lacks dedicated soundproofed head spa zones", "Good styling, lacks specialized soft-water filtration and private bays")
    html = html.replace("head spa and scalp treatments are secondary", "technical coloring and precision cuts remain their secondary strength")
    html = html.replace("head spa steam water rings", "double-filtration soft-water systems")
    html = html.replace("head spa/scalp care", "soft-water hair therapy")
    html = html.replace("head spa care", "premium scalp and hair care")
    html = html.replace("head spa beds", "luxury backwash beds")
    html = html.replace("head spa treatment", "premium hair treatment")
    html = html.replace("Head Spa treatment", "Premium Hair Treatment")
    html = html.replace("head spa service", "styling and hair care service")
    html = html.replace("head spa zone", "backwash styling zone")

    # Competitor weakness mentions
    html = html.replace("lacks premium private head spa equipment", "lacks soft-water filtration and private styling comfort")
    html = html.replace("lacks dedicated soundproofed head spa zones", "lacks specialized scalp therapy and private styling zones")
    html = html.replace("no specialized head spa equipment", "no soft-water filtration systems")
    html = html.replace("but head spa and scalp treatments", "but advanced scalp-care integration")
    
    # Market fit / competitive environment
    html = html.replace("acoustic head spa sanctuaries", "premium boutique styling studios")
    html = html.replace("lacks a dedicated premium boutique salon offering consistent luxury standards and bilingual, internationally-trained staff. Oasis Salon fills this gap perfectly by offering high-end styling alongside integrated Japanese head spa care.",
                        "lacks a dedicated premium boutique salon offering consistent luxury styling, advanced technical coloring, and bilingual internationally-trained staff. Oasis Salon fills this gap perfectly by offering ground-floor premium styling with soft-water filtration systems protecting color longevity.")
    html = html.replace("basic local beauty shops, but lacking premium specialized acoustic head spa sanctuaries",
                        "basic local beauty shops, but lacking premium ground-floor boutique salons with specialized technical coloring and soft-water systems")
    html = html.replace("Lacks specialized Japanese head spa/scalp therapy",
                        "Lacks soft-water color protection and specialized scalp therapy")
    
    # Generic head spa
    html = re.sub(r'\bhead spa\b', 'hair salon', html, flags=re.IGNORECASE)

    # ---- SCALP WELLNESS remnants ----
    html = html.replace("integrated scalp wellness", "integrated scalp therapy and hair care")
    html = html.replace("specialized scalp wellness", "specialized scalp care and hair therapy")
    html = html.replace("scalp wellness center", "hair salon and scalp therapy center")
    html = html.replace("Scalp Wellness", "Hair & Scalp Wellness")
    html = html.replace("scalp wellness", "hair and scalp health")
    html = html.replace("SOHO adjacent tower suite. High-income expat density", "SOHO adjacent ground-floor storefront. High-income expat density")
    
    # ---- SCALP SCAN remnants ----
    html = html.replace("scalp scan consultation", "hair health consultation")
    html = html.replace("scalp scan shows", "hair health assessment shows")
    html = html.replace("scalp scan", "hair health consultation")
    html = html.replace("Scalp scan", "Hair health assessment")
    
    # ---- UPSTAIRS remnants ----
    # In location candidate names
    html = re.sub(r'Candidate \w+: (\w[^\n"]+) Upstairs ([^\n"]+) Suite', 
                  lambda m: m.group(0).replace('Upstairs ', 'Ground-Floor ').replace('Suite', 'Storefront'), html)
    html = re.sub(r'Candidate \w+: (\w[^\n"]+) Upstairs ([^\n"]+)',
                  lambda m: m.group(0).replace('Upstairs ', 'Ground-Floor '), html)
    
    # In candidate name strings in JavaScript
    html = re.sub(r'(name:\s*"[^"]*?)Upstairs', r'\1Ground-Floor', html)
    html = re.sub(r'(name:\s*"[^"]*?)upstairs', r'\1ground-floor', html)
    
    # In candidate notes strings in JavaScript
    html = re.sub(r'(note:\s*"[^"]*?)upstairs', r'\1ground-floor', html)
    
    # In location table cells
    html = re.sub(r'<td>([^<]*?)Upstairs ([^<]*?)</td>', 
                  lambda m: '<td>' + m.group(1) + 'Ground-Floor ' + m.group(2) + '</td>', html)
    
    # In strategy text
    html = html.replace("Opt for an upstairs unit in a Ginza-style commercial tower",
                        "Opt for a ground-floor or first-floor unit in a premium commercial block")
    html = html.replace("This upstairs hideaway model ensures absolute acoustic peace and privacy",
                        "This ground-floor boutique model ensures excellent street visibility and walk-in traffic")
    html = html.replace("bypassing high street-level retail rents", "securing affordable ground-floor storefronts")
    html = html.replace("upstairs commercial", "ground-floor commercial")
    html = html.replace("upstairs viewings", "ground-floor storefront viewings")
    html = html.replace("upstairs unit", "ground-floor unit")
    html = html.replace("Upstairs unit", "Ground-floor unit")
    html = html.replace("upstairs boutique", "ground-floor boutique")
    html = html.replace("Causeway Bay (Upstairs commercial)", "Causeway Bay (Ground-Floor Storefront)")

    # ---- STRATEGY TEXT - upstairs ----
    # General upstairs in body text
    html = re.sub(r'\bupstairs\b(?!\s+or ground floor)', 'ground-floor', html, flags=re.IGNORECASE)
    
    return html

print("=== DEEP CLEANING ALL PAGES ===")
updated = 0
for fname in sorted(files):
    path = os.path.join(WORKDIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()
    cleaned = clean_file(original, fname)
    if cleaned != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"  Cleaned: {fname}")
        updated += 1

print(f"\nDone. Updated {updated} files.")
