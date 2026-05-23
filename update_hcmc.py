import re

# Read hcmc.html
with open('hcmc.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Executive Summary Stats
old_stats = """                <div class="grid-stats">
                    <div class="stat-box">
                        <span class="label">Recommendation</span>
                        <span class="value success">Proceed (Expat Salon PoC)</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Setup Size</span>
                        <span class="value">800 sq ft</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Initial CAPEX</span>
                        <span class="value">USD 65k - 75k</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Monthly OPEX</span>
                        <span class="value">USD 9,400</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Breakeven Volume</span>
                        <span class="value">~4.1 Customers / Day</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Average Ticket</span>
                        <span class="value">USD 85</span>
                    </div>
                </div>"""

new_stats = """                <div class="grid-stats">
                    <div class="stat-box">
                        <span class="label">Recommendation</span>
                        <span class="value success">Proceed (Premium Salon MVP)</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Setup Size</span>
                        <span class="value">800 sq ft</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Initial CAPEX</span>
                        <span class="value">USD 90k - 110k</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Monthly OPEX</span>
                        <span class="value">USD 10,700</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Breakeven Volume</span>
                        <span class="value">~4.2 Customers / Day</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Average Ticket</span>
                        <span class="value">USD 95</span>
                    </div>
                </div>"""

content = content.replace(old_stats, new_stats)

# 2. Executive Summary Success Condition Description
old_sc = '<p><strong>Main Success Condition:</strong> Establishing the PoC in District 1/3 (Vo Thi Sau / Dong Khoi) to capture affluent Vietnamese professionals, Japanese/Korean/Western expat executives and their spouses near key retail and business districts. The focus is to build a prestige-based relationship with high-margin creative color work, premium cuts, and advanced scalp rejuvenation, supported by high-retention package models.</p>'
new_sc = '<p><strong>Main Success Condition:</strong> Establishing the salon in District 1/3 or Thao Dien to capture affluent Vietnamese professionals, Japanese/Korean/Western expat executives and their spouses near key retail and business districts. The focus is to build a prestige-based relationship with high-margin creative color work, premium cuts, and advanced hair therapies, supported by high-retention package models.</p>'
content = content.replace(old_sc, new_sc)

# 3. Target Customer Segments Table
old_segments_tbody = """                        <tbody>
                            <tr>
                                <td>Expat Corporate Pros</td>
                                <td><span class="badge high">High</span></td>
                                <td>English-speaking stylist, professional business cuts, scalp detox from city pollution</td>
                                <td>$50 - $120</td>
                                <td>Google Maps, LinkedIn, Expat networks</td>
                                <td>"Precision Cut & Scalp Treatment"</td>
                            </tr>
                            <tr>
                                <td>Expat Spouses & Mothers</td>
                                <td><span class="badge high">High</span></td>
                                <td>Prestige color work (balayage), hair health, relaxed daytime environment</td>
                                <td>$100 - $180</td>
                                <td>Word of mouth, Instagram, LINE groups</td>
                                <td>"Signature Balayage & Highlights"</td>
                            </tr>
                            <tr>
                                <td>Affluent Locals</td>
                                <td><span class="badge med">Medium</span></td>
                                <td>Status-driven services, trend styling, advanced hair treatments (botox)</td>
                                <td>$80 - $150</td>
                                <td>Instagram, TikTok, local KOLs</td>
                                <td>"Luxury Hair Botox & Rejuvenation"</td>
                            </tr>
                        </tbody>"""

new_segments_tbody = """                        <tbody>
                            <tr>
                                <td>Expat Corporate Pros</td>
                                <td><span class="badge high">High</span></td>
                                <td>English-fluent international styling, precision cuts, damage-free coloring, and chlorine protection from tap water</td>
                                <td>$50 - $120</td>
                                <td>Google Maps, LinkedIn, Expat networks</td>
                                <td>"Precision Cut, Styling & Soft-Water Detox"</td>
                            </tr>
                            <tr>
                                <td>Expat Spouses & Mothers</td>
                                <td><span class="badge high">High</span></td>
                                <td>Advanced dimensional color work (balayage, highlights), premium hair care, and color protection from local water</td>
                                <td>$100 - $180</td>
                                <td>Word of mouth, Instagram, LINE groups</td>
                                <td>"Signature Balayage & Highlights"</td>
                            </tr>
                            <tr>
                                <td>Affluent Locals</td>
                                <td><span class="badge med">Medium</span></td>
                                <td>Trend styling, creative coloring, damage repair treatments (Olaplex/Botox), and soft-water hair wash</td>
                                <td>$80 - $150</td>
                                <td>Instagram, TikTok, local KOLs</td>
                                <td>"Creative Color, Cut & Hair Botox"</td>
                            </tr>
                        </tbody>"""

content = content.replace(old_segments_tbody, new_segments_tbody)

# 4. Location Study Table and Strategy Box
old_loc_table_tbody = """                        <tbody>
                            <tr class="highlight-row">
                                <td>District 3 (Vo Thi Sau / Turtle Lake)</td>
                                <td>USD 1,400 - 2,200</td>
                                <td>Leafy boutique villa zone, quiet artistic feel, spacious layouts, easier parking</td>
                                <td>Lower street-level footfall, destination-driven booking</td>
                                <td>4.9 / 5 (Recommended)</td>
                            </tr>
                            <tr>
                                <td>District 1 (Dong Khoi / Ben Nghe)</td>
                                <td>USD 2,200 - 3,500</td>
                                <td>Ultra-luxury retail street, high expat corporate executive & tourist traffic</td>
                                <td>Extremely high rent, parking and utility limits</td>
                                <td>4.8 / 5</td>
                            </tr>
                            <tr>
                                <td>Thao Dien (District 2)</td>
                                <td>USD 1,200 - 1,800</td>
                                <td>Expat residential enclave, high-income families</td>
                                <td>Highly competitive, further away from central corporate core</td>
                                <td>4.5 / 5</td>
                            </tr>
                        </tbody>"""

new_loc_table_tbody = """                        <tbody>
                            <tr class="highlight-row">
                                <td>District 3 (Vo Thi Sau / Turtle Lake)</td>
                                <td>USD 1,190 - 1,870</td>
                                <td>Leafy boutique villa zone, quiet artistic feel, spacious layouts, easier parking</td>
                                <td>Lower street-level footfall, destination-driven booking</td>
                                <td>4.9 / 5 (Recommended)</td>
                            </tr>
                            <tr>
                                <td>District 1 (Dong Khoi / Ben Nghe)</td>
                                <td>USD 1,870 - 2,975</td>
                                <td>Ultra-luxury retail street, high expat corporate executive & tourist traffic</td>
                                <td>Extremely high rent, parking and utility limits</td>
                                <td>4.8 / 5</td>
                            </tr>
                            <tr>
                                <td>Thao Dien (District 2)</td>
                                <td>USD 1,020 - 1,530</td>
                                <td>Expat residential enclave, high-income families</td>
                                <td>Highly competitive, further away from central corporate core</td>
                                <td>4.5 / 5</td>
                            </tr>
                        </tbody>"""

content = content.replace(old_loc_table_tbody, new_loc_table_tbody)

old_loc_conclusion = 'Strategy: Establish the boutique salon in District 3 (Vo Thi Sau St) in a premium villa-style unit. Rent target: USD 1,600/month (scaled to USD 1,360) for a 800 sq ft space. This balances prestige, layout flexibility, and reasonable fixed rent.'
new_loc_conclusion = 'Strategy: Establish the boutique salon in District 1/3 (Vo Thi Sau St) in a premium ground-floor unit. Rent target: USD 2,000/month for a 800 sq ft space. This balances prestige, layout flexibility, and reasonable fixed rent.'
content = content.replace(old_loc_conclusion, new_loc_conclusion)

# 5. Competitor Study Table
old_comp_tbody = """                        <tbody>
                            <tr>
                                <td>Japanese Luxury Salons</td>
                                <td>J-First Tokyo (D1)</td>
                                <td>$40 - $200</td>
                                <td>Premium reputation, Japanese stylists, strong expat base</td>
                                <td>Located in D1; booking backlog, high color prices</td>
                                <td>Integrated specialized scalp care, more competitive pricing</td>
                            </tr>
                            <tr>
                                <td>French Premium Salons</td>
                                <td>Concept Coiffure (D3)</td>
                                <td>$35 - $180</td>
                                <td>Established expat clientele, western-style styling</td>
                                <td>High price point, less focus on head spa/scalp care</td>
                                <td>Scalp-hair fusion therapies, semi-private styling bays</td>
                            </tr>
                            <tr>
                                <td>Trendy Local Salons</td>
                                <td>Vampire Hair Salon (D1/D3)</td>
                                <td>$25 - $120</td>
                                <td>Popular on social media, excellent balayage</td>
                                <td>Loud, crowded open layout, basic wash station comfort</td>
                                <td>Private, quiet styling stations, high-end relaxing experience</td>
                            </tr>
                        </tbody>"""

new_comp_tbody = """                        <tbody>
                            <tr>
                                <td>Japanese Luxury Salons</td>
                                <td>J-First Tokyo (D1/D3)</td>
                                <td>$40 - $200</td>
                                <td>Premium reputation, Japanese stylists, strong expat base</td>
                                <td>Busy D1 street noise, long booking backlog, premium pricing</td>
                                <td>Quiet styling bays, soft-water hair rinse, and luxury styling stations</td>
                            </tr>
                            <tr>
                                <td>French Premium Salons</td>
                                <td>Concept Coiffure (Thao Dien)</td>
                                <td>$35 - $180</td>
                                <td>Established expat clientele, western-style styling</td>
                                <td>High price point, lacks water filtration to prevent chlorine/mineral fade</td>
                                <td>Double water filtration, Western styling standards, and competitive pricing packages</td>
                            </tr>
                            <tr>
                                <td>Trendy Premium Salons</td>
                                <td>Vamp Hair Line (D1)</td>
                                <td>$25 - $150</td>
                                <td>Japanese Peek-A-Boo style training, excellent balayage and highlights</td>
                                <td>Loud, high-turnover environment, lack of personalized styling stations comfort</td>
                                <td>Quiet, ground-floor premium boutique styling bays, damage-free organic dyes, and filtered soft-water care</td>
                            </tr>
                        </tbody>"""

content = content.replace(old_comp_tbody, new_comp_tbody)

# 6. Product Service Menu Table
old_menu_tbody = """                        <tbody>
                            <tr>
                                <td>Express Cut & Blowout</td>
                                <td>45m</td>
                                <td>$35</td>
                                <td>Quick wash, trim, and styling blowout for events</td>
                                <td>$3.50</td>
                                <td>90% - Volume builder</td>
                            </tr>
                            <tr>
                                <td>Precision Cut & Scalp Treatment</td>
                                <td>60m</td>
                                <td>$65</td>
                                <td>Detailed hair shaping and deep scalp cleansing</td>
                                <td>$6.50</td>
                                <td>90% - Core service</td>
                            </tr>
                            <tr>
                                <td>Luxury Hair Botox & Rejuvenation</td>
                                <td>75m</td>
                                <td>$95</td>
                                <td>Deep structural hair repair and follicle styling</td>
                                <td>$9.50</td>
                                <td>90% - High-end care</td>
                            </tr>
                            <tr>
                                <td>Signature Balayage & Highlights</td>
                                <td>120m</td>
                                <td>$145</td>
                                <td>Creative coloring, custom balayage, and full blowout</td>
                                <td>$14.50</td>
                                <td>90% - High ticket upsell</td>
                            </tr>
                        </tbody>"""

new_menu_tbody = """                        <tbody>
                            <tr>
                                <td>Signature Precision Cut & Blowout</td>
                                <td>60 min</td>
                                <td>$40</td>
                                <td>Quick wash, trim, and styling blowout for events</td>
                                <td>$4.00</td>
                                <td>90% - Volume builder</td>
                            </tr>
                            <tr>
                                <td>Precision Cut & Scalp Treatment</td>
                                <td>75 min</td>
                                <td>$70</td>
                                <td>Detailed hair shaping and deep scalp cleansing with soft water</td>
                                <td>$7.00</td>
                                <td>90% - Core service</td>
                            </tr>
                            <tr>
                                <td>Luxury Hair Botox & Rejuvenation</td>
                                <td>90 min</td>
                                <td>$120</td>
                                <td>Intensive deep-conditioning fiber repair for damaged hair</td>
                                <td>$12.00</td>
                                <td>90% - High-end care</td>
                            </tr>
                            <tr>
                                <td>Signature Balayage & Highlights</td>
                                <td>180 min</td>
                                <td>$185</td>
                                <td>Premium artistic hand-painted coloring, toner, and blowout styling</td>
                                <td>$18.50</td>
                                <td>90% - High ticket upsell</td>
                            </tr>
                        </tbody>"""

content = content.replace(old_menu_tbody, new_menu_tbody)

# 7. Packages and Memberships boxes
old_packages = """                    <div class="stat-box">
                        <span class="label">Precision Cut & Style Pack</span>
                        <span class="value">$290</span>
                        <span class="subtext">5x Precision Cut sessions ($58/session, 3 mo)</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Rejuvenation & Botox Pack</span>
                        <span class="value">$420</span>
                        <span class="subtext">5x Hair Botox & Scalp Care sessions ($84/session, 3 mo)</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Signature Balayage Club</span>
                        <span class="value">$650</span>
                        <span class="subtext">5x Balayage & Highlights/Touch-up sessions ($130/session, 6 mo)</span>
                    </div>"""

new_packages = """                    <div class="stat-box">
                        <span class="label">Precision Cut & Scalp Pack</span>
                        <span class="value">$300</span>
                        <span class="subtext">5x Precision Cut & Scalp Treatment sessions ($60/session, 3 mo)</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Rejuvenation & Botox Pack</span>
                        <span class="value">$510</span>
                        <span class="subtext">5x Hair Botox & Rejuvenation sessions ($102/session, 3 mo)</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Signature Balayage Club</span>
                        <span class="value">$785</span>
                        <span class="subtext">5x Balayage & Highlights/Touch-up sessions ($157/session, 6 mo)</span>
                    </div>"""

content = content.replace(old_packages, new_packages)

# 8. Layout table Backwash area description
old_backwash_layout = '<td>2 luxury backstyling chairs/basins, head spa steam water rings</td>'
new_backwash_layout = '<td>2 luxury backwash beds, double-filtration water systems</td>'
content = content.replace(old_backwash_layout, new_backwash_layout)

# 9. Staffing Model table and note
old_staff_tbody = """                        <tbody>
                            <tr>
                                <td>Salon Director / Master Stylist</td>
                                <td>1</td>
                                <td>$1,500</td>
                                <td>5% of store monthly net revenue</td>
                            </tr>
                            <tr>
                                <td>Senior Hair Stylist</td>
                                <td>1</td>
                                <td>$1,000</td>
                                <td>10% service commission</td>
                            </tr>
                            <tr>
                                <td>Assistant Stylist / Junior Washer</td>
                                <td>2</td>
                                <td>$450</td>
                                <td>Performance bonuses & service tips</td>
                            </tr>
                        </tbody>"""

new_staff_tbody = """                        <tbody>
                            <tr>
                                <td>Salon Director / Master Stylist</td>
                                <td>1</td>
                                <td>$2,000</td>
                                <td>Senior styling work, English consultation, and overall management</td>
                            </tr>
                            <tr>
                                <td>Senior Hair Stylist</td>
                                <td>1</td>
                                <td>$1,200</td>
                                <td>Premium cuts, complex coloring, balayage, and training assistants</td>
                            </tr>
                            <tr>
                                <td>Assistant Stylist / Junior Washer</td>
                                <td>2</td>
                                <td>$500</td>
                                <td>Shampooing, head massage, blowouts, color prep, and client care</td>
                            </tr>
                        </tbody>"""

content = content.replace(old_staff_tbody, new_staff_tbody)

old_staff_note = '<em>Total Base Payroll: USD 3,400/month (+Social Security & Loaded Insurance buffers = USD 4,800/mo)</em>'
new_staff_note = '<em>Total Base Payroll: USD 4,200/month (+Social Security & Loaded Insurance buffers = USD 5,400/mo)</em>'
content = content.replace(old_staff_note, new_staff_note)

# 10. Monthly OPEX Table
old_opex_tbody = """                        <tbody>
                            <tr>
                                <td>Rent</td>
                                <td>$1,800</td>
                                <td>District 3 boutique villa / ground floor, 800 sqft</td>
                            </tr>
                            <tr>
                                <td>Payroll & Insurance</td>
                                <td>$4,800</td>
                                <td>4 headcount total, loaded with taxes/insurance</td>
                            </tr>
                            <tr>
                                <td>Consumables (Color, dyes, shampoos)</td>
                                <td>$1,200</td>
                                <td>Premium salon-grade styling product inventory</td>
                            </tr>
                            <tr>
                                <td>Utilities (Water/Power)</td>
                                <td>$700</td>
                                <td>Water heating, lighting & high AC runs</td>
                            </tr>
                            <tr>
                                <td>Marketing / Ads</td>
                                <td>$500</td>
                                <td>Instagram local ads & KOL influencer marketing</td>
                            </tr>
                            <tr>
                                <td>Software/POS/Misc</td>
                                <td>$400</td>
                                <td>Salon POS booking software, merchant fees, laundry</td>
                            </tr>
                            <tr class="highlight-row">
                                <td><strong>Total Base OPEX</strong></td>
                                <td><strong>$9,400</strong></td>
                                <td><em>OPEX target: $9,400</em></td>
                            </tr>
                        </tbody>"""

new_opex_tbody = """                        <tbody>
                            <tr>
                                <td>Rent</td>
                                <td>$2,000</td>
                                <td>District 1/3 ground-floor premium boutique space, 800 sqft</td>
                            </tr>
                            <tr>
                                <td>Payroll & Insurance</td>
                                <td>$5,400</td>
                                <td>4 headcount total, loaded with taxes/insurance</td>
                            </tr>
                            <tr>
                                <td>Consumables (Color, dyes, shampoos)</td>
                                <td>$1,500</td>
                                <td>European/Japanese imported styling & color products</td>
                            </tr>
                            <tr>
                                <td>Utilities (Water/Power)</td>
                                <td>$800</td>
                                <td>Water double-filtration maintenance, electricity & AC</td>
                            </tr>
                            <tr>
                                <td>Marketing / Ads</td>
                                <td>$600</td>
                                <td>Instagram campaigns & local expat targeting</td>
                            </tr>
                            <tr>
                                <td>Software/POS/Misc</td>
                                <td>$400</td>
                                <td>Salon POS booking, accounting, laundry, merchant fees</td>
                            </tr>
                            <tr class="highlight-row">
                                <td><strong>Total Base OPEX</strong></td>
                                <td><strong>$10,700</strong></td>
                                <td><em>OPEX target: $10,700</em></td>
                            </tr>
                        </tbody>"""

content = content.replace(old_opex_tbody, new_opex_tbody)

# 11. CAPEX Table/Grid
old_capex_grid = """                <div class="grid-stats capex-grid">
                    <div class="stat-box">
                        <span class="label">Boutique Renovation & Fitout</span>
                        <span class="value">$25,000</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Salon Equipment</span>
                        <span class="value">$15,000</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Lease Deposit (3 months)</span>
                        <span class="value">$5,400</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Plumbing & Electrical</span>
                        <span class="value">$8,000</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Tools & Initial Inventory</span>
                        <span class="value">$7,000</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Working Capital</span>
                        <span class="value">$9,600</span>
                    </div>
                </div>"""

new_capex_grid = """                <div class="grid-stats capex-grid">
                    <div class="stat-box">
                        <span class="label">Boutique Renovation & Fitout</span>
                        <span class="value">$40,000</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Salon Equipment</span>
                        <span class="value">$18,000</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Lease Deposit (3 months)</span>
                        <span class="value">$6,000</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Plumbing & Electrical</span>
                        <span class="value">$10,000</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Tools & Initial Inventory</span>
                        <span class="value">$8,000</span>
                    </div>
                    <div class="stat-box">
                        <span class="label">Working Capital</span>
                        <span class="value">$18,000</span>
                    </div>
                </div>"""

content = content.replace(old_capex_grid, new_capex_grid)

old_capex_conclusion = """                <div class="conclusion-box">
                    <strong>Total Estimate: USD 70,000</strong> (Range: USD 65k - 75k)<br>
                    <strong>Equipment Strategy:</strong> Procuring 4 high-quality styling stations and 2 luxury backstyling chairs with carbonated halo rinse systems. This layout optimizes space usage while keeping initial capex in check.
                </div>"""

new_capex_conclusion = """                <div class="conclusion-box">
                    <strong>Total Estimate: USD 100,000</strong> (Range: USD 90k - 110k)<br>
                    <strong>Equipment Strategy:</strong> Procuring 4 high-quality styling stations and 2 luxury backwash beds with double-filtration soft-water rinse systems. This layout optimizes space usage while keeping initial capex in check.
                </div>"""

content = content.replace(old_capex_conclusion, new_capex_conclusion)

# 12. Unit Economics
old_economics_text = """                    <ul>
                        <li><strong>Average Ticket:</strong> USD 85</li>
                        <li><strong>Contribution Margin per Ticket:</strong> USD 76.50</li>
                        <li><strong>Monthly Breakeven Volume:</strong> USD 9,400 (OPEX) / USD 76.50 = ~123 customers/month</li>
                        <li><strong>Daily Breakeven:</strong> ~4.1 customers per day (Across 4 styling stations)</li>
                    </ul>"""

new_economics_text = """                    <ul>
                        <li><strong>Average Ticket:</strong> USD 95</li>
                        <li><strong>Contribution Margin per Ticket:</strong> USD 85.50</li>
                        <li><strong>Monthly Breakeven Volume:</strong> USD 10,700 (OPEX) / USD 85.50 = ~125 customers/month</li>
                        <li><strong>Daily Breakeven:</strong> ~4.2 customers per day (Across 4 styling stations)</li>
                    </ul>"""

content = content.replace(old_economics_text, new_economics_text)

old_economics_tbody = """                        <tbody>
                            <tr>
                                <td>Breakeven</td>
                                <td>4.1</td>
                                <td>$10,455</td>
                                <td>$9,400</td>
                                <td style="color: #00e676;">+$10</td>
                            </tr>
                            <tr class="highlight-row">
                                <td>Base Case (17.3 Cust/Day)</td>
                                <td>17.3</td>
                                <td>$44,030</td>
                                <td>$9,400</td>
                                <td style="color: #00e676;">+$30,227</td>
                            </tr>
                            <tr>
                                <td>High Case (21.6 Cust/Day)</td>
                                <td>21.6</td>
                                <td>$55,080</td>
                                <td>$9,400</td>
                                <td style="color: #00e676;">+$40,172</td>
                            </tr>
                        </tbody>"""

new_economics_tbody = """                        <tbody>
                            <tr>
                                <td>Breakeven</td>
                                <td>4.2</td>
                                <td>$11,875</td>
                                <td>$10,700</td>
                                <td style="color: #00e676;">+$0</td>
                            </tr>
                            <tr class="highlight-row">
                                <td>Base Case (13.2 Cust/Day)</td>
                                <td>13.2</td>
                                <td>$37,715</td>
                                <td>$10,700</td>
                                <td style="color: #00e676;">+$23,244</td>
                            </tr>
                            <tr>
                                <td>High Case (16.5 Cust/Day)</td>
                                <td>16.5</td>
                                <td>$47,120</td>
                                <td>$10,700</td>
                                <td style="color: #00e676;">+$31,708</td>
                            </tr>
                        </tbody>"""

content = content.replace(old_economics_tbody, new_economics_tbody)

old_posttax = """                    <ul style="margin-top: 0.5rem; margin-left: 1.5rem; list-style-type: disc;">
                        <li><strong>Base Case Pre-Tax Monthly Net Profit:</strong> USD 30,227</li>
                        <li><strong>Estimated Monthly Corporate Income Tax:</strong> USD 6,045</li>
                        <li><strong>Post-Tax Net Monthly Profit (PAT):</strong> USD 24,182</li>
                        <li><strong>Post-Tax Profit to OPEX Ratio:</strong> <strong>257% (Post-Tax)</strong> (vs. 322% pre-tax)</li>
                        <li><strong>Post-Tax CAPEX Payback Period:</strong> <strong>3 Months</strong> (vs. 2.3 months pre-tax)</li>
                    </ul>"""

new_posttax = """                    <ul style="margin-top: 0.5rem; margin-left: 1.5rem; list-style-type: disc;">
                        <li><strong>Base Case Pre-Tax Monthly Net Profit:</strong> USD 23,244</li>
                        <li><strong>Estimated Monthly Corporate Income Tax:</strong> USD 4,649</li>
                        <li><strong>Post-Tax Net Monthly Profit (PAT):</strong> USD 18,595</li>
                        <li><strong>Post-Tax Profit to OPEX Ratio:</strong> <strong>174% (Post-Tax)</strong> (vs. 217% pre-tax)</li>
                        <li><strong>Post-Tax CAPEX Payback Period:</strong> <strong>5 Months</strong> (vs. 4.3 months pre-tax)</li>
                    </ul>"""

content = content.replace(old_posttax, new_posttax)

# 13. Timeline Weeks 5-8
old_timeline_fit = '<div class="content">Renovation, track lighting installation, and setup of 4 styling stations and 2 backstyling chairs.</div>'
new_timeline_fit = '<div class="content">Renovation, track lighting installation, and setup of 4 styling stations and 2 backwash beds.</div>'
content = content.replace(old_timeline_fit, new_timeline_fit)

# 14. Key Risks and Controls
old_risk_rent = '<td>Focus on side streets, villa spaces, or upper floors in D1/D3; rent must remain under USD 2,500/month.</td>'
new_risk_rent = '<td>Focus on side streets, villa spaces, or upper floors in D1/D3; rent must remain under USD 2,800/month.</td>'
content = content.replace(old_risk_rent, new_risk_rent)

# 15. Final Recommendation Success Box
old_rec_box = """                    <h3>Decision: GO (Expat Salon PoC)</h3>
                    <ul>
                        <li><strong>Location:</strong> District 3 (Vo Thi Sau St / Turtle Lake Area).</li>
                        <li><strong>Setup:</strong> 4 styling stations, 2 styling chairs, 800 sq ft boutique space.</li>
                        <li><strong>Budget:</strong> USD 70k CAPEX, USD 9.4k OPEX.</li>
                        <li><strong>Expansion Trigger:</strong> Once store hits USD 35k monthly revenue with 30%+ package conversions, begin planning a second branch in District 1 (Dong Khoi).</li>
                    </ul>"""

new_rec_box = """                    <h3>Decision: GO (Premium Salon MVP)</h3>
                    <ul>
                        <li><strong>Location:</strong> District 1/3 or Thao Dien (ground floor boutique).</li>
                        <li><strong>Setup:</strong> 4 styling stations, 2 backwash beds, 800 sq ft boutique space.</li>
                        <li><strong>Budget:</strong> USD 100k CAPEX, USD 10.7k OPEX.</li>
                        <li><strong>Expansion Trigger:</strong> Once store hits USD 45k monthly revenue with 30%+ package conversions, begin planning a second branch in District 1 (Dong Khoi) or Thao Dien.</li>
                    </ul>"""

content = content.replace(old_rec_box, new_rec_box)

# 16. Next Steps
old_next_step1 = '<li>Create equipment list for vanity/styling equipment ordering (4 stations, 2 backstyling chairs, Dyson dryers, steamers).</li>'
new_next_step1 = '<li>Create equipment list for vanity/styling equipment ordering (4 stations, 2 backwash beds, Dyson dryers, steamers).</li>'
content = content.replace(old_next_step1, new_next_step1)

old_next_step3 = '<li>Begin local viewing of 70-80 sqm villa or retail units in District 3/1 (rent target <$2,000/mo).</li>'
new_next_step3 = '<li>Begin local viewing of 70-80 sqm villa or retail units in District 3/1/Thao Dien (rent target <$2,500/mo).</li>'
content = content.replace(old_next_step3, new_next_step3)

# 17. Map Script Competitors
old_map_competitors = """        const competitors = [
            { name: "J-First Tokyo (Premium Japanese Salon)", lat: 10.774567, lng: 106.706176, price: "US$40-200", footfall: 65, comment: "Premium reputation, Japanese stylists, strong expat base. Located in D1." },
            { name: "Concept Coiffure (French Premium Salon)", lat: 10.775317, lng: 106.704251, price: "US$35-180", footfall: 55, comment: "Established expat clientele, western-style styling. Located in D3." },
            { name: "Vampire Hair Salon (Trendy Local Salon)", lat: 10.776530, lng: 106.698960, price: "US$25-120", footfall: 70, comment: "Popular on social media, excellent balayage. Loud, crowded open layout." }
        ];"""

new_map_competitors = """        const competitors = [
            { name: "J-First Tokyo (Premium Japanese Salon)", lat: 10.774567, lng: 106.706176, price: "US$40-200", footfall: 65, comment: "Premium Japanese stylists, high-quality coloring, expat base. Located in D1/D3." },
            { name: "Concept Coiffure (French Premium Salon)", lat: 10.775317, lng: 106.704251, price: "US$35-180", footfall: 55, comment: "French & Western styling, premium color. Located in Thao Dien (D2)." },
            { name: "Vamp Hair Line (Premium Japanese-Trained Salon)", lat: 10.776530, lng: 106.698960, price: "US$25-150", footfall: 70, comment: "Peek-A-Boo style training, strong color services. Loud, high-turnover environment. Located in D1." }
        ];"""

content = content.replace(old_map_competitors, new_map_competitors)

# 18. Map Script Candidates
# rent A: 1530 -> 1300, premiumTargetPct A: 36 -> 43.2, competitorCapacity A: 9000 -> 13500
# rent B: 1105 -> 939, premiumTargetPct B: 30 -> 36, competitorCapacity B: 6750 -> 10125
# rent C: 1870 -> 1590, premiumTargetPct C: 34 -> 40.8, competitorCapacity C: 9750 -> 14625
old_map_candidates = """        const candidates = [
            { 
                name: "Candidate A: Xuan Thuy St (Thao Dien)", 
                lat: 10.8048, 
                lng: 106.7360, 
                note: "Top choice. High street-level expat traffic, excellent visibility.", 
                rent: 1530,
                catchment: 40000,
                premiumTargetPct: 36, // 30% premium segment
                competitorCapacity: 9000,
                airportTime: "30 mins from SGN"
            },
            { 
                name: "Candidate B: Quoc Huong St (Thao Dien)", 
                lat: 10.8025, 
                lng: 106.7350, 
                note: "Near apartment towers & transit, quieter side road.", 
                rent: 1105,
                catchment: 30000,
                premiumTargetPct: 30, // 25% premium segment
                competitorCapacity: 6750,
                airportTime: "32 mins from SGN"
            },
            { 
                name: "Candidate C: Le Thanh Ton Alley (D1)", 
                lat: 10.7785, 
                lng: 106.7055, 
                note: "Heart of Japan Town. High premium density, small space.", 
                rent: 1870,
                catchment: 25000,
                premiumTargetPct: 34, // 28% premium segment
                competitorCapacity: 9750,
                airportTime: "25 mins from SGN"
            }
        ];"""

new_map_candidates = """        const candidates = [
            { 
                name: "Candidate A: Xuan Thuy St (Thao Dien)", 
                lat: 10.8048, 
                lng: 106.7360, 
                note: "Top choice. High street-level expat traffic, excellent visibility.", 
                rent: 1300,
                catchment: 40000,
                premiumTargetPct: 43.2,
                competitorCapacity: 13500,
                airportTime: "30 mins from SGN"
            },
            { 
                name: "Candidate B: Quoc Huong St (Thao Dien)", 
                lat: 10.8025, 
                lng: 106.7350, 
                note: "Near apartment towers & transit, quieter side road.", 
                rent: 939,
                catchment: 30000,
                premiumTargetPct: 36,
                competitorCapacity: 10125,
                airportTime: "32 mins from SGN"
            },
            { 
                name: "Candidate C: Le Thanh Ton Alley (D1)", 
                lat: 10.7785, 
                lng: 106.7055, 
                note: "Heart of Japan Town. High premium density, small space.", 
                rent: 1590,
                catchment: 25000,
                premiumTargetPct: 40.8,
                competitorCapacity: 14625,
                airportTime: "25 mins from SGN"
            }
        ];"""

content = content.replace(old_map_candidates, new_map_candidates)

# Write updated hcmc.html
with open('hcmc.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HCMC HTML Updated successfully!")
