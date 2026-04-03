"""
Danh sách nguồn tin quốc tế đa ngôn ngữ phục vụ thu thập thông tin an ninh đối ngoại.
Tối thiểu 30 nguồn uy tín + nguồn OSINT + mạng xã hội.
Cập nhật: 2026-04-03 - Thay thế các RSS feed đã ngừng hoạt động.
"""

# ═══════════════════════════════════════════════════════════════
# NGUỒN TIN CHÍNH THỐNG (RSS feeds)
# ═══════════════════════════════════════════════════════════════

NEWS_SOURCES = [
    # ── TIẾNG ANH ──────────────────────────────────────────────

    # Reuters đã ngừng RSS từ 2020 → dùng Google News lọc theo Reuters
    {
        "name": "Reuters (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:reuters.com+world&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Thông tấn quốc tế"
    },
    # AP News đã ngừng RSS → dùng Google News lọc theo AP News
    {
        "name": "AP News (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:apnews.com+world&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Thông tấn quốc tế"
    },
    {
        "name": "BBC World News",
        "url": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "type": "rss",
        "lang": "en",
        "category": "Truyền thông Anh"
    },
    {
        "name": "BBC Asia",
        "url": "http://feeds.bbci.co.uk/news/world/asia/rss.xml",
        "type": "rss",
        "lang": "en",
        "category": "Truyền thông Anh"
    },
    {
        "name": "Al Jazeera English",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "type": "rss",
        "lang": "en",
        "category": "Truyền thông Trung Đông"
    },
    {
        "name": "The Guardian - World",
        "url": "https://www.theguardian.com/world/rss",
        "type": "rss",
        "lang": "en",
        "category": "Truyền thông Anh"
    },
    {
        "name": "CNN World",
        "url": "http://rss.cnn.com/rss/edition_world.rss",
        "type": "rss",
        "lang": "en",
        "category": "Truyền thông Mỹ"
    },
    {
        "name": "Foreign Affairs",
        "url": "https://www.foreignaffairs.com/rss.xml",
        "type": "rss",
        "lang": "en",
        "category": "Phân tích chiến lược"
    },
    {
        "name": "The Diplomat (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:thediplomat.com&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Phân tích châu Á-TBD"
    },
    {
        "name": "South China Morning Post",
        "url": "https://www.scmp.com/rss/91/feed",
        "type": "rss",
        "lang": "en",
        "category": "Truyền thông Hồng Kông"
    },
    # Nikkei Asia RSS không ổn định → dùng Google News
    {
        "name": "Nikkei Asia (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:asia.nikkei.com&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Truyền thông Nhật Bản"
    },
    # CSIS đã ngừng RSS công khai → dùng Google News
    {
        "name": "CSIS (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:csis.org&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Think tank an ninh"
    },
    {
        "name": "Brookings Institution",
        "url": "https://www.brookings.edu/feed/",
        "type": "rss",
        "lang": "en",
        "category": "Think tank chính sách"
    },
    # RAND feed không ổn định → dùng Google News
    {
        "name": "RAND Corporation (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:rand.org&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Think tank an ninh"
    },
    {
        "name": "Defense One",
        "url": "https://www.defenseone.com/rss/all/",
        "type": "rss",
        "lang": "en",
        "category": "Quốc phòng"
    },
    # Jane's cần subscription → thay bằng Defense News (công khai, cùng lĩnh vực)
    {
        "name": "Defense News",
        "url": "https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml",
        "type": "rss",
        "lang": "en",
        "category": "Quốc phòng"
    },
    {
        "name": "Strait Times - Asia",
        "url": "https://www.straitstimes.com/news/asia/rss.xml",
        "type": "rss",
        "lang": "en",
        "category": "Truyền thông Singapore"
    },
    # Stars and Stripes - tin quân sự Mỹ (thay cho Jane's)
    {
        "name": "Stars and Stripes (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:stripes.com+military&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Quốc phòng"
    },

    # ── QUỐC PHÒNG & AN NINH BỔ SUNG ──────────────────────────
    {
        "name": "War on the Rocks",
        "url": "https://warontherocks.com/feed/",
        "type": "rss",
        "lang": "en",
        "category": "Phân tích quốc phòng"
    },
    {
        "name": "Breaking Defense",
        "url": "https://breakingdefense.com/feed/",
        "type": "rss",
        "lang": "en",
        "category": "Công nghệ quốc phòng"
    },
    {
        "name": "Military Times (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:militarytimes.com&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Quốc phòng"
    },

    # ── THINK TANK BỔ SUNG ────────────────────────────────────
    {
        "name": "Carnegie Endowment",
        "url": "https://carnegieendowment.org/rss/",
        "type": "rss",
        "lang": "en",
        "category": "Think tank quốc tế"
    },
    {
        "name": "International Crisis Group (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:crisisgroup.org&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Phân tích xung đột"
    },
    {
        "name": "Jamestown Foundation",
        "url": "https://jamestown.org/feed/",
        "type": "rss",
        "lang": "en",
        "category": "An ninh Á-Âu"
    },

    # ── TRUYỀN THÔNG QUỐC TẾ BỔ SUNG ────────────────────────
    {
        "name": "Deutsche Welle (DW)",
        "url": "https://rss.dw.com/rdf/rss-en-all",
        "type": "rss",
        "lang": "en",
        "category": "Truyền thông Đức"
    },
    {
        "name": "Channel News Asia",
        "url": "https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml",
        "type": "rss",
        "lang": "en",
        "category": "Truyền thông Singapore"
    },
    {
        "name": "RealClear Defense (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:realcleardefense.com&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Tổng hợp quốc phòng"
    },
    {
        "name": "ABC Australia - Asia Pacific",
        "url": "https://www.abc.net.au/news/feed/51120/rss.xml",
        "type": "rss",
        "lang": "en",
        "category": "Truyền thông Úc"
    },

    # ── GOOGLE NEWS (ổn định cao, hoạt động ở hầu hết mọi mạng) ──
    {
        "name": "Google News - World",
        "url": "https://news.google.com/rss/search?q=world+news&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Tổng hợp Google News"
    },
    {
        "name": "Google News - Vietnam",
        "url": "https://news.google.com/rss/search?q=Vietnam&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Tổng hợp Google News"
    },
    {
        "name": "Google News - Asia Pacific",
        "url": "https://news.google.com/rss/search?q=ASEAN+OR+%22South+China+Sea%22+OR+%22Asia+Pacific%22&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Tổng hợp Google News"
    },
    # Thêm Google News - Security / Defense
    {
        "name": "Google News - Defense & Security",
        "url": "https://news.google.com/rss/search?q=military+OR+defense+OR+%22national+security%22&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "en",
        "category": "Tổng hợp Google News"
    },

    # ── TIẾNG PHÁP ─────────────────────────────────────────────
    {
        "name": "Le Monde - International",
        "url": "https://www.lemonde.fr/international/rss_full.xml",
        "type": "rss",
        "lang": "fr",
        "category": "Truyền thông Pháp"
    },
    {
        "name": "France 24 - Actualités",
        "url": "https://www.france24.com/fr/rss",
        "type": "rss",
        "lang": "fr",
        "category": "Truyền thông Pháp"
    },
    # RFI feed không ổn định → dùng Google News tiếng Pháp
    {
        "name": "RFI (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:rfi.fr+monde&hl=fr&gl=FR&ceid=FR:fr",
        "type": "rss",
        "lang": "fr",
        "category": "Truyền thông Pháp"
    },

    # ── TIẾNG NGA ──────────────────────────────────────────────
    {
        "name": "TASS (Nga)",
        "url": "https://tass.com/rss/v2.xml",
        "type": "rss",
        "lang": "ru",
        "category": "Thông tấn Nga"
    },
    {
        "name": "RT News",
        "url": "https://www.rt.com/rss/news/",
        "type": "rss",
        "lang": "ru",
        "category": "Truyền thông Nga"
    },

    # ── TIẾNG TRUNG ────────────────────────────────────────────
    {
        "name": "Xinhua (Tân Hoa Xã)",
        "url": "http://www.xinhuanet.com/world/news_world.xml",
        "type": "rss",
        "lang": "zh",
        "category": "Thông tấn Trung Quốc"
    },
    {
        "name": "Global Times",
        "url": "https://www.globaltimes.cn/rss/outbrain.xml",
        "type": "rss",
        "lang": "zh",
        "category": "Truyền thông Trung Quốc"
    },
    # Caixin RSS đã ngừng → dùng Google News
    {
        "name": "Caixin Global (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:caixinglobal.com&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "zh",
        "category": "Truyền thông Trung Quốc"
    },

    # ── TIẾNG HÀN ─────────────────────────────────────────────
    {
        "name": "Yonhap News (연합뉴스)",
        "url": "https://en.yna.co.kr/RSS/news.xml",
        "type": "rss",
        "lang": "ko",
        "category": "Thông tấn Hàn Quốc"
    },
    {
        "name": "Korea Herald",
        "url": "http://www.koreaherald.com/common/rss_xml.php?ct=102",
        "type": "rss",
        "lang": "ko",
        "category": "Truyền thông Hàn Quốc"
    },

    # ── TIẾNG NHẬT ─────────────────────────────────────────────
    {
        "name": "NHK World Japan",
        "url": "https://www3.nhk.or.jp/rss/news/cat0.xml",
        "type": "rss",
        "lang": "ja",
        "category": "Truyền thông Nhật Bản"
    },
    # Kyodo News đổi thành Japan Wire → dùng Google News
    {
        "name": "Kyodo News (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:english.kyodonews.net+OR+site:japanwire.net&hl=en-US&gl=US&ceid=US:en",
        "type": "rss",
        "lang": "ja",
        "category": "Thông tấn Nhật Bản"
    },

    # ── TIẾNG TÂY BAN NHA ─────────────────────────────────────
    {
        "name": "EFE (via Google News)",
        "url": "https://news.google.com/rss/search?q=site:efe.com&hl=es&gl=ES&ceid=ES:es",
        "type": "rss",
        "lang": "es",
        "category": "Thông tấn Tây Ban Nha"
    },
    {
        "name": "El País - Internacional",
        "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada",
        "type": "rss",
        "lang": "es",
        "category": "Truyền thông Tây Ban Nha"
    },
]

# ═══════════════════════════════════════════════════════════════
# NGUỒN TÌNH BÁO MỞ (OSINT)
# ═══════════════════════════════════════════════════════════════

OSINT_SOURCES = [
    {
        "name": "GDELT Project (HTTPS)",
        "url": "https://api.gdeltproject.org/api/v2/doc/doc",
        "type": "api",
        "description": "Global Database of Events, Language, and Tone - HTTPS endpoint"
    },
    {
        "name": "GDELT Project (HTTP)",
        "url": "http://api.gdeltproject.org/api/v2/doc/doc",
        "type": "api",
        "description": "Global Database of Events, Language, and Tone - HTTP fallback"
    },
    {
        "name": "ACLED (Armed Conflict)",
        "url": "https://acleddata.com/data-export-tool/",
        "type": "api",
        "description": "Dữ liệu xung đột vũ trang toàn cầu"
    },
    {
        "name": "SIPRI (Arms Transfers)",
        "url": "https://www.sipri.org/databases",
        "type": "reference",
        "description": "Viện nghiên cứu hòa bình Stockholm - chuyển giao vũ khí"
    },
]

# ═══════════════════════════════════════════════════════════════
# MẠNG XÃ HỘI
# ═══════════════════════════════════════════════════════════════

SOCIAL_SOURCES = [
    {
        "name": "X (Twitter) - Search",
        "url": "https://api.twitter.com/2/tweets/search/recent",
        "type": "social",
        "description": "Tìm kiếm tweet realtime (cần API key)"
    },
    {
        "name": "Reddit - WorldNews",
        "url": "https://www.reddit.com/r/worldnews/.rss",
        "type": "social",
        "description": "Tin tức quốc tế từ cộng đồng Reddit"
    },
    {
        "name": "Reddit - Geopolitics",
        "url": "https://www.reddit.com/r/geopolitics/.rss",
        "type": "social",
        "description": "Phân tích địa chính trị từ Reddit"
    },
    {
        "name": "Reddit - OSINT",
        "url": "https://www.reddit.com/r/OSINT/.rss",
        "type": "social",
        "description": "Cộng đồng tình báo mở Reddit"
    },
]

# Tổng hợp tất cả nguồn
ALL_SOURCES = NEWS_SOURCES + OSINT_SOURCES + SOCIAL_SOURCES

LANG_LABELS = {
    "en": "Tiếng Anh",
    "fr": "Tiếng Pháp",
    "ru": "Tiếng Nga",
    "zh": "Tiếng Trung",
    "ko": "Tiếng Hàn",
    "ja": "Tiếng Nhật",
    "es": "Tiếng Tây Ban Nha",
}
