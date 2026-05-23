with open('binhduong.html', 'r', encoding='utf-8') as f:
    content = f.read()

blocks = {}

blocks["loc_table"] = """                             <tr class="highlight-row">
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

blocks["conclusion_box"] = """                <div class="conclusion-box">
                    <strong>Strategy:</strong> Lease an 800 sq ft ground-floor commercial unit in Thuan An near Aeon Mall/VSIP 1 to target the main expat traffic. Target rent: USD 795/month.
                </div>"""

blocks["competitors"] = """                             <tr>
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

blocks["menu_packages"] = """            <!-- 8. Product / Service Menu -->
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

blocks["journey_layout"] = """            <!-- 10. Customer Journey -->
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

blocks["opex_capex"] = """            <!-- 13. Monthly OPEX -->
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

blocks["economics_timeline"] = """            <!-- 15. Unit Economics -->
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

blocks["recommendation"] = """            <!-- 19. Recommendation -->
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

blocks["competitors_js"] = """        // Competitors
        const competitors = [
            { name: "Toto Hair Studio", price: "US$12-60", footfall: 75, lat: 10.9754, lng: 106.6660, comment: "Trendy Chanh Nghia hair salon. Good modern styling and recovery services, but noisy open floor layout." },
            { name: "Hair Salon Mr. D", price: "US$15-75", footfall: 70, lat: 10.9702, lng: 106.6610, comment: "Luxury hair styling salon. Good chemical services (perm/dye) but lacks private styling stations and scalp therapy." },
            { name: "Trendy Hair", price: "US$18-90", footfall: 65, lat: 10.9730, lng: 106.6690, comment: "High-end salon with advanced styling services. Expensive, situated in busy residential area with limited parking." }
        ];"""

blocks["candidates_js"] = """        // Shop Candidates
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

for name, block in blocks.items():
    # normalize CRLF / LF to test
    block_norm = block.replace('\r\n', '\n').strip()
    content_norm = content.replace('\r\n', '\n')
    if block_norm in content_norm:
        print(f"[{name}] Found!")
    else:
        print(f"[{name}] NOT found!")
        # Print a short slice of the start of the block to see what it looks like
        start = block.split('\n')[0][:50]
        print(f"   Searching for: {repr(start)}")
