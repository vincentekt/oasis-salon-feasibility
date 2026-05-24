"""
update_location_tables.py
Updates the location-study table rows in each subpage to match the new
candidate site research (recommended corridor, rent, pros/cons, rating).
"""
import os, re

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

LOCATION_TABLES = {

"hcmc.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Concept Coiffure (Xuan Thuy St)</td>
                                  <td>USD 2,500 - 3,500</td>
                                  <td>Heart of Japanese/Korean/Western expat cluster. Concept Coiffure &amp; J-First within 500m confirm premium demand. Ground-floor shophouse on main expat street.</td>
                                  <td>High rent premium for Thao Dien address; weekday parking can be congested</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Masteri T5 (Quoc Huong St)</td>
                                  <td>USD 2,000 - 2,800</td>
                                  <td>Parallel street, quieter lane, lower rent. Same expat density. Better parking for school-run appointment timing.</td>
                                  <td>Slightly less main-road visibility; needs signage investment</td>
                                  <td>4.5 / 5</td>
                              </tr>
                              <tr>
                                  <td>Sheraton Saigon Hotel (Le Thanh Ton St)</td>
                                  <td>USD 3,500 - 5,000</td>
                                  <td>Central D1 expat corridor. Vampire Hair (competitor) validates premium demand. Captures business-traveler and hotel-guest walk-in market.</td>
                                  <td>High D1 rent; lower residential density than Thao Dien; more tourist-mix than expat-resident</td>
                                  <td>3.8 / 5</td>
                              </tr>
             </tbody>""",

"hanoi.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Syrena Center (Xuan Dieu St)</td>
                                  <td>USD 1,800 - 2,800</td>
                                  <td>Diplomatic Quarter / Expat Central. West Lake views. Maika Hair and KUKAI Hanoi within 400m confirm premium demand. Ground-floor shophouse with outdoor-signage potential.</td>
                                  <td>Hard water (TDS 400+ ppm) requires soft-water filtration investment — but this becomes a USP vs all local competitors</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Saint Honoré Bakery (To Ngoc Van St)</td>
                                  <td>USD 1,400 - 2,200</td>
                                  <td>Side street off Xuan Dieu. French School, UN building, Korean Embassy nearby — captive expat residential corridor. Lower rent for same demographic.</td>
                                  <td>Less main-road visibility; requires stronger digital marketing to drive foot traffic</td>
                                  <td>4.4 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Trang Tien Plaza</td>
                                  <td>USD 2,200 - 3,000</td>
                                  <td>High foot traffic, business traveler access, near Sofitel Legend Metropole. Good for premium walk-in market.</td>
                                  <td>Lower premium residential density than Tay Ho; more mid-tier competition from local salons on same street</td>
                                  <td>3.6 / 5</td>
                              </tr>
             </tbody>""",

"danang.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Holiday Beach Club (An Thuong Beach)</td>
                                  <td>USD 600 - 1,000</td>
                                  <td>Digital nomad + Korean expat residential cluster. Highest per-capita expat density in Da Nang. Ground-floor shophouse within walking distance of beach cafes and co-working spaces.</td>
                                  <td>Seasonal volume variance (Nov–Mar monsoon slows tourism); smaller total catchment than city center</td>
                                  <td>4.8 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks TMS Hotel (My Khe Beach)</td>
                                  <td>USD 500 - 850</td>
                                  <td>Adjacent to resort strip. Strong tourist walk-in potential and resort-staff clientele. Growing year-round Korean permanent resident base.</td>
                                  <td>Slightly lower Korean residential density than An Thuong; more resort-tourist than professional-expat</td>
                                  <td>4.2 / 5</td>
                              </tr>
                              <tr>
                                  <td>Highlands Coffee Indochina Riverside Mall</td>
                                  <td>USD 700 - 1,100</td>
                                  <td>City-center anchor. Captures Vietnamese professional market. Access to larger commercial retail space with better loading/logistics.</td>
                                  <td>Lower expat density; more mid-tier local competition; less "destination boutique" feel</td>
                                  <td>3.5 / 5</td>
                              </tr>
             </tbody>""",

"haiphong.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Highlands Coffee Museum Area (Minh Khai St)</td>
                                  <td>USD 500 - 800</td>
                                  <td>5-min drive from Deep C Industrial Zone gate (20,000+ Korean workers). Ground-floor shophouse with direct road access. Zero premium competition in entire corridor. Factory bus routes pass this street.</td>
                                  <td>Requires active marketing into industrial zone networks; no organic walk-in from general public</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Vincom Plaza Imperia</td>
                                  <td>USD 650 - 950</td>
                                  <td>Captive resident market within premium gated community. Korean/Japanese families in compound. Guaranteed residential repeat clientele with very short travel time.</td>
                                  <td>Smaller total catchment; community lease terms may restrict external marketing</td>
                                  <td>4.4 / 5</td>
                              </tr>
                              <tr>
                                  <td>Highlands Coffee Lach Tray St</td>
                                  <td>USD 600 - 900</td>
                                  <td>Central commercial zone. HaLa and Nguyen Hung competition validates premium demand. Broader Vietnamese professional catchment.</td>
                                  <td>More competitive environment; HaLa and Nguyen Hung already entrenched here; harder to differentiate</td>
                                  <td>3.5 / 5</td>
                              </tr>
             </tbody>""",

"binhduong.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Highlands Coffee Canary Plaza</td>
                                  <td>USD 500 - 750</td>
                                  <td>Adjacent to VSIP I (50,000+ Korean/Japanese workers). Ground-floor unit within walking distance of factory bus stop. Zero premium competition within 10km. Anchor tenant positioning in a blank-slate market.</td>
                                  <td>Industrial area feel — boutique interior design critical to create contrasting premium atmosphere; logistics from HCMC needed for premium products</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Aeon Mall Binh Duong</td>
                                  <td>USD 750 - 1,100</td>
                                  <td>Guaranteed foot traffic from Korean family shopping trips. Multiple Korean restaurants confirm demand in zone. Higher mall rent but lower fit-out risk — established premium retail environment.</td>
                                  <td>Mall rent premium; mall hours constrain operating schedule; competitor risk from national chain anchors</td>
                                  <td>4.2 / 5</td>
                              </tr>
                              <tr>
                                  <td>Highlands Coffee Becamex Tower</td>
                                  <td>USD 400 - 650</td>
                                  <td>Provincial capital hub. Larger Vietnamese management-class catchment. Good for Phase 2 after industrial expat base is established.</td>
                                  <td>Lower Korean expat density; further from VSIP/AMATA zones; primarily serves Vietnamese professional rather than expat market</td>
                                  <td>3.4 / 5</td>
                              </tr>
             </tbody>""",

"dongnai.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Highlands Coffee Amata Gate</td>
                                  <td>USD 400 - 650</td>
                                  <td>AMATA Industrial City main gate road. 40,000+ Korean/Japanese workers within 2km. Currently ZERO premium salon competition in entire zone. Factory family residential compounds within 3km. Highest underserved demand in entire 27-city portfolio.</td>
                                  <td>Requires heavy marketing investment to bootstrap awareness; no existing premium salon precedent to piggyback on</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>The Coffee House Loteco Gate</td>
                                  <td>USD 380 - 600</td>
                                  <td>Captures Loteco 1 &amp; 2 and Nhon Trach overflow. Korean restaurant cluster confirms expat demand. Slightly lower density than AMATA gate but lower rent.</td>
                                  <td>Smaller total Korean catchment than AMATA zone; less established commercial strip</td>
                                  <td>4.4 / 5</td>
                              </tr>
                              <tr>
                                  <td>Highlands Coffee Pegasus Plaza</td>
                                  <td>USD 500 - 800</td>
                                  <td>Biên Hòa's premier high-street dining & lifestyle corridor. Highest concentration of upscale cafes, Korean restaurants, and premium local consumer spending. Best visibility for a flagship brand.</td>
                                  <td>Higher rental rates; parking can be highly constrained during evening dining peaks; slightly further from AMATA/Loteco industrial parks (10-12 mins) compared to gate-side options.</td>
                                  <td>4.1 / 5</td>
                              </tr>
             </tbody>""",

"kuala_lumpur.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Suria KLCC (Jalan Ampang)</td>
                                  <td>MYR 12,000 - 18,000</td>
                                  <td>Embassy Row / KLCC expat corridor. 25-min drive from all Bangsar alternatives — serves KL's highest-income diplomatic and corporate expat community (PETRONAS, Standard Chartered, Shell). Number76/Bottega are 25 min away — captive gap.</td>
                                  <td>High KLCC-zone rent; requires strong soft-water + Muslimah bay differentiation to justify premium over established Bangsar options</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Feeka Coffee Roasters (Bukit Ceylon)</td>
                                  <td>MYR 9,000 - 14,000</td>
                                  <td>Established expat residential enclave. Walking distance from Pavilion KL and KLCC. Lower rent than Ampang corridor. High concentration of diplomatic, legal, and finance professionals.</td>
                                  <td>Slightly less accessible for Embassy Row / Ampang Hilir expat families; limited Muslimah private bay walk-in demand in this sub-zone</td>
                                  <td>4.5 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Bangsar Village II</td>
                                  <td>MYR 10,500 - 15,500</td>
                                  <td>Established premium zone with Number76, Bottega, Aube all operating — validates premium demand. Best as Phase 2 second outlet after KLCC flagship.</td>
                                  <td>Highly saturated premium zone — competing directly with 4 established premium salons; limited differentiation space</td>
                                  <td>3.5 / 5 (Phase 2 Only)</td>
                              </tr>
             </tbody>""",

"johor.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks R&F Mall</td>
                                  <td>MYR 5,000 - 8,000</td>
                                  <td>Direct RTS Link skybridge — Singapore cross-border clients enter without street-level commute. Premium mall positioning. Singapore clients budget SGD pricing (USD 65–120+). REDS Hair Salon confirms premium hair demand in RTS zone.</td>
                                  <td>Mall hours constrain operating schedule; RTS operational delays still possible; requires premium mall fit-out</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Komtar JBCC</td>
                                  <td>MYR 4,000 - 6,500</td>
                                  <td>Largest mall in JB. High foot traffic from Singapore day-trippers and JB residents. Direct CIQ connection. REDS and Stay B proximity confirms demand.</td>
                                  <td>Older mall — less premium brand environment; competition from established JB salons in same building</td>
                                  <td>4.3 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Mall of Medini</td>
                                  <td>MYR 3,000 - 5,000</td>
                                  <td>Fast-growing business district. International School cluster. IHH Healthcare and Pinewood Studios expat families. Lower competition, high growth trajectory.</td>
                                  <td>Currently low foot traffic; 20-min from CIQ checkpoint; relies on Iskandar Medini development pace</td>
                                  <td>3.8 / 5</td>
                              </tr>
             </tbody>""",

"penang.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Gurney Paragon (Jalan Burma)</td>
                                  <td>MYR 2,500 - 4,000</td>
                                  <td>Georgetown's premium lifestyle corridor between Gurney Drive and Penang Hill Road junction. A-Saloon and Wave Hair within 600m confirm premium demand. Heritage shophouse aesthetic fits boutique positioning naturally.</td>
                                  <td>Heritage conservation area requires MBPP planning approval for fit-out changes; limited parking on Burma Rd itself</td>
                                  <td>4.8 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Gurney Plaza (Gurney Drive)</td>
                                  <td>MYR 3,500 - 6,000</td>
                                  <td>Adjacent to Penang's most premium mall. High visibility to HNWI families. Good parking. Strong luxury retail environment for premium positioning.</td>
                                  <td>Higher rent; mall-adjacent means closer competition from Gurney Paragon anchor salon tenants</td>
                                  <td>4.3 / 5</td>
                              </tr>
                              <tr>
                                  <td>The Mugshot Cafe (Chulia St)</td>
                                  <td>MYR 1,800 - 3,000</td>
                                  <td>Instagram-worthy heritage setting. High tourist traffic. Best for brand awareness and digital nomad market.</td>
                                  <td>Lower premium residential density; tourist-heavy means lower repeat-visit rate; heritage lane limits signage options</td>
                                  <td>3.6 / 5</td>
                              </tr>
             </tbody>""",

"sabah.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Jesselton Point</td>
                                  <td>MYR 3,000 - 5,000</td>
                                  <td>KK's premier waterfront. Ground-floor retail facing Jesselton Point Ferry Terminal — maximum tourist and expat visibility. Oil &amp; gas executives from Menara TH and Sabah Energy cluster nearby. No premium colour studio in this corridor.</td>
                                  <td>Ferry terminal proximity means tourist-heavy crowd — need clear positioning to attract resident premium clients vs day-trippers</td>
                                  <td>4.8 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Suria Sabah (Jalan Gaya)</td>
                                  <td>MYR 2,500 - 4,000</td>
                                  <td>KK's main commercial street. Within walking distance of Suria Sabah and Oceanus Mall. Michael &amp; Guys nearby confirms premium hair demand. Best balance of rent vs established foot traffic.</td>
                                  <td>Michael &amp; Guys direct competition on same commercial strip; ground-floor availability limited</td>
                                  <td>4.4 / 5</td>
                              </tr>
                              <tr>
                                  <td>Magellan Club Restaurant (Sutera Harbour)</td>
                                  <td>MYR 5,000 - 9,000</td>
                                  <td>5-star resort corridor. Guaranteed HNWI clientele from Shell, Murphy Oil, resort management. Highest average ticket potential of three candidates.</td>
                                  <td>Very high rent; very low walk-in; appointment-only model requires strong advance booking system; limited Muslimah privacy options in resort-facing boutiques</td>
                                  <td>4.0 / 5</td>
                              </tr>
             </tbody>""",

"sarawak.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Vivacity Megamall (Tabuan Jaya)</td>
                                  <td>MYR 2,000 - 3,500</td>
                                  <td>Shell Sarawak / Petronas Carigali expat residential hub. Ground-floor shophouse 5-min drive from expatriate housing estates (Green Road, Stutong). Zero premium competition in zone. Captured Shell rotation-cycle clientele.</td>
                                  <td>Requires active corporate partnership with Shell/Petronas HR for staff awareness; less organic tourist walk-in</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Tealive Hikmah Exchange</td>
                                  <td>MYR 2,500 - 4,000</td>
                                  <td>Kuching's emerging premium lifestyle hub. Gene's Work Hair Studio present — validates premium market. Central location accessible to entire Kuching metro. Growing F&amp;B and retail ecosystem.</td>
                                  <td>Gene's Work is an entrenched competitor in this zone; higher rent than Tabuan Jaya</td>
                                  <td>4.3 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Northbank Drive-Thru</td>
                                  <td>MYR 1,800 - 3,000</td>
                                  <td>Kuching's revitalised waterfront. Mane Society confirms premium hair interest in zone. Heritage boutique aesthetic advantage. Tourist and professional cross-traffic.</td>
                                  <td>Mane Society direct competition; tourist-heavy waterfront lowers repeat-client residential density</td>
                                  <td>3.8 / 5</td>
                              </tr>
             </tbody>""",

"taipei.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Taipei Yongkang (Da'an District)</td>
                                  <td>NTD 90,000 - 130,000</td>
                                  <td>Japan-quality boutique density. Eddie Tham and SeeFu within 400m confirm premium demand. AIT (American Institute Taiwan) expat community in catchment. Ground-floor alleyway boutique positioning — highest Instagram appeal in Taipei.</td>
                                  <td>Competitive zone — must differentiate on bilingual service and no-wait booking vs. 6–9 hr wait competitors</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks ATT 4 FUN (Xinyi District)</td>
                                  <td>NTD 120,000 - 180,000</td>
                                  <td>Taipei's financial and luxury retail hub near Taipei 101. TSMC and tech international executives in Xinyi luxury condos. Highest per-client WTP of any Taipei zone.</td>
                                  <td>Very high rent; after-work appointments must compete with Xinyi's existing premium service density</td>
                                  <td>4.4 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Zhongshan MRT (Zhongshan District)</td>
                                  <td>NTD 70,000 - 100,000</td>
                                  <td>Creative design district. Japanese expat families cluster near Minami Tokyo community spaces. Fashion-forward creative class for vivid/fashion colour portfolio. Lower rent than Da'an.</td>
                                  <td>Lower premium density than Da'an; requires stronger creative colour portfolio to attract design-district clientele</td>
                                  <td>4.1 / 5</td>
                              </tr>
             </tbody>""",

"taichung.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Theater Café (National Taichung Theater)</td>
                                  <td>NTD 80,000 - 120,000</td>
                                  <td>Taichung's most affluent zone. W Taichung and Kimpton Hotels anchors the area. Japanese business families from Advantech/Giant cluster in luxury towers. No boutique colour studio in this zone — first-mover opportunity.</td>
                                  <td>Premium rent; requires strong luxury positioning and differentiated bilingual service to justify premium over existing ELF/VS options</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Shin Kong Mitsukoshi (Xitun)</td>
                                  <td>NTD 60,000 - 85,000</td>
                                  <td>ELF Salon and VS Hair present — confirms premium demand and established foot traffic. Lower rent than Qi-qi. Good transit access.</td>
                                  <td>ELF and VS Hair direct competition on same boulevard; need clear differentiation on creative colour and bilingual service</td>
                                  <td>4.2 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Beitun Wenxin</td>
                                  <td>NTD 45,000 - 65,000</td>
                                  <td>Emerging premium residential corridor north of Qi-qi. Lower competition, growing family demographic. Best as second outlet once Qi-qi flagship is profitable.</td>
                                  <td>Lower current foot traffic; less established premium commercial environment; longer time to build awareness</td>
                                  <td>3.6 / 5 (Phase 2)</td>
                              </tr>
             </tbody>""",

"kaohsiung.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Shin Kong Mitsukoshi (Zuoying THSR)</td>
                                  <td>NTD 60,000 - 80,000</td>
                                  <td>High-speed rail terminus. First-mover position — zero premium salon in zone. THSR commuters from Taipei book appointments around train schedule. Japanese Foxconn/Innolux corporate housing adjacent. Highest underserved score in Kaohsiung.</td>
                                  <td>Lower current foot traffic than Lingya; relies on THSR commuter booking behavior; requires appointment-heavy model</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Pacific SOGO (Sanduo Shopping)</td>
                                  <td>NTD 70,000 - 95,000</td>
                                  <td>Kaohsiung's premier shopping/lifestyle district. Round2 Hair Salon presence validates premium demand. Highest total catchment of three candidates. Best for fashion-forward creative class.</td>
                                  <td>Round2 is entrenched here; higher rent; must differentiate on Japanese-bilingual service and creative colour range</td>
                                  <td>4.3 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Central Park MRT (Xinxing District)</td>
                                  <td>NTD 55,000 - 75,000</td>
                                  <td>Near Kaohsiung's Central Park and cultural institutions. Growing premium residential catchment. Lower competition than Lingya. Good for Japanese business community nearby.</td>
                                  <td>Less established premium retail environment than Lingya or Zuoying; lower total foot traffic</td>
                                  <td>4.0 / 5</td>
                              </tr>
             </tbody>""",

"tainan.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Tainan Sinshih (Sinshih District)</td>
                                  <td>NTD 40,000 - 60,000</td>
                                  <td>Adjacent to TSMC Fab 18 international staff housing. Japanese, US, European TSMC engineers live within 1km. Zero premium salon competition within 10km. Entirely captive high-income target market. Highest underserved % in Taiwan portfolio.</td>
                                  <td>New commercial zone — lower existing foot traffic; relies on TSMC expat community network discovery; requires proactive outreach to TSMC HR/community channels</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Tainan NCKU (East District)</td>
                                  <td>NTD 32,000 - 48,000</td>
                                  <td>NCKU university zone with growing young professional catchment. More established commercial street. Better foot traffic than Sinshih. Captures younger, fashion-forward demographic.</td>
                                  <td>Lower TSMC expat density; less affluent demographic than Sinshih; more price-sensitive clientele</td>
                                  <td>4.1 / 5</td>
                              </tr>
                              <tr>
                                  <td>Hayashi Department Store (West Central)</td>
                                  <td>NTD 35,000 - 52,000</td>
                                  <td>Historic Tainan city center. Higher general foot traffic. Best for capturing broader professional and tourist market as second phase.</td>
                                  <td>Lower premium density than Sinshih; higher local mid-tier salon competition; less TSMC-adjacent catchment</td>
                                  <td>3.6 / 5</td>
                              </tr>
             </tbody>""",

"brisbane.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Coles Merthyr Village (Brunswick St)</td>
                                  <td>AUD 3,500 - 5,500</td>
                                  <td>Brisbane's highest-income inner-east residential corridor (median house AUD 2.1M+). Zero premium colour boutique within 15-min walk. UV-damage + Asian hair specialist gap confirmed by research. All Sol Hair / Beau Gordon clients are in Paddington — 20+ min drive away.</td>
                                  <td>Heritage terrace buildings may require council DA for fit-out; premium rent demands high average ticket discipline</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Hellenika at The Calile (James St)</td>
                                  <td>AUD 3,800 - 6,500</td>
                                  <td>Adjacent to James St luxury retail (Camilla, Zimmermann). Growing Korean/Japanese community. Lower boutique colour studio density than Paddington — white space for premium colour.</td>
                                  <td>James St retail is fashion-retail heavy — needs positioning to separate from fashion brands; higher commercial rent</td>
                                  <td>4.4 / 5</td>
                              </tr>
                              <tr>
                                  <td>Sol Hair (Given Tce)</td>
                                  <td>AUD 2,800 - 4,500</td>
                                  <td>Sol Hair confirms premium demand. Strong foot traffic on Given Tce. Established premium residential catchment (Paddington, Bardon, Ashgrove).</td>
                                  <td>Sol Hair is an entrenched local brand — entering here means direct competition on their home turf; must differentiate on Asian hair expertise and UV protection angle</td>
                                  <td>3.8 / 5</td>
                              </tr>
             </tbody>""",

"sydney.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Cuckoo Callay Newtown (King St)</td>
                                  <td>AUD 4,000 - 6,500</td>
                                  <td>Sydney's most underserved premium corridor. Young professional dual-income households. Nearest premium boutique is 15-min commute to Surry Hills. Zero premium colour boutique on King St. All-inclusive transparent pricing is specifically what this demographic demands vs Surry Hills add-on fee model.</td>
                                  <td>Heritage shopfront footprints may limit salon layout; parking requires clear direction to nearby stations (Newtown/Macdonaldtown)</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Sonoma Bakery Glebe (Glebe Point Rd)</td>
                                  <td>AUD 3,200 - 5,500</td>
                                  <td>Adjacent to Newtown. University of Sydney proximity creates young professional catchment. Same demographic profile as Newtown with slightly lower foot traffic and rent.</td>
                                  <td>Lower foot traffic than King St; requires stronger appointment-driven model vs walk-in reliance</td>
                                  <td>4.4 / 5</td>
                              </tr>
                              <tr>
                                  <td>The Clock Hotel Surry Hills (Crown St)</td>
                                  <td>AUD 5,500 - 9,000</td>
                                  <td>RAW Anthony Nader, Flock, Wakefields within 300m confirm premium demand and premium client density. Highest total premium catchment of three candidates.</td>
                                  <td>4 entrenched premium competitors within 300m; very high rent; must have extremely clear differentiation (transparent pricing, Asian hair, UV-adaptive) to compete</td>
                                  <td>3.6 / 5 (Requires strong differentiation)</td>
                              </tr>
             </tbody>""",

"melbourne.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Jam Factory (Chapel St)</td>
                                  <td>AUD 4,500 - 7,000</td>
                                  <td>Melbourne's premier lifestyle corridor. Highest per-capita luxury spend in Melbourne. Japanese expat community in surrounding Prahran/Toorak. Ground-floor boutique between Toorak Rd and Commercial Rd — maximum premium visibility.</td>
                                  <td>High Chapel St rent; competition from established premium salons (Rokk Ebony, Kerluxe) on same strip; DA/lease negotiations can be complex</td>
                                  <td>4.8 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Industry Beans (Brunswick St, Fitzroy)</td>
                                  <td>AUD 3,200 - 5,500</td>
                                  <td>Creative professional zone. Fashion-forward demographic with high WTP for specialist creative colour. Growing Korean community in Carlton. Lower rent than Chapel St. Creative colour portfolio strongest competitive angle here.</td>
                                  <td>Less affluent than South Yarra; WTP ceiling lower for balayage vs vivid creative services; higher turnover retail environment</td>
                                  <td>4.3 / 5</td>
                              </tr>
                              <tr>
                                  <td>Laurent Bakery Collins Place (CBD)</td>
                                  <td>AUD 6,000 - 10,000</td>
                                  <td>Melbourne's corporate financial spine. After-work appointments from CBD professionals. Largest total catchment. Lunchtime/after-work appointment density best for corporate membership program.</td>
                                  <td>Highest rent; after-work only model limits daily capacity utilisation; CBD weekend foot traffic low</td>
                                  <td>4.0 / 5</td>
                              </tr>
             </tbody>""",

"perth.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Woolworths Subiaco Square (Rokeby Rd)</td>
                                  <td>AUD 2,500 - 4,000</td>
                                  <td>Perth's premium inner-western suburb. High FIFO mining/resources executive family density (2-weeks-on/off rotation creates regular appointment windows). Ground-floor on Rokeby Rd retail strip. UV-protection angle strongest in Perth (UV 11+ summer). No premium colour boutique in zone.</td>
                                  <td>FIFO rotation cycles create appointment volatility; Rokeby Rd parking can be congested on market days</td>
                                  <td>4.8 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Claremont Quarter (St Quentin Ave)</td>
                                  <td>AUD 2,200 - 3,800</td>
                                  <td>Old-money western suburbs. Highest household income in Perth metro. Premium boutique aesthetic fits heritage streetscape. HNWI appointment-only clientele — matches premium model.</td>
                                  <td>Small total catchment; very appointment-dependent model; limited organic foot traffic</td>
                                  <td>4.3 / 5</td>
                              </tr>
                              <tr>
                                  <td>Cottesloe Beach Hotel (Marine Pde)</td>
                                  <td>AUD 2,000 - 3,500</td>
                                  <td>Coastal boutique positioning. Beach lifestyle + UV damage angle strongest here. Summer tourist season (Oct–Apr) boosts volume significantly. Beach aesthetic aligns with UV-protect brand narrative.</td>
                                  <td>Significant seasonality risk (May–Sep winter slump); smaller permanent resident catchment; tourist clients rarely repeat</td>
                                  <td>3.8 / 5</td>
                              </tr>
             </tbody>""",

"fukuoka.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>saco Japan (Daimyo Central Lane)</td>
                                  <td>JPY 150,000 - 250,000</td>
                                  <td>Fukuoka's most fashionable boutique district. saco japan flagship and TONI&amp;GUY Tenjin within 600m confirm premium demand. Korean expat community (8,000+) in Hakata/Tenjin nearby. Creative colour + Korean-bilingual service differentiates from Japanese natural-tone dominant competitors.</td>
                                  <td>Boutique lane ground-floor availability is limited; premium creative colour requires extensive staff training investment vs natural-tone consensus competitors</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Solaria Plaza (Watanabe-dori)</td>
                                  <td>JPY 200,000 - 350,000</td>
                                  <td>Main commercial boulevard. TONI&amp;GUY directly here — validates premium demand. Maximum visibility to Fukuoka's widest catchment. Highest foot traffic of three candidates.</td>
                                  <td>Direct TONI&amp;GUY competition on same boulevard; highest rent; open plan vs boutique positioning tension</td>
                                  <td>4.2 / 5</td>
                              </tr>
                              <tr>
                                  <td>Blue Bottle Coffee Tenjin (Imaizumi Park)</td>
                                  <td>JPY 100,000 - 180,000</td>
                                  <td>Trendy alleyway boutique zone. Creative/art professional demographic. High Instagram potential for vivid fashion colour portfolio. Korean expat community adjacent in Sumiyoshi. Lowest rent of three candidates.</td>
                                  <td>Lower total catchment; alleyway requires strong signage/digital marketing; less natural foot traffic than Daimyo main lane</td>
                                  <td>4.0 / 5</td>
                              </tr>
             </tbody>""",

"okinawa.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks San-A Naha Main Place</td>
                                  <td>JPY 100,000 - 180,000</td>
                                  <td>Naha's civilian expat core — ENTIRELY UNSERVED by English/Korean-friendly premium salons. BLOOM and Borjan are 30+ min north in Chatan. Korean tourists (200,000+/yr) and Japanese civilian residents make this the highest-underserved zone in Japan portfolio. DFS Galleria and Naha Shin-toshin premium retail anchor the area.</td>
                                  <td>Japanese licensing requirements are strict; bilingual stylist recruitment requires significant lead time; 25-30 min from Kadena military base clients</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Palais Ryubo (Kumoji)</td>
                                  <td>JPY 80,000 - 140,000</td>
                                  <td>Naha central business district. Mixed Japanese professionals, Ryukyu University community, Korean tourist hotels. Good balance of resident and tourist traffic. Lower rent than Omoromachi strip.</td>
                                  <td>Less premium environment than Omoromachi; lower HNWI density; more mid-market catchment</td>
                                  <td>4.3 / 5</td>
                              </tr>
                              <tr>
                                  <td>Don Quijote Kokusai-dori</td>
                                  <td>JPY 120,000 - 220,000</td>
                                  <td>Main tourist shopping street. Maximum Korean tourist walk-in volume. High brand visibility for first-time visitors. Best for initial awareness building.</td>
                                  <td>Tourist-trap perception risk for premium positioning; very high tourist turnover lowers repeat-client rate; rent elevated relative to catchment quality</td>
                                  <td>3.6 / 5</td>
                              </tr>
             </tbody>""",

"busan.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Marine City (Haeundae I-Park)</td>
                                  <td>KRW 2,500,000 - 4,000,000</td>
                                  <td>Marine City HNWI residential towers (Zenith, I-Park Marine). Happynian (competitor) is 20 min away in Seomyeon — captive gap. No premium colour boutique in Marine City. Busan's highest-income residential zone with deepest WTP. Direct ground-floor retail in tower podium available.</td>
                                  <td>Appointment-only model required — Marine City lacks casual street foot traffic; requires active luxury residential community marketing</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Shinsegae Centum City</td>
                                  <td>KRW 3,000,000 - 5,000,000</td>
                                  <td>International business hub. BEXCO convention events drive regular business visitor influx. Shinsegae Centum confirms premium retail demand. Strong after-work catchment from Centum City IT/finance cluster.</td>
                                  <td>Business convention seasonality creates volume variance; higher competition from Shinsegae in-store salon options</td>
                                  <td>4.4 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Paradise Hotel (Haeundae Beach)</td>
                                  <td>KRW 2,800,000 - 4,500,000</td>
                                  <td>Beach Road tourism strip. Strong peak-season (Jun–Aug) volume. Proximity to Grand Hyatt and Westin creates hotel guest walk-in opportunity. Best for summer brand awareness campaigns.</td>
                                  <td>Strong seasonality (Oct–Feb quiet); tourist clients rarely repeat; premium positioning harder to maintain on tourist strip vs residential boutique</td>
                                  <td>3.8 / 5</td>
                              </tr>
             </tbody>""",

"singapore.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Da Paolo Gastronomia (Chip Bee Gardens)</td>
                                  <td>SGD 7,000 - 11,000</td>
                                  <td>Singapore's expat residential core. Chez Vous HideAway is in Scotts (2km away). Love Hair is in Jiak Chuan (3km). Holland V is a whitespace for premium colour. Ground-floor shophouse on the pedestrianised Lorong Mambong or Merah Saga strip — maximum expat community visibility.</td>
                                  <td>High Singapore rent; Holland V commercial leases from HDB have standard terms requiring SCDF fire safety and BCA fit-out approval</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Tanglin Mall</td>
                                  <td>SGD 8,000 - 13,000</td>
                                  <td>Dempsey Hill boutique zone. Blonde Boudoir here validates demand. Tanglin corridor has highest per-household income in Singapore. American Club proximity — captive HNWI community.</td>
                                  <td>Very high rent; Dempsey conservation bungalows have URA heritage restrictions on shopfront signage; smaller total catchment than Holland V</td>
                                  <td>4.5 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks 100 AM Mall (Tanjong Pagar)</td>
                                  <td>SGD 8,500 - 14,000</td>
                                  <td>Growing CBD-adjacent expat zone. Love Hair confirms premium demand. Best for after-work appointments from CBD financial professionals. Corporate membership program potential is highest here.</td>
                                  <td>Higher corporate-skew means weekend volume drop; Love Hair is direct competition; CBD proximity means primarily after-work appointments only (not daytime)</td>
                                  <td>4.2 / 5</td>
                              </tr>
             </tbody>""",

"bangkok.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Donki Mall Thonglor (Soi 10)</td>
                                  <td>USD 4,000 - 6,000</td>
                                  <td>Epicentre of Bangkok's Japanese and Western expat community. The London Hair and Yumoto are 400–600m away — confirms premium demand and establishes soft-water filtration USP against competitors using same tap water system. Ground-floor suite, high visibility, BTS Thonglor within walking distance.</td>
                                  <td>Very high demand creates availability pressure for lease signing; premium Bangkok tap water TDS 300–500 ppm requires RO filtration investment (budgeted in CAPEX)</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Featherstone Cafe (Ekkamai Soi 4)</td>
                                  <td>USD 3,200 - 4,800</td>
                                  <td>Large expat residential corridor adjacent to Thonglor. CYAN Salon validates premium colour demand. Lower rent than Thonglor main. Better parking for suburban expat families (school-run appointments).</td>
                                  <td>CYAN is direct competition here; slightly lower organic footfall than main Thonglor road; BTS access 5-min walk vs Thonglor direct</td>
                                  <td>4.4 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks The Manor 39 (Phrom Phong)</td>
                                  <td>USD 5,500 - 8,000</td>
                                  <td>Exclusive condo retail lane near EmQuartier. Highest per-capita income of any Bangkok expat zone. Micha &amp; Justin and Japanese hair salons validate ultra-premium demand. Highest average ticket potential of three candidates.</td>
                                  <td>Extremely limited ground-floor availability; highest rent; better as second-outlet vs first boutique given lease scarcity</td>
                                  <td>4.0 / 5 (Phase 2)</td>
                              </tr>
             </tbody>""",

"hongkong.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Sogo Causeway Bay (Lockhart Rd)</td>
                                  <td>HKD 60,000 - 100,000</td>
                                  <td>HK's most accessible premium retail zone. Bruneblonde and Love Hair both operate in district — high premium colour demand confirmed. Soft-water filtration is a genuine USP vs all Causeway Bay competitors on same tap water (TDS 50–100 ppm, high chloramine). MTR Causeway Bay station at doorstep.</td>
                                  <td>Extremely high HK commercial rent; Lockhart Rd premium ground-floor units have limited availability and short lease terms; must secure multi-year lease upfront</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks The Centrium (Wyndham St)</td>
                                  <td>HKD 80,000 - 130,000</td>
                                  <td>HK's financial and expat social hub. SHHH salon validates ultra-premium demand. Ground-floor on Wyndham or Peel St. After-work and lunch appointments from IFC/Wyndham St financial professionals. Highest average ticket potential in HK portfolio.</td>
                                  <td>Ultra-high rent; Central after-hours quiet means evening appointments only; SHHH is an entrenched luxury competitor requiring strong differentiation on product quality</td>
                                  <td>4.5 / 5</td>
                              </tr>
             </tbody>""",

"macau.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Taipa Village</td>
                                  <td>MOP 12,000 - 20,000</td>
                                  <td>Macau's preferred residential zone for casino management expats. Hair Cloud (competitor) presence confirms premium demand. Consistent non-gaming clientele unlike Cotai Strip. Taipa Village has the most stable year-round foot traffic from expat residents vs. tourist-only zones.</td>
                                  <td>Taipa Village is small — catchment limited to expat management community; growth ceiling lower than Cotai but more reliable baseline</td>
                                  <td>4.8 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks MGM Macau (NAPE)</td>
                                  <td>MOP 10,000 - 18,000</td>
                                  <td>Macau Peninsula modern commercial zone. Higher mixed resident/business foot traffic. Easier logistics from Macau-Zhuhai border — important for Mainland Chinese premium clients visiting Macau. Waxmeup nearby validates demand.</td>
                                  <td>More tourist-mixed than Taipa; harder to sustain premium positioning in NAPE's mid-market commercial mix</td>
                                  <td>4.2 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks The Venetian Macao (Cotai Strip)</td>
                                  <td>MOP 30,000 - 60,000</td>
                                  <td>Le SPA'tique and Wynn Salon confirm ultra-premium demand in casino zone. Wynn-level pricing possible (USD 200+/session). Hotel foot traffic is built-in.</td>
                                  <td>Extreme casino hotel rent; gaming downturn exposure; unpredictable foot traffic; best as Phase 2 hotel partnership (revenue-share) not standalone lease</td>
                                  <td>3.5 / 5 (Hotel Partnership Only)</td>
                              </tr>
             </tbody>""",

"dubai.html": """<tbody>
                              <tr class="highlight-row">
                                  <td>Starbucks Safa Park (Jumeirah Rd)</td>
                                  <td>AED 120,000 - 180,000 / yr</td>
                                  <td>Dubai's Western expat residential core. British, American, Australian expat families concentrated here. Ground-floor villa shopfront on Jumeirah Rd near Safa Park. Soft-water filtration is essential — Dubai tap water TDS 500–1200 ppm destroys colour. This is the most defensible USP in Dubai's overcrowded salon market.</td>
                                  <td>Villa shopfront leases are DEWA-metered — utility costs higher than commercial units; requires annual lease upfront per UAE commercial norms</td>
                                  <td>4.9 / 5 (Recommended)</td>
                              </tr>
                              <tr>
                                  <td>Starbucks The Beach JBR</td>
                                  <td>AED 180,000 - 280,000 / yr</td>
                                  <td>High-density expat residential towers. Strong walk-in from JBR beach promenade. Diverse European, Russian, Indian expat community. Multiple salons present — validates premium demand in zone.</td>
                                  <td>Very high rent; Marina has 30+ premium salons — most saturated premium zone in Dubai; must have exceptional soft-water + balayage differentiation to compete</td>
                                  <td>4.2 / 5</td>
                              </tr>
                              <tr>
                                  <td>Starbucks Boxpark (Al Wasl Rd)</td>
                                  <td>AED 100,000 - 160,000 / yr</td>
                                  <td>Old-established expat zone. Lower rent, loyal long-term Dubai resident clientele. Best for word-of-mouth growth among established expat community vs tourist-heavy Marina zone.</td>
                                  <td>Lower foot traffic than Jumeirah Rd or Marina; requires stronger referral and loyalty marketing; less Instagram-visible than beachfront alternatives</td>
                                  <td>4.1 / 5</td>
                              </tr>
             </tbody>""",
}

print("=== UPDATING LOCATION STUDY TABLES IN ALL SUBPAGES ===\n")
updated = 0
for fname, new_tbody in LOCATION_TABLES.items():
    path = os.path.join(WORKDIR, fname)
    if not os.path.exists(path):
        print(f"  MISSING: {fname}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Match the location study section's table tbody only
    pattern = r'(<section id="location-study".*?)(<tbody>.*?</tbody>)'
    replacement = r'\g<1>' + new_tbody
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    
    if count == 0:
        print(f"  [NO TABLE MATCH]: {fname}")
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  [Updated]: {fname}")
        updated += 1

print(f"\nDone. {updated} files updated.")
