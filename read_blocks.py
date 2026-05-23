with open("Oasis_Salon_Web/script.js", "r", encoding="utf-8") as f:
    text = f.read()

# Let's find "name": "Sarawak" in script.js and print its surrounding lines and their line numbers
lines = text.split("\n")
start_idx = -1
for i, line in enumerate(lines):
    if '"name": "Sarawak"' in line:
        start_idx = i
        break

if start_idx != -1:
    print(f"Sarawak entry starts around line {start_idx + 1}")
    for j in range(max(0, start_idx - 5), min(len(lines), start_idx + 30)):
        print(f"Line {j+1}: {lines[j]}")
else:
    print("Sarawak not found")
