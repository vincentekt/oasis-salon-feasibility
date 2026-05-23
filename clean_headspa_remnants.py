import os

def clean_files():
    folder = r"c:\Users\vince\Projects\HairSpa\Oasis_Salon_Web"
    
    # Define replacements: (Search string, Replacement string)
    replacements = [
        # Long/Specific Microscope and VIP Pod sentences
        ("Microscope check displays scalp health to the customer.", "Hair type and damage consultation to determine coloring & treatment plans."),
        ("Microscope check displays scalp health to the customer", "Hair type and damage consultation to determine coloring & treatment plans"),
        ("Microscope scanner checks scalp health.", "Detailed consultation to determine hair damage and coloring plans."),
        ("Microscope scanner checks scalp health", "Detailed consultation to determine hair damage and coloring plans"),
        ("Scalp Analysis: Microscope scanner checks scalp health.", "Hair Analysis: Detailed consultation to determine hair damage and coloring plans."),
        ("Scalp Analysis: Microscope scanner checks scalp health", "Hair Analysis: Detailed consultation to determine hair damage and coloring plans"),
        ("Microscope check displays scalp health", "Hair type and damage consultation"),
        ("Microscope scanner checks scalp health", "Detailed consultation to determine hair damage and coloring plans"),
        
        # VIP pod and private custom suites replacements
        ("private custom track lighting VIP pod for carbonated therapy", "semi-private styling station for custom coloring and soft-water washing"),
        ("private custom track lighting suite", "semi-private styling station"),
        ("Transition to private custom track lighting VIP pod for carbonated therapy.", "Transition to semi-private styling station for custom coloring and soft-water washing."),
        ("Transition to private custom track lighting VIP pod for carbonated therapy", "Transition to semi-private styling station for custom coloring and soft-water washing"),
        ("VIP pod for carbonated therapy", "semi-private styling station for custom coloring and soft-water washing"),
        ("VIP pod", "semi-private styling station"),
        ("vip pod", "semi-private styling station"),
        ("private pod", "semi-private styling station"),
        ("VIP pods", "semi-private styling stations"),
        ("vip pods", "semi-private styling stations"),
        ("private pods", "semi-private styling stations"),
        
        # Scalp-hair fusion / Rejuvenation replacements
        ("Scalp-Hair Fusion Therapy", "Soft-Water Hair Detox & Cut"),
        ("scalp-hair fusion therapy", "luxury soft-water hair treatment"),
        ("scalp-hair fusion", "luxury soft-water treatment"),
        ("scalp fusion", "soft-water hair conditioning"),
        ("deep scalp rejuvenation", "purified hair recovery"),
        ("scalp rejuvenation", "soft-water hair conditioning"),
        ("Carbonated Scalp Rejuvenation & Cut", "Soft-Water Hair Detox & Cut"),
        ("Carbonated Scalp Rejuvenation", "Soft-Water Hair Detox"),
        ("Scalp Rejuvenation", "Soft-Water Hair Conditioning"),
        ("Botanical Color & Scalp Rejuvenation", "Botanical Color & Soft-Water Rejuvenation"),
        ("Balayage & Scalp Fusion Therapy", "Balayage & Soft-Water Hair Conditioning"),
        ("Japanese-inspired scalp hair therapy", "purified soft-water conditioning"),
        ("scalp relief from sun/humidity", "hair detox from sun/humidity"),
        ("scalp care add-ons", "soft-water conditioning add-ons"),
        
        # Microscope scan general terms
        ("microscope check", "hair type and damage consultation"),
        ("microscope scan", "hair damage consultation"),
        ("microscope scanner", "hair damage consultation"),
        ("scalp scan", "hair damage consultation"),
        
        # Carbonated water systems replacements
        ("Japanese carbonated mist scalp therapy + stylist cut", "Japanese purified soft-water conditioning + stylist cut"),
        ("Japanese Carbonated Scalp & Precision Cut Combo", "Japanese Soft-Water Conditioning & Precision Cut Combo"),
        ("Japanese-spec carbonated water generators, treatment domes", "commercial water softening and filtration systems, premium styling stations"),
        ("Japanese carbonated (CO2) rinse generators", "commercial water softening and filtration systems"),
        ("Japanese carbonated scalp-hair conditioning", "commercial water softening and conditioning"),
        ("Japanese carbonated soft-water systems", "Japanese purified soft-water systems"),
        ("Japanese carbonated water therapy", "purified soft-water conditioning"),
        ("Carbonated water therapy + scalp hair health assessment verification", "Purified soft-water therapy + hair type and damage consultation"),
        ("commercial carbonated hair rinse systems", "commercial water softening and filtration systems"),
        ("Secure quotes for carbonated hair rinse systems.", "Secure quotes for commercial water softening and filtration systems."),
        ("Secure quotes for commercial carbonated hair rinse systems.", "Secure quotes for commercial water softening and filtration systems."),
        ("Secure quotes for commercial carbonated hair rinse systems", "Secure quotes for commercial water softening and filtration systems"),
        ("Secure quotes for carbonated hair rinse systems", "Secure quotes for commercial water softening and filtration systems"),
        ("carbonated water system generator", "multi-stage water filtration and softening tanks"),
        ("carbonated water generators", "multi-stage water filtration and softening tanks"),
        ("carbonated system generators", "multi-stage water filtration and softening tanks"),
        ("carbonated generators", "multi-stage water filtration and softening tanks"),
        ("carbonated water generator", "commercial water softening and filtration system"),
        ("Carbonated water generators", "Multi-stage water filtration and softening tanks"),
        ("Carbonated system generators", "Multi-stage water filtration and softening tanks"),
        ("Carbonated generators", "Multi-stage water filtration and softening tanks"),
        ("Carbonated water generator", "Commercial water softening and filtration system"),
        ("carbonated water filtration systems", "purified water filtration and softening systems"),
        ("carbonated hair rinse systems", "purified soft-water wash systems"),
        ("carbonated hair rinse system", "purified soft-water wash system"),
        ("carbonated rinse systems", "purified soft-water rinse systems"),
        ("carbonated rinse system", "purified soft-water rinse system"),
        ("carbonated rinse generators", "water softening and filtration systems"),
        ("Carbonated hair rinse systems", "Purified soft-water wash systems"),
        ("Carbonated hair rinse system", "Purified soft-water wash system"),
        ("Carbonated rinse systems", "Purified soft-water rinse systems"),
        ("Carbonated rinse system", "Purified soft-water rinse system"),
        ("carbonated water rinse system", "purified soft-water wash system"),
        ("carbonated water systems", "purified soft-water wash systems"),
        ("carbonated water-ring cleanse", "soft-water halo ring cleanse"),
        ("carbonated waterfall ring", "soft-water halo ring"),
        ("carbonated water-ring", "soft-water halo ring"),
        ("carbonated water ring", "soft-water halo ring"),
        ("carbonated soft-water", "purified soft-water"),
        ("carbonated scaling", "soft-water conditioning"),
        ("carbonated washing", "soft-water washing"),
        ("carbonated rinsing", "soft-water rinsing"),
        ("carbonated treatment", "soft-water treatment"),
        ("Carbonated Treatment", "Soft-Water Treatment"),
        ("carbonated hair rinse", "purified soft-water rinse"),
        ("carbonated mist rinse", "purified soft-water rinse"),
        ("carbonated scalp", "soft-water scalp"),
        ("carbonated mist generators", "commercial water softeners"),
        ("carbonated mist installation", "central water softener setup"),
        ("carbonated tank rentals", "water filtration filter replacements"),
        ("carbonated water system power", "water softening system power"),
        ("carbonated backwash stations", "purified soft-water backwash stations"),
        ("carbonated backwash station", "purified soft-water backwash station"),
        ("carbonated backstyling chairs", "lay-flat backwash beds"),
        ("carbonated styling chairs", "backwash styling beds"),
        ("carbonated rinse water generators", "water softening and filtration systems"),
        ("carbonated wash", "soft-water wash"),
        ("carbonated hair washes", "purified soft-water washes"),
        ("carbonated washes", "soft-water washes"),
        ("carbonated, chlorine-filtered water", "purified, chlorine-filtered water"),
        ("carbonated water filters", "purified water filters"),
        ("filtered carbonated water", "filtered soft-water"),
        ("carbonated systems", "water softening and filtration systems"),
        ("carbonated rinse setup", "purified soft-water rinse setup"),
        ("carbonated rinse", "purified soft-water rinse"),
        ("carbonated filtration systems", "water filtration systems"),
        ("carbon carbonated", "carbon"),
        
        # Lay-flat / Yume beds replacements
        ("Takara Belmont Yume flat-beds", "Premium lay-flat shampoo beds"),
        ("Takara Belmont Yume flat-bed", "Premium lay-flat shampoo bed"),
        ("Yume flat-beds", "lay-flat shampoo beds"),
        ("Yume flat-bed", "lay-flat shampoo bed"),
        ("Yume flat backstyling chairs", "ergonomic lay-flat shampoo beds"),
        ("Yume flat", "lay-flat shampoo bed"),
        ("Yume", "Lay-flat shampoo bed"),
        ("yume", "lay-flat shampoo bed"),
        
        # General formatting and specific terms
        ("Renovation & Pod Soundproofing", "Renovation & Semi-Private Partitioning"),
        ("Pod Soundproofing", "Semi-Private Partitioning"),
        
        # Bangkok specific cleanup fixes
        ("Creative Styling & Carbonated Soft-Water Reset", "Creative Styling & Soft-Water Deep Conditioning"),
    ]
    
    danang_specifics = [
        ("<strong>Location:</strong> Hai Chau city center ground-floor commercial unit.", "<strong>Location:</strong> An Thuong Beach precinct ground-floor commercial unit."),
        ("<strong>Expansion Trigger:</strong> Achieve USD 15k monthly revenue with 25%+ membership retention for 3 consecutive months before looking at An Thuong ward.", "<strong>Expansion Trigger:</strong> Achieve USD 15k monthly revenue with 25%+ membership retention for 3 consecutive months before looking at Hai Chau city center."),
        ("Rent (Hai Chau city space)", "Rent (An Thuong Beach space)"),
        ("in Hai Chau or a side-street in An Thuong. Target rent: USD 800/month", "in the An Thuong Beach precinct. Target rent: USD 800/month"),
    ]

    html_files = [f for f in os.listdir(folder) if f.endswith(".html")]
    
    for filename in sorted(html_files):
        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        original_content = content
        
        # Apply general replacements
        for search, replace in replacements:
            content = content.replace(search, replace)
            
        # Apply Da Nang specific replacements
        if filename == "danang.html":
            for search, replace in danang_specifics:
                content = content.replace(search, replace)
                
        if content != original_content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {filename}")

if __name__ == "__main__":
    clean_files()
