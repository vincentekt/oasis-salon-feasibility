with open('hcmc.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'head spa' in line.lower() or 'starlight' in line.lower() or 'nihon' in line.lower() or 'upstairs' in line.lower():
        print(f"Line {idx+1}: {line.strip()}")
