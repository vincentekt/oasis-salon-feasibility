document.addEventListener('DOMContentLoaded', () => {
    // ==========================================
    // MULTILINGUAL DICTIONARY & LOGIC
    // ==========================================
    const jaTranslations = {
        // UI Navigation
        "Feasibility Study": "フィジビリティスタディ",
        "Dashboard": "ダッシュボード",
        "Vietnam": "ベトナム",
        "Malaysia": "マレーシア",
        "Taiwan": "台湾",
        "Australia": "オーストラリア",
        "Japan": "日本",
        "South Korea": "韓国",
        "Middle East": "中東",
        "Other APAC": "その他アジア太平洋",
        "Executive Summary": "エグゼクティブサマリー",
        "Business Positioning": "ビジネスポジショニング",
        "Market Context": "市場背景",
        "Target Segments": "ターゲット層",
        "Target Customer Segments": "ターゲット顧客層",
        "Location Study": "立地調査",
        "Competitor Study": "競合調査",
        "Unmet Needs & Gap": "未充足ニーズとギャップ",
        "Unmet Needs & Market Gap": "未充足ニーズと市場ギャップ",
        "Product Menu": "サービスメニュー",
        "Product / Service Menu": "サービスメニュー",
        "Packages & Memberships": "パッケージ＆会員制度",
        "Customer Journey": "カスタマージャーニー",
        "Customer Journey & Sales Flow": "カスタマージャーニー＆セールスフロー",
        "Setup & Layout": "店舗設計＆レイアウト",
        "Outlet Setup & Layout": "店舗設計＆レイアウト",
        "Staffing Model": "人員配置モデル",
        "Staffing Model (Base Operations)": "人員配置モデル（基本運営）",
        "Monthly OPEX": "月間運営費（OPEX）",
        "Monthly OPEX Estimate": "月間運営費想定",
        "CAPEX": "初期投資金額 (CAPEX)",
        "Initial Investment / CAPEX": "初期想定投資額 (CAPEX)",
        "Initial CAPEX Estimate": "初期想定投資額",
        "Initial CAPEX": "初期想定投資額",
        "Unit Economics": "ユニットエコノミクス",
        "Unit Economics & Breakeven": "ユニットエコノミクス＆損益分岐",
        "Setup Timeline": "開業スケジュール",
        "Setup Timeline (12 Weeks)": "開業スケジュール（12週間）",
        "Marketing Strategy": "マーケティング戦略",
        "Marketing": "マーケティング戦略",
        "Risks & Controls": "リスクと対策",
        "Key Risks & Controls": "主要リスクと対策",
        "Risks": "リスクと対策",
        "Recommendation": "最終提言",
        "Final Recommendation": "最終提言",
        "Next Steps": "今後の進め方",
        "Immediate Next Steps": "今後の進め方",
        
        // Table Columns
        "City": "都市",
        "Outlet Format": "店舗形態",
        "Target Size": "想定面積",
        "Average Ticket": "想定客単価",
        "COGS per Session": "施術原価",
        "Gross Margin": "売上総利益率",
        "Monthly Breakeven": "月間損益分岐点",
        "Daily Breakeven": "日間損益分岐点",
        "Corporate Income Tax (CIT) Rate": "法人税率 (CIT)",
        "Post-Tax Profit to OPEX Ratio": "税後利益/運営費比率",
        "Time to Payback (Post-Tax CAPEX)": "投資回収期間 (税後)",
        "Underserved Demand Gap (%)": "未充足需要ギャップ (%)",
        "Time from Nearest Airport": "最寄空港からの時間",
        "Key Strategic Risk": "主要な戦略的リスク",

        // Region Tabs & Buttons
        "All": "すべて",
        "Search cities...": "都市名で検索...",
        "Download Report": "レポートをダウンロード",
        
        // Custom Selector Regions
        "Select Region": "地域を選択",
        "All Regions": "すべての地域",
        
        // Model Toggle Names
        "Hair Spa": "ヘアスパモデル",
        "Pure Salon": "通常サロンモデル",
        
        // Cities
        "Bangkok": "バンコク",
        "Binh Duong": "ビンダイン",
        "Brisbane": "ブリスベン",
        "Busan": "釜山",
        "Da Nang": "ダナン",
        "Dong Nai": "ドンナイ",
        "Dubai": "ドバイ",
        "Fukuoka": "福岡",
        "Hai Phong": "ハイフォン",
        "Hanoi": "ハノイ",
        "Ho Chi Minh": "ホーチミン",
        "Hong Kong": "香港",
        "Johor Bahru": "ジョホールバル",
        "Johor Bahru (RTS)": "ジョホールバル (RTS)",
        "Kaohsiung": "高雄",
        "Kuala Lumpur": "クアラルンプール",
        "Macau": "マカオ",
        "Melbourne": "メルボルン",
        "Okinawa": "沖縄",
        "Penang": "ペナン",
        "Perth": "パース",
        "Sabah": "サバ",
        "Sarawak": "サラワク",
        "Singapore": "シンガポール",
        "Sydney": "シドニー",
        "Taichung": "台中",
        "Tainan": "台南",
        "Taipei": "台北",
        
        // Formats
        "Premium Boutique (MVP)": "プレミアムブティック (MVP)",
        "Industrial Corridor (MVP)": "産業回廊モデル (MVP)",
        "Subtropical Oasis (MVP)": "亜熱帯オアシスモデル (MVP)",
        "Coastal Luxury Suite (MVP)": "沿岸ラグジュアリースイート (MVP)",
        "Ultra-Luxury Suite (MVP)": "超ラグジュアリースィート (MVP)",
        "Coastal Tourism PoC / MVP": "沿岸観光PoC / MVP",
        "Heritage Boutique PoC": "歴史遺産ブティックPoC",
        "Coastal Expat Spa (MVP)": "沿岸移住者向けスパ (MVP)",
        "Luxury Micro-Spa / PoC": "高級マイクロスパ / PoC",
        "Luxury Suite PoC": "高級スイートPoC",
        "Boutique Salon / PoC": "ブティックサロン / PoC",
        "Premium Boutique Salon": "プレミアムブティックサロン",
        "Seaside Resort PoC / MVP": "海辺リゾートPoC / MVP",
        "Metro Port PoC / MVP": "港湾都市PoC / MVP",
        "Cross-Border PoC": "国境間PoC",
        "Aesthetic Lane Spa (MVP)": "路地裏美学スパ (MVP)",
        "Expat PoC / MVP": "移住者向けPoC / MVP",
        
        // Salon Formats
        "Premium Boutique Salon (MVP)": "ブティックヘアサロン (MVP)",
        "Industrial Corridor Salon (MVP)": "産業回廊サロン (MVP)",
        "Subtropical Oasis Salon (MVP)": "亜熱帯オアシスサロン (MVP)",
        "Coastal Luxury Salon Suite (MVP)": "沿岸贅沢サロン (MVP)",
        "Ultra-Luxury Salon Suite (MVP)": "超豪華ヘアサロン (MVP)",
        "Coastal Tourism Salon PoC / MVP": "PoC / MVP salon du lịch ven biển",
        "Heritage Boutique Salon PoC": "歴史遺産サロンPoC",
        "Coastal Expat Salon (MVP)": "沿岸移住者サロン (MVP)",
        "Luxury Micro-Salon / PoC": "高級マイクロサロン / PoC",
        "Luxury Salon Suite PoC": "高級サロンスイートPoC",
        "Boutique Salon Suite / PoC": "ブティックサロンスイートPoC",
        "Seaside Resort Salon PoC / MVP": "海辺リゾートサロンPoC",
        "Metro Port Salon PoC / MVP": "港湾都市サロンPoC",
        "Cross-Border Salon PoC": "国境間サロンPoC",
        "Aesthetic Lane Salon (MVP)": "路地裏美学サロン (MVP)",
        "Expat Salon PoC / MVP": "移住者向けサロンPoC",
        
        // Risks in table
        "Local market pricing pressure": "ローカル市場における価格競争",
        "Factory shift fluctuations": "工場シフトによる需要変動",
        "Regulatory & staff turnover": "規制変更およびスタッフ離職",
        "Seasonal tourist fluctuations": "観光客の季節的変動",
        "HCMC customs/shipping": "ホーチミン税関・物流遅延",
        "Cat Bi port customs": "カットビ港通関手続き",
        "Customs clearance from HK/MY": "香港・マレーシアからの通関遅延",
        "Malaysian OEM import customs": "マレーシアOEM輸入通関手続き",
        "High upstairs rent pressure": "空中階店舗の家賃上昇懸念",
        "RTS delays & staff retention": "RTS接続遅延と人材確保",
        "Staff retention & local competition": "人材流出と現地競合の台頭",
        "Licensing approvals & grease trap path": "営業ライセンス承認および排水設備",
        "Heritage DA & staff award labor": "歴史的建造物規制と労務アワード",
        "Expat season fluctuations": "外国人居住者の季節的帰国変動",
        "Lower local expat volume density": "地域における外国人居住者の低密度",
        "Isolation & remote supply chain": "地理的孤立とリモートサプライチェーン",
        "Extremely high rent overheads": "極めて高い家賃負担",
        "High overheads & DA delays": "高額な固定費と開発承認遅延",
        "Lobby size utilization": "ロビースペースの有効活用",
        "Lower volume density": "想定来店客数の低密度化",
        "Intense local competition": "激しい現地競合",
        "High local competition & high tax rate": "激しい競合および高水準の税率",
        "Staff recruitment award rates & local chains": "採用における法定賃金と現地チェーン",
        "High setup barrier & rent overheads": "高い参入障壁と高額な家賃",
        "Seasonal tourist fluctuations & typhoon risk": "季節的な観光変動と台風リスク",
        "Port traffic fluctuations & local salon competitors": "港湾交通の変動と現地競合サロン",
        "Lower local expat volume density": "地元外国人コミュニティの規模制限",
        
        // Subpage details tags
        "Target:": "対象エリア:",
        "Model:": "想定モデル:",
        "Currency:": "通貨:",
        "Scope:": "範囲:",
        "Version:": "バージョン:",
        "Prepared by Antigravity": "作成者: Antigravity",
        "Main Success Condition:": "主な成功条件:",
        "Positioned as:": "ポジショニング目標:",
        "Avoid being positioned as:": "回避すべきポジショニング:",
        "Core Customer Promise:": "顧客への提供価値:",
        "Market Fit:": "市場適合性（マーケットフィット）:",
        "Demographics:": "人口動態:",
        "Spending Power:": "購買力・消費動向:",
        "Weather Relevance:": "気候要因と需要:",
        "Environmental Drivers:": "環境要因と需要:",
        "Cultural Drivers:": "文化的推進要因:",
        "Regulatory Context:": "規制環境:",
        "Platform Focus:": "プロモーションチャネル:",
        "Influencer Seeding:": "インフルエンサー施策:",
        "Visual Proof:": "効果の可視化:",
        "Identified Risk": "特定されたリスク",
        "Severity": "重大度",
        "Control / Mitigation Strategy": "リスク対策・緩和策",
        "Risk Type": "リスク種類",
        "Mitigation / Control": "リスク対策",
        "Decision:": "決定事項:",
        "Location:": "立地選定:",
        "Setup:": "設備概要:",
        "Budget Ceiling:": "最大予算枠:",
        "Expansion Trigger:": "展開トリガー:",
        "Total Initial CAPEX": "初期投資想定額合計",
        "Total Base OPEX": "基本運営費合計",
        "Total Monthly OPEX": "月間運営費合計",
        "Contribution Margin per Ticket:": "1客あたり限界利益:",
        "Monthly Breakeven Volume:": "月間損益分岐客数:",
        "Daily Breakeven:": "日間損益分岐客数:",
        "Base Case Pre-Tax Monthly Net Profit:": "基本シナリオ 税引前月間純利益:",
        "Estimated Monthly Corporate Income Tax:": "推定月間法人税額:",
        "Post-Tax Net Monthly Profit (PAT):": "税引後月間純利益 (PAT):",
        "Post-Tax Profit to OPEX Ratio:": "税引後利益/運営費比率:",
        "Post-Tax CAPEX Payback Period:": "税引後投資回収期間:",
        "Post-Tax Financial Feasibility Analysis": "税後財務フィジビリティ分析",
        "All calculations in the table above represent pre-tax performance. Factoring in the local Corporate Income Tax (CIT) rate of": "上記テーブル内の数値はすべて税引前の値です。各都市の法人税率",
        "we arrive at the following post-tax projections for the Base Case:": "を反映した、基本シナリオの税後シミュレーションは以下の通りです:",
        
        // Table items
        "Breakeven Case": "損益分岐点シナリオ",
        "Base Case": "基本シナリオ",
        "High-Performance Case": "高成長シナリオ",
        "High Case": "高成長シナリオ",
        "Monthly Revenue": "月間売上",
        "COGS (10%)": "売上原価 (10%)",
        "Net Profit": "純利益",
        "Scenario": "シナリオ",
        "Monthly Revenue (USD)": "月間売上 (USD)",
        "Net Monthly Profit (USD)": "月間純利益 (USD)"
    };

    const viTranslations = {
        // UI Navigation
        "Feasibility Study": "Nghiên cứu khả thi",
        "Dashboard": "Bảng điều khiển",
        "Vietnam": "Việt Nam",
        "Malaysia": "Malaysia",
        "Taiwan": "Đài Loan",
        "Australia": "Úc",
        "Japan": "Nhật Bản",
        "South Korea": "Hàn Quốc",
        "Middle East": "Trung Đông",
        "Other APAC": "Khu vực APAC khác",
        "Executive Summary": "Tóm tắt dự án",
        "Business Positioning": "Định vị kinh doanh",
        "Market Context": "Bối cảnh thị trường",
        "Target Segments": "Phân khúc mục tiêu",
        "Target Customer Segments": "Phân khúc khách hàng mục tiêu",
        "Location Study": "Nghiên cứu vị trí",
        "Competitor Study": "Nghiên cứu đối thủ",
        "Unmet Needs & Gap": "Nhu cầu chưa đáp ứng & Khoảng trống",
        "Unmet Needs & Market Gap": "Nhu cầu chưa đáp ứng & Khoảng trống",
        "Product Menu": "Danh mục sản phẩm",
        "Product / Service Menu": "Danh mục dịch vụ",
        "Packages & Memberships": "Gói dịch vụ & Thẻ thành viên",
        "Customer Journey": "Hành trình khách hàng",
        "Customer Journey & Sales Flow": "Hành trình khách hàng & Quy trình bán hàng",
        "Setup & Layout": "Thiết lập & Mặt bằng",
        "Outlet Setup & Layout": "Thiết lập & Mặt bằng cửa hàng",
        "Staffing Model": "Mô hình nhân sự",
        "Staffing Model (Base Operations)": "Mô hình nhân sự (Vận hành cơ bản)",
        "Monthly OPEX": "Chi phí vận hành hàng tháng (OPEX)",
        "Monthly OPEX Estimate": "Ước tính OPEX hàng tháng",
        "CAPEX": "Chi phí đầu tư ban đầu (CAPEX)",
        "Initial Investment / CAPEX": "Vốn đầu tư ban đầu (CAPEX)",
        "Initial CAPEX Estimate": "Ước tính vốn đầu tư ban đầu",
        "Initial CAPEX": "Vốn đầu tư ban đầu",
        "Unit Economics": "Hiệu quả tài chính cửa hàng",
        "Unit Economics & Breakeven": "Hiệu quả tài chính & Điểm hòa vốn",
        "Setup Timeline": "Lộ trình thiết lập",
        "Setup Timeline (12 Weeks)": "Lộ trình thiết lập (12 tuần)",
        "Marketing Strategy": "Chiến lược tiếp thị",
        "Marketing": "Tiếp thị",
        "Risks & Controls": "Rủi ro & Kiểm soát",
        "Key Risks & Controls": "Rủi ro chính & Kiểm soát",
        "Risks": "Rủi ro chính",
        "Recommendation": "Khuyến nghị",
        "Final Recommendation": "Khuyến nghị cuối cùng",
        "Next Steps": "Các bước tiếp theo",
        "Immediate Next Steps": "Các bước tiếp theo",
        
        // Table Columns
        "City": "Thành phố",
        "Outlet Format": "Định dạng cửa hàng",
        "Target Size": "Diện tích mục tiêu",
        "Average Ticket": "Giá dịch vụ trung bình",
        "COGS per Session": "Giá vốn mỗi lượt",
        "Gross Margin": "Biên lợi nhuận gộp",
        "Monthly Breakeven": "Hòa vốn hàng tháng",
        "Daily Breakeven": "Hòa vốn hàng ngày",
        "Corporate Income Tax (CIT) Rate": "Thuế suất TNDN",
        "Post-Tax Profit to OPEX Ratio": "Thuế sau thuế / OPEX",
        "Time to Payback (Post-Tax CAPEX)": "Thời gian hoàn vốn (sau thuế)",
        "Underserved Demand Gap (%)": "Khoảng trống nhu cầu (%)",
        "Time from Nearest Airport": "Thời gian từ sân bay",
        "Key Strategic Risk": "Rủi ro chiến lược chính",

        // Region Tabs & Buttons
        "All": "Tất cả",
        "Search cities...": "Tìm kiếm thành phố...",
        "Download Report": "Tải báo cáo",
        
        // Custom Selector Regions
        "Select Region": "Chọn khu vực",
        "All Regions": "Tất cả khu vực",
        
        // Model Toggle Names
        "Hair Spa": "Gội đầu dưỡng sinh",
        "Pure Salon": "Salon tóc tiêu chuẩn",
        
        // Cities
        "Bangkok": "Bangkok",
        "Binh Duong": "Bình Dương",
        "Brisbane": "Brisbane",
        "Busan": "Busan",
        "Da Nang": "Đà Nẵng",
        "Dong Nai": "Đồng Nai",
        "Dubai": "Dubai",
        "Fukuoka": "Fukuoka",
        "Hai Phong": "Hải Phòng",
        "Hanoi": "Hà Nội",
        "Ho Chi Minh": "Hồ Chí Minh",
        "Hong Kong": "Hồng Kông",
        "Johor Bahru": "Johor Bahru",
        "Johor Bahru (RTS)": "Johor Bahru (RTS)",
        "Kaohsiung": "Cao Hùng",
        "Kuala Lumpur": "Kuala Lumpur",
        "Macau": "Macau",
        "Melbourne": "Melbourne",
        "Okinawa": "Okinawa",
        "Penang": "Penang",
        "Perth": "Perth",
        "Sabah": "Sabah",
        "Sarawak": "Sarawak",
        "Singapore": "Singapore",
        "Sydney": "Sydney",
        "Taichung": "Đài Trung",
        "Tainan": "Đài Nam",
        "Taipei": "Đài Bắc",
        
        // Formats
        "Premium Boutique (MVP)": "Boutique cao cấp (MVP)",
        "Industrial Corridor (MVP)": "Hành lang công nghiệp (MVP)",
        "Subtropical Oasis (MVP)": "Ốc đảo cận nhiệt đới (MVP)",
        "Coastal Luxury Suite (MVP)": "Suite ven biển cao cấp (MVP)",
        "Ultra-Luxury Suite (MVP)": "Suite siêu sang (MVP)",
        "Coastal Tourism PoC / MVP": "PoC / MVP du lịch ven biển",
        "Heritage Boutique PoC": "PoC Boutique di sản",
        "Coastal Expat Spa (MVP)": "Spa ven biển cho người nước ngoài (MVP)",
        "Luxury Micro-Spa / PoC": "Micro-Spa cao cấp / PoC",
        "Luxury Suite PoC": "PoC Suite cao cấp",
        "Boutique Salon / PoC": "Salon Boutique / PoC",
        "Premium Boutique Salon": "Salon Boutique cao cấp",
        "Seaside Resort PoC / MVP": "PoC / MVP resort ven biển",
        "Metro Port PoC / MVP": "PoC / MVP thành phố cảng",
        "Cross-Border PoC": "PoC xuyên biên giới",
        "Aesthetic Lane Spa (MVP)": "Spa thẩm mỹ trong ngõ (MVP)",
        "Expat PoC / MVP": "PoC / MVP cho người nước ngoài",
        
        // Salon Formats
        "Premium Boutique Salon (MVP)": "Boutique tóc (MVP)",
        "Industrial Corridor Salon (MVP)": "Salon hành lang công nghiệp (MVP)",
        "Subtropical Oasis Salon (MVP)": "Salon ốc đảo cận nhiệt đới (MVP)",
        "Coastal Luxury Salon Suite (MVP)": "Salon ven biển cao cấp (MVP)",
        "Ultra-Luxury Salon Suite (MVP)": "Salon siêu sang (MVP)",
        "Coastal Tourism Salon PoC / MVP": "PoC / MVP salon du lịch ven biển",
        "Heritage Boutique Salon PoC": "PoC Salon di sản",
        "Coastal Expat Salon (MVP)": "Salon ven biển cho người nước ngoài (MVP)",
        "Luxury Micro-Salon / PoC": "Micro-Salon cao cấp / PoC",
        "Luxury Salon Suite PoC": "PoC Salon Suite cao cấp",
        "Boutique Salon Suite / PoC": "PoC Boutique Salon Suite",
        "Seaside Resort Salon PoC / MVP": "PoC / MVP salon resort ven biển",
        "Metro Port Salon PoC / MVP": "PoC / MVP salon thành phố cảng",
        "Cross-Border Salon PoC": "PoC salon xuyên biên giới",
        "Aesthetic Lane Salon (MVP)": "Salon thẩm mỹ trong ngõ (MVP)",
        "Expat Salon PoC / MVP": "PoC / MVP salon ngoại quốc",
        
        // Risks in table
        "Local market pricing pressure": "Áp lực về giá ở thị trường nội địa",
        "Factory shift fluctuations": "Biến động theo ca tại nhà máy",
        "Regulatory & staff turnover": "Quy định pháp lý & biến động nhân sự",
        "Seasonal tourist fluctuations": "Biến động khách du lịch theo mùa",
        "HCMC customs/shipping": "Hải quan/vận chuyển tại TP.HCM",
        "Cat Bi port customs": "Thủ tục hải quan cảng Cát Bi",
        "Customs clearance from HK/MY": "Thông quan từ Hồng Kông/Malaysia",
        "Malaysian OEM import customs": "Hải quan nhập khẩu OEM từ Malaysia",
        "High upstairs rent pressure": "Áp lực thuê nhà ở tầng trên cao",
        "RTS delays & staff retention": "Trễ tuyến RTS & giữ chân nhân viên",
        "Staff retention & local competition": "Giữ chân nhân viên & cạnh tranh nội địa",
        "Licensing approvals & grease trap path": "Giấy phép & hệ thống lọc mỡ thải",
        "Heritage DA & staff award labor": "Quy định di sản & thỏa ước lao động",
        "Expat season fluctuations": "Biến động mùa cư trú của người nước ngoài",
        "Lower local expat volume density": "Mật độ người nước ngoài thấp tại địa phương",
        "Isolation & remote supply chain": "Cô lập địa lý & chuỗi cung ứng xa",
        "Extremely high rent overheads": "Chi phí thuê mặt bằng cực kỳ cao",
        "High overheads & DA delays": "Chi phí cố định cao & trễ giấy phép xây dựng",
        "Lobby size utilization": "Hiệu quả sử dụng diện tích sảnh",
        "Lower volume density": "Mật độ lượt khách thấp hơn",
        "Intense local competition": "Cạnh tranh nội địa gay gắt",
        "High local competition & high tax rate": "Cạnh tranh cao & thuế suất cao",
        "Staff recruitment award rates & local chains": "Lương nhân viên theo luật định & chuỗi nội địa",
        "High setup barrier & rent overheads": "Rào cản gia nhập cao & chi phí thuê mặt bằng lớn",
        "Seasonal tourist fluctuations & typhoon risk": "Biến động mùa du lịch & rủi ro bão",
        "Port traffic fluctuations & local salon competitors": "Biến động lượt khách cảng biển & đối thủ salon nội địa",
        "Lower local expat volume density": "Mật độ cộng đồng ngoại quốc thấp tại địa phương",
        
        // Subpage details tags
        "Target:": "Khu vực mục tiêu:",
        "Model:": "Mô hình dự kiến:",
        "Currency:": "Tiền tệ:",
        "Scope:": "Phạm vi:",
        "Version:": "Phiên bản:",
        "Prepared by Antigravity": "Người lập: Antigravity",
        "Main Success Condition:": "Điều kiện thành công chính:",
        "Positioned as:": "Định vị thương hiệu:",
        "Avoid being positioned as:": "Tránh định vị thương hiệu là:",
        "Core Customer Promise:": "Cam kết cốt lõi với khách hàng:",
        "Market Fit:": "Mức độ phù hợp thị trường:",
        "Demographics:": "Nhân khẩu học:",
        "Spending Power:": "Sức mua & Hành vi tiêu dùng:",
        "Weather Relevance:": "Tác động của thời tiết:",
        "Environmental Drivers:": "Yếu tố môi trường:",
        "Cultural Drivers:": "Yếu tố văn hóa:",
        "Regulatory Context:": "Môi trường pháp lý:",
        "Platform Focus:": "Kênh truyền thông tập trung:",
        "Influencer Seeding:": "Chiến dịch KOL/Influencer:",
        "Visual Proof:": "Minh chứng trực quan:",
        "Identified Risk": "Rủi ro được xác định",
        "Severity": "Mức độ nghiêm trọng",
        "Control / Mitigation Strategy": "Biện pháp kiểm soát & Giảm thiểu",
        "Risk Type": "Loại rủi ro",
        "Mitigation / Control": "Biện pháp kiểm soát",
        "Decision:": "Quyết định:",
        "Location:": "Vị trí địa lý:",
        "Setup:": "Thiết lập mặt bằng:",
        "Budget Ceiling:": "Ngân sách tối đa:",
        "Expansion Trigger:": "Kích hoạt mở rộng:",
        "Total Initial CAPEX": "Tổng vốn đầu tư ban đầu (CAPEX)",
        "Total Base OPEX": "Tổng chi phí vận hành cơ bản",
        "Total Monthly OPEX": "Tổng chi phí vận hành hàng tháng",
        "Contribution Margin per Ticket:": "Biên đóng góp trên mỗi dịch vụ:",
        "Monthly Breakeven Volume:": "Số lượng khách hòa vốn hàng tháng:",
        "Daily Breakeven:": "Số lượng khách hòa vốn hàng ngày:",
        "Base Case Pre-Tax Monthly Net Profit:": "Lợi nhuận thuần trước thuế (Kịch bản cơ sở):",
        "Estimated Monthly Corporate Income Tax:": "Thuế thu nhập doanh nghiệp ước tính:",
        "Post-Tax Net Monthly Profit (PAT):": "Lợi nhuận thuần sau thuế hàng tháng (PAT):",
        "Post-Tax Profit to OPEX Ratio:": "Tỷ lệ lợi nhuận sau thuế / OPEX:",
        "Post-Tax CAPEX Payback Period:": "Thời gian hoàn vốn sau thuế:",
        "Post-Tax Financial Feasibility Analysis": "Phân tích tính khả thi tài chính sau thuế",
        "All calculations in the table above represent pre-tax performance. Factoring in the local Corporate Income Tax (CIT) rate of": "Tất cả các tính toán trong bảng trên đại diện cho hiệu suất trước thuế. Tính thêm thuế suất TNDN",
        "we arrive at the following post-tax projections for the Base Case:": "chúng ta có các dự báo sau thuế cho kịch bản cơ sở như sau:",
        
        // Table items
        "Breakeven Case": "Kịch bản hòa vốn",
        "Base Case": "Kịch bản cơ sở",
        "High-Performance Case": "Kịch bản tăng trưởng cao",
        "High Case": "Kịch bản tăng trưởng cao",
        "Monthly Revenue": "Doanh thu hàng tháng",
        "COGS (10%)": "Giá vốn hàng bán (10%)",
        "Net Profit": "Lợi nhuận thuần",
        "Scenario": "Kịch bản",
        "Monthly Revenue (USD)": "Doanh thu hàng tháng (USD)",
        "Net Monthly Profit (USD)": "Lợi nhuận thuần hàng tháng (USD)"
    };

    function translateDOM(root) {
        const lang = getActiveState().lang;
        if (lang === 'en') return;

        const translations = lang === 'ja' ? jaTranslations : viTranslations;

        const walker = document.createTreeWalker(
            root, 
            NodeFilter.SHOW_TEXT, 
            null, 
            false
        );
        
        let node;
        while (node = walker.nextNode()) {
            const text = node.nodeValue.trim();
            const cleanText = text.replace(/:$/, "").trim();
            if (translations[cleanText]) {
                let translated = translations[cleanText];
                if (node.nodeValue.endsWith(':')) {
                    translated += ':';
                }
                node.nodeValue = node.nodeValue.replace(text, translated);
            }
        }

        // Placeholders translation
        const inputs = root.querySelectorAll ? root.querySelectorAll('input[placeholder]') : [];
        inputs.forEach(input => {
            const ph = input.getAttribute('placeholder');
            if (translations[ph]) {
                input.setAttribute('placeholder', translations[ph]);
            }
        });
    }

    // Dynamic URL hash propagation
    function updateLinkHashes(lang) {
        const links = document.querySelectorAll('a');
        links.forEach(link => {
            const href = link.getAttribute('href');
            if (!href) return;
            
            if (href.includes('.html') && !href.startsWith('#')) {
                const baseHref = href.split('#')[0];
                const pageHash = href.split('#')[1] || '';
                
                const hashParts = [];
                if (lang !== 'en') hashParts.push(lang);
                
                let anchor = '';
                if (pageHash) {
                    const parts = pageHash.split('-');
                    const stateCodes = ['ja', 'vi', 'en', 'spa', 'salon'];
                    anchor = parts.filter(p => !stateCodes.includes(p)).join('-');
                }
                
                if (anchor) hashParts.push(anchor);
                
                const newHash = hashParts.join('-');
                link.setAttribute('href', baseHref + (newHash ? '#' + newHash : ''));
            }
        });
    }

    function getActiveState() {
        let lang = 'en';
        const hash = window.location.hash;
        
        if (hash) {
            const cleanHash = hash.substring(1); // remove '#'
            const parts = cleanHash.split('-');
            
            if (parts[0] === 'ja') {
                lang = 'ja';
            } else if (parts[0] === 'vi') {
                lang = 'vi';
            }
        } else {
            try {
                lang = localStorage.getItem('selectedLanguage') || 'en';
            } catch (e) {
                lang = 'en';
            }
        }
        return { lang, model: 'salon' };
    }

    // Save to localStorage
    const activeState = getActiveState();
    try {
        localStorage.setItem('selectedLanguage', activeState.lang);
        localStorage.removeItem('selectedModel');
    } catch (e) {}

    // ==========================================
    // DYNAMIC CITIES DATABASE
    // ==========================================
    const citiesDb = [
    {
        "name": "Bangkok",
        "region": "Other APAC",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 110k - 120k",
        "opex": "USD 14,000",
        "ticket": "USD 180",
        "cogs": "USD 18.00",
        "margin": "90%",
        "breakeven": "~86 customers",
        "daily_breakeven": "~2.9 customers/day",
        "tax": "20.0%",
        "pat_ratio": "410% (Post-Tax)",
        "payback": "2 Months",
        "underserved": "42%",
        "airport": "30 mins (BKK) / 35 mins (DMK)",
        "risk": "Hard water (TDS 300–500 ppm) requires soft-water filtration investment",
        "complexity": {
            "total": 355,
            "loc": "90 hrs (Thonglor search)",
            "design": "65 hrs (Boutique styling layout)",
            "staff": "120 hrs (4 total headcount)",
            "logistics": "80 hrs (Filtration & imports)"
        },
        "coords": [
            13.73,
            100.58
        ],
        "url": "bangkok.html"
    },
    {
        "name": "Binh Duong",
        "region": "Vietnam",
        "format": "Industrial Expat Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 19k - 24k",
        "opex": "USD 4,750",
        "ticket": "USD 45",
        "cogs": "USD 4.50",
        "margin": "90%",
        "breakeven": "~117 customers",
        "daily_breakeven": "~3.9 customers/day",
        "tax": "20.0%",
        "pat_ratio": "186% (Post-Tax)",
        "payback": "3 Months",
        "underserved": "61%",
        "airport": "45 mins (SGN)",
        "risk": "Korean factory shift rotation cycles",
        "complexity": {
            "total": 388,
            "loc": "110 hrs (Factory corridor search)",
            "design": "38 hrs (Styling stations layout)",
            "staff": "130 hrs (5 total headcount)",
            "logistics": "110 hrs (HCMC customs)"
        },
        "coords": [
            10.9805,
            106.6515
        ],
        "url": "binhduong.html"
    },
    {
        "name": "Brisbane",
        "region": "Australia",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 110k - 130k",
        "opex": "USD 25,000",
        "ticket": "USD 240",
        "cogs": "USD 24.00",
        "margin": "90%",
        "breakeven": "~116 customers",
        "daily_breakeven": "~3.9 customers/day",
        "tax": "30.0%",
        "pat_ratio": "82% (Post-Tax)",
        "payback": "7 Months",
        "underserved": "42%",
        "airport": "20 mins (BNE)",
        "risk": "High AU labour costs & UV color fade turnover",
        "complexity": {
            "total": 335,
            "loc": "100 hrs (Fortitude Valley search)",
            "design": "35 hrs (Subtropical garden & plumbing)",
            "staff": "110 hrs (4 total headcount)",
            "logistics": "90 hrs (Premium styling tools)"
        },
        "coords": [
            -27.4705,
            153.026
        ],
        "url": "brisbane.html"
    },
    {
        "name": "Da Nang",
        "region": "Vietnam",
        "format": "Coastal Expat (MVP) Salon",
        "size": "800 sq ft",
        "capex": "USD 18k - 23k",
        "opex": "USD 4,800",
        "ticket": "USD 20",
        "cogs": "USD 2.00",
        "margin": "90%",
        "breakeven": "~267 customers",
        "daily_breakeven": "~8.9 customers/day",
        "tax": "20.0%",
        "pat_ratio": "24% (Post-Tax)",
        "payback": "18 Months",
        "underserved": "29%",
        "airport": "10 mins (DAD)",
        "risk": "Seasonal tourism drop",
        "complexity": {
            "total": 320,
            "loc": "80 hrs (Hai Chau/An Thuong search)",
            "design": "60 hrs (4 styling stations)",
            "staff": "110 hrs (5 total headcount)",
            "logistics": "70 hrs (Da Nang port access)"
        },
        "coords": [
            16.0544,
            108.2022
        ],
        "url": "danang.html"
    },
    {
        "name": "Dong Nai",
        "region": "Vietnam",
        "format": "Industrial Expat Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 18k - 23k",
        "opex": "USD 4,640",
        "ticket": "USD 55",
        "cogs": "USD 5.50",
        "margin": "90%",
        "breakeven": "~93 customers",
        "daily_breakeven": "~3.1 customers/day",
        "tax": "20.0%",
        "pat_ratio": "136% (Post-Tax)",
        "payback": "8 Months",
        "underserved": "71%",
        "airport": "60 mins (SGN)",
        "risk": "Zero local competition but small total expat population",
        "complexity": {
            "total": 440,
            "loc": "110 hrs (Bien Hoa city search)",
            "design": "80 hrs (Soundproof styling stations)",
            "staff": "130 hrs (5 total headcount)",
            "logistics": "120 hrs (HCMC customs/shipping)"
        },
        "coords": [
            10.9574,
            106.8427
        ],
        "url": "dongnai.html"
    },
    {
        "name": "Hai Phong",
        "region": "Vietnam",
        "format": "Industrial Expat (MVP) Salon",
        "size": "800 sq ft",
        "capex": "USD 18k - 23k",
        "opex": "USD 5,200",
        "ticket": "USD 45",
        "cogs": "USD 4.50",
        "margin": "90%",
        "breakeven": "~129 customers",
        "daily_breakeven": "~4.3 customers/day",
        "tax": "20.0%",
        "pat_ratio": "91% (Post-Tax)",
        "payback": "7 Months",
        "underserved": "55%",
        "airport": "15 mins (HPH)",
        "risk": "Reliance on Deep C / VSIP industrial zone expat demand",
        "complexity": {
            "total": 410,
            "loc": "100 hrs (Vinhomes Imperia search)",
            "design": "70 hrs (Soundproof styling stations)",
            "staff": "120 hrs (5 total headcount)",
            "logistics": "120 hrs (Cat Bi port customs)"
        },
        "coords": [
            20.8449,
            106.6881
        ],
        "url": "haiphong.html"
    },
    {
        "name": "Hanoi",
        "region": "Vietnam",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 50k - 58k",
        "opex": "USD 6,600",
        "ticket": "USD 95",
        "cogs": "USD 9.50",
        "margin": "90%",
        "breakeven": "~77 customers",
        "daily_breakeven": "~2.6 customers/day",
        "tax": "20.0%",
        "pat_ratio": "331% (Post-Tax)",
        "payback": "2 Months",
        "underserved": "30%",
        "airport": "30 mins (HAN)",
        "risk": "Foreign license compliance",
        "complexity": {
            "total": 445,
            "loc": "110 hrs (Tay Ho lakefront search)",
            "design": "75 hrs (Quiet styling stations)",
            "staff": "140 hrs (6 total headcount)",
            "logistics": "120 hrs (Customs clearance from HK/MY)"
        },
        "coords": [
            21.0285,
            105.8522
        ],
        "url": "hanoi.html"
    },
    {
        "name": "Ho Chi Minh",
        "region": "Vietnam",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 90k - 110k",
        "opex": "USD 10,700",
        "ticket": "USD 95",
        "cogs": "USD 9.50",
        "margin": "90%",
        "breakeven": "~125 customers",
        "daily_breakeven": "~4.2 customers/day",
        "tax": "20.0%",
        "pat_ratio": "174% (Post-Tax)",
        "payback": "5 Months",
        "underserved": "38%",
        "airport": "30 mins (SGN)",
        "risk": "Foreign license compliance",
        "complexity": {
            "total": 430,
            "loc": "120 hrs (District 1/3 search)",
            "design": "40 hrs (Styling stations layout)",
            "staff": "150 hrs (4 total headcount)",
            "logistics": "120 hrs (Imported salon color products)"
        },
        "coords": [
            10.79,
            106.72
        ],
        "url": "hcmc.html"
    },
    {
        "name": "Hong Kong",
        "region": "Other APAC",
        "format": "Premium Boutique Salon (MVP)",
        "size": "750 sq ft",
        "capex": "USD 170k - 190k",
        "opex": "USD 32,000",
        "ticket": "USD 200",
        "cogs": "USD 20.00",
        "margin": "90%",
        "breakeven": "~178 customers",
        "daily_breakeven": "~5.9 customers/day",
        "tax": "16.5%",
        "pat_ratio": "103% (Post-Tax)",
        "payback": "5 Months",
        "underserved": "48%",
        "airport": "40 mins (HKG)",
        "risk": "High setup barrier & rent overheads",
        "complexity": {
            "total": 260,
            "loc": "80 hrs (Causeway Bay search)",
            "design": "30 hrs (Compact 4-station layout)",
            "staff": "100 hrs (3 total headcount)",
            "logistics": "50 hrs (Standard shipping hubs)"
        },
        "coords": [
            22.285,
            114.157
        ],
        "url": "hongkong.html"
    },
    {
        "name": "Johor Bahru (RTS)",
        "region": "Malaysia",
        "format": "Cross-Border Premium Salon (RTS PoC)",
        "size": "1,000 sq ft",
        "capex": "USD 42k - 51k",
        "opex": "USD 6,800",
        "ticket": "USD 65",
        "cogs": "USD 6.50",
        "margin": "90%",
        "breakeven": "~116 customers",
        "daily_breakeven": "~3.9 customers/day",
        "tax": "24.0%",
        "pat_ratio": "72% (Post-Tax)",
        "payback": "12 Months",
        "underserved": "52%",
        "airport": "30 mins (JHB) / 50 mins (SIN)",
        "risk": "RTS delays & staff retention",
        "complexity": {
            "total": 315,
            "loc": "90 hrs (RTS skybridge connection)",
            "design": "65 hrs (1,000 sq ft layout)",
            "staff": "110 hrs (5 total headcount)",
            "logistics": "50 hrs (Local MY supplier access)"
        },
        "coords": [
            1.464,
            103.768
        ],
        "url": "johor.html"
    },
    {
        "name": "Kuala Lumpur",
        "region": "Malaysia",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 90k - 100k",
        "opex": "USD 8,928",
        "ticket": "USD 90",
        "cogs": "USD 9.00",
        "margin": "90%",
        "breakeven": "~110 customers",
        "daily_breakeven": "~3.7 customers/day",
        "tax": "24.0%",
        "pat_ratio": "239% (Post-Tax)",
        "payback": "4 Months",
        "underserved": "52%",
        "airport": "45 mins (KUL)",
        "risk": "Bangsar clustering — KLCC/Ampang corridor unaddressed by all competitors",
        "complexity": {
            "total": 375,
            "loc": "90 hrs (Mont Kiara search)",
            "design": "65 hrs (Luxurious styling stations layout)",
            "staff": "130 hrs (5 total headcount)",
            "logistics": "90 hrs (Premium styling products)"
        },
        "coords": [
            3.139,
            101.6869
        ],
        "url": "kuala_lumpur.html"
    },
    {
        "name": "Macau",
        "region": "Other APAC",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 95k - 110k",
        "opex": "USD 15,000",
        "ticket": "USD 115",
        "cogs": "USD 11.50",
        "margin": "90%",
        "breakeven": "~145 customers",
        "daily_breakeven": "~4.8 customers/day",
        "tax": "12.0%",
        "pat_ratio": "121% (Post-Tax)",
        "payback": "6 Months",
        "underserved": "25%",
        "airport": "10 mins (MFM)",
        "risk": "Licensing approvals & grease trap path",
        "complexity": {
            "total": 350,
            "loc": "100 hrs (Taipa Central search)",
            "design": "70 hrs (Boutique layout & drainage path)",
            "staff": "110 hrs (5 total headcount)",
            "logistics": "70 hrs (Hong Kong border ports)"
        },
        "coords": [
            22.1987,
            113.5439
        ],
        "url": "macau.html"
    },
    {
        "name": "Melbourne",
        "region": "Australia",
        "format": "Ground-Floor Premium Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 126k - 145k",
        "opex": "USD 25,200",
        "ticket": "USD 250",
        "cogs": "USD 25.00",
        "margin": "90%",
        "breakeven": "~112 customers",
        "daily_breakeven": "~3.7 customers/day",
        "tax": "30.0%",
        "pat_ratio": "216% (Post-Tax)",
        "payback": "2.5 Months",
        "underserved": "0%",
        "airport": "28 mins (MEL)",
        "risk": "Staff recruitment award rates & local chains",
        "complexity": {
            "total": 329,
            "loc": "110 hrs (South Yarra/Fitzroy)",
            "design": "19 hrs (Acoustic design & plumbing)",
            "staff": "110 hrs (4 total headcount)",
            "logistics": "90 hrs (Premium styling chairs)"
        },
        "coords": [
            -37.8136,
            144.9631
        ],
        "url": "melbourne.html"
    },
    {
        "name": "Penang",
        "region": "Malaysia",
        "format": "Expat Salon PoC / MVP",
        "size": "800 sq ft",
        "capex": "USD 55k - 65k",
        "opex": "USD 6,400",
        "ticket": "USD 45",
        "cogs": "USD 4.50",
        "margin": "90%",
        "breakeven": "~158 customers",
        "daily_breakeven": "~5.3 customers/day",
        "tax": "24.0%",
        "pat_ratio": "118% (Post-Tax)",
        "payback": "8 Months",
        "underserved": "11%",
        "airport": "35 mins (PEN)",
        "risk": "Expat season fluctuations",
        "complexity": {
            "total": 305,
            "loc": "80 hrs (Gurney Drive shophouses)",
            "design": "55 hrs (Compact 4-station style)",
            "staff": "110 hrs (5 total headcount)",
            "logistics": "60 hrs (Local organic supplier)"
        },
        "coords": [
            5.4282,
            100.315
        ],
        "url": "penang.html"
    },
    {
        "name": "Sabah",
        "region": "Malaysia",
        "format": "Coastal Tourism PoC / MVP Salon",
        "size": "800 sq ft",
        "capex": "USD 24k - 30k",
        "opex": "USD 4,800",
        "ticket": "USD 26",
        "cogs": "USD 2.60",
        "margin": "90%",
        "breakeven": "~205 customers",
        "daily_breakeven": "~6.8 customers/day",
        "tax": "24.0%",
        "pat_ratio": "52% (Post-Tax)",
        "payback": "11 Months",
        "underserved": "35%",
        "airport": "15 mins (BKI)",
        "risk": "Seasonal tourist fluctuations",
        "complexity": {
            "total": 425,
            "loc": "80 hrs (KK prime retail search)",
            "design": "65 hrs (Waterfront coastal layout)",
            "staff": "110 hrs (5 total headcount)",
            "logistics": "80 hrs (Shipments from West Malaysia)"
        },
        "coords": [
            5.9804,
            116.0735
        ],
        "url": "sabah.html"
    },
    {
        "name": "Sarawak",
        "region": "Malaysia",
        "format": "Heritage Boutique Salon PoC",
        "size": "800 sq ft",
        "capex": "USD 54k - 66k",
        "opex": "USD 6,200",
        "ticket": "USD 46",
        "cogs": "USD 4.60",
        "margin": "90%",
        "breakeven": "~150 customers",
        "daily_breakeven": "~5.0 customers/day",
        "tax": "24.0%",
        "pat_ratio": "99% (Post-Tax)",
        "payback": "10 Months",
        "underserved": "22%",
        "airport": "20 mins (KCH)",
        "risk": "Shell/Petronas expat rotation cycles & East Malaysia logistics cost",
        "complexity": {
            "total": 400,
            "loc": "80 hrs (Waterfront heritage hunting)",
            "design": "60 hrs (Wabi-sabi boutique layout)",
            "staff": "110 hrs (5 total headcount)",
            "logistics": "70 hrs (East Malaysia shipping paths)"
        },
        "coords": [
            1.5533,
            110.3592
        ],
        "url": "sarawak.html"
    },
    {
        "name": "Perth",
        "region": "Australia",
        "format": "Coastal Expat Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 78k - 90k",
        "opex": "USD 18,400",
        "ticket": "USD 78",
        "cogs": "USD 7.80",
        "margin": "90%",
        "breakeven": "~262 customers",
        "daily_breakeven": "~8.7 customers/day",
        "tax": "30.0%",
        "pat_ratio": "22% (Post-Tax)",
        "payback": "21 Months",
        "underserved": "24%",
        "airport": "22 mins (PER)",
        "risk": "Isolation & remote supply chain",
        "complexity": {
            "total": 350,
            "loc": "90 hrs (Subiaco/Cottesloe)",
            "design": "70 hrs (Coastal design & plumbing)",
            "staff": "110 hrs (5 total headcount)",
            "logistics": "80 hrs (Imported cosmetics)"
        },
        "coords": [
            -31.9505,
            115.8605
        ],
        "url": "perth.html"
    },
    {
        "name": "Singapore",
        "region": "Other APAC",
        "format": "Premium Boutique Salon",
        "size": "750 sq ft",
        "capex": "USD 110k - 126k",
        "opex": "USD 21,800",
        "ticket": "USD 180",
        "cogs": "USD 18.00",
        "margin": "90%",
        "breakeven": "~135 customers",
        "daily_breakeven": "~4.5 customers/day",
        "tax": "17.0%",
        "pat_ratio": "162% (Post-Tax)",
        "payback": "3 Months",
        "underserved": "45%",
        "airport": "25 mins (SIN)",
        "risk": "Extremely high rent overheads",
        "complexity": {
            "total": 280,
            "loc": "85 hrs (Orchard boutique search)",
            "design": "30 hrs (Semi-private layout)",
            "staff": "110 hrs (4 total headcount)",
            "logistics": "55 hrs (Imported salon systems)"
        },
        "coords": [
            1.3521,
            103.8198
        ],
        "url": "singapore.html"
    },
    {
        "name": "Sydney",
        "region": "Australia",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 110k - 130k",
        "opex": "USD 27,500",
        "ticket": "USD 250",
        "cogs": "USD 25.00",
        "margin": "90%",
        "breakeven": "~122 customers",
        "daily_breakeven": "~4.1 customers/day",
        "tax": "30.0%",
        "pat_ratio": "128% (Post-Tax)",
        "payback": "3 Months",
        "underserved": "38%",
        "airport": "22 mins (SYD)",
        "risk": "High AU labour costs & inner-west DA heritage restrictions",
        "complexity": {
            "total": 360,
            "loc": "120 hrs (Paddington/Double Bay)",
            "design": "40 hrs (Heritage DA acoustics & styling layout)",
            "staff": "120 hrs (4 total headcount)",
            "logistics": "80 hrs (Imported cosmetics)"
        },
        "coords": [
            -33.8688,
            151.2093
        ],
        "url": "sydney.html"
    },
    {
        "name": "Kaohsiung",
        "region": "Taiwan",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 95k - 115k",
        "opex": "USD 10,500",
        "ticket": "USD 120",
        "cogs": "USD 12.00",
        "margin": "90%",
        "breakeven": "~97 customers",
        "daily_breakeven": "~3.2 customers/day",
        "tax": "20.0%",
        "pat_ratio": "166% (Post-Tax)",
        "payback": "6 Months",
        "underserved": "22%",
        "airport": "15 mins (KHH)",
        "risk": "THSR weekend traffic dependency & Round2/UCA chain pricing pressure",
        "complexity": {
            "total": 170,
            "loc": "60 hrs (Zuoying storefront search)",
            "design": "30 hrs (Styling stations layout)",
            "staff": "80 hrs (Stylist hiring & training)",
            "logistics": "40 hrs (Styling equipment delivery)"
        },
        "coords": [
            22.6273,
            120.3014
        ],
        "url": "kaohsiung.html"
    },
    {
        "name": "Taichung",
        "region": "Taiwan",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 90k - 110k",
        "opex": "USD 14,000",
        "ticket": "USD 110",
        "cogs": "USD 11.00",
        "margin": "90%",
        "breakeven": "~141 customers",
        "daily_breakeven": "~4.7 customers/day",
        "tax": "20.0%",
        "pat_ratio": "115% (Post-Tax)",
        "payback": "6 Months",
        "underserved": "44%",
        "airport": "30 mins (RMQ)",
        "risk": "Qi-qi district premium rent inflation & experienced color stylist scarcity",
        "complexity": {
            "total": 405,
            "loc": "130 hrs (Xitun storefront search)",
            "design": "55 hrs (4 styling stations & lobby)",
            "staff": "130 hrs (4 total headcount)",
            "logistics": "90 hrs (High-end styling tools)"
        },
        "coords": [
            24.162,
            120.64
        ],
        "url": "taichung.html"
    },
    {
        "name": "Tainan",
        "region": "Taiwan",
        "format": "Premium Boutique Salon (MVP)",
        "size": "750 sq ft",
        "capex": "USD 90k - 110k",
        "opex": "USD 10,200",
        "ticket": "USD 80",
        "cogs": "USD 8.00",
        "margin": "90%",
        "breakeven": "~142 customers",
        "daily_breakeven": "~4.7 customers/day",
        "tax": "20.0%",
        "pat_ratio": "144% (Post-Tax)",
        "payback": "7 Months",
        "underserved": "22%",
        "airport": "15 mins (TNN) / 45 mins (KHH)",
        "risk": "TSMC expat base still building — 2025–2026 ramp dependency",
        "complexity": {
            "total": 355,
            "loc": "90 hrs (East District location search)",
            "design": "65 hrs (Premium styling layout)",
            "staff": "120 hrs (Hiring & styling training)",
            "logistics": "80 hrs (Organic salon imports)"
        },
        "coords": [
            22.9908,
            120.2133
        ],
        "url": "tainan.html"
    },
    {
        "name": "Taipei",
        "region": "Taiwan",
        "format": "Premium Boutique Salon",
        "size": "850 sq ft",
        "capex": "USD 63k - 75k",
        "opex": "USD 11,360",
        "ticket": "USD 104",
        "cogs": "USD 10.40",
        "margin": "90%",
        "breakeven": "~122 customers",
        "daily_breakeven": "~4.1 customers/day",
        "tax": "20.0%",
        "pat_ratio": "182% (Post-Tax)",
        "payback": "3 Months",
        "underserved": "30%",
        "airport": "15 mins (TSA) / 45 mins (TPE)",
        "risk": "Intense local competition",
        "complexity": {
            "total": 405,
            "loc": "100 hrs (Da'an alleyway search)",
            "design": "75 hrs (Wabi-sabi aesthetics)",
            "staff": "130 hrs (4 total headcount)",
            "logistics": "100 hrs (Organic imports)"
        },
        "coords": [
            25.033,
            121.565
        ],
        "url": "taipei.html"
    },
    {
        "name": "Fukuoka",
        "region": "Japan",
        "format": "Premium Boutique Salon (MVP)",
        "size": "900 sq ft",
        "capex": "USD 57k - 66k",
        "opex": "USD 9,600",
        "ticket": "USD 49",
        "cogs": "USD 4.90",
        "margin": "90%",
        "breakeven": "~218 customers",
        "daily_breakeven": "~7.3 customers/day",
        "tax": "30.0%",
        "pat_ratio": "41% (Post-Tax)",
        "payback": "16 Months",
        "underserved": "12%",
        "airport": "15 mins (FUK)",
        "risk": "30% JP corporate tax & intense TONI&GUY / saco japan local competition",
        "complexity": {
            "total": 425,
            "loc": "80 hrs (Tenjin prime storefront search)",
            "design": "65 hrs (Premium luxury spa layout)",
            "staff": "120 hrs (Staff licensing compliance)",
            "logistics": "160 hrs (Local premium product distribution)"
        },
        "coords": [
            33.5902,
            130.4017
        ],
        "url": "fukuoka.html"
    },
    {
        "name": "Okinawa",
        "region": "Japan",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 90k - 106k",
        "opex": "USD 13,000",
        "ticket": "USD 120",
        "cogs": "USD 12.00",
        "margin": "90%",
        "breakeven": "~120 customers",
        "daily_breakeven": "~4.0 customers/day",
        "tax": "30.0%",
        "pat_ratio": "161% (Post-Tax)",
        "payback": "5 Months",
        "underserved": "55%",
        "airport": "15 mins (OKA)",
        "risk": "Military-zone dependency & bilingual stylist scarcity",
        "complexity": {
            "total": 480,
            "loc": "120 hrs (Omoromachi premium boutique search)",
            "design": "90 hrs (Premium boutique styling layout)",
            "staff": "165 hrs (Stylist & assistant hiring & training)",
            "logistics": "105 hrs (Takara Belmont logistics setup)"
        },
        "coords": [
            26.2124,
            127.6809
        ],
        "url": "okinawa.html"
    },
        {
        "name": "Busan",
        "region": "South Korea",
        "format": "Ground-Floor Premium Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 120k - 144k",
        "opex": "USD 15,400",
        "ticket": "USD 100",
        "cogs": "USD 10.00",
        "margin": "90%",
        "breakeven": "~171 customers",
        "daily_breakeven": "~5.7 customers/day",
        "tax": "20.0%",
        "pat_ratio": "106% (Post-Tax)",
        "payback": "8 Months",
        "underserved": "35%",
        "airport": "30 mins (PUS)",
        "risk": "K-franchise salon dominance (Juno Hair 200+ outlets) & stylist poaching",
        "complexity": {
            "total": 403,
            "loc": "90 hrs (Haeundae ground-floor location search)",
            "design": "33 hrs (Ground-floor styling stations layout)",
            "staff": "130 hrs (Local service culture coaching)",
            "logistics": "150 hrs (Korean organic cosmetic distribution)"
        },
        "coords": [
            35.1585,
            129.1625
        ],
        "url": "busan.html"
    },
    {
        "name": "Dubai",
        "region": "Middle East",
        "format": "Premium Boutique Salon (MVP)",
        "size": "800 sq ft",
        "capex": "USD 90k - 110k",
        "opex": "USD 16,600",
        "ticket": "USD 160",
        "cogs": "USD 16.00",
        "margin": "90%",
        "breakeven": "~115 customers",
        "daily_breakeven": "~3.8 customers/day",
        "tax": "9.0%",
        "pat_ratio": "222% (Post-Tax)",
        "payback": "3 Months",
        "underserved": "50%",
        "airport": "15 mins (DXB)",
        "risk": "Extreme hard water (TDS 500–1200 ppm) requires heavy filtration investment",
        "complexity": {
            "total": 405,
            "loc": "120 hrs (Mainland freezone setup)",
            "design": "45 hrs (Premium styling layout)",
            "staff": "140 hrs (Talent visa & high training)",
            "logistics": "100 hrs (Gulf customs clearance)"
        },
        "coords": [
            25.2048,
            55.2708
        ],
        "url": "dubai.html"
    }
];;

    // Volumes Database for all 27 cities based on actual Base Case customer metrics
    const volumesDb = {
    "bangkok": 529,
    "binhduong": 397,
    "brisbane": 397,
    "danang": 345,
    "dongnai": 345,
    "haiphong": 345,
    "hanoi": 397,
    "hcmc": 397,
    "hongkong": 397,
    "johor": 345,
    "kuala_lumpur": 457,
    "macau": 345,
    "melbourne": 457,
    "penang": 403,
    "sabah": 345,
    "sarawak": 345,
    "perth": 345,
    "singapore": 397,
    "sydney": 345,
    "kaohsiung": 397,
    "taichung": 345,
    "tainan": 397,
    "taipei": 397,
    "fukuoka": 345,
    "okinawa": 397,
    "busan": 397,
    "dubai": 397
};;

    // Parse baseline numerical values dynamically from string representations
    citiesDb.forEach(city => {
        const key = city.url.replace('.html', '');
        city.volume = volumesDb[key] || 300;
        
        // ticketVal
        if (city.ticket) {
            city.ticketVal = parseInt(city.ticket.replace(/[^0-9]/g, '')) || 0;
        } else {
            city.ticketVal = 0;
        }
        
        // opexVal
        if (city.opex) {
            city.opexVal = parseInt(city.opex.replace(/[^0-9]/g, '')) || 0;
        } else {
            city.opexVal = 0;
        }
        
        // capexVal
        if (city.capex) {
            const capexMatches = city.capex.match(/(\d+)k/g);
            if (capexMatches) {
                const nums = capexMatches.map(m => parseInt(m) * 1000);
                city.capexVal = nums.reduce((a, b) => a + b, 0) / nums.length;
            } else {
                city.capexVal = parseInt(city.capex.replace(/[^0-9]/g, '')) || 0;
            }
        } else {
            city.capexVal = 0;
        }
        
        // taxVal
        if (city.tax) {
            city.taxVal = (parseFloat(city.tax.replace(/[^0-9.]/g, '')) || 0) / 100;
        } else {
            city.taxVal = 0;
        }
    });

    // Helper functions to get model adjusted values
    function getModelFormat(baseFormat, model) {
        if (model === 'spa') return baseFormat;
        return baseFormat
            .replace("Boutique (MVP)", "Boutique Salon (MVP)")
            .replace("Boutique PoC", "Boutique Salon PoC")
            .replace("Luxury Suite PoC", "Luxury Salon Suite PoC")
            .replace("Boutique Salon / PoC", "Boutique Salon PoC")
            .replace("Luxury Suite", "Salon Suite")
            .replace("Ultra-Luxury Suite", "Premium Salon Suite")
            .replace("Micro-Spa", "Micro-Salon")
            .replace("Expat PoC", "Expat Salon PoC")
            .replace("Expat PoC / MVP", "Expat Salon PoC / MVP")
            .replace("Seaside Resort PoC / MVP", "Seaside Resort Salon PoC / MVP")
            .replace("Metro Port PoC / MVP", "Metro Port Salon PoC / MVP")
            .replace("Cross-Border PoC", "Cross-Border Salon PoC")
            .replace("Aesthetic Lane Spa", "Aesthetic Lane Salon")
            .replace("Hair Spa", "Hair Salon")
            .replace("Spa", "Salon");
    }

    function getModelCapex(baseCapex, model) {
        if (model === 'spa') return baseCapex;
        return baseCapex.replace(/(\d+)k/g, (match, p1) => {
            return Math.round(parseInt(p1) * 0.60) + "k";
        });
    }

    function getModelOpex(baseOpex, model) {
        if (model === 'spa') return baseOpex;
        return baseOpex.replace(/([0-9,]+)/g, (match, p1) => {
            const val = parseInt(p1.replace(/,/g, ''));
            return Math.round(val * 0.80).toLocaleString();
        });
    }

    function getModelTicket(baseTicket, model) {
        if (model === 'spa') return baseTicket;
        return baseTicket.replace(/([0-9,]+)/g, (match, p1) => {
            const val = parseInt(p1.replace(/,/g, ''));
            return Math.round(val * 0.65).toLocaleString();
        });
    }

    function getModelCogs(baseCogs, model, ticketVal) {
        if (model === 'spa') return baseCogs;
        const cogsVal = ticketVal * 0.10;
        return "USD " + cogsVal.toFixed(2);
    }

    function getModelComplexity(baseComplexity, model) {
        if (model === 'spa' || !baseComplexity) return baseComplexity;
        
        let designHrs = 0;
        const match = baseComplexity.design.match(/(\d+)\s*hrs/);
        if (match) {
            designHrs = parseInt(match[1]);
        }
        
        const designRed = Math.round(designHrs * 0.50);
        const newDesign = baseComplexity.design.replace(/(\d+)\s*hrs/, (match, p1) => {
            return (parseInt(p1) - designRed) + " hrs";
        });
        
        const newTotal = baseComplexity.total - designRed;
        
        return {
            total: newTotal,
            loc: baseComplexity.loc,
            design: newDesign.replace("VIP pods", "styling stations").replace("VIP suites", "styling suites").replace("VIP starlight", "lighting designs"),
            staff: baseComplexity.staff.replace("VIP", "Stylist"),
            logistics: baseComplexity.logistics.replace("OEM wash beds", "styling chairs")
        };
    }

    // ==========================================
    // DYNAMIC SIDEBAR SELECTOR & CITY LIST RENDER
    // ==========================================
    const sidebarCities = [
        { name: "Binh Duong", region: "Vietnam", url: "binhduong.html" },
        { name: "Da Nang", region: "Vietnam", url: "danang.html" },
        { name: "Dong Nai", region: "Vietnam", url: "dongnai.html" },
        { name: "Hai Phong", region: "Vietnam", url: "haiphong.html" },
        { name: "Hanoi", region: "Vietnam", url: "hanoi.html" },
        { name: "Ho Chi Minh", region: "Vietnam", url: "hcmc.html" },
        { name: "Johor Bahru", region: "Malaysia", url: "johor.html" },
        { name: "Kuala Lumpur", region: "Malaysia", url: "kuala_lumpur.html" },
        { name: "Penang", region: "Malaysia", url: "penang.html" },
        { name: "Sabah", region: "Malaysia", url: "sabah.html" },
        { name: "Sarawak", region: "Malaysia", url: "sarawak.html" },
        { name: "Kaohsiung", region: "Taiwan", url: "kaohsiung.html" },
        { name: "Taichung", region: "Taiwan", url: "taichung.html" },
        { name: "Tainan", region: "Taiwan", url: "tainan.html" },
        { name: "Taipei", region: "Taiwan", url: "taipei.html" },
        { name: "Brisbane", region: "Australia", url: "brisbane.html" },
        { name: "Melbourne", region: "Australia", url: "melbourne.html" },
        { name: "Perth", region: "Australia", url: "perth.html" },
        { name: "Sydney", region: "Australia", url: "sydney.html" },
        { name: "Fukuoka", region: "Japan", url: "fukuoka.html" },
        { name: "Okinawa", region: "Japan", url: "okinawa.html" },
        { name: "Busan", region: "South Korea", url: "busan.html" },
        { name: "Dubai", region: "Middle East", url: "dubai.html" },
        { name: "Bangkok", region: "Other APAC", url: "bangkok.html" },
        { name: "Hong Kong", region: "Other APAC", url: "hongkong.html" },
        { name: "Macau", region: "Other APAC", url: "macau.html" },
        { name: "Singapore", region: "Other APAC", url: "singapore.html" }
    ];

    function renderSidebar() {
        const citySelector = document.querySelector('.city-selector');
        if (!citySelector) return;

        const pathname = window.location.pathname;
        const currentPage = pathname.substring(pathname.lastIndexOf('/') + 1) || 'index.html';
        const activeCityEntry = sidebarCities.find(c => currentPage.includes(c.url));
        
        let initialRegion = "All";
        if (activeCityEntry) {
            initialRegion = activeCityEntry.region;
        }

        // Clean out existing selector HTML
        citySelector.innerHTML = '';

        // 1. Dashboard Direct Link
        const dashBtn = document.createElement('a');
        dashBtn.href = "index.html";
        dashBtn.className = "city-btn direct-link";
        dashBtn.id = "sidebar-dashboard-btn";
        dashBtn.textContent = "Dashboard";
        if (currentPage === 'index.html' || currentPage === '') {
            dashBtn.classList.add('active');
        }
        citySelector.appendChild(dashBtn);

        // 2. Custom Select Region Wrapper
        const selectWrapper = document.createElement('div');
        selectWrapper.className = "custom-select-wrapper";
        
        const selectTrigger = document.createElement('div');
        selectTrigger.className = "custom-select-trigger";
        
        const triggerLabel = document.createElement('span');
        triggerLabel.textContent = initialRegion === "All" ? "All Regions" : initialRegion;
        selectTrigger.appendChild(triggerLabel);
        
        const arrow = document.createElement('div');
        arrow.className = "arrow";
        selectTrigger.appendChild(arrow);
        
        selectWrapper.appendChild(selectTrigger);

        // Options List
        const optionsList = document.createElement('div');
        optionsList.className = "custom-options";

        const regions = ["All", "Vietnam", "Malaysia", "Taiwan", "Australia", "Japan", "South Korea", "Middle East", "Other APAC"];
        regions.forEach(reg => {
            const opt = document.createElement('span');
            opt.className = "custom-option";
            if (reg === initialRegion) opt.classList.add('selected');
            opt.setAttribute('data-value', reg);
            opt.textContent = reg === "All" ? "All Regions" : reg;
            optionsList.appendChild(opt);
        });
        selectWrapper.appendChild(optionsList);
        citySelector.appendChild(selectWrapper);

        // 3. City list container
        const cityListContainer = document.createElement('div');
        cityListContainer.className = "sidebar-city-list";
        citySelector.appendChild(cityListContainer);

        // Dropdown toggle events
        selectTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            selectWrapper.classList.toggle('open');
        });

        document.addEventListener('click', () => {
            selectWrapper.classList.remove('open');
        });

        // Option selections
        const options = optionsList.querySelectorAll('.custom-option');
        options.forEach(opt => {
            opt.addEventListener('click', (e) => {
                const val = opt.getAttribute('data-value');
                options.forEach(o => o.classList.remove('selected'));
                opt.classList.add('selected');
                triggerLabel.textContent = val === "All" ? "All Regions" : val;
                
                // Re-render filtered city list
                renderCityList(val);
                
                // Keep dropdown closed after click
                selectWrapper.classList.remove('open');
                
                // Re-apply current language translations
                translateDOM(citySelector);
            });
        });

        // Primary city list render function
        function renderCityList(selectedRegion) {
            cityListContainer.innerHTML = '';
            const filtered = selectedRegion === 'All' 
                ? sidebarCities 
                : sidebarCities.filter(c => c.region === selectedRegion);

            filtered.forEach(city => {
                const btn = document.createElement('a');
                btn.href = city.url;
                btn.className = "city-btn";
                btn.textContent = city.name;
                
                if (activeCityEntry && city.name === activeCityEntry.name) {
                    btn.classList.add('active');
                }
                cityListContainer.appendChild(btn);
            });
            
            // Immediately apply active language hash propagation on links
            const state = getActiveState();
            updateLinkHashes(state.lang);
        }

        // Render city list initial state
        renderCityList(initialRegion);
    }

    // ==========================================
    // PAGE UPDATERS & STATE SYNC
    // ==========================================
    let mapInstance = null;
    let mapMarkers = [];

    function updatePlatformComponents() {
        const state = getActiveState();
        const pathname = window.location.pathname;
        const currentPage = pathname.substring(pathname.lastIndexOf('/') + 1) || 'index.html';
        const isDashboard = currentPage === 'index.html' || currentPage === '';
        
        // 1. Update side bar link hashes
        updateLinkHashes(state.lang);

        if (isDashboard) {
            // Populate Dashboard Tables
            populateDashboardTables(state.model);
            // Re-render Map Markers
            renderMapMarkers(state.model);
        } else {
            // Update Subpage contents
            updateSubpageContent(currentPage, state.model);
        }
        
        // Apply Global Translations
        if (state.lang !== 'en') {
            translateDOM(document.body);
        }
    }

    // POPULATE DASHBOARD TABLES ON INDEX.HTML
    function populateDashboardTables(model) {
        const overviewTbody = document.getElementById('overview-table-body');
        const complexityTbody = document.getElementById('complexity-table-body');
        if (!overviewTbody || !complexityTbody) return;

        overviewTbody.innerHTML = '';
        complexityTbody.innerHTML = '';

        citiesDb.forEach(city => {
            const sizeStr = city.size;
            const capexStr = city.capex;
            const opexStr = city.opex;
            const ticketStr = city.ticket;
            
            // Values for math
            const ticketVal = city.ticketVal;
            const opexVal = city.opexVal;
            const capexVal = city.capexVal;
            const volumeBase = city.volume;
            const taxRate = city.taxVal;

            const cogsVal = ticketVal * 0.10;
            const contribMargin = ticketVal - cogsVal;
            const monthlyBreakeven = Math.round(opexVal / contribMargin);
            const dailyBreakeven = (monthlyBreakeven / 30).toFixed(1);

            const preTaxPAT = (volumeBase * contribMargin) - opexVal;
            const taxVal = preTaxPAT > 0 ? preTaxPAT * taxRate : 0;
            const pat = preTaxPAT - taxVal;
            const ratio = Math.round((pat / opexVal) * 100);
            const payback = pat > 0 ? Math.round(capexVal / pat) : 0;

            const paybackStr = payback > 0 ? `${payback} Months` : "N/A";
            const ratioStr = `${ratio}% (Post-Tax)`;
            const formatStr = city.format;
            const cogsStr = "USD " + cogsVal.toFixed(2);
            const breakevenStr = `~${monthlyBreakeven} customers`;
            const dailyBreakevenStr = `~${dailyBreakeven} customers/day`;

            // Row 1: Overview
            const trOverview = document.createElement('tr');
            trOverview.setAttribute('data-region', city.region);
            trOverview.setAttribute('data-city', city.name);
            
            trOverview.innerHTML = `
                <td><strong><a href="${city.url}" style="color: var(--accent); font-weight: 600; text-decoration: none; border-bottom: 1px dashed rgba(198,168,124,0.4);">${city.name}</a></strong></td>
                <td>${formatStr}</td>
                <td>${sizeStr}</td>
                <td>${capexStr}</td>
                <td>${opexStr}</td>
                <td>${ticketStr}</td>
                <td>${cogsStr}</td>
                <td>90%</td>
                <td>${breakevenStr}</td>
                <td>${dailyBreakevenStr}</td>
                <td>${(taxRate * 100).toFixed(1)}%</td>
                <td>${ratioStr}</td>
                <td>${paybackStr}</td>
                <td>${city.underserved}</td>
                <td>${city.airport}</td>
                <td>${city.risk}</td>
            `;
            overviewTbody.appendChild(trOverview);

            // Row 2: Complexity
            const comp = getModelComplexity(city.complexity, model);
            if (comp) {
                const trComp = document.createElement('tr');
                trComp.setAttribute('data-region', city.region);
                trComp.setAttribute('data-city', city.name);
                trComp.innerHTML = `
                    <td><strong><a href="${city.url}" style="color: var(--accent); font-weight: 600; text-decoration: none; border-bottom: 1px dashed rgba(198,168,124,0.4);">${city.name}</a> (${comp.total} hrs)</strong></td>
                    <td>${comp.loc}</td>
                    <td>${comp.design}</td>
                    <td>${comp.staff}</td>
                    <td>${comp.logistics}</td>
                `;
                complexityTbody.appendChild(trComp);
            }
        });
        
        // Reapply current search/tab filters
        if (typeof applyFilters === 'function') {
            applyFilters('overview');
            applyFilters('complexity');
        }
    }

    // MAP RENDERING LOGIC ON DASHBOARD
    function renderMapMarkers(model) {
        if (typeof L === 'undefined' || !document.getElementById('map')) return;

        // Create Leaflet map if not initialized
        if (!mapInstance) {
            mapInstance = L.map('map', {
                scrollWheelZoom: true,
            }).setView([15.0, 112.0], 4.5);

            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap &copy; CARTO',
                subdomains: 'abcd',
                maxZoom: 20
            }).addTo(mapInstance);
            
            // Auto-fit bounds initially
            const markerCoords = citiesDb.map(city => city.coords);
            if (markerCoords.length > 0) {
                mapInstance.fitBounds(markerCoords, { padding: [50, 50] });
            }
        }

        // Remove existing markers
        mapMarkers.forEach(m => mapInstance.removeLayer(m));
        mapMarkers = [];

        // Helper calculations
        const getColor = (payback) => {
            if (payback <= 6) return "#10b981"; // Emerald green (5-6 months)
            if (payback <= 8) return "#eab308"; // Amber yellow (7-8 months)
            if (payback <= 10) return "#f97316"; // Orange (9-10 months)
            return "#ef4444"; // Red (11-12 months)
        };

        const getOpacity = (capex) => {
            const minCapex = 30000;
            const maxCapex = 180000;
            const minOpacity = 0.25;
            const maxOpacity = 0.95;
            if (capex <= minCapex) return maxOpacity;
            if (capex >= maxCapex) return minOpacity;
            return maxOpacity - ((capex - minCapex) / (maxCapex - minCapex)) * (maxOpacity - minOpacity);
        };

        const getRadius = (underservedStr) => {
            const pct = parseInt(underservedStr) || 0;
            const minPct = 20;
            const maxPct = 70;
            const minRad = 6;
            const maxRad = 16;
            if (pct <= minPct) return minRad;
            if (pct >= maxPct) return maxRad;
            return minRad + ((pct - minPct) / (maxPct - minPct)) * (maxRad - minRad);
        };

        // Render markers
        citiesDb.forEach(city => {
            const ticketVal = city.ticketVal;
            const opexVal = city.opexVal;
            const capexVal = city.capexVal;
            const volumeBase = city.volume;
            const taxRate = city.taxVal;

            const cogsVal = ticketVal * 0.10;
            const contribMargin = ticketVal - cogsVal;
            const monthlyBreakeven = Math.round(opexVal / contribMargin);

            const preTaxPAT = (volumeBase * contribMargin) - opexVal;
            const taxVal = preTaxPAT > 0 ? preTaxPAT * taxRate : 0;
            const pat = preTaxPAT - taxVal;
            const ratio = Math.round((pat / opexVal) * 100);
            const payback = pat > 0 ? Math.round(capexVal / pat) : 0;

            const color = getColor(payback);
            const opacity = getOpacity(capexVal);
            const radius = getRadius(city.underserved);

            const formatStr = city.format;
            const capexStr = city.capex;
            const opexStr = city.opex;
            const paybackStr = payback > 0 ? `${payback} Months` : "N/A";
            const ratioStr = `${ratio}% (Post-Tax)`;

            const customIcon = L.divIcon({
                html: `<div class="dynamic-marker" style="--marker-color: ${color}; width: ${radius * 2}px; height: ${radius * 2}px; background: ${color}; opacity: ${opacity};"></div>`,
                className: 'custom-leaflet-icon',
                iconSize: [radius * 2, radius * 2],
                iconAnchor: [radius, radius]
            });

            const popupContent = `
                <div class="popup-content">
                    <h3>${city.name}</h3>
                    <p>Format: <strong>${formatStr}</strong></p>
                    <p>Initial CAPEX: <strong>${capexStr}</strong></p>
                    <p>Monthly OPEX: <strong>${opexStr}</strong></p>
                    <p>Post-Tax Payback: <strong>${paybackStr}</strong></p>
                    <p>Post-Tax Profit/OPEX: <strong>${ratioStr}</strong></p>
                    <p>Underserved Gap: <strong>${city.underserved}</strong></p>
                    <p>Nearest Airport: <strong>${city.airport}</strong></p>
                    <a href="${city.url}" class="popup-btn">View Detailed Study</a>
                </div>
            `;
            
            const marker = L.marker(city.coords, { icon: customIcon }).addTo(mapInstance).bindPopup(popupContent);
            mapMarkers.push(marker);
        });
    }

    // UPDATE DYNAMIC SUBPAGE CONTENT ON LOAD
    function updateSubpageContent(url, model) {
        const city = citiesDb.find(c => url.includes(c.url));
        if (!city) return;

        // Parameters
        const ticketVal = city.ticketVal;
        const opexVal = city.opexVal;
        const capexVal = city.capexVal;
        const volumeBase = city.volume;
        const taxRate = city.taxVal;

        const cogsVal = ticketVal * 0.10;
        const contribMargin = ticketVal - cogsVal;
        const monthlyBreakeven = Math.round(opexVal / contribMargin);
        const dailyBreakeven = Math.round(monthlyBreakeven / 30);

        const formatStr = city.format;
        const capexStr = city.capex;
        const opexStr = city.opex;
        const ticketStr = city.ticket;

        // 1. Update Hero Subtitle Model Info
        const subtitleEl = document.querySelector('.hero .subtitle');
        if (subtitleEl) {
            subtitleEl.textContent = subtitleEl.textContent.replace("Feasibility Study", model === 'spa' ? "Feasibility Study" : "Standard Salon Feasibility");
        }
        
        const heroMetaEl = document.querySelector('.hero .hero-meta');
        if (heroMetaEl) {
            const spans = Array.from(heroMetaEl.querySelectorAll('span'));
            spans.forEach(s => {
                if (s.textContent.includes("Model:")) {
                    s.innerHTML = `Model: ${formatStr}`;
                }
            });
        }

        // 2. Update Stats Boxes (Grid Stats)
        const statsGrid = document.querySelector('.grid-stats');
        if (statsGrid) {
            const boxes = Array.from(statsGrid.querySelectorAll('.stat-box'));
            boxes.forEach(box => {
                const label = box.querySelector('.label').textContent.trim();
                const valueEl = box.querySelector('.value');
                if (label.includes("Initial CAPEX")) {
                    valueEl.textContent = capexStr;
                } else if (label.includes("Monthly OPEX")) {
                    valueEl.textContent = opexStr;
                } else if (label.includes("Average Ticket")) {
                    valueEl.textContent = ticketStr;
                } else if (label.includes("Breakeven Volume")) {
                    valueEl.textContent = `${dailyBreakeven} Customers / Day`;
                }
            });
        }

        // 3. Update OPEX and CAPEX tables
        scaleOPEXTable(1.0);
        scaleCAPEXTable(1.0);

        // 4. Update Unit Economics Scenario Table
        updateEconomicsTable(ticketVal, opexVal, volumeBase, taxRate, capexVal);

        // 5. Update Timeline duration Weeks
        updateTimelineTable(model);

        // 6. Update Recommendation Box Setup beds description
        const recBox = document.querySelector('#recommendation .conclusion-box');
        if (recBox) {
            const recTitle = recBox.querySelector('h3');
            if (recTitle) {
                recTitle.textContent = model === 'spa' ? "Decision: GO (Industrial Corridor PoC)" : "Decision: GO (Standard Salon PoC)";
            }
            const items = recBox.querySelectorAll('ul li');
            items.forEach(li => {
                if (li.textContent.includes("Setup:")) {
                    li.textContent = model === 'spa' ? "Setup: 4 VIP Beds (OEM), 800 sq ft" : "Setup: 4 Styling Chairs, 800 sq ft";
                } else if (li.textContent.includes("Budget Ceiling:")) {
                    li.textContent = `Budget Ceiling: ${capexStr}`;
                }
            });
        }
    }

    // Helper functions for table scaling in subpages
    function scaleOPEXTable(factor) {
        const opexTable = document.querySelector('#opex table');
        if (!opexTable) return;
        const rows = Array.from(opexTable.querySelectorAll('tbody tr'));
        let items = [];
        let total = 0;
        rows.forEach((row) => {
            if (row.classList.contains('total-row')) return;
            const costCell = row.cells[1];
            if (costCell) {
                const text = costCell.textContent.trim();
                const val = parseInt(text.replace(/[^0-9]/g, ''));
                if (!isNaN(val)) {
                    const newVal = Math.round(val * factor);
                    costCell.textContent = `$${newVal.toLocaleString()}`;
                    total += newVal;
                    items.push({ row, val: newVal });
                }
            }
        });
        
        const totalRow = opexTable.querySelector('.total-row');
        if (totalRow) {
            const totalCell = totalRow.cells[1];
            if (totalCell) {
                totalCell.innerHTML = `<strong>$${total.toLocaleString()}</strong>`;
            }
        }
        
        items.forEach(item => {
            const pctCell = item.row.cells[2];
            if (pctCell) {
                const pct = total > 0 ? Math.round((item.val / total) * 100) : 0;
                pctCell.textContent = `${pct}%`;
            }
        });
    }

    function scaleCAPEXTable(factor) {
        const capexTable = document.querySelector('#capex table');
        if (!capexTable) return;
        const rows = Array.from(capexTable.querySelectorAll('tbody tr'));
        let total = 0;
        rows.forEach((row) => {
            if (row.classList.contains('total-row')) return;
            const costCell = row.cells[1];
            if (costCell) {
                const text = costCell.textContent.trim();
                const val = parseInt(text.replace(/[^0-9]/g, ''));
                if (!isNaN(val)) {
                    const newVal = Math.round(val * factor);
                    costCell.textContent = `$${newVal.toLocaleString()}`;
                    total += newVal;
                }
            }
        });
        
        const totalRow = capexTable.querySelector('.total-row');
        if (totalRow) {
            const totalCell = totalRow.cells[1];
            if (totalCell) {
                totalCell.innerHTML = `<strong>$${total.toLocaleString()}</strong>`;
            }
        }
    }

    function updateEconomicsTable(ticket, opex, baseVol, taxRate, capexMid) {
        const econTable = document.querySelector('#economics table');
        if (!econTable) return;
        const rows = Array.from(econTable.querySelectorAll('tbody tr'));
        
        const cogs = ticket * 0.10;
        const contribMargin = ticket - cogs;
        
        const scenarios = [
            { name: "Breakeven Case", vol: Math.round(opex / contribMargin) },
            { name: "Base Case", vol: Math.round(baseVol) },
            { name: "High-Performance Case", vol: Math.round(baseVol * 1.25) }
        ];
        
        scenarios.forEach((scen, idx) => {
            const row = rows[idx];
            if (!row) return;
            
            const rev = scen.vol * ticket;
            const cogVal = scen.vol * cogs;
            const netProfit = rev - cogVal - opex;
            
            if (row.cells[1]) row.cells[1].textContent = `${scen.vol.toLocaleString()} customers`;
            if (row.cells[2]) row.cells[2].textContent = `$${Math.round(rev).toLocaleString()}`;
            if (row.cells[3]) row.cells[3].textContent = `$${Math.round(cogVal).toLocaleString()}`;
            if (row.cells[4]) row.cells[4].textContent = `$${Math.round(opex).toLocaleString()}`;
            if (row.cells[5]) row.cells[5].textContent = `$${Math.round(netProfit).toLocaleString()}`;
        });
        
        const conclusionBox = document.querySelector('#economics .conclusion-box');
        if (conclusionBox) {
            const preTaxPAT = (baseVol * contribMargin) - opex;
            const taxVal = preTaxPAT > 0 ? preTaxPAT * taxRate : 0;
            const pat = preTaxPAT - taxVal;
            const ratio = Math.round((pat / opex) * 100);
            const payback = pat > 0 ? (capexMid / pat).toFixed(1) : "N/A";
            
            const lang = getActiveState().lang;
            const isJa = lang === 'ja';
            const isVi = lang === 'vi';
            
            let html = '';
            if (isJa) {
                html = `
                    <h3 style="color: var(--success); font-size: 1.2rem; margin-bottom: 0.5rem; font-family: var(--font-heading);">税後財務フィジビリティ分析</h3>
                    <p>上記テーブル内の数値はすべて税引前の値です。各都市の法人税率 <strong>${(taxRate * 100).toFixed(1)}%</strong> を反映した、基本シナリオの税後シミュレーションは以下の通りです:</p>
                    <ul style="margin-top: 0.5rem; margin-left: 1.5rem; list-style-type: disc;">
                        <li><strong>基本シナリオ 税引前月間純利益:</strong> USD ${Math.round(preTaxPAT).toLocaleString()}</li>
                        <li><strong>推定月間法人税額:</strong> USD ${Math.round(taxVal).toLocaleString()}</li>
                        <li><strong>税引後月間純利益 (PAT):</strong> USD ${Math.round(pat).toLocaleString()}</li>
                        <li><strong>税引後利益/運営費比率:</strong> <strong>${ratio}% (税後)</strong></li>
                        <li><strong>税引後投資回収期間:</strong> <strong>${payback}ヶ月</strong></li>
                    </ul>
                `;
            } else if (isVi) {
                html = `
                    <h3 style="color: var(--success); font-size: 1.2rem; margin-bottom: 0.5rem; font-family: var(--font-heading);">Phân tích tính khả thi tài chính sau thuế</h3>
                    <p>Tất cả các tính toán trong bảng trên đại diện cho hiệu suất trước thuế. Tính thêm thuế suất TNDN <strong>${(taxRate * 100).toFixed(1)}%</strong> chúng ta có các dự báo sau thuế cho kịch bản cơ sở như sau:</p>
                    <ul style="margin-top: 0.5rem; margin-left: 1.5rem; list-style-type: disc;">
                        <li><strong>Lợi nhuận thuần trước thuế (Kịch bản cơ sở):</strong> USD ${Math.round(preTaxPAT).toLocaleString()}</li>
                        <li><strong>Thuế thu nhập doanh nghiệp ước tính:</strong> USD ${Math.round(taxVal).toLocaleString()}</li>
                        <li><strong>Lợi nhuận thuần sau thuế hàng tháng (PAT):</strong> USD ${Math.round(pat).toLocaleString()}</li>
                        <li><strong>Tỷ lệ lợi nhuận sau thuế / OPEX:</strong> <strong>${ratio}% (sau thuế)</strong></li>
                        <li><strong>Thời gian hoàn vốn sau thuế:</strong> <strong>${payback} tháng</strong></li>
                    </ul>
                `;
            } else {
                html = `
                    <h3 style="color: var(--success); font-size: 1.2rem; margin-bottom: 0.5rem; font-family: var(--font-heading);">Post-Tax Financial Feasibility Analysis</h3>
                    <p>All calculations in the table above represent pre-tax performance. Factoring in the local Corporate Income Tax (CIT) rate of <strong>${(taxRate * 100).toFixed(1)}%</strong>, we arrive at the following post-tax projections for the Base Case:</p>
                    <ul style="margin-top: 0.5rem; margin-left: 1.5rem; list-style-type: disc;">
                        <li><strong>Base Case Pre-Tax Monthly Net Profit:</strong> USD ${Math.round(preTaxPAT).toLocaleString()}</li>
                        <li><strong>Estimated Monthly Corporate Income Tax:</strong> USD ${Math.round(taxVal).toLocaleString()}</li>
                        <li><strong>Post-Tax Net Monthly Profit (PAT):</strong> USD ${Math.round(pat).toLocaleString()}</li>
                        <li><strong>Post-Tax Profit to OPEX Ratio:</strong> <strong>${ratio}% (Post-Tax)</strong></li>
                        <li><strong>Post-Tax CAPEX Payback Period:</strong> <strong>${payback} Months</strong></li>
                    </ul>
                `;
            }
            conclusionBox.innerHTML = html;
        }
    }

    function updateTimelineTable(model) {
        const timelineTable = document.querySelector('#timeline table');
        if (!timelineTable) return;
        const rows = timelineTable.querySelectorAll('tbody tr');
        if (rows.length < 4) return;
        
        if (model === 'salon') {
            rows[1].cells[1].textContent = "Weeks 5 - 7";
            rows[1].cells[2].textContent = rows[1].cells[2].textContent.replace("OEM wash beds installed", "standard styling stations installed");
            
            rows[2].cells[1].textContent = "Weeks 8 - 9";
            rows[2].cells[2].textContent = rows[2].cells[2].textContent.replace("Omotenashi service coaching", "standard styling service coaching");
            
            rows[3].cells[1].textContent = "Week 10+";
        } else {
            rows[1].cells[1].textContent = "Weeks 5 - 9";
            rows[1].cells[2].textContent = rows[1].cells[2].textContent.replace("standard styling stations installed", "OEM wash beds installed");
            
            rows[2].cells[1].textContent = "Weeks 10 - 11";
            rows[2].cells[2].textContent = rows[2].cells[2].textContent.replace("standard styling service coaching", "Omotenashi service coaching");
            
            rows[3].cells[1].textContent = "Week 12+";
        }
    }

    function initMobileNav() {
        // Create mobile header bar if not exists
        let mobileHeader = document.querySelector('.mobile-header');
        if (!mobileHeader) {
            mobileHeader = document.createElement('div');
            mobileHeader.className = 'mobile-header';
            
            const hmbBtn = document.createElement('button');
            hmbBtn.className = 'hamburger-btn';
            hmbBtn.setAttribute('aria-label', 'Toggle Navigation');
            hmbBtn.innerHTML = `
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            `;
            
            const logo = document.createElement('div');
            logo.className = 'mobile-logo';
            logo.textContent = 'Oasis Salon';
            
            mobileHeader.appendChild(hmbBtn);
            mobileHeader.appendChild(logo);
            
            document.body.prepend(mobileHeader);
            
            // Toggle event
            hmbBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                document.body.classList.toggle('sidebar-open');
            });
        }
        
        // Create overlay backdrop if not exists
        let overlay = document.querySelector('.sidebar-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'sidebar-overlay';
            document.body.appendChild(overlay);
            
            // Close event
            overlay.addEventListener('click', () => {
                document.body.classList.remove('sidebar-open');
            });
        }
        
        // Auto-close sidebar on link navigation inside sidebar using event delegation
        document.addEventListener('click', (e) => {
            const link = e.target.closest('.sidebar a');
            if (link) {
                document.body.classList.remove('sidebar-open');
            }
        });
        
        // Close sidebar on window resize to desktop sizes
        window.addEventListener('resize', () => {
            if (window.innerWidth > 1024) {
                document.body.classList.remove('sidebar-open');
            }
        });
    }
    function handleScrollAnchor() {
        const hash = window.location.hash;
        if (hash) {
            const cleanHash = hash.substring(1);
            const parts = cleanHash.split('-');
            
            // The anchor is the last part if it is not a language or model code
            const lastPart = parts[parts.length - 1];
            const stateCodes = ['ja', 'vi', 'en', 'spa', 'salon'];
            if (lastPart && !stateCodes.includes(lastPart)) {
                const targetEl = document.getElementById(lastPart);
                if (targetEl) {
                    setTimeout(() => {
                        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 400);
                }
            }
        }
    }

    // ==========================================
    // INITIALIZATION CODE
    // ==========================================
    // Initialize mobile nav layout
    initMobileNav();

    // Execute sidebar generation
    renderSidebar();

    // Execute Global Page updates (Calculations, maps, table structures)
    updatePlatformComponents();

    // Scroll to the active section if an anchor is present in URL hash
    handleScrollAnchor();

    // Monitor hashchange events for browser history navigation
    let currentActiveState = getActiveState();
    window.addEventListener('hashchange', () => {
        const newState = getActiveState();
        if (newState.lang !== currentActiveState.lang || newState.model !== currentActiveState.model) {
            window.location.reload();
        }
    });

    // Auto-update Leaflet global instance if available on subpages
    if (typeof L !== 'undefined' && L.Map) {
        L.Map.addInitHook(function() {
            this.on('popupopen', function(e) {
                if (getActiveState().lang !== 'en') {
                    const popupNode = e.popup.getElement();
                    if (popupNode) {
                        translateDOM(popupNode);
                    }
                }
            });
        });
    }

    // Configure language switcher buttons
    const langBtns = document.querySelectorAll('.lang-btn');
    langBtns.forEach(btn => {
        const btnLang = btn.getAttribute('data-lang');
        const state = getActiveState();
        
        if (btnLang === state.lang) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }

        btn.addEventListener('click', (e) => {
            e.preventDefault();
            try {
                localStorage.setItem('selectedLanguage', btnLang);
            } catch (err) {}
            
            const currentBaseUrl = window.location.href.split('#')[0];
            
            const hashParts = [];
            if (btnLang !== 'en') hashParts.push(btnLang);
            
            const currentHash = window.location.hash.substring(1);
            let anchor = '';
            if (currentHash) {
                const parts = currentHash.split('-');
                const stateCodes = ['ja', 'vi', 'en', 'spa', 'salon'];
                anchor = parts.filter(p => !stateCodes.includes(p)).join('-');
            }
            if (anchor) hashParts.push(anchor);
            
            window.location.href = `${currentBaseUrl}#${hashParts.join('-')}`;
            window.location.reload();
        });
    });

    // ==========================================
    // INTERSECTION OBSERVER ANIMATIONS
    // ==========================================
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(el => observer.observe(el));

    // ==========================================
    // SIDEBAR NAVIGATION SCROLL HIGHLIGHTING
    // ==========================================
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-links a');

    window.addEventListener('scroll', () => {
        let current = '';
        const scrollY = window.pageYOffset;

        sections.forEach(section => {
            const sectionHeight = section.offsetHeight;
            const sectionTop = section.offsetTop - 100;
            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current) && current !== '') {
                link.classList.add('active');
            }
        });
    });

    // ==========================================
    // HERO ANIMATION DELAY
    // ==========================================
    setTimeout(() => {
        const hero = document.querySelector('.hero');
        if(hero) {
            hero.style.transform = 'translateY(0)';
            hero.style.opacity = '1';
        }
    }, 100);
});

// Expose filter functions globally so onclick events can trigger them
window.filterTable = function(region, type) {
    const tableId = type === 'overview' ? 'overview-table' : 'complexity';
    const buttons = document.querySelectorAll(`#${tableId} .tab-btn`);
    buttons.forEach(btn => {
        if (btn.dataset.region === region) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Apply filters
    applyFilters(type);
};

window.filterTableBySearch = function(type) {
    applyFilters(type);
};

function applyFilters(type) {
    const tableId = type === 'overview' ? 'overview-table' : 'complexity';
    const activeTab = document.querySelector(`#${tableId} .tab-btn.active`).dataset.region;
    const query = document.querySelector(`#${tableId} .search-input`).value.toLowerCase();
    
    const rows = document.querySelectorAll(`#${tableId} table tbody tr`);
    rows.forEach(row => {
        const region = row.dataset.region;
        const city = row.dataset.city.toLowerCase();
        
        const matchTab = (activeTab === 'All' || region === activeTab);
        const matchQuery = city.includes(query);
        
        if (matchTab && matchQuery) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}
