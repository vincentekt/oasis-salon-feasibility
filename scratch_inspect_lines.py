with open('script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'const volumesDb' in line or '"hcmc":' in line:
        start = max(0, idx - 5)
        end = min(len(lines), idx + 10)
        print(f"=== Match at line {idx+1} ===")
        for i in range(start, end):
            print(f"{i+1}: {lines[i]}", end="")
