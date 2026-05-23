with open('script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '"name": "Dubai"' in line or '"dubai":' in line:
        print(f"Line {i+1}: {line.strip()}")
