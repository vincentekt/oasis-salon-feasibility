"""Fix kuala_lumpur.html using the KL data from batch 2."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

def replace_section(content, section_id, new_inner_html):
    pattern = rf'(<section id="{section_id}"[^>]*>)(.*?)(</section>)'
    replacement = r'\1' + new_inner_html + r'\3'
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count == 0:
        print(f"  WARNING: section #{section_id} not found!")
    return new_content

# Re-import the data from batch2 by running it and grabbing vars
import importlib.util, types
spec = importlib.util.spec_from_file_location("b2", os.path.join(WORKDIR, "substantive_update_batch2.py"))
# Just re-declare the KL vars inline
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
                                <td>KLCC/Ampang Hilir and "Embassy Row" (Ampang, Ukay Perdana) house KL's largest Western diplomatic and executive expat community. All quality salons require a 25–40 min drive to Bangsar — a genuine access gap for KL's most affluent expat zone</td>
                                <td>Ground-floor boutique in Jalan Ampang or Bukit Ceylon — serving KLCC tower executives and Embassy Row expat families within 5-min walk</td>
                            </tr>
                            <tr>
                                <td>Soft-water color protection in KL's hard, heavily chlorinated water</td>
                                <td>No KL premium salon deploys soft-water filtration — all use Syabas/PBA municipal water (TDS 150–300 ppm, high chlorine residual)</td>
                                <td>KL's municipal water has higher chlorine than Singapore or Taipei — color fade and hair porosity are documented expat complaints in KL beauty forums. No competitor has made this a service proposition</td>
                                <td>RO + activated carbon + ion-exchange filtration across all basins — "KL's first soft-water color salon"; color longevity guarantee vs. all Bangsar competitors</td>
                            </tr>
                            <tr>
                                <td>Premium Muslimah private suite in KLCC corridor</td>
                                <td>Bangsar salons have basic Muslimah screens; no KLCC/Ampang boutique offers it at all</td>
                                <td>KLCC area houses KL's Malaysian Muslim professional and HNWI community (PETRONAS, Maybank, GLiC executives). Premium Muslimah hair services at boutique quality are chronically undersupplied in this corridor</td>
                                <td>Enclosed luxury Muslimah private suite with separate entrance — serving Malaysia's most commercially powerful Muslim professional demographic in the correct geographic zone</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
"""

KL_MARKET = """
                <h2>3. Market Context</h2>
                <ul class="context-list">
                    <li><strong>Demographics:</strong> Kuala Lumpur has 250,000+ foreign nationals including 70,000+ Western expats (UK, US, Australia, France) in Bukit Ceylon, KLCC, Ampang Hilir, and Bangsar. Japanese community (~20,000) in Bangsar and Ampang. Korean community (~15,000) near KL Sentral. PETRONAS, Shell, Standard Chartered, and international law firm clusters dominate the KLCC corridor.</li>
                    <li><strong>Spending Power:</strong> KLCC corridor professionals earn $150,000–350,000+ USD equivalent packages. WTP: MYR 500–900 per color session. Bangsar HNWI household income averages MYR 30,000+/month. This is one of Southeast Asia's deepest premium beauty markets with proven spending precedent.</li>
                    <li><strong>Water Quality:</strong> Syabas/PBA KL municipal water has residual chlorine 0.3–0.6 mg/L and TDS 150–300 ppm — damaging for bleach-based balayage. Color fade and hair porosity are consistent expat complaints. Soft-water filtration is both technically warranted and commercially compelling in KL.</li>
                    <li><strong>Competitive Environment:</strong> Bangsar is over-concentrated (Number76, Bottega, Aube, Shawn Cutler) all competing for the same clientele. KLCC/Ampang corridor — with a larger expat population — has zero equivalent quality boutique. The Muslimah premium gap in the KLCC zone is entirely unaddressed.</li>
                    <li><strong>Regulatory Context:</strong> SSM business registration. Ministry of Health salon hygiene certification. EP (Employment Pass) for foreign stylists — apply minimum 3 months in advance. Muslimah private bay is best practice and commercially essential; design into floor plan from day one.</li>
                </ul>
"""

path = os.path.join(WORKDIR, "kuala_lumpur.html")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
content = replace_section(content, "competitors", KL_COMPETITORS)
content = replace_section(content, "unmet-needs", KL_UNMET)
content = replace_section(content, "market-context", KL_MARKET)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated: kuala_lumpur.html")
