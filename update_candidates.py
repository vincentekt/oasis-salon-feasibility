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
                name: "Candidate A: Thao Dien - Xuan Thuy St (Concept Coiffure)", 
                lat: 10.8045, lng: 106.7375, 
                note: "Pinned to Concept Coiffure for road reference. TOP PICK. Heart of Japanese/Korean/Western expat cluster. Ground-floor shophouse. Concept Coiffure and J-First within 500m — confirms premium demand. Rent USD 2,500–3,500/mo for 70 sqm.", 
                rent: 3000, catchment: 45000, premiumTargetPct: 38, competitorCapacity: 14000,
                airportTime: "30 mins from SGN"
            },
            { 
                name: "Candidate B: Thao Dien - Quoc Huong St (Masteri T5)", 
                lat: 10.804, lng: 106.745, 
                note: "Pinned to Masteri Thao Dien T5 for road reference. Parallel to Xuan Thuy, slightly quieter lane with lower rent. Still within 300m of Thao Dien Square. Better parking. Same expat density.", 
                rent: 2400, catchment: 40000, premiumTargetPct: 35, competitorCapacity: 12000,
                airportTime: "30 mins from SGN"
            },
            { 
                name: "Candidate C: District 1 - Le Thanh Ton St (Sheraton Saigon)", 
                lat: 10.7745, lng: 106.7032, 
                note: "Pinned to Sheraton Saigon Hotel for road reference. Central D1 expat corridor near Sheraton/Caravelle. Vampire Hair (competitor) within 200m — validates premium demand. Higher rent, lower residential density than Thao Dien.", 
                rent: 4000, catchment: 30000, premiumTargetPct: 28, competitorCapacity: 18000,
                airportTime: "30 mins from SGN"
            }
        ]""",

"hanoi.html": """[
            { 
                name: "Candidate A: Tay Ho - Xuan Dieu Lakefront (Syrena Center)", 
                lat: 21.0625, lng: 105.828, 
                note: "Pinned to Syrena Shopping Center for road reference. TOP PICK. Diplomatic Quarter / Expat Central. Ground-floor commercial on Xuan Dieu with West Lake views. Maika Hair and KUKAI Hanoi within 400m. USD 1,800–2,800/mo for 70 sqm.", 
                rent: 2200, catchment: 35000, premiumTargetPct: 32, competitorCapacity: 10000,
                airportTime: "30 mins from HAN"
            },
            { 
                name: "Candidate B: Tay Ho - To Ngoc Van St (To Ngoc Van Villas)", 
                lat: 21.0585, lng: 105.8252, 
                note: "Pinned to To Ngoc Van Villas for road reference. Side street off Xuan Dieu with lower rent. Proximity to French School, UN building, and Korean Embassy compound — captive expat residential corridor.", 
                rent: 1700, catchment: 28000, premiumTargetPct: 28, competitorCapacity: 8000,
                airportTime: "30 mins from HAN"
            },
            { 
                name: "Candidate C: Hoan Kiem - Trang Tien St (Trang Tien Plaza)", 
                lat: 21.0252, lng: 105.8525, 
                note: "Pinned to Trang Tien Plaza for road reference. High foot traffic tourist/business zone. Lower premium residential density than Tay Ho but accessible for business traveler clients. Higher competition from mid-tier local salons.", 
                rent: 2500, catchment: 22000, premiumTargetPct: 22, competitorCapacity: 12000,
                airportTime: "35 mins from HAN"
            }
        ]""",

"danang.html": """[
            { 
                name: "Candidate A: An Thuong Beach Area (Holiday Beach Hotel)", 
                lat: 16.0485, lng: 108.2455, 
                note: "Pinned to Holiday Beach Danang Hotel for road reference. TOP PICK. Digital nomad + Korean expat residential cluster. Ground-floor shophouse on An Thuong 1-6 network. Highest per-capita expat density in Da Nang. Rent USD 600–1,000/mo for 60 sqm.", 
                rent: 800, catchment: 18000, premiumTargetPct: 35, competitorCapacity: 4000,
                airportTime: "12 mins from DAD"
            },
            { 
                name: "Candidate B: My Khe Beach Rd (TMS Hotel Beach)", 
                lat: 16.0416, lng: 108.2483, 
                note: "Pinned to TMS Hotel Da Nang Beach for road reference. Adjacent to resort strip. Strong tourist walk-in potential and resort-worker clientele. Lower Korean residential density than An Thuong but growing fast.", 
                rent: 650, catchment: 14000, premiumTargetPct: 28, competitorCapacity: 3000,
                airportTime: "15 mins from DAD"
            },
            { 
                name: "Candidate C: Hai Chau City Center (Indochina Riverside Mall)", 
                lat: 16.061, lng: 108.223, 
                note: "Pinned to Indochina Riverside Mall for road reference. City-center anchor. Lower expat density but captures business traveler and Vietnamese professional market. Access to larger commercial retail space.", 
                rent: 900, catchment: 25000, premiumTargetPct: 18, competitorCapacity: 6000,
                airportTime: "10 mins from DAD"
            }
        ]""",

"haiphong.html": """[
            { 
                name: "Candidate A: Minh Khai St near Deep C IP Gate (Museum area)", 
                lat: 20.841, lng: 106.683, 
                note: "Pinned to Haiphong Museum for road reference. TOP PICK. 5-min drive from Deep C Industrial Zone gate (20,000+ Korean workers). Ground-floor shophouse with direct road access. Zero premium competition in this corridor. Rent USD 500–800/mo.", 
                rent: 650, catchment: 22000, premiumTargetPct: 45, competitorCapacity: 2000,
                airportTime: "15 mins from HPH"
            },
            { 
                name: "Candidate B: Vinhomes Imperia Commercial Strip (Vincom Plaza)", 
                lat: 20.8625, lng: 106.6705, 
                note: "Pinned to Vincom Plaza Imperia for road reference. Captive resident market within the Vinhomes gated community. Korean and Japanese families cluster in premium compounds. Slightly lower footfall than Minh Khai but guaranteed residential clientele.", 
                rent: 800, catchment: 18000, premiumTargetPct: 40, competitorCapacity: 2500,
                airportTime: "18 mins from HPH"
            },
            { 
                name: "Candidate C: Lach Tray St (Lach Tray Stadium)", 
                lat: 20.8432, lng: 106.6965, 
                note: "Pinned to Lach Tray Stadium for road reference. Central Haiphong commercial zone. HaLa and Nguyen Hung competition present — validates premium demand. Broader catchment but more competitive environment.", 
                rent: 700, catchment: 28000, premiumTargetPct: 22, competitorCapacity: 8000,
                airportTime: "15 mins from HPH"
            }
        ]""",

"binhduong.html": """[
            { 
                name: "Candidate A: VSIP I Commercial Zone (Canary Plaza)", 
                lat: 10.9305, lng: 106.7115, 
                note: "Pinned to Canary Plaza for road reference. TOP PICK. Adjacent to VSIP I (50,000+ Korean/Japanese workers). Ground-floor commercial unit within walking distance of factory bus stop. Zero premium competition within 10km. Rent USD 500–750/mo.", 
                rent: 600, catchment: 55000, premiumTargetPct: 42, competitorCapacity: 1500,
                airportTime: "45 mins from SGN"
            },
            { 
                name: "Candidate B: Aeon Mall Binh Duong (Aeon Mall Canopy)", 
                lat: 10.9332, lng: 106.6978, 
                note: "Pinned to Aeon Mall Binh Duong for road reference. Mall anchor near Aeon — guaranteed foot traffic from Korean family shopping visits. Multiple Korean restaurants confirm demand in zone. Higher mall rent but lower fit-out cost.", 
                rent: 900, catchment: 45000, premiumTargetPct: 35, competitorCapacity: 4000,
                airportTime: "45 mins from SGN"
            },
            { 
                name: "Candidate C: Thu Dau Mot - Chanh Nghia (Becamex Tower)", 
                lat: 10.9778, lng: 106.6568, 
                note: "Pinned to Becamex Tower for road reference. Provincial capital hub serving Binh Duong management class. Higher Vietnamese professional density — good for secondary growth phase after industrial expat base established.", 
                rent: 500, catchment: 32000, premiumTargetPct: 22, competitorCapacity: 5000,
                airportTime: "50 mins from SGN"
            }
        ]""",

"dongnai.html": """[
            { 
                name: "Candidate A: AMATA City Gate Commercial Row (Highlands Coffee)", 
                lat: 10.9535, lng: 106.8405, 
                note: "Pinned to Highlands Coffee Amata Gate for road reference. TOP PICK. AMATA Industrial City main gate road. 40,000+ Korean/Japanese workers within 2km. Currently ZERO premium salon competition in entire zone. Rent USD 400–650/mo for 70 sqm.", 
                rent: 550, catchment: 48000, premiumTargetPct: 52, competitorCapacity: 500,
                airportTime: "60 mins from SGN"
            },
            { 
                name: "Candidate B: Loteco Zone Commercial Strip (Loteco Office Gate)", 
                lat: 10.9615, lng: 106.8515, 
                note: "Pinned to Loteco Gate Office for road reference. Second major industrial zone in Bien Hoa. Captures Korean factory managers from Loteco 1 & 2 and Nhon Trach overflow. Korean restaurant cluster confirms expat demand exists.", 
                rent: 480, catchment: 35000, premiumTargetPct: 48, competitorCapacity: 500,
                airportTime: "60 mins from SGN"
            },
            { 
                name: "Candidate C: Vo Thi Sau Commercial Corridor (Pegasus Plaza)", 
                lat: 10.9495, lng: 106.8328, 
                note: "Pinned to The Pegasus Plaza for road reference. Biên Hòa's premier lifestyle and dining high-street. High local wealthy foot traffic and Korean restaurant clusters, but higher rent and active local salon competition.", 
                rent: 700, catchment: 45000, premiumTargetPct: 35, competitorCapacity: 2500,
                airportTime: "55 mins from SGN"
            }
        ]""",

# ── MALAYSIA ─────────────────────────────────────────────────────────────────

"kuala_lumpur.html": """[
            { 
                name: "Candidate A: Jalan Ampang - KLCC Corridor (Suria KLCC)", 
                lat: 3.1578, lng: 101.7118, 
                note: "Pinned to Suria KLCC for road reference. TOP PICK. Embassy Row / KLCC expat corridor. Ground-floor boutique on Jln Ampang near ING Tower / Wisma UOA. 25-min walk from all Bangsar alternatives — serves KL's highest-income diplomatic and corporate expat community. Rent MYR 12,000–18,000/mo.", 
                rent: 3500, catchment: 55000, premiumTargetPct: 45, competitorCapacity: 8000,
                airportTime: "45 mins from KUL"
            },
            { 
                name: "Candidate B: Bukit Ceylon - Expat Hill (Lanson Place)", 
                lat: 3.1495, lng: 101.7075, 
                note: "Pinned to Lanson Place Bukit Ceylon for road reference. Established expat residential enclave. Jln Mesui / Jln Ceylon ground-floor shophouse. Walking distance from Pavilion KL and KLCC. Lower rent than Ampang corridor but excellent expat concentration. Rent MYR 9,000–14,000/mo.", 
                rent: 2600, catchment: 42000, premiumTargetPct: 40, competitorCapacity: 7000,
                airportTime: "45 mins from KUL"
            },
            { 
                name: "Candidate C: Bangsar - Jalan Telawi Alt (Bangsar Village II)", 
                lat: 3.1305, lng: 101.6715, 
                note: "Pinned to Bangsar Village II for road reference. Established premium zone where Number76 / Bottega / Aube all operate. Validates premium demand but highly saturated. Only viable as third-outlet expansion after KLCC flagship. Rent MYR 10,500–15,500/mo.", 
                rent: 3000, catchment: 35000, premiumTargetPct: 38, competitorCapacity: 18000,
                airportTime: "40 mins from KUL"
            }
        ]""",

"johor.html": """[
            { 
                name: "Candidate A: R&F Mall Skybridge Commercial (R&F Mall)", 
                lat: 1.4608, lng: 103.7711, 
                note: "Pinned to R&F Mall for road reference. TOP PICK. Direct RTS Link skybridge connection. Singapore cross-border clients enter without street commute. Premium mall positioning. Rent MYR 5,000–8,000/mo. Singapore commuters budget SGD pricing (USD 65–120 range).", 
                rent: 1700, catchment: 50000, premiumTargetPct: 40, competitorCapacity: 6000,
                airportTime: "30 mins from JHB / 50 mins from SIN"
            },
            { 
                name: "Candidate B: Komtar JBCC (Komtar JBCC)", 
                lat: 1.4628, lng: 103.7645, 
                note: "Pinned to Komtar JBCC for road reference. Largest mall in JB city center. High foot traffic from Singapore day-trippers and JB residents. REDS Hair Salon confirmed presence validates premium hair demand. Ground floor with direct CIQ access.", 
                rent: 1400, catchment: 45000, premiumTargetPct: 35, competitorCapacity: 8000,
                airportTime: "30 mins from JHB"
            },
            { 
                name: "Candidate C: Medini Iskandar (Mall of Medini)", 
                lat: 1.4285, lng: 103.633, 
                note: "Pinned to Mall of Medini for road reference. Fast-growing business district with International School cluster. Expat families from IHH Healthcare, Pinewood Studios Malaysia cluster here. Lower current density but rapid growth trajectory.", 
                rent: 1100, catchment: 28000, premiumTargetPct: 30, competitorCapacity: 2000,
                airportTime: "35 mins from JHB"
            }
        ]""",

"penang.html": """[
            { 
                name: "Candidate A: Jalan Burma - Georgetown (Gurney Paragon)", 
                lat: 5.4355, lng: 100.309, 
                note: "Pinned to Gurney Paragon Mall for road reference. TOP PICK. Georgetown's premium lifestyle corridor. Ground-floor shophouse between Gurney Drive and Jln Burma junction. A-Saloon and Wave Hair within 600m confirm premium demand. Heritage conservation area — boutique aesthetic naturally fits. Rent MYR 2,500–4,000/mo.", 
                rent: 800, catchment: 30000, premiumTargetPct: 32, competitorCapacity: 7000,
                airportTime: "25 mins from PEN"
            },
            { 
                name: "Candidate B: Gurney Drive - Upscale Mall (Gurney Plaza)", 
                lat: 5.4375, lng: 100.308, 
                note: "Pinned to Gurney Plaza for road reference. Adjacent to Gurney Paragon Mall — Penang's most premium retail address. High visibility to HNWI families. More expensive rent but premium positioning justified. Good parking access.", 
                rent: 1100, catchment: 35000, premiumTargetPct: 28, competitorCapacity: 8000,
                airportTime: "22 mins from PEN"
            },
            { 
                name: "Candidate C: Chulia St Heritage Lane (Chulia Shophouses)", 
                lat: 5.4185, lng: 100.3365, 
                note: "Pinned to Chulia Street Shophouses for road reference. Heritage boutique zone. Instagram-worthy setting in Penang's most photographed street. Higher tourist traffic but lower premium residential density. Better for digital nomad and tourist walk-in market.", 
                rent: 600, catchment: 20000, premiumTargetPct: 25, competitorCapacity: 3000,
                airportTime: "30 mins from PEN"
            }
        ]""",

"sabah.html": """[
            { 
                name: "Candidate A: Jesselton Point Waterfront Retail (Jesselton Point)", 
                lat: 5.993, lng: 116.079, 
                note: "Pinned to Jesselton Point Ferry Terminal for road reference. TOP PICK. KK's premier waterfront commercial zone. Ground-floor retail facing Jesselton Point Ferry Terminal — maximum tourist and expat visibility. Oil & gas executives from nearby Menara TH clusters here. Rent MYR 3,000–5,000/mo.", 
                rent: 900, catchment: 25000, premiumTargetPct: 40, competitorCapacity: 3000,
                airportTime: "20 mins from BKI"
            },
            { 
                name: "Candidate B: Jalan Gaya Commercial (Suria Sabah)", 
                lat: 5.988, lng: 116.076, 
                note: "Pinned to Suria Sabah Mall for road reference. KK's main commercial street. Ground-floor unit within walking distance of Suria Sabah and Oceanus Mall. Michael & Guys nearby confirms premium hair demand. Best balance of rent vs foot traffic.", 
                rent: 800, catchment: 22000, premiumTargetPct: 35, competitorCapacity: 4000,
                airportTime: "20 mins from BKI"
            },
            { 
                name: "Candidate C: Sutera Harbour Boulevard (Sutera Harbour Resort)", 
                lat: 5.969, lng: 116.059, 
                note: "Pinned to Sutera Harbour Resort for road reference. 5-star resort corridor. Expat families from Shell, Murphy Oil, and resort management cluster in Sutera Harbour. Guaranteed HNWI clientele but lower total foot traffic and very high rent.", 
                rent: 1500, catchment: 15000, premiumTargetPct: 50, competitorCapacity: 1500,
                airportTime: "18 mins from BKI"
            }
        ]""",

"sarawak.html": """[
            { 
                name: "Candidate A: Tabuan Jaya Commercial Strip (Vivacity Megamall)", 
                lat: 1.5285, lng: 110.355, 
                note: "Pinned to Vivacity Megamall for road reference. TOP PICK. Shell Sarawak / Petronas expat residential hub. Ground-floor shophouse in Tabuan Jaya commercial area — 5-min drive from expatriate housing estates (Green Road, Stutong). Zero premium competition in zone. Rent MYR 2,000–3,500/mo.", 
                rent: 700, catchment: 20000, premiumTargetPct: 42, competitorCapacity: 2000,
                airportTime: "20 mins from KCH"
            },
            { 
                name: "Candidate B: Hikmah Exchange Commercial (Hikmah Exchange)", 
                lat: 1.5275, lng: 110.364, 
                note: "Pinned to Hikmah Exchange for road reference. Sarawak's premium lifestyle hub. Gene's Work Hair Studio present — validates premium market. Central location accessible to entire Kuching metro. Emerging F&B and retail scene creates premium ambiance.", 
                rent: 900, catchment: 28000, premiumTargetPct: 35, competitorCapacity: 5000,
                airportTime: "18 mins from KCH"
            },
            { 
                name: "Candidate C: The Northbank - Waterfront (Northbank Commercial)", 
                lat: 1.5585, lng: 110.3465, 
                note: "Pinned to The Northbank Commercial Centre for road reference. Kuching's revitalised waterfront precinct. Mane Society salon present — confirms premium hair interest in zone. Tourist and professional cross-traffic. Heritage boutique aesthetic advantage.", 
                rent: 750, catchment: 18000, premiumTargetPct: 28, competitorCapacity: 4000,
                airportTime: "20 mins from KCH"
            }
        ]""",

# ── TAIWAN ───────────────────────────────────────────────────────────────────

"taipei.html": """[
            { 
                name: "Candidate A: Da'an District - Yongkang St (Yongkang Park)", 
                lat: 25.0322, lng: 121.5298, 
                note: "Pinned to Yongkang Park for road reference. TOP PICK. Da'an's premium lifestyle lane — Japan-quality boutique density. Ground-floor alleyway unit. Eddie Tham and SeeFu within 400m confirm premium demand. AIT (American Institute Taiwan) expat community nearby. Rent NTD 90,000–130,000/mo.", 
                rent: 3400, catchment: 40000, premiumTargetPct: 32, competitorCapacity: 12000,
                airportTime: "15 mins from TSA / 45 mins from TPE"
            },
            { 
                name: "Candidate B: Xinyi District - Songshou Rd (ATT 4 FUN)", 
                lat: 25.0354, lng: 121.5658, 
                note: "Pinned to ATT 4 FUN for road reference. Taipei's financial and luxury retail hub. Near Taipei 101 and W Hotel. TSMC and tech company international executives cluster in Xinyi luxury condos. Premium pricing power strongest here. Rent NTD 120,000–180,000/mo.", 
                rent: 4600, catchment: 35000, premiumTargetPct: 30, competitorCapacity: 10000,
                airportTime: "15 mins from TSA"
            },
            { 
                name: "Candidate C: Zhongshan - Chifeng St (Zhongshan MRT Exit 4)", 
                lat: 25.0522, lng: 121.5205, 
                note: "Pinned to Zhongshan MRT Station Exit 4 for road reference. Creative design district with highest concentration of Taipei's fashion/art professional class. Japanese expat families cluster in Zhongshan near Minami Tokyo community areas. Lower rent than Xinyi. Rent NTD 70,000–100,000/mo.", 
                rent: 2600, catchment: 32000, premiumTargetPct: 28, competitorCapacity: 9000,
                airportTime: "10 mins from TSA"
            }
        ]""",

"taichung.html": """[
            { 
                name: "Candidate A: Qi-qi Zone - Shizheng North Rd (Taichung Theater)", 
                lat: 24.1628, lng: 120.6408, 
                note: "Pinned to National Taichung Theater for road reference. TOP PICK. Taichung's most affluent zone (Qi-qi / 7th Redevelopment Zone). Ground-floor boutique on Shizheng North Rd near W Taichung and Kimpton hotels. Japanese business families from Advantech/Giant cluster in nearby luxury towers. Rent NTD 80,000–120,000/mo.", 
                rent: 3000, catchment: 38000, premiumTargetPct: 35, competitorCapacity: 8000,
                airportTime: "30 mins from RMQ"
            },
            { 
                name: "Candidate B: Xitun - Taiwan Boulevard (Shin Kong Mitsukoshi)", 
                lat: 24.1648, lng: 120.6435, 
                note: "Pinned to Shin Kong Mitsukoshi Taichung Zhonggang for road reference. Xitun district's commercial spine. ELF Salon and VS Hair present — confirms premium demand but also direct competition zone. Lower rent than Qi-qi but established premium foot traffic. Rent NTD 60,000–85,000/mo.", 
                rent: 2200, catchment: 32000, premiumTargetPct: 28, competitorCapacity: 12000,
                airportTime: "30 mins from RMQ"
            },
            { 
                name: "Candidate C: Beitun - Wenxin Rd (Beitun Main Station)", 
                lat: 24.2021, lng: 120.6425, 
                note: "Pinned to Beitun Main Station for road reference. Emerging premium residential corridor north of Qi-qi. Lower current competition, growing family demographic. Best for second-outlet once Qi-qi flagship is established. Rent NTD 45,000–65,000/mo.", 
                rent: 1700, catchment: 25000, premiumTargetPct: 22, competitorCapacity: 4000,
                airportTime: "25 mins from RMQ"
            }
        ]""",

"kaohsiung.html": """[
            { 
                name: "Candidate A: Zuoying THSR Commercial Zone (Mitsukoshi)", 
                lat: 22.6875, lng: 120.3015, 
                note: "Pinned to Shin Kong Mitsukoshi Kaohsiung Zuoying for road reference. TOP PICK. High-speed rail terminus commercial zone. First-mover position — zero premium salon in zone. THSR commuters from Taipei book appointments around train schedule. Japanese Foxconn/Innolux corporate housing in adjacent Zuoying towers. Rent NTD 60,000–80,000/mo.", 
                rent: 2000, catchment: 30000, premiumTargetPct: 35, competitorCapacity: 2000,
                airportTime: "15 mins from KHH"
            },
            { 
                name: "Candidate B: Lingya District - Sanduo Shopping (Pacific SOGO)", 
                lat: 22.6145, lng: 120.3045, 
                note: "Pinned to Pacific SOGO Kaohsiung for road reference. Kaohsiung's premier shopping and lifestyle district. Round2 Hair Salon present — confirms premium demand. Higher competition but large total catchment. Best for capturing Kaohsiung's fashion-forward creative class. Rent NTD 70,000–95,000/mo.", 
                rent: 2500, catchment: 42000, premiumTargetPct: 28, competitorCapacity: 15000,
                airportTime: "15 mins from KHH"
            },
            { 
                name: "Candidate C: Xinxing District (Central Park MRT)", 
                lat: 22.6245, lng: 120.3025, 
                note: "Pinned to Central Park MRT Station Exit 1 for road reference. Near Kaohsiung's Central Park MRT and cultural facilities. Growing premium residential catchment with access to Kaohsiung's Japanese business community. Lower competition than Lingya. Rent NTD 55,000–75,000/mo.", 
                rent: 1800, catchment: 28000, premiumTargetPct: 26, competitorCapacity: 6000,
                airportTime: "12 mins from KHH"
            }
        ]""",

"tainan.html": """[
            { 
                name: "Candidate A: Sinshih District - TSMC Housing (Sinshih Station)", 
                lat: 23.0782, lng: 120.297, 
                note: "Pinned to Sinshih Station for road reference. TOP PICK. Adjacent to TSMC Fab 18 and STSP company housing. TSMC international engineers (Japanese, US, European) live within 1km. Zero premium salon competition within 10km. Ground-floor commercial in Sinshih new development zone. Rent NTD 40,000–60,000/mo.", 
                rent: 1500, catchment: 22000, premiumTargetPct: 55, competitorCapacity: 500,
                airportTime: "35 mins from TNN / 50 mins from KHH"
            },
            { 
                name: "Candidate B: East District (NCKU Campus)", 
                lat: 22.9972, lng: 120.2185, 
                note: "Pinned to National Cheng Kung University for road reference. NCKU university zone with growing premium professional catchment. Tainan's young professional and academic community. Better established commercial street — more foot traffic than Sinshih but lower TSMC expat density. Rent NTD 32,000–48,000/mo.", 
                rent: 1200, catchment: 35000, premiumTargetPct: 28, competitorCapacity: 4000,
                airportTime: "15 mins from TNN"
            },
            { 
                name: "Candidate C: West Central - Zhongzheng Rd (Hayashi Dept Store)", 
                lat: 22.9918, lng: 120.202, 
                note: "Pinned to Hayashi Department Store for road reference. Historic Tainan city center. Higher general foot traffic but lower premium density. Best for capturing Tainan's broader professional and tourist market as second phase of expansion. Rent NTD 35,000–52,000/mo.", 
                rent: 1300, catchment: 40000, premiumTargetPct: 20, competitorCapacity: 6000,
                airportTime: "20 mins from TNN"
            }
        ]""",

# ── AUSTRALIA ────────────────────────────────────────────────────────────────

"brisbane.html": """[
            { 
                name: "Candidate A: New Farm - Brunswick St (Merthyr Village)", 
                lat: -27.4612, lng: 153.0425, 
                note: "Pinned to Merthyr Village Shopping Centre for road reference. TOP PICK. Brisbane's highest-income inner-east residential corridor (median house AUD 2.1M+). Ground-floor boutique on Brunswick St New Farm. Zero premium colour boutique within 15-min walk. UV-damage + Asian hair specialist gap confirmed by research. Rent AUD 3,500–5,500/mo.", 
                rent: 2800, catchment: 35000, premiumTargetPct: 38, competitorCapacity: 5000,
                airportTime: "20 mins from BNE"
            },
            { 
                name: "Candidate B: Fortitude Valley - James St Precinct (The Calile Hotel)", 
                lat: -27.4583, lng: 153.037, 
                note: "Pinned to The Calile Hotel for road reference. Adjacent to James St luxury retail (Camilla, Zimmermann). Growing Korean/Japanese community in Valley. Boutique hair studio density lower than Paddington — white space for premium colour.", 
                rent: 3200, catchment: 40000, premiumTargetPct: 32, competitorCapacity: 4000,
                airportTime: "20 mins from BNE"
            },
            { 
                name: "Candidate C: Paddington - Given Tce (Sol Hair area)", 
                lat: -27.4619, lng: 152.9988, 
                note: "Pinned to Sol Hair for road reference. Sol Hair (main competitor) at Given Tce confirms premium demand. Entry here means direct competition with entrenched local brand — only viable if Asian hair specialisation clearly differentiates. High foot traffic, moderate rent.", 
                rent: 2600, catchment: 30000, premiumTargetPct: 30, competitorCapacity: 14000,
                airportTime: "22 mins from BNE"
            }
        ]""",

"sydney.html": """[
            { 
                name: "Candidate A: Newtown - King St (Newtown Station)", 
                lat: -33.8978, lng: 151.1795, 
                note: "Pinned to Newtown Station for road reference. TOP PICK. Sydney's most underserved premium corridor. Young professional dual-income households (25–45). Nearest premium boutique is 15-min commute to Surry Hills. Zero premium colour boutique on King St. UV + transparent pricing gap. Rent AUD 4,000–6,500/mo.", 
                rent: 3200, catchment: 42000, premiumTargetPct: 35, competitorCapacity: 3000,
                airportTime: "22 mins from SYD"
            },
            { 
                name: "Candidate B: Glebe - Glebe Point Rd (Glebe Markets)", 
                lat: -33.8785, lng: 151.1852, 
                note: "Pinned to Glebe Markets for road reference. Adjacent to Newtown but with higher residential density and less foot traffic competition. University of Sydney proximity creates young professional catchment. Same income profile as Newtown, slightly lower rent.", 
                rent: 2800, catchment: 35000, premiumTargetPct: 32, competitorCapacity: 2500,
                airportTime: "22 mins from SYD"
            },
            { 
                name: "Candidate C: Surry Hills - Crown St (The Clock Hotel)", 
                lat: -33.8885, lng: 151.212, 
                note: "Pinned to The Clock Hotel for road reference. RAW Anthony Nader, Flock, Wakefields within 300m — confirms premium demand but highly competitive. Only viable if transparent all-inclusive pricing model creates clear differentiation from add-on fee competitors.", 
                rent: 4500, catchment: 50000, premiumTargetPct: 38, competitorCapacity: 22000,
                airportTime: "20 mins from SYD"
            }
        ]""",

"melbourne.html": """[
            { 
                name: "Candidate A: South Yarra - Chapel St (The Jam Factory)", 
                lat: -37.8395, lng: 144.995, 
                note: "Pinned to The Jam Factory for road reference. TOP PICK. Melbourne's premier lifestyle corridor. Ground-floor boutique on Chapel St between Toorak Rd and Commercial Rd. Highest per-capita luxury spend in Melbourne. Japanese expat community concentrated in surrounding Prahran/Toorak. Rent AUD 4,500–7,000/mo.", 
                rent: 3500, catchment: 45000, premiumTargetPct: 35, competitorCapacity: 12000,
                airportTime: "30 mins from MEL"
            },
            { 
                name: "Candidate B: Fitzroy - Brunswick St (Fitzroy Town Hall)", 
                lat: -37.802, lng: 144.979, 
                note: "Pinned to Fitzroy Town Hall for road reference. Melbourne's creative professional zone. Fashion-forward demographic with high WTP for specialist creative colour (balayage, vivid, copper). Lower rent than Chapel St. Growing Korean community in surrounding Carlton.", 
                rent: 2800, catchment: 38000, premiumTargetPct: 30, competitorCapacity: 8000,
                airportTime: "30 mins from MEL"
            },
            { 
                name: "Candidate C: CBD - Collins St (Collins Place)", 
                lat: -37.8138, lng: 144.9715, 
                note: "Pinned to Collins Place for road reference. Melbourne's corporate financial spine. After-work appointments from CBD professionals. Access to largest total catchment. Highest rent but strongest lunchtime/after-work booking density. Best for corporate membership program.", 
                rent: 5500, catchment: 60000, premiumTargetPct: 28, competitorCapacity: 18000,
                airportTime: "30 mins from MEL"
            }
        ]""",

"perth.html": """[
            { 
                name: "Candidate A: Subiaco - Rokeby Rd (Subiaco Square)", 
                lat: -31.9465, lng: 115.8245, 
                note: "Pinned to Subiaco Square Shopping Centre for road reference. TOP PICK. Perth's premium inner-western suburb. High FIFO worker family density (mining/resources executives on 2-weeks-on/off cycles). Ground-floor shophouse on Rokeby Rd retail strip. UV-protection angle strong given Perth's extreme UV index (UV 11+ in summer). Rent AUD 2,500–4,000/mo.", 
                rent: 2000, catchment: 28000, premiumTargetPct: 32, competitorCapacity: 6000,
                airportTime: "22 mins from PER"
            },
            { 
                name: "Candidate B: Claremont - St Quentin Ave (Claremont Quarter)", 
                lat: -31.981, lng: 115.782, 
                note: "Pinned to Claremont Quarter for road reference. Old-money western suburbs. Highest household income in Perth metro. Premium boutique aesthetic fits heritage streetscape. Less foot traffic than Subiaco but HNWI appointment-only clientele — matches premium model.", 
                rent: 1800, catchment: 18000, premiumTargetPct: 40, competitorCapacity: 4000,
                airportTime: "25 mins from PER"
            },
            { 
                name: "Candidate C: Cottesloe - Marine Pde (Cottesloe Beach Hotel)", 
                lat: -31.996, lng: 115.751, 
                note: "Pinned to Cottesloe Beach Hotel for road reference. Coastal boutique positioning. Beach lifestyle + UV damage angle is strongest here. Tourist season (Oct–Apr) boosts volume. Lowest year-round footfall consistency of three candidates.", 
                rent: 1600, catchment: 15000, premiumTargetPct: 35, competitorCapacity: 2500,
                airportTime: "30 mins from PER"
            }
        ]""",

# ── JAPAN ─────────────────────────────────────────────────────────────────────

"fukuoka.html": """[
            { 
                name: "Candidate A: Daimyo - Central Lane (saco Japan)", 
                lat: 33.5878, lng: 130.395, 
                note: "Pinned to saco Japan for road reference. TOP PICK. Fukuoka's most fashionable boutique district. Ground-floor commercial unit on Daimyo's main shopping lane. saco japan flagship and TONI&GUY Tenjin within 600m — confirms premium demand. Korean expat community of 8,000+ nearby in Hakata/Tenjin. Rent JPY 150,000–250,000/mo.", 
                rent: 1600, catchment: 35000, premiumTargetPct: 28, competitorCapacity: 12000,
                airportTime: "15 mins from FUK"
            },
            { 
                name: "Candidate B: Tenjin - Watanabe-dori (Solaria Plaza)", 
                lat: 33.5897, lng: 130.3989, 
                note: "Pinned to Solaria Plaza for road reference. Tenjin's main commercial boulevard. TONI&GUY and Shiki Hair immediately adjacent — highest premium footfall in Fukuoka. Entry here requires differentiation on vivid/creative colour vs. Japanese natural-tone consensus. High rent but maximum visibility.", 
                rent: 2200, catchment: 50000, premiumTargetPct: 25, competitorCapacity: 20000,
                airportTime: "15 mins from FUK"
            },
            { 
                name: "Candidate C: Imaizumi - Boutique Alleyway (Imaizumi Park)", 
                lat: 33.5852, lng: 130.399, 
                note: "Pinned to Imaizumi Park for road reference. Trendy alleyway boutique zone between Tenjin and Daimyo. Lower rent, creative/art professional demographic, high Instagram potential for fashion colour portfolio. Korean expat community adjacent in Sumiyoshi.", 
                rent: 1100, catchment: 22000, premiumTargetPct: 22, competitorCapacity: 6000,
                airportTime: "15 mins from FUK"
            }
        ]""",

"okinawa.html": """[
            { 
                name: "Candidate A: Omoromachi / Shin-toshin (San-A Main Place)", 
                lat: 26.2222, lng: 127.6958, 
                note: "Pinned to San-A Naha Main Place for road reference. TOP PICK. Naha's civilian expat core — entirely unserved by English/Korean-friendly premium salons. Ground-floor commercial near DFS Galleria and Naha Shin-toshin. Korean tourists (200,000+/year) pass through this zone. BLOOM/Borjan are 30+ min north in Chatan — this is a true whitespace. Rent JPY 100,000–180,000/mo.", 
                rent: 1100, catchment: 28000, premiumTargetPct: 52, competitorCapacity: 1500,
                airportTime: "15 mins from OKA"
            },
            { 
                name: "Candidate B: Kumoji Business Center (Palais Ryubo)", 
                lat: 26.2155, lng: 127.681, 
                note: "Pinned to Palais Ryubo for road reference. Naha central business district. Mix of Japanese professionals, Ryukyu University community, and Korean tourist hotels. Good balance of resident and tourist traffic. Lower rent than Omoromachi premium strip.", 
                rent: 800, catchment: 22000, premiumTargetPct: 35, competitorCapacity: 2000,
                airportTime: "15 mins from OKA"
            },
            { 
                name: "Candidate C: Kokusai-dori (Don Quijote Kokusai-dori)", 
                lat: 26.2152, lng: 127.688, 
                note: "Pinned to Don Quijote Kokusai-dori for road reference. Okinawa's main tourist shopping street. Maximum Korean tourist walk-in volume. Risk of being perceived as tourist-trap rather than premium boutique. Best for pop-up testing Korean tourist demand before permanent commitment.", 
                rent: 1400, catchment: 35000, premiumTargetPct: 30, competitorCapacity: 5000,
                airportTime: "15 mins from OKA"
            }
        ]""",

# ── SOUTH KOREA ────────────────────────────────────────────────────────────────

"busan.html": """[
            { 
                name: "Candidate A: Haeundae Marine City (Haeundae I-Park)", 
                lat: 35.1578, lng: 129.1438, 
                note: "Pinned to Haeundae I-Park for road reference. TOP PICK. Marine City luxury residential towers. HNWI Busan residents in sky-high condos (Zenith, I-Park Marine). Happynian salon (competitor) is in Seomyeon — 20-min drive away. Marine City currently has no premium boutique colour studio. Rent KRW 2.5M–4M/mo.", 
                rent: 2200, catchment: 35000, premiumTargetPct: 40, competitorCapacity: 3000,
                airportTime: "30 mins from PUS"
            },
            { 
                name: "Candidate B: Centum City (Shinsegae Centum)", 
                lat: 35.1691, lng: 129.1302, 
                note: "Pinned to Shinsegae Centum City for road reference. Busan's international business hub. BEXCO convention centre creates regular influx of Korean and international business visitors. Adjacent Shinsegae Centum (world's largest department store) confirms premium retail demand.", 
                rent: 2800, catchment: 45000, premiumTargetPct: 32, competitorCapacity: 8000,
                airportTime: "28 mins from PUS"
            },
            { 
                name: "Candidate C: Haeundae Beach Front (Paradise Hotel)", 
                lat: 35.1601, lng: 129.1638, 
                note: "Pinned to Paradise Hotel Busan for road reference. Beach Road tourism strip. Strong summer volume but seasonality risk (peak Jun–Aug, quiet Oct–Feb). Best for high-season volume boost after Marine City flagship established.", 
                rent: 2500, catchment: 38000, premiumTargetPct: 28, competitorCapacity: 6000,
                airportTime: "30 mins from PUS"
            }
        ]""",

# ── OTHER APAC ─────────────────────────────────────────────────────────────────

"singapore.html": """[
            { 
                name: "Candidate A: Holland Village - Jalan Merah Saga (Chip Bee Gardens)", 
                lat: 1.3115, lng: 103.7965, 
                note: "Pinned to Chip Bee Gardens for road reference. TOP PICK. Holland Village's expat residential core — unserved by a premium colour boutique at this price level. Chez Vous HideAway is in Scotts (2km), Love Hair in Jiak Chuan (3km). Ground-floor shophouse at Holland V fringe. Rent SGD 7,000–11,000/mo.", 
                rent: 5500, catchment: 45000, premiumTargetPct: 42, competitorCapacity: 8000,
                airportTime: "25 mins from SIN"
            },
            { 
                name: "Candidate B: Tanglin - Cluny Rd / Dempsey Hill (Tanglin Mall)", 
                lat: 1.3045, lng: 103.8235, 
                note: "Pinned to Tanglin Mall for road reference. Dempsey Hill boutique zone. Blonde Boudoir operates here — validates premium demand. Tanglin corridor has highest per-household income in Singapore. Ground-floor shophouse near American Club. Premium positioning strongest here but smaller total catchment.", 
                rent: 6500, catchment: 30000, premiumTargetPct: 48, competitorCapacity: 6000,
                airportTime: "22 mins from SIN"
            },
            { 
                name: "Candidate C: Tanjong Pagar (100 AM Mall)", 
                lat: 1.275, lng: 103.8425, 
                note: "Pinned to 100 AM Mall for road reference. Growing CBD-adjacent expat zone. Luxury condo density (Altez, The Pinnacle@Duxton vicinity). Love Hair nearby validates demand. Best for after-work appointments from CBD professionals. Higher corporate membership potential.", 
                rent: 7000, catchment: 40000, premiumTargetPct: 35, competitorCapacity: 12000,
                airportTime: "20 mins from SIN"
            }
        ]""",

"bangkok.html": """[
            { 
                name: "Candidate A: Thonglor Soi 10 (Donki Mall Thonglor)", 
                lat: 13.7335, lng: 100.5833, 
                note: "Pinned to Donki Mall Thonglor for road reference. TOP PICK. Thonglor is the epicentre of Bangkok's Japanese and Western expat community. The London Hair and Yumoto are 400-600m away — confirms premium demand and establishes our soft-water filtration USP against competitors on same tap water system. Ground-floor suite, high visibility. Rent USD 4,000–6,000/mo.", 
                rent: 5000, catchment: 45000, premiumTargetPct: 38, competitorCapacity: 14000,
                airportTime: "30 mins from BKK / 35 mins from DMK"
            },
            { 
                name: "Candidate B: Ekkamai Soi 4 (Featherstone Cafe)", 
                lat: 13.7259, lng: 100.5855, 
                note: "Pinned to Featherstone Cafe for road reference. Large expat residential corridor adjacent to Thonglor. CYAN Salon is here — validates premium colour demand. Lower rent than Thonglor main but same demographic catchment. Better parking for suburban expat families.", 
                rent: 3800, catchment: 38000, premiumTargetPct: 32, competitorCapacity: 10000,
                airportTime: "32 mins from BKK / 37 mins from DMK"
            },
            { 
                name: "Candidate C: Phrom Phong Soi 39 (The Manor 39)", 
                lat: 13.7332, lng: 100.5725, 
                note: "Pinned to The Manor 39 for road reference. Exclusive condo retail lane near EmQuartier. Highest per-capita income of any Bangkok expat zone. Micha & Justin and Japanese hair salons operate nearby. Extremely limited availability and highest rent — reserve for second outlet.", 
                rent: 6500, catchment: 40000, premiumTargetPct: 35, competitorCapacity: 16000,
                airportTime: "35 mins from BKK / 40 mins from DMK"
            }
        ]""",

"hongkong.html": """[
            { 
                name: "Candidate A: Causeway Bay - Lockhart Rd (Sogo CWB)", 
                lat: 22.28, lng: 114.1839, 
                note: "Pinned to Sogo Causeway Bay for road reference. TOP PICK. Causeway Bay is HK's most accessible premium retail zone. Ground-floor unit on Lockhart Rd. Bruneblonde and Love Hair both operate in the district — high premium colour demand confirmed. HKD 60,000–100,000/mo rent. Soft-water filtration is a genuine USP vs all Causeway Bay competitors on same tap water.", 
                rent: 8500, catchment: 50000, premiumTargetPct: 40, competitorCapacity: 18000,
                airportTime: "40 mins from HKG"
            },
            { 
                name: "Candidate B: Central - Wyndham St / SOHO (The Centrium)", 
                lat: 22.281, lng: 114.1555, 
                note: "Pinned to The Centrium for road reference. HK's financial and expat social hub. Kimrobinson flagship nearby — validates ultra-premium demand. Ground-floor on Wyndham or Peel St. After-work and lunch appointments from IFC/Chater House financial professionals. Highest average ticket potential.", 
                rent: 11000, catchment: 42000, premiumTargetPct: 45, competitorCapacity: 20000,
                airportTime: "40 mins from HKG"
            }
        ]""",

"macau.html": """[
            { 
                name: "Candidate A: Taipa Village Commercial Row (Taipa Art Space)", 
                lat: 22.1578, lng: 113.5582, 
                note: "Pinned to Taipa Village Art Space for road reference. TOP PICK. Taipa is Macau's preferred residential zone for casino management expats. Ground-floor shophouse in Taipa Village commercial area. Hair Cloud (competitor) presence confirms premium demand. Consistent non-gaming clientele unlike Cotai Strip. Rent MOP 12,000–20,000/mo.", 
                rent: 1800, catchment: 25000, premiumTargetPct: 42, competitorCapacity: 5000,
                airportTime: "15 mins from MFM"
            },
            { 
                name: "Candidate B: NAPE Commercial District (MGM Macau)", 
                lat: 22.1855, lng: 113.5545, 
                note: "Pinned to MGM Macau for road reference. Macau Peninsula's modern commercial zone. Higher foot traffic from mixed resident/business crowd. Waxmeup operates nearby. Easier logistics from Macau-Zhuhai border crossing — important for Mainland Chinese premium clients visiting Macau.", 
                rent: 1500, catchment: 30000, premiumTargetPct: 32, competitorCapacity: 6000,
                airportTime: "15 mins from MFM"
            },
            { 
                name: "Candidate C: Cotai Strip Hotel Retail (The Venetian)", 
                lat: 22.1472, lng: 113.5597, 
                note: "Pinned to The Venetian Macao for road reference. Le SPA'tique / Wynn Salon confirm demand in casino zone. Wynn-level pricing possible (USD 200+). However, casino retail rent is extreme and client flow unpredictable during gaming downturns. Viable as Phase 2 hotel partnership rather than standalone lease.", 
                rent: 4500, catchment: 20000, premiumTargetPct: 35, competitorCapacity: 12000,
                airportTime: "15 mins from MFM"
            }
        ]""",

"dubai.html": """[
            { 
                name: "Candidate A: Jumeirah 1 / Safa Park Corridor (Safa Park Gate)", 
                lat: 25.205, lng: 55.245, 
                note: "Pinned to Safa Park Gate for road reference. TOP PICK. Dubai's Western expat residential core. Ground-floor villa shopfront on Jumeirah Rd near Safa Park. British, American, Australian expat families concentrated here. Soft-water filtration is essential — Dubai tap water TDS 500–1200 ppm destroys colour. Rent AED 120,000–180,000/yr.", 
                rent: 3500, catchment: 45000, premiumTargetPct: 48, competitorCapacity: 10000,
                airportTime: "15 mins from DXB"
            },
            { 
                name: "Candidate B: Dubai Marina / JBR Promenade (The Beach JBR)", 
                lat: 25.0768, lng: 55.1312, 
                note: "Pinned to The Beach JBR for road reference. High-density expat residential towers. Strong walk-in traffic from JBR beach promenade. Diverse European, Russian, Indian expat community. Multiple salons present but soft-water filtration advantage meaningful in this hard-water zone.", 
                rent: 4000, catchment: 55000, premiumTargetPct: 38, competitorCapacity: 14000,
                airportTime: "25 mins from DXB"
            },
            { 
                name: "Candidate C: Al Wasl Rd (Boxpark Dubai)", 
                lat: 25.1865, lng: 55.2248, 
                note: "Pinned to Boxpark Dubai for road reference. Old-established expat zone. Lower rent, loyal residential clientele. Best for word-of-mouth growth among long-term Dubai residents vs. tourist-heavy Marina zone.", 
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
