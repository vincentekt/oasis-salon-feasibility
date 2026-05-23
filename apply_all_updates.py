import os

def main():
    bd_path = r'c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web\binhduong.html'
    js_path = r'c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web\script.js'

    # Read files
    with open(bd_path, 'r', encoding='utf-8') as f:
        bd_content = f.read()

    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    # Normalize newlines to \n to make replacement robust
    bd_content = bd_content.replace('\r\n', '\n')
    js_content = js_content.replace('\r\n', '\n')

    # 1. Update script.js CitiesDb
    old_city_obj = """    {
        "name": "Binh Duong",
        "region": "Vietnam",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 19k - 24k",
        "opex": "USD 4,750",
        "ticket": "USD 36",
        "cogs": "USD 3.60",
        "margin": "90%",
        "breakeven": "~147 customers",
        "daily_breakeven": "~4.9 customers/day",
        "tax": "20.0%",
        "pat_ratio": "137% (Post-Tax)",
        "payback": "3 Months",
        "underserved": "48%",
        "airport": "45 mins (SGN)",
        "risk": "Factory shift fluctuations",
        "complexity": {
            "total": 388,
            "loc": "110 hrs (Factory corridor search)",
            "design": "38 hrs (Styling stations layout)",
            "staff": "130 hrs (5 total headcount)",
            "logistics": "110 hrs (HCMC customs)"
        },
        "coords": [
            10.9805,
            106.6515
        ],
        "url": "binhduong.html"
    },"""

    new_city_obj = """    {
        "name": "Binh Duong",
        "region": "Vietnam",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 19k - 23k",
        "opex": "USD 4,553",
        "ticket": "USD 36",
        "cogs": "USD 3.60",
        "margin": "90%",
        "breakeven": "~141 customers",
        "daily_breakeven": "~4.7 customers/day",
        "tax": "20.0%",
        "pat_ratio": "180% (Post-Tax)",
        "payback": "3 Months",
        "underserved": "2%",
        "airport": "55 mins (SGN)",
        "risk": "Factory shift fluctuations",
        "complexity": {
            "total": 369,
            "loc": "110 hrs (Chanh Nghia expat search)",
            "design": "19 hrs (Styling stations layout)",
            "staff": "130 hrs (4 total headcount)",
            "logistics": "110 hrs (HCMC customs)"
        },
        "coords": [
            10.9780,
            106.6560
        ],
        "url": "binhduong.html"
    },"""

    # Normalize old/new city obj newlines to \n
    old_city_obj = old_city_obj.replace('\r\n', '\n')
    new_city_obj = new_city_obj.replace('\r\n', '\n')

    if old_city_obj in js_content:
        print("[script.js] Found old Binh Duong city object. Replacing...")
        js_content = js_content.replace(old_city_obj, new_city_obj)
    else:
        print("[ERROR] Could not find Binh Duong city object in script.js!")
        return

    # 2. Update volumesDb in script.js
    old_vol = '"binhduong": 397,'
    new_vol = '"binhduong": 457,'
    if old_vol in js_content:
        print("[script.js] Found old volume. Replacing...")
        js_content = js_content.replace(old_vol, new_vol)
    else:
        print("[ERROR] Could not find '\"binhduong\": 397,' in script.js!")
        return

    # 3. Update binhduong.html Executive Summary stats boxes
    old_stats = """                    <div class="stat-box">
                        <span class="label">Initial CAPEX</span>
                        <span class="value">USD 19k - 24k</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Monthly OPEX</span>
                        <span class="value">USD 4,750</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Breakeven Volume</span>
                        <span class="value">5 Customers / Day</span>
                    </div>"""
    
    new_stats = """                    <div class="stat-box">
                        <span class="label">Initial CAPEX</span>
                        <span class="value">USD 19k - 23k</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Monthly OPEX</span>
                        <span class="value">USD 4,553</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Breakeven Volume</span>
                        <span class="value">4.7 Customers / Day</span>
                    </div>"""
    
    old_stats = old_stats.replace('\r\n', '\n')
    new_stats = new_stats.replace('\r\n', '\n')

    if old_stats in bd_content:
        print("[binhduong.html] Found old stats box. Replacing...")
        bd_content = bd_content.replace(old_stats, new_stats)
    else:
        print("[ERROR] Could not find stats box in binhduong.html!")
        return

    # 4. Update Main Success Condition
    old_success = """<p><strong>Main Success Condition:</strong> Establishing a premium boutique hair salon with specialized Japanese head spa and scalp therapy in Binh Duong (Thuan An near Aeon Mall / VSIP 1) to target manufacturing expats and affluent locals. High-quality Japanese-spec OEM equipment keeps setup CAPEX low.</p>"""
    new_success = """<p><strong>Main Success Condition:</strong> Establishing a premium boutique hair styling and color salon in Binh Duong (Chanh Nghia, Thu Dau Mot) targeting manufacturing expats and high-income locals. Custom water softener filtration to remove iron rust and calcium hardness keeps chemical treatment quality high.</p>"""

    old_success = old_success.replace('\r\n', '\n')
    new_success = new_success.replace('\r\n', '\n')

    if old_success in bd_content:
        print("[binhduong.html] Found old success condition. Replacing...")
        bd_content = bd_content.replace(old_success, new_success)
    else:
        print("[ERROR] Could not find success condition in binhduong.html!")
        return

    # 5. Update Business Positioning
    old_positioning = """                    <p><strong>Positioned as:</strong> A premium boutique hair salon integrating Japanese carbonated soft-water systems, advanced scalp diagnostics, specialized organic styling, and private styling stations. Focuses on damage-free coloring and customized hair restoration therapies.</p>
                    <p><strong>Avoid being positioned as:</strong> A low-cost local hair wash shop, a standard open-floor noisy salon, or a chemical-heavy generic barber.</p>
                    <blockquote class="positioning-statement">"Botanical Rejuvenation. Premium styling and therapeutic scalp care in Vietnam's industrial heart."</blockquote>
                    <p><strong>Core Customer Promise:</strong> Damage-free styling, luxury hair restoration, and private scalp rejuvenation using organic botanical extracts and Japanese technology.</p>
                    <p><strong>Market Fit:</strong> Binh Duong's high-income expat managers and business professionals need a quiet, luxury space for premium cuts, styling, and scalp care, escaping the industrial dust and heat.</p>"""

    new_positioning = """                    <p><strong>Positioned as:</strong> A premium boutique hair styling and coloring salon integrating advanced water filtration (iron-removal and water softening), specialized organic dyes, and private styling stations. Focuses on damage-free coloring, artistic balayage, and customized hair conditioning.</p>
                    <p><strong>Avoid being positioned as:</strong> A low-cost local hair wash shop, a standard open-floor noisy salon, a mass-market chemical factory, or a generic barber.</p>
                    <blockquote class="positioning-statement">"Vibrant Color, Pure Care. Premium hair styling and damage-free color in Vietnam's industrial hub."</blockquote>
                    <p><strong>Core Customer Promise:</strong> Long-lasting vibrant color, damage-free styling, and personalized conditioning using organic botanical extracts and purified, softened water.</p>
                    <p><strong>Market Fit:</strong> Binh Duong's expat managers and professionals require a high-end salon for premium cuts and technical coloring, needing specialized water treatment to prevent local tap water iron from fading their hair color.</p>"""

    old_positioning = old_positioning.replace('\r\n', '\n')
    new_positioning = new_positioning.replace('\r\n', '\n')

    if old_positioning in bd_content:
        print("[binhduong.html] Found old business positioning. Replacing...")
        bd_content = bd_content.replace(old_positioning, new_positioning)
    else:
        print("[ERROR] Could not find business positioning in binhduong.html!")
        return

    # 6. Update Market Context
    old_context = """            <!-- 3. Market Context -->
            <section id="market-context" class="card fade-in">
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Over 100,000 foreign workers in Binh Duong, with major enclaves in Thu Dau Mot and Thuan An.</li>
                    <li><strong>Spending Power:</strong> High corporate expat allowances and expanding local industrial middle class.</li>
                    <li><strong>Environmental Drivers:</strong> Heavy industrial dust, factory heat, and soot cause oily scalp and dandruff.</li>
                    <li><strong>Competitive Environment:</strong> Low-cost local hair washes and standard beauty salons, but zero specialized acoustic Japanese head spas.</li>
            </ul>
            </section>"""

    new_context = """            <!-- 3. Market Context -->
            <section id="market-context" class="card fade-in">
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Over 100,000 foreign workers in Binh Duong, with major enclaves in the Chanh Nghia expat quarter of Thu Dau Mot.</li>
                    <li><strong>Spending Power:</strong> High corporate expat allowances and expanding local industrial middle class with high WTP for beauty.</li>
                    <li><strong>Water Quality Constraints:</strong> Local tap water contains high iron (rust) and hardness, which reacts with hair bleach and dyes, causing rapid color fading, brassiness, and dry hair texture.</li>
                    <li><strong>Competitive Environment:</strong> Abundant low-cost local salons and barbers, but a complete absence of premium boutique salons featuring professional water softening systems for color preservation.</li>
            </ul>
            </section>"""

    old_context = old_context.replace('\r\n', '\n')
    new_context = new_context.replace('\r\n', '\n')

    if old_context in bd_content:
        print("[binhduong.html] Found old market context. Replacing...")
        bd_content = bd_content.replace(old_context, new_context)
    else:
        print("[ERROR] Could not find market context in binhduong.html!")
        return

    # 7. Update Target Customer Segments
    old_segments = """                             <tr>
                                <td>Taiwanese, Japanese & Korean Managers</td>
                                <td><span class="badge high">High</span></td>
                                <td>Scalp detox from industrial dust, damage-free styling & premium cuts, quiet/private stations, English/Asian language support</td>
                                <td>$35 - $60</td>
                                <td>Expat social clubs, factory HR partnerships</td>
                                <td>"Premium Cut & Japanese Head Spa" (90m)</td>
                            </tr>
                            <tr>
                                <td>Local High-Income Families</td>
                                <td><span class="badge high">High</span></td>
                                <td>Modern organic color, balayage without damage, premium styling, scalp health checks</td>
                                <td>$30 - $55</td>
                                <td>Word of mouth, Becamex residential groups</td>
                                <td>"Botanical Color & Scalp Rejuvenation" (120m)</td>
                            </tr>"""

    new_segments = """                             <tr>
                                <td>Taiwanese, Japanese & Korean Managers</td>
                                <td><span class="badge high">High</span></td>
                                <td>Damage-free styling & precision cuts, color preservation, private styling stations, English/Asian language support</td>
                                <td>$35 - $60</td>
                                <td>Expat social clubs, factory HR partnerships</td>
                                <td>"Premium Cut & Purified Hair Wash" (60m)</td>
                            </tr>
                            <tr>
                                <td>Local High-Income Families</td>
                                <td><span class="badge high">High</span></td>
                                <td>Modern organic color, balayage without damage, premium styling, iron-free water wash to prevent brassiness</td>
                                <td>$30 - $55</td>
                                <td>Word of mouth, Becamex residential groups</td>
                                <td>"Botanical Color & Soft-Water Hair Treatment" (120m)</td>
                            </tr>"""

    old_segments = old_segments.replace('\r\n', '\n')
    new_segments = new_segments.replace('\r\n', '\n')

    if old_segments in bd_content:
        print("[binhduong.html] Found old segments. Replacing...")
        bd_content = bd_content.replace(old_segments, new_segments)
    else:
        print("[ERROR] Could not find segments in binhduong.html!")
        return

    # 8. Update Location Study Table
    old_loc_table = """                             <tr class="highlight-row">
                                <td>Thuan An (near Aeon Mall / VSIP 1)</td>
                                <td>USD 850 - 1,100</td>
                                <td>High visibility, massive expat foot traffic, premium modern complexes</td>
                                <td>Higher rent premium for main road frontage</td>
                                <td>4.8 / 5 (Recommended)</td>
                            </tr>
                            <tr>
                                <td>Thu Dau Mot City Core</td>
                                <td>USD 680 - 935</td>
                                <td>Stable local high-income demographic, steady year-round traffic</td>
                                <td>Slightly further from VSIP industrial zones</td>
                                <td>4.3 / 5</td>
                            </tr>"""

    new_loc_table = """                             <tr class="highlight-row">
                                <td>Thu Dau Mot City Core (Chanh Nghia)</td>
                                <td>USD 578 - 795</td>
                                <td>Direct access to expat residential core, stable high-income traffic, street visibility</td>
                                <td>Constrained parking space during business hours</td>
                                <td>4.8 / 5 (Recommended)</td>
                            </tr>
                            <tr>
                                <td>Thuan An (near Aeon Mall / VSIP 1)</td>
                                <td>USD 723 - 935</td>
                                <td>High visibility near mall traffic, modern commercial complexes</td>
                                <td>Further away from central Thu Dau Mot expat residential enclaves</td>
                                <td>4.3 / 5</td>
                            </tr>"""

    old_loc_table = old_loc_table.replace('\r\n', '\n')
    new_loc_table = new_loc_table.replace('\r\n', '\n')

    if old_loc_table in bd_content:
        print("[binhduong.html] Found old location table. Replacing...")
        bd_content = bd_content.replace(old_loc_table, new_loc_table)
    else:
        print("[ERROR] Could not find location table in binhduong.html!")
        return

    # 9. Update Location Study Conclusion Box
    old_conclusion = """                <div class="conclusion-box">
                    <strong>Strategy:</strong> Lease an 800 sq ft ground-floor commercial unit in Thuan An near Aeon Mall/VSIP 1 to target the main expat traffic. Target rent: USD 795/month.
                </div>"""

    new_conclusion = """                <div class="conclusion-box">
                    <strong>Strategy:</strong> Lease an 800 sq ft ground-floor commercial unit in Thu Dau Mot City Core (Chanh Nghia) to target the main expat residential corridor. Target rent: USD 553/month.
                </div>"""

    old_conclusion = old_conclusion.replace('\r\n', '\n')
    new_conclusion = new_conclusion.replace('\r\n', '\n')

    if old_conclusion in bd_content:
        print("[binhduong.html] Found old conclusion box. Replacing...")
        bd_content = bd_content.replace(old_conclusion, new_conclusion)
    else:
        print("[ERROR] Could not find conclusion box in binhduong.html!")
        return

    # 10. Update Competitors Table
    old_competitors = """                             <tr>
                                <td>Premium Styling Salon</td>
                                <td>Toto Hair Studio</td>
                                <td>$12 - $60</td>
                                <td>Professional styling, high-end care, trendy hair</td>
                                <td>Open layout, loud environment, lacks specialized scalp therapy and privacy</td>
                                <td>Sound-isolated stations, integrated carbonated scalp rejuvenation</td>
                            </tr>
                            <tr>
                                <td>Luxury Styling Salon</td>
                                <td>Hair Salon Mr. D</td>
                                <td>$15 - $75</td>
                                <td>Luxury chemical service, professional perm/dye</td>
                                <td>Lacks dedicated scalp wellness and quiet relaxation pods</td>
                                <td>Private consultation, organic botanical colorants, restorative head spa</td>
                            </tr>
                            <tr>
                                <td>High-End Salon</td>
                                <td>Trendy Hair</td>
                                <td>$18 - $90</td>
                                <td>Modern high-tech treatment, spacious layout</td>
                                <td>Expensive service menu, busy street traffic, limited parking space</td>
                                <td>Quiet sanctuary vibe, microscopic camera scalp analysis, VIP style care</td>
                            </tr>"""

    new_competitors = """                             <tr>
                                <td>Premium Styling Salon</td>
                                <td>Toto Hair Studio</td>
                                <td>$12 - $60</td>
                                <td>Professional styling, modern coloring techniques</td>
                                <td>Open floor plan, high noise levels, standard chlorinated tap water</td>
                                <td>Semi-private styling stations, specialized water softener filtration for color retention</td>
                            </tr>
                            <tr>
                                <td>Luxury Styling Salon</td>
                                <td>Hair Salon Mr. D</td>
                                <td>$15 - $75</td>
                                <td>High-end chemical services (perm, dye, bleaching)</td>
                                <td>Lacks semi-private stations, uses untreated hard municipal water</td>
                                <td>Private styling areas, premium organic styling products, iron-filtering water treatment</td>
                            </tr>
                            <tr>
                                <td>High-End Salon</td>
                                <td>Trendy Hair</td>
                                <td>$18 - $90</td>
                                <td>Modern high-tech heat styling, spacious interior</td>
                                <td>Expensive services, limited parking, no soft-water systems for color care</td>
                                <td>Calm boutique environment, custom soft-water rinse, specialized hair recovery formulas</td>
                            </tr>"""

    old_competitors = old_competitors.replace('\r\n', '\n')
    new_competitors = new_competitors.replace('\r\n', '\n')

    if old_competitors in bd_content:
        print("[binhduong.html] Found old competitors table. Replacing...")
        bd_content = bd_content.replace(old_competitors, new_competitors)
    else:
        print("[ERROR] Could not find competitors table in binhduong.html!")
        return

    # 11. Update Product Menu & Packages (incorporating exact indentation of tbody and tags)
    old_menu_packages = """            <!-- 8. Product / Service Menu -->
            <section id="menu" class="card fade-in">
                <h2>8. Product / Service Menu</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Service Name</th>
                                <th>Duration</th>
                                <th>Target Price (USD)</th>
                                <th>Use Case</th>
                                <th>COGS Est. (USD)</th>
                                <th>Margin Logic</th>
                            </tr>
                        </thead>
<tbody>
                             <tr>
                                <td>Premium Cut & Styling</td>
                                <td>45 min</td>
                                <td>$20</td>
                                <td>Precision cut, shampoo, styling blowout</td>
                                <td>$2.00</td>
                                <td>90% (Entry tier)</td>
                            </tr>
                            <tr class="highlight-row">
                                <td>Carbonated Scalp Rejuvenation & Cut</td>
                                <td>75 min</td>
                                <td>$35</td>
                                <td>Japanese carbonated mist scalp therapy + stylist cut</td>
                                <td>$3.50</td>
                                <td>90% (Primary offer)</td>
                            </tr>
                            <tr>
                                <td>Organic Botanical Color & Restorative Spa</td>
                                <td>120 min</td>
                                <td>$55</td>
                                <td>Damage-free organic coloring + scalp detoxification</td>
                                <td>$5.50</td>
                                <td>90% (Color tier)</td>
                            </tr>
                            <tr>
                                <td>Signature Balayage / Perm & Therapy</td>
                                <td>150 min</td>
                                <td>$80</td>
                                <td>Artistic balayage or custom perm + intensive hair repair</td>
                                <td>$8.00</td>
                                <td>90% (Premium tier)</td>
                            </tr>
            </tbody>
                    </table>
                </div>
            </section>

            <!-- 9. Packages & Memberships -->
            <section id="packages" class="card fade-in">
                <h2>9. Packages & Memberships</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Tier Name</th>
                                <th>Price (USD)</th>
                                <th>Services Included</th>
                                <th>Validity</th>
                                <th>Target Conversion</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Expat Styling & Rejuvenation Pack (5 sessions)</td>
                                <td>$150 (15% off)</td>
                                <td>5x Carbonated Scalp Rejuvenation & Styling Cuts</td>
                                <td>6 Months</td>
                                <td>25% of new clients</td>
                            </tr>
                            <tr class="highlight-row">
                                <td>Oasis Salon Annual Membership (12 sessions)</td>
                                <td>$350 (15% off)</td>
                                <td>12x Carbonated Scalp Rejuvenation & Styling Cuts</td>
                                <td>12 Months</td>
                                <td>15% of repeat guests</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>"""

    new_menu_packages = """            <!-- 8. Product / Service Menu -->
            <section id="menu" class="card fade-in">
                <h2>8. Product / Service Menu</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Service Name</th>
                                <th>Duration</th>
                                <th>Target Price (USD)</th>
                                <th>Use Case</th>
                                <th>COGS Est. (USD)</th>
                                <th>Margin Logic</th>
                            </tr>
                        </thead>
<tbody>
                             <tr>
                                <td>Premium Cut & Styling</td>
                                <td>45 min</td>
                                <td>$20</td>
                                <td>Precision cut, soft-water rinse, styling blowout</td>
                                <td>$2.00</td>
                                <td>90% (Entry tier)</td>
                            </tr>
                            <tr class="highlight-row">
                                <td>Soft-Water Hair Detox & Cut</td>
                                <td>75 min</td>
                                <td>$35</td>
                                <td>Purified soft-water rinse + deep hair conditioning + custom cut</td>
                                <td>$3.50</td>
                                <td>90% (Primary offer)</td>
                            </tr>
                            <tr>
                                <td>Organic Botanical Color & Recovery</td>
                                <td>120 min</td>
                                <td>$55</td>
                                <td>Damage-free organic coloring + soft-water antioxidant rinse</td>
                                <td>$5.50</td>
                                <td>90% (Color tier)</td>
                            </tr>
                            <tr>
                                <td>Signature Balayage & Bond Repair</td>
                                <td>150 min</td>
                                <td>$80</td>
                                <td>Artistic balayage + intensive hair structural restoration</td>
                                <td>$8.00</td>
                                <td>90% (Premium tier)</td>
                            </tr>
            </tbody>
                    </table>
                </div>
            </section>

            <!-- 9. Packages & Memberships -->
            <section id="packages" class="card fade-in">
                <h2>9. Packages & Memberships</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Tier Name</th>
                                <th>Price (USD)</th>
                                <th>Services Included</th>
                                <th>Validity</th>
                                <th>Target Conversion</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Expat Styling & Soft-Water Detox Pack (5 sessions)</td>
                                <td>$150 (15% off)</td>
                                <td>5x Soft-Water Hair Detox & Custom Styling Cuts</td>
                                <td>6 Months</td>
                                <td>25% of new clients</td>
                            </tr>
                            <tr class="highlight-row">
                                <td>Oasis Salon Annual Membership (12 sessions)</td>
                                <td>$350 (15% off)</td>
                                <td>12x Soft-Water Hair Detox & Custom Styling Cuts</td>
                                <td>12 Months</td>
                                <td>15% of repeat guests</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>"""

    old_menu_packages = old_menu_packages.replace('\r\n', '\n')
    new_menu_packages = new_menu_packages.replace('\r\n', '\n')

    if old_menu_packages in bd_content:
        print("[binhduong.html] Found old menu & packages. Replacing...")
        bd_content = bd_content.replace(old_menu_packages, new_menu_packages)
    else:
        print("[ERROR] Could not find menu & packages in binhduong.html!")
        return

    # 12. Update Customer Journey & Setup Layout
    old_journey_layout = """            <!-- 10. Customer Journey -->
            <section id="customer-journey" class="card fade-in">
                <h2>10. Customer Journey</h2>
                <ol class="journey-list">
                    <li><strong>Booking:</strong> Online via Instagram/Whatsapp with automated slot booking.</li>
                    <li><strong>Welcome:</strong> Arrive in our cozy botanical lobby, served warm ginger tea.</li>
                    <li><strong>Analysis:</strong> Microscope check displays scalp health to the customer.</li>
                    <li><strong>Treatment:</strong> Transition to private custom track lighting VIP pod for carbonated therapy.</li>
                    <li><strong>Blowdry & Close:</strong> Post-treatment comparison scan, blowout styling, package promotion.</li>
                </ol>
            </section>

            <!-- 11. Setup & Layout -->
            <section id="setup-layout" class="card fade-in">
                <h2>11. Setup & Layout</h2>
                <div class="text-content">
                    
                     <p>The 800 sq ft space is optimized for visual privacy and client flow:</p>
                    <ul>
                        <li><strong>Lobby & Consultation (150 sqft):</strong> Botanical theme, organic product display.</li>
                        <li><strong>4 Premium Styling Stations (400 sqft):</strong> Custom vanity mirrors and professional styling chairs.</li>
                        <li><strong>2 Japanese Backwash Beds (150 sqft):</strong> Custom track lighting and carbonated water systems in quiet area.</li>
                        <li><strong>Storage & Utility (100 sqft):</strong> Carbonated generators, towel laundry, organic inventory.</li>
                    </ul>
            
                </div>
            </section>"""

    new_journey_layout = """            <!-- 10. Customer Journey -->
            <section id="customer-journey" class="card fade-in">
                <h2>10. Customer Journey</h2>
                <ol class="journey-list">
                    <li><strong>Booking:</strong> Online via Instagram/Whatsapp with automated slot booking.</li>
                    <li><strong>Welcome:</strong> Arrive in our cozy botanical lobby, served warm ginger tea.</li>
                    <li><strong>Analysis:</strong> Hair type and damage consultation to select organic formulas.</li>
                    <li><strong>Treatment:</strong> Transition to semi-private styling station for custom coloring and soft-water washing.</li>
                    <li><strong>Styling & Close:</strong> Premium blowout styling, color care maintenance tips, package promotion.</li>
                </ol>
            </section>

            <!-- 11. Setup & Layout -->
            <section id="setup-layout" class="card fade-in">
                <h2>11. Setup & Layout</h2>
                <div class="text-content">
                    
                     <p>The 800 sq ft ground-floor space is optimized for client flow and service efficiency:</p>
                    <ul>
                        <li><strong>Lobby & Consultation (150 sqft):</strong> Botanical theme, organic color swatch display.</li>
                        <li><strong>4 Premium Styling Stations (400 sqft):</strong> Custom vanity mirrors and professional styling chairs.</li>
                        <li><strong>2 Japanese Backwash Beds (150 sqft):</strong> Purified soft-water wash systems in quiet area.</li>
                        <li><strong>Storage & Utility (100 sqft):</strong> Multi-stage water filtration and softening tanks, towel laundry, color mixing bar.</li>
                    </ul>
            
                </div>
            </section>"""

    old_journey_layout = old_journey_layout.replace('\r\n', '\n')
    new_journey_layout = new_journey_layout.replace('\r\n', '\n')

    if old_journey_layout in bd_content:
        print("[binhduong.html] Found old journey and layout. Replacing...")
        bd_content = bd_content.replace(old_journey_layout, new_journey_layout)
    else:
        print("[ERROR] Could not find journey and layout in binhduong.html!")
        return

    # 13. Update Monthly OPEX and CAPEX Tables
    old_opex_capex = """            <!-- 13. Monthly OPEX -->
            <section id="opex" class="card fade-in">
                <h2>13. Monthly OPEX</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>OPEX Category</th>
                                <th>Monthly Cost (USD)</th>
                                <th>% of Total</th>
                                <th>Notes</th>
                            </tr>
                        </thead>
<tbody>
                             <tr class="highlight-row">
                                <td>Rent (Thuan An commercial unit)</td>
                                <td>$750</td>
                                <td>15.8%</td>
                                <td>800 sq ft unit</td>
                            </tr>
                            <tr class="highlight-row">
                                <td>Staff Salaries (4 total headcount)</td>
                                <td>$2,600</td>
                                <td>54.7%</td>
                                <td>Master Stylist, Senior Stylist, 2 Assistants</td>
                            </tr>
                            <tr>
                                <td>Marketing (Social/Expat ads)</td>
                                <td>$450</td>
                                <td>9.5%</td>
                                <td>Targeted campaigns for expats and locals</td>
                            </tr>
                            <tr>
                                <td>Utilities & Water Filtration</td>
                                <td>$350</td>
                                <td>7.4%</td>
                                <td>AC usage, hot water heaters, filters</td>
                            </tr>
                            <tr>
                                <td>Inventory & Consumables</td>
                                <td>$400</td>
                                <td>8.4%</td>
                                <td>Shampoos, conditioners, colorants</td>
                            </tr>
                            <tr>
                                <td>POS, Insurance & Misc</td>
                                <td>$200</td>
                                <td>4.2%</td>
                                <td>Booking software license, cleaning supplies</td>
                            </tr>
                            <tr class="total-row">
                                <td><strong>Total Monthly OPEX</strong></td>
                                <td><strong>$4,750</strong></td>
                                <td><strong>100%</strong></td>
                                <td><strong>Optimized operations budget</strong></td>
                            </tr>
            </tbody>
                    </table>
                </div>
            </section>

            <!-- 14. CAPEX -->
            <section id="capex" class="card fade-in">
                <h2>14. Initial CAPEX Estimate</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>CAPEX Item</th>
                                <th>Estimated Cost (USD)</th>
                                <th>Notes</th>
                            </tr>
                        </thead>
<tbody>
                             <tr class="highlight-row">
                                <td>Renovation & Partitioning</td>
                                <td>$7,500</td>
                                <td>Styling stations fitout, lighting, flooring</td>
                            </tr>
                            <tr class="highlight-row">
                                <td>Equipment (4 stations, 2 styling chairs)</td>
                                <td>$4,500</td>
                                <td>Styling chairs, vanities, backstyling chairs</td>
                            </tr>
                            <tr>
                                <td>Rental Deposit (3 Months)</td>
                                <td>$2,250</td>
                                <td>Refundable commercial lease deposit</td>
                            </tr>
                            <tr>
                                <td>Plumbing, Heating & Filtration</td>
                                <td>$2,500</td>
                                <td>Boiler systems, water pumps, carbon filters</td>
                            </tr>
                            <tr>
                                <td>Professional Styling Tools</td>
                                <td>$1,500</td>
                                <td>Blow dryers, curling irons, scissors, clippers</td>
                            </tr>
                            <tr>
                                <td>Working Capital & Inventory</td>
                                <td>$3,250</td>
                                <td>Opening inventory, licensing, cash reserves</td>
                            </tr>
                            <tr class="total-row">
                                <td><strong>Total Initial CAPEX</strong></td>
                                <td><strong>$21,500</strong></td>
                                <td><strong>Investment midpoint (Range: $19k - $24k)</strong></td>
                            </tr>
            </tbody>
                    </table>
                </div>
            </section>"""

    new_opex_capex = """            <!-- 13. Monthly OPEX -->
            <section id="opex" class="card fade-in">
                <h2>13. Monthly OPEX</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>OPEX Category</th>
                                <th>Monthly Cost (USD)</th>
                                <th>% of Total</th>
                                <th>Notes</th>
                            </tr>
                        </thead>
<tbody>
                             <tr class="highlight-row">
                                <td>Rent (Chanh Nghia commercial unit)</td>
                                <td>$553</td>
                                <td>12.1%</td>
                                <td>800 sq ft ground-floor unit</td>
                            </tr>
                            <tr class="highlight-row">
                                <td>Staff Salaries (4 total headcount)</td>
                                <td>$2,600</td>
                                <td>57.1%</td>
                                <td>Master Stylist, Senior Stylist, 2 Assistants</td>
                            </tr>
                            <tr>
                                <td>Marketing (Social/Expat ads)</td>
                                <td>$450</td>
                                <td>9.9%</td>
                                <td>Targeted campaigns for expats and locals</td>
                            </tr>
                            <tr>
                                <td>Utilities & Water Softener Replacement</td>
                                <td>$350</td>
                                <td>7.7%</td>
                                <td>AC usage, hot water, salt/filters replacement</td>
                            </tr>
                            <tr>
                                <td>Inventory & Consumables</td>
                                <td>$400</td>
                                <td>8.8%</td>
                                <td>Organic dyes, developers, haircare products</td>
                            </tr>
                            <tr>
                                <td>POS, Insurance & Misc</td>
                                <td>$200</td>
                                <td>4.4%</td>
                                <td>Booking software license, cleaning supplies</td>
                            </tr>
                            <tr class="total-row">
                                <td><strong>Total Monthly OPEX</strong></td>
                                <td><strong>$4,553</strong></td>
                                <td><strong>100%</strong></td>
                                <td><strong>Optimized operations budget</strong></td>
                            </tr>
            </tbody>
                    </table>
                </div>
            </section>

            <!-- 14. CAPEX -->
            <section id="capex" class="card fade-in">
                <h2>14. Initial CAPEX Estimate</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>CAPEX Item</th>
                                <th>Estimated Cost (USD)</th>
                                <th>Notes</th>
                            </tr>
                        </thead>
<tbody>
                             <tr class="highlight-row">
                                <td>Renovation & Partitioning</td>
                                <td>$7,500</td>
                                <td>Styling stations fitout, mirrors, lighting, flooring</td>
                            </tr>
                            <tr class="highlight-row">
                                <td>Equipment (4 stations, 2 styling chairs)</td>
                                <td>$4,500</td>
                                <td>Styling chairs, backstyling washbeds, vanities</td>
                            </tr>
                            <tr>
                                <td>Rental Deposit (3 Months)</td>
                                <td>$1,659</td>
                                <td>Refundable commercial lease deposit ($553/month)</td>
                            </tr>
                            <tr>
                                <td>Plumbing, Heating & Water Softening System</td>
                                <td>$2,500</td>
                                <td>Multi-stage carbon & resin filtration (iron & hardness removal)</td>
                            </tr>
                            <tr>
                                <td>Professional Styling Tools</td>
                                <td>$1,500</td>
                                <td>Blow dryers, hair straighteners, scissors, color tools</td>
                            </tr>
                            <tr>
                                <td>Working Capital & Inventory</td>
                                <td>$3,250</td>
                                <td>Opening dye & product inventory, local business license</td>
                            </tr>
                            <tr class="total-row">
                                <td><strong>Total Initial CAPEX</strong></td>
                                <td><strong>$20,909</strong></td>
                                <td><strong>Investment midpoint (Range: $19k - $23k)</strong></td>
                            </tr>
            </tbody>
                    </table>
                </div>
            </section>"""

    old_opex_capex = old_opex_capex.replace('\r\n', '\n')
    new_opex_capex = new_opex_capex.replace('\r\n', '\n')

    if old_opex_capex in bd_content:
        print("[binhduong.html] Found old opex/capex tables. Replacing...")
        bd_content = bd_content.replace(old_opex_capex, new_opex_capex)
    else:
        print("[ERROR] Could not find opex/capex tables in binhduong.html!")
        return

    # 14. Update Unit Economics and Setup Timeline
    old_economics_timeline = """            <!-- 15. Unit Economics -->
            <section id="economics" class="card fade-in">
                <h2>15. Unit Economics</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Scenario</th>
                                <th>Monthly Customers</th>
                                <th>Monthly Revenue (USD)</th>
                                <th>COGS (10%)</th>
                                <th>OPEX (USD)</th>
                                <th>Net Monthly Profit (USD)</th>
                            </tr>
                        </thead>
<tbody>
                             <tr>
                                <td>Breakeven Case</td>
                                <td>147 customers</td>
                                <td>$5,292</td>
                                <td>$529</td>
                                <td>$4,750</td>
                                <td>$13 (Approx. 0)</td>
                              </tr>
                              <tr class="highlight-row">
                                <td>Base Case</td>
                                <td>397 customers</td>
                                <td>$14,292</td>
                                <td>$1,429</td>
                                <td>$4,750</td>
                                <td>$8,113</td>
                              </tr>
                              <tr>
                                <td>High-Performance Case</td>
                                <td>500 customers</td>
                                <td>$18,000</td>
                                <td>$1,800</td>
                                <td>$4,750</td>
                                <td>$11,450</td>
                              </tr>
            </tbody>
                    </table>
                </div>
            
                <div class="conclusion-box" style="margin-top: 2rem; border-left-color: var(--success); background: rgba(16, 185, 129, 0.02);">
                    <h3 style="color: var(--success); font-size: 1.2rem; margin-bottom: 0.5rem; font-family: var(--font-heading);">Post-Tax Financial Feasibility Analysis</h3>
                    <p>All calculations in the table above represent pre-tax performance. Factoring in the local Corporate Income Tax (CIT) rate of <strong>20.0%</strong>, we arrive at the following post-tax projections for the Base Case:</p>
                    <ul style="margin-top: 0.5rem; margin-left: 1.5rem; list-style-type: disc;">
                        <li><strong>Base Case Pre-Tax Monthly Net Profit:</strong> USD 8,113</li>
                        <li><strong>Estimated Monthly Corporate Income Tax:</strong> USD 1,623</li>
                        <li><strong>Post-Tax Net Monthly Profit (PAT):</strong> USD 6,490</li>
                        <li><strong>Post-Tax Profit to OPEX Ratio:</strong> <strong>137% (Post-Tax)</strong> (vs. 171% pre-tax)</li>
                        <li><strong>Post-Tax CAPEX Payback Period:</strong> <strong>3 Months</strong> (vs. 2.6 months pre-tax)</li>
                    </ul>
                </div>
            </section>

            <!-- 16. Setup Timeline -->
            <section id="timeline" class="card fade-in">
                <h2>16. Setup Timeline</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Milestone Phase</th>
                                <th>Duration</th>
                                <th>Key Tasks</th>
                            </tr>
                        </thead>
<tbody>
                             <tr>
                                <td>Phase 1: Legal & Property search</td>
                                <td>Weeks 1 - 4</td>
                                <td>Lease signed in Binh Duong, local corporate setup registered</td>
                            </tr>
                            <tr>
                                <td>Phase 2: Construction</td>
                                <td>Weeks 5 - 9</td>
                                <td>Styling stations & backstyling chairs built, OEM equipment installed</td>
                            </tr>"""

    new_economics_timeline = """            <!-- 15. Unit Economics -->
            <section id="economics" class="card fade-in">
                <h2>15. Unit Economics</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Scenario</th>
                                <th>Monthly Customers</th>
                                <th>Monthly Revenue (USD)</th>
                                <th>COGS (10%)</th>
                                <th>OPEX (USD)</th>
                                <th>Net Monthly Profit (USD)</th>
                            </tr>
                        </thead>
<tbody>
                             <tr>
                                <td>Breakeven Case</td>
                                <td>141 customers</td>
                                <td>$5,076</td>
                                <td>$508</td>
                                <td>$4,553</td>
                                <td>$15 (Approx. 0)</td>
                              </tr>
                              <tr class="highlight-row">
                                <td>Base Case</td>
                                <td>457 customers</td>
                                <td>$16,452</td>
                                <td>$1,645</td>
                                <td>$4,553</td>
                                <td>$10,254</td>
                              </tr>
                              <tr>
                                <td>High-Performance Case</td>
                                <td>520 customers</td>
                                <td>$18,720</td>
                                <td>$1,872</td>
                                <td>$4,553</td>
                                <td>$12,295</td>
                              </tr>
            </tbody>
                    </table>
                </div>
            
                <div class="conclusion-box" style="margin-top: 2rem; border-left-color: var(--success); background: rgba(16, 185, 129, 0.02);">
                    <h3 style="color: var(--success); font-size: 1.2rem; margin-bottom: 0.5rem; font-family: var(--font-heading);">Post-Tax Financial Feasibility Analysis</h3>
                    <p>All calculations in the table above represent pre-tax performance. Factoring in the local Corporate Income Tax (CIT) rate of <strong>20.0%</strong>, we arrive at the following post-tax projections for the Base Case:</p>
                    <ul style="margin-top: 0.5rem; margin-left: 1.5rem; list-style-type: disc;">
                        <li><strong>Base Case Pre-Tax Monthly Net Profit:</strong> USD 10,254</li>
                        <li><strong>Estimated Monthly Corporate Income Tax:</strong> USD 2,051</li>
                        <li><strong>Post-Tax Net Monthly Profit (PAT):</strong> USD 8,203</li>
                        <li><strong>Post-Tax Profit to OPEX Ratio:</strong> <strong>180% (Post-Tax)</strong> (vs. 225% pre-tax)</li>
                        <li><strong>Post-Tax CAPEX Payback Period:</strong> <strong>3 Months</strong> (vs. 2.0 months pre-tax)</li>
                    </ul>
                </div>
            </section>

            <!-- 16. Setup Timeline -->
            <section id="timeline" class="card fade-in">
                <h2>16. Setup Timeline</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Milestone Phase</th>
                                <th>Duration</th>
                                <th>Key Tasks</th>
                            </tr>
                        </thead>
<tbody>
                             <tr>
                                <td>Phase 1: Legal & Property search</td>
                                <td>Weeks 1 - 4</td>
                                <td>Lease signed in Binh Duong, local corporate setup registered</td>
                            </tr>
                            <tr>
                                <td>Phase 2: Construction</td>
                                <td>Weeks 5 - 9</td>
                                <td>4 styling stations & 2 backwash beds built, water softening filter system installed</td>
                            </tr>"""

    old_economics_timeline = old_economics_timeline.replace('\r\n', '\n')
    new_economics_timeline = new_economics_timeline.replace('\r\n', '\n')

    if old_economics_timeline in bd_content:
        print("[binhduong.html] Found old economics/timeline. Replacing...")
        bd_content = bd_content.replace(old_economics_timeline, new_economics_timeline)
    else:
        print("[ERROR] Could not find economics/timeline in binhduong.html!")
        return

    # 15. Update Recommendation
    old_recommendation = """            <!-- 19. Recommendation -->
            <section id="recommendation" class="card fade-in">
                <h2>19. Final Recommendation</h2>
                <div class="conclusion-box success-box">

                     <h3>Decision: GO (Industrial Corridor PoC)</h3>
                    <ul>
                        <li><strong>Location:</strong> Thuan An shophouse near Aeon Mall.</li>
                        <li><strong>Setup:</strong> 4 Styling Stations, 2 Backwash Beds, 800 sq ft.</li>
                        <li><strong>Budget Ceiling:</strong> USD 24,000.</li>
                        <li><strong>Expansion Trigger:</strong> Achieve USD 15k monthly revenue with 20%+ membership retention for 3 consecutive months before looking at Thu Dau Mot city center.</li>
                    </ul>
            
                </div>
            </section>"""

    new_recommendation = """            <!-- 19. Recommendation -->
            <section id="recommendation" class="card fade-in">
                <h2>19. Final Recommendation</h2>
                <div class="conclusion-box success-box">

                     <h3>Decision: GO (Chanh Nghia Expat PoC)</h3>
                    <ul>
                        <li><strong>Location:</strong> Thu Dau Mot City Core (Chanh Nghia) shophouse.</li>
                        <li><strong>Setup:</strong> 4 Styling Stations, 2 Backwash Beds, 800 sq ft.</li>
                        <li><strong>Budget Ceiling:</strong> USD 23,000.</li>
                        <li><strong>Expansion Trigger:</strong> Achieve USD 15k monthly revenue with 20%+ membership retention for 3 consecutive months before looking at Thuan An (near Aeon Mall).</li>
                    </ul>
            
                </div>
            </section>"""

    old_recommendation = old_recommendation.replace('\r\n', '\n')
    new_recommendation = new_recommendation.replace('\r\n', '\n')

    if old_recommendation in bd_content:
        print("[binhduong.html] Found old recommendation. Replacing...")
        bd_content = bd_content.replace(old_recommendation, new_recommendation)
    else:
        print("[ERROR] Could not find recommendation in binhduong.html!")
        return

    # 16. Update inline JS competitors
    old_competitors_js = """        // Competitors
        const competitors = [
            { name: "Toto Hair Studio", price: "US$12-60", footfall: 75, lat: 10.9754, lng: 106.6660, comment: "Trendy Chanh Nghia hair salon. Good modern styling and recovery services, but noisy open floor layout." },
            { name: "Hair Salon Mr. D", price: "US$15-75", footfall: 70, lat: 10.9702, lng: 106.6610, comment: "Luxury hair styling salon. Good chemical services (perm/dye) but lacks private styling stations and scalp therapy." },
            { name: "Trendy Hair", price: "US$18-90", footfall: 65, lat: 10.9730, lng: 106.6690, comment: "High-end salon with advanced styling services. Expensive, situated in busy residential area with limited parking." }
        ];"""

    new_competitors_js = """        // Competitors
        const competitors = [
            { name: "Toto Hair Studio", price: "US$12-60", footfall: 75, lat: 10.9754, lng: 106.6660, comment: "Trendy Chanh Nghia hair salon. Good modern styling and color services, but noisy open floor layout and untreated hard water." },
            { name: "Hair Salon Mr. D", price: "US$15-75", footfall: 70, lat: 10.9702, lng: 106.6610, comment: "Luxury hair styling salon. Good chemical services (perm/dye) but lacks private styling stations and professional water softening systems." },
            { name: "Trendy Hair", price: "US$18-90", footfall: 65, lat: 10.9730, lng: 106.6690, comment: "High-end salon with advanced styling services. Expensive, situated in busy residential area with standard tap water." }
        ];"""

    old_competitors_js = old_competitors_js.replace('\r\n', '\n')
    new_competitors_js = new_competitors_js.replace('\r\n', '\n')

    if old_competitors_js in bd_content:
        print("[binhduong.html] Found old competitors JS. Replacing...")
        bd_content = bd_content.replace(old_competitors_js, new_competitors_js)
    else:
        print("[ERROR] Could not find competitors JS in binhduong.html!")
        return

    # 17. Update inline JS candidates
    old_candidates_js = """        // Shop Candidates
        const candidates = [
            { 
                name: "Candidate A: Thuan An Shophouse Unit (near Aeon Mall)", 
                lat: 10.9330, 
                lng: 106.6970, 
                note: "Top recommendation. Near Aeon Mall. Excellent visibility, parking, and premium expat access.", 
                rent: 795,
                catchment: 30000,
                premiumTargetPct: 28.8,
                competitorCapacity: 4500,
                airportTime: "45 mins from SGN"
            },
            { 
                name: "Candidate B: Thu Dau Mot City Shoplot (Chanh Nghia)", 
                lat: 10.9780, 
                lng: 106.6560, 
                note: "Located in Chanh Nghia expat quarter. Excellent walk-in potential, but parking is constrained during business hours.", 
                rent: 650,
                catchment: 20000,
                premiumTargetPct: 21.6,
                competitorCapacity: 3375,
                airportTime: "55 mins from SGN"
            }
        ];"""

    new_candidates_js = """        // Shop Candidates
        const candidates = [
            { 
                name: "Candidate A: Thuan An Shophouse Unit (near Aeon Mall)", 
                lat: 10.9330, 
                lng: 106.6970, 
                note: "Alternative option near Aeon Mall in Thuan An. Excellent visibility, but further from the central Chanh Nghia expat enclaves.", 
                rent: 676,
                catchment: 30000,
                premiumTargetPct: 34.6,
                competitorCapacity: 6750,
                airportTime: "45 mins from SGN"
            },
            { 
                name: "Candidate B: Thu Dau Mot City Shoplot (Chanh Nghia)", 
                lat: 10.9780, 
                lng: 106.6560, 
                note: "Top recommendation. Located in Chanh Nghia expat quarter. Excellent walk-in potential and high concentration of foreign managers.", 
                rent: 553,
                catchment: 20000,
                premiumTargetPct: 25.9,
                competitorCapacity: 5063,
                airportTime: "55 mins from SGN"
            }
        ];"""

    old_candidates_js = old_candidates_js.replace('\r\n', '\n')
    new_candidates_js = new_candidates_js.replace('\r\n', '\n')

    if old_candidates_js in bd_content:
        print("[binhduong.html] Found old candidates JS. Replacing...")
        bd_content = bd_content.replace(old_candidates_js, new_candidates_js)
    else:
        print("[ERROR] Could not find candidates JS in binhduong.html!")
        return

    # Write files back
    # Convert all LF back to CRLF or keep LF. Git status warning mentions CRLF conversion, so keeping LF is fine.
    with open(bd_path, 'w', encoding='utf-8') as f:
        f.write(bd_content)
    print("[binhduong.html] Successfully updated!")

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("[script.js] Successfully updated!")

if __name__ == '__main__':
    main()
