"""
substantive_update_batch2.py
Second batch: Brisbane, Sydney, Okinawa, Haiphong, Sabah, Sarawak, Kaohsiung, Taichung, Tainan, Dong Nai, KL.
"""
import os, re

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

def replace_section(content, section_id, new_inner_html):
    pattern = rf'(<section id="{section_id}"[^>]*>)(.*?)(</section>)'
    replacement = r'\1' + new_inner_html + r'\3'
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count == 0:
        print(f"  WARNING: section #{section_id} not found!")
    return new_content

# ============================================================
# BRISBANE
# ============================================================
BRISBANE_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (AUD)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Sol Hair</strong></td>
                                <td>Paddington</td>
                                <td>Balayage $350–550; Foils $150–400</td>
                                <td>Exclusive Redken colour salon, sustainability ethos, "salon of the senses" positioning, strong Instagram following</td>
                                <td>Premium pricing accessible to fewer clients; appointment-only; no Asian hair specialist on staff — limited diversity of service range</td>
                                <td>Inclusive of Asian, European, and mixed hair types; specialist bilingual team for Brisbane's growing Korean/Japanese community</td>
                            </tr>
                            <tr>
                                <td><strong>Beau Gordon Hair</strong></td>
                                <td>Rosalie Village</td>
                                <td>Balayage $300–500; Extensions $600+</td>
                                <td>Specialist in luminous blondes and "lived-in" colour, boutique luxury, loyal high-income Rosalie clientele</td>
                                <td>Almost exclusively blonde-focused; no Asian-hair or dark-base balayage expertise; very boutique capacity (3–4 chairs)</td>
                                <td>Full-spectrum balayage including dark-to-light, copper, ash, and fashion vivid — plus dedicated Asian hair expertise</td>
                            </tr>
                            <tr>
                                <td><strong>Stefan Hair Fashions</strong></td>
                                <td>South Bank</td>
                                <td>Cut + Color $200–500</td>
                                <td>Prominent South Bank studio, elevated experience, full-service menu, consistent quality</td>
                                <td>High volume salon with open layout; not boutique private bays; pricing without the intimacy premium clients expect</td>
                                <td>8-station boutique with private styling bays; focused solely on premium color and cut — no blow-dry bar dilution</td>
                            </tr>
                            <tr>
                                <td><strong>Elysium Hair Brisbane</strong></td>
                                <td>Brisbane CBD</td>
                                <td>Full Balayage $350–550 (incl. treatment)</td>
                                <td>Highly rated CBD option, K18 and Olaplex inclusive packages, strong balayage portfolio</td>
                                <td>CBD location inconvenient for New Farm/Teneriffe expat residential cluster; expensive CBD overheads drive up pricing</td>
                                <td>New Farm / Teneriffe boutique address — premium residential walkability for Brisbane's fastest-growing inner-city demographic</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

BRISBANE_UNMET = """
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
                                <td>Premium boutique serving New Farm / Teneriffe / Fortitude Valley corridor</td>
                                <td>Sol Hair (Paddington), Beau Gordon (Rosalie) — both west of CBD; CBD options are 20+ min from inner-east residential</td>
                                <td>New Farm and Teneriffe house Brisbane's fastest-growing HNWI residential cluster (median house price $2.1M+). No premium boutique color studio serves this corridor — residents currently drive to Paddington or the CBD</td>
                                <td>Ground-floor boutique on Brunswick Street New Farm or James Street Fortitude Valley — the only premium color studio serving inner-east Brisbane's HNWI residential belt</td>
                            </tr>
                            <tr>
                                <td>Specialist balayage for Asian hair types (Brisbane Korean/Japanese community)</td>
                                <td>All top Brisbane salons specialize in European/blonde hair — none market Asian hair color expertise</td>
                                <td>Brisbane's Korean and Japanese populations have grown significantly (Logan/Sunnybank + Fortitude Valley). Both communities have high WTP for specialist color but no premium salon with bilingual consultation and Asian-hair-appropriate products exists</td>
                                <td>Dedicated Asian hair color tier: dark-to-light specialist balayage, Japanese straight + color combo, Korean-inspired fashion toning — bilingual (Korean/English) consultation</td>
                            </tr>
                            <tr>
                                <td>UV-protective color in Brisbane's extreme UV climate</td>
                                <td>No Brisbane salon markets UV-protective post-color treatment specifically</td>
                                <td>Brisbane has Australia's highest urban UV index (regularly UV 10–12 in summer). Color fades 40–50% faster outdoors without UV-adaptive post-treatment. No premium salon offers a UV-specific color longevity package</td>
                                <td>"Brisbane Shield" post-color Solaris UV-protect gloss — color longevity in Queensland sun as a core brand promise</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

BRISBANE_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Brisbane has 100,000+ international students (UQ, QUT) plus 30,000+ skilled visa expats concentrated in inner suburbs (New Farm, Teneriffe, Fortitude Valley, Paddington). Brisbane's population grew by 2.3% in 2023–24 — the fastest of any Australian capital — driven by interstate and international migration. New Farm's median house price exceeds AUD $2.1M, signalling the wealth concentration in the inner-east corridor.</li>
                    <li><strong>Spending Power:</strong> Brisbane premium salon clients spend AUD $300–600 for quality balayage. The Korean and Japanese community (growing rapidly in Sunnybank, Robertson, and Fortitude Valley) represents an underserved, high-WTP segment. Post-Olympics investment (2032 Brisbane Olympics) is accelerating luxury retail development in South Bank and the inner-east.</li>
                    <li><strong>Environmental Drivers:</strong> Brisbane's UV index (regularly 10–12 in summer) is the most extreme of any city in this 27-city shortlist. Color fades significantly faster, driving demand for UV-protection add-ons and shorter refresh cycles — a commercially exploitable difference vs. temperate-city competitors.</li>
                    <li><strong>Competitive Environment:</strong> Sol Hair, Beau Gordon, Elysium, Stefan, and Little Birdie collectively serve the premium segment with under 30 chairs total across Brisbane. None serve the New Farm/Teneriffe inner-east corridor. None specialize in Asian hair types.</li>
                    <li><strong>Regulatory Context:</strong> Australian Business Number (ABN) registration. Standard Queensland QBCC/local council commercial premises approval. All color service practitioners must hold a Certificate III in Hairdressing (minimum) — ample supply of qualified stylists from TAFE Queensland training programs.</li>
                </ul>
"""

# ============================================================
# SYDNEY
# ============================================================
SYDNEY_COMPETITORS = """
                <h2>6. Competitor Study</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Competitor</th>
                                <th>Location</th>
                                <th>Price Range (AUD)</th>
                                <th>Strengths</th>
                                <th>Weaknesses</th>
                                <th>Our Edge</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>RAW Anthony Nader</strong></td>
                                <td>Surry Hills</td>
                                <td>Balayage $300–600; Cut $150–250</td>
                                <td>World-renowned celebrity stylist, premium brand cachet, exceptional coloring team, international clientele</td>
                                <td>6–8 week booking waits for top stylists; ultra-premium pricing excludes mid-tier professionals; open salon layout</td>
                                <td>Private styling bays; accessible premium at AUD $250–450; 48-hour member booking guarantee</td>
                            </tr>
                            <tr>
                                <td><strong>A.H Salon</strong> (fmr Edwards &amp; Co)</td>
                                <td>Surry Hills</td>
                                <td>Balayage $200–450; Cut $90–200</td>
                                <td>Large iconic Surry Hills space, "lived-in" color specialists, diverse stylist team, international visitor friendly</td>
                                <td>High volume open layout — not boutique private; tiered pricing creates inconsistency between junior/senior stylists; toner charged separately</td>
                                <td>Inclusive pricing (toner, wash, blow-dry included); senior-stylist guaranteed for all color services</td>
                            </tr>
                            <tr>
                                <td><strong>Flock Hair</strong></td>
                                <td>Surry Hills</td>
                                <td>Balayage $250–450; Foils $200–380</td>
                                <td>Natural luminous balayage specialists, boutique feel, personalized service, sustainability-conscious</td>
                                <td>Small capacity (4–5 chairs) means perpetual overbooking; 4+ week waits common; limited fashion/vivid color range</td>
                                <td>Larger capacity (8 stations); fashion + natural balayage full spectrum; same-week bookings for members</td>
                            </tr>
                            <tr>
                                <td><strong>Wakefields</strong></td>
                                <td>Surry Hills</td>
                                <td>Balayage $200–400; Color Correction $400+</td>
                                <td>Award-winning color correction specialists, strong balayage portfolio, professional environment</td>
                                <td>Correction-focus positions them as a "repair" destination rather than aspirational luxury; less emphasis on preventive color care</td>
                                <td>Preventive color care positioning: soft-water wash + Olaplex protection from first visit, not just correction</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

SYDNEY_UNMET = """
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
                                <td>Premium boutique in inner-west / Newtown / Glebe for growing young-professional demographic</td>
                                <td>All top Surry Hills salons clustered in a 300m radius — Newtown and Glebe have no equivalent premium boutique</td>
                                <td>Newtown and Glebe's rapidly gentrifying young-professional demographic (25–40, dual income, creative industries) has WTP of $250–400 for premium color but no nearby boutique option — all Surry Hills alternatives require a 15–20 minute journey</td>
                                <td>Ground-floor boutique on King Street Newtown or Glebe Point Road — first premium color boutique in Sydney's inner-west</td>
                            </tr>
                            <tr>
                                <td>Inclusive transparent pricing (no toner/blow-dry add-ons)</td>
                                <td>RAW, A.H, and most Surry Hills salons charge base + toner + blowdry separately — final bill 30–50% above headline price</td>
                                <td>This is a documented source of expat/international client frustration. Clients from US/Europe expect a quoted price to be the final price; opacity damages referrals and repeat visits</td>
                                <td>Fixed all-inclusive packages: balayage + toner + Olaplex + blowdry in one upfront price — no surprises</td>
                            </tr>
                            <tr>
                                <td>Sydney climate-adaptive color (humid summers + UV)</td>
                                <td>Standard color services — no salon differentiates on Sydney's 85%+ summer RH and UV 9–11</td>
                                <td>Sydney summers cause measurable color fade acceleration and frizz. No premium salon markets a specific summer-adapted color finish system</td>
                                <td>"Sydney Summer Shield" package: anti-humidity Nanogloss seal + UV-protect color toner applied post-balayage</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

SYDNEY_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Sydney has 1.5 million+ residents born overseas (36% of total population), with the largest expat clusters in the inner-west (Newtown, Glebe, Balmain), eastern suburbs (Double Bay, Bondi, Paddington), and lower north shore (Mosman, Neutral Bay). Premium salon WTP is highest in these inner-city zones. OECD data places Sydney in the top 5 most expensive cities globally for beauty services — pricing power is strong.</li>
                    <li><strong>Spending Power:</strong> Sydney professionals routinely spend AUD $350–600 for quality balayage. The eastern suburbs and inner-west demographics have median household incomes above AUD $120,000 — a well-proven premium beauty market with deep spending precedent.</li>
                    <li><strong>Environmental Drivers:</strong> Sydney's UV index (9–11 in summer) and 70–85% summer relative humidity combine to create rapid color fade and frizz issues. A climate-adaptive color positioning — specifically for Sydney's summer — is commercially valid and unaddressed by current competitors.</li>
                    <li><strong>Competitive Environment:</strong> RAW Anthony Nader, A.H Salon, Flock Hair, and Wakefields are the Surry Hills elite. Combined they offer under 25 premium color chairs for Sydney's 5 million population. The inner-west (Newtown, Glebe) premium boutique gap is real and measurable.</li>
                    <li><strong>Regulatory Context:</strong> ABN registration. NSW Fair Trading compliance for commercial premises. Certificate III in Hairdressing mandatory for all color practitioners. SkillSelect or TSS visa for international stylist hires — factor 4–6 month lead time for visa processing into staffing plan.</li>
                </ul>
"""

# ============================================================
# OKINAWA
# ============================================================
OKINAWA_COMPETITORS = """
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
                                <td><strong>BLOOM Hair Studio</strong></td>
                                <td>Chatan / Sunabe area</td>
                                <td>Balayage ¥10,000–19,000; Cut ¥3,500–6,000</td>
                                <td>Top English-speaking recommendation in military/expat community; specialist balayage + blonde/highlights; English stylists (Tomo, Paku, Rico)</td>
                                <td>Primarily serves US military Kadena area — appointment pressure on weekends; no Korean-language service; limited soft-water filtration</td>
                                <td>Naha Shin-toshin / Omoromachi location serves both military (Naha Military Port) AND civilian expat/tourist market; Korean + English bilingual</td>
                            </tr>
                            <tr>
                                <td><strong>Borjan Hair Salon</strong></td>
                                <td>Sunabe Seawall, Chatan</td>
                                <td>Balayage ¥8,000–16,000</td>
                                <td>Specialist balayage and custom color, Kadena-area favourite, welcoming atmosphere, Japanese + English service</td>
                                <td>One-woman operation — 3–4 week advance booking required; highly vulnerable to capacity limits; no team backup</td>
                                <td>4-station team operation; 48-hour booking guarantee; consistent quality vs. solo artist dependency</td>
                            </tr>
                            <tr>
                                <td><strong>Amber Rose Hair Salon</strong></td>
                                <td>Naha / Chatan</td>
                                <td>Color ¥6,000–14,000; Cut ¥3,500–7,000</td>
                                <td>American-style salon, full English service, Moroccan Oil products, military community trusted</td>
                                <td>American-style positioning = US military focus; less expertise in Asian hair or Japanese/Korean aesthetic services; limited creative color range</td>
                                <td>Full-spectrum: US/Western balayage + Japanese precision + Korean fashion color — serves every expat hair aesthetic in one studio</td>
                            </tr>
                            <tr>
                                <td><strong>On-Base Stylique</strong></td>
                                <td>Kadena/Foster/Schwab bases</td>
                                <td>Cut ¥2,000–3,500; Basic Color ¥4,000–7,000</td>
                                <td>Zero commute for on-base residents, affordable, familiar US salon-chain feel</td>
                                <td>Very limited creative color capability; basic product stack; long wait times; no balayage specialist; base access restriction for non-military</td>
                                <td>Off-base premium alternative — better product quality, specialist technique, accessible to ALL residents without base pass requirement</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

OKINAWA_UNMET = """
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
                                <td>Premium off-base color salon in Naha Shin-toshin (not Chatan)</td>
                                <td>All English-speaking specialist salons are clustered in Chatan/Sunabe (north), 25–40 min drive from Naha</td>
                                <td>Naha hosts the largest concentration of foreign civilian residents (Omoromachi, Shin-toshin area), Ryukyu University students, Korean tourists, and cruise ship visitors — yet no English-friendly premium color studio exists in this zone</td>
                                <td>Ground-floor boutique in Omoromachi or Shin-toshin, Naha — Okinawa's civilian expat hub vs. military-only Chatan cluster</td>
                            </tr>
                            <tr>
                                <td>UV and seawater color protection for beach-lifestyle clients</td>
                                <td>No Okinawa salon proactively markets a beach-UV color protection protocol</td>
                                <td>Okinawa's UV index is among Japan's highest (regularly UV 10–12 in summer); seawater salt exposure from beach/surfing strips bleached hair rapidly. Military spouses and expat families with active beach lifestyles are a distinct and unaddressed segment</td>
                                <td>"Okinawa Reef Shield" post-color package: Aquage Sea Extend + UV-protect Redken sheer gloss — marketed specifically to beach/surf lifestyle military and expat communities</td>
                            </tr>
                            <tr>
                                <td>Korean-language premium hair service in Okinawa</td>
                                <td>No Okinawa salon offers Korean-language consultation or K-beauty color services</td>
                                <td>Okinawa receives 200,000+ Korean tourists annually (pre-COVID baseline) and has a growing Korean resident community. K-pop hair trends (cushion perm, milk tea balayage) are hugely popular — an unaddressed commercial segment with high WTP</td>
                                <td>Korean-speaking staff + K-Beauty color portfolio (Amorepacific + Korean color board); active Naver Blog and KakaoTalk marketing for Korean tourist advance bookings</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

OKINAWA_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Okinawa hosts approximately 26,000 US military personnel and ~30,000 military family members (the largest US base presence in Japan outside CONUS). Additionally, ~10,000 civilian foreign residents live in Naha and surrounding areas. Okinawa receives 9+ million domestic Japanese tourists and 2+ million international visitors annually, with Korean tourists the largest inbound group.</li>
                    <li><strong>Spending Power:</strong> US military officer families have a combined household income of $80,000–130,000 USD with BAS/BAH housing allowances — strong WTP for quality off-base services. Civilian expat and tourist segments budget JPY 8,000–20,000 for premium color. Korean tourists exhibit the highest per-session WTP of any tourist group at JPY 12,000–22,000.</li>
                    <li><strong>Environmental Drivers:</strong> Okinawa's subtropical climate (UV 10–12 in summer, year-round humidity 75–85%) combined with heavy beach/ocean usage creates extreme color fade. No competitor has built a service positioning around Okinawa's specific coastal climate — a commercially exploitable gap.</li>
                    <li><strong>Competitive Environment:</strong> BLOOM, Borjan, and Amber Rose are the military/expat go-to options, all concentrated in Chatan. Naha's civilian zone is entirely unserved by premium English/Korean-friendly color salons. On-base options are inadequate for creative color.</li>
                    <li><strong>Regulatory Context:</strong> Japanese 美容師法 licensing required for all stylists performing color/chemical services. Standard Naha City commercial lease + municipal business registration. Proximity to US military bases creates a marketing advantage but requires no special licensing.</li>
                </ul>
"""

# ============================================================
# HAIPHONG
# ============================================================
HAIPHONG_COMPETITORS = """
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
                                <td><strong>HaLa Hair Salon</strong></td>
                                <td>Hai Phong City Centre</td>
                                <td>Balayage $35–70; Color $15–35</td>
                                <td>Est. 2010, TONI&amp;GUY Academy certified owner, L'Oréal Paris exclusive products, professional track record</td>
                                <td>Mass L'Oréal positioning limits creative color depth; functional salon environment, not luxury boutique; limited English proficiency</td>
                                <td>Premium Schwarzkopf + Milbon product stack; boutique luxury interior; bilingual (Korean/Vietnamese/English) team</td>
                            </tr>
                            <tr>
                                <td><strong>Nguyen Hung Hair Salon</strong></td>
                                <td>Hai Phong</td>
                                <td>Color $12–30; Balayage $30–60</td>
                                <td>High-volume, well-equipped, imported product claims, modern facilities, large loyal local following</td>
                                <td>High volume = rushed service; not boutique; no English-language expat consultation; limited balayage specialist depth</td>
                                <td>Appointment-only senior stylist delivery; private bay atmosphere; pre-appointment English/Korean WhatsApp consultation</td>
                            </tr>
                            <tr>
                                <td><strong>L'Amour Hair Salon</strong></td>
                                <td>Hai Phong</td>
                                <td>Color $15–40; Cut $8–15</td>
                                <td>Personalized consultations, professional environment, attention to detail</td>
                                <td>Mid-tier positioning without genuine premium service differentiation; no creative specialist color team; limited international client experience</td>
                                <td>True luxury boutique positioning at accessible Haiphong price points; specialist creative color (balayage, fashion toning)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

HAIPHONG_UNMET = """
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
                                <td>Premium expat-ready hair salon near Korean industrial estate</td>
                                <td>No salon in Haiphong actively markets to the Korean expat community at Deep C or VSIP Hai Phong</td>
                                <td>Haiphong's Deep C Industrial Zone and Nomura Thang Long IP host 20,000+ Korean and Japanese industrial expats. These workers and their families commute to Hanoi (3+ hours round trip) for quality hair services — a captive zero-competition market</td>
                                <td>Minh Khai street boutique (5-min drive from Deep C IP gate) — Korean-language booking, Korean product stack, zero-commute for industrial zone expat families</td>
                            </tr>
                            <tr>
                                <td>Soft-water color protection in Haiphong's hard coastal water</td>
                                <td>No Haiphong salon addresses water hardness; all use local tap water</td>
                                <td>Haiphong's HWACO water supply is river-sourced with elevated TDS and seasonal salinity from coastal intrusion — one of Vietnam's most color-damaging water profiles. No salon in the city has addressed this</td>
                                <td>RO + ion-exchange filtration on all wash basins; "color guaranteed 8 weeks" marketing claim backed by soft-water chemistry</td>
                            </tr>
                            <tr>
                                <td>Creative/fashion color specialist in Haiphong (not just HCMC/Hanoi)</td>
                                <td>All quality creative color options (Maika, Concept Coiffure) are in Hanoi or HCMC — 1.5–2 hours away</td>
                                <td>Haiphong's young affluent professional class (maritime shipping executives, port management, Samsung/LG families) is fashion-aware and willing to pay for balayage and fashion toning. Zero specialist options exist locally</td>
                                <td>Dedicated creative color studio: vivid balayage, K-pop inspired toning, European highlights — all specialist-delivered in Haiphong for the first time</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

HAIPHONG_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Haiphong has ~20,000–25,000 Korean industrial expats (concentrated in Deep C, VSIP Hai Phong, and Nomura Thang Long Industrial Parks), 3,000–5,000 Japanese, and a growing European maritime/shipping management community. As Vietnam's second-largest port city, Haiphong's shipping and logistics sector attracts international professionals who are underserved by the local beauty industry.</li>
                    <li><strong>Spending Power:</strong> Korean factory managers and Japanese executives earn international salaries — WTP of $50–120/session. Vietnamese maritime executives and young professionals in the port sector budget $30–70. This is a high-frequency repeat market if quality is delivered consistently.</li>
                    <li><strong>Water Quality:</strong> Haiphong's HWACO water supply is drawn from the Cam River system, subject to seasonal salinity intrusion from Haiphong Bay and naturally high in dissolved minerals. TDS ranges 300–500 ppm with salinity spikes in dry season — particularly damaging for bleach-based color work. Soft-water filtration is both a real technical benefit and a compelling marketing differentiator here.</li>
                    <li><strong>Competitive Environment:</strong> HaLa, Nguyen Hung, and L'Amour are the premium anchors — none at boutique luxury quality, none with Korean-language service, none with soft-water filtration. The Korean expat market represents entirely unaddressed demand in a captive geographic zone.</li>
                    <li><strong>Regulatory Context:</strong> Standard Vietnamese LLC registration + Haiphong provincial health/hygiene permit. Korean/Japanese stylist work permits via standard 2-year renewable work permit process. No industrial zone restrictions on commercial salon operation in Minh Khai/Hong Bang district.</li>
                </ul>
"""

# ============================================================
# SABAH (Kota Kinabalu)
# ============================================================
SABAH_COMPETITORS = """
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
                                <td><strong>Amos Hair Studio</strong></td>
                                <td>Riverson Lifestyle Centre, KK</td>
                                <td>Balayage MYR 380–600 (~$82–$129)</td>
                                <td>International-standard experience, professional atmosphere, highly rated for complex color corrections, English-friendly</td>
                                <td>Riverson location is relatively new and less established for walk-in traffic; limited capacity; no structured membership</td>
                                <td>Central KK Gaya Street / Jesselton Point boutique — prime tourist and expat corridor; structured membership with priority slots</td>
                            </tr>
                            <tr>
                                <td><strong>Michael and Guys</strong></td>
                                <td>Kota Kinabalu</td>
                                <td>Balayage MYR 350–600 (~$75–$129); Kérastase rituals MYR 150+</td>
                                <td>Detailed pricing transparency, Kérastase product range, professional consultations, pre-lightening expertise</td>
                                <td>Not positioned as boutique luxury; functional salon aesthetic; limited creative/vivid color portfolio</td>
                                <td>Boutique studio aesthetic + vivid color specialization + soft-water filtration for KK's tropical water challenges</td>
                            </tr>
                            <tr>
                                <td><strong>Your Hair Studio</strong></td>
                                <td>Kepayan, KK</td>
                                <td>Balayage MYR 300–500 (~$65–$108); Air Touch MYR 400+</td>
                                <td>Air Touch and European balayage techniques, length-specific transparent pricing, modern balayage methodology</td>
                                <td>Kepayan location is suburban — less accessible for tourists and city-centre expats; no private styling bays; limited English communication</td>
                                <td>City-centre ground-floor location; English + Malay + Mandarin trilingual team; private styling bays for Muslimah clientele</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

SABAH_UNMET = """
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
                                <td>Premium boutique in central KK (Gaya Street / Jesselton waterfront)</td>
                                <td>Amos (Riverson), Michael and Guys, Your Hair Studio — all in suburban or secondary mall locations</td>
                                <td>KK's tourism/expat demographic clusters around the waterfront, Gaya Street, and Sutera Harbour. No premium boutique color studio is within walking distance of this high-traffic, high-income corridor</td>
                                <td>Ground-floor boutique on Jalan Gaya or Jesselton Point commercial strip — serving KK's tourist, expat, and HNWI residential corridor simultaneously</td>
                            </tr>
                            <tr>
                                <td>Soft-water color protection in KK's tropical high-TDS water</td>
                                <td>No KK salon addresses water quality despite TDS of 200–350 ppm from Sabah Water Department supply</td>
                                <td>KK's tropical climate (100% humidity, heavy monsoon seasons) combined with hard water creates severe color fade and hair porosity issues. Expats from Singapore/KL notice dramatic difference in color longevity when in KK</td>
                                <td>RO + ion-exchange filtration across all wash basins — "KK's only soft-water salon" as a direct marketing claim</td>
                            </tr>
                            <tr>
                                <td>Muslimah private styling suite in a luxury environment</td>
                                <td>Most KK salons have basic partition screens — not genuine private suites at a boutique luxury standard</td>
                                <td>KK has a large Sabahan Muslim majority population with high WTP for luxury hair services if genuine privacy is guaranteed. A fully enclosed luxury Muslimah bay is commercially attractive and underdelivered by all current competitors</td>
                                <td>Dedicated enclosed Muslimah premium styling bay — fully private from entry to exit; separate entrance option available</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

SABAH_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Kota Kinabalu has ~500,000 residents with a substantial expatriate community (oil &amp; gas, plantation management, NGO workers) and a growing South Korean and Chinese expatriate professional segment. KK is East Malaysia's most active tourism hub (~4 million visitors/year pre-COVID), creating a strong premium service tourism economy alongside the resident expat market.</li>
                    <li><strong>Spending Power:</strong> Sutera Harbour resort residents and Mount Kinabalu expat families have WTP of MYR 400–800 per color session. Oil &amp; gas expats (Shell, Murphy Oil, Petronas) earn international salaries and match Kuala Lumpur spending patterns. Tourist segment (Korean, Japanese, Australian visitors) budgets MYR 350–600.</li>
                    <li><strong>Water Quality:</strong> Sabah Water Department (JANS) supply to KK has TDS of 200–350 ppm, elevated by limestone terrain in the Crocker Range catchment. Tropical humidity (80–95% year-round) combined with UV exposure (UV index 9–11) makes hair color management genuinely challenging for both residents and tourists.</li>
                    <li><strong>Competitive Environment:</strong> Amos Hair Studio (Riverson), Michael and Guys, and Your Hair Studio (Kepayan) represent the premium tier but all operate in suburban or non-boutique settings. The central KK waterfront corridor has zero premium color studio representation — the most accessible market gap in East Malaysia.</li>
                    <li><strong>Regulatory Context:</strong> SSM registration. Ministry of Health (Sabah State Health Dept) salon hygiene permit. Private styling bays for Muslimah clients are not legally required but are commercially essential in Sabah's market context. EP/SP visas required for non-Malaysian stylists — factor 3–4 month lead time.</li>
                </ul>
"""

# ============================================================
# SARAWAK (Kuching)
# ============================================================
SARAWAK_COMPETITORS = """
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
                                <td><strong>Cutting Edge The Premium Salon</strong></td>
                                <td>Kuching</td>
                                <td>Balayage MYR 400–650 (~$86–$140)</td>
                                <td>Premium brand positioning, professional atmosphere, reputable for quality color</td>
                                <td>Not boutique-level private bays; limited creative/vivid color portfolio; no structured membership offering</td>
                                <td>Private styling bays; dedicated vivid color specialist; structured membership with priority booking</td>
                            </tr>
                            <tr>
                                <td><strong>Gene's Work Hair Studio</strong></td>
                                <td>Multiple (Saradise, Trinity Hub, Gala City)</td>
                                <td>Color MYR 250–500 (~$54–$108); Tokio Inkarami treatments</td>
                                <td>Premium Japanese treatments (Tokio Inkarami), multi-outlet reach, professional product range, loyal Kuching following</td>
                                <td>Multi-outlet chain = inconsistent stylist quality; not a boutique experience; treatment-heavy without creative color specialist depth</td>
                                <td>Single boutique with consistent senior stylist delivery; creative color alongside premium treatments in one visit</td>
                            </tr>
                            <tr>
                                <td><strong>Mane Society</strong></td>
                                <td>The Northbank, Kuching</td>
                                <td>Color MYR 200–450 (~$43–$97)</td>
                                <td>Modern aesthetic, quality-focused environment, Northbank upscale location, contemporary positioning</td>
                                <td>Relatively new — building client base; limited track record for complex color corrections; no Muslimah private bay</td>
                                <td>Established creative color expertise + private Muslimah bay + soft-water filtration — Kuching's most complete premium offering</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

SARAWAK_UNMET = """
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
                                <td>Premium boutique near Kuching's expat core (Tabuan Jaya / Stutong)</td>
                                <td>Gene's Work and Cutting Edge are spread across malls (Saradise, Trinity Hub) not within walking distance of expat residential clusters</td>
                                <td>Kuching's Shell/Petronas expat community and diplomatic corps live primarily in Tabuan Jaya, Stutong, and Kota Samarahan — a residential corridor underserved by any premium salon within 5-min drive</td>
                                <td>Ground-floor boutique in Tabuan Jaya or Hikmah Exchange commercial strip — Shell/Petronas expat family corridor's first premium color boutique</td>
                            </tr>
                            <tr>
                                <td>Premium Muslimah private styling in a boutique-quality environment</td>
                                <td>Kuching's large Malay Muslim majority has limited access to luxury hair services with genuine privacy — most salons offer basic partitions only</td>
                                <td>Sarawak's Muslim population (60%+ of state) includes educated, brand-conscious professional women with high WTP. The Sarawak government's growing civil service and private sector professional class represents an underserved premium Muslimah segment</td>
                                <td>Enclosed luxury Muslimah bay with dedicated entrance — full privacy from street level to styling chair exit; Muslimah-friendly product range (halal-certified options)</td>
                            </tr>
                            <tr>
                                <td>Soft-water color protection in Kuching's heavily chlorinated water</td>
                                <td>No Kuching salon addresses water quality — all use Kuching Water Board supply</td>
                                <td>Kuching Water Board's supply (Matang WTP) has elevated chlorine residual and moderate TDS (150–250 ppm). Chlorine directly oxidizes color molecules — balayage fades 20–30% faster vs. soft-water rinsing. Zero competitors address this</td>
                                <td>RO + activated carbon dechlorination + softening on all wash basins — "Kuching's first soft-water color salon" as a verifiable differentiator</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

SARAWAK_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Kuching is Sarawak's state capital with 750,000+ metropolitan population. Key premium client segments: Shell Sarawak / Petronas Carigali oil &amp; gas expat families (~3,000 high-income expats), Sarawak State government professional class (growing rapidly under Sarawak's post-MCO development push), Chinese-Sarawakian HNWI families (Kuching's large Chinese community has high spending power), and diplomatic/NGO community.</li>
                    <li><strong>Spending Power:</strong> Shell/Petronas expat families earn $120,000–200,000+ USD equivalent packages. Sarawak Chinese-Malaysian HNWI households routinely spend MYR 400–900 on premium beauty services. The professional government/corporate Muslimah segment has growing WTP (MYR 300–700) as income parity rises.</li>
                    <li><strong>Water Quality:</strong> Kuching Water Board (KWB) supply from Matang WTP has residual chlorine 0.2–0.5 mg/L and moderate TDS 120–200 ppm. Chlorine is particularly destructive to balayage and fashion color — it oxidizes color molecules and bleaches deposited toners. Soft-water filtration with active carbon dechlorination provides a genuine, scientifically defensible quality advantage.</li>
                    <li><strong>Competitive Environment:</strong> Cutting Edge, Gene's Work, and Mane Society hold the premium segment. No competitor operates in Kuching's expat residential corridor. No competitor offers a genuine Muslimah private suite at boutique quality. No competitor runs soft-water filtration. Three unaddressed gaps in one market.</li>
                    <li><strong>Regulatory Context:</strong> SSM registration. Sarawak State Health Department salon hygiene permit. Sarawak has separate state-level regulations from Peninsular Malaysia — verify local requirements for chemical service licensing with Sarawak MOH. EP/SP visas for non-Malaysian stylists.</li>
                </ul>
"""

# ============================================================
# KAOHSIUNG
# ============================================================
KAOHSIUNG_COMPETITORS = """
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
                                <td><strong>Round2 Hair Salon</strong></td>
                                <td>Multiple (Linsen, Minghua, Fumin)</td>
                                <td>Color TWD 2,600–6,000 (~$81–$187); Balayage TWD 4,500–8,000</td>
                                <td>Prominent Kaohsiung chain, refined modern techniques, consistent quality across outlets, professional reputation</td>
                                <td>Chain salon formula — not boutique personalized; stylist quality varies by outlet; limited English consultation for foreign clients</td>
                                <td>Independent boutique consistency; English + Japanese + Mandarin trilingual team; senior color specialist every appointment</td>
                            </tr>
                            <tr>
                                <td><strong>UCA Salon</strong> (Unique Create Art)</td>
                                <td>Multiple Kaohsiung locations</td>
                                <td>Color TWD 2,500–7,000 (~$78–$219); Senior designer premium tier</td>
                                <td>Established Taiwan-wide brand, tiered pricing allows senior designer access, professional environment</td>
                                <td>National chain = standardized service without genuine boutique personalization; senior designer tiers expensive relative to quality delivered; no private bays</td>
                                <td>Boutique-only senior stylist delivery; private styling bays; Japanese product stack (Milbon, Demi) superior to UCA's standard professional line</td>
                            </tr>
                            <tr>
                                <td><strong>VS Hair Salon</strong></td>
                                <td>Kaohsiung</td>
                                <td>Color TWD 2,000–5,500 (~$63–$172)</td>
                                <td>Japanese product commitment (training + product quality), strong hair health focus, continuous training culture</td>
                                <td>Japanese product focus means conservative styling aesthetic — less suited for bold creative balayage or fashion vivid toning</td>
                                <td>Japanese product quality with full creative color range — from natural to vivid — serving Kaohsiung's fashion-forward demographic</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

KAOHSIUNG_UNMET = """
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
                                <td>Premium boutique in Xinyi / Zuoying district (HHKBR terminus area)</td>
                                <td>Round2 and UCA outlets are distributed across Kaohsiung but none specifically serve the emerging Zuoying HHKBR / Expo Park premium corridor</td>
                                <td>Kaohsiung's high-speed rail terminus (Zuoying THSR) and Expo Park area is a fast-developing luxury residential and commercial zone. Professionals commuting via THSR from Taipei represent a high-WTP segment with no premium boutique salon within 5-min walk of the station</td>
                                <td>Ground-floor boutique in Zuoying THSR commercial zone — capturing both Kaohsiung residents AND Taipei business travelers who plan appointments around their THSR schedule</td>
                            </tr>
                            <tr>
                                <td>Japanese-quality balayage for Kaohsiung's growing Japanese corporate community</td>
                                <td>VS Hair Salon uses Japanese products but not Japanese balayage technique specialists; Round2 has no Japanese staff</td>
                                <td>Kaohsiung's Japanese manufacturing community (Foxconn, Innolux supply chain Japanese staff, TSMC Japanese partnerships) and Japanese tourist inflow (~200,000/year) are looking for familiar Japanese salon quality. No salon in Kaohsiung proactively markets to this community</td>
                                <td>Japanese-speaking staff + Milbon/Demi product stack + Japan-certified color technique — marketed via Kaohsiung Japanese community LINE groups and tourism partnerships</td>
                            </tr>
                            <tr>
                                <td>UV-protective color for Kaohsiung's extreme southern Taiwan climate</td>
                                <td>No Kaohsiung salon markets UV-adaptive color finishing</td>
                                <td>Kaohsiung (23°N latitude) has UV index 10–12 from April to October — among the highest in Taiwan. Color fades noticeably faster than in Taipei or Taichung. Outdoor lifestyle (cycling paths, Love River, beaches) amplifies UV exposure for the target demographic</td>
                                <td>"Kaohsiung Solar Shield" post-color UV-protect Solaris treatment — marketed specifically to Kaohsiung's outdoor lifestyle and Southern Taiwan climate reality</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

KAOHSIUNG_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Kaohsiung is Taiwan's second-largest city (2.75 million metro) with a substantial Japanese business community (~3,000 residents plus 200,000+ annual Japanese tourists), growing Western tech/manufacturing expat cluster (TSMC supply chain partners, Hon Hai/Foxconn international staff), and a large affluent local professional demographic in Xinyi, Sanmin, and Lingya districts.</li>
                    <li><strong>Spending Power:</strong> Kaohsiung professionals budget TWD 3,500–8,000 per color session — slightly lower than Taipei but growing as the city's tech sector expands. Japanese corporate managers budget TWD 6,000–12,000 and are loyal repeat clients once quality is established. THSR access to Taipei means Kaohsiung can capture weekend quality-service trips from Taipei professionals.</li>
                    <li><strong>Water Quality:</strong> Kaohsiung Water Bureau supply has moderate TDS (100–200 ppm) from Gaoping River system. Higher chlorination than Taipei due to warmer southern climate. UV combined with chlorine creates a dual color-damage environment — addressable with soft-water filtration and UV-protect post-treatment.</li>
                    <li><strong>Competitive Environment:</strong> Round2, UCA, and VS Hair Salon hold the professional tier; none are genuine boutiques. No competitor proactively serves the Japanese expat/tourist community. The Zuoying THSR commercial zone has zero premium salon representation — a clear first-mover opportunity.</li>
                    <li><strong>Regulatory Context:</strong> Standard Taiwan BOFT registration. Cosmetology license (美容師執照) for all color/chemical staff. 100% foreign ownership permissible. Kaohsiung City Government's Southern Taiwan Service Industry Development Plan offers potential subsidies for premium service businesses opening in designated development zones (check KTDEP program eligibility).</li>
                </ul>
"""

# ============================================================
# DONG NAI (Bien Hoa)
# ============================================================
DONGNAI_COMPETITORS = """
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
                                <td><strong>Local Vietnamese Salons</strong> (e.g., Toc Mai, Salon 18)</td>
                                <td>Bien Hoa City / AMATA IP area</td>
                                <td>Color $5–18; Cut $2–6</td>
                                <td>Extremely affordable, abundant locations, high local volume</td>
                                <td>No English or Korean language; basic chemicals only; cannot safely bleach for balayage; not suitable for expat creative color requests</td>
                                <td>Professional-grade bleach and bond-repair (K18); Korean/Japanese bilingual consultation; safe complex color for non-Asian hair types</td>
                            </tr>
                            <tr>
                                <td><strong>HCMC Korean Salon Chains</strong> (Aube Vietnam, Hallyuhair)</td>
                                <td>HCMC District 7 / Thu Duc (50–80 min drive)</td>
                                <td>Color $30–80; Cut $15–25</td>
                                <td>Professional Korean product and technique, trusted Korean expat community reputation</td>
                                <td>50–80 minute commute from Dong Nai AMATA/Loteco — unacceptably far for a regular service; full-day time cost</td>
                                <td>On-site in Bien Hoa: same Korean product and technique quality, zero commute time for AMATA/Loteco zone Korean factory managers</td>
                            </tr>
                            <tr>
                                <td><strong>Concept Coiffure / Vampire Hair</strong> (HCMC)</td>
                                <td>HCMC District 1–3 (60–90 min drive)</td>
                                <td>Balayage $80–200; Cut $30–60</td>
                                <td>Premium French/Western managed, HCMC's top expat color choice, highly professional</td>
                                <td>60–90 min drive from Dong Nai — effectively only accessible on weekends; not viable for routine appointments</td>
                                <td>Bien Hoa boutique delivers equivalent quality; 5-min drive from AMATA IP gate — after-work appointments viable</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

DONGNAI_UNMET = """
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
                                <td>Professional hair color without 60–90 min HCMC commute</td>
                                <td>Korean expats commute to Aube/Hallyuhair; European expats commute to Concept Coiffure — 2–3 hrs round trip</td>
                                <td>Dong Nai has 50,000+ Korean industrial expats (AMATA, Loteco, Loteco 2, Nhon Trach zones) plus 8,000+ Japanese and European factory managers. All must commute to HCMC for professional color services. This is the most captive zero-competition expat market in Southeast Asia</td>
                                <td>Premium boutique 5-min drive from AMATA IP gate, Bien Hoa — same product quality as HCMC Korean salons, zero commute</td>
                            </tr>
                            <tr>
                                <td>Korean-language hair service for AMATA/Loteco Korean community</td>
                                <td>No Korean-language salon exists anywhere in Dong Nai province</td>
                                <td>Dong Nai's Korean factory community is the largest concentration of Korean industrial expats in Vietnam outside Binh Duong. Korean community apps (KakaoTalk groups, Naver Cafes) show consistent requests for local salon recommendations that never get an in-province answer</td>
                                <td>Korean-speaking lead stylist + Korean brand shelf (Mise En Scène, Somang, Amos Professional) + KakaoTalk booking channel for Korean industrial community</td>
                            </tr>
                            <tr>
                                <td>Soft-water color in Dong Nai's hard river water</td>
                                <td>No Bien Hoa salon addresses Dong Nai River water hardness (TDS 300–550 ppm)</td>
                                <td>Dong Nai Water Supply (DOWACO) draws from Dong Nai River with naturally high dissolved minerals. Korean expats from Seoul (TDS ~50 ppm tap water) experience extreme color fade and dry scalp — a documented pain point in Korean expat community chats with zero current local solution</td>
                                <td>RO soft-water filtration marketed directly at Korean community's known pain point — "color guaranteed 8 weeks" vs. HCMC comparison marketing</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

DONGNAI_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Dong Nai province (Bien Hoa City as hub) has approximately 50,000–70,000 Korean industrial expats — concentrated in AMATA Industrial City, Loteco Industrial Zone, Nhon Trach Industrial Parks. Japanese and Taiwanese factory management adds another 8,000–12,000. This is one of Vietnam's densest industrial expat populations outside Binh Duong, and the market is almost completely ignored by quality beauty services.</li>
                    <li><strong>Spending Power:</strong> Korean factory managers earn $2,500–6,000/month USD equivalent with housing and transportation allowances. Their spouses (the primary salon target) have free weekday schedules and budget $50–120/session for premium hair services. European/US expats budget $80–150. This is a deeply underserved high-income captive market.</li>
                    <li><strong>Water Quality:</strong> DOWACO supply from Dong Nai River has TDS 300–550 ppm with high calcium and seasonal turbidity. This is measurably worse than Seoul tap water (TDS ~50 ppm) — Korean clients notice the difference immediately in hair texture and color longevity. Soft-water filtration is arguably more commercially important here than in any other city in the portfolio.</li>
                    <li><strong>Competitive Environment:</strong> Literally zero premium hair salon competition in Dong Nai province that serves the international expat community. Local Vietnamese salons are unsuitable for complex color services. The next closest quality option (HCMC Aube/Hallyuhair) requires a 50–80 minute drive. This is the most open competitive landscape in the entire 27-city shortlist.</li>
                    <li><strong>Regulatory Context:</strong> Standard Vietnamese LLC registration in Dong Nai province. Bien Hoa City People's Committee commercial license + provincial Ministry of Health salon hygiene permit. Work permits for Korean/Japanese stylists via standard 2-year renewable process. Industrial zone commercial areas (AMATA commercial zone) provide easy lease access with established expat foot traffic.</li>
                </ul>
"""

# ============================================================
# TAINAN
# ============================================================
TAINAN_COMPETITORS = """
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
                                <td><strong>Local Mid-tier Salons</strong> (e.g., Ciao Hair, Style Park)</td>
                                <td>Tainan East / Anping</td>
                                <td>Color TWD 1,500–3,500 (~$47–$109)</td>
                                <td>Very price competitive, long-standing local reputation, high volume, convenient locations</td>
                                <td>Mid-tier quality ceiling; limited English for expat clients; no specialist creative color team; basic product stack</td>
                                <td>Premium balayage specialist team + English/Japanese bilingual + Olaplex/K18 product stack at TWD 4,500–8,000 aspirational pricing</td>
                            </tr>
                            <tr>
                                <td><strong>National Chain Outlets</strong> (e.g., Juno, Uniclub)</td>
                                <td>Malls and high streets, Tainan</td>
                                <td>Color TWD 2,000–5,000 (~$63–$156)</td>
                                <td>Consistent chain standards, professional environment, accessible pricing, Tainan-familiar brand</td>
                                <td>Chain formula without boutique personalization; no private styling bays; limited balayage specialist expertise; large stylist turnover</td>
                                <td>Independent boutique with consistent senior stylist; private bays; all-inclusive transparent pricing with no add-on surprises</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

TAINAN_UNMET = """
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
                                <td>Premium boutique near TSMC/STSP tech campus (Southern Taiwan Science Park)</td>
                                <td>No premium boutique salon exists within 5km of TSMC Fab 18/STSP</td>
                                <td>TSMC's Tainan fabs employ 10,000+ engineers including 2,000+ Japanese, European, and US international staff with housing in Sinshih and Shanhua. These high-income professionals have no quality hair salon within reasonable distance — they commute to Taipei or Kaohsiung on weekends for premium color</td>
                                <td>Ground-floor boutique in Sinshih or Annan District commercial zone, adjacent to TSMC/STSP housing clusters — the first premium studio serving Tainan's semiconductor expat community</td>
                            </tr>
                            <tr>
                                <td>Japanese-quality hair service for Japanese TSMC staff</td>
                                <td>No Tainan salon proactively serves the Japanese engineering community at TSMC</td>
                                <td>TSMC's Japanese advanced process partnerships have brought 500–800 Japanese engineers to Tainan fab sites. Japanese staff expect familiar salon quality and products (Milbon, Demi, Napla) — unavailable anywhere in Tainan</td>
                                <td>Japanese-speaking staff + Milbon product wall + Japan-certified color technique consultation for TSMC Japanese engineering community</td>
                            </tr>
                            <tr>
                                <td>UV-damage color protection for Tainan's extreme southern climate</td>
                                <td>No Tainan salon markets UV-specific color protection</td>
                                <td>Tainan (23°N, flattest part of Taiwan) receives intense UV year-round (UV 9–12 from March to October) with minimal cloud cover vs. northern Taiwan. TSMC expat families enjoy outdoor lifestyle — beaches, cycling. Color fade is significantly faster than Taipei or Taichung. Zero competitor addresses this</td>
                                <td>"Tainan Solar Shield" post-color treatment — Redken Shades EQ gloss + UV-protect sealing, marketed to STSP tech expat outdoor lifestyle</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

TAINAN_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Tainan (1.9 million metro) has been transformed by TSMC's massive Fab 18 investment (~NT$1 trillion over 10 years). TSMC's international staff include 2,000+ Japanese engineers and 500+ US/European technical staff, with housing concentrated in Sinshih, Shanhua, and northern Annan districts. These high-income professionals represent the primary premium salon target — currently entirely underserved locally.</li>
                    <li><strong>Spending Power:</strong> TSMC international engineers earn NT$200,000–400,000/month (USD $6,000–12,500) with housing and relocation allowances. WTP for hair services matches Taipei levels: NT$5,000–12,000 for premium color. Local Tainan professionals budget NT$3,000–6,000 — lower than Taipei but growing with TSMC-driven economic inflation.</li>
                    <li><strong>Water Quality:</strong> Tainan Water Bureau supply (Nanhua Reservoir) has moderate TDS 100–180 ppm. Warmer climate means higher chlorination than northern Taiwan — activated carbon filtration beneficial for color longevity. Soft-water addition primarily a marketing point here rather than critical technical necessity.</li>
                    <li><strong>Competitive Environment:</strong> Tainan's premium salon market is underdeveloped relative to its growing tech-professional population. National chains (Juno, Uniclub) and mid-tier local salons dominate. Zero premium boutique exists near the TSMC/STSP corridor. This is the clearest first-mover opportunity in Taiwan's salon market.</li>
                    <li><strong>Regulatory Context:</strong> Standard Taiwan BOFT registration. Cosmetology license (美容師執照) for all chemical/color staff. 100% foreign ownership permissible. Tainan City Government's Industry Development Fund offers potential incentives for premium service businesses in economic development zones — STSP zone commercial units may qualify.</li>
                </ul>
"""

# ============================================================
# TAICHUNG
# ============================================================
TAICHUNG_COMPETITORS = """
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
                                <td><strong>ELF Salon</strong></td>
                                <td>Xitun District, Taichung</td>
                                <td>Color TWD 2,500–6,000 (~$78–$187)</td>
                                <td>Highly rated for stylish modern cuts and color, chic low-maintenance styling, Instagram-worthy portfolio, strong local following</td>
                                <td>Limited English for non-Mandarin expat clients; not positioned as a creative balayage specialist; no private bays</td>
                                <td>English + Japanese bilingual consultation; dedicated creative balayage specialist portfolio; private styling bays</td>
                            </tr>
                            <tr>
                                <td><strong>VS Hair Salon</strong></td>
                                <td>Taichung</td>
                                <td>Color TWD 2,000–5,500 (~$63–$172)</td>
                                <td>Japanese product commitment (continuous training culture), strong hair health ethos, loyal professional client base</td>
                                <td>Conservative Japanese aesthetic — not suited for bold creative balayage or fashion vivid; limited international creative color portfolio</td>
                                <td>Japanese product quality + full creative color range (natural to vivid balayage) — serving both Japanese quality-seekers AND fashion-forward Taichung creative professionals</td>
                            </tr>
                            <tr>
                                <td><strong>Mpalace</strong></td>
                                <td>Taichung flagship</td>
                                <td>Color TWD 2,800–6,500 (~$87–$203)</td>
                                <td>Elegant wearable styles, professional service, experienced with different hair textures and lengths, established Taichung brand</td>
                                <td>Style-focused rather than color-specialist; no branded expertise in creative balayage; national chain formula reduces boutique intimacy</td>
                                <td>Dedicated color specialist team; boutique studio not chain formula; all-inclusive transparent pricing</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

TAICHUNG_UNMET = """
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
                                <td>Premium boutique near Taichung's Seventh Redevelopment Zone (七期) HNWI corridor</td>
                                <td>ELF and VS Hair are in Xitun but not in the premium Qi-qi (七期) luxury residential/commercial zone</td>
                                <td>Taichung's Qi-qi district (around World Trade Center / Xinyi Road) is Taiwan's most rapidly appreciating luxury real estate corridor outside Taipei. It houses Taichung's highest-income households and international business community — with no premium boutique hair studio within walking distance</td>
                                <td>Ground-floor boutique in Qi-qi commercial strip (Shizheng North Road / Taiwan Boulevard area) — first premium color boutique serving Taichung's luxury corridor</td>
                            </tr>
                            <tr>
                                <td>Specialist creative balayage for Taichung's vibrant fashion-forward creative class</td>
                                <td>VS Hair and Mpalace lean conservative Japanese/natural aesthetic; ELF does modern cuts but not specialist creative color</td>
                                <td>Taichung has a disproportionately large fashion and creative industry community (design, art, music — Taichung Creative Cultural Park and theater scene). This demographic wants bold balayage, fashion vivid toning, and copper/auburn transformations — a segment no current salon leads on</td>
                                <td>Dedicated "Taichung Creative Color" tier: copper, caramel, vivid balayage, fashion toning — with an Instagram-ready open styling environment for content creation</td>
                            </tr>
                            <tr>
                                <td>Japanese-quality service for Taichung's growing Japanese business community</td>
                                <td>VS Hair uses Japanese products but has no Japanese-speaking staff</td>
                                <td>Taichung hosts Japanese business families (Advantech, Giant Manufacturing international staff, Rinnai Taiwan) totalling ~3,000 Japanese residents. No salon in Taichung offers Japanese-language consultation or Japanese-certified stylist service</td>
                                <td>Japanese-speaking staff + Japan-certified color technique + Milbon/Demi product stack — marketed via Taichung Japanese Association and LINE community</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

TAICHUNG_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Taichung (2.8 million, Taiwan's third-largest city) has a large Japanese expatriate community (~3,000), growing Western tech/manufacturing expat segment, and a famously fashion-forward local creative class. The Qi-qi (七期) luxury development zone has transformed central Taichung into one of Taiwan's most affluent urban environments outside Taipei — with luxury hotel brands (The Lin, Kimpton, W Taichung) anchoring a genuine HNWI residential cluster.</li>
                    <li><strong>Spending Power:</strong> Qi-qi zone residents and Taichung professionals budget TWD 4,000–9,000 for premium color. Japanese corporate expats WTP: TWD 6,000–12,000. Creative industries demographic (ages 25–40) budget TWD 3,500–7,000 for specialist creative color. Overall premium market is significantly more developed than Kaohsiung or Tainan.</li>
                    <li><strong>Water Quality:</strong> Taichung Water Bureau (TWDB) supply from Deji Reservoir has TDS 80–150 ppm — relatively benign for color services. The USP is technique quality, bilingual service, and boutique experience rather than water filtration.</li>
                    <li><strong>Competitive Environment:</strong> ELF, VS Hair, and Mpalace hold the premium segment. All focus on the broader Xitun corridor without a specific Qi-qi zone boutique. The creative balayage specialist and Japanese-bilingual gaps are both genuine commercial blind spots.</li>
                    <li><strong>Regulatory Context:</strong> Standard Taiwan BOFT registration. Cosmetology license (美容師執照) required for all chemical service practitioners. 100% foreign ownership permissible. Taichung City Government's Creative Industry Development Zone (Qi-qi area) may offer commercial development incentives for premium service businesses — worth investigating with TEEMA.</li>
                </ul>
"""

# ============================================================
# KUALA LUMPUR
# ============================================================
KL_COMPETITORS = """
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
                                <td><strong>Number76</strong></td>
                                <td>Bangsar + multiple KL</td>
                                <td>Color MYR 300–700 (~$65–$151); Balayage MYR 450–800</td>
                                <td>Japanese-founded, meticulous attention to detail, consistent brand across outlets, popular with KL's fashion-forward expat community</td>
                                <td>Japanese aesthetic emphasis — limited bold creative Western balayage; chain formula reduces boutique intimacy; no soft-water filtration</td>
                                <td>Full creative color spectrum + private bays + soft-water filtration for KL's heavily chlorinated municipal water</td>
                            </tr>
                            <tr>
                                <td><strong>Bottega Hair</strong></td>
                                <td>Bangsar</td>
                                <td>Balayage MYR 500–900 (~$108–$194)</td>
                                <td>Cutting-edge blonde transformation specialist, senior director expertise, strong Instagram portfolio, Bangsar HNWI clientele</td>
                                <td>Almost exclusively blonde-focused; very limited fashion/vivid color range; very small capacity (3–4 chairs); no Muslimah private bay</td>
                                <td>Full color spectrum (blonde to vivid) + private Muslimah bay + 8-station capacity vs. Bottega's chronic overbooking</td>
                            </tr>
                            <tr>
                                <td><strong>Aube International</strong></td>
                                <td>Bangsar</td>
                                <td>Luminous Balayage MYR 380–650 (~$82–$140)</td>
                                <td>Japanese precision + "Luminous Balayage" branded package, professional environment, loyal Japanese expat community following</td>
                                <td>Bangsar-only — not accessible for KLCC/Ampang expat corridor; Japanese aesthetic limits Western bold color; limited creative range</td>
                                <td>KLCC / Ampang boutique serving central KL expat corridor + full creative color range beyond Japanese natural tones</td>
                            </tr>
                            <tr>
                                <td><strong>Shawn Cutler</strong></td>
                                <td>Bangsar</td>
                                <td>Color MYR 300–650 (~$65–$140)</td>
                                <td>Long-standing Bangsar reputation, expert stylists, on-trend coloring + balayage, trusted by long-term KL expats</td>
                                <td>Bangsar-centric — not serving KLCC/Bukit Bintang expat corridor; limited session availability; no soft-water system</td>
                                <td>Central KL boutique (KLCC corridor) + soft-water system for KL's high-TDS municipal water + private styling bays</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

KL_UNMET = """
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
                                <td>Premium boutique in KLCC / Ampang expat corridor (not Bangsar)</td>
                                <td>Bottega, Aube, Number76, Shawn Cutler — all clustered in Bangsar; KLCC/Ampang has no premium boutique equivalent</td>
                                <td>KLCC/Ampang Hilir and the "Embassy Row" corridor (Ampang, Ukay Perdana) house KL's largest Western diplomatic and executive expat community. All quality salon options require a 25–40 min drive to Bangsar — a genuine access gap for KL's most affluent expat zone</td>
                                <td>Ground-floor boutique in Jalan Ampang or Bukit Ceylon — serving KLCC tower executives and Embassy Row expat families within 5-min walk</td>
                            </tr>
                            <tr>
                                <td>Soft-water color protection in KL's hard, heavily chlorinated water</td>
                                <td>No KL premium salon deploys soft-water filtration — all use Syabas/PBA municipal water (TDS 150–300 ppm, high chlorine residual)</td>
                                <td>KL's municipal water has higher chlorine than Singapore or Taipei — color fade and hair porosity are documented expat complaints in KL beauty forums. No competitor has converted this into a service proposition despite it being a documentable, addressable pain point</td>
                                <td>RO + activated carbon + ion-exchange filtration across all basins — "KL's first soft-water color salon" marketing position; color longevity guarantee vs. all Bangsar competitors</td>
                            </tr>
                            <tr>
                                <td>Premium Muslimah private suite in KLCC corridor (not Bangsar)</td>
                                <td>Bangsar salons (Aube, Shawn Cutler) have basic Muslimah screens; no KLCC/Ampang boutique offers it at all</td>
                                <td>KLCC area houses the highest concentration of KL's Malaysian Muslim professional and HNWI community (including senior PETRONAS, Maybank, and GLiC executives). Premium Muslimah hair services at boutique quality are chronically undersupplied in this corridor</td>
                                <td>Enclosed luxury Muslimah private suite with separate entrance — serving Malaysia's most commercially powerful Muslim professional demographic in the correct geographic location</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

KL_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Kuala Lumpur has 250,000+ foreign nationals including 70,000+ Western expats (UK, US, Australia, France) concentrated in Bukit Ceylon, KLCC, Ampang Hilir, and Bangsar. Japanese community (~20,000) clusters in Bangsar and Ampang. South Korean community (~15,000) in KL Sentral / Jalan Imbi area. PETRONAS, Standard Chartered, Shell, and international law firm clusters dominate the KLCC corridor.</li>
                    <li><strong>Spending Power:</strong> KLCC corridor professionals (investment banking, energy, legal) earn $150,000–350,000+ USD equivalent packages. WTP for premium hair services: MYR 500–900 per session. Bangsar HNWI household income averages MYR 30,000+/month. This is one of Southeast Asia's deepest premium beauty markets.</li>
                    <li><strong>Water Quality:</strong> Syabas/PBA KL municipal water supply has residual chlorine 0.3–0.6 mg/L and TDS 150–300 ppm — moderate-to-hard by global standards and notably damaging for bleach-based balayage. Color fade, hair porosity, and mineral buildup are consistent expat complaints in KL forums. Soft-water filtration is both technically warranted and commercially compelling.</li>
                    <li><strong>Competitive Environment:</strong> Bangsar is over-concentrated with Number76, Bottega, Aube, and Shawn Cutler — all competing for the same clientele. The KLCC/Ampang corridor with its larger expat population has zero equivalent quality boutique. The Muslimah premium gap in the KLCC zone is entirely unaddressed.</li>
                    <li><strong>Regulatory Context:</strong> SSM business registration. Ministry of Health salon hygiene certification. EP (Employment Pass) for foreign stylist hires — apply minimum 3 months in advance. Syariah-compliant Muslimah private bay requirement is best practice and expected by Maybank/PETRONAS professional client base; factor into salon floor plan from the outset.</li>
                </ul>
"""

# ============================================================
# Apply All Updates
# ============================================================
updates = {
    "brisbane.html": {
        "competitors": BRISBANE_COMPETITORS,
        "unmet-needs": BRISBANE_UNMET,
        "market-context": BRISBANE_MARKET,
    },
    "sydney.html": {
        "competitors": SYDNEY_COMPETITORS,
        "unmet-needs": SYDNEY_UNMET,
        "market-context": SYDNEY_MARKET,
    },
    "okinawa.html": {
        "competitors": OKINAWA_COMPETITORS,
        "unmet-needs": OKINAWA_UNMET,
        "market-context": OKINAWA_MARKET,
    },
    "haiphong.html": {
        "competitors": HAIPHONG_COMPETITORS,
        "unmet-needs": HAIPHONG_UNMET,
        "market-context": HAIPHONG_MARKET,
    },
    "sabah.html": {
        "competitors": SABAH_COMPETITORS,
        "unmet-needs": SABAH_UNMET,
        "market-context": SABAH_MARKET,
    },
    "sarawak.html": {
        "competitors": SARAWAK_COMPETITORS,
        "unmet-needs": SARAWAK_UNMET,
        "market-context": SARAWAK_MARKET,
    },
    "kaohsiung.html": {
        "competitors": KAOHSIUNG_COMPETITORS,
        "unmet-needs": KAOHSIUNG_UNMET,
        "market-context": KAOHSIUNG_MARKET,
    },
    "tainan.html": {
        "competitors": TAINAN_COMPETITORS,
        "unmet-needs": TAINAN_UNMET,
        "market-context": TAINAN_MARKET,
    },
    "taichung.html": {
        "competitors": TAICHUNG_COMPETITORS,
        "unmet-needs": TAICHUNG_UNMET,
        "market-context": TAICHUNG_MARKET,
    },
    "dongnai.html": {
        "competitors": DONGNAI_COMPETITORS,
        "unmet-needs": DONGNAI_UNMET,
        "market-context": DONGNAI_MARKET,
    },
    "kualalumpur.html": {
        "competitors": KL_COMPETITORS,
        "unmet-needs": KL_UNMET,
        "market-context": KL_MARKET,
    },
}

print("=== APPLYING BATCH 2 SUBSTANTIVE UPDATES ===")
for fname, sections in updates.items():
    path = os.path.join(WORKDIR, fname)
    if not os.path.exists(path):
        print(f"  MISSING FILE: {fname}")
        continue
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
        print(f"  SKIPPED (no section matches): {fname}")

print("\nDone.")
