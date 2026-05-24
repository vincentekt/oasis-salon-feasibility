import openpyxl

xlsx_path = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web\salon_data.xlsx"
wb = openpyxl.load_workbook(xlsx_path)
ws = wb["Cities"]

# We already found that cell S17 corresponds to Hong Kong's Underserved Gap %
cell = ws["S17"]
print("Current value of S17:", cell.value)
cell.value = 16
print("New value of S17:", cell.value)

wb.save(xlsx_path)
print("Saved salon_data.xlsx successfully.")
