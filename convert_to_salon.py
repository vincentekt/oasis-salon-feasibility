import json
import re
import os

# Define folders
WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
JSON_DB_PATH = r"C:\Users\vince\.gemini\antigravity\brain\2679f13b-3258-4ac7-9d03-21d60bdc0cdc\scratch\cities_parsed.json"

TAX_RATES = {
    "bangkok.html": 0.20,
    "binhduong.html": 0.20,
    "danang.html": 0.20,
    "dongnai.html": 0.20,
    "haiphong.html": 0.20,
    "hanoi.html": 0.20,
    "hcmc.html": 0.20,
    "hongkong.html": 0.165,
    "johor.html": 0.24,
    "kuala_lumpur.html": 0.24,
    "penang.html": 0.24,
    "singapore.html": 0.17,
    "taichung.html": 0.20,
    "tainan.html": 0.20,
    "taipei.html": 0.20,
    "brisbane.html": 0.30,
    "melbourne.html": 0.30,
    "perth.html": 0.30,
    "sydney.html": 0.30,
    "fukuoka.html": 0.30,
    "okinawa.html": 0.30,
    "busan.html": 0.20,
    "dubai.html": 0.09,
    "macau.html": 0.12,
    "sabah.html": 0.24,
    "sarawak.html": 0.24,
    "kaohsiung.html": 0.20
}

# 1. Format replacements helper
def format_replacement(fmt):
    repls = {
        "Premium Boutique (MVP)": "Premium Boutique Salon (MVP)",
        "Boutique (MVP)": "Boutique Salon (MVP)",
        "Boutique PoC": "Boutique Salon PoC",
        "Luxury Suite PoC": "Luxury Salon Suite PoC",
        "Boutique Salon / PoC": "Boutique Salon PoC",
        "Luxury Suite": "Salon Suite",
        "Ultra-Luxury Suite": "Premium Salon Suite",
        "Micro-Spa": "Micro-Salon",
        "Expat PoC": "Expat Salon PoC",
        "Expat PoC / MVP": "Expat Salon PoC / MVP",
        "Seaside Resort PoC / MVP": "Seaside Resort Salon PoC / MVP",
        "Metro Port PoC / MVP": "Metro Port Salon PoC / MVP",
        "Cross-Border PoC": "Cross-Border Salon PoC",
        "Aesthetic Lane Spa": "Aesthetic Lane Salon",
        "Heritage Boutique PoC": "Heritage Boutique Salon PoC",
        "Hair Spa": "Hair Salon",
        "Spa": "Salon"
    }
    for k, v in repls.items():
        if k in fmt:
            return fmt.replace(k, v)
    return fmt + " Salon" if "Salon" not in fmt else fmt

def scale_capex_str(capex_str):
    matches = re.findall(r'(\d+)k', capex_str)
    if len(matches) == 2:
        cmin = int(matches[0]) * 0.60
        cmax = int(matches[1]) * 0.60
        return f"USD {round(cmin)}k - {round(cmax)}k", round(cmin)*1000, round(cmax)*1000
    elif len(matches) == 1:
        cval = int(matches[0]) * 0.60
        return f"USD {round(cval)}k", round(cval)*1000, round(cval)*1000
    else:
        num_match = re.search(r'\d+', capex_str.replace(',', ''))
        if num_match:
            num = int(num_match.group(0))
            if num < 1000:
                cval = num * 1000 * 0.60
            else:
                cval = num * 0.60
            return f"USD {round(cval):,}", round(cval), round(cval)
        return capex_str, 50000, 50000

def get_original_numeric_value(val_str):
    num_match = re.search(r'\d+', val_str.replace(',', ''))
    if num_match:
        return int(num_match.group(0))
    return 0

def scale_cities_db(cities):
    scaled_cities = []
    scaled_volumes = {}
    
    for city in cities:
        name = city['name']
        url = city['url']
        tax_rate = TAX_RATES.get(url, 0.20)
        
        # Read parameters
        ticket_raw = get_original_numeric_value(city['ticket'])
        opex_raw = get_original_numeric_value(city['opex'])
        volume_raw = city.get('volume', 300) # Fallback to 300 if missing
        
        # Scale parameters
        ticket_val = round(ticket_raw * 0.65)
        opex_val = round(opex_raw * 0.80)
        volume_val = round(volume_raw * 1.15)
        
        capex_str, capex_min, capex_max = scale_capex_str(city['capex'])
        capex_mid = (capex_min + capex_max) / 2
        
        # Underserved
        u_val = float(city['underserved'].replace('%','')) / 100.0
        u_new = max(0.0, 1.25 * u_val - 0.25)
        u_str = f"{round(u_new * 100)}%"
        
        # Format string
        fmt_str = format_replacement(city['format'])
        
        # COGS and Math
        cogs_val = ticket_val * 0.10
        contrib = ticket_val - cogs_val
        breakeven_m = round(opex_val / contrib)
        breakeven_d = round(breakeven_m / 30, 1)
        
        # Post tax math
        pre_tax_profit = volume_val * contrib - opex_val
        tax_val = pre_tax_profit * tax_rate if pre_tax_profit > 0 else 0
        pat = pre_tax_profit - tax_val
        ratio = round((pat / opex_val) * 100) if opex_val > 0 else 0
        payback = round(capex_mid / pat) if pat > 0 else 99
        
        payback_str = f"{payback} Months" if payback > 0 else "N/A"
        ratio_str = f"{ratio}% (Post-Tax)"
        
        # Complexity design scaling
        if 'complexity' in city and city['complexity']:
            comp = city['complexity'].copy()
            design_match = re.search(r'(\d+)\s*hrs', comp.get('design', ''))
            if design_match:
                design_hrs = int(design_match.group(1))
                new_design_hrs = round(design_hrs * 0.50)
                comp['design'] = comp['design'].replace(f"{design_hrs} hrs", f"{new_design_hrs} hrs")
                comp['design'] = comp['design'].replace("VIP pods", "styling stations").replace("VIP suites", "styling suites").replace("VIP starlight", "lighting designs")
                comp['total'] = comp['total'] - (design_hrs - new_design_hrs)
            if 'staff' in comp:
                comp['staff'] = comp['staff'].replace("VIP", "Stylist")
            if 'logistics' in comp:
                comp['logistics'] = comp['logistics'].replace("OEM wash beds", "styling chairs")
        else:
            comp = {
                "total": 200,
                "loc": "60 hrs (Location search)",
                "design": "60 hrs (Styling stations layout)",
                "staff": "80 hrs (Hiring & styling training)",
                "logistics": "40 hrs (Equipment delivery)"
            }
        
        # Create copy and scale
        new_city = {
            "name": name,
            "region": city['region'],
            "format": fmt_str,
            "size": city['size'],
            "capex": capex_str,
            "opex": f"USD {opex_val:,}",
            "ticket": f"USD {ticket_val}",
            "cogs": f"USD {cogs_val:.2f}",
            "margin": "90%",
            "breakeven": f"~{breakeven_m} customers",
            "daily_breakeven": f"~{breakeven_d} customers/day",
            "tax": f"{tax_rate*100:.1f}%",
            "pat_ratio": ratio_str,
            "payback": payback_str,
            "underserved": u_str,
            "airport": city['airport'],
            "risk": city['risk'].replace("salon", "hair salon").replace("Spa", "Salon").replace("spa", "salon"),
            "complexity": comp,
            "coords": city['coords'],
            "url": url
        }
        
        scaled_cities.append(new_city)
        
        key = url.replace('.html', '')
        scaled_volumes[key] = volume_val
        
    return scaled_cities, scaled_volumes

def update_script_js(scaled_cities, scaled_volumes):
    path = os.path.join(WORKDIR, "script.js")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace citiesDb
    start_idx = content.find("const citiesDb = [")
    if start_idx == -1:
        print("Could not find const citiesDb in script.js")
        return
        
    bracket_count = 1
    end_idx = start_idx + len("const citiesDb = [")
    while bracket_count > 0 and end_idx < len(content):
        if content[end_idx] == '[':
            bracket_count += 1
        elif content[end_idx] == ']':
            bracket_count -= 1
        end_idx += 1
        
    cities_js = "const citiesDb = " + json.dumps(scaled_cities, indent=4) + ";"
    content = content[:start_idx] + cities_js + content[end_idx:]
    
    # Replace volumesDb
    vol_start = content.find("const volumesDb = {")
    if vol_start == -1:
        print("Could not find const volumesDb in script.js")
        return
        
    brace_count = 1
    vol_end = vol_start + len("const volumesDb = {")
    while brace_count > 0 and vol_end < len(content):
        if content[vol_end] == '{':
            brace_count += 1
        elif content[vol_end] == '}':
            brace_count -= 1
        vol_end += 1
        
    volumes_js = "const volumesDb = " + json.dumps(scaled_volumes, indent=4) + ";"
    content = content[:vol_start] + volumes_js + content[vol_end:]
    
    # Simplify state retrieval to default to salon
    content = content.replace("return { lang, model: 'spa' };", "return { lang, model: 'salon' };")
    
    # Update updateEconomicsTable to the robust header-matching implementation
    econ_start = content.find("function updateEconomicsTable")
    if econ_start != -1:
        econ_end = content.find("function scaleOPEXTable", econ_start)
        if econ_end != -1:
            robust_econ_js = """function updateEconomicsTable(ticket, opex, baseVol, taxRate, capexMid) {
        const econTable = document.querySelector('#economics table');
        if (!econTable) return;
        
        const headers = Array.from(econTable.querySelectorAll('thead th')).map(th => th.textContent.trim().toLowerCase());
        const rows = Array.from(econTable.querySelectorAll('tbody tr'));
        
        const cogs = ticket * 0.10;
        const contribMargin = ticket - cogs;
        
        let scenarios = [];
        if (rows.length === 4) {
            scenarios = [
                { name: "Low Case", vol: Math.round(baseVol * 0.60) },
                { name: "Breakeven", vol: Math.round(opex / contribMargin) },
                { name: "Base Case", vol: Math.round(baseVol) },
                { name: "High Case", vol: Math.round(baseVol * 1.60) }
            ];
        } else {
            scenarios = [
                { name: "Breakeven Case", vol: Math.round(opex / contribMargin) },
                { name: "Base Case", vol: Math.round(baseVol) },
                { name: "High-Performance Case", vol: Math.round(baseVol * 1.25) }
            ];
        }
        
        scenarios.forEach((scen, idx) => {
            const row = rows[idx];
            if (!row) return;
            
            const rev = scen.vol * ticket;
            const cogVal = scen.vol * cogs;
            const netProfit = rev - cogVal - opex;
            const dailyVol = (scen.vol / 30).toFixed(1);
            
            headers.forEach((header, colIdx) => {
                const cell = row.cells[colIdx];
                if (!cell) return;
                if (colIdx === 0) return;
                
                if (header.includes("customers/day") || header.includes("customers / day")) {
                    cell.textContent = dailyVol;
                } else if (header.includes("monthly customers") || header.includes("customers")) {
                    cell.textContent = `${scen.vol.toLocaleString()} customers`;
                } else if (header.includes("revenue")) {
                    cell.textContent = `$${Math.round(rev).toLocaleString()}`;
                } else if (header.includes("cogs")) {
                    cell.textContent = `$${Math.round(cogVal).toLocaleString()}`;
                } else if (header.includes("opex") || header.includes("operating opex")) {
                    cell.textContent = `$${Math.round(opex).toLocaleString()}`;
                } else if (header.includes("net profit") || header.includes("profit")) {
                    if (netProfit < 0) {
                        cell.textContent = `-$${Math.abs(Math.round(netProfit)).toLocaleString()}`;
                        cell.style.color = "#ff4d4d";
                    } else {
                        cell.textContent = `+$${Math.round(netProfit).toLocaleString()}`;
                        cell.style.color = "#00e676";
                    }
                }
            });
        });
        
        const conclusionBox = document.querySelector('#economics .conclusion-box');
        if (conclusionBox) {
            const preTaxPAT = (baseVol * contribMargin) - opex;
            const taxVal = preTaxPAT > 0 ? preTaxPAT * taxRate : 0;
            const pat = preTaxPAT - taxVal;
            const ratio = Math.round((pat / opex) * 100);
            const payback = pat > 0 ? (capexMid / pat).toFixed(1) : "N/A";
            
            const lang = getActiveState().lang;
            const isJa = lang === 'ja';
            const isVi = lang === 'vi';
            
            let html = '';
            if (isJa) {
                html = `
                    <h3 style="color: var(--success); font-size: 1.2rem; margin-bottom: 0.5rem; font-family: var(--font-heading);">税後財務フィジビリティ分析</h3>
                    <p>上記テーブル内の数値はすべて税引前の値です。各都市の法人税率 <strong>${(taxRate * 100).toFixed(1)}%</strong> を反映した、基本シナリオの税後シミュレーションは以下の通りです:</p>
                    <ul style="margin-top: 0.5rem; margin-left: 1.5rem; list-style-type: disc;">
                        <li><strong>基本シナリオ 税引前月間純利益:</strong> USD ${Math.round(preTaxPAT).toLocaleString()}</li>
                        <li><strong>推定月間法人税額:</strong> USD ${Math.round(taxVal).toLocaleString()}</li>
                        <li><strong>税引後月間純利益 (PAT):</strong> USD ${Math.round(pat).toLocaleString()}</li>
                        <li><strong>税引後利益/運営費比率:</strong> <strong>${ratio}% (税後)</strong></li>
                        <li><strong>税引後投資回収期間:</strong> <strong>${payback}ヶ月</strong></li>
                    </ul>
                `;
            } else if (isVi) {
                html = `
                    <h3 style="color: var(--success); font-size: 1.2rem; margin-bottom: 0.5rem; font-family: var(--font-heading);">Phân tích tính khả thi tài chính sau thuế</h3>
                    <p>Tất cả các tính toán trong bảng trên đại diện cho hiệu suất trước thuế. Tính thêm thuế suất TNDN <strong>${(taxRate * 100).toFixed(1)}%</strong> chúng ta có các dự báo sau thuế cho kịch bản cơ sở như sau:</p>
                    <ul style="margin-top: 0.5rem; margin-left: 1.5rem; list-style-type: disc;">
                        <li><strong>Lợi nhuận thuần trước thuế (Kịch bản cơ sở):</strong> USD ${Math.round(preTaxPAT).toLocaleString()}</li>
                        <li><strong>Thuế thu nhập doanh nghiệp ước tính:</strong> USD ${Math.round(taxVal).toLocaleString()}</li>
                        <li><strong>Lợi nhuận thuần sau thuế hàng tháng (PAT):</strong> USD ${Math.round(pat).toLocaleString()}</li>
                        <li><strong>Tỷ lệ lợi nhuận sau thuế / OPEX:</strong> <strong>${ratio}% (sau thuế)</strong></li>
                        <li><strong>Thời gian hoàn vốn sau thuế:</strong> <strong>${payback} tháng</strong></li>
                    </ul>
                `;
            } else {
                html = `
                    <h3 style="color: var(--success); font-size: 1.2rem; margin-bottom: 0.5rem; font-family: var(--font-heading);">Post-Tax Financial Feasibility Analysis</h3>
                    <p>All calculations in the table above represent pre-tax performance. Factoring in the local Corporate Income Tax (CIT) rate of <strong>${(taxRate * 100).toFixed(1)}%</strong>, we arrive at the following post-tax projections for the Base Case:</p>
                    <ul style="margin-top: 0.5rem; margin-left: 1.5rem; list-style-type: disc;">
                        <li><strong>Base Case Pre-Tax Monthly Net Profit:</strong> USD ${Math.round(preTaxPAT).toLocaleString()}</li>
                        <li><strong>Estimated Monthly Corporate Income Tax:</strong> USD ${Math.round(taxVal).toLocaleString()}</li>
                        <li><strong>Post-Tax Net Monthly Profit (PAT):</strong> USD ${Math.round(pat).toLocaleString()}</li>
                        <li><strong>Post-Tax Profit to OPEX Ratio:</strong> <strong>${ratio}% (Post-Tax)</strong></li>
                        <li><strong>Post-Tax CAPEX Payback Period:</strong> <strong>${payback} Months</strong></li>
                    </ul>
                `;
            }
            conclusionBox.innerHTML = html;
        }
    }\n\n    """
            content = content[:econ_start] + robust_econ_js + content[econ_end:]
            
    # Simplify model calculations in script.js to load directly from citiesDb
    content = content.replace("const ticketVal = Math.round(city.ticketVal * (model === 'spa' ? 1.0 : 0.65));", "const ticketVal = city.ticketVal;")
    content = content.replace("const opexVal = Math.round(city.opexVal * (model === 'spa' ? 1.0 : 0.80));", "const opexVal = city.opexVal;")
    content = content.replace("const capexVal = Math.round(city.capexVal * (model === 'spa' ? 1.0 : 0.60));", "const capexVal = city.capexVal;")
    content = content.replace("const volumeBase = Math.round(city.volume * (model === 'spa' ? 1.0 : 1.15));", "const volumeBase = city.volume;")
    content = content.replace("const capexStr = getModelCapex(city.capex, model);", "const capexStr = city.capex;")
    content = content.replace("const opexStr = getModelOpex(city.opex, model);", "const opexStr = city.opex;")
    content = content.replace("const ticketStr = getModelTicket(city.ticket, model);", "const ticketStr = city.ticket;")
    content = content.replace("const formatStr = getModelFormat(city.format, model);", "const formatStr = city.format;")
    
    # In updateSubpageContent
    content = content.replace("const ticketVal = Math.round(city.ticketVal * (model === 'spa' ? 1.0 : 0.65));", "const ticketVal = city.ticketVal;")
    content = content.replace("const opexVal = Math.round(city.opexVal * (model === 'spa' ? 1.0 : 0.80));", "const opexVal = city.opexVal;")
    content = content.replace("const capexVal = Math.round(city.capexVal * (model === 'spa' ? 1.0 : 0.60));", "const capexVal = city.capexVal;")
    content = content.replace("const volumeBase = Math.round(city.volume * (model === 'spa' ? 1.0 : 1.15));", "const volumeBase = city.volume;")
    content = content.replace("const formatStr = getModelFormat(city.format, model);", "const formatStr = city.format;")
    content = content.replace("const capexStr = getModelCapex(city.capex, model);", "const capexStr = city.capex;")
    content = content.replace("const opexStr = getModelOpex(city.opex, model);", "const opexStr = city.opex;")
    content = content.replace("const ticketStr = getModelTicket(city.ticket, model);", "const ticketStr = city.ticket;")
    
    # OPEX and CAPEX scaling in script.js (change factor to 1.0 so we do not scale twice)
    content = content.replace("scaleOPEXTable(model === 'spa' ? 1.0 : 0.80);", "scaleOPEXTable(1.0);")
    content = content.replace("scaleCAPEXTable(model === 'spa' ? 1.0 : 0.60);", "scaleCAPEXTable(1.0);")
    
    # Replace logo name dynamically
    content = content.replace("logo.textContent = 'Oasis Spa';", "logo.textContent = 'Oasis Salon';")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully updated script.js database and functions.")

def convert_html_pages(scaled_cities):
    # Loop over all files
    files = [f for f in os.listdir(WORKDIR) if f.endswith(".html")]
    
    city_map = {c['url']: c for c in scaled_cities}
    
    for file in files:
        path = os.path.join(WORKDIR, file)
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
            
        is_index = file == "index.html"
        
        # 1. Direct string replacements for branding and labels
        html = html.replace("<title>Hong Kong Hair Spa", "<title>Hong Kong Hair Salon")
        html = html.replace("APAC Hair Spa |", "APAC Hair Salon |")
        html = html.replace("<h2>Oasis Spa</h2>", "<h2>Oasis Salon</h2>")
        html = html.replace("<h1>Oasis Head Spa & Salon</h1>", "<h1>Oasis Hair Salon</h1>")
        html = html.replace("Prepared by Antigravity | Global Feasibility Comparison", "Prepared by Antigravity | Global Salon Feasibility Comparison")
        html = html.replace("Prepared by Antigravity | For BINHDUONG Hair Spa Project", "Prepared by Antigravity | For BINHDUONG Hair Salon Project")
        html = html.replace("Prepared by Antigravity | For HONGKONG Hair Spa Project", "Prepared by Antigravity | For HONGKONG Hair Salon Project")
        
        # Replace general branding
        html = re.sub(r'Oasis Spa', 'Oasis Salon', html)
        html = re.sub(r'Hair Spa Project', 'Hair Salon Project', html)
        
        if is_index:
            # Specific updates for index.html
            html = html.replace("Feasibility Study Dashboard", "Hair Salon Feasibility Study Dashboard")
            # Replace recommendations summary text to reflect salon expansion
            html = html.replace("Phase 1: Low-CAPEX PoCs", "Phase 1: Low-CAPEX Salon PoCs")
            html = html.replace("Phase 2: Refined Boutique", "Phase 2: Boutique Salon Suites")
            html = html.replace("Phase 3: High-Yield Premium", "Phase 3: Elite Salon Hubs")
            html = html.replace("low-CAPEX opportunities in HCMC, Johor, and Penang; deploy refined boutique models in Taipei, Kuala Lumpur, Tainan, Brisbane, Perth, and Macau; and scale to high-ticket premium models in Singapore, Taichung, Hong Kong, Sydney, and Melbourne.",
                                "low-CAPEX salon entry points in HCMC, Johor, and Penang; deploy specialized boutique salons in Taipei, Kuala Lumpur, Tainan, Brisbane, Perth, and Macau; and scale to high-yielding premium styling hubs in Singapore, Taichung, Hong Kong, Sydney, and Melbourne.")
            html = html.replace("Proprietary D2C Scalp Products", "Proprietary Salon Retail Lines")
            html = html.replace("Oasis Scalp Wellness Academy", "Oasis Hair Styling Academy")
            html = html.replace("Franchising & Equipment B2B Supply", "Salon Franchising & B2B Supply")
            
        else:
            # Specific updates for subpages
            city_data = city_map.get(file)
            if not city_data:
                print(f"Skipping page conversion for {file} (not in citiesDb)")
                continue
                
            # Title conversion
            title_city = file.replace('.html', '').upper()
            html = html.replace(f"Prepared by Antigravity | For {title_city} Hair Spa Project", f"Prepared by Antigravity | For {title_city} Hair Salon Project")
            html = re.sub(r'<title>([A-Za-z\s]+) Hair Spa \| Business Proposal</title>', r'<title>\1 Hair Salon | Business Proposal</title>', html)
            
            # Positionings text transformation
            html = html.replace("A premium urban sanctuary focused on mental wellness, stress relief, and scientific scalp health. Operated in an exclusive Ginza-style upstairs tower suite to provide absolute privacy and escape from the concrete jungle while maintaining commercial lease viability.",
                                "A premium boutique hair salon specializing in advanced color techniques (balayage, highlight), precision cuts, and luxury scalp-hair therapy. It should operate in upscale, high-visibility upstairs or ground floor units to capture high-value creative color clients while optimizing lease viability.")
            
            html = html.replace("A premium, private scalp wellness spa utilizing Japanese carbonated mist systems, soundproofed VIP treatment pods, and micro-camera analytics. Focuses on service quality and deep relaxation.",
                                "A premium boutique hair salon specializing in advanced color techniques (balayage, highlight), precision cuts, and luxury scalp-hair therapy. Focuses on premium service quality and expert styling.")
                                
            html = html.replace("A standard high-volume hair salon, or a purely clinical/medical trichology center. It must feel like luxury hospitality.",
                                "A standard high-volume discount hair salon, or a purely therapeutic head spa. It must feel like a premium creative design studio.")
                                
            html = html.replace("A standard generic beauty shop, a budget massage center, or a noisy haircut salon.",
                                "A standard generic beauty shop, a budget haircut shop, or a noisy low-end chain salon.")
                                
            html = html.replace('"Your 60-minute escape. Restore your scalp, reset your mind."',
                                '"Your signature look. Expert styling, premium care."')
                                
            html = html.replace("Immediate physiological stress relief (ASMR-style relaxation) paired with visible, camera-proven scalp health improvements.",
                                "Artistic hair transformation, high-end coloring, and deep scalp rejuvenation in a premium aesthetic environment.")
                                
            html = html.replace("Japanese head spa viral videos on TikTok/IG have primed the market demand without sufficient high-end supply.",
                                "Surging demand for premium chemical work (balayage/highlights) and high-quality international styling among affluent professionals and expat communities.")
                                
            html = html.replace("Acoustic isolation, microscopic scanning, Japanese CO2 water systems",
                                "Specialized scalp-hair fusion therapy, damage-free organic colorants, premium styling blowouts")
                                
            html = html.replace("Standard local hair shops. Loud, lack premium private pods.",
                                "Traditional hair salons. Lack specialized scalp care integration, crowded open layouts.")
                                
            html = html.replace("Noisy open layouts, basic wash beds, no private VIP pods",
                                "Crowded open layouts, lack specialized scalp care, standard styling lines")

            # 2. Setup layout replacements
            html = html.replace("Treatment Rooms (3)", "Styling Station Bays (4)")
            html = html.replace("Treatment Rooms", "Styling Station Bays")
            html = html.replace("VIP treatment rooms", "Styling bays")
            html = html.replace("3 Japanese Takara Belmont wash beds, dark aesthetics", "4 premium styling stations, professional vanity setup")
            html = html.replace("4 Private VIP Pods (400 sqft): Soundproofed walls, starlight projection ceilings, Japanese wash beds.",
                                "4 Boutique Styling Stations (400 sqft): Semi-private bays, professional track lighting, styling vanity.")
            html = html.replace("4 VIP Beds (OEM), 800 sq ft", "4 Styling Stations, 2 Backwash Beds, 800 sq ft")
            html = html.replace("4 VIP Beds (OEM)", "4 Styling Chairs, 2 Wash Beds")
            html = html.replace("4 VIP Beds", "4 Styling Chairs")
            html = html.replace("wash beds", "styling chairs")
            html = html.replace("wash bed", "styling chair")
            html = html.replace("Yume Beds", "Styling Chairs")
            html = html.replace("Yume beds", "styling chairs")
            html = html.replace("VIP treatment pods", "styling stations")
            html = html.replace("VIP pods", "styling stations")
            html = html.replace("VIP starlight projection", "modern track lighting")
            html = html.replace("water filtration units", "carbonated hair rinse systems")
            
            # 3. Staffing roles replacements
            html = html.replace("Store Manager / Lead", "Salon Director / Master Stylist")
            html = html.replace("Store Manager", "Salon Director")
            html = html.replace("Senior Therapist", "Senior Hair Stylist")
            html = html.replace("3 Therapists:", "3 Stylist Assistants:")
            html = html.replace("therapists", "stylists")
            html = html.replace("therapist", "stylist")
            html = html.replace("Therapist", "Stylist")
            
            # 4. Service Menu replacements
            html = html.replace("Express Reset", "Express Cut & Blowout")
            html = html.replace("Signature Head Spa", "Precision Cut & Scalp Treatment")
            html = html.replace("Scalp Detox Focus", "Luxury Hair Botox & Rejuvenation")
            html = html.replace("Ultimate Zen", "Signature Balayage & Highlights")
            
            html = html.replace("Executive Reset", "Executive Cut & Blowout")
            html = html.replace("VSIP Industrial Reset", "VSIP Stylist Cut & Blowout")
            html = html.replace("Hard Water Detox", "International Color & Custom Style")
            html = html.replace("Viral Scalp Facial", "Viral Balayage / Accent Highlights")
            html = html.replace("Oxygen Mist Scalp Reset", "Custom Color & Blowout")
            
            # Scale menu items pricing (by 0.65) and opex/capex items programmatically
            # Using simple parser functions
            html = scale_opex_section(html)
            html = scale_capex_section(html)
            html = scale_menu_section(html)
            html = scale_package_section(html)
            html = update_candidates_map_in_html(html)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
            
    print(f"Successfully processed all {len(files)} HTML files for the Salon model.")

# Detailed scaling regex functions
def scale_opex_section(html):
    opex_match = re.search(r'(<section id="opex".*?>)(.*?)(</section>)', html, re.DOTALL)
    if opex_match:
        section_start, content, section_end = opex_match.groups()
        # Scale any dollar amounts like $5,500, $10,500 etc.
        def repl(m):
            val = int(m.group(1).replace(',', ''))
            new_val = round(val * 0.80)
            return f"${new_val:,}"
        new_content = re.sub(r'\$([0-9,]+)', repl, content)
        # Also clean up text labels
        new_content = new_content.replace("Consumables (Shampoo, oil)", "Consumables (Color, dyes, shampoos)")
        return html[:opex_match.start()] + section_start + new_content + section_end + html[opex_match.end():]
    return html

def scale_capex_section(html):
    capex_match = re.search(r'(<section id="capex".*?>)(.*?)(</section>)', html, re.DOTALL)
    if capex_match:
        section_start, content, section_end = capex_match.groups()
        def repl(m):
            val = int(m.group(1).replace(',', ''))
            new_val = round(val * 0.60)
            return f"${new_val:,}"
        new_content = re.sub(r'\$([0-9,]+)', repl, content)
        
        # Scale "USD XXX,XXX" or "USD XXXk"
        def repl_usd(m):
            val = int(m.group(1).replace(',', ''))
            new_val = round(val * 0.60)
            return f"USD {new_val:,}"
        new_content = re.sub(r'USD\s+([0-9,]+)', repl_usd, new_content)
        
        # Scale ranges in title or stats "135k - 160k" -> "81k - 96k"
        def repl_range(m):
            v1 = round(int(m.group(1)) * 0.60)
            v2 = round(int(m.group(2)) * 0.60)
            return f"USD {v1}k - {v2}k"
        new_content = re.sub(r'USD\s+(\d+)k\s*-\s*(\d+)k', repl_range, new_content)
        
        # Replace equipment text
        new_content = new_content.replace("3 Yume Beds", "4 Styling chairs, 2 wash beds")
        new_content = new_content.replace("3 Wash beds", "4 Styling chairs, 2 wash beds")
        new_content = new_content.replace("Wash beds & filtration units", "Styling chairs & rinse stations")
        return html[:capex_match.start()] + section_start + new_content + section_end + html[capex_match.end():]
    return html

def scale_menu_section(html):
    menu_match = re.search(r'(<section id="menu".*?>)(.*?)(</section>)', html, re.DOTALL)
    if menu_match:
        section_start, content, section_end = menu_match.groups()
        def repl(m):
            val = int(m.group(1).replace(',', ''))
            new_val = round(val * 0.65)
            return f"${new_val:,}"
        new_content = re.sub(r'\$([0-9,]+)', repl, content)
        return html[:menu_match.start()] + section_start + new_content + section_end + html[menu_match.end():]
    return html

def scale_package_section(html):
    package_match = re.search(r'(<section id="packages".*?>)(.*?)(</section>)', html, re.DOTALL)
    if package_match:
        section_start, content, section_end = package_match.groups()
        def repl(m):
            val = int(m.group(1).replace(',', ''))
            new_val = round(val * 0.65)
            return f"${new_val:,}"
        new_content = re.sub(r'\$([0-9,]+)', repl, content)
        return html[:package_match.start()] + section_start + new_content + section_end + html[package_match.end():]
    return html

def update_candidates_map_in_html(html):
    # Scale rent, premiumTargetPct, competitorCapacity in candidates array inside inline script
    cand_match = re.search(r'(const candidates = \[(.*?)\];)', html, re.DOTALL)
    if cand_match:
        array_declaration, array_content = cand_match.groups()
        
        # Scale rent
        def repl_rent(m):
            val = int(m.group(1))
            return f"rent: {round(val * 0.85)}"
        new_content = re.sub(r'rent:\s*(\d+)', repl_rent, array_content)
        
        # Scale premiumTargetPct
        def repl_target(m):
            val = float(m.group(1))
            return f"premiumTargetPct: {round(val * 1.20)}"
        new_content = re.sub(r'premiumTargetPct:\s*([\d.]+)', repl_target, new_content)
        
        # Scale competitorCapacity
        def repl_comp(m):
            val = int(m.group(1))
            return f"competitorCapacity: {round(val * 1.50)}"
        new_content = re.sub(r'competitorCapacity:\s*(\d+)', repl_comp, new_content)
        
        # Replace comment text in map markers
        new_content = new_content.replace("wash beds", "styling chairs")
        
        new_declaration = f"const candidates = [{new_content}];"
        html = html.replace(array_declaration, new_declaration)
        
    # Scale competitor prices in map marker popup
    # e.g. price: "US$100-190" -> "US$80-152"
    comp_match = re.search(r'(const competitors = \[(.*?)\];)', html, re.DOTALL)
    if comp_match:
        array_decl, array_content = comp_match.groups()
        def repl_comp_price(m):
            # Parse price range, e.g. "US$100-190" or "US$50 - 90" or "US$10-20"
            price_str = m.group(1)
            nums = re.findall(r'\d+', price_str)
            if len(nums) == 2:
                n1 = round(int(nums[0]) * 0.80)
                n2 = round(int(nums[1]) * 0.80)
                return f'price: "US${n1}-{n2}"'
            elif len(nums) == 1:
                n1 = round(int(nums[0]) * 0.80)
                return f'price: "US${n1}"'
            return m.group(0)
        new_content = re.sub(r'price:\s*"US\$([0-9\-\s\+]+)"', repl_comp_price, array_content)
        new_content = new_content.replace("VIP pods", "styling stations").replace("wash beds", "styling chairs")
        html = html.replace(array_decl, f"const competitors = [{new_content}];")
        
    return html

def main():
    print("=== STARTING OASIS SALON BATCH CONVERSION ===")
    
    # 1. Load baseline data from JSON
    if not os.path.exists(JSON_DB_PATH):
        print(f"Error: baseline parsed cities data not found at {JSON_DB_PATH}")
        return
        
    with open(JSON_DB_PATH, "r", encoding="utf-8") as f:
        cities = json.load(f)
        
    # 2. Scale metrics to Salon model
    scaled_cities, scaled_volumes = scale_cities_db(cities)
    print(f"Scaled parameters for {len(scaled_cities)} cities.")
    
    # 3. Update script.js
    update_script_js(scaled_cities, scaled_volumes)
    
    # 4. Update all HTML pages in workspace
    convert_html_pages(scaled_cities)
    
    print("\n=== CONVERSION COMPLETE ===")

if __name__ == "__main__":
    main()
