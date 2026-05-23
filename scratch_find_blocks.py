import re

with open('hcmc.html', 'r', encoding='utf-8') as f:
    text = f.read()
    lines = text.splitlines()

def find_block(pattern, name):
    print(f"=== {name} ===")
    matches = [i for i, line in enumerate(lines) if pattern in line]
    for idx in matches:
        start = max(0, idx - 2)
        end = min(len(lines), idx + 8)
        print(f"Match at line {idx+1}:")
        for i in range(start, end):
            print(f"  {i+1}: {lines[i]}")
        print()

find_block("grid-stats", "Executive Summary Stats")
find_block("Positioned as:", "Section 2 Positioning")
find_block("Target Customer Segments", "Section 4 Table Start")
find_block("Vo Thi Sau / Turtle Lake", "Section 5 Table")
find_block("rent target", "Section 5 Conclusion")
find_block("J-First Tokyo", "Section 6 Competitors Table")
find_block("Express Cut & Blowout", "Section 8 Menu Table")
find_block("Precision Cut & Style Pack", "Section 9 Packages")
find_block("Utility & Staff Room", "Section 11 Layout Table")
find_block("Salon Director / Master Stylist", "Section 12 Staffing Table")
find_block("Rent", "Section 13 OPEX")
find_block("Boutique Renovation & Fitout", "Section 14 CAPEX")
find_block("Average Ticket", "Section 15 Economics")
find_block("Breakeven", "Section 15 Table")
find_block("Timeline (12 Weeks)", "Section 16 Timeline Header")
find_block("Decision: GO", "Section 19 Recommendation")
find_block("Candidate A", "Script Candidates")
find_block("J-First Tokyo", "Script Competitors")
