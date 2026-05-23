import re

with open('script.js', 'r', encoding='utf-8') as f:
    text = f.read()

print("=== citiesDb Dubai ===")
# Find the object for Dubai in citiesDb
match = re.search(r'\{\s*"id":\s*"dubai".*?\}', text, re.DOTALL)
if match:
    print(match.group(0))
else:
    # try lowercase or name case
    match2 = re.search(r'\{\s*"name":\s*"Dubai".*?\}', text, re.DOTALL)
    if match2:
        print(match2.group(0))
    else:
        print("Dubai not found in citiesDb")

print("\n=== volumesDb Dubai ===")
vol_match = re.search(r'"dubai":\s*\d+', text)
if vol_match:
    print(vol_match.group(0))
else:
    print("Dubai not found in volumesDb")
