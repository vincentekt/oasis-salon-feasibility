"""
update_candidates.py

Rewrites the `const candidates = [...]` block in every city HTML page
to reflect the underserved corridors identified by our market research.

Each candidate has:
  name, lat, lng, note, rent (USD/mo), catchment, premiumTargetPct, 
  competitorCapacity, airportTime
"""
import os, re

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

# ============================================================
# CANDIDATE DATA — Research-driven locations
# ============================================================

CANDIDATES = {

# ── VIETNAM ──────────────────────────────────────────────────────────────────

"hcmc.html": """[
            { 
                name: "Candidate A: Thao Dien - Xuan Thuy St (Primary)", 
                lat: 10.8048, lng: 106.7360, 
                note: "TOP PICK. Heart of Japanese/Korean/Western expat cluster. Ground-floor shophouse. Concept Coiffure and J-First within 500m — confirms premium demand. Rent USD 2,500–3,500/mo for 70 sqm.", 
                rent: 3000, catchment: 45000, premiumTargetPct: 38, competitorCapacity: 14000,
                airportTime: "30 mins from SGN"
            },
            { 
                name: "Candidate B: Thao Dien - Quoc Huong St", 
                lat: 10.8025, lng: 106.7350, 
                note: "Parallel to Xuan Thuy, slightly quieter lane with lower rent. Still within 300m of Thao Dien Square. Better parking. Same expat density.", 
                rent: 2400, catchment: 40000, premiumTargetPct: 35, competitorCapacity: 12000,
                airportTime: "30 mins from SGN"
            },
            { 
                name: "Candidate C: District 1 - Le Thanh Ton (Alt)", 
                lat: 10.7785, lng: 106.7055, 
                note: "Central D1 expat corridor near Sheraton/Caravelle. Vampire Hair (competitor) within 200m — validates premium demand. Higher rent, lower residential density than Thao Dien.", 
                rent: 4000, catchment: 30000, premiumTargetPct: 28, competitorCapacity: 18000,
                airportTime: "30 mins from SGN"
            }
        ]""",

"hanoi.html": """[
            { 
                name: "Candidate A: Tay Ho - Xuan Dieu Lakefront (Primary)", 
                lat: 21.0620, lng: 105.8285, 
                note: "TOP PICK. Diplomatic Quarter / Expat Central. Ground-floor commercial on Xuan Dieu with West Lake views. Maika Hair and KUKAI Hanoi within 400m. USD 1,800–2,800/mo for 70 sqm.", 
                rent: 2200, catchment: 35000, premiumTargetPct: 32, competitorCapacity: 10000,
                airportTime: "30 mins from HAN"
            },
            { 
                name: "Candidate B: Tay Ho - To Ngoc Van St", 
                lat: 21.0580, lng: 105.8250, 
                note: "Side street off Xuan Dieu with lower rent. Proximity to French School, UN building, and Korean Embassy compound — captive expat residential corridor.", 
                rent: 1700, catchment: 28000, premiumTargetPct: 28, competitorCapacity: 8000,
                airportTime: "30 mins from HAN"
            },
            { 
                name: "Candidate C: Hoan Kiem - Trang Tien St (Alt)", 
                lat: 21.0285, lng: 105.8522, 
                note: "High foot traffic tourist/business zone. Lower premium residential density than Tay Ho but accessible for business traveler clients. Higher competition from mid-tier local salons.", 
                rent: 2500, catchment: 22000, premiumTargetPct: 22, competitorCapacity: 12000,
                airportTime: "35 mins from HAN"
            }
        ]""",

"danang.html": """[
            { 
                name: "Candidate A: An Thuong Beach Area (Primary)", 
                lat: 16.0490, lng: 108.2450, 
                note: "TOP PICK. Digital nomad + Korean expat residential cluster. Ground-floor shophouse on An Thuong 1-6 network. Highest per-capita expat density in Da Nang. Rent USD 600–1,000/mo for 60 sqm.", 
                rent: 800, catchment: 18000, premiumTargetPct: 35, competitorCapacity: 4000,
                airportTime: "12 mins from DAD"
            },
            { 
                name: "Candidate B: My Khe Beach Rd (Non Nuoc Zone)", 
                lat: 16.0390, lng: 108.2500, 
                note: "Adjacent to resort strip. Strong tourist walk-in potential and resort-worker clientele. Lower Korean residential density than An Thuong but growing fast.", 
                rent: 650, catchment: 14000, premiumTargetPct: 28, competitorCapacity: 3000,
                airportTime: "15 mins from DAD"
            },
            { 
                name: "Candidate C: Hai Chau City Center", 
                lat: 16.0580, lng: 108.2210, 
                note: "City-center anchor. Lower expat density but captures business traveler and Vietnamese professional market. Access to larger commercial retail space.", 
                rent: 900, catchment: 25000, premiumTargetPct: 18, competitorCapacity: 6000,
                airportTime: "10 mins from DAD"
            }
        ]""",

"haiphong.html": """[
            { 
                name: "Candidate A: Minh Khai St near Deep C IP Gate (Primary)", 
                lat: 20.8380, lng: 106.7150, 
                note: "TOP PICK. 5-min drive from Deep C Industrial Zone gate (20,000+ Korean workers). Ground-floor shophouse with direct road access. Zero premium competition in this corridor. Rent USD 500–800/mo.", 
                rent: 650, catchment: 22000, premiumTargetPct: 45, competitorCapacity: 2000,
                airportTime: "15 mins from HPH"
            },
            { 
                name: "Candidate B: Vinhomes Imperia Commercial Strip", 
                lat: 20.8620, lng: 106.6700, 
                note: "Captive resident market within the Vinhomes gated community. Korean and Japanese families cluster in premium compounds. Slightly lower footfall than Minh Khai but guaranteed residential clientele.", 
                rent: 800, catchment: 18000, premiumTargetPct: 40, competitorCapacity: 2500,
                airportTime: "18 mins from HPH"
            },
            { 
                name: "Candidate C: Lach Tray St (City Center Alt)", 
                lat: 20.8430, lng: 106.6960, 
                note: "Central Haiphong commercial zone. HaLa and Nguyen Hung competition present — validates premium demand. Broader catchment but more competitive environment.", 
                rent: 700, catchment: 28000, premiumTargetPct: 22, competitorCapacity: 8000,
                airportTime: "15 mins from HPH"
            }
        ]""",

"binhduong.html": """[
            { 
                name: "Candidate A: VSIP I Commercial Zone (Primary)", 
                lat: 10.9300, lng: 106.7100, 
                note: "TOP PICK. Adjacent to VSIP I (50,000+ Korean/Japanese workers). Ground-floor commercial unit within walking distance of factory bus stop. Zero premium competition within 10km. Rent USD 500–750/mo.", 
                rent: 600, catchment: 55000, premiumTargetPct: 42, competitorCapacity: 1500,
                airportTime: "45 mins from SGN"
            },
            { 
                name: "Candidate B: Aeon Mall Binh Duong (Thuan An)", 
                lat: 10.9330, lng: 106.6970, 
                note: "Mall anchor near Aeon — guaranteed foot traffic from Korean family shopping visits. Multiple Korean restaurants confirm demand in zone. Higher mall rent but lower fit-out cost.", 
                rent: 900, catchment: 45000, premiumTargetPct: 35, competitorCapacity: 4000,
                airportTime: "45 mins from SGN"
            },
            { 
                name: "Candidate C: Thu Dau Mot - Chanh Nghia (Admin Hub)", 
                lat: 10.9780, lng: 106.6560, 
                note: "Provincial capital hub serving Binh Duong management class. Higher Vietnamese professional density — good for secondary growth phase after industrial expat base established.", 
                rent: 500, catchment: 32000, premiumTargetPct: 22, competitorCapacity: 5000,
                airportTime: "50 mins from SGN"
            }
        ]""",

"dongnai.html": """[
            { 
                name: "Candidate A: AMATA City Gate Commercial Row (Primary)", 
                lat: 10.9530, lng: 106.8400, 
                note: "TOP PICK. AMATA Industrial City main gate road. 40,000+ Korean/Japanese workers within 2km. Currently ZERO premium salon competition in entire zone. Rent USD 400–650/mo for 70 sqm.", 
                rent: 550, catchment: 48000, premiumTargetPct: 52, competitorCapacity: 500,
                airportTime: "60 mins from SGN"
            },
            { 
                name: "Candidate B: Loteco Zone Commercial Strip (Bien Hoa)", 
                lat: 10.9620, lng: 106.8520, 
                note: "Second major industrial zone in Bien Hoa. Captures Korean factory managers from Loteco 1 & 2 and Nhon Trach overflow. Korean restaurant cluster confirms expat demand exists.", 
                rent: 480, catchment: 35000, premiumTargetPct: 48, competitorCapacity: 500,
                airportTime: "60 mins from SGN"
            },
            { 
                name: "Candidate C: Bien Hoa City Center (Buu Long)", 
                lat: 10.9600, lng: 106.8250, 
                note: "Urban center fallback. More foot traffic from general public but lower Korean expat density. Better brand visibility for future Vietnamese professional market expansion.", 
                rent: 550, catchment: 40000, premiumTargetPct: 28, competitorCapacity: 3000,
                airportTime: "58 mins from SGN"
            }
        ]""",

# ── MALAYSIA ─────────────────────────────────────────────────────────────────

"kuala_lumpur.html": """[
            { 
                name: "Candidate A: Jalan Ampang (KLCC Corridor) (Primary)", 
                lat: 3.1580, lng: 101.7120, 
                note: "TOP PICK. Embassy Row / KLCC expat corridor. Ground-floor boutique on Jln Ampang near ING Tower / Wisma UOA. 25-min walk from all Bangsar alternatives — serves KL's highest-income diplomatic and corporate expat community. Rent MYR 12,000–18,000/mo.", 
                rent: 3500, catchment: 55000, premiumTargetPct: 45, competitorCapacity: 8000,
                airportTime: "45 mins from KUL"
            },
            { 
                name: "Candidate B: Bukit Ceylon (Expat Hill)", 
                lat: 3.1490, lng: 101.7080, 
                note: "Established expat residential enclave. Jln Mesui / Jln Ceylon ground-floor shophouse. Walking distance from Pavilion KL and KLCC. Lower rent than Ampang corridor but excellent expat concentration. Rent MYR 9,000–14,000/mo.", 
                rent: 2600, catchment: 42000, premiumTargetPct: 40, competitorCapacity: 7000,
                airportTime: "45 mins from KUL"
            },
            { 
                name: "Candidate C: Bangsar (Jalan Telawi Alt)", 
                lat: 3.1310, lng: 101.6710, 
                note: "Established premium zone where Number76 / Bottega / Aube all operate. Validates premium demand but highly saturated. Only viable as third-outlet expansion after KLCC flagship. Rent MYR 10,500–15,500/mo.", 
                rent: 3000, catchment: 35000, premiumTargetPct: 38, competitorCapacity: 18000,
                airportTime: "40 mins from KUL"
            }
        ]""",

"johor.html": """[
            { 
                name: "Candidate A: R&F Mall Skybridge Commercial (Primary)", 
                lat: 1.4608, lng: 103.7711, 
                note: "TOP PICK. Direct RTS Link skybridge connection. Singapore cross-border clients enter without street commute. Premium mall positioning. Rent MYR 5,000–8,000/mo. Singapore commuters budget SGD pricing (USD 65–120 range).", 
                rent: 1700, catchment: 50000, premiumTargetPct: 40, competitorCapacity: 6000,
                airportTime: "30 mins from JHB / 50 mins from SIN"
            },
            { 
                name: "Candidate B: Komtar JBCC (JB City Centre)", 
                lat: 1.4628, lng: 103.7645, 
                note: "Largest mall in JB city center. High foot traffic from Singapore day-trippers and JB residents. REDS Hair Salon confirmed presence validates premium hair demand. Ground floor with direct CIQ access.", 
                rent: 1400, catchment: 45000, premiumTargetPct: 35, competitorCapacity: 8000,
                airportTime: "30 mins from JHB"
            },
            { 
                name: "Candidate C: Medini Iskandar (Legoland / APAC Zone)", 
                lat: 1.4250, lng: 103.6290, 
                note: "Fast-growing business district with International School cluster. Expat families from IHH Healthcare, Pinewood Studios Malaysia cluster here. Lower current density but rapid growth trajectory.", 
                rent: 1100, catchment: 28000, premiumTargetPct: 30, competitorCapacity: 2000,
                airportTime: "35 mins from JHB"
            }
        ]""",

"penang.html": """[
            { 
                name: "Candidate A: Jalan Burma (Georgetown Premium Corridor) (Primary)", 
                lat: 5.4310, lng: 100.3150, 
                note: "TOP PICK. Georgetown's premium lifestyle corridor. Ground-floor shophouse between Gurney Drive and Jln Burma junction. A-Saloon and Wave Hair within 600m confirm premium demand. Heritage conservation area — boutique aesthetic naturally fits. Rent MYR 2,500–4,000/mo.", 
                rent: 800, catchment: 30000, premiumTargetPct: 32, competitorCapacity: 7000,
                airportTime: "25 mins from PEN"
            },
            { 
                name: "Candidate B: Gurney Drive (Upscale Mall-Adjacent)", 
                lat: 5.4370, lng: 100.3070, 
                note: "Adjacent to Gurney Paragon Mall — Penang's most premium retail address. High visibility to HNWI families. More expensive rent but premium positioning justified. Good parking access.", 
                rent: 1100, catchment: 35000, premiumTargetPct: 28, competitorCapacity: 8000,
                airportTime: "22 mins from PEN"
            },
            { 
                name: "Candidate C: Chulia St Heritage Lane (Boutique Alt)", 
                lat: 5.4180, lng: 100.3360, 
                note: "Heritage boutique zone. Instagram-worthy setting in Penang's most photographed street. Higher tourist traffic but lower premium residential density. Better for digital nomad and tourist walk-in market.", 
                rent: 600, catchment: 20000, premiumTargetPct: 25, competitorCapacity: 3000,
                airportTime: "30 mins from PEN"
            }
        ]""",

"sabah.html": """[
            { 
                name: "Candidate A: Jesselton Point Waterfront Retail (Primary)", 
                lat: 5.9925, lng: 116.0800, 
                note: "TOP PICK. KK's premier waterfront commercial zone. Ground-floor retail facing Jesselton Point Ferry Terminal — maximum tourist and expat visibility. Oil & gas executives from nearby Menara TH clusters here. Rent MYR 3,000–5,000/mo.", 
                rent: 900, catchment: 25000, premiumTargetPct: 40, competitorCapacity: 3000,
                airportTime: "20 mins from BKI"
            },
            { 
                name: "Candidate B: Jalan Gaya Commercial (City Center)", 
                lat: 5.9890, lng: 116.0745, 
                note: "KK's main commercial street. Ground-floor unit within walking distance of Suria Sabah and Oceanus Mall. Michael & Guys nearby confirms premium hair demand. Best balance of rent vs foot traffic.", 
                rent: 800, catchment: 22000, premiumTargetPct: 35, competitorCapacity: 4000,
                airportTime: "20 mins from BKI"
            },
            { 
                name: "Candidate C: Sutera Harbour Boulevard", 
                lat: 5.9820, lng: 116.0650, 
                note: "5-star resort corridor. Expat families from Shell, Murphy Oil, and resort management cluster in Sutera Harbour. Guaranteed HNWI clientele but lower total foot traffic and very high rent.", 
                rent: 1500, catchment: 15000, premiumTargetPct: 50, competitorCapacity: 1500,
                airportTime: "18 mins from BKI"
            }
        ]""",

"sarawak.html": """[
            { 
                name: "Candidate A: Tabuan Jaya Commercial Strip (Primary)", 
                lat: 1.5120, lng: 110.3750, 
                note: "TOP PICK. Shell Sarawak / Petronas expat residential hub. Ground-floor shophouse in Tabuan Jaya commercial area — 5-min drive from expatriate housing estates (Green Road, Stutong). Zero premium competition in zone. Rent MYR 2,000–3,500/mo.", 
                rent: 700, catchment: 20000, premiumTargetPct: 42, competitorCapacity: 2000,
                airportTime: "20 mins from KCH"
            },
            { 
                name: "Candidate B: Hikmah Exchange Commercial", 
                lat: 1.5275, lng: 110.3640, 
                note: "Sarawak's premium lifestyle hub. Gene's Work Hair Studio present — validates premium market. Central location accessible to entire Kuching metro. Emerging F&B and retail scene creates premium ambiance.", 
                rent: 900, catchment: 28000, premiumTargetPct: 35, competitorCapacity: 5000,
                airportTime: "18 mins from KCH"
            },
            { 
                name: "Candidate C: The Northbank (Waterfront)", 
                lat: 1.5585, lng: 110.3465, 
                note: "Kuching's revitalised waterfront precinct. Mane Society salon present — confirms premium hair interest in zone. Tourist and professional cross-traffic. Heritage boutique aesthetic advantage.", 
                rent: 750, catchment: 18000, premiumTargetPct: 28, competitorCapacity: 4000,
                airportTime: "20 mins from KCH"
            }
        ]""",

# ── TAIWAN ───────────────────────────────────────────────────────────────────

"taipei.html": """[
            { 
                name: "Candidate A: Da'an District - Yongkang St Laneway (Primary)", 
                lat: 25.0330, lng: 121.5305, 
                note: "TOP PICK. Da'an's premium lifestyle lane — Japan-quality boutique density. Ground-floor alleyway unit. Eddie Tham and SeeFu within 400m confirm premium demand. AIT (American Institute Taiwan) expat community nearby. Rent NTD 90,000–130,000/mo.", 
                rent: 3400, catchment: 40000, premiumTargetPct: 32, competitorCapacity: 12000,
                airportTime: "15 mins from TSA / 45 mins from TPE"
            },
            { 
                name: "Candidate B: Xinyi District - Songshou Rd Commercial", 
                lat: 25.0380, lng: 121.5645, 
                note: "Taipei's financial and luxury retail hub. Near Taipei 101 and W Hotel. TSMC and tech company international executives cluster in Xinyi luxury condos. Premium pricing power strongest here. Rent NTD 120,000–180,000/mo.", 
                rent: 4600, catchment: 35000, premiumTargetPct: 30, competitorCapacity: 10000,
                airportTime: "15 mins from TSA"
            },
            { 
                name: "Candidate C: Zhongshan - Chifeng St Design Quarter", 
                lat: 25.0520, lng: 121.5205, 
                note: "Creative design district with highest concentration of Taipei's fashion/art professional class. Japanese expat families cluster in Zhongshan near Minami Tokyo community areas. Lower rent than Xinyi. Rent NTD 70,000–100,000/mo.", 
                rent: 2600, catchment: 32000, premiumTargetPct: 28, competitorCapacity: 9000,
                airportTime: "10 mins from TSA"
            }
        ]""",

"taichung.html": """[
            { 
                name: "Candidate A: Qi-qi Zone - Shizheng North Rd (Primary)", 
                lat: 24.1610, lng: 120.6420, 
                note: "TOP PICK. Taichung's most affluent zone (Qi-qi / 7th Redevelopment Zone). Ground-floor boutique on Shizheng North Rd near W Taichung and Kimpton hotels. Japanese business families from Advantech/Giant cluster in nearby luxury towers. Rent NTD 80,000–120,000/mo.", 
                rent: 3000, catchment: 38000, premiumTargetPct: 35, competitorCapacity: 8000,
                airportTime: "30 mins from RMQ"
            },
            { 
                name: "Candidate B: Xitun - Taiwan Boulevard (ELF/VS area)", 
                lat: 24.1520, lng: 120.6505, 
                note: "Xitun district's commercial spine. ELF Salon and VS Hair present — confirms premium demand but also direct competition zone. Lower rent than Qi-qi but established premium foot traffic. Rent NTD 60,000–85,000/mo.", 
                rent: 2200, catchment: 32000, premiumTargetPct: 28, competitorCapacity: 12000,
                airportTime: "30 mins from RMQ"
            },
            { 
                name: "Candidate C: Huludun - Wenxin Rd (Northern Expansion)", 
                lat: 24.1850, lng: 120.6380, 
                note: "Emerging premium residential corridor north of Qi-qi. Lower current competition, growing family demographic. Best for second-outlet once Qi-qi flagship is established. Rent NTD 45,000–65,000/mo.", 
                rent: 1700, catchment: 25000, premiumTargetPct: 22, competitorCapacity: 4000,
                airportTime: "25 mins from RMQ"
            }
        ]""",

"kaohsiung.html": """[
            { 
                name: "Candidate A: Zuoying THSR Commercial Zone (Primary)", 
                lat: 22.6860, lng: 120.2980, 
                note: "TOP PICK. High-speed rail terminus commercial zone. First-mover position — zero premium salon in zone. THSR commuters from Taipei book appointments around train schedule. Japanese Foxconn/Innolux corporate housing in adjacent Zuoying towers. Rent NTD 60,000–80,000/mo.", 
                rent: 2000, catchment: 30000, premiumTargetPct: 35, competitorCapacity: 2000,
                airportTime: "15 mins from KHH"
            },
            { 
                name: "Candidate B: Lingya District - Sanduo Shopping (Round2 zone)", 
                lat: 22.6140, lng: 120.3040, 
                note: "Kaohsiung's premier shopping and lifestyle district. Round2 Hair Salon present — confirms premium demand. Higher competition but large total catchment. Best for capturing Kaohsiung's fashion-forward creative class. Rent NTD 70,000–95,000/mo.", 
                rent: 2500, catchment: 42000, premiumTargetPct: 28, competitorCapacity: 15000,
                airportTime: "15 mins from KHH"
            },
            { 
                name: "Candidate C: Xinyi District (Central Park Adjacent)", 
                lat: 22.6250, lng: 120.3150, 
                note: "Near Kaohsiung's Central Park MRT and cultural facilities. Growing premium residential catchment with access to Kaohsiung's Japanese business community. Lower competition than Lingya. Rent NTD 55,000–75,000/mo.", 
                rent: 1800, catchment: 28000, premiumTargetPct: 26, competitorCapacity: 6000,
                airportTime: "12 mins from KHH"
            }
        ]""",

"tainan.html": """[
            { 
                name: "Candidate A: Sinshih District - TSMC Housing Cluster (Primary)", 
                lat: 23.0750, lng: 120.3550, 
                note: "TOP PICK. Adjacent to TSMC Fab 18 and STSP company housing. TSMC international engineers (Japanese, US, European) live within 1km. Zero premium salon competition within 10km. Ground-floor commercial in Sinshih new development zone. Rent NTD 40,000–60,000/mo.", 
                rent: 1500, catchment: 22000, premiumTargetPct: 55, competitorCapacity: 500,
                airportTime: "35 mins from TNN / 50 mins from KHH"
            },
            { 
                name: "Candidate B: East District (NCKU / Shu-Lin Corridor)", 
                lat: 22.9940, lng: 120.2220, 
                note: "NCKU university zone with growing premium professional catchment. Tainan's young professional and academic community. Better established commercial street — more foot traffic than Sinshih but lower TSMC expat density. Rent NTD 32,000–48,000/mo.", 
                rent: 1200, catchment: 35000, premiumTargetPct: 28, competitorCapacity: 4000,
                airportTime: "15 mins from TNN"
            },
            { 
                name: "Candidate C: West Central - Zhongzheng Rd (City Center)", 
                lat: 22.9920, lng: 120.2025, 
                note: "Historic Tainan city center. Higher general foot traffic but lower premium density. Best for capturing Tainan's broader professional and tourist market as second phase of expansion. Rent NTD 35,000–52,000/mo.", 
                rent: 1300, catchment: 40000, premiumTargetPct: 20, competitorCapacity: 6000,
                airportTime: "20 mins from TNN"
            }
        ]""",

# ── AUSTRALIA ────────────────────────────────────────────────────────────────

"brisbane.html": """[
            { 
                name: "Candidate A: New Farm - Brunswick St (Primary)", 
                lat: -27.4605, lng: 153.0405, 
                note: "TOP PICK. Brisbane's highest-income inner-east residential corridor (median house AUD 2.1M+). Ground-floor boutique on Brunswick St New Farm. Zero premium colour boutique within 15-min walk. UV-damage + Asian hair specialist gap confirmed by research. Rent AUD 3,500–5,500/mo.", 
                rent: 2800, catchment: 35000, premiumTargetPct: 38, competitorCapacity: 5000,
                airportTime: "20 mins from BNE"
            },
            { 
                name: "Candidate B: Fortitude Valley - James St Precinct", 
                lat: -27.4585, lng: 153.0365, 
                note: "Adjacent to James St luxury retail (Camilla, Zimmermann). Growing Korean/Japanese community in Valley. Boutique hair studio density lower than Paddington — white space for premium colour.", 
                rent: 3200, catchment: 40000, premiumTargetPct: 32, competitorCapacity: 4000,
                airportTime: "20 mins from BNE"
            },
            { 
                name: "Candidate C: Paddington - Given Tce (Sol Hair Zone)", 
                lat: -27.4620, lng: 152.9990, 
                note: "Sol Hair (main competitor) at Given Tce confirms premium demand. Entry here means direct competition with entrenched local brand — only viable if Asian hair specialisation clearly differentiates. High foot traffic, moderate rent.", 
                rent: 2600, catchment: 30000, premiumTargetPct: 30, competitorCapacity: 14000,
                airportTime: "22 mins from BNE"
            }
        ]""",

"sydney.html": """[
            { 
                name: "Candidate A: Newtown - King St Ground Floor (Primary)", 
                lat: -33.8965, lng: 151.1785, 
                note: "TOP PICK. Sydney's most underserved premium corridor. Young professional dual-income households (25–45). Nearest premium boutique is 15-min commute to Surry Hills. Zero premium colour boutique on King St. UV + transparent pricing gap. Rent AUD 4,000–6,500/mo.", 
                rent: 3200, catchment: 42000, premiumTargetPct: 35, competitorCapacity: 3000,
                airportTime: "22 mins from SYD"
            },
            { 
                name: "Candidate B: Glebe - Glebe Point Rd", 
                lat: -33.8765, lng: 151.1870, 
                note: "Adjacent to Newtown but with higher residential density and less foot traffic competition. University of Sydney proximity creates young professional catchment. Same income profile as Newtown, slightly lower rent.", 
                rent: 2800, catchment: 35000, premiumTargetPct: 32, competitorCapacity: 2500,
                airportTime: "22 mins from SYD"
            },
            { 
                name: "Candidate C: Surry Hills - Crown St (Competition Zone)", 
                lat: -33.8865, lng: 151.2115, 
                note: "RAW Anthony Nader, Flock, Wakefields within 300m — confirms premium demand but highly competitive. Only viable if transparent all-inclusive pricing model creates clear differentiation from add-on fee competitors.", 
                rent: 4500, catchment: 50000, premiumTargetPct: 38, competitorCapacity: 22000,
                airportTime: "20 mins from SYD"
            }
        ]""",

"melbourne.html": """[
            { 
                name: "Candidate A: South Yarra - Chapel St Ground Floor (Primary)", 
                lat: -37.8385, lng: 144.9925, 
                note: "TOP PICK. Melbourne's premier lifestyle corridor. Ground-floor boutique on Chapel St between Toorak Rd and Commercial Rd. Highest per-capita luxury spend in Melbourne. Japanese expat community concentrated in surrounding Prahran/Toorak. Rent AUD 4,500–7,000/mo.", 
                rent: 3500, catchment: 45000, premiumTargetPct: 35, competitorCapacity: 12000,
                airportTime: "30 mins from MEL"
            },
            { 
                name: "Candidate B: Fitzroy - Brunswick St Boutique", 
                lat: -37.8015, lng: 144.9795, 
                note: "Melbourne's creative professional zone. Fashion-forward demographic with high WTP for specialist creative colour (balayage, vivid, copper). Lower rent than Chapel St. Growing Korean community in surrounding Carlton.", 
                rent: 2800, catchment: 38000, premiumTargetPct: 30, competitorCapacity: 8000,
                airportTime: "30 mins from MEL"
            },
            { 
                name: "Candidate C: CBD - Collins St Ground Floor", 
                lat: -37.8145, lng: 144.9635, 
                note: "Melbourne's corporate financial spine. After-work appointments from CBD professionals. Access to largest total catchment. Highest rent but strongest lunchtime/after-work booking density. Best for corporate membership program.", 
                rent: 5500, catchment: 60000, premiumTargetPct: 28, competitorCapacity: 18000,
                airportTime: "30 mins from MEL"
            }
        ]""",

"perth.html": """[
            { 
                name: "Candidate A: Subiaco - Rokeby Rd (Primary)", 
                lat: -31.9475, lng: 115.8265, 
                note: "TOP PICK. Perth's premium inner-western suburb. High FIFO worker family density (mining/resources executives on 2-weeks-on/off cycles). Ground-floor shophouse on Rokeby Rd retail strip. UV-protection angle strong given Perth's extreme UV index (UV 11+ in summer). Rent AUD 2,500–4,000/mo.", 
                rent: 2000, catchment: 28000, premiumTargetPct: 32, competitorCapacity: 6000,
                airportTime: "22 mins from PER"
            },
            { 
                name: "Candidate B: Claremont - St Quentin Ave", 
                lat: -31.9805, lng: 115.7830, 
                note: "Old-money western suburbs. Highest household income in Perth metro. Premium boutique aesthetic fits heritage streetscape. Less foot traffic than Subiaco but HNWI appointment-only clientele — matches premium model.", 
                rent: 1800, catchment: 18000, premiumTargetPct: 40, competitorCapacity: 4000,
                airportTime: "25 mins from PER"
            },
            { 
                name: "Candidate C: Cottesloe - Marine Pde Coastal", 
                lat: -31.9965, lng: 115.7595, 
                note: "Coastal boutique positioning. Beach lifestyle + UV damage angle is strongest here. Tourist season (Oct–Apr) boosts volume. Lowest year-round footfall consistency of three candidates.", 
                rent: 1600, catchment: 15000, premiumTargetPct: 35, competitorCapacity: 2500,
                airportTime: "30 mins from PER"
            }
        ]""",

# ── JAPAN ─────────────────────────────────────────────────────────────────────

"fukuoka.html": """[
            { 
                name: "Candidate A: Daimyo - Central Lane (Primary)", 
                lat: 33.5875, lng: 130.3955, 
                note: "TOP PICK. Fukuoka's most fashionable boutique district. Ground-floor commercial unit on Daimyo's main shopping lane. saco japan flagship and TONI&GUY Tenjin within 600m — confirms premium demand. Korean expat community of 8,000+ nearby in Hakata/Tenjin. Rent JPY 150,000–250,000/mo.", 
                rent: 1600, catchment: 35000, premiumTargetPct: 28, competitorCapacity: 12000,
                airportTime: "15 mins from FUK"
            },
            { 
                name: "Candidate B: Tenjin - Watanabe-dori", 
                lat: 33.5898, lng: 130.3985, 
                note: "Tenjin's main commercial boulevard. TONI&GUY and Shiki Hair immediately adjacent — highest premium footfall in Fukuoka. Entry here requires differentiation on vivid/creative colour vs. Japanese natural-tone consensus. High rent but maximum visibility.", 
                rent: 2200, catchment: 50000, premiumTargetPct: 25, competitorCapacity: 20000,
                airportTime: "15 mins from FUK"
            },
            { 
                name: "Candidate C: Imaizumi - Boutique Alleyway", 
                lat: 33.5855, lng: 130.3995, 
                note: "Trendy alleyway boutique zone between Tenjin and Daimyo. Lower rent, creative/art professional demographic, high Instagram potential for fashion colour portfolio. Korean expat community adjacent in Sumiyoshi.", 
                rent: 1100, catchment: 22000, premiumTargetPct: 22, competitorCapacity: 6000,
                airportTime: "15 mins from FUK"
            }
        ]""",

"okinawa.html": """[
            { 
                name: "Candidate A: Omoromachi / Shin-toshin (Primary)", 
                lat: 26.2230, lng: 127.6960, 
                note: "TOP PICK. Naha's civilian expat core — entirely unserved by English/Korean-friendly premium salons. Ground-floor commercial near DFS Galleria and Naha Shin-toshin. Korean tourists (200,000+/year) pass through this zone. BLOOM/Borjan are 30+ min north in Chatan — this is a true whitespace. Rent JPY 100,000–180,000/mo.", 
                rent: 1100, catchment: 28000, premiumTargetPct: 52, competitorCapacity: 1500,
                airportTime: "15 mins from OKA"
            },
            { 
                name: "Candidate B: Kumoji Business Center", 
                lat: 26.2160, lng: 127.6815, 
                note: "Naha central business district. Mix of Japanese professionals, Ryukyu University community, and Korean tourist hotels. Good balance of resident and tourist traffic. Lower rent than Omoromachi premium strip.", 
                rent: 800, catchment: 22000, premiumTargetPct: 35, competitorCapacity: 2000,
                airportTime: "15 mins from OKA"
            },
            { 
                name: "Candidate C: Kokusai-dori (Tourist Strip Alt)", 
                lat: 26.2155, lng: 127.6875, 
                note: "Okinawa's main tourist shopping street. Maximum Korean tourist walk-in volume. Risk of being perceived as tourist-trap rather than premium boutique. Best for pop-up testing Korean tourist demand before permanent commitment.", 
                rent: 1400, catchment: 35000, premiumTargetPct: 30, competitorCapacity: 5000,
                airportTime: "15 mins from OKA"
            }
        ]""",

# ── SOUTH KOREA ────────────────────────────────────────────────────────────────

"busan.html": """[
            { 
                name: "Candidate A: Haeundae Marine City (Primary)", 
                lat: 35.1580, lng: 129.1440, 
                note: "TOP PICK. Marine City luxury residential towers. HNWI Busan residents in sky-high condos (Zenith, I-Park Marine). Happynian salon (competitor) is in Seomyeon — 20-min drive away. Marine City currently has no premium boutique colour studio. Rent KRW 2.5M–4M/mo.", 
                rent: 2200, catchment: 35000, premiumTargetPct: 40, competitorCapacity: 3000,
                airportTime: "30 mins from PUS"
            },
            { 
                name: "Candidate B: Centum City (BEXCO Area)", 
                lat: 35.1700, lng: 129.1320, 
                note: "Busan's international business hub. BEXCO convention centre creates regular influx of Korean and international business visitors. Adjacent Shinsegae Centum (world's largest department store) confirms premium retail demand.", 
                rent: 2800, catchment: 45000, premiumTargetPct: 32, competitorCapacity: 8000,
                airportTime: "28 mins from PUS"
            },
            { 
                name: "Candidate C: Haeundae Beach Front", 
                lat: 35.1600, lng: 129.1640, 
                note: "Beach Road tourism strip. Strong summer volume but seasonality risk (peak Jun–Aug, quiet Oct–Feb). Best for high-season volume boost after Marine City flagship established.", 
                rent: 2500, catchment: 38000, premiumTargetPct: 28, competitorCapacity: 6000,
                airportTime: "30 mins from PUS"
            }
        ]""",

# ── OTHER APAC ─────────────────────────────────────────────────────────────────

"singapore.html": """[
            { 
                name: "Candidate A: Holland Village - Jalan Merah Saga (Primary)", 
                lat: 1.3110, lng: 103.7960, 
                note: "TOP PICK. Holland Village's expat residential core — unserved by a premium colour boutique at this price level. Chez Vous HideAway is in Scotts (2km), Love Hair in Jiak Chuan (3km). Ground-floor shophouse at Holland V fringe. Rent SGD 7,000–11,000/mo.", 
                rent: 5500, catchment: 45000, premiumTargetPct: 42, competitorCapacity: 8000,
                airportTime: "25 mins from SIN"
            },
            { 
                name: "Candidate B: Tanglin - Cluny Rd / Dempsey Hill Adjacent", 
                lat: 1.3080, lng: 103.8180, 
                note: "Dempsey Hill boutique zone. Blonde Boudoir operates here — validates premium demand. Tanglin corridor has highest per-household income in Singapore. Ground-floor shophouse near American Club. Premium positioning strongest here but smaller total catchment.", 
                rent: 6500, catchment: 30000, premiumTargetPct: 48, competitorCapacity: 6000,
                airportTime: "22 mins from SIN"
            },
            { 
                name: "Candidate C: Tanjong Pagar (CBD-Adjacent Alt)", 
                lat: 1.2785, lng: 103.8430, 
                note: "Growing CBD-adjacent expat zone. Luxury condo density (Altez, The Pinnacle@Duxton vicinity). Love Hair nearby validates demand. Best for after-work appointments from CBD professionals. Higher corporate membership potential.", 
                rent: 7000, catchment: 40000, premiumTargetPct: 35, competitorCapacity: 12000,
                airportTime: "20 mins from SIN"
            }
        ]""",

"bangkok.html": """[
            { 
                name: "Candidate A: Thonglor Soi 10 Ground-Floor (Primary)", 
                lat: 13.7340, lng: 100.5820, 
                note: "TOP PICK. Thonglor is the epicentre of Bangkok's Japanese and Western expat community. The London Hair and Yumoto are 400-600m away — confirms premium demand and establishes our soft-water filtration USP against competitors on same tap water system. Ground-floor suite, high visibility. Rent USD 4,000–6,000/mo.", 
                rent: 5000, catchment: 45000, premiumTargetPct: 38, competitorCapacity: 14000,
                airportTime: "30 mins from BKK / 35 mins from DMK"
            },
            { 
                name: "Candidate B: Ekkamai Soi 4 (Expat Alt)", 
                lat: 13.7260, lng: 100.5840, 
                note: "Large expat residential corridor adjacent to Thonglor. CYAN Salon is here — validates premium colour demand. Lower rent than Thonglor main but same demographic catchment. Better parking for suburban expat families.", 
                rent: 3800, catchment: 38000, premiumTargetPct: 32, competitorCapacity: 10000,
                airportTime: "32 mins from BKK / 37 mins from DMK"
            },
            { 
                name: "Candidate C: Phrom Phong Soi 39 (Ultra-Premium Alt)", 
                lat: 13.7320, lng: 100.5720, 
                note: "Exclusive condo retail lane near EmQuartier. Highest per-capita income of any Bangkok expat zone. Micha & Justin and Japanese hair salons operate nearby. Extremely limited availability and highest rent — reserve for second outlet.", 
                rent: 6500, catchment: 40000, premiumTargetPct: 35, competitorCapacity: 16000,
                airportTime: "35 mins from BKK / 40 mins from DMK"
            }
        ]""",

"hongkong.html": """[
            { 
                name: "Candidate A: Causeway Bay - Lockhart Rd Ground Floor (Primary)", 
                lat: 22.2808, lng: 114.1839, 
                note: "TOP PICK. Causeway Bay is HK's most accessible premium retail zone. Ground-floor unit on Lockhart Rd. Bruneblonde and Love Hair both operate in the district — high premium colour demand confirmed. HKD 60,000–100,000/mo rent. Soft-water filtration is a genuine USP vs all Causeway Bay competitors on same tap water.", 
                rent: 8500, catchment: 50000, premiumTargetPct: 40, competitorCapacity: 18000,
                airportTime: "40 mins from HKG"
            },
            { 
                name: "Candidate B: Central - Wyndham St / SOHO", 
                lat: 22.2815, lng: 114.1555, 
                note: "HK's financial and expat social hub. Kimrobinson flagship nearby — validates ultra-premium demand. Ground-floor on Wyndham or Peel St. After-work and lunch appointments from IFC/Chater House financial professionals. Highest average ticket potential.", 
                rent: 11000, catchment: 42000, premiumTargetPct: 45, competitorCapacity: 20000,
                airportTime: "40 mins from HKG"
            }
        ]""",

"macau.html": """[
            { 
                name: "Candidate A: Taipa Village Commercial Row (Primary)", 
                lat: 22.1580, lng: 113.5580, 
                note: "TOP PICK. Taipa is Macau's preferred residential zone for casino management expats. Ground-floor shophouse in Taipa Village commercial area. Hair Cloud (competitor) presence confirms premium demand. Consistent non-gaming clientele unlike Cotai Strip. Rent MOP 12,000–20,000/mo.", 
                rent: 1800, catchment: 25000, premiumTargetPct: 42, competitorCapacity: 5000,
                airportTime: "15 mins from MFM"
            },
            { 
                name: "Candidate B: NAPE Commercial District", 
                lat: 22.1885, lng: 113.5510, 
                note: "Macau Peninsula's modern commercial zone. Higher foot traffic from mixed resident/business crowd. Waxmeup operates nearby. Easier logistics from Macau-Zhuhai border crossing — important for Mainland Chinese premium clients visiting Macau.", 
                rent: 1500, catchment: 30000, premiumTargetPct: 32, competitorCapacity: 6000,
                airportTime: "15 mins from MFM"
            },
            { 
                name: "Candidate C: Cotai Strip Hotel Retail (Casino Zone)", 
                lat: 22.1450, lng: 113.5700, 
                note: "Le SPA'tique / Wynn Salon confirm demand in casino zone. Wynn-level pricing possible (USD 200+). However, casino retail rent is extreme and client flow unpredictable during gaming downturns. Viable as Phase 2 hotel partnership rather than standalone lease.", 
                rent: 4500, catchment: 20000, premiumTargetPct: 35, competitorCapacity: 12000,
                airportTime: "15 mins from MFM"
            }
        ]""",

"dubai.html": """[
            { 
                name: "Candidate A: Jumeirah 1 / Safa Park Corridor (Primary)", 
                lat: 25.2100, lng: 55.2400, 
                note: "TOP PICK. Dubai's Western expat residential core. Ground-floor villa shopfront on Jumeirah Rd near Safa Park. British, American, Australian expat families concentrated here. Soft-water filtration is essential — Dubai tap water TDS 500–1200 ppm destroys colour. Rent AED 120,000–180,000/yr.", 
                rent: 3500, catchment: 45000, premiumTargetPct: 48, competitorCapacity: 10000,
                airportTime: "15 mins from DXB"
            },
            { 
                name: "Candidate B: Dubai Marina / JBR Promenade", 
                lat: 25.0780, lng: 55.1350, 
                note: "High-density expat residential towers. Strong walk-in traffic from JBR beach promenade. Diverse European, Russian, Indian expat community. Multiple salons present but soft-water filtration advantage meaningful in this hard-water zone.", 
                rent: 4000, catchment: 55000, premiumTargetPct: 38, competitorCapacity: 14000,
                airportTime: "25 mins from DXB"
            },
            { 
                name: "Candidate C: Al Wasl Rd (Traditional Expat Residential)", 
                lat: 25.1850, lng: 55.2200, 
                note: "Old-established expat zone. Lower rent, loyal residential clientele. Best for word-of-mouth growth among long-term Dubai residents vs. tourist-heavy Marina zone.", 
                rent: 2800, catchment: 35000, premiumTargetPct: 40, competitorCapacity: 8000,
                airportTime: "18 mins from DXB"
            }
        ]"""
}

# ============================================================
# Apply updates
# ============================================================
print("=== UPDATING CANDIDATE LOCATIONS IN ALL SUBPAGES ===\n")
for fname, new_candidates_block in CANDIDATES.items():
    path = os.path.join(WORKDIR, fname)
    if not os.path.exists(path):
        print(f"  MISSING: {fname}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Match and replace the candidates block
    pattern = r'(const candidates\s*=\s*)\[.*?\](;)'
    replacement = r'\g<1>' + new_candidates_block + r'\g<2>'
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    
    if count == 0:
        print(f"  [NO MATCH]: {fname}")
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  [Updated]: {fname}")

print("\nDone.")
