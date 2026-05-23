"""
create_salon_excel.py
=====================
Creates salon_data.xlsx — the single source of truth for all 27 city financials.

Architecture:
  - "Country" sheet:   Tax rates + salary data per country (editable)
  - "Cities" sheet:    All raw inputs per city (editable, yellow cells)
  - "Model" sheet:     Calculated metrics using Excel formulas (blue, read-only)
  - "Instructions" sheet: How to use + update workflow

After editing the Excel:
  Run: python excel_to_json.py
  This regenerates city_data.json AND updates the citiesDb in script.js.
  Then: git add -A && git commit && git push
"""

import openpyxl
from openpyxl.styles import (PatternFill, Font, Alignment, Border, Side,
                              GradientFill)
from openpyxl.utils import get_column_letter
from openpyxl.styles.numbers import FORMAT_PERCENTAGE_00
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import ColorScaleRule
import os

WORKDIR = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
OUT_FILE = os.path.join(WORKDIR, "salon_data.xlsx")

wb = openpyxl.Workbook()

# ── STYLES ────────────────────────────────────────────────────────────────────
INPUT_FILL    = PatternFill("solid", fgColor="FFF9C4")  # yellow
CALC_FILL     = PatternFill("solid", fgColor="DDEEFF")  # light blue
HEADER_FILL   = PatternFill("solid", fgColor="1E3A5F")  # dark navy
SUBHDR_FILL   = PatternFill("solid", fgColor="2E6DA4")  # medium blue
COUNTRY_FILL  = PatternFill("solid", fgColor="E8F5E9")  # light green
WARN_FILL     = PatternFill("solid", fgColor="FFCCCC")  # light red
OK_FILL       = PatternFill("solid", fgColor="CCFFCC")  # light green

HDR_FONT  = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
BODY_FONT = Font(name="Calibri", size=10)
TITLE_FONT= Font(name="Calibri", bold=True, size=14, color="1E3A5F")
BOLD_FONT = Font(name="Calibri", bold=True, size=10)

thin = Side(style="thin", color="BBBBBB")
thick= Side(style="medium", color="2E6DA4")
BORDER_THIN = Border(left=thin, right=thin, top=thin, bottom=thin)

CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT   = Alignment(horizontal="left",   vertical="center")
RIGHT  = Alignment(horizontal="right",  vertical="center")

def apply_header(cell, text, fill=None):
    cell.value = text
    cell.fill  = fill or HEADER_FILL
    cell.font  = HDR_FONT
    cell.alignment = CENTER
    cell.border = BORDER_THIN

def apply_input(cell, value=None, number_format=None):
    if value is not None:
        cell.value = value
    cell.fill = INPUT_FILL
    cell.font = BODY_FONT
    cell.alignment = RIGHT
    cell.border = BORDER_THIN
    if number_format:
        cell.number_format = number_format

def apply_calc(cell, formula=None, number_format=None):
    if formula is not None:
        cell.value = formula
    cell.fill = CALC_FILL
    cell.font = BODY_FONT
    cell.alignment = RIGHT
    cell.border = BORDER_THIN
    if number_format:
        cell.number_format = number_format

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 1: Country Parameters
# ══════════════════════════════════════════════════════════════════════════════
ws_c = wb.active
ws_c.title = "Country"
ws_c.sheet_view.showGridLines = True
ws_c.column_dimensions["A"].width = 14
ws_c.column_dimensions["B"].width = 22
ws_c.column_dimensions["C"].width = 12
ws_c.column_dimensions["D"].width = 14
ws_c.column_dimensions["E"].width = 20
ws_c.column_dimensions["F"].width = 20
ws_c.column_dimensions["G"].width = 20
ws_c.column_dimensions["H"].width = 20

# Title
ws_c.merge_cells("A1:H1")
ws_c["A1"].value = "Country Parameters — Salon Financial Model"
ws_c["A1"].font  = TITLE_FONT
ws_c["A1"].alignment = CENTER
ws_c.row_dimensions[1].height = 32

# Subtitle
ws_c.merge_cells("A2:H2")
ws_c["A2"].value = "✏ Edit these cells to update assumptions. Run excel_to_json.py after any change."
ws_c["A2"].font  = Font(name="Calibri", italic=True, size=10, color="555555")
ws_c["A2"].alignment = CENTER

# Headers
headers = ["Country Code", "Country Name", "Corp. Tax Rate",
           "Currency", "Senior Stylist\n(USD/mo)",
           "Junior Stylist\n(USD/mo)", "Assistant\n(USD/mo)", "Manager\n(USD/mo)"]
for c, h in enumerate(headers, 1):
    apply_header(ws_c.cell(3, c), h)
ws_c.row_dimensions[3].height = 36

# Country data (research-backed rates in USD/month)
countries = [
    # code, name, tax, currency, senior, junior, asst, manager
    ("AU",  "Australia",   0.30, "AUD", 4225, 2800, 2470, 4550),
    ("JP",  "Japan",       0.30, "JPY", 2345, 1474, 1474, 3015),
    ("KR",  "South Korea", 0.20, "KRW", 2044, 1314, 1314, 2555),
    ("SG",  "Singapore",   0.17, "SGD", 3330, 2480, 1850, 4440),
    ("HK",  "Hong Kong",   0.165,"HKD", 2432, 1792, 1664, 3072),
    ("MC",  "Macau",       0.12, "HKD", 2304, 1536, 1536, 2816),
    ("TW",  "Taiwan",      0.20, "NTD", 1705,  992,  992, 2170),
    ("MY",  "Malaysia",    0.24, "MYR",  990,  660,  484, 1320),
    ("VN",  "Vietnam",     0.20, "VND",  800,  500,  420, 1100),
    ("TH",  "Thailand",    0.20, "THB", 1305,  870,  638, 1740),
    ("AE",  "UAE / Dubai", 0.09, "AED", 2720, 1904, 1632, 3808),
]

for r, row in enumerate(countries, 4):
    ws_c.cell(r, 1).value = row[0]; ws_c.cell(r, 1).fill = PatternFill("solid", fgColor="E3F2FD"); ws_c.cell(r, 1).font = BOLD_FONT; ws_c.cell(r, 1).alignment = CENTER; ws_c.cell(r, 1).border = BORDER_THIN
    ws_c.cell(r, 2).value = row[1]; apply_input(ws_c.cell(r, 2), row[1])
    ws_c.cell(r, 3).value = row[2]; apply_input(ws_c.cell(r, 3), row[2], "0.0%")
    ws_c.cell(r, 4).value = row[3]; apply_input(ws_c.cell(r, 4), row[3])
    for c, v in enumerate(row[4:], 5):
        apply_input(ws_c.cell(r, c), v, '"USD "[$-en-US]#,##0')

# Named range helper note
ws_c.merge_cells("A16:H16")
ws_c["A16"].value = ("💡 Country lookup: These rows are referenced by VLOOKUP in the Cities sheet. "
                      "Do not change the Country Code column (column A). Add new countries at the bottom.")
ws_c["A16"].font = Font(name="Calibri", italic=True, size=9, color="777777")

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 2: Cities (Raw Inputs)
# ══════════════════════════════════════════════════════════════════════════════
ws_i = wb.create_sheet("Cities")
ws_i.sheet_view.showGridLines = True
ws_i.freeze_panes = "C4"

# Column widths
col_widths = {
    "A": 22, "B": 14, "C": 12, "D": 12,  # identity
    "E": 10, "F": 12, "G": 12,            # space/session
    "H": 10, "I": 9,                       # ticket/cogs
    "J": 12, "K": 14, "L": 14, "M": 14, "N": 11, # rent/capex inputs
    "O": 9,  "P": 9,                       # utilisation
}
for col, width in col_widths.items():
    ws_i.column_dimensions[col].width = width

# Title
ws_i.merge_cells("A1:P1")
ws_i["A1"].value = "Oasis Salon — City Input Parameters"
ws_i["A1"].font  = TITLE_FONT
ws_i["A1"].alignment = CENTER
ws_i.row_dimensions[1].height = 32

ws_i.merge_cells("A2:P2")
ws_i["A2"].value = "✏ YELLOW = editable inputs. BLUE (Model sheet) = auto-calculated. After editing, run: python excel_to_json.py"
ws_i["A2"].font  = Font(name="Calibri", italic=True, size=10, color="555555")
ws_i["A2"].alignment = CENTER
ws_i.row_dimensions[2].height = 20

# Section headers (row 3)
sections = [
    (1, 4, "IDENTITY"),
    (5, 7, "SPACE & TIME"),
    (8, 9, "PRICING"),
    (10, 14, "COSTS & CAPEX"),
    (15, 16, "UTILISATION"),
]
for start, end, label in sections:
    ws_i.merge_cells(f"{get_column_letter(start)}3:{get_column_letter(end)}3")
    apply_header(ws_i.cell(3, start), label, SUBHDR_FILL)
ws_i.row_dimensions[3].height = 24

# Column headers (row 4)
col_headers = [
    "City Name", "URL", "Region", "Country\nCode",
    "Space\n(sq ft)", "Sessions/\nStation/Day", "Working\nDays/Month",
    "Ticket\n(USD)", "COGS %",
    "Rent\n(USD/mo)", "Fitout\n(USD)", "Equipment\n(USD)", "Other\nCAPEX (USD)", "Deposit\nMonths",
    "Util Y1\n(%)", "Util Y2\n(%)",
]
for c, h in enumerate(col_headers, 1):
    apply_header(ws_i.cell(4, c), h)
ws_i.row_dimensions[4].height = 42

# City input data
city_inputs = [
    # name, url, region, country, sqft, sess, wd, ticket, cogs, rent, fitout, equip, other, dep_mo, u1, u2
    ("Ho Chi Minh",       "hcmc.html",          "Vietnam",    "VN",  800, 3, 26,  95, 0.10, 3000, 20000, 20000, 9000,  3, 0.65, 0.75),
    ("Hanoi",             "hanoi.html",          "Vietnam",    "VN",  800, 3, 26,  95, 0.10, 2200, 18000, 18000, 7600,  3, 0.65, 0.75),
    ("Da Nang",           "danang.html",         "Vietnam",    "VN",  800, 4, 26,  55, 0.10,  800, 12000, 16000, 4600,  3, 0.65, 0.75),
    ("Hai Phong",         "haiphong.html",       "Vietnam",    "VN",  800, 4, 26,  45, 0.10,  650, 10000, 15000, 3300,  3, 0.65, 0.75),
    ("Binh Duong",        "binhduong.html",      "Vietnam",    "VN",  800, 4, 26,  45, 0.10,  600, 10000, 14000, 3200,  3, 0.65, 0.75),
    ("Dong Nai",          "dongnai.html",        "Vietnam",    "VN",  800, 4, 26,  55, 0.10,  550,  9000, 13000, 3100,  3, 0.65, 0.75),
    ("Kuala Lumpur",      "kuala_lumpur.html",   "Malaysia",   "MY",  800, 3, 26,  90, 0.10, 2000, 33000, 20000, 6000,  3, 0.65, 0.75),
    ("Johor Bahru (RTS)", "johor.html",          "Malaysia",   "MY", 1000, 4, 26,  65, 0.10, 1700, 28600, 18000, 5400,  3, 0.65, 0.75),
    ("Penang",            "penang.html",         "Malaysia",   "MY",  800, 4, 26,  55, 0.10,  800, 22000, 15000, 4800,  3, 0.65, 0.75),
    ("Sabah",             "sabah.html",          "Malaysia",   "MY",  800, 4, 26,  45, 0.10,  900, 19800, 14500, 4500,  3, 0.65, 0.75),
    ("Sarawak",           "sarawak.html",        "Malaysia",   "MY",  800, 4, 26,  46, 0.10,  700, 18700, 14000, 4200,  3, 0.65, 0.75),
    ("Singapore",         "singapore.html",      "Other APAC", "SG",  750, 3, 26, 180, 0.10, 5500, 66600, 22000,16500,  3, 0.65, 0.75),
    ("Hong Kong",         "hongkong.html",       "Other APAC", "HK",  750, 3, 26, 200, 0.10, 8500, 76800, 22000,25500,  3, 0.65, 0.75),
    ("Bangkok",           "bangkok.html",        "Other APAC", "TH",  800, 3, 26, 160, 0.10, 5000, 43500, 20000,15000,  3, 0.65, 0.75),
    ("Macau",             "macau.html",          "Other APAC", "MC",  750, 3, 26, 130, 0.10, 1800, 44800, 18000, 5400,  3, 0.65, 0.75),
    ("Dubai",             "dubai.html",          "Middle East", "AE", 800, 3, 26, 160, 0.10, 3500, 54400, 22000,42000, 12, 0.65, 0.75),
    ("Taipei",            "taipei.html",         "Taiwan",     "TW",  850, 3, 26, 104, 0.10, 2200, 55800, 20000, 6600,  3, 0.65, 0.75),
    ("Taichung",          "taichung.html",       "Taiwan",     "TW",  800, 3, 26, 110, 0.10, 1800, 46500, 18000, 5400,  3, 0.65, 0.75),
    ("Kaohsiung",         "kaohsiung.html",      "Taiwan",     "TW",  800, 3, 26, 120, 0.10, 1200, 37200, 17000, 3600,  3, 0.65, 0.75),
    ("Tainan",            "tainan.html",         "Taiwan",     "TW",  750, 3, 26, 100, 0.10,  900, 34100, 16000, 2700,  3, 0.65, 0.75),
    ("Fukuoka",           "fukuoka.html",        "Japan",      "JP",  800, 3, 22, 130, 0.10, 1600,100500, 20000, 4800,  3, 0.65, 0.75),
    ("Okinawa",           "okinawa.html",        "Japan",      "JP",  800, 3, 26, 120, 0.10, 1100, 80400, 18000, 3300,  3, 0.65, 0.75),
    ("Busan",             "busan.html",          "South Korea","KR",  800, 3, 26, 100, 0.10, 2200, 58400, 18000, 6600,  3, 0.65, 0.75),
    ("Sydney",            "sydney.html",         "Australia",  "AU",  800, 3, 26, 250, 0.10, 3200, 91000, 22000, 9600,  3, 0.65, 0.75),
    ("Melbourne",         "melbourne.html",      "Australia",  "AU",  800, 3, 26, 220, 0.10, 3500, 87750, 22000,10500,  3, 0.65, 0.75),
    ("Brisbane",          "brisbane.html",       "Australia",  "AU",  800, 3, 26, 240, 0.10, 2800, 78000, 20000, 8400,  3, 0.65, 0.75),
    ("Perth",             "perth.html",          "Australia",  "AU",  800, 3, 26, 200, 0.10, 2000, 74750, 19000, 6000,  3, 0.65, 0.75),
]

for r_idx, row in enumerate(city_inputs, 5):
    (name, url, region, country, sqft, sess, wd, ticket, cogs,
     rent, fitout, equip, other, dep_mo, u1, u2) = row
    ws_i.cell(r_idx, 1).value = name;    ws_i.cell(r_idx, 1).fill = PatternFill("solid", fgColor="E3F2FD"); ws_i.cell(r_idx, 1).font = BOLD_FONT; ws_i.cell(r_idx, 1).alignment = LEFT;  ws_i.cell(r_idx, 1).border = BORDER_THIN
    ws_i.cell(r_idx, 2).value = url;     apply_input(ws_i.cell(r_idx, 2), url); ws_i.cell(r_idx, 2).alignment = LEFT
    ws_i.cell(r_idx, 3).value = region;  apply_input(ws_i.cell(r_idx, 3), region); ws_i.cell(r_idx, 3).alignment = LEFT
    ws_i.cell(r_idx, 4).value = country; apply_input(ws_i.cell(r_idx, 4), country); ws_i.cell(r_idx, 4).alignment = CENTER
    apply_input(ws_i.cell(r_idx,  5), sqft,   "#,##0")
    apply_input(ws_i.cell(r_idx,  6), sess,   "0")
    apply_input(ws_i.cell(r_idx,  7), wd,     "0")
    apply_input(ws_i.cell(r_idx,  8), ticket, '"$"#,##0')
    apply_input(ws_i.cell(r_idx,  9), cogs,   "0.0%")
    apply_input(ws_i.cell(r_idx, 10), rent,   '"$"#,##0')
    apply_input(ws_i.cell(r_idx, 11), fitout, '"$"#,##0')
    apply_input(ws_i.cell(r_idx, 12), equip,  '"$"#,##0')
    apply_input(ws_i.cell(r_idx, 13), other,  '"$"#,##0')
    apply_input(ws_i.cell(r_idx, 14), dep_mo, "0")
    apply_input(ws_i.cell(r_idx, 15), u1,     "0%")
    apply_input(ws_i.cell(r_idx, 16), u2,     "0%")

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 3: Model (All calculations)
# ══════════════════════════════════════════════════════════════════════════════
ws_m = wb.create_sheet("Model")
ws_m.sheet_view.showGridLines = True
ws_m.freeze_panes = "C4"

# Column widths
model_widths = {
    "A": 22,  # City name (linked)
    "B": 12,  # Country
    # Space → Staff
    "C": 8,   "D": 9,   "E": 8,   "F": 8,   "G": 8,   "H": 10,  # stations calc
    # Country lookups
    "I": 9,   "J": 14,  "K": 14,  "L": 14,  "M": 14,
    # Staff cost breakdown
    "N": 14,
    # OPEX
    "O": 12,  "P": 12,  "Q": 12,  "R": 14,
    # Capacity
    "S": 11,  "T": 11,  "U": 11,
    # Economics
    "V": 13,  "W": 13,  "X": 13,  "Y": 14,
    # CAPEX & Payback
    "Z": 12,  "AA": 12, "AB": 12, "AC": 12, "AD": 13,
    # Viability
    "AE": 12,
}
for col, width in model_widths.items():
    ws_m.column_dimensions[col].width = width

# Title
ws_m.merge_cells("A1:AE1")
ws_m["A1"].value = "Oasis Salon — Calculated Financial Model (Auto-Generated from Cities Sheet)"
ws_m["A1"].font  = TITLE_FONT
ws_m["A1"].alignment = CENTER
ws_m.row_dimensions[1].height = 32

ws_m.merge_cells("A2:AE2")
ws_m["A2"].value = "🔒 Do not edit this sheet directly — change inputs in Cities sheet. BLUE = formula cells."
ws_m["A2"].font  = Font(name="Calibri", italic=True, size=10, color="CC0000")
ws_m["A2"].alignment = CENTER

# Section headers (row 3)
model_sections = [
    (1, 2, "IDENTITY"),
    (3, 8, "SPACE → STAFF"),
    (9, 13, "COUNTRY RATES"),
    (14, 14, "STAFF COST"),
    (15, 18, "MONTHLY OPEX"),
    (19, 21, "CAPACITY"),
    (22, 25, "UNIT ECONOMICS"),
    (26, 30, "CAPEX & PAYBACK"),
    (31, 31, "VIABLE?"),
]
for start, end, label in model_sections:
    ws_m.merge_cells(f"{get_column_letter(start)}3:{get_column_letter(end)}3")
    apply_header(ws_m.cell(3, start), label, SUBHDR_FILL)
ws_m.row_dimensions[3].height = 24

# Column headers (row 4)
model_headers = [
    "City Name", "Country",
    "Stations", "Wash\nBasins", "Seniors", "Juniors", "Assistants", "Total\nStaff",
    "Tax Rate", "Senior\n(USD/mo)", "Junior\n(USD/mo)", "Assistant\n(USD/mo)", "Manager\n(USD/mo)",
    "Total Staff\nCost (USD/mo)",
    "Rent\n(USD/mo)", "Utilities\n(USD/mo)", "Mktg+Misc\n(USD/mo)", "Total OPEX\n(USD/mo)",
    "Max\nCapacity", "Y1 Clients\n(65%)", "Y2 Clients\n(75%)",
    "Breakeven\n(clients/mo)", "COGS/session", "GM/session\n(90%)", "Y2 Monthly\nPAT (USD)",
    "CAPEX Low", "CAPEX High", "CAPEX Mid", "Payback\n(months)", "PAT/OPEX\n(%)",
    "VIABLE?\n(BE < 80%cap)",
]
for c, h in enumerate(model_headers, 1):
    apply_header(ws_m.cell(4, c), h)
ws_m.row_dimensions[4].height = 48

# Formula rows (rows 5–31 = 27 cities)
# Cities!A5 = Ho Chi Minh, Cities!A6 = Hanoi, etc.
# Country!A4:H14 has country data (11 countries, rows 4-14)

for r_idx in range(5, 32):   # rows 5-31 (27 cities)
    ci = r_idx  # cities row index (same row number as model)
    cr = r_idx  # model row
    
    # Helper: reference to Cities sheet column
    def c_col(col_letter):
        return f"Cities!{col_letter}{ci}"
    # Helper: VLOOKUP country code in Country sheet (A4:H14)
    def vlookup(col_num):
        return f"VLOOKUP({c_col('D')},Country!$A$4:$H$14,{col_num},FALSE)"
    
    # A: City Name (linked from Cities)
    ws_m.cell(cr, 1).value  = f"=Cities!A{ci}"
    ws_m.cell(cr, 1).fill   = PatternFill("solid", fgColor="E3F2FD")
    ws_m.cell(cr, 1).font   = BOLD_FONT
    ws_m.cell(cr, 1).alignment = LEFT
    ws_m.cell(cr, 1).border = BORDER_THIN
    
    # B: Country Code
    ws_m.cell(cr, 2).value = f"={c_col('D')}"
    ws_m.cell(cr, 2).fill  = PatternFill("solid", fgColor="E3F2FD")
    ws_m.cell(cr, 2).font  = BOLD_FONT
    ws_m.cell(cr, 2).alignment = CENTER
    ws_m.cell(cr, 2).border = BORDER_THIN
    
    # C: Stations = IF(sqft<=750,3, IF(sqft<=850,4, 5))
    apply_calc(ws_m.cell(cr, 3),
        f"=IF({c_col('E')}<=750,3,IF({c_col('E')}<=850,4,5))", "0")
    
    # D: Wash Basins = IF(stations<=4, 2, 3)
    apply_calc(ws_m.cell(cr, 4),
        f"=IF(C{cr}<=4,2,3)", "0")
    
    # E: Seniors = IF(stations<=4, 2, 3)
    apply_calc(ws_m.cell(cr, 5),
        f"=IF(C{cr}<=4,2,3)", "0")
    
    # F: Juniors = Stations - Seniors
    apply_calc(ws_m.cell(cr, 6),
        f"=C{cr}-E{cr}", "0")
    
    # G: Assistants = CEILING(stations/2, 1)
    apply_calc(ws_m.cell(cr, 7),
        f"=CEILING(C{cr}/2,1)", "0")
    
    # H: Total Staff = Seniors + Juniors + Assistants + 1 (manager)
    apply_calc(ws_m.cell(cr, 8),
        f"=E{cr}+F{cr}+G{cr}+1", "0")
    
    # I: Tax Rate (VLOOKUP col 3)
    apply_calc(ws_m.cell(cr, 9),
        f"={vlookup(3)}", "0.0%")
    
    # J: Senior rate (col 5)
    apply_calc(ws_m.cell(cr, 10),
        f"={vlookup(5)}", '"$"#,##0')
    
    # K: Junior rate (col 6)
    apply_calc(ws_m.cell(cr, 11),
        f"={vlookup(6)}", '"$"#,##0')
    
    # L: Assistant rate (col 7)
    apply_calc(ws_m.cell(cr, 12),
        f"={vlookup(7)}", '"$"#,##0')
    
    # M: Manager rate (col 8)
    apply_calc(ws_m.cell(cr, 13),
        f"={vlookup(8)}", '"$"#,##0')
    
    # N: Total Staff Cost = seniors×J + juniors×K + assistants×L + 1×M
    apply_calc(ws_m.cell(cr, 14),
        f"=E{cr}*J{cr}+F{cr}*K{cr}+G{cr}*L{cr}+M{cr}", '"$"#,##0')
    
    # O: Rent
    apply_calc(ws_m.cell(cr, 15),
        f"={c_col('J')}", '"$"#,##0')
    
    # P: Utilities = 200 + stations*80
    apply_calc(ws_m.cell(cr, 16),
        f"=200+C{cr}*80", '"$"#,##0')
    
    # Q: Marketing + Misc = 350+stations*50 + 300+stations*30
    apply_calc(ws_m.cell(cr, 17),
        f"=350+C{cr}*50+300+C{cr}*30", '"$"#,##0')
    
    # R: Total OPEX = Rent + StaffCost + Utilities + Mktg+Misc
    apply_calc(ws_m.cell(cr, 18),
        f"=O{cr}+N{cr}+P{cr}+Q{cr}", '"$"#,##0')
    
    # S: Max Capacity = stations × sessions × working_days
    apply_calc(ws_m.cell(cr, 19),
        f"=C{cr}*{c_col('F')}*{c_col('G')}", "0")
    
    # T: Y1 Clients = INT(max_cap * util_y1)
    apply_calc(ws_m.cell(cr, 20),
        f"=INT(S{cr}*{c_col('O')})", "0")
    
    # U: Y2 Clients = INT(max_cap * util_y2)
    apply_calc(ws_m.cell(cr, 21),
        f"=INT(S{cr}*{c_col('P')})", "0")
    
    # V: Breakeven = CEILING(OPEX / (ticket * (1-cogs%)), 1)
    apply_calc(ws_m.cell(cr, 22),
        f"=CEILING(R{cr}/({c_col('H')}*(1-{c_col('I')})),1)", "0")
    
    # W: COGS per session
    apply_calc(ws_m.cell(cr, 23),
        f"={c_col('H')}*{c_col('I')}", '"$"#,##0.00')
    
    # X: Gross Margin per session = ticket - cogs
    apply_calc(ws_m.cell(cr, 24),
        f"={c_col('H')}-W{cr}", '"$"#,##0.00')
    
    # Y: Y2 Monthly PAT = (Y2_clients × ticket × (1-cogs%) - OPEX) × (1-tax)
    apply_calc(ws_m.cell(cr, 25),
        f"=(U{cr}*{c_col('H')}*(1-{c_col('I')})-R{cr})*(1-I{cr})", '"$"#,##0')
    
    # Z: CAPEX Low = (fitout+equipment+other+rent*deposit) × 0.92, rounded to 5k
    apply_calc(ws_m.cell(cr, 26),
        f"=FLOOR(({c_col('K')}+{c_col('L')}+{c_col('M')}+{c_col('J')}*{c_col('N')})*0.92,5000)",
        '"$"#,##0')
    
    # AA: CAPEX High
    apply_calc(ws_m.cell(cr, 27),
        f"=CEILING(({c_col('K')}+{c_col('L')}+{c_col('M')}+{c_col('J')}*{c_col('N')})*1.08,5000)",
        '"$"#,##0')
    
    # AB: CAPEX Mid
    apply_calc(ws_m.cell(cr, 28),
        f"=(Z{cr}+AA{cr})/2", '"$"#,##0')
    
    # AC: Payback months = CEILING(CAPEX_mid / Y2_PAT, 1)   [handle div/0]
    apply_calc(ws_m.cell(cr, 29),
        f"=IF(Y{cr}>0,CEILING(AB{cr}/Y{cr},1),999)", "0")
    
    # AD: PAT/OPEX ratio
    apply_calc(ws_m.cell(cr, 30),
        f"=IF(R{cr}>0,Y{cr}/R{cr},0)", "0%")
    
    # AE: Viable? = breakeven < 80% of max capacity
    cell_ae = ws_m.cell(cr, 31)
    cell_ae.value = f"=IF(V{cr}<S{cr}*0.8,\"✓ YES\",\"⚠ TIGHT\")"
    cell_ae.fill  = CALC_FILL
    cell_ae.font  = BOLD_FONT
    cell_ae.alignment = CENTER
    cell_ae.border = BORDER_THIN

# Conditional formatting for Viable column
from openpyxl.formatting.rule import CellIsRule
ws_m.conditional_formatting.add(
    f"AE5:AE31",
    CellIsRule(operator="containsText", formula=['"✓"'], fill=OK_FILL, font=Font(color="006100", bold=True))
)

# ══════════════════════════════════════════════════════════════════════════════
# SHEET 4: Instructions
# ══════════════════════════════════════════════════════════════════════════════
ws_inst = wb.create_sheet("Instructions")
ws_inst.column_dimensions["A"].width = 100

instructions = [
    ("Oasis Salon Feasibility — Excel Workbook Guide", "title"),
    ("", ""),
    ("📋 HOW THIS WORKBOOK IS STRUCTURED", "section"),
    ("", ""),
    ("• Country sheet:    Edit tax rates and monthly staff salaries (in USD) per country.", "body"),
    ("• Cities sheet:     Edit all raw inputs per city (yellow cells only):", "body"),
    ("   - Space (sq ft), sessions/day, working days, ticket price, COGS %", "sub"),
    ("   - Rent, fitout cost, equipment cost, other CAPEX, deposit months", "sub"),
    ("   - Year 1 and Year 2 utilisation targets", "sub"),
    ("• Model sheet:      All formulas. Do NOT edit directly. Reads from Cities + Country.", "body"),
    ("", ""),
    ("⚙️ KEY FORMULAS", "section"),
    ("", ""),
    ("  Stations         = IF(sqft ≤ 750 → 3, sqft ≤ 850 → 4, else 5)", "body"),
    ("  Max Capacity     = stations × sessions/day × working_days/month", "body"),
    ("  Y2 Clients       = INT(max_capacity × util_Y2)", "body"),
    ("  Staff Cost       = seniors×senior_rate + juniors×junior_rate + assistants×asst_rate + manager_rate", "body"),
    ("  Total OPEX       = Rent + Staff_Cost + Utilities(200+stations×80) + Mktg+Misc(650+stations×80)", "body"),
    ("  Breakeven        = CEILING(OPEX / (ticket × (1 − COGS%)), 1)", "body"),
    ("  CAPEX Low        = FLOOR((fitout+equip+other+rent×dep_months) × 0.92, $5,000)", "body"),
    ("  CAPEX High       = CEILING((fitout+equip+other+rent×dep_months) × 1.08, $5,000)", "body"),
    ("  Y2 Monthly PAT   = (Y2_clients × ticket × (1−COGS%) − OPEX) × (1 − tax_rate)", "body"),
    ("  Payback          = CEILING(CAPEX_mid / Y2_PAT, 1 month)", "body"),
    ("  PAT/OPEX         = Y2_PAT / OPEX", "body"),
    ("  Viable?          = YES if Breakeven < 80% of Max Capacity", "body"),
    ("", ""),
    ("🔄 UPDATE WORKFLOW", "section"),
    ("", ""),
    ("  1. Edit values in Country or Cities sheet (yellow cells).", "body"),
    ("  2. Review the Model sheet to check that all formulas recalculate correctly.", "body"),
    ("  3. Save the Excel file.", "body"),
    ("  4. Open a terminal and run:", "body"),
    ("       cd c:\\Users\\vince\\Projects\\HairSpa\\Oasis_Salon_Web", "code"),
    ("       python excel_to_json.py", "code"),
    ("  5. This regenerates city_data.json AND updates the citiesDb in script.js.", "body"),
    ("  6. Commit and push:", "body"),
    ("       git add -A && git commit -m \"Update financials\" && git push", "code"),
    ("", ""),
    ("📌 NOTES", "section"),
    ("", ""),
    ("  • Taipei vs Taichung CAPEX: Taipei (USD 75-95k) > Taichung (USD 65-80k) because", "body"),
    ("    Taipei has: higher rent ($2,200 vs $1,800) + higher Da'an district fitout (NTD 1.8M vs 1.5M) + 850 sqft vs 800 sqft.", "sub"),
    ("  • Fukuoka uses 22 working days/month (Japanese boutique: closed Mon + limited Sun).", "body"),
    ("  • Dubai uses 12 deposit months (UAE annual lease pre-payment norm).", "body"),
    ("  • All staff rates are in USD/month at mid-2025 exchange rates.", "body"),
    ("  • COGS (10%) covers professional colour products (Schwarzkopf/Milbon/Redken).", "body"),
    ("  • Utilisation: 65% Year 1 (ramp-up), 75% Year 2 (steady state).", "body"),
    ("  • Payback period is calculated at Year 2 (75%) utilisation.", "body"),
]

style_map = {
    "title":   (TITLE_FONT, 20),
    "section": (Font(name="Calibri", bold=True, size=12, color="1E3A5F"), 18),
    "body":    (Font(name="Calibri", size=10), 15),
    "sub":     (Font(name="Calibri", size=10, color="555555"), 14),
    "code":    (Font(name="Courier New", size=10, color="006400"), 14),
    "":        (Font(name="Calibri", size=10), 8),
}

for r_idx, (text, style) in enumerate(instructions, 1):
    cell = ws_inst.cell(r_idx, 1)
    cell.value = text
    font, height = style_map.get(style, (BODY_FONT, 14))
    cell.font = font
    cell.alignment = Alignment(horizontal="left", vertical="center")
    ws_inst.row_dimensions[r_idx].height = height

# ── ORDER SHEETS ──────────────────────────────────────────────────────────────
wb.move_sheet("Instructions", offset=-10)  # Move to front

# ── SAVE ──────────────────────────────────────────────────────────────────────
wb.save(OUT_FILE)
print(f"✅ Created: {OUT_FILE}")
print(f"   Sheets: {[ws.title for ws in wb.worksheets]}")
print(f"   Cities: {len(city_inputs)} rows")
print(f"   Countries: {len(countries)} rows")
print(f"\nNext step: python excel_to_json.py")
