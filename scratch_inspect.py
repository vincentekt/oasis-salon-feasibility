import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for "hcmc.html" in script.js and print its block.
# Usually it's in a block starting with { and ending with } containing hcmc.html
match = re.search(r'\{[^{}]*?"url"\s*:\s*"hcmc\.html"[^{}]*?\}', text, re.DOTALL)
if match:
    print("=== HCMC Object ===")
    print(match.group(0))
else:
    # Try finding with some nesting if complexity is inside a nested object
    # Find hcmc.html and look backwards to the matching {
    idx = text.find('hcmc.html')
    if idx != -1:
        # scan backwards to { and forwards to }
        # Since complexity has its own { }, we need to handle nested braces or just print a large chunk.
        print("Found hcmc.html at index", idx)
        start = idx - 1000
        end = idx + 200
        print(text[start:end])
    else:
        print("hcmc.html not found in script.js")
