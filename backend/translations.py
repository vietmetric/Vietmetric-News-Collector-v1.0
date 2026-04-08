"""
Bảng dịch từ khóa đa ngôn ngữ (7 ngôn ngữ).
Dùng để mở rộng từ khóa tìm kiếm sang các ngôn ngữ: en, fr, ja, ko, es, zh, ru.
Bao gồm: thuật ngữ an ninh, quốc phòng, địa chính trị, tổ chức quốc tế, quốc gia, vùng lãnh thổ.
"""

# Cấu trúc: key (English lowercase) → {lang_code: translation}
# Mỗi entry có thể có nhiều biến thể (list) hoặc 1 giá trị (str)

MULTILANG_DICT = {
    # ═══════════════════════════════════════════════════════════
    # QUỐC GIA & VÙNG LÃNH THỔ
    # ═══════════════════════════════════════════════════════════
    "vietnam": {
        "en": "Vietnam", "fr": "Vietnam", "ja": "ベトナム", "ko": "베트남",
        "es": "Vietnam", "zh": "越南", "ru": "Вьетнам", "vi": "Việt Nam"
    },
    "china": {
        "en": "China", "fr": "Chine", "ja": "中国", "ko": "중국",
        "es": "China", "zh": "中国", "ru": "Китай", "vi": "Trung Quốc"
    },
    "japan": {
        "en": "Japan", "fr": "Japon", "ja": "日本", "ko": "일본",
        "es": "Japón", "zh": "日本", "ru": "Япония", "vi": "Nhật Bản"
    },
    "south korea": {
        "en": "South Korea", "fr": "Corée du Sud", "ja": "韓国", "ko": "한국",
        "es": "Corea del Sur", "zh": "韩国", "ru": "Южная Корея", "vi": "Hàn Quốc"
    },
    "north korea": {
        "en": "North Korea", "fr": "Corée du Nord", "ja": "北朝鮮", "ko": "북한",
        "es": "Corea del Norte", "zh": "朝鲜", "ru": "Северная Корея", "vi": "Triều Tiên"
    },
    "russia": {
        "en": "Russia", "fr": "Russie", "ja": "ロシア", "ko": "러시아",
        "es": "Rusia", "zh": "俄罗斯", "ru": "Россия", "vi": "Nga"
    },
    "united states": {
        "en": "United States", "fr": "États-Unis", "ja": "アメリカ", "ko": "미국",
        "es": "Estados Unidos", "zh": "美国", "ru": "США", "vi": "Hoa Kỳ"
    },
    "usa": {
        "en": "USA", "fr": "États-Unis", "ja": "米国", "ko": "미국",
        "es": "EE.UU.", "zh": "美国", "ru": "США", "vi": "Mỹ"
    },
    "taiwan": {
        "en": "Taiwan", "fr": "Taïwan", "ja": "台湾", "ko": "대만",
        "es": "Taiwán", "zh": "台湾", "ru": "Тайвань", "vi": "Đài Loan"
    },
    "philippines": {
        "en": "Philippines", "fr": "Philippines", "ja": "フィリピン", "ko": "필리핀",
        "es": "Filipinas", "zh": "菲律宾", "ru": "Филиппины", "vi": "Philippines"
    },
    "india": {
        "en": "India", "fr": "Inde", "ja": "インド", "ko": "인도",
        "es": "India", "zh": "印度", "ru": "Индия", "vi": "Ấn Độ"
    },
    "indonesia": {
        "en": "Indonesia", "fr": "Indonésie", "ja": "インドネシア", "ko": "인도네시아",
        "es": "Indonesia", "zh": "印度尼西亚", "ru": "Индонезия", "vi": "Indonesia"
    },
    "thailand": {
        "en": "Thailand", "fr": "Thaïlande", "ja": "タイ", "ko": "태국",
        "es": "Tailandia", "zh": "泰国", "ru": "Таиланд", "vi": "Thái Lan"
    },
    "malaysia": {
        "en": "Malaysia", "fr": "Malaisie", "ja": "マレーシア", "ko": "말레이시아",
        "es": "Malasia", "zh": "马来西亚", "ru": "Малайзия", "vi": "Malaysia"
    },
    "cambodia": {
        "en": "Cambodia", "fr": "Cambodge", "ja": "カンボジア", "ko": "캄보디아",
        "es": "Camboya", "zh": "柬埔寨", "ru": "Камбоджа", "vi": "Campuchia"
    },
    "laos": {
        "en": "Laos", "fr": "Laos", "ja": "ラオス", "ko": "라오스",
        "es": "Laos", "zh": "老挝", "ru": "Лаос", "vi": "Lào"
    },
    "myanmar": {
        "en": "Myanmar", "fr": "Myanmar", "ja": "ミャンマー", "ko": "미얀마",
        "es": "Myanmar", "zh": "缅甸", "ru": "Мьянма", "vi": "Myanmar"
    },
    "ukraine": {
        "en": "Ukraine", "fr": "Ukraine", "ja": "ウクライナ", "ko": "우크라이나",
        "es": "Ucrania", "zh": "乌克兰", "ru": "Украина", "vi": "Ukraine"
    },
    "iran": {
        "en": "Iran", "fr": "Iran", "ja": "イラン", "ko": "이란",
        "es": "Irán", "zh": "伊朗", "ru": "Иран", "vi": "Iran"
    },
    "israel": {
        "en": "Israel", "fr": "Israël", "ja": "イスラエル", "ko": "이스라엘",
        "es": "Israel", "zh": "以色列", "ru": "Израиль", "vi": "Israel"
    },
    "palestine": {
        "en": "Palestine", "fr": "Palestine", "ja": "パレスチナ", "ko": "팔레스타인",
        "es": "Palestina", "zh": "巴勒斯坦", "ru": "Палестина", "vi": "Palestine"
    },
    "australia": {
        "en": "Australia", "fr": "Australie", "ja": "オーストラリア", "ko": "호주",
        "es": "Australia", "zh": "澳大利亚", "ru": "Австралия", "vi": "Australia"
    },
    "germany": {
        "en": "Germany", "fr": "Allemagne", "ja": "ドイツ", "ko": "독일",
        "es": "Alemania", "zh": "德国", "ru": "Германия", "vi": "Đức"
    },
    "france": {
        "en": "France", "fr": "France", "ja": "フランス", "ko": "프랑스",
        "es": "Francia", "zh": "法国", "ru": "Франция", "vi": "Pháp"
    },
    "united kingdom": {
        "en": "United Kingdom", "fr": "Royaume-Uni", "ja": "イギリス", "ko": "영국",
        "es": "Reino Unido", "zh": "英国", "ru": "Великобритания", "vi": "Anh"
    },

    # ═══════════════════════════════════════════════════════════
    # VÙNG BIỂN & ĐỊA LÝ
    # ═══════════════════════════════════════════════════════════
    "south china sea": {
        "en": "South China Sea", "fr": "mer de Chine méridionale", "ja": "南シナ海",
        "ko": "남중국해", "es": "mar de China Meridional", "zh": "南海",
        "ru": "Южно-Китайское море", "vi": "Biển Đông"
    },
    "east china sea": {
        "en": "East China Sea", "fr": "mer de Chine orientale", "ja": "東シナ海",
        "ko": "동중국해", "es": "mar de China Oriental", "zh": "东海",
        "ru": "Восточно-Китайское море", "vi": "Biển Hoa Đông"
    },
    "taiwan strait": {
        "en": "Taiwan Strait", "fr": "détroit de Taïwan", "ja": "台湾海峡",
        "ko": "대만 해협", "es": "estrecho de Taiwán", "zh": "台湾海峡",
        "ru": "Тайваньский пролив", "vi": "Eo biển Đài Loan"
    },
    "mekong": {
        "en": "Mekong", "fr": "Mékong", "ja": "メコン", "ko": "메콩",
        "es": "Mekong", "zh": "湄公河", "ru": "Меконг", "vi": "Mê Kông"
    },
    "indo-pacific": {
        "en": "Indo-Pacific", "fr": "Indo-Pacifique", "ja": "インド太平洋",
        "ko": "인도태평양", "es": "Indo-Pacífico", "zh": "印太",
        "ru": "Индо-Тихоокеанский", "vi": "Ấn Độ Dương - Thái Bình Dương"
    },
    "southeast asia": {
        "en": "Southeast Asia", "fr": "Asie du Sud-Est", "ja": "東南アジア",
        "ko": "동남아시아", "es": "Sudeste Asiático", "zh": "东南亚",
        "ru": "Юго-Восточная Азия", "vi": "Đông Nam Á"
    },
    "asia pacific": {
        "en": "Asia Pacific", "fr": "Asie-Pacifique", "ja": "アジア太平洋",
        "ko": "아시아태평양", "es": "Asia-Pacífico", "zh": "亚太",
        "ru": "Азиатско-Тихоокеанский", "vi": "châu Á - Thái Bình Dương"
    },
    "middle east": {
        "en": "Middle East", "fr": "Moyen-Orient", "ja": "中東", "ko": "중동",
        "es": "Medio Oriente", "zh": "中东", "ru": "Ближний Восток", "vi": "Trung Đông"
    },

    # ═══════════════════════════════════════════════════════════
    # TỔ CHỨC QUỐC TẾ
    # ═══════════════════════════════════════════════════════════
    "asean": {
        "en": "ASEAN", "fr": "ASEAN", "ja": "ASEAN", "ko": "ASEAN",
        "es": "ASEAN", "zh": "东盟", "ru": "АСЕАН", "vi": "ASEAN"
    },
    "nato": {
        "en": "NATO", "fr": "OTAN", "ja": "NATO", "ko": "NATO",
        "es": "OTAN", "zh": "北约", "ru": "НАТО", "vi": "NATO"
    },
    "united nations": {
        "en": "United Nations", "fr": "Nations Unies", "ja": "国連",
        "ko": "유엔", "es": "Naciones Unidas", "zh": "联合国",
        "ru": "ООН", "vi": "Liên Hợp Quốc"
    },
    "european union": {
        "en": "European Union", "fr": "Union européenne", "ja": "EU",
        "ko": "유럽연합", "es": "Unión Europea", "zh": "欧盟",
        "ru": "Европейский Союз", "vi": "Liên minh châu Âu"
    },
    "aukus": {
        "en": "AUKUS", "fr": "AUKUS", "ja": "AUKUS", "ko": "AUKUS",
        "es": "AUKUS", "zh": "奥库斯", "ru": "АУКУС", "vi": "AUKUS"
    },
    "quad": {
        "en": "Quad", "fr": "Quad", "ja": "クアッド", "ko": "쿼드",
        "es": "Quad", "zh": "四方安全对话", "ru": "КВАД", "vi": "Quad"
    },
    "g7": {
        "en": "G7", "fr": "G7", "ja": "G7", "ko": "G7",
        "es": "G7", "zh": "七国集团", "ru": "G7", "vi": "G7"
    },
    "brics": {
        "en": "BRICS", "fr": "BRICS", "ja": "BRICS", "ko": "브릭스",
        "es": "BRICS", "zh": "金砖国家", "ru": "БРИКС", "vi": "BRICS"
    },

    # ═══════════════════════════════════════════════════════════
    # AN NINH & QUỐC PHÒNG
    # ═══════════════════════════════════════════════════════════
    "military": {
        "en": "military", "fr": "militaire", "ja": "軍事", "ko": "군사",
        "es": "militar", "zh": "军事", "ru": "военный", "vi": "quân sự"
    },
    "defense": {
        "en": "defense", "fr": "défense", "ja": "防衛", "ko": "국방",
        "es": "defensa", "zh": "国防", "ru": "оборона", "vi": "quốc phòng"
    },
    "war": {
        "en": "war", "fr": "guerre", "ja": "戦争", "ko": "전쟁",
        "es": "guerra", "zh": "战争", "ru": "война", "vi": "chiến tranh"
    },
    "conflict": {
        "en": "conflict", "fr": "conflit", "ja": "紛争", "ko": "분쟁",
        "es": "conflicto", "zh": "冲突", "ru": "конфликт", "vi": "xung đột"
    },
    "nuclear": {
        "en": "nuclear", "fr": "nucléaire", "ja": "核", "ko": "핵",
        "es": "nuclear", "zh": "核", "ru": "ядерный", "vi": "hạt nhân"
    },
    "missile": {
        "en": "missile", "fr": "missile", "ja": "ミサイル", "ko": "미사일",
        "es": "misil", "zh": "导弹", "ru": "ракета", "vi": "tên lửa"
    },
    "submarine": {
        "en": "submarine", "fr": "sous-marin", "ja": "潜水艦", "ko": "잠수함",
        "es": "submarino", "zh": "潜艇", "ru": "подводная лодка", "vi": "tàu ngầm"
    },
    "navy": {
        "en": "navy", "fr": "marine", "ja": "海軍", "ko": "해군",
        "es": "armada", "zh": "海军", "ru": "флот", "vi": "hải quân"
    },
    "air force": {
        "en": "air force", "fr": "armée de l'air", "ja": "空軍", "ko": "공군",
        "es": "fuerza aérea", "zh": "空军", "ru": "ВВС", "vi": "không quân"
    },
    "army": {
        "en": "army", "fr": "armée", "ja": "陸軍", "ko": "육군",
        "es": "ejército", "zh": "陆军", "ru": "армия", "vi": "lục quân"
    },
    "cybersecurity": {
        "en": "cybersecurity", "fr": "cybersécurité", "ja": "サイバーセキュリティ",
        "ko": "사이버보안", "es": "ciberseguridad", "zh": "网络安全",
        "ru": "кибербезопасность", "vi": "an ninh mạng"
    },
    "cyberattack": {
        "en": "cyberattack", "fr": "cyberattaque", "ja": "サイバー攻撃",
        "ko": "사이버공격", "es": "ciberataque", "zh": "网络攻击",
        "ru": "кибератака", "vi": "tấn công mạng"
    },
    "terrorism": {
        "en": "terrorism", "fr": "terrorisme", "ja": "テロリズム", "ko": "테러리즘",
        "es": "terrorismo", "zh": "恐怖主义", "ru": "терроризм", "vi": "khủng bố"
    },
    "sanctions": {
        "en": "sanctions", "fr": "sanctions", "ja": "制裁", "ko": "제재",
        "es": "sanciones", "zh": "制裁", "ru": "санкции", "vi": "trừng phạt"
    },
    "ceasefire": {
        "en": "ceasefire", "fr": "cessez-le-feu", "ja": "停戦", "ko": "휴전",
        "es": "alto el fuego", "zh": "停火", "ru": "прекращение огня", "vi": "ngừng bắn"
    },
    "arms race": {
        "en": "arms race", "fr": "course aux armements", "ja": "軍拡競争",
        "ko": "군비경쟁", "es": "carrera armamentista", "zh": "军备竞赛",
        "ru": "гонка вооружений", "vi": "chạy đua vũ trang"
    },
    "weapons": {
        "en": "weapons", "fr": "armes", "ja": "兵器", "ko": "무기",
        "es": "armas", "zh": "武器", "ru": "оружие", "vi": "vũ khí"
    },
    "fighter jet": {
        "en": "fighter jet", "fr": "avion de chasse", "ja": "戦闘機",
        "ko": "전투기", "es": "avión de combate", "zh": "战斗机",
        "ru": "истребитель", "vi": "máy bay chiến đấu"
    },
    "aircraft carrier": {
        "en": "aircraft carrier", "fr": "porte-avions", "ja": "空母",
        "ko": "항공모함", "es": "portaaviones", "zh": "航空母舰",
        "ru": "авианосец", "vi": "tàu sân bay"
    },
    "military exercise": {
        "en": "military exercise", "fr": "exercice militaire", "ja": "軍事演習",
        "ko": "군사훈련", "es": "ejercicio militar", "zh": "军事演习",
        "ru": "военные учения", "vi": "tập trận"
    },
    "military base": {
        "en": "military base", "fr": "base militaire", "ja": "軍事基地",
        "ko": "군사기지", "es": "base militar", "zh": "军事基地",
        "ru": "военная база", "vi": "căn cứ quân sự"
    },

    # ═══════════════════════════════════════════════════════════
    # NGOẠI GIAO & CHÍNH TRỊ
    # ═══════════════════════════════════════════════════════════
    "diplomacy": {
        "en": "diplomacy", "fr": "diplomatie", "ja": "外交", "ko": "외교",
        "es": "diplomacia", "zh": "外交", "ru": "дипломатия", "vi": "ngoại giao"
    },
    "sovereignty": {
        "en": "sovereignty", "fr": "souveraineté", "ja": "主権", "ko": "주권",
        "es": "soberanía", "zh": "主权", "ru": "суверенитет", "vi": "chủ quyền"
    },
    "territorial dispute": {
        "en": "territorial dispute", "fr": "différend territorial", "ja": "領土紛争",
        "ko": "영토분쟁", "es": "disputa territorial", "zh": "领土争端",
        "ru": "территориальный спор", "vi": "tranh chấp lãnh thổ"
    },
    "trade war": {
        "en": "trade war", "fr": "guerre commerciale", "ja": "貿易戦争",
        "ko": "무역전쟁", "es": "guerra comercial", "zh": "贸易战",
        "ru": "торговая война", "vi": "chiến tranh thương mại"
    },
    "coup": {
        "en": "coup", "fr": "coup d'État", "ja": "クーデター", "ko": "쿠데타",
        "es": "golpe de estado", "zh": "政变", "ru": "переворот", "vi": "đảo chính"
    },
    "election": {
        "en": "election", "fr": "élection", "ja": "選挙", "ko": "선거",
        "es": "elección", "zh": "选举", "ru": "выборы", "vi": "bầu cử"
    },
    "human rights": {
        "en": "human rights", "fr": "droits de l'homme", "ja": "人権", "ko": "인권",
        "es": "derechos humanos", "zh": "人权", "ru": "права человека", "vi": "nhân quyền"
    },
    "refugee": {
        "en": "refugee", "fr": "réfugié", "ja": "難民", "ko": "난민",
        "es": "refugiado", "zh": "难民", "ru": "беженец", "vi": "người tị nạn"
    },
    "espionage": {
        "en": "espionage", "fr": "espionnage", "ja": "スパイ活動", "ko": "간첩",
        "es": "espionaje", "zh": "间谍", "ru": "шпионаж", "vi": "gián điệp"
    },
    "alliance": {
        "en": "alliance", "fr": "alliance", "ja": "同盟", "ko": "동맹",
        "es": "alianza", "zh": "联盟", "ru": "альянс", "vi": "liên minh"
    },
    "summit": {
        "en": "summit", "fr": "sommet", "ja": "首脳会談", "ko": "정상회담",
        "es": "cumbre", "zh": "峰会", "ru": "саммит", "vi": "hội nghị thượng đỉnh"
    },

    # ═══════════════════════════════════════════════════════════
    # KINH TẾ & THƯƠNG MẠI
    # ═══════════════════════════════════════════════════════════
    "supply chain": {
        "en": "supply chain", "fr": "chaîne d'approvisionnement", "ja": "サプライチェーン",
        "ko": "공급망", "es": "cadena de suministro", "zh": "供应链",
        "ru": "цепочка поставок", "vi": "chuỗi cung ứng"
    },
    "semiconductor": {
        "en": "semiconductor", "fr": "semi-conducteur", "ja": "半導体",
        "ko": "반도체", "es": "semiconductor", "zh": "半导体",
        "ru": "полупроводник", "vi": "bán dẫn"
    },
    "rare earth": {
        "en": "rare earth", "fr": "terres rares", "ja": "レアアース",
        "ko": "희토류", "es": "tierras raras", "zh": "稀土",
        "ru": "редкоземельные", "vi": "đất hiếm"
    },
    "tariff": {
        "en": "tariff", "fr": "tarif douanier", "ja": "関税", "ko": "관세",
        "es": "arancel", "zh": "关税", "ru": "тариф", "vi": "thuế quan"
    },
    "energy security": {
        "en": "energy security", "fr": "sécurité énergétique", "ja": "エネルギー安全保障",
        "ko": "에너지 안보", "es": "seguridad energética", "zh": "能源安全",
        "ru": "энергетическая безопасность", "vi": "an ninh năng lượng"
    },

    # ═══════════════════════════════════════════════════════════
    # CÔNG NGHỆ
    # ═══════════════════════════════════════════════════════════
    "artificial intelligence": {
        "en": "artificial intelligence", "fr": "intelligence artificielle",
        "ja": "人工知能", "ko": "인공지능", "es": "inteligencia artificial",
        "zh": "人工智能", "ru": "искусственный интеллект", "vi": "trí tuệ nhân tạo"
    },
    "drone": {
        "en": "drone", "fr": "drone", "ja": "ドローン", "ko": "드론",
        "es": "dron", "zh": "无人机", "ru": "дрон", "vi": "máy bay không người lái"
    },
    "hypersonic": {
        "en": "hypersonic", "fr": "hypersonique", "ja": "極超音速",
        "ko": "극초음속", "es": "hipersónico", "zh": "高超音速",
        "ru": "гиперзвуковой", "vi": "siêu vượt âm"
    },
    "satellite": {
        "en": "satellite", "fr": "satellite", "ja": "衛星", "ko": "위성",
        "es": "satélite", "zh": "卫星", "ru": "спутник", "vi": "vệ tinh"
    },
    "5g": {
        "en": "5G", "fr": "5G", "ja": "5G", "ko": "5G",
        "es": "5G", "zh": "5G", "ru": "5G", "vi": "5G"
    },

    # ═══════════════════════════════════════════════════════════
    # AN NINH HÀNG HẢI & MÔI TRƯỜNG
    # ═══════════════════════════════════════════════════════════
    "maritime security": {
        "en": "maritime security", "fr": "sécurité maritime", "ja": "海洋安全保障",
        "ko": "해양안보", "es": "seguridad marítima", "zh": "海上安全",
        "ru": "морская безопасность", "vi": "an ninh hàng hải"
    },
    "freedom of navigation": {
        "en": "freedom of navigation", "fr": "liberté de navigation",
        "ja": "航行の自由", "ko": "항행의 자유", "es": "libertad de navegación",
        "zh": "航行自由", "ru": "свобода навигации", "vi": "tự do hàng hải"
    },
    "fishing": {
        "en": "fishing", "fr": "pêche", "ja": "漁業", "ko": "어업",
        "es": "pesca", "zh": "渔业", "ru": "рыболовство", "vi": "ngư nghiệp"
    },
    "climate change": {
        "en": "climate change", "fr": "changement climatique", "ja": "気候変動",
        "ko": "기후변화", "es": "cambio climático", "zh": "气候变化",
        "ru": "изменение климата", "vi": "biến đổi khí hậu"
    },
    "natural disaster": {
        "en": "natural disaster", "fr": "catastrophe naturelle", "ja": "自然災害",
        "ko": "자연재해", "es": "desastre natural", "zh": "自然灾害",
        "ru": "стихийное бедствие", "vi": "thiên tai"
    },

    # ═══════════════════════════════════════════════════════════
    # ĐỊA DANH VIỆT NAM (phổ biến trong tin quốc tế)
    # ═══════════════════════════════════════════════════════════
    "hanoi": {
        "en": "Hanoi", "fr": "Hanoï", "ja": "ハノイ", "ko": "하노이",
        "es": "Hanói", "zh": "河内", "ru": "Ханой", "vi": "Hà Nội"
    },
    "ho chi minh city": {
        "en": "Ho Chi Minh City", "fr": "Hô Chi Minh-Ville",
        "ja": "ホーチミン市", "ko": "호치민시", "es": "Ciudad Ho Chi Minh",
        "zh": "胡志明市", "ru": "Хошимин", "vi": "Thành phố Hồ Chí Minh"
    },
    "da nang": {
        "en": "Da Nang", "fr": "Da Nang", "ja": "ダナン", "ko": "다낭",
        "es": "Da Nang", "zh": "岘港", "ru": "Дананг", "vi": "Đà Nẵng"
    },
    "spratly": {
        "en": "Spratly", "fr": "Spratleys", "ja": "スプラトリー",
        "ko": "스프래틀리", "es": "Spratly", "zh": "南沙群岛",
        "ru": "Спратли", "vi": "Trường Sa"
    },
    "paracel": {
        "en": "Paracel", "fr": "Paracels", "ja": "パラセル",
        "ko": "파라셀", "es": "Paracel", "zh": "西沙群岛",
        "ru": "Парасельские", "vi": "Hoàng Sa"
    },
}

# Tạo reverse lookup: từ bất kỳ ngôn ngữ nào → key gốc (English)
_REVERSE_LOOKUP = {}
for _key, _translations in MULTILANG_DICT.items():
    for _lang, _val in _translations.items():
        _REVERSE_LOOKUP[_val.lower()] = _key
    _REVERSE_LOOKUP[_key.lower()] = _key


# 7 ngôn ngữ mục tiêu
TARGET_LANGS = ["en", "fr", "ja", "ko", "es", "zh", "ru"]


def translate_keyword(keyword: str) -> tuple[dict, bool]:
    """Dịch 1 từ khóa sang 7 ngôn ngữ.

    Returns:
        tuple: (dict {lang_code: [translations]}, found: bool)
        found=True nếu tìm thấy trong từ điển, False nếu không.
    """
    result = {lang: set() for lang in TARGET_LANGS}
    kw_lower = keyword.lower().strip()

    # Tìm trực tiếp trong dict
    if kw_lower in MULTILANG_DICT:
        entry = MULTILANG_DICT[kw_lower]
        for lang in TARGET_LANGS:
            if lang in entry:
                result[lang].add(entry[lang])
        return {lang: list(vals) for lang, vals in result.items()}, True

    # Tìm qua reverse lookup (từ khóa có thể là tiếng Việt, Nhật, Trung...)
    if kw_lower in _REVERSE_LOOKUP:
        base_key = _REVERSE_LOOKUP[kw_lower]
        entry = MULTILANG_DICT[base_key]
        for lang in TARGET_LANGS:
            if lang in entry:
                result[lang].add(entry[lang])
        return {lang: list(vals) for lang, vals in result.items()}, True

    # Viết HOA toàn bộ (acronyms: AI, UN, EU...) → giống nhau đa ngôn ngữ, coi như đã dịch
    if keyword.strip().isupper() and len(keyword.strip()) >= 2:
        for lang in TARGET_LANGS:
            result[lang].add(keyword.strip())
        return {lang: list(vals) for lang, vals in result.items()}, True

    # Không tìm thấy → giữ nguyên cho tất cả ngôn ngữ
    for lang in TARGET_LANGS:
        result[lang].add(keyword)
    return {lang: list(vals) for lang, vals in result.items()}, False


def expand_keywords_multilang(keywords: list[str]) -> dict:
    """Mở rộng danh sách keywords sang 7 ngôn ngữ.

    Args:
        keywords: Danh sách từ khóa gốc (có thể là tiếng Anh, Việt, hoặc bất kỳ)

    Returns:
        dict: {
            "original": [...],          # Từ khóa gốc
            "by_lang": {lang: [...]},   # Từ khóa theo ngôn ngữ
            "all_keywords": [...],      # Tất cả từ khóa (gộp)
            "untranslated": [...]       # Từ khóa không có trong từ điển
        }
    """
    if not keywords:
        return {"original": [], "by_lang": {}, "all_keywords": [], "untranslated": []}

    by_lang = {lang: set() for lang in TARGET_LANGS}
    all_kws = set()
    untranslated = []

    for kw in keywords:
        kw_stripped = kw.strip()
        if not kw_stripped:
            continue

        # Giữ nguyên keyword gốc
        all_kws.add(kw_stripped)

        # Xử lý AND: dịch từng phần rồi ghép lại
        if " AND " in kw_stripped:
            parts = [p.strip() for p in kw_stripped.split(" AND ") if p.strip()]
            # Dịch từng phần
            parts_by_lang = {lang: [] for lang in TARGET_LANGS}
            for part in parts:
                translated, found = translate_keyword(part)
                if not found:
                    untranslated.append(part)
                for lang in TARGET_LANGS:
                    if translated[lang]:
                        parts_by_lang[lang].append(translated[lang][0])
                    else:
                        parts_by_lang[lang].append(part)
            # Ghép lại thành AND expression cho từng ngôn ngữ
            for lang in TARGET_LANGS:
                if parts_by_lang[lang]:
                    and_expr = " AND ".join(parts_by_lang[lang])
                    by_lang[lang].add(and_expr)
                    all_kws.add(and_expr)
        else:
            translated, found = translate_keyword(kw_stripped)
            if not found:
                untranslated.append(kw_stripped)
            for lang in TARGET_LANGS:
                for t in translated[lang]:
                    by_lang[lang].add(t)
                    all_kws.add(t)

    return {
        "original": keywords,
        "by_lang": {lang: list(vals) for lang, vals in by_lang.items()},
        "all_keywords": list(all_kws),
        "untranslated": list(dict.fromkeys(untranslated))  # Loại trùng, giữ thứ tự
    }
