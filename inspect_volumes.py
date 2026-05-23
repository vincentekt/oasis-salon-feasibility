with open('script.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
match = re.search(r'const volumesDb\s*=\s*\{(.*?)\};', text, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("volumesDb not found")
