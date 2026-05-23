"""
apply_map_links.py
Automates the integration of direct Google Maps links and expat nationalities
across all 27 subpage HTML files for Oasis Salon.
"""
import os
import re
import glob
import json
import urllib.parse

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

# Expat nationalities mapping based on city and area name keywords
EXPATS_NATIONALITIES = {
    # HCMC
    "masteri thao dien": "Japanese, Korean & Western Expats",
    "japan town": "Japanese Expats",
    "vinhomes golden river": "Korean, Japanese & Western Expats",
    
    # Hanoi
    "tay ho lakeside": "Western & European Expats",
    "ciputra": "Korean, Japanese & Western Expats",
    
    # Da Nang
    "hai chau": "Western & Asian Expats",
    "an thuong": "Western, Korean & Russian Expats (Digital Nomads)",
    
    # Binh Duong
    "thuan an expat": "Korean & Japanese Expats",
    "thu dau mot corporate": "Korean & Japanese Expats",
    
    # Dong Nai
    "bien hoa expat": "Korean & Japanese Expats",
    
    # Bangkok
    "sathorn": "Western & European Expats",
    "sukhumvit": "Mixed Western, Japanese & Asian Expats",
    "phrom phong": "Japanese Expats",
    
    # Johor Bahru
    "rts bukit chagar": "Singaporean & Malaysian cross-border commuters",
    
    # Kuala Lumpur
    "mont kiara": "Korean & Japanese Expats",
    "bangsar": "Western & European Expats",
    "klcc / ampang": "Western, European & Middle Eastern Expats",
    
    # Penang
    "gurney drive": "Western, Japanese & British retirees/expats",
    "tanjung tokong": "Western, Japanese & Korean Expats",
    
    # Sabah
    "likas bay": "Korean, Japanese & Western Expats",
    "sutera harbour": "Korean, Japanese & Western Expats",
    
    # Sarawak
    "waterfront heritage": "British & European Expats",
    "jalan song": "British & European Expats (Shell/Petronas)",
    
    # Singapore
    "orchard": "Western, British & Japanese Expats",
    "tanjong pagar": "Western & European Expats",
    "river valley": "Western, British & Japanese Expats",
    
    # Sydney
    "double bay": "British, American & European Expats",
    "paddington terrace": "British, American & European Expats",
    "surry hills": "British, American & European Expats",
    
    # Melbourne
    "south yarra": "British, European & Asian Expats",
    "fitzroy": "British, European & Western Expats",
    "east melbourne": "British, European & Western Expats",
    
    # Brisbane
    "fortitude valley": "British & European Expats",
    "ascot / hamilton": "British, European & Kiwi Expats",
    "paddington qld": "Western & European Expats",
    
    # Perth
    "subiaco": "British & European Expats",
    "cottesloe": "British & European Expats",
    "dalkeith": "British & European Expats",
    
    # Fukuoka
    "daimyo/tenjin": "Western, Korean & Chinese Expats",
    "ohori park": "Western & Asian Expats",
    
    # Okinawa
    "omoromachi": "American & Western Expats",
    "kumoji": "American & Western Expats",
    
    # Taipei
    "da'an": "Japanese, American & Western Expats",
    "songshan": "Japanese & Western Expats",
    
    # Taichung
    "7th district": "Japanese & Western Expats",
    "west district": "Japanese & Western Expats",
    
    # Tainan
    "west central": "Japanese & Western Expats",
    "east district ncku": "Japanese & Western Expats",
    "sinshih district": "Japanese, US & European TSMC engineers/expats",
    
    # Kaohsiung
    "gushan": "Japanese & Western Expats",
    "sanduo": "Japanese & Western Expats",
    
    # Busan
    "marine city": "Western, Japanese & Chinese Expats",
    "haeundae": "Western & Asian Expats",
    "centum city": "Western & Asian Expats",
    
    # Dubai
    "jumeirah": "British, American & European Expats",
    "dubai marina": "European, British & Russian Expats",
    "palm jumeirah": "European, British & Russian Expats",
    
    # Macau
    "taipa central": "Western & Hong Kong Expats (Casino management)",
    "nape premium": "Western & Hong Kong Expats",
    "fai chi kei": "Mainland Chinese & Hong Kong Expats"
}

def parse_javascript_objects(array_str):
    blocks = re.findall(r"\{([^}]+)\}", array_str, re.DOTALL)
    objects = []
    for b in blocks:
        obj = {}
        name_match = re.search(r"name\s*:\s*([\"'`])(.*?)\1", b)
        if name_match:
            obj["name"] = name_match.group(2)
        else:
            name_match2 = re.search(r"\"name\"\s*:\s*([\"'`])(.*?)\1", b)
            if name_match2:
                obj["name"] = name_match2.group(2)
        
        lat_match = re.search(r"lat\s*:\s*(-?\d+\.\d+)", b)
        if lat_match:
            obj["lat"] = float(lat_match.group(1))
        
        lng_match = re.search(r"lng\s*:\s*(-?\d+\.\d+)", b)
        if lng_match:
            obj["lng"] = float(lng_match.group(1))
        elif re.search(r"lon\s*:\s*(-?\d+\.\d+)", b):
            obj["lng"] = float(re.search(r"lon\s*:\s*(-?\d+\.\d+)", b).group(1))
            
        # radius
        radius_match = re.search(r"radius\s*:\s*(\d+)", b)
        if radius_match:
            obj["radius"] = int(radius_match.group(1))
        
        # estPop
        pop_match = re.search(r"estPop\s*:\s*(\d+)", b)
        if pop_match:
            obj["estPop"] = int(pop_match.group(1))
            
        objects.append(obj)
    return objects

def format_js_array(obj_list):
    lines = ["[\n"]
    for obj in obj_list:
        item_parts = []
        key_order = ["name", "lat", "lng", "radius", "estPop", "nationality"]
        for k in obj:
            if k not in key_order:
                key_order.append(k)
        
        for k in key_order:
            if k in obj:
                v = obj[k]
                if isinstance(v, str):
                    escaped_v = v.replace('"', '\\"')
                    item_parts.append(f'{k}: "{escaped_v}"')
                elif isinstance(v, (int, float)):
                    item_parts.append(f'{k}: {v}')
                else:
                    item_parts.append(f'{k}: {json.dumps(v)}')
        lines.append("            { " + ", ".join(item_parts) + " },\n")
    if len(obj_list) > 0:
        lines[-1] = lines[-1].rstrip(",\n") + "\n"
    lines.append("        ]")
    return "".join(lines)

def find_loop_block(content, loop_prefix):
    start_match = re.search(re.escape(loop_prefix), content)
    if not start_match:
        pattern = re.sub(r'\\\s+', r'\\s+', re.escape(loop_prefix))
        start_match = re.search(pattern, content)
        if not start_match:
            return None
    start_idx = start_match.start()
    brace_start = content.find('{', start_idx)
    if brace_start == -1:
        return None
    
    open_braces = 1
    idx = brace_start + 1
    while open_braces > 0 and idx < len(content):
        if content[idx] == '{':
            open_braces += 1
        elif content[idx] == '}':
            open_braces -= 1
        idx += 1
        
    end_idx = idx
    while end_idx < len(content) and content[end_idx] in (' ', '\t', '\n', '\r'):
        end_idx += 1
    if end_idx < len(content) and content[end_idx] == ')':
        end_idx += 1
    while end_idx < len(content) and content[end_idx] in (' ', '\t', '\n', '\r'):
        end_idx += 1
    if end_idx < len(content) and content[end_idx] == ';':
        end_idx += 1
        
    return start_idx, end_idx

def find_matching_competitor(table_name, js_competitors):
    t_name_clean = table_name.lower().strip()
    t_name_clean = re.sub(r'\(.*?\)', '', t_name_clean).strip()
    t_name_clean = t_name_clean.replace("&amp;", "&")
    
    for js_comp in js_competitors:
        js_name_clean = js_comp['name'].lower().strip()
        js_name_clean = re.sub(r'\(.*?\)', '', js_name_clean).strip()
        js_name_clean = js_name_clean.replace("&amp;", "&")
        
        if t_name_clean in js_name_clean or js_name_clean in t_name_clean:
            return js_comp
            
        t_words = re.findall(r'\w+', t_name_clean)
        js_words = re.findall(r'\w+', js_name_clean)
        if t_words and js_words:
            if t_words[0] == js_words[0] and len(t_words[0]) >= 3:
                return js_comp
    return None

def process_file(path):
    name = os.path.basename(path)
    content = open(path, "r", encoding="utf-8").read()
    
    # Extract data-city
    city_match = re.search(r'<body data-city="([^"]+)"', content)
    city = city_match.group(1) if city_match else name.split(".")[0].capitalize()
    
    # 1. Parse JS data arrays
    cands_match = re.search(r"(?:const|let)\s+candidates\s*=\s*(\[.*?\]);", content, re.DOTALL)
    if not cands_match:
        print(f"  [ERROR]: candidates list not found in {name}")
        return False
    cands = parse_javascript_objects(cands_match.group(1))
    
    comps_match = re.search(r"(?:const|let)\s+competitors\s*=\s*(\[.*?\]);", content, re.DOTALL)
    if not comps_match:
        print(f"  [ERROR]: competitors list not found in {name}")
        return False
    comps = parse_javascript_objects(comps_match.group(1))
    
    # 2. Update residential array with nationalities
    res_match = re.search(r"(const|let)\s+residential\s*=\s*(\[.*?\]);", content, re.DOTALL)
    if res_match:
        res_var = res_match.group(1)
        res_list = parse_javascript_objects(res_match.group(2))
        
        # Map nationalities
        for r_obj in res_list:
            r_name_lower = r_obj.get("name", "").lower().strip()
            # find match
            found_nat = "Mixed Expats"
            for k, v in EXPATS_NATIONALITIES.items():
                if k in r_name_lower:
                    found_nat = v
                    break
            r_obj["nationality"] = found_nat
            
        new_res_decl = f"{res_var} residential = {format_js_array(res_list)};"
        content = content.replace(res_match.group(0), new_res_decl, 1)
        
    # 3. Update map scripts loops
    # Replace residential.forEach loop
    res_range = find_loop_block(content, "residential.forEach")
    if res_range:
        color = "#c6a87c"
        fillColor = "#c6a87c"
        loop_text = content[res_range[0]:res_range[1]]
        color_m = re.search(r"color:\s*['\"](#?[a-zA-Z0-9]+)['\"]", loop_text)
        if color_m: color = color_m.group(1)
        fillColor_m = re.search(r"fillColor:\s*['\"](#?[a-zA-Z0-9]+)['\"]", loop_text)
        if fillColor_m: fillColor = fillColor_m.group(1)
        
        new_res_loop = f"""residential.forEach(res => {{
            const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${{res.lat}},${{res.lng}}`;
            let natText = res.nationality ? `<p><strong>Nationalities:</strong> ${{res.nationality}}</p>` : "";
            L.circle([res.lat, res.lng], {{
                color: '{color}',
                fillColor: '{fillColor}',
                fillOpacity: 0.15,
                weight: 1.5,
                radius: res.radius
            }}).addTo(map).bindPopup(`
                <div class="popup-content">
                    <h3 style="color: {color};"><a href="${{mapsUrl}}" target="_blank" style="color: inherit; text-decoration: none;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">${{res.name}}</a></h3>
                    <p><strong>Expat Residential Hub</strong></p>
                    ${{natText}}
                    <p><strong>Est. Population:</strong> ~${{res.estPop.toLocaleString()}} residents</p>
                    <p style="margin-top: 8px;"><a href="${{mapsUrl}}" target="_blank" style="color: {color}; text-decoration: underline; font-weight: bold;">📍 View on Google Maps</a></p>
                </div>
            `);
        }});"""
        content = content[:res_range[0]] + new_res_loop + content[res_range[1]:]
        
    # Replace malls.forEach loop
    malls_range = find_loop_block(content, "malls.forEach")
    if malls_range:
        color = "#c6a87c"
        fillColor = "#fff"
        loop_text = content[malls_range[0]:malls_range[1]]
        color_m = re.search(r"color:\s*['\"](#?[a-zA-Z0-9]+)['\"]", loop_text)
        if color_m: color = color_m.group(1)
        fillColor_m = re.search(r"fillColor:\s*['\"](#?[a-zA-Z0-9]+)['\"]", loop_text)
        if fillColor_m: fillColor = fillColor_m.group(1)
        
        new_malls_loop = f"""malls.forEach(loc => {{
            const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${{loc.lat}},${{loc.lng}}`;
            L.circleMarker([loc.lat, loc.lng], {{
                radius: getRadius(loc.footfall),
                fillColor: "{fillColor}",
                color: "{color}",
                weight: 1.5,
                opacity: 1,
                fillOpacity: 0.8
            }}).addTo(map).bindPopup(`
                <div class="popup-content">
                    <h3><a href="${{mapsUrl}}" target="_blank" style="color: inherit; text-decoration: none;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">🛍️ ${{loc.name}}</a></h3>
                    <p><strong>Est. Relative Footfall:</strong> ${{loc.footfall}}/100</p>
                    <p style="margin-top: 8px;"><a href="${{mapsUrl}}" target="_blank" style="color: {color}; text-decoration: underline; font-weight: bold;">📍 View on Google Maps</a></p>
                </div>
            `);
        }});"""
        content = content[:malls_range[0]] + new_malls_loop + content[malls_range[1]:]
        
    # Replace competitors.forEach loop
    comp_range = find_loop_block(content, "competitors.forEach")
    if comp_range:
        color = "#fff"
        fillColor = "#ef4444"
        loop_text = content[comp_range[0]:comp_range[1]]
        color_m = re.search(r"color:\s*['\"](#?[a-zA-Z0-9]+)['\"]", loop_text)
        if color_m: color = color_m.group(1)
        fillColor_m = re.search(r"fillColor:\s*['\"](#?[a-zA-Z0-9]+)['\"]", loop_text)
        if fillColor_m: fillColor = fillColor_m.group(1)
        
        new_comp_loop = f"""competitors.forEach(loc => {{
            const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${{loc.lat}},${{loc.lng}}`;
            L.circleMarker([loc.lat, loc.lng], {{
                radius: getRadius(loc.footfall),
                fillColor: "{fillColor}",
                color: "{color}",
                weight: 1.5,
                opacity: 1,
                fillOpacity: 0.9
            }}).addTo(map).bindPopup(`
                <div class="popup-content">
                    <h3 style="color: {fillColor};"><a href="${{mapsUrl}}" target="_blank" style="color: inherit; text-decoration: none;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">🔴 ${{loc.name}}</a></h3>
                    <p><strong>Price Level:</strong> ${{loc.price}}</p>
                    <p><strong>Est. Footfall Traffic:</strong> ${{loc.footfall}}/100</p>
                    <p><strong>Note:</strong> ${{loc.comment}}</p>
                    <p style="margin-top: 8px;"><a href="${{mapsUrl}}" target="_blank" style="color: {fillColor}; text-decoration: underline; font-weight: bold;">📍 View on Google Maps</a></p>
                </div>
            `);
        }});"""
        content = content[:comp_range[0]] + new_comp_loop + content[comp_range[1]:]
        
    # Replace candidates.forEach loop
    cands_range = find_loop_block(content, "candidates.forEach")
    if cands_range:
        new_cands_loop = """candidates.forEach(loc => {
            const targetDemand = Math.round(loc.catchment * (loc.premiumTargetPct / 100));
            const underservedDemand = Math.max(0, targetDemand - loc.competitorCapacity);
            const underservedPct = Math.round((underservedDemand / targetDemand) * 100);
            const ratio = (underservedDemand / loc.rent).toFixed(2);
            const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${loc.lat},${loc.lng}`;

            L.marker([loc.lat, loc.lng], { icon: starIcon }).addTo(map).bindPopup(`
                <div class="popup-content" style="min-width: 240px; color: #333;">
                    <h3 style="color: var(--accent); font-weight: 600; font-size: 14px; margin-top: 0; margin-bottom: 6px; border-bottom: 1px solid #eee; padding-bottom: 4px;"><a href="${mapsUrl}" target="_blank" style="color: inherit; text-decoration: none;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">✨ ${loc.name}</a></h3>
                    <p style="margin: 4px 0; font-size: 12px; color: #666; line-height: 1.4;">${loc.note}</p>
                    <hr style="margin: 6px 0; border: 0; border-top: 1px solid #eee;">
                    <p style="margin: 3px 0; font-size: 11px; display: flex; justify-content: space-between;"><span>Monthly Catchment:</span> <strong style="color: #111;">${loc.catchment.toLocaleString()} pax</strong></p>
                    <p style="margin: 3px 0; font-size: 11px; display: flex; justify-content: space-between;"><span>Premium Target Segment:</span> <strong style="color: #111;">${loc.premiumTargetPct}%</strong></p>
                    <p style="margin: 3px 0; font-size: 11px; display: flex; justify-content: space-between;"><span>Monthly Premium Demand:</span> <strong style="color: #111;">${targetDemand.toLocaleString()} visits</strong></p>
                    <p style="margin: 3px 0; font-size: 11px; display: flex; justify-content: space-between;"><span>Nearby Competitor Capacity:</span> <strong style="color: #111;">${loc.competitorCapacity.toLocaleString()} visits</strong></p>
                    <p style="margin: 3px 0; font-size: 11px; display: flex; justify-content: space-between;"><span>Underserved Demand Gap:</span> <strong style="color: #e11d48;">${underservedDemand.toLocaleString()} visits (${underservedPct}%)</strong></p>
                    <p style="margin: 3px 0; font-size: 11px; display: flex; justify-content: space-between;"><span>Airport Travel Time:</span> <strong style="color: #111;">${loc.airportTime}</strong></p>
                    <p style="margin: 3px 0; font-size: 11px; display: flex; justify-content: space-between;"><span>Monthly Rent:</span> <strong style="color: #111;">USD ${loc.rent.toLocaleString()}</strong></p>
                    <div style="background: rgba(198,168,124,0.15); padding: 8px; border-radius: 6px; border-left: 3px solid var(--accent); margin-top: 8px; margin-bottom: 8px;">
                        <strong style="color: var(--accent); font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 2px;">Potential Customer to Rent Ratio:</strong>
                        <span style="font-size: 14px; font-weight: bold; color: #111;">${ratio} potential customers/USD 1 rent</span>
                    </div>
                    <p style="margin-top: 8px; text-align: center;"><a href="${mapsUrl}" target="_blank" style="color: var(--accent); text-decoration: underline; font-weight: bold; font-size: 12px;">📍 View on Google Maps</a></p>
                </div>
            `);
        });"""
        content = content[:cands_range[0]] + new_cands_loop + content[cands_range[1]:]
        
    # Manual check for johor.html Transit Corridor
    if "johor.html" in name:
        johor_circle_pattern = r"L\.circle\(\[1\.464,\s*103\.768\].*?\.bindPopup\(`.*?`\);"
        new_johor_circle = """L.circle([1.464, 103.768], {
            color: '#c6a87c',
            fillColor: '#c6a87c',
            fillOpacity: 0.15,
            weight: 1.5,
            radius: 350
        }).addTo(map).bindPopup(`
            <div class="popup-content">
                <h3 style="color: #c6a87c;"><a href="https://www.google.com/maps/search/?api=1&query=1.464,103.768" target="_blank" style="color: inherit; text-decoration: none;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">RTS Bukit Chagar Terminal Area</a></h3>
                <p><strong>Primary Transit Hub</strong></p>
                <p><strong>Nationalities:</strong> Singaporean & Malaysian cross-border commuters</p>
                <p>Over 10,000 hourly commuters expected upon RTS completion. High Singaporean day-tripper density.</p>
                <p style="margin-top: 8px;"><a href="https://www.google.com/maps/search/?api=1&query=1.464,103.768" target="_blank" style="color: #c6a87c; text-decoration: underline; font-weight: bold;">📍 View on Google Maps</a></p>
            </div>
        `);"""
        content = re.sub(johor_circle_pattern, new_johor_circle, content, flags=re.DOTALL)

    # 4. Update Table 5 (Location study table)
    tbody_match = re.search(r'(<section id="location-study".*?)(<tbody>.*?</tbody>)', content, re.DOTALL)
    if tbody_match:
        section_part = tbody_match.group(1)
        tbody_html = tbody_match.group(2)
        
        # Find rows
        rows = re.findall(r'<tr[^>]*>.*?</tr>', tbody_html, re.DOTALL)
        new_rows = []
        for idx, r in enumerate(rows):
            td_match = re.search(r'<td([^>]*)>(.*?)</td>', r, re.DOTALL)
            if td_match and idx < len(cands):
                td_attrs = td_match.group(1)
                td_content = td_match.group(2)
                
                if "href=" not in td_content and "<a" not in td_content:
                    lat, lng = cands[idx]["lat"], cands[idx]["lng"]
                    link = f'<a href="https://www.google.com/maps/search/?api=1&query={lat},{lng}" target="_blank">{td_content}</a>'
                    new_td = f'<td{td_attrs}>{link}</td>'
                    r = r.replace(td_match.group(0), new_td, 1)
            new_rows.append(r)
        
        new_tbody = "<tbody>\n" + "\n".join(new_rows) + "\n</tbody>"
        content = content.replace(tbody_html, new_tbody, 1)

    # 5. Update Table 6 (Competitor study table)
    tbody_match_comp = re.search(r'(<section id="competitors".*?)(<tbody>.*?</tbody>)', content, re.DOTALL)
    if tbody_match_comp:
        section_part = tbody_match_comp.group(1)
        tbody_html = tbody_match_comp.group(2)
        
        # Determine comp_col_idx based on table headers
        thead_match = re.search(r'<thead>(.*?)</thead>', section_part, re.DOTALL)
        comp_col_idx = 0
        if thead_match:
            headers = re.findall(r'<th[^>]*>(.*?)</th>', thead_match.group(1), re.DOTALL)
            headers_clean = [re.sub(r'<[^>]+>', '', h).strip() for h in headers]
            if headers_clean and headers_clean[0].lower().startswith("type"):
                comp_col_idx = 1
                
        rows = re.findall(r'<tr[^>]*>.*?</tr>', tbody_html, re.DOTALL)
        new_rows = []
        for r in rows:
            tds = re.findall(r'<td[^>]*>.*?</td>', r, re.DOTALL)
            if len(tds) > comp_col_idx:
                target_td = tds[comp_col_idx]
                td_match = re.search(r'<td([^>]*)>(.*?)</td>', target_td, re.DOTALL)
                if td_match:
                    td_attrs = td_match.group(1)
                    td_content = td_match.group(2)
                    
                    if "href=" not in td_content and "<a" not in td_content:
                        raw_name = re.sub(r'<[^>]+>', '', td_content).strip()
                        raw_name = raw_name.replace("&amp;", "&")
                        
                        match = find_matching_competitor(raw_name, comps)
                        if match:
                            lat, lng = match["lat"], match["lng"]
                            link = f'https://www.google.com/maps/search/?api=1&query={lat},{lng}'
                        else:
                            # Clean query string
                            clean_q = re.sub(r'\(.*?\)', '', raw_name).strip()
                            query_str = f"{clean_q}, {city}"
                            encoded_q = urllib.parse.quote_plus(query_str)
                            link = f'https://www.google.com/maps/search/?api=1&query={encoded_q}'
                            
                        new_link_html = f'<a href="{link}" target="_blank">{td_content}</a>'
                        new_td = f'<td{td_attrs}>{new_link_html}</td>'
                        r = r.replace(target_td, new_td, 1)
            new_rows.append(r)
            
        new_tbody = "<tbody>\n" + "\n".join(new_rows) + "\n</tbody>"
        content = content.replace(tbody_html, new_tbody, 1)
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def main():
    print("=== STARTING MAP INTEGRATION UPDATE ===")
    files = glob.glob(os.path.join(WORKDIR, "*.html"))
    updated = 0
    for f in sorted(files):
        name = os.path.basename(f)
        if name == "index.html":
            continue
        try:
            success = process_file(f)
            if success:
                print(f"  [SUCCESS] Updated {name}")
                updated += 1
        except Exception as e:
            print(f"  [ERROR] Failed to process {name}: {e}")
            
    print(f"\nDone. Updated {updated} files out of {len(files) - 1} subpages.")

if __name__ == "__main__":
    main()
