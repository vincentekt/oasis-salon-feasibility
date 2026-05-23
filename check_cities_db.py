import json
import re

path = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web\script.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Locate citiesDb array content
start = content.find("const citiesDb = [")
if start != -1:
    end = content.find("];", start)
    db_str = content[start + len("const citiesDb = "):end + 1]
    try:
        cities = json.loads(db_str)
        for city in cities:
            if city["name"] in ["Bangkok", "Kaohsiung"]:
                print(f"--- {city['name']} ---")
                print(json.dumps(city, indent=2))
    except Exception as e:
        print("Error parsing citiesDb JSON:", e)
else:
    print("Could not find citiesDb in script.js")
