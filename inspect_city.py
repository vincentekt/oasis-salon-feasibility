import re

with open('script.js', 'r', encoding='utf-8') as f:
    text = f.read()

cities = ["Singapore", "Hong Kong", "Sydney", "Dubai"]
for city in cities:
    print(f"=== {city} ===")
    match = re.search(r'\{\s*"name":\s*"' + city + r'".*?\}', text, re.DOTALL)
    if match:
        print(match.group(0))
    else:
        print("Not found")
