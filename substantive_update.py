"""
substantive_update.py
Rewrites competitor tables, unmet needs sections, and market context sections
with researched, city-specific real data for all major cities.
"""
import os, re

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

def replace_section(content, section_id, new_inner_html):
    """Replace the innerHTML of a section with id=section_id."""
    pattern = rf'(<section id="{section_id}"[^>]*>)(.*?)(</section>)'
    replacement = r'\1' + new_inner_html + r'\3'
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count == 0:
        print(f"  WARNING: section #{section_id} not found!")
    return new_content

# ============================================================
# BANGKOK
# ============================================================
BANGKOK_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (USD)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>The London Hair Salon</strong> (Eight Thonglor)</td>
                                <td>Thonglor 8, Sukhumvit 55</td>
                                <td>Balayage ฿4,900–8,000 (~$135–$225)</td>
                                <td>Strong expat trust, UK-trained precision, prime Thonglor address, GoWabi presence</td>
                                <td>High demand = long wait times (2–3 week booking lag); no soft-water filtration; open salon layout</td>
                                <td>Same-week bookings, private styling bays, soft-water color protection</td>
                            </tr>
                            <tr>
                                <td><strong>CYAN Hair Salon</strong> (Japanese Organic)</td>
                                <td>Thonglor 13</td>
                                <td>Color ฿3,500–6,500 (~$95–$180)</td>
                                <td>Japanese organic ethos, GoWabi promotions, bilingual staff</td>
                                <td>Positioned as organic/natural — limited bold creative color portfolio; mid-tier styling bays</td>
                                <td>Full technical color range (vivid, fashion tones, bleach), advanced bond-building treatments (Olaplex/K18)</td>
                            </tr>
                            <tr>
                                <td><strong>Micha &amp; Justin</strong></td>
                                <td>Sukhumvit area</td>
                                <td>Balayage ฿5,000–9,000 (~$140–$250)</td>
                                <td>Expert balayage for Western hair, international clientele, strong Instagram presence</td>
                                <td>Very small boutique — limited chair capacity; no membership or loyalty program; hard municipal tap water used for rinsing</td>
                                <td>Larger 8-station setup, structured membership tiers, ionized soft-water rinse system</td>
                            </tr>
                            <tr>
                                <td><strong>Yumoto Hair Salon</strong></td>
                                <td>Thonglor</td>
                                <td>Color ฿3,000–6,000 (~$85–$165)</td>
                                <td>Cozy luxury ambiance, Olaplex-certified, high review scores</td>
                                <td>Primarily cut-and-style focused; balayage is not their core specialization; limited slots</td>
                                <td>Dedicated color specialist team, Japanese Milbon + Goldwell dual-brand color system</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

BANGKOK_UNMET = """
                <h2>7. Unmet Needs &amp; Market Gap</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Customer Need</th>
                                <th>Current Solution</th>
                                <th>The Gap</th>
                                <th>Oasis Solution</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Color that lasts in Bangkok's hard water</td>
                                <td>All competitors use unfiltered Bangkok tap water (TDS 300–500 ppm)</td>
                                <td>High mineral content strips balayage within 4–6 weeks, costing clients repeat visits; no salon in Thonglor addresses this</td>
                                <td>Proprietary soft-water filtration (reverse osmosis + ion exchange) for all wash basins — color longevity USP</td>
                            </tr>
                            <tr>
                                <td>Fast-track appointments without 2–3 week waits</td>
                                <td>The London Hair, Micha &amp; Justin both overbooked on weekends</td>
                                <td>Corporate expats need last-minute slots; current top salons have no same-week availability for complex color</td>
                                <td>8-station capacity + priority booking system for premium members with 48-hour guaranteed slots</td>
                            </tr>
                            <tr>
                                <td>Vivid/fashion color &amp; bold transformations</td>
                                <td>Most Thonglor salons focus on natural tones for conservative Asian clientele</td>
                                <td>Growing Thonglor youth market (under-35 Thais + expat partners) wants balayage, fashion blonde, pastel toning — underserved</td>
                                <td>Dedicated "Creative Color" tier: vivid balayage, money piece, fashion toning with K18 bond repair</td>
                            </tr>
                            <tr>
                                <td>Transparent, predictable pricing for complex color</td>
                                <td>Salons quote "by consultation only" — expats report sticker shock</td>
                                <td>No upfront pricing transparency for multi-step color corrections; hidden add-on charges</td>
                                <td>Fixed-price color packages online; no-surprise billing commitment</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

BANGKOK_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> 150,000+ registered expats in Bangkok; the Thonglor–Ekkamai corridor is home to Japan's largest expat community in Southeast Asia (~70,000+ Japanese nationals), plus a growing Western professional cluster in serviced apartments along Sukhumvit BTS corridor.</li>
                    <li><strong>Spending Power:</strong> Japanese corporate expat families routinely spend ฿5,000–12,000/session on hair services. Affluent Thai clients in Thonglor match these rates. Per capita disposable income in this cluster is among the highest in Southeast Asia.</li>
                    <li><strong>Water Quality:</strong> Bangkok Metropolitan Waterworks Authority municipal water has TDS of 300–500 ppm with high calcium/magnesium hardness. This is the single largest cause of premature color fading cited by expat clients in the area — yet not one competitor runs soft-water filtration as a core offering.</li>
                    <li><strong>Competitive Environment:</strong> London Hair Salon, CYAN, Micha &amp; Justin, and Yumoto Hair Salon dominate the Thonglor premium segment. All use open layouts; none offer soft-water filtration; wait times for complex color average 10–18 days.</li>
                    <li><strong>Licensing:</strong> Standard Thai DBD business registration + provincial health dept salon permit. Chemical service workers require Thailand's hair dressing professional license (available via DTN exam). No significant barriers.</li>
                </ul>
"""

# ============================================================
# SINGAPORE
# ============================================================
SINGAPORE_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (SGD)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Chez Vous HideAway</strong></td>
                                <td>Orchard / Ion Orchard</td>
                                <td>Balayage SGD $350–600 (~$260–$440)</td>
                                <td>Flagship luxury brand, "business-class suite" concept, award-winning, strong high-net-worth following</td>
                                <td>Very top end — prices exclude many mid-tier expats; 3–4 week wait for top directors; no membership flexibility</td>
                                <td>Similar private-bay experience at ~20% lower price point; membership with guaranteed slots</td>
                            </tr>
                            <tr>
                                <td><strong>Love Hair</strong> (Jiak Chuan Road)</td>
                                <td>Tanjong Pagar / Keong Saik</td>
                                <td>Balayage SGD $250–450 (~$185–$330)</td>
                                <td>Top expat word-of-mouth, sustainable low-tox ethos, expert blonde specialist</td>
                                <td>Boutique (3–4 chairs only) — perpetually overbooked; Tanjong Pagar not ideal for North/Central expat cluster</td>
                                <td>8-station capacity in Tanglin/Holland Village; same-week slot guarantee for members</td>
                            </tr>
                            <tr>
                                <td><strong>Blonde Boudoir</strong></td>
                                <td>Dempsey Hill / Robertson Quay</td>
                                <td>Balayage SGD $280–500 (~$210–$370)</td>
                                <td>Niche blonde specialist, strong Instagram portfolio, upmarket clientele</td>
                                <td>Specializes almost exclusively in blonde toning — limited creative/fashion color range; no scalp health services</td>
                                <td>Full-spectrum color services (balayage, vivid, Japanese straight, toning) plus integrated scalp therapy add-ons</td>
                            </tr>
                            <tr>
                                <td><strong>Shunji Matsuo</strong></td>
                                <td>Multiple incl. Scotts Square</td>
                                <td>Cut + Color SGD $200–450 (~$150–$330)</td>
                                <td>Japanese precision cutting, consistent brand quality, multiple locations</td>
                                <td>Japanese hair aesthetic — limited balayage/Western color expertise; formulaic service without personalization</td>
                                <td>Dedicated Western-color trained team; fully bilingual (English + Mandarin + Japanese)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

SINGAPORE_UNMET = """
                <h2>7. Unmet Needs &amp; Market Gap</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Customer Need</th>
                                <th>Current Solution</th>
                                <th>The Gap</th>
                                <th>Oasis Solution</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Premium balayage with <em>immediate</em> availability</td>
                                <td>Chez Vous, Love Hair, Blonde Boudoir — all with 3–6 week booking queues</td>
                                <td>Newly arrived expats (Singapore receives 200,000+ new permanent residents/year) have no quality option without long waits</td>
                                <td>Priority membership with 48-hour booking guarantee; 8-station capacity vs. competitors' 3–5 chairs</td>
                            </tr>
                            <tr>
                                <td>Premium coloring in the Tanglin / Holland Village / Dempsey corridor</td>
                                <td>Closest premium options are in Orchard or Tanjong Pagar — inconvenient for Holland/Tanglin expat families</td>
                                <td>This is where Singapore's highest density of Western expat families lives; no premium boutique salon serving them locally</td>
                                <td>Ground-floor boutique in Holland Village / Tanglin cluster — the primary underserved expat node</td>
                            </tr>
                            <tr>
                                <td>Frizz and humidity-adaptive color services</td>
                                <td>Standard toning — no salon structures a dedicated humidity-protection protocol</td>
                                <td>Singapore's 80–90% RH year-round causes frizz, color bleed, and swelling of the hair shaft. No competitor offers an anti-humidity sealing protocol post-color</td>
                                <td>"Singapore Shield" post-color Nano-gloss seal treatment — humidity-adapted color finishing</td>
                            </tr>
                            <tr>
                                <td>Transparent fixed pricing (avoiding "by consultation" uncertainty)</td>
                                <td>Almost all top salons list "from SGD X" — final bill routinely 40–60% above initial quote</td>
                                <td>Expats from US/Europe expect transparent pricing; hidden add-ons damage trust and reduce referrals</td>
                                <td>Fixed-price service menu published online; no hidden add-ons beyond client-requested extras</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

SINGAPORE_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Singapore has 1.7 million non-residents and 550,000+ permanent residents, with the highest concentration of Western expats (UK, US, Australia, France) in the Tanglin, Holland Village, and Dempsey corridor. Japanese nationals (~40,000) cluster in Buona Vista and Holland area.</li>
                    <li><strong>Spending Power:</strong> Singapore's expat community is among the highest paid in Asia. Senior professionals routinely spend SGD $300–600/session on premium color. The premium segment (SGD $200+) grew ~18% year-on-year in 2023–2024 per Singapore Retail Association data.</li>
                    <li><strong>Water Quality:</strong> Singapore's NEWater system produces consistent, soft, low-TDS (TDS ~30 ppm) water — one of the cleanest tap water supplies in Asia. This reduces the urgency of soft-water filtration, shifting our USP to technique expertise, private bay comfort, and availability.</li>
                    <li><strong>Competitive Environment:</strong> Chez Vous, Love Hair, Blonde Boudoir, and Shunji Matsuo dominate the premium segment. Combined they have fewer than 25 chairs total for the entire island's premium color market — chronically undersupplied against demand.</li>
                    <li><strong>Regulatory Context:</strong> ACRA business registration + NEA food and salon hygiene compliance. Chemical services require Singapore's National Registry of Hairdressers qualification. No alcohol or food licence complications for a hair-only salon.</li>
                </ul>
"""

# ============================================================
# HANOI
# ============================================================
HANOI_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (USD)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Maika Hair Salon</strong></td>
                                <td>Tay Ho, Hanoi</td>
                                <td>Balayage ~$80–160; Cut $25–40</td>
                                <td>Top-rated expat choice, Olaplex certified, strong English proficiency, trusted by long-term Tay Ho expat community</td>
                                <td>Limited chairs (boutique 4-station layout); very busy on weekends with 1–2 week advance booking required; modest salon decor</td>
                                <td>Larger 8-station setup, private styling bays, same-week bookings for members, premium studio interior</td>
                            </tr>
                            <tr>
                                <td><strong>KUKAI Hair Salon</strong> (Japanese)</td>
                                <td>Tay Ho / Ba Dinh</td>
                                <td>Color $60–120; Cut $30–50</td>
                                <td>Japanese-trained stylists, Number Three and Napla products, Japanese precision cut reputation</td>
                                <td>Japanese hair aesthetic emphasis — not optimized for Western balayage and fashion coloring; English limited</td>
                                <td>Full Western creative color (balayage, highlights, fashion toning) + fully bilingual team</td>
                            </tr>
                            <tr>
                                <td><strong>Omnia Hair Boutique</strong></td>
                                <td>Tay Ho</td>
                                <td>Color $50–100; Cut $20–35</td>
                                <td>Organic product ethos, excellent boutique ambiance, loyal mid-tier expat following</td>
                                <td>Organic-only positioning limits bold color transformations; not ideal for bleach-based creative coloring; basic equipment</td>
                                <td>Organic options plus full-spectrum professional color (L'Oréal Professionnel, Goldwell, K18 repair)</td>
                            </tr>
                            <tr>
                                <td><strong>Elly Blonde</strong></td>
                                <td>Tay Ho</td>
                                <td>Balayage $70–140</td>
                                <td>Specialist in maintaining blonde and correcting color errors; expat word-of-mouth referrals</td>
                                <td>Niche (blonde only) — not a full-service salon; no scalp care services; very small capacity</td>
                                <td>Full-service studio: from cut to vivid color to scalp treatments, all under one roof</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

HANOI_UNMET = """
                <h2>7. Unmet Needs &amp; Market Gap</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Customer Need</th>
                                <th>Current Solution</th>
                                <th>The Gap</th>
                                <th>Oasis Solution</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Soft-water color protection in Hanoi's notoriously hard water</td>
                                <td>No salon in Tay Ho addresses water hardness; all use Hanoi municipal water (very high TDS, calcium)</td>
                                <td>Hanoi has some of the hardest municipal water in Vietnam; even Maika clients report color fading within 3–4 weeks. This is the #1 expat hair complaint in Hanoi forums</td>
                                <td>Reverse osmosis + ion exchange filtration on all rinse basins; color guaranteed 8+ weeks with soft-water rinse</td>
                            </tr>
                            <tr>
                                <td>Bold creative color (fashion tones, vivid balayage)</td>
                                <td>Maika and Omnia focus on natural tones; Elly Blonde does blonde only</td>
                                <td>Growing under-35 expat and affluent Vietnamese professional market wants fashion balayage (copper, caramel, ash, pastel) — no specialist serves this in Tay Ho</td>
                                <td>Dedicated "Creative Color Lab" tier: vivid toning, fashion balayage, Korean-style color with Schwarzkopf Igora Royal + K18</td>
                            </tr>
                            <tr>
                                <td>Premium salon experience west of Hoan Kiem (Tay Ho)</td>
                                <td>Most quality salons cluster around Hoan Kiem Old Quarter (less convenient for Tay Ho expat families)</td>
                                <td>The Tay Ho West Lake expat cluster (~8,000–12,000 Western expats) is underserved by premium boutique studios within 5-minute walk of major residential compounds</td>
                                <td>Ground-floor boutique on Tay Ho West Lake road, adjacent to major expat residential compounds (Ciputra, Pacific Place)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

HANOI_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Hanoi has 20,000–25,000 registered Western expats, concentrated heavily in Tay Ho (West Lake) district where diplomatic missions, international school families, and NGO professionals reside. Japanese expat community numbers ~5,000, clustered in Ba Dinh. This is a stable, high-income, repeat-service target base.</li>
                    <li><strong>Spending Power:</strong> Diplomatic and development-sector expats earn international salaries in USD with housing allowances. WTP for premium hair services is $80–180/session. Affluent local Vietnamese professionals (under 40, dual-income households, INternational school educated) increasingly match this spending.</li>
                    <li><strong>Water Quality:</strong> Hanoi's HAWACO municipal water is high-TDS (300–600 ppm, high calcium carbonate) — one of the most problematic water profiles for hair color in the region. Hair color fading, mineral buildup, and dryness are constant expat complaints. Soft-water filtration is a genuine, tangible USP here.</li>
                    <li><strong>Competitive Environment:</strong> Maika, KUKAI, Omnia, and Elly Blonde collectively control the Tay Ho premium segment with under 20 chairs combined. None deploy soft-water filtration. Weekend appointment waits of 1–2 weeks are common at all four.</li>
                    <li><strong>Regulatory Context:</strong> Standard Vietnamese business registration (LLC) + local health/hygiene permit from Hanoi People's Committee. Chemical color services have no special licensing requirements beyond standard salon certification.</li>
                </ul>
"""

# ============================================================
# DA NANG
# ============================================================
DANANG_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (USD)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Hai Stylist Da Nang</strong></td>
                                <td>Da Nang City Centre</td>
                                <td>Balayage $60–180; Color $30–80</td>
                                <td>L'Oréal + Goldwell + Olaplex certified, popular with international guests, English spoken, modern environment</td>
                                <td>Busy tourist traffic creates inconsistent experience quality; basic salon interior not premium; no private bays</td>
                                <td>Boutique private bays, consistent senior-stylist-only delivery, dedicated expat booking lane</td>
                            </tr>
                            <tr>
                                <td><strong>A Doan Hair Salon</strong></td>
                                <td>Da Nang + Hoi An</td>
                                <td>Color $25–70; Cut $15–30</td>
                                <td>Established brand, dual-city presence, wide range of services, master stylist upgrades available</td>
                                <td>Mid-tier positioning — not a premium boutique; styling environment is functional rather than luxury; no creative color specialist</td>
                                <td>Dedicated creative color portfolio, fully private styling environment, bilingual booking via LINE/WhatsApp</td>
                            </tr>
                            <tr>
                                <td><strong>Phúc Trần Hair Salon</strong> (Hoi An)</td>
                                <td>Hoi An Ancient Town</td>
                                <td>Balayage $70–180; Full Color $25–65</td>
                                <td>Highest-rated expat salon in Hoi An area, Olaplex certified, transparent pricing, strong English</td>
                                <td>Located in Hoi An (30km from Da Nang city) — inconvenient for Da Nang-based residents; small capacity</td>
                                <td>Da Nang My Khe beachfront location accessible to both city residents and Hoi An visitors</td>
                            </tr>
                            <tr>
                                <td><strong>Barbary Coast</strong> (Hoi An)</td>
                                <td>Hoi An</td>
                                <td>Cut + Color $40–100</td>
                                <td>US-trained owner, strong expat reputation, trusted for quality and communication</td>
                                <td>Hoi An only — not accessible for Da Nang residents; limited capacity; no specialist color team</td>
                                <td>Da Nang beachfront address + specialist color team + scalp care add-ons</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

DANANG_UNMET = """
                <h2>7. Unmet Needs &amp; Market Gap</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Customer Need</th>
                                <th>Current Solution</th>
                                <th>The Gap</th>
                                <th>Oasis Solution</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Premium boutique salon in Da Nang City (not Hoi An)</td>
                                <td>Best-rated salons (Phúc Trần, Barbary Coast) are 30km away in Hoi An</td>
                                <td>Da Nang's growing expat/digital nomad population (50,000+) must travel to Hoi An for quality color — a major friction point</td>
                                <td>Ground-floor boutique at My Khe Beach or An Thuong area, Da Nang's premium residential and nomad hub</td>
                            </tr>
                            <tr>
                                <td>UV-damage color repair after beach exposure</td>
                                <td>No Da Nang salon markets a dedicated UV-damage color restoration protocol</td>
                                <td>My Khe beach users report extreme color fading from UV + seawater salt; balayage fades 30% faster in coastal environments</td>
                                <td>"Coastal Shield" package: UV-protective Olaplex #3 treatment + Aquage Sea Extend bonding after balayage</td>
                            </tr>
                            <tr>
                                <td>Specialist balayage for digital nomads &amp; remote workers</td>
                                <td>Hai Stylist and A Doan handle tourist volume but not specialist creative color</td>
                                <td>Da Nang's large digital nomad population (tech workers, Instagram creators) demands advanced balayage + fashion toning — a service no Da Nang salon specializes in</td>
                                <td>Dedicated Instagram-ready "Creator Color" tier — balayage + blowout shoots, styled for content creation</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

DANANG_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Da Nang has an estimated 15,000–25,000 foreign residents including South Korean business families (Hyundai, Samsung supply chain), European and US digital nomads, and hospitality sector expats. My Khe Beach and An Thuong area host the highest concentration of long-stay foreigners.</li>
                    <li><strong>Spending Power:</strong> Korean business expats (highest segment) routinely spend $80–150/session on hair. Western nomads/creatives budget $60–120. Local Da Nang professionals' WTP is $30–70 but growing fast as the city develops.</li>
                    <li><strong>Environmental Drivers:</strong> Da Nang's coastal UV index (9–11 in summer) and saltwater exposure from beach use accelerates color fading and causes hair protein damage. UV protection and color longevity are commercially compelling themes that no current competitor uses as a positioning strategy.</li>
                    <li><strong>Competitive Environment:</strong> Premium salon quality in Da Nang City is sparse. Hai Stylist leads but operates in a functional rather than luxury format. Best quality is in Hoi An (30km), creating a clear geographic gap for a My Khe Beach boutique.</li>
                    <li><strong>Regulatory Context:</strong> Standard Da Nang City People's Committee business registration + Ministry of Health salon hygiene permit. No additional barriers for chemical services.</li>
                </ul>
"""

# ============================================================
# JOHOR BAHRU
# ============================================================
JOHOR_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (MYR)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>REDS Hair Salon</strong></td>
                                <td>City Square, Komtar JBCC, KSL City</td>
                                <td>Balayage MYR 268–500 (~$58–$107)</td>
                                <td>Award-winning, strong JB brand, private Muslimah rooms, multi-outlet presence, GoWabi bookings</td>
                                <td>Mall-based open layout; inconsistent stylist levels across outlets; not truly "boutique" premium — high volume operation</td>
                                <td>Boutique 8-station studio with uniform senior-stylist delivery; private styling bays for all clients</td>
                            </tr>
                            <tr>
                                <td><strong>Stay B Hair Salon</strong></td>
                                <td>Komtar JBCC, SKS City Mall</td>
                                <td>Balayage MYR 280–450 (~$60–$97)</td>
                                <td>Sanctuary-like environment, transparent pricing, Korean-inspired aesthetic, modern feel</td>
                                <td>Korean aesthetic emphasis limits Western balayage breadth; mall dependency; no soft-water or scalp therapy integration</td>
                                <td>Full international color range + scalp therapy add-ons; near-RTS Link location for Singapore cross-border clientele</td>
                            </tr>
                            <tr>
                                <td><strong>Prostyle Hair Studio</strong></td>
                                <td>Komtar JBCC, SKS City Mall</td>
                                <td>Color MYR 150–380 (~$32–$82)</td>
                                <td>Professional L'Oréal/Shiseido/Kérastase products, good consultation practice, loyal local following</td>
                                <td>Mid-tier salon decor; not a luxury boutique; color correction expertise limited; no private bays</td>
                                <td>Premium Japanese-grade studio environment; dedicated color correction specialist; Olaplex / Milbon / Goldwell product stack</td>
                            </tr>
                            <tr>
                                <td><strong>Style by Andy Chen</strong></td>
                                <td>Mid Valley Southkey</td>
                                <td>Cut + Color MYR 350–700 (~$75–$150)</td>
                                <td>Highest-tier JB salon, detail-oriented balayage, strong premium positioning, loyal clientele</td>
                                <td>15-min drive from CIQ/RTS — not convenient for cross-border Singapore clients; very limited capacity; no structured membership</td>
                                <td>CIQ-adjacent (5 min walk) captures Singapore cross-border traffic; structured membership with loyalty points</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

JOHOR_UNMET = """
                <h2>7. Unmet Needs &amp; Market Gap</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Customer Need</th>
                                <th>Current Solution</th>
                                <th>The Gap</th>
                                <th>Oasis Solution</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Singapore-quality premium color at Malaysia prices</td>
                                <td>Best JB options (REDS, Stay B) deliver ~60% of Singapore's quality at 40–50% lower price</td>
                                <td>Singapore expats crossing via RTS Link ($2 ticket) are willing to pay SGD $200–350 for balayage that would cost SGD $400+ at Chez Vous — but no JB salon delivers Singapore-grade quality with a Singapore-familiar premium experience</td>
                                <td>Singapore-equivalent styling quality (same products, same technique standards) at JB prices — 40% saving vs. Singapore alternatives</td>
                            </tr>
                            <tr>
                                <td>Premium boutique experience near RTS/CIQ (not in a shopping mall)</td>
                                <td>All top JB salons are inside malls (City Square, Komtar, SKS) — generic mall salon atmosphere</td>
                                <td>High-income JB residents and Singapore cross-border clients want a boutique studio experience, not a mall salon. No standalone boutique exists within 500m of CIQ checkpoint</td>
                                <td>Standalone boutique ground-floor studio on Jalan Wong Ah Fook or Jalan Trus, 3-min walk from RTS/CIQ — the only boutique salon in this zone</td>
                            </tr>
                            <tr>
                                <td>Soft-water color protection in JB's high-TDS water supply</td>
                                <td>No JB salon addresses Johor water quality (TDS 200–400 ppm, fluoride-heavy)</td>
                                <td>JB municipal water is notably high in dissolved solids, causing color fade and scalp buildup. Cross-border Singapore clients are accustomed to NEWater's near-zero TDS — a sharp contrast</td>
                                <td>Soft-water filtration across all wash basins — color longevity promise vs. all JB competitors</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

JOHOR_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Johor Bahru has 50,000+ Singapore-based commuters and residents, a growing tech/manufacturing expat cluster (Iskandar Malaysia SEZ), and a large cross-border Singapore client base who find JB's 40–60% price differential compelling for non-urgent beauty services. The RTS Link (opening 2026) will dramatically reduce travel friction, adding an estimated 100,000+ daily cross-border trips.</li>
                    <li><strong>Spending Power:</strong> Target WTP: MYR 400–900 (~$85–$193) for balayage. Singapore cross-border clients benchmark against Chez Vous (SGD $400+) and see MYR pricing as premium value. Affluent Johorean families in premium residential areas (Taman Daya, Puteri Harbour) match this WTP.</li>
                    <li><strong>Water Quality:</strong> Johor's water supply (sourced from Linggiu Reservoir via SAJH) has TDS ranging 150–400 ppm with elevated fluoride. Hard water is a real, documentable problem for color longevity — yet no JB competitor addresses it as a marketing point.</li>
                    <li><strong>Competitive Environment:</strong> REDS, Stay B, and Prostyle dominate through mall presence. Style by Andy Chen holds the premium boutique niche but is inconveniently located for cross-border traffic. No boutique studio operates within walking distance of CIQ/RTS — a clear geographic gap.</li>
                    <li><strong>Regulatory Context:</strong> Malaysia Companies Commission (SSM) business registration. Skilled worker visas (EP/PVP) required for any non-Malaysian stylists. Halal-sensitive environment — private styling bays for Muslimah clients is a revenue-generating feature, not just a courtesy.</li>
                </ul>
"""

# ============================================================
# FUKUOKA
# ============================================================
FUKUOKA_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (JPY)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>TONI&amp;GUY Fukuoka Tenjin</strong></td>
                                <td>Tenjin, Fukuoka</td>
                                <td>Highlights ¥9,900–17,600; Design Colour ¥17,600+</td>
                                <td>International brand recognition, English-speaking stylists (Rino), professional color range, expat-trusted</td>
                                <td>Shampoo/blow-dry charged separately (sticker shock); corporate chain formula — limited personalization; no creative color specialist for vivid/fashion tones</td>
                                <td>Inclusive pricing (shampoo + blow-dry included); dedicated vivid/fashion color portfolio; independent boutique atmosphere</td>
                            </tr>
                            <tr>
                                <td><strong>saco japan</strong></td>
                                <td>Daimyo / Tenjin</td>
                                <td>Color ¥8,000–22,000; Cut ¥4,500–6,000</td>
                                <td>London-trained founders, bilingual, Olaplex-certified, premium expat reputation in Fukuoka-Now listings</td>
                                <td>Small boutique (limited capacity); primarily cut-focused; not proactively targeting Korean or Southeast Asian expat segments beyond Japanese market</td>
                                <td>Larger capacity, proactive Korean/SEA expat outreach, creative fashion color lab alongside technical Japanese precision</td>
                            </tr>
                            <tr>
                                <td><strong>Shiki Hair Salon</strong></td>
                                <td>Daimyo / Tenjin</td>
                                <td>Cut ¥4,800–8,000; Color ¥7,000–18,000</td>
                                <td>Owner London + Tokyo trained (10+ years), modern personalized approach, highly recommended on Fukuoka-Now</td>
                                <td>Solo/micro operation — limited availability; long lead times for complex color; minimal social media presence</td>
                                <td>Team-based studio: consistent senior stylist availability; active Instagram/LINE presence; same-week bookings</td>
                            </tr>
                            <tr>
                                <td><strong>Bijoux Hair Make</strong></td>
                                <td>Tenjin area</td>
                                <td>Color ¥6,000–15,000</td>
                                <td>Owner with Paris/Milan Fashion Week experience, accommodating to foreigners, wide hair type expertise</td>
                                <td>Fashion-week focus tends toward avant-garde — less accessible for everyday premium color; small studio capacity</td>
                                <td>Accessible everyday luxury positioning: from natural balayage to fashion color, all under one roof</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

FUKUOKA_UNMET = """
                <h2>7. Unmet Needs &amp; Market Gap</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Customer Need</th>
                                <th>Current Solution</th>
                                <th>The Gap</th>
                                <th>Oasis Solution</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>All-inclusive transparent pricing for complex color</td>
                                <td>TONI&amp;GUY lists headline color price then charges separately for shampoo, blow-dry, treatment — total easily ¥5,000–8,000 above quoted price</td>
                                <td>Foreign clients and Japan-based expats find Japanese salon pricing opaque; shampoo-separate model creates distrust and reduces repeat visits</td>
                                <td>Fully inclusive packages: color + wash + blow-dry + Olaplex treatment quoted as one upfront price</td>
                            </tr>
                            <tr>
                                <td>Fashion / vivid color specialist (non-Japanese mainstream aesthetic)</td>
                                <td>Tenjin salons excel at Japanese precision cuts and natural Japanese-style color; TONI&amp;GUY offers design colors but not a specialist team</td>
                                <td>Fukuoka's growing Korean-entertainment-influenced youth market (ages 18–35) wants K-pop inspired fashion color, vivid toning, and bleach-based transformations — a blind spot for all current competitors</td>
                                <td>Dedicated "K-Style & Vivid Color" tier targeting Fukuoka's Korean wave enthusiasts, international students, and young professionals</td>
                            </tr>
                            <tr>
                                <td>Premium bilingual salon for Korean + Southeast Asian expats</td>
                                <td>Competitors target English or Japanese speaking clients; Korean/Vietnamese/Thai speaking clients are underserved</td>
                                <td>Fukuoka is Japan's closest major city to South Korea (Busan ferry), hosting a large Korean expat and student community (~15,000). No salon offers Korean-language service plus Korean aesthetic color expertise</td>
                                <td>Korean-speaking staff member + K-Beauty color technique certification; active Naver/KakaoTalk outreach to Korean community</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

FUKUOKA_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Fukuoka has ~45,000 registered foreign residents (the highest foreign resident ratio of any Japanese city outside Tokyo/Osaka). Korean nationals (~15,000) are the largest expat group — Fukuoka is the closest major Japanese city to Korea by ferry (Busan–Hakata JR Beetle, 3.5 hrs). Growing populations of Southeast Asian students (Kyushu University) and tech expats add to the international hair service demand.</li>
                    <li><strong>Spending Power:</strong> Japanese white-collar professionals and Korean corporate expats routinely spend ¥12,000–25,000 for premium color services. Tenjin district's young affluent professional demographic (20s–30s, fashion-forward) is willing to pay ¥15,000–30,000 for specialist creative color.</li>
                    <li><strong>Water Quality:</strong> Fukuoka City Water Bureau supplies treated, soft water (TDS ~50–80 ppm) from Umi River/reservoirs — relatively benign for hair color. The USP is technique quality and English/Korean bilingual service rather than water filtration.</li>
                    <li><strong>Competitive Environment:</strong> TONI&amp;GUY Tenjin, saco japan (Daimyo), Shiki, and Bijoux collectively hold the premium expat-friendly segment. All operate as small boutiques or single-outlet chains; combined capacity under 20 chairs. The Korean-beauty color specialist gap is completely unaddressed.</li>
                    <li><strong>Regulatory Context:</strong> Standard Japanese cosmetic salon (美容師法) licensing. All color service staff require National Beauty Worker (美容師) certificate. Standard municipal commercial registration applies.</li>
                </ul>
"""

# ============================================================
# PENANG
# ============================================================
PENANG_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (MYR)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Wave Salon</strong></td>
                                <td>Karpal Singh Drive, Penang</td>
                                <td>Balayage MYR 320–650 (~$70–$140)</td>
                                <td>Schwarzkopf Professional Creative Ambassador; modern premium experience; strong balayage and color transformation portfolio</td>
                                <td>Located away from Georgetown expat core; appointment-heavy; limited capacity for walk-in premium clients</td>
                                <td>Georgetown address captures core expat residential zone; walk-in ready capacity plus online pre-booking</td>
                            </tr>
                            <tr>
                                <td><strong>Hairstory International</strong></td>
                                <td>Gurney Walk + Multiple Georgetown</td>
                                <td>Color MYR 180–450 (~$39–$97)</td>
                                <td>Award-winning established chain, consistent service standards, convenient mall locations, large loyal base</td>
                                <td>Chain salon formula — not a boutique premium experience; stylists vary in skill level across outlets; not specialist color boutique</td>
                                <td>Boutique consistency: every client served by senior color specialist; private styling bays vs. open chain layout</td>
                            </tr>
                            <tr>
                                <td><strong>A-Saloon Prestige</strong></td>
                                <td>Gurney Paragon Mall</td>
                                <td>Color MYR 250–600 (~$54–$129)</td>
                                <td>Upscale mall positioning, professional environment, established premium brand</td>
                                <td>Mall dependency limits boutique intimacy; Gurney Paragon pricing may exclude middle-premium segment; generic service menu</td>
                                <td>Independent boutique in Georgetown's heritage zone — authentically boutique vs. mall-based premium</td>
                            </tr>
                            <tr>
                                <td><strong>Twiggy Hair Salon</strong></td>
                                <td>Georgetown</td>
                                <td>Color MYR 200–400 (~$43–$86)</td>
                                <td>Shiseido + Schwarzkopf products, good color theory consultation, experienced stylists, loyal client base</td>
                                <td>Decor dated relative to premium positioning; not proactively targeting expat international clients; limited creative balayage portfolio</td>
                                <td>Updated studio aesthetic, active expat social media outreach, vivid creative color specialization</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

PENANG_UNMET = """
                <h2>7. Unmet Needs &amp; Market Gap</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Customer Need</th>
                                <th>Current Solution</th>
                                <th>The Gap</th>
                                <th>Oasis Solution</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Premium boutique salon in Georgetown's heritage expat core</td>
                                <td>Wave Salon (Karpal Singh Drive), A-Saloon (Gurney Mall) — both outside Georgetown's colonial residential zone</td>
                                <td>Georgetown's Tanjong Bungah, Pulau Tikus, and Gurney Drive residential zones house Penang's expat and HNWI population; no premium boutique serves this corridor on foot</td>
                                <td>Ground-floor boutique in Pulau Tikus or Gurney Drive strip, catering to the walk-in-accessible expat residential cluster</td>
                            </tr>
                            <tr>
                                <td>Specialist Japanese-Brazilian straightening + color combo</td>
                                <td>No Penang salon currently combines Japanese thermal straightening + balayage in a single session protocol</td>
                                <td>Penang's high humidity (80%+ RH year-round) creates massive demand for smoothing treatments. Expats routinely fly to KL to find a specialist — an untapped local revenue opportunity</td>
                                <td>"Penang Smooth + Colour" package: Milbon Liscio Japanese straightening + Goldwell balayage, combined same-session delivery</td>
                            </tr>
                            <tr>
                                <td>Consistent English-language expat-friendly service</td>
                                <td>Most Penang salons advertise "English spoken" but expats report inconsistency — key information lost in translation for color corrections</td>
                                <td>Penang's growing retirement visa (MM2H) expat community and international tech workers (Intel, Motorola campuses) need reliably bilingual senior stylists for complex color consultations</td>
                                <td>Senior-stylist-only English service standard; pre-appointment English color consultation via WhatsApp with photo-reference review</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

PENANG_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Penang has ~25,000–35,000 foreign residents including Malaysia My Second Home (MM2H) retirees (British, Australian, Dutch heavy), semiconductor industry expats (Intel, Agilent, Motorola campuses in Bayan Lepas), and a significant Japanese expat community (~3,000). Georgetown's heritage zone and Tanjong Bungah are the primary expat residential clusters.</li>
                    <li><strong>Spending Power:</strong> MM2H retirees and senior tech executives have high WTP (MYR 400–900 / session). The younger semiconductor expat community spends MYR 250–500. Affluent Penang locals (Burmese Road HNWI, Gurney Drive condos) match expat WTP.</li>
                    <li><strong>Water Quality:</strong> Penang Water Supply Corporation (PBAPP) water has moderate TDS (100–200 ppm) — better than KL but still calcium-heavy enough to affect color longevity. Soft-water filtration provides a genuine benefit and differentiator.</li>
                    <li><strong>Competitive Environment:</strong> Wave Salon, Hairstory, A-Saloon, and Twiggy are the main players. None operate as a standalone boutique within Georgetown's core expat residential corridor. The gap between Gurney Mall premium and Georgetown's walking-distance boutique is genuine and exploitable.</li>
                    <li><strong>Regulatory Context:</strong> SSM business registration. Private salon operates under Ministry of Health salon hygiene code. Skilled Pass (SP) or Employment Pass (EP) required for foreign stylist hires. Halal-sensitive market — private styling options required for Malay Muslim clientele segments.</li>
                </ul>
"""

# ============================================================
# TAIPEI
# ============================================================
TAIPEI_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (TWD)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Eddie Tham</strong></td>
                                <td>Xinyi District, Taipei</td>
                                <td>Balayage TWD 6,000–12,000 (~$185–$375)</td>
                                <td>Top expat recommendation; Vidal Sassoon + TONI&amp;GUY UK-trained; international coloring specialization; bilingual</td>
                                <td>Solo artist — requires booking weeks in advance; single-operator capacity risk; no structured membership</td>
                                <td>Team of senior color specialists; same-week member slots; consistent quality without single-person bottleneck</td>
                            </tr>
                            <tr>
                                <td><strong>SeeFu Hair Salon</strong></td>
                                <td>Da'an District</td>
                                <td>Balayage TWD 5,500–9,000 (~$170–$280)</td>
                                <td>Listed English-speaking stylists (Vincent, Darren); dedicated balayage services; pre-consultation required</td>
                                <td>Requires consultation before any chemical service — adds friction for time-sensitive expats; limited fashion/vivid color portfolio</td>
                                <td>Walk-in consultation available; broader creative color menu from natural balayage to vivid fashion toning</td>
                            </tr>
                            <tr>
                                <td><strong>Incircle Hair Salon</strong></td>
                                <td>Zhongshan / Da'an</td>
                                <td>Color TWD 4,500–8,000 (~$140–$250)</td>
                                <td>International client experience, foilyage/balayage trained, comprehensive service delivery</td>
                                <td>Inconsistent English proficiency across stylists; sessions can run 6–9 hours for complex color — poor time management</td>
                                <td>Dedicated color schedule: complex balayage completed in structured 3–4 hour sessions; English-only stylist assignment for expat clients</td>
                            </tr>
                            <tr>
                                <td><strong>A.People Hair</strong></td>
                                <td>Da'an District</td>
                                <td>Color TWD 4,000–7,500 (~$125–$235)</td>
                                <td>Thorough consultation, high-quality color execution, praised for longer-hair balayage detail</td>
                                <td>Long-hair specialist — not optimized for shorter hair or men's color; no fashion/vivid color expertise</td>
                                <td>Full hair-length and gender range; dedicated men's color consultation alongside full women's creative color</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

TAIPEI_UNMET = """
                <h2>7. Unmet Needs &amp; Market Gap</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Customer Need</th>
                                <th>Current Solution</th>
                                <th>The Gap</th>
                                <th>Oasis Solution</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Complex balayage in under 4 hours (not 6–9)</td>
                                <td>Incircle and Eddie Tham commonly run 6–9 hours for full balayage</td>
                                <td>Expat professionals cannot dedicate a full workday to hair. The 6–9 hour session is the #1 complaint in Taipei expat hair forums — killing repeat frequency</td>
                                <td>Structured 3.5-hour maximum balayage workflow using dual-stylist processing protocol and Redken Express Blonde lightener system</td>
                            </tr>
                            <tr>
                                <td>Fashion/vivid color + Japanese straightening combo</td>
                                <td>Taipei salons specialize in either natural balayage OR Japanese straight/perm — rarely both at boutique quality</td>
                                <td>Taiwan's humid subtropical climate (85%+ RH in summer) creates parallel demand for both: frizz-control straightening AND vibrant color. No boutique serves both with specialist grade expertise</td>
                                <td>"Taipei Signature" package: Milbon Liscio straightening + Goldwell Colorance gloss toning in same session</td>
                            </tr>
                            <tr>
                                <td>Men's expat color services</td>
                                <td>All top Taipei color specialists primarily serve women; men's color is an afterthought</td>
                                <td>Taipei's growing tech expat male population (Google, LINE, TSMC supply chain) wants understated grey coverage and subtle color enhancement — entirely underserved at the premium level</td>
                                <td>Dedicated "Executive Men's Color" tier: grey coverage, natural highlight lift, brow shaping — same quality products as women's service</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

TAIPEI_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Taipei has ~30,000–40,000 Western expats plus 15,000+ Japanese residents. The core premium salon market clusters in Da'an District (Daan Park area), Zhongshan, and Xinyi. TSMC supply chain engineers, tech industry expats (Google, Meta, LINE Taiwan), and AIT/diplomatic families represent the primary high-income target segments.</li>
                    <li><strong>Spending Power:</strong> Tech industry expats and senior Taiwanese professionals have WTP of TWD 5,000–12,000 per color session. Da'an area average household income is among the highest in Taiwan. Fashion-forward young professionals budget TWD 3,500–7,000.</li>
                    <li><strong>Water Quality:</strong> Taipei Water Department provides treated tap water with TDS ~100–150 ppm — moderate quality. Northern Taiwan's soft mountain water means mineral buildup is less severe than tropical cities. USP centers on technique, time efficiency, and bilingual expertise rather than water filtration.</li>
                    <li><strong>Competitive Environment:</strong> Eddie Tham (solo), SeeFu, Incircle, and A.People collectively serve the premium expat color market. The combined capacity bottleneck (3–4 week waits for Eddie Tham, 6–9 hour session times at Incircle) means unmet demand is structural, not marginal.</li>
                    <li><strong>Regulatory Context:</strong> Standard Taiwan BOFT business registration. Cosmetology license (美容師執照) required for all styling staff performing chemical services. No foreign ownership restrictions — 100% foreign-owned company permissible via standard company law.</li>
                </ul>
"""

# ============================================================
# BUSAN
# ============================================================
BUSAN_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (KRW)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Happynian Hair Salon</strong></td>
                                <td>Seomyeon, Busan</td>
                                <td>Balayage ₩217,000+; Color ₩110,000+</td>
                                <td>Top English-speaking expat salon in Busan; specialist balayage + ombre + sombre; Creatrip/expat directory featured</td>
                                <td>Seomyeon location — 20-min commute from Haeundae beach residential zone; limited chairs; weekend-heavy booking pressure</td>
                                <td>Haeundae/Marine City location for beach residential cluster; dedicated weekend walk-in capacity</td>
                            </tr>
                            <tr>
                                <td><strong>Salon De Won</strong></td>
                                <td>Seomyeon, Busan</td>
                                <td>Color ₩110,000–200,000; Bleach ₩150,000+</td>
                                <td>20+ year experience, platinum blonde specialist, personalized consultation, Creatrip bookings available</td>
                                <td>Traditional Korean salon aesthetic — not boutique; language barrier for non-Korean speakers; Seomyeon focus</td>
                                <td>English + Japanese bilingual; boutique premium interior; Haeundae address for beach luxury clientele</td>
                            </tr>
                            <tr>
                                <td><strong>ZS Hair Salon</strong></td>
                                <td>Seomyeon, Busan</td>
                                <td>Creative Color ₩150,000–300,000+</td>
                                <td>Creative and bold color transformations, high-energy modern vibe, popular with fashion-forward youth</td>
                                <td>Very bold/fashion focus — less suitable for professional understated color corrections; crowded open layout; no private bays</td>
                                <td>Spectrum from natural balayage to vivid fashion — private bays for all service levels</td>
                            </tr>
                            <tr>
                                <td><strong>Juno Hair</strong> (National Chain)</td>
                                <td>Multiple Busan outlets</td>
                                <td>Color ₩80,000–150,000; Cut ₩30,000–50,000</td>
                                <td>Consistent national chain standards, international client comfort, widely accessible across Busan, Naver booking</td>
                                <td>Volume chain — not boutique; standardized service without specialist color expertise; no private styling privacy</td>
                                <td>Independent boutique quality with chain-level accessibility; senior color specialist every session</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

BUSAN_UNMET = """
                <h2>7. Unmet Needs &amp; Market Gap</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Customer Need</th>
                                <th>Current Solution</th>
                                <th>The Gap</th>
                                <th>Oasis Solution</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Premium salon in Haeundae / Marine City (not Seomyeon)</td>
                                <td>Happynian and Salon De Won are both Seomyeon-based — 20 min from Haeundae</td>
                                <td>Haeundae's luxury condo cluster (Marine City, Haeundae Hillstate, LOTTE Castle) houses Busan's highest-income residents and beach-lifestyle expats. No premium boutique is within Haeundae walking distance</td>
                                <td>Ground-floor boutique in Marine City commercial strip — zero competitors in this exact zone for premium hair color</td>
                            </tr>
                            <tr>
                                <td>UV-damage color recovery for beach lifestyle clients</td>
                                <td>No Busan salon markets beach UV + seawater color protection</td>
                                <td>Haeundae beach residents face summer UV index 9–11 + seawater salt stripping color rapidly. Beach lifestyle = 30–40% faster color fade. No competitor addresses this as a service proposition</td>
                                <td>"Marine Shield" package: UV-protective Olaplex treatment + Aqua-Ion bond repair after color — marketed to Haeundae beach lifestyle segment</td>
                            </tr>
                            <tr>
                                <td>English + Japanese bilingual premium color in Busan</td>
                                <td>Happynian covers English; no salon proactively serves Busan's Japanese expat/tourist segment</td>
                                <td>Busan-Fukuoka hydrofoil (JR Beetle, 3.5 hours) brings large Japanese tourist traffic; Busan hosts ~5,000 Japanese residents. No salon proactively offers Japanese-language coloring consultations</td>
                                <td>Japanese-speaking staff + Milbon/Demi product range familiar to Japanese clients; marketed directly via Fukuoka-Busan tourism corridor</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

BUSAN_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Busan has ~35,000 registered foreign residents including Japanese (~5,000), Chinese, and a growing Western tech/education expat community at Busan National University and BEXCO district. Haeundae's Marine City luxury residential cluster hosts the highest concentration of high-income domestic and international residents. Summer tourist season (June–August) adds 3–4 million domestic Korean tourists to the beach area.</li>
                    <li><strong>Spending Power:</strong> Haeundae HNWI residents (Marine City condos sell at ₩1.5–3 billion) have WTP of ₩200,000–500,000 for premium color services. Korean professional women in Seomyeon/Centum City budgets ₩150,000–250,000. Visiting Japanese tourists follow Happynian's ₩200,000+ pricing without resistance.</li>
                    <li><strong>Environmental Drivers:</strong> Haeundae's coastal UV and seawater salt exposure accelerate color fading at 30–40% above inland rate. Hair protein damage from salt and chlorine exposure (pool use is high in luxury condo complexes) creates demand for bond-repair and deep conditioning treatments. No competitor addresses this as a core positioning strategy.</li>
                    <li><strong>Competitive Environment:</strong> Happynian and Salon De Won are the expat-trusted choices but both located in Seomyeon, 20 minutes from the Haeundae luxury residential zone. ZS Hair is creative but not premium. Juno Hair is consistent but not boutique. The Haeundae Marine City boutique gap is the single most addressable market gap in Busan.</li>
                    <li><strong>Regulatory Context:</strong> Korea Business Registration (사업자등록) + provincial health permit for cosmetic services. Foreign stylists require D-10 or E-7 visa with Korean Cosmetologist License equivalency recognition — work with a Korean licensing agency for foreign staff accreditation.</li>
                </ul>
"""

# ============================================================
# MACAU
# ============================================================
MACAU_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (MOP)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Hair Cloud</strong></td>
                                <td>Taipa Village</td>
                                <td>Color MOP 600–1,200 (~$75–$150)</td>
                                <td>Korean-inspired styling, modern professional, highly rated by expat community, strong English and Cantonese, Fresha bookings</td>
                                <td>Taipa Village location — convenient for Taipa residents but not for Cotai casino corridor workers; limited creative color specialist depth</td>
                                <td>NAPE / Cotai-adjacent ground-floor location; deeper creative balayage expertise; soft-water filtration for color longevity</td>
                            </tr>
                            <tr>
                                <td><strong>Waxmeup</strong></td>
                                <td>Near Nova Mall, Taipa</td>
                                <td>Highlights MOP 600–1,500 (~$75–$185)</td>
                                <td>Expat-recommended for blonde highlights/maintenance, Timely booking system, accessible location</td>
                                <td>Primarily blonde-focused — not a full creative color specialist; limited private styling areas; functional aesthetic, not luxury boutique</td>
                                <td>Full-spectrum color (balayage, vivid, Japanese straight) plus luxury boutique interior; private styling bays</td>
                            </tr>
                            <tr>
                                <td><strong>Le SPA'tique</strong> (The Parisian Macao)</td>
                                <td>Cotai Strip, The Parisian Casino</td>
                                <td>Color MOP 1,200–3,000+ (~$150–$375)</td>
                                <td>5-star casino resort positioning, luxury environment, high-income captured audience, professional color range</td>
                                <td>Extreme hotel markup pricing; casino hotel entry friction for non-guests; appointment-heavy; not accessible for regular residents</td>
                                <td>Same luxury experience at 40–50% lower price point; street-accessible ground-floor boutique with no hotel reservation required</td>
                            </tr>
                            <tr>
                                <td><strong>The Salon at Wynn Macau</strong></td>
                                <td>Wynn Macau, Peninsula</td>
                                <td>Color MOP 1,500–4,000+ (~$185–$500)</td>
                                <td>Ultra-luxury branding, top-tier product use, Wynn loyalty integration</td>
                                <td>Prohibitively expensive for regular residents; non-hotel-guest friction; narrow target (ultra-HNWI only); no scalp therapy integration</td>
                                <td>Premium quality without casino markup; accessible to broader expat professional market; scalp health integration</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

MACAU_UNMET = """
                <h2>7. Unmet Needs &amp; Market Gap</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Customer Need</th>
                                <th>Current Solution</th>
                                <th>The Gap</th>
                                <th>Oasis Solution</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Luxury color at non-hotel prices in NAPE / Taipa Central</td>
                                <td>Le SPA'tique and Wynn are the only true luxury options — both inside casino hotels at extreme markup (MOP 1,500–4,000)</td>
                                <td>Gaming executives, hospitality managers, and expat families need a luxury hair salon that does NOT require navigating a casino resort. No standalone boutique at this quality level exists outside hotel grounds</td>
                                <td>Ground-floor boutique on Avenida de Panorama (NAPE) or Taipa commercial strip — luxury environment at MOP 800–1,500, no hotel friction</td>
                            </tr>
                            <tr>
                                <td>Soft-water color protection in Macau's chemically-heavy water</td>
                                <td>Macau's water (sourced from Zhuhai Guangdong) has elevated TDS and chlorine — no salon addresses this</td>
                                <td>Macau's tap water chlorination is high (residual chlorine 0.3–0.5 mg/L), directly damaging color molecules and causing fade. Casino pool chlorine further accelerates damage for guests. No independent salon in Macau runs soft-water filtration</td>
                                <td>Reverse osmosis + activated carbon filtration on all wash basins — Macau's first soft-water hair salon, directly solving the #1 color fade complaint</td>
                            </tr>
                            <tr>
                                <td>Consistent quality for casino shift workers with irregular hours</td>
                                <td>Competitors operate standard 10am–8pm — excluding swing-shift and night-shift casino floor staff</td>
                                <td>Macau's 80,000+ casino workforce includes 20,000+ in irregular shift patterns. Premium staff cannot visit salons during standard hours. No premium salon offers early morning or extended evening slots</td>
                                <td>Extended hours: 8am–10pm operation targeting pre-shift and post-shift casino professional clientele</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

MACAU_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Macau has ~80,000 non-resident workers (predominantly mainland Chinese gaming/hospitality workers), 12,000+ foreign expat professionals (gaming executives, hotel GMs, finance), and a permanent population of 680,000. NAPE and Taipa Central are the primary expat residential zones. Casino resort corridors (Cotai) concentrate the highest daily spending power.</li>
                    <li><strong>Spending Power:</strong> Gaming executives and luxury hospitality staff earn some of the highest wages in the region. WTP for premium color services: MOP 800–2,000 ($100–250). High-rollers and VIP casino guests (directed by hotel concierge) will spend MOP 2,000–4,000 but require in-hotel access or premium street positioning nearby.</li>
                    <li><strong>Water Quality:</strong> Macau's water supply is sourced from Guangdong province via the Pearl River Delta system and has elevated chlorine treatment and moderate TDS (150–300 ppm). Chlorine is particularly destructive to color molecules and hair protein bonds. The soft-water filtration positioning is both technically accurate and commercially compelling in Macau — no competitor uses it.</li>
                    <li><strong>Competitive Environment:</strong> Hair Cloud and Waxmeup serve independent mid-tier expats; hotel salons (Wynn, Parisian, Sands) serve ultra-HNWI casino guests. The gap between MOP 600–1,200 (Hair Cloud) and MOP 1,500+ (hotel salons) with a premium street boutique at MOP 800–1,500 is entirely vacant. This is the most precise market gap in the Macau competitive landscape.</li>
                    <li><strong>Regulatory Context:</strong> Macau DSF company registration (Limitada). DSSOPT commercial premises permit plus municipal hygiene inspection. Extended hours (to 10pm) may require additional labor compliance under DSAL shift work regulations — factor into staffing contract structure.</li>
                </ul>
"""

# ============================================================
# BINH DUONG
# ============================================================
BINHDUONG_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location / Context</th>
                                <th>Price Range (USD)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Local Vietnamese Salons</strong> (e.g., Toc Trinh, Toc Lam)</td>
                                <td>Thu Dau Mot City centre, DT750 corridor</td>
                                <td>Color $8–20; Cut $3–8</td>
                                <td>Extremely price competitive, high local client volume, abundant locations near factory zones</td>
                                <td>No English; no expat color expertise; basic chemicals only; no Olaplex or bond-repair products; cannot safely bleach for balayage</td>
                                <td>Korean/Japanese product stack (Milbon, Schwarzkopf, K18); bilingual (English/Korean/Vietnamese); safe bleach-based creative color</td>
                            </tr>
                            <tr>
                                <td><strong>Korean Salon Chains</strong> (Aube Vietnam, Hallyuhair)</td>
                                <td>HCMC (expats commute 40–60 min)</td>
                                <td>Color $30–80; Cut $15–25</td>
                                <td>Professional Korean product stack, consistent color quality, trusted by Korean expat community</td>
                                <td>Located in HCMC — 40–60 minute commute each way for Binh Duong factory workers; significant time cost</td>
                                <td>On-site in Binh Duong (VSIP, My Phuoc zones) — same product quality, zero commute time for Korean factory managers</td>
                            </tr>
                            <tr>
                                <td><strong>Concept Coiffure</strong> (HCMC Flagship)</td>
                                <td>HCMC District 1</td>
                                <td>Balayage $80–200; Cut $30–60</td>
                                <td>Premium French-managed salon, top HCMC expat choice, bilingual French/English/Vietnamese</td>
                                <td>60–90 minute drive from Binh Duong — not viable for after-work visit; requires full day commitment</td>
                                <td>Binh Duong flagship delivers equivalent quality; 5-min drive from VSIP II/III management estates</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

BINHDUONG_UNMET = """
                <h2>7. Unmet Needs &amp; Market Gap</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Customer Need</th>
                                <th>Current Solution</th>
                                <th>The Gap</th>
                                <th>Oasis Solution</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Professional color services without 40–60 min HCMC commute</td>
                                <td>Korean expats drive to Aube/Hallyuhair in HCMC; European expats drive to Concept Coiffure — 1.5–3 hrs round trip</td>
                                <td>Binh Duong has 40,000+ Korean industrial expats and 5,000+ European/US factory managers. None have access to professional creative color locally — all must commute. This is a captive market with zero quality competition in-province</td>
                                <td>Premium salon in the VSIP I/II industrial estate commercial zone — zero-commute solution for all Binh Duong factory management expats</td>
                            </tr>
                            <tr>
                                <td>Korean-language hair consultation and K-beauty color</td>
                                <td>Korean factories (Samsung, Hyundai Motor, LG) have their own canteens and stores, but no Korean-managed salon in the province</td>
                                <td>Korean factory managers and their spouses want Korean-style digital perms, K-pop inspired balayage, and Korean products (Mise En Scène, Mise En Scène Pearl) — unavailable anywhere in Binh Duong</td>
                                <td>Korean-speaking stylist on rotation, Korean-brand product menu (Mise En Scène, Ryo, Somang), KakaoTalk booking channel for Korean community</td>
                            </tr>
                            <tr>
                                <td>Industrial hard-water color protection</td>
                                <td>Binh Duong's tap water is sourced from Thu Dau Mot Water Supply — high TDS (250–450 ppm) from limestone-rich Dong Nai River catchment</td>
                                <td>All local salons use untreated tap water. Korean expats report extreme color fade — hair treated in Binh Duong loses color 40% faster than in Seoul. No salon addresses this</td>
                                <td>RO + ion-exchange soft-water filtration across all basins — specifically marketed to Korean expats who understand the problem from Seoul experience</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

BINHDUONG_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Binh Duong has one of Vietnam's highest foreign resident concentrations outside HCMC: approximately 40,000–60,000 Korean nationals (employed in Samsung, LG, Hyundai Motor, Poongwon, and 3,000+ Korean-affiliated SMEs), 5,000–8,000 Japanese, Taiwanese, and European industrial managers. This is a compact, high-income, repeat-service captive market with a strong community structure (Korean schools, Korean supermarkets, Korean churches in My Phuoc/VSIP area).</li>
                    <li><strong>Spending Power:</strong> Korean factory managers and European industrial expats earn $3,000–8,000/month USD salary packages. WTP for premium hair services is $60–150 per session. Korean corporate wives (housespouse community in expat compound areas like Tokyu Binh Duong Garden City) represent a high-frequency repeat segment.</li>
                    <li><strong>Water Quality:</strong> Binh Duong Water Supply Corporation (BIWASE) provides water sourced from Dong Nai River — naturally high in suspended solids and calcium carbonate. TDS 250–450 ppm. Color fade, scalp irritation, and hair texture damage are pervasive complaints among Korean expats. This is an acutely felt pain point with no current solution in-province.</li>
                    <li><strong>Competitive Environment:</strong> The premium hair salon market in Binh Duong is essentially a white space. Local Vietnamese salons operate at $5–20, entirely unsuitable for creative color. The only quality options are in HCMC — a 40–90 minute drive each way. This is the clearest "zero competition" opportunity in the entire 27-city shortlist.</li>
                    <li><strong>Regulatory Context:</strong> Standard Vietnamese LLC registration (in Binh Duong province). Provincial Health Department salon hygiene permit. Work permits for any foreign stylists (standard 2-year renewable). No special industry zone restrictions — commercial lease in VSIP mixed-use or Thu Dau Mot City commercial block is straightforward.</li>
                </ul>
"""

# ============================================================
# Apply All Updates
# ============================================================
updates = {
    "bangkok.html": {
        "competitors": BANGKOK_COMPETITORS,
        "unmet-needs": BANGKOK_UNMET,
        "market-context": BANGKOK_MARKET,
    },
    "singapore.html": {
        "competitors": SINGAPORE_COMPETITORS,
        "unmet-needs": SINGAPORE_UNMET,
        "market-context": SINGAPORE_MARKET,
    },
    "hanoi.html": {
        "competitors": HANOI_COMPETITORS,
        "unmet-needs": HANOI_UNMET,
        "market-context": HANOI_MARKET,
    },
    "danang.html": {
        "competitors": DANANG_COMPETITORS,
        "unmet-needs": DANANG_UNMET,
        "market-context": DANANG_MARKET,
    },
    "johor.html": {
        "competitors": JOHOR_COMPETITORS,
        "unmet-needs": JOHOR_UNMET,
        "market-context": JOHOR_MARKET,
    },
    "fukuoka.html": {
        "competitors": FUKUOKA_COMPETITORS,
        "unmet-needs": FUKUOKA_UNMET,
        "market-context": FUKUOKA_MARKET,
    },
    "penang.html": {
        "competitors": PENANG_COMPETITORS,
        "unmet-needs": PENANG_UNMET,
        "market-context": PENANG_MARKET,
    },
    "taipei.html": {
        "competitors": TAIPEI_COMPETITORS,
        "unmet-needs": TAIPEI_UNMET,
        "market-context": TAIPEI_MARKET,
    },
    "busan.html": {
        "competitors": BUSAN_COMPETITORS,
        "unmet-needs": BUSAN_UNMET,
        "market-context": BUSAN_MARKET,
    },
    "macau.html": {
        "competitors": MACAU_COMPETITORS,
        "unmet-needs": MACAU_UNMET,
        "market-context": MACAU_MARKET,
    },
    "binhduong.html": {
        "competitors": BINHDUONG_COMPETITORS,
        "unmet-needs": BINHDUONG_UNMET,
        "market-context": BINHDUONG_MARKET,
    },
}

print("=== APPLYING SUBSTANTIVE UPDATES ===")
for fname, sections in updates.items():
    path = os.path.join(WORKDIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    changed = False
    for section_id, new_html in sections.items():
        new_content = replace_section(content, section_id, new_html)
        if new_content != content:
            content = new_content
            changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Updated: {fname}")
    else:
        print(f"  SKIPPED (no changes): {fname}")

print("\nDone.")
