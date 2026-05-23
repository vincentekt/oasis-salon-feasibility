import os
import re
from html.parser import HTMLParser

class SimpleHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.errors = []
        
    def handle_starttag(self, tag, attrs):
        # We don't need to track self-closing tags in HTML5
        self_closing = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 
                        'link', 'meta', 'param', 'source', 'track', 'wbr']
        if tag not in self_closing:
            self.tags.append(tag)
            
    def handle_endtag(self, tag):
        self_closing = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 
                        'link', 'meta', 'param', 'source', 'track', 'wbr']
        if tag in self_closing:
            return
        if not self.tags:
            self.errors.append(f"Unexpected closing tag </{tag}> without open tag")
        else:
            last_tag = self.tags.pop()
            if last_tag != tag:
                self.errors.append(f"Mismatched closing tag </{tag}> for <{last_tag}>")

def check_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    parser = SimpleHTMLValidator()
    try:
        parser.feed(html_content)
    except Exception as e:
        return False, [f"Parser error: {e}"]
        
    # Check for specific remnants
    remnants = []
    if "model-selector" in html_content:
        remnants.append("Found 'model-selector' remnant")
    if "model-btn" in html_content:
        remnants.append("Found 'model-btn' remnant")
        
    errors = parser.errors + remnants
    return len(errors) == 0, errors

def main():
    folder = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
    files = [f for f in os.listdir(folder) if f.endswith(".html")]
    
    print("=== VERIFYING WEB PROJECT FILES ===")
    
    all_ok = True
    for file in sorted(files):
        path = os.path.join(folder, file)
        ok, errors = check_html(path)
        if ok:
            print(f"[HTML: OK] - {file}")
        else:
            print(f"[HTML: ERROR] - {file}")
            for err in errors:
                print(f"  -> {err}")
            all_ok = False
            
    # Verify script.js using node check
    import subprocess
    js_path = os.path.join(folder, "script.js")
    result = subprocess.run(["node", "--check", js_path], capture_output=True, text=True)
    if result.returncode == 0:
        print("[JS: OK] - script.js")
    else:
        print("[JS: ERROR] - script.js")
        print(result.stderr)
        all_ok = False
        
    if all_ok:
        print("\nAll files verified successfully! [HTML: OK | JS: OK]")
    else:
        print("\nVerification found errors.")

if __name__ == "__main__":
    main()
