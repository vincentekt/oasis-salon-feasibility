import os, re

folder = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"

# Print ALL cities' candidate blocks + location table to audit what's there
files = [
    ('bangkok', 'bangkok.html'),
    ('binhduong', 'binhduong.html'),
    ('brisbane', 'brisbane.html'),
    ('busan', 'busan.html'),
    ('danang', 'danang.html'),
    ('dongnai', 'dongnai.html'),
    ('dubai', 'dubai.html'),
    ('fukuoka', 'fukuoka.html'),
    ('haiphong', 'haiphong.html'),
    ('hanoi', 'hanoi.html'),
    ('hcmc', 'hcmc.html'),
    ('hongkong', 'hongkong.html'),
    ('johor', 'johor.html'),
    ('kaohsiung', 'kaohsiung.html'),
    ('kuala_lumpur', 'kuala_lumpur.html'),
    ('macau', 'macau.html'),
    ('melbourne', 'melbourne.html'),
    ('okinawa', 'okinawa.html'),
    ('penang', 'penang.html'),
    ('perth', 'perth.html'),
    ('sabah', 'sabah.html'),
    ('sarawak', 'sarawak.html'),
    ('singapore', 'singapore.html'),
    ('sydney', 'sydney.html'),
    ('taichung', 'taichung.html'),
    ('tainan', 'tainan.html'),
    ('taipei', 'taipei.html'),
]

for key, fname in files:
    path = os.path.join(folder, fname)
    if not os.path.exists(path):
        print(f"MISSING: {fname}")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    m = re.search(r'const candidates\s*=\s*\[(.*?)\];', html, re.DOTALL)
    if m:
        block = m.group(1)
        # Extract each candidate name and lat/lng
        names = re.findall(r'name:\s*"([^"]+)"', block)
        lats = re.findall(r'lat:\s*([\d\.\-]+)', block)
        lngs = re.findall(r'lng:\s*([\d\.\-]+)', block)
        print(f"\n{key.upper()}:")
        for n, la, ln in zip(names, lats, lngs):
            print(f"  {n}  [{la}, {ln}]")
    else:
        print(f"\n{key.upper()}: NO candidates block found")
