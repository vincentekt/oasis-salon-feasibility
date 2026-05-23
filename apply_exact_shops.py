import re
import os

# Definition of the exact shop updates for all 27 cities
# Format: {city_filename: [(candidate_index, new_candidate_name, lat, lng, new_table_name, new_ref), ...]}
SHOP_UPDATES = {
    "hcmc.html": [
        (0, "Candidate A: Concept Coiffure (Xuan Thuy St)", 10.8045, 106.7375, "Concept Coiffure (Xuan Thuy St)", "Concept Coiffure"),
        (1, "Candidate B: Starbucks Masteri T5 (Quoc Huong St)", 10.8040, 106.7450, "Starbucks Masteri T5 (Quoc Huong St)", "Starbucks Masteri T5"),
        (2, "Candidate C: Sheraton Saigon Hotel (Le Thanh Ton St)", 10.7745, 106.7032, "Sheraton Saigon Hotel (Le Thanh Ton St)", "Sheraton Saigon Hotel")
    ],
    "hanoi.html": [
        (0, "Candidate A: Starbucks Syrena Center (Xuan Dieu St)", 21.0625, 105.8280, "Starbucks Syrena Center (Xuan Dieu St)", "Starbucks Syrena Center"),
        (1, "Candidate B: Saint Honoré Bakery (To Ngoc Van St)", 21.0585, 105.8252, "Saint Honoré Bakery (To Ngoc Van St)", "Saint Honoré Bakery"),
        (2, "Candidate C: Starbucks Trang Tien Plaza", 21.0252, 105.8525, "Starbucks Trang Tien Plaza", "Starbucks Trang Tien Plaza")
    ],
    "binhduong.html": [
        (0, "Candidate A: Highlands Coffee Canary Plaza", 10.9305, 106.7115, "Highlands Coffee Canary Plaza", "Highlands Coffee Canary Plaza"),
        (1, "Candidate B: Starbucks Aeon Mall Binh Duong", 10.9332, 106.6978, "Starbucks Aeon Mall Binh Duong", "Starbucks Aeon Mall"),
        (2, "Candidate C: Highlands Coffee Becamex Tower", 10.9778, 106.6568, "Highlands Coffee Becamex Tower", "Highlands Coffee Becamex Tower")
    ],
    "danang.html": [
        (0, "Candidate A: Holiday Beach Club (An Thuong Beach)", 16.0485, 108.2455, "Holiday Beach Club (An Thuong Beach)", "Holiday Beach Club"),
        (1, "Candidate B: Starbucks TMS Hotel (My Khe Beach)", 16.0416, 108.2483, "Starbucks TMS Hotel (My Khe Beach)", "Starbucks TMS Hotel"),
        (2, "Candidate C: Highlands Coffee Indochina Riverside Mall", 16.0610, 108.2230, "Highlands Coffee Indochina Riverside Mall", "Highlands Coffee Indochina Mall")
    ],
    "dongnai.html": [
        (0, "Candidate A: Highlands Coffee Amata Gate", 10.9535, 106.8405, "Highlands Coffee Amata Gate", "Highlands Coffee Amata Gate"),
        (1, "Candidate B: The Coffee House Loteco Gate", 10.9615, 106.8515, "The Coffee House Loteco Gate", "The Coffee House Loteco Gate"),
        (2, "Candidate C: Highlands Coffee Pegasus Plaza", 10.9495, 106.8328, "Highlands Coffee Pegasus Plaza", "Highlands Coffee Pegasus Plaza")
    ],
    "haiphong.html": [
        (0, "Candidate A: Highlands Coffee Museum Area", 20.8410, 106.6830, "Highlands Coffee Museum Area (Minh Khai St)", "Highlands Coffee Museum Area"),
        (1, "Candidate B: Starbucks Vincom Plaza Imperia", 20.8625, 106.6705, "Starbucks Vincom Plaza Imperia", "Starbucks Vincom Plaza Imperia"),
        (2, "Candidate C: Highlands Coffee Lach Tray St", 20.8432, 106.6965, "Highlands Coffee Lach Tray St", "Highlands Coffee Lach Tray")
    ],
    "johor.html": [
        (0, "Candidate A: Starbucks R&F Mall", 1.4608, 103.7711, "Starbucks R&F Mall", "Starbucks R&F Mall"),
        (1, "Candidate B: Starbucks Komtar JBCC", 1.4628, 103.7645, "Starbucks Komtar JBCC", "Starbucks Komtar JBCC"),
        (2, "Candidate C: Starbucks Mall of Medini", 1.4285, 103.6330, "Starbucks Mall of Medini", "Starbucks Mall of Medini")
    ],
    "kuala_lumpur.html": [
        (0, "Candidate A: Starbucks Suria KLCC (Jalan Ampang)", 3.1578, 101.7118, "Starbucks Suria KLCC (Jalan Ampang)", "Starbucks Suria KLCC"),
        (1, "Candidate B: Feeka Coffee Roasters (Bukit Ceylon)", 3.1495, 101.7075, "Feeka Coffee Roasters (Bukit Ceylon)", "Feeka Coffee Roasters"),
        (2, "Candidate C: Starbucks Bangsar Village II", 3.1305, 101.6715, "Starbucks Bangsar Village II", "Starbucks Bangsar Village II")
    ],
    "penang.html": [
        (0, "Candidate A: Starbucks Gurney Paragon (Jalan Burma)", 5.4355, 100.3090, "Starbucks Gurney Paragon (Jalan Burma)", "Starbucks Gurney Paragon"),
        (1, "Candidate B: Starbucks Gurney Plaza (Gurney Drive)", 5.4375, 100.3080, "Starbucks Gurney Plaza (Gurney Drive)", "Starbucks Gurney Plaza"),
        (2, "Candidate C: The Mugshot Cafe (Chulia St)", 5.4185, 100.3365, "The Mugshot Cafe (Chulia St)", "The Mugshot Cafe")
    ],
    "sabah.html": [
        (0, "Candidate A: Starbucks Jesselton Point", 5.9930, 116.0790, "Starbucks Jesselton Point", "Starbucks Jesselton Point"),
        (1, "Candidate B: Starbucks Suria Sabah (Jalan Gaya)", 5.9880, 116.0760, "Starbucks Suria Sabah (Jalan Gaya)", "Starbucks Suria Sabah"),
        (2, "Candidate C: Magellan Club Restaurant (Sutera Harbour)", 5.9690, 116.0590, "Magellan Club Restaurant (Sutera Harbour)", "Magellan Club Restaurant")
    ],
    "sarawak.html": [
        (0, "Candidate A: Starbucks Vivacity Megamall (Tabuan Jaya)", 1.5285, 110.3550, "Starbucks Vivacity Megamall (Tabuan Jaya)", "Starbucks Vivacity Megamall"),
        (1, "Candidate B: Tealive Hikmah Exchange", 1.5275, 110.3640, "Tealive Hikmah Exchange", "Tealive Hikmah Exchange"),
        (2, "Candidate C: Starbucks Northbank Drive-Thru", 1.5585, 110.3465, "Starbucks Northbank Drive-Thru", "Starbucks Northbank Drive-Thru")
    ],
    "brisbane.html": [
        (0, "Candidate A: Coles Merthyr Village (Brunswick St)", -27.4612, 153.0425, "Coles Merthyr Village (Brunswick St)", "Coles Merthyr Village"),
        (1, "Candidate B: Hellenika at The Calile (James St)", -27.4583, 153.0370, "Hellenika at The Calile (James St)", "Hellenika at The Calile"),
        (2, "Candidate C: Sol Hair (Given Tce)", -27.4619, 152.9988, "Sol Hair (Given Tce)", "Sol Hair")
    ],
    "melbourne.html": [
        (0, "Candidate A: Starbucks Jam Factory (Chapel St)", -37.8395, 144.9950, "Starbucks Jam Factory (Chapel St)", "Starbucks Jam Factory"),
        (1, "Candidate B: Industry Beans (Brunswick St, Fitzroy)", -37.8020, 144.9790, "Industry Beans (Brunswick St, Fitzroy)", "Industry Beans"),
        (2, "Candidate C: Laurent Bakery Collins Place (CBD)", -37.8138, 144.9715, "Laurent Bakery Collins Place (CBD)", "Laurent Bakery Collins Place")
    ],
    "perth.html": [
        (0, "Candidate A: Woolworths Subiaco Square (Rokeby Rd)", -31.9465, 115.8245, "Woolworths Subiaco Square (Rokeby Rd)", "Woolworths Subiaco Square"),
        (1, "Candidate B: Starbucks Claremont Quarter (St Quentin Ave)", -31.9810, 115.7820, "Starbucks Claremont Quarter (St Quentin Ave)", "Starbucks Claremont Quarter"),
        (2, "Candidate C: Cottesloe Beach Hotel (Marine Pde)", -31.9960, 115.7510, "Cottesloe Beach Hotel (Marine Pde)", "Cottesloe Beach Hotel")
    ],
    "sydney.html": [
        (0, "Candidate A: Cuckoo Callay Newtown (King St)", -33.8978, 151.1795, "Cuckoo Callay Newtown (King St)", "Cuckoo Callay"),
        (1, "Candidate B: Sonoma Bakery Glebe (Glebe Point Rd)", -33.8785, 151.1852, "Sonoma Bakery Glebe (Glebe Point Rd)", "Sonoma Bakery Glebe"),
        (2, "Candidate C: The Clock Hotel Surry Hills (Crown St)", -33.8885, 151.2120, "The Clock Hotel Surry Hills (Crown St)", "The Clock Hotel")
    ],
    "fukuoka.html": [
        (0, "Candidate A: saco Japan (Daimyo Central Lane)", 33.5878, 130.3950, "saco Japan (Daimyo Central Lane)", "saco Japan"),
        (1, "Candidate B: Starbucks Solaria Plaza (Watanabe-dori)", 33.5897, 130.3989, "Starbucks Solaria Plaza (Watanabe-dori)", "Starbucks Solaria Plaza"),
        (2, "Candidate C: Blue Bottle Coffee Tenjin (Imaizumi Park)", 33.5852, 130.3990, "Blue Bottle Coffee Tenjin (Imaizumi Park)", "Blue Bottle Coffee Tenjin")
    ],
    "okinawa.html": [
        (0, "Candidate A: Starbucks San-A Naha Main Place", 26.2222, 127.6958, "Starbucks San-A Naha Main Place", "Starbucks San-A Naha Main Place"),
        (1, "Candidate B: Starbucks Palais Ryubo (Kumoji)", 26.2155, 127.6810, "Starbucks Palais Ryubo (Kumoji)", "Starbucks Palais Ryubo"),
        (2, "Candidate C: Don Quijote Kokusai-dori", 26.2152, 127.6880, "Don Quijote Kokusai-dori", "Don Quijote Kokusai-dori")
    ],
    "busan.html": [
        (0, "Candidate A: Starbucks Marine City (Haeundae I-Park)", 35.1578, 129.1438, "Starbucks Marine City (Haeundae I-Park)", "Starbucks Marine City"),
        (1, "Candidate B: Starbucks Shinsegae Centum City", 35.1691, 129.1302, "Starbucks Shinsegae Centum City", "Starbucks Shinsegae Centum City"),
        (2, "Candidate C: Starbucks Paradise Hotel (Haeundae Beach)", 35.1601, 129.1638, "Starbucks Paradise Hotel (Haeundae Beach)", "Starbucks Paradise Hotel")
    ],
    "dubai.html": [
        (0, "Candidate A: Starbucks Safa Park (Jumeirah Rd)", 25.2050, 55.2450, "Starbucks Safa Park (Jumeirah Rd)", "Starbucks Safa Park"),
        (1, "Candidate B: Starbucks The Beach JBR", 25.0768, 55.1312, "Starbucks The Beach JBR", "Starbucks The Beach JBR"),
        (2, "Candidate C: Starbucks Boxpark (Al Wasl Rd)", 25.1865, 55.2248, "Starbucks Boxpark (Al Wasl Rd)", "Starbucks Boxpark")
    ],
    "bangkok.html": [
        (0, "Candidate A: Starbucks Donki Mall Thonglor (Soi 10)", 13.7335, 100.5833, "Starbucks Donki Mall Thonglor (Soi 10)", "Starbucks Donki Mall Thonglor"),
        (1, "Candidate B: Featherstone Cafe (Ekkamai Soi 4)", 13.7259, 100.5855, "Featherstone Cafe (Ekkamai Soi 4)", "Featherstone Cafe"),
        (2, "Candidate C: Starbucks The Manor 39 (Phrom Phong)", 13.7332, 100.5725, "Starbucks The Manor 39 (Phrom Phong)", "Starbucks The Manor 39")
    ],
    "hongkong.html": [
        (0, "Candidate A: Starbucks Sogo Causeway Bay (Lockhart Rd)", 22.2800, 114.1839, "Starbucks Sogo Causeway Bay (Lockhart Rd)", "Starbucks Sogo Causeway Bay"),
        (1, "Candidate B: Starbucks The Centrium (Wyndham St)", 22.2810, 114.1555, "Starbucks The Centrium (Wyndham St)", "Starbucks The Centrium")
    ],
    "macau.html": [
        (0, "Candidate A: Starbucks Taipa Village", 22.1578, 113.5582, "Starbucks Taipa Village", "Starbucks Taipa Village"),
        (1, "Candidate B: Starbucks MGM Macau (NAPE)", 22.1855, 113.5545, "Starbucks MGM Macau (NAPE)", "Starbucks MGM Macau"),
        (2, "Candidate C: Starbucks The Venetian Macao (Cotai Strip)", 22.1472, 113.5597, "Starbucks The Venetian Macao (Cotai Strip)", "Starbucks The Venetian Macao")
    ],
    "singapore.html": [
        (0, "Candidate A: Da Paolo Gastronomia (Chip Bee Gardens)", 1.3115, 103.7965, "Da Paolo Gastronomia (Chip Bee Gardens)", "Da Paolo Gastronomia"),
        (1, "Candidate B: Starbucks Tanglin Mall", 1.3045, 103.8235, "Starbucks Tanglin Mall", "Starbucks Tanglin Mall"),
        (2, "Candidate C: Starbucks 100 AM Mall (Tanjong Pagar)", 1.2750, 103.8425, "Starbucks 100 AM Mall (Tanjong Pagar)", "Starbucks 100 AM Mall")
    ],
    "kaohsiung.html": [
        (0, "Candidate A: Starbucks Shin Kong Mitsukoshi (Zuoying THSR)", 22.6875, 120.3015, "Starbucks Shin Kong Mitsukoshi (Zuoying THSR)", "Starbucks Shin Kong Mitsukoshi"),
        (1, "Candidate B: Starbucks Pacific SOGO (Sanduo Shopping)", 22.6145, 120.3045, "Starbucks Pacific SOGO (Sanduo Shopping)", "Starbucks Pacific SOGO"),
        (2, "Candidate C: Starbucks Central Park MRT (Xinxing District)", 22.6245, 120.3025, "Starbucks Central Park MRT (Xinxing District)", "Starbucks Central Park MRT")
    ],
    "taichung.html": [
        (0, "Candidate A: Theater Café (National Taichung Theater)", 24.1628, 120.6408, "Theater Café (National Taichung Theater)", "Theater Café"),
        (1, "Candidate B: Starbucks Shin Kong Mitsukoshi (Xitun)", 24.1648, 120.6435, "Starbucks Shin Kong Mitsukoshi (Xitun)", "Starbucks Shin Kong Mitsukoshi"),
        (2, "Candidate C: Starbucks Beitun Wenxin", 24.2021, 120.6425, "Starbucks Beitun Wenxin", "Starbucks Beitun Wenxin")
    ],
    "tainan.html": [
        (0, "Candidate A: Starbucks Tainan Sinshih (Sinshih District)", 23.0782, 120.2970, "Starbucks Tainan Sinshih (Sinshih District)", "Starbucks Tainan Sinshih"),
        (1, "Candidate B: Starbucks Tainan NCKU (East District)", 22.9972, 120.2185, "Starbucks Tainan NCKU (East District)", "Starbucks Tainan NCKU"),
        (2, "Candidate C: Hayashi Department Store (West Central)", 22.9918, 120.2020, "Hayashi Department Store (West Central)", "Hayashi Department Store")
    ],
    "taipei.html": [
        (0, "Candidate A: Starbucks Taipei Yongkang (Da'an District)", 25.0322, 121.5298, "Starbucks Taipei Yongkang (Da'an District)", "Starbucks Taipei Yongkang"),
        (1, "Candidate B: Starbucks ATT 4 FUN (Xinyi District)", 25.0354, 121.5658, "Starbucks ATT 4 FUN (Xinyi District)", "Starbucks ATT 4 FUN"),
        (2, "Candidate C: Starbucks Zhongshan MRT (Zhongshan District)", 25.0522, 121.5205, "Starbucks Zhongshan MRT (Zhongshan District)", "Starbucks Zhongshan MRT")
    ]
}

def update_candidates_py():
    path = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web\update_candidates.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    for fname, updates in SHOP_UPDATES.items():
        pattern = f'"{fname}"\\s*:\\s*"""\\[(.*?)\\]"""'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            print(f"Failed to find city block for {fname} in update_candidates.py")
            continue
            
        block_content = match.group(1)
        obj_matches = list(re.finditer(r'\{([^}]+)\}', block_content, re.DOTALL))
        
        new_block_content = block_content
        for idx, obj_match in reversed(list(enumerate(obj_matches))):
            if idx >= len(updates):
                continue
            _, new_cand_name, new_lat, new_lng, _, new_ref = updates[idx]
            
            obj_str = obj_match.group(0)
            obj_str = re.sub(r'name:\s*"(.*?)"', f'name: "{new_cand_name}"', obj_str)
            obj_str = re.sub(r'lat:\s*[0-9.-]+', f'lat: {new_lat}', obj_str)
            obj_str = re.sub(r'lng:\s*[0-9.-]+', f'lng: {new_lng}', obj_str)
            
            # Clean and prepend correct prefix
            note_match = re.search(r'note:\s*"(.*?)"', obj_str)
            if note_match:
                note_val = note_match.group(1)
                note_val = re.sub(r'^(Pinned to|Located at|Located in)\s+.*?\.\s*', '', note_val)
                if any(x in new_ref for x in ["Starbucks", "Highlands", "Coffee", "Cafe", "saco", "Coles", "Sonoma", "Cuckoo", "Tealive"]):
                    prefix = f"Located at {new_ref}."
                elif any(x in new_ref for x in ["Hotel", "Resort", "Theater", "University", "Pub"]):
                    prefix = f"Located at {new_ref}."
                else:
                    prefix = f"Located in {new_ref}."
                note_val = f"{prefix} " + note_val
                obj_str = obj_str.replace(note_match.group(0), f'note: "{note_val}"')
            
            start, end = obj_match.span()
            new_block_content = new_block_content[:start] + obj_str + new_block_content[end:]
            
        content = content.replace(block_content, new_block_content)
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully updated update_candidates.py")

def update_location_tables_py():
    path = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web\update_location_tables.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    for fname, updates in SHOP_UPDATES.items():
        pattern = f'"{fname}"\\s*:\\s*"""<tbody>(.*?)</tbody>"""'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            print(f"Failed to find table block for {fname} in update_location_tables.py")
            continue
            
        block_content = match.group(1)
        rows = list(re.finditer(r'<tr[^>]*>.*?</tr>', block_content, re.DOTALL))
        
        new_block_content = block_content
        for idx, row_match in reversed(list(enumerate(rows))):
            if idx >= len(updates):
                continue
            _, _, _, _, new_table_name, _ = updates[idx]
            
            row_str = row_match.group(0)
            td_match = re.search(r'<td>(.*?)</td>', row_str, re.DOTALL)
            if td_match:
                row_str = row_str.replace(td_match.group(0), f"<td>{new_table_name}</td>")
                start, end = row_match.span()
                new_block_content = new_block_content[:start] + row_str + new_block_content[end:]
                
        content = content.replace(block_content, new_block_content)
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully updated update_location_tables.py")

if __name__ == "__main__":
    update_candidates_py()
    update_location_tables_py()
