import os
import json
import re

# Directory Paths
WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
JSON_FILE = os.path.join(WORKDIR, "city_data.json")

# Load city_data.json to map HTML filenames to country codes
with open(JSON_FILE, "r", encoding="utf-8") as f:
    cities = json.load(f)

url_to_country = {}
for city in cities:
    url_to_country[city["url"]] = city["country"]

# Regulatory context updates map
reg_bullets = {
    'VN': """
                    <li><strong>Foreign Ownership & Corporate Structure:</strong> Direct 100% Foreign-Invested Enterprise (FIE) setup takes 3–6 months with high setup administrative barriers. Using a local Vietnamese nominee (title holder) to bypass capital limits and global income tax exposure creates a severe nominee dispute risk.</li>
                    <li><strong>Nominee Legality & Disputes:</strong> Nominee (trustee) agreements designed to circumvent foreign investment laws are legally unenforceable in Vietnamese courts. Disputes must rely on secondary collateral contracts (equity pledges, proxy voting mandates) rather than direct property rights, presenting a High strategic risk.</li>""",
    'TH': """
                    <li><strong>Foreign Shareholding Limits:</strong> Service salons are restricted to 49% foreign ownership under the Foreign Business Act. Setting up requires a Thai nominee partnership or applying for a highly restrictive Foreign Business License (FBL).</li>
                    <li><strong>Nominee Legality & Disputes:</strong> Nominee structures to evade the FBA are illegal and subject to criminal liability. Shareholder disputes in Thai courts are highly unfavorable to foreign investors. Control must be secured through preference shares (10:1 voting rights) and debt control.</li>""",
    'MY': """
                    <li><strong>WRT License & Capital Requirements:</strong> 100% foreign-owned retail and service salons require a WRT (Wholesale, Retail, Trade) license, mandating a minimum paid-up capital of RM 1 million (~USD 210,000).</li>
                    <li><strong>Legality & Dispute Resolution:</strong> WRT registration provides full corporate ownership protection and dispute enforceability under Malaysian common law, referable to the AIAC. Nominee setups to bypass the RM 1M capital are not recommended due to WRT compliance.</li>""",
    'SG': """
                    <li><strong>Foreign Corporate Structure:</strong> 100% direct foreign ownership is permitted with fast online setup. Singapore requires a local resident director (nominee director).</li>
                    <li><strong>Legality & Dispute Resolution:</strong> Excellent legal protection with highly enforceable commercial dispute resolution (SIAC in Singapore). Annual nominee resident agent services must be budgeted.</li>""",
    'HK': """
                    <li><strong>Foreign Corporate Structure:</strong> 100% direct foreign ownership is permitted with fast online setup. Hong Kong requires a local resident company secretary.</li>
                    <li><strong>Legality & Dispute Resolution:</strong> Excellent legal protection with highly enforceable commercial dispute resolution (HKIAC in Hong Kong). Annual nominee agent services must be budgeted.</li>""",
    'MC': """
                    <li><strong>Foreign Corporate Structure:</strong> 100% foreign ownership is permissible but requires local DSF registration and DSSOPT premises check. A local resident representative or attorney is required to handle administrative filings.</li>
                    <li><strong>Legality & Dispute Resolution:</strong> Full legal asset protection under Macau commercial codes. Disputes are subject to Macau civil courts, with filings requiring certified Portuguese translations.</li>""",
    'AE': """
                    <li><strong>Foreign Corporate Structure:</strong> Mainland Dubai professional services licensing permits 100% foreign ownership of salons but requires appointing a Local Service Agent (LSA). The LSA holds no equity but handles government relations for an annual retainer.</li>
                    <li><strong>Legality & Dispute Resolution:</strong> Mainland corporate contracts are subject to UAE civil courts. Commercial dispute filings require certified Arabic translations, making clear LSA contract terms essential.</li>""",
    'TW': """
                    <li><strong>Foreign Corporate Structure:</strong> 100% foreign ownership is permitted but requires pre-approval from the Investment Commission (MOEAIC) and capital verification.</li>
                    <li><strong>Legality & Dispute Resolution:</strong> Strong commercial asset protection. Profit remittance to non-resident shareholders is subject to a 21% dividend withholding tax (WHT) unless reduced under double taxation treaties.</li>""",
    'JP': """
                    <li><strong>Foreign Corporate Structure:</strong> 100% foreign ownership of a Kabushiki Kaisha (KK) is permitted, but requires a local bank account and at least one resident representative director in Japan to complete incorporation.</li>
                    <li><strong>Legality & Dispute Resolution:</strong> Complete asset protection under Japanese commercial code. Profit remittance is subject to a 20.42% dividend withholding tax (WHT), which can be reduced under tax treaties.</li>""",
    'KR': """
                    <li><strong>Foreign Corporate Structure:</strong> 100% foreign ownership is permitted under FIPA, but requires a minimum investment of KRW 100 million (~USD 75,000) per investor to qualify for foreign direct investment (FDI) visa status.</li>
                    <li><strong>Legality & Dispute Resolution:</strong> FDI status guarantees full asset protection and profit remittance. Dividend withholding tax is 20% (subject to treaty reductions). Disputes are handled in Korean courts or the KCAB.</li>""",
    'AU': """
                    <li><strong>Foreign Corporate Structure:</strong> 100% foreign ownership of Australian Pty Ltd companies is allowed, but at least one director must ordinarily reside in Australia.</li>
                    <li><strong>Legality & Dispute Resolution:</strong> High asset protection under ASIC. Unfranked dividend remittance is subject to a 30% withholding tax (WHT) unless reduced under tax treaties (typically to 15%).</li>"""
}

reg_risks = {
    'VN': """                            <tr>
                                <td>Nominee Dispute & Legal Recourse Risk</td>
                                <td><span class="badge high">High</span></td>
                                <td>Nominee trust agreements to bypass foreign restrictions are legally unenforceable in local courts. Mitigation: Execute robust loan agreements, equity pledges, and proxy mandates. Restrict bank access to foreign managers only.</td>
                            </tr>""",
    'TH': """                            <tr>
                                <td>Nominee Control & FBA Compliance Dispute</td>
                                <td><span class="badge high">High</span></td>
                                <td>Thai nominee shareholder structures to bypass the FBA are illegal and unenforceable in court. Mitigation: Structure the entity using preference shares giving 10:1 voting rights control and secure debt-to-equity collateral.</td>
                            </tr>""",
    'MY': """                            <tr>
                                <td>WRT Licensing & Capital Hurdles</td>
                                <td><span class="badge med">Medium</span></td>
                                <td>WRT license approval requires RM 1M paid-up capital. Mitigation: Inject capital from parent entity to ensure 100% legal ownership, avoiding risky nominee partnerships. Choose standard common-law arbitration.</td>
                            </tr>""",
    'SG': """                            <tr>
                                <td>Resident Nominee Agent Retainer Compliance</td>
                                <td><span class="badge low">Low</span></td>
                                <td>Failure to maintain local resident director agent compliance. Mitigation: Retain professional licensed corporate service firms and budget annual agent fees ($3,000–$5,000).</td>
                            </tr>""",
    'HK': """                            <tr>
                                <td>Resident Nominee Agent Retainer Compliance</td>
                                <td><span class="badge low">Low</span></td>
                                <td>Failure to maintain local resident company secretary agent compliance. Mitigation: Retain professional licensed corporate service firms and budget annual agent fees ($2,000–$4,000).</td>
                            </tr>""",
    'MC': """                            <tr>
                                <td>Local Representative & Language Compliance</td>
                                <td><span class="badge low">Low</span></td>
                                <td>Administrative delays due to bilingual (Chinese/Portuguese) legal filings. Mitigation: Appoint a local licensed lawyer/attorney to handle DSF/DSSOPT filings.</td>
                            </tr>""",
    'AE': """                            <tr>
                                <td>Local Service Agent Retainer & Civil Dispute</td>
                                <td><span class="badge med">Medium</span></td>
                                <td>LSA disputes can disrupt operations. Mitigation: Execute a clear, notarized LSA contract specifying a fixed annual retainer fee and excluding any profit/equity sharing. Use English-language DIFC arbitration where available.</td>
                            </tr>""",
    'TW': """                            <tr>
                                <td>MOEAIC Approval Delays & Dividend Withholding Tax</td>
                                <td><span class="badge med">Medium</span></td>
                                <td>Setup delays from Investment Commission approvals and 21% WHT on remitted profits. Mitigation: Appoint a local accountant to optimize corporate filings and WHT structures.</td>
                            </tr>""",
    'JP': """                            <tr>
                                <td>Representative Director & Banking Verification</td>
                                <td><span class="badge med">Medium</span></td>
                                <td>Difficulty opening local corporate bank accounts as a foreign entity. Mitigation: Retain a local judicial scrivener (Shiho-shoshi) and appoint a temporary resident co-representative director.</td>
                            </tr>""",
    'KR': """                            <tr>
                                <td>FDI Minimum Capital & D-9 Visa Compliance</td>
                                <td><span class="badge med">Medium</span></td>
                                <td>Failure to maintain the KRW 100M minimum capital can void the FDI visa status. Mitigation: Direct wire capital to an authorized local FDI bank account and register under FIPA.</td>
                            </tr>""",
    'AU': """                            <tr>
                                <td>Resident Director Retainer & Dividend Withholding Tax</td>
                                <td><span class="badge med">Medium</span></td>
                                <td>ASIC compliance requires an Australian resident nominee director, and unfranked dividends face 30% WHT. Mitigation: Appoint a nominee director via licensed firms and structure transfer pricing to minimize unfranked dividends.</td>
                            </tr>"""
}

# Iterate through HTML subpages and inject details
subpages = [f for f in os.listdir(WORKDIR) if f.endswith('.html') and f != 'index.html']

for html_file in subpages:
    country = url_to_country.get(html_file)
    if not country:
        print(f"⚠ Warning: No country mapped for {html_file}")
        continue
        
    path = os.path.join(WORKDIR, html_file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 1. Inject regulatory context bullets
    # Look for the <li> containing Regulatory Context or Licensing
    # We will append the foreign ownership bullet points right after it
    pattern_reg = r'(<li><strong>(?:Regulatory Context|Licensing):</strong>.*?</li>)'
    match = re.search(pattern_reg, content, re.DOTALL | re.IGNORECASE)
    if match:
        old_bullet = match.group(1)
        # Avoid duplicate injection
        if "Foreign Ownership" not in content and "WRT License" not in content and "Foreign Shareholding" not in content:
            new_bullets = old_bullet + reg_bullets[country]
            content = content.replace(old_bullet, new_bullets)
            modified = True
            print(f"[{html_file}] Injected regulatory bullet for country: {country}")
    else:
        print(f"⚠ Warning: Could not find Regulatory/Licensing bullet in {html_file}")

    # 2. Inject risks table row
    # Look for the risks table tbody block and append our custom row at the end
    # First, let's find the risks section
    risks_start = content.find('id="risks"')
    if risks_start != -1:
        tbody_start = content.find('<tbody>', risks_start)
        tbody_end = content.find('</tbody>', tbody_start)
        if tbody_start != -1 and tbody_end != -1:
            tbody_content = content[tbody_start:tbody_end]
            # Avoid duplicate injection
            if "Nominee Dispute" not in tbody_content and "WRT Licensing" not in tbody_content and "Resident Nominee Agent" not in tbody_content and "MOEAIC Approval" not in tbody_content:
                new_tbody = tbody_content + reg_risks[country] + "\n"
                content = content[:tbody_start] + new_tbody + content[tbody_end:]
                modified = True
                print(f"[{html_file}] Injected risk table row for country: {country}")
            else:
                pass
        else:
            print(f"⚠ Warning: Could not find tbody in risks section of {html_file}")
    else:
        print(f"⚠ Warning: Risks section NOT found in {html_file}")

    if modified:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

print("\nDone applying regulatory and risk updates to subpages.")
