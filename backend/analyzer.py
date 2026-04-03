"""
Module phân tích thông tin thu thập được.
Tổng hợp, phân loại, đánh giá mức độ quan trọng, phân tích tác động tới Việt Nam.
"""

import re
from datetime import datetime, timezone
from collections import Counter


# ═══════════════════════════════════════════════════════════════
# TỪ KHÓA AN NINH ĐỐI NGOẠI
# ═══════════════════════════════════════════════════════════════

SECURITY_KEYWORDS = {
    "high": [
        "military", "conflict", "war", "attack", "missile", "nuclear",
        "sanctions", "invasion", "coup", "terrorism", "armed",
        "south china sea", "bien dong", "spratly", "paracel",
        "sovereignty", "territorial", "maritime dispute",
        "cyber attack", "espionage", "intelligence",
        "ASEAN", "Indo-Pacific", "Quad", "AUKUS",
        "militaire", "conflit", "guerre",
        "военный", "конфликт",
        "军事", "冲突", "南海",
        "군사", "분쟁",
        "軍事", "紛争",
    ],
    "medium": [
        "diplomacy", "treaty", "alliance", "defense", "strategic",
        "geopolitics", "trade war", "tariff", "embargo",
        "human rights", "refugee", "migration",
        "infrastructure", "belt and road", "BRI",
        "submarine", "aircraft carrier", "navy",
        "diplomat", "ambassador", "summit", "bilateral",
        "diplomatique", "traité",
        "дипломатия", "договор",
        "外交", "条约",
    ],
    "low": [
        "economy", "trade", "investment", "cooperation",
        "technology", "climate", "environment",
        "education", "culture", "tourism",
        "économie", "commerce",
        "экономика", "торговля",
    ]
}

FOCUS_ENTITIES = {
    "critical": [
        "Vietnam", "Viet Nam", "China", "United States", "USA",
        "South China Sea", "Bien Dong",
        "Taiwan", "North Korea", "DPRK",
    ],
    "high": [
        "ASEAN", "Japan", "South Korea", "Australia", "India",
        "Russia", "Philippines", "Indonesia", "Thailand",
        "Cambodia", "Laos", "Myanmar", "Malaysia", "Singapore",
    ],
    "medium": [
        "EU", "NATO", "United Nations", "G7", "G20",
        "Middle East", "Africa", "Latin America",
        "France", "Germany", "United Kingdom",
    ]
}

# ═══════════════════════════════════════════════════════════════
# TỪ KHÓA LIÊN QUAN VIỆT NAM
# ═══════════════════════════════════════════════════════════════

VIETNAM_KEYWORDS = [
    "vietnam", "viet nam", "vietnamese", "hanoi", "ho chi minh",
    "saigon", "mekong", "south china sea", "bien dong",
    "spratly", "paracel", "hoang sa", "truong sa",
    "tonkin", "indochina",
]

# Chủ đề tác động tới Việt Nam
VIETNAM_IMPACT_CATEGORIES = {
    "Maritime & Territorial": [
        "south china sea", "bien dong", "spratly", "paracel",
        "maritime", "territorial", "island", "reef", "shoal",
        "fishing", "coast guard", "exclusive economic zone", "EEZ",
        "freedom of navigation", "FONOP", "nine-dash line",
    ],
    "Military & Security": [
        "military", "defense", "weapon", "missile", "submarine",
        "aircraft carrier", "navy", "air force", "army",
        "arms deal", "military exercise", "war game",
        "cyber", "espionage", "intelligence",
    ],
    "Trade & Economy": [
        "trade", "tariff", "export", "import", "FDI",
        "investment", "supply chain", "manufacturing",
        "semiconductor", "textile", "electronics",
        "trade war", "sanctions", "embargo",
    ],
    "Diplomacy & Alliances": [
        "ASEAN", "bilateral", "summit", "treaty", "alliance",
        "partnership", "diplomatic", "ambassador", "foreign minister",
        "Quad", "AUKUS", "Indo-Pacific", "comprehensive strategic",
    ],
    "Regional Stability": [
        "Taiwan", "North Korea", "Myanmar", "coup",
        "refugee", "migration", "Mekong", "conflict",
        "humanitarian", "crisis",
    ],
    "Technology & Cyber": [
        "cyber", "AI", "technology transfer", "5G",
        "semiconductor", "digital", "surveillance",
        "data", "internet", "telecom",
    ],
}

# ═══════════════════════════════════════════════════════════════
# PHÂN LOẠI NGUỒN
# ═══════════════════════════════════════════════════════════════

SOURCE_CATEGORIES = {
    "Wire Services": ["Reuters", "AP News", "Xinhua", "TASS", "Yonhap", "Kyodo", "EFE"],
    "Western Media": ["BBC", "CNN", "Guardian", "Le Monde", "France 24", "RFI", "El País", "Deutsche Welle", "DW"],
    "Asia-Pacific Media": ["South China Morning Post", "Nikkei", "Strait Times", "Korea Herald", "NHK", "Channel News Asia", "ABC Australia"],
    "Defense & Security": ["Defense One", "Defense News", "Stars and Stripes", "War on the Rocks", "Breaking Defense", "Military Times", "RealClear Defense", "CSIS", "RAND", "Brookings"],
    "Analysis & Think Tank": ["Foreign Affairs", "Diplomat", "CSIS", "Brookings", "RAND", "Carnegie", "Crisis Group", "Jamestown"],
    "Middle East Media": ["Al Jazeera"],
    "Russian Media": ["TASS", "RT News"],
    "Chinese Media": ["Xinhua", "Global Times", "Caixin", "South China Morning Post"],
    "Google News": ["Google News"],
    "OSINT / GDELT": ["GDELT"],
    "Social / Reddit": ["Reddit"],
}


def categorize_source(source_name: str) -> list[str]:
    """Phân loại 1 nguồn vào các nhóm."""
    cats = []
    for cat, patterns in SOURCE_CATEGORIES.items():
        for pat in patterns:
            if pat.lower() in source_name.lower():
                cats.append(cat)
                break
    return cats if cats else ["Other"]


# ═══════════════════════════════════════════════════════════════
# CHẤM ĐIỂM
# ═══════════════════════════════════════════════════════════════

def calculate_relevance_score(article: dict) -> dict:
    """
    Scoring system (0-100):
    - High security keywords:    +15 each
    - Medium security keywords:  +8 each
    - Low security keywords:     +3 each
    - Critical entities:         +20 each (Vietnam, China, USA, SCS, Taiwan, DPRK)
    - High entities:             +10 each (ASEAN, Japan, Korea, Australia...)
    - Medium entities:           +5 each  (EU, NATO, UN, G7...)

    Classification:
    - Critical: >= 60 points
    - High:     35-59 points
    - Medium:   15-34 points
    - Low:      < 15 points
    """
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
    score = 0
    matched = []

    for kw in SECURITY_KEYWORDS["high"]:
        if kw.lower() in text:
            score += 15
            matched.append(kw)
    for kw in SECURITY_KEYWORDS["medium"]:
        if kw.lower() in text:
            score += 8
            matched.append(kw)
    for kw in SECURITY_KEYWORDS["low"]:
        if kw.lower() in text:
            score += 3
            matched.append(kw)

    for entity in FOCUS_ENTITIES["critical"]:
        if entity.lower() in text:
            score += 20
            matched.append(f"[Entity] {entity}")
    for entity in FOCUS_ENTITIES["high"]:
        if entity.lower() in text:
            score += 10
            matched.append(f"[Entity] {entity}")
    for entity in FOCUS_ENTITIES["medium"]:
        if entity.lower() in text:
            score += 5
            matched.append(f"[Entity] {entity}")

    score = min(score, 100)

    if score >= 60:
        level = "critical"
    elif score >= 35:
        level = "high"
    elif score >= 15:
        level = "medium"
    else:
        level = "low"

    return {
        "score": score,
        "level": level,
        "matched_keywords": list(set(matched))[:10]
    }


def check_vietnam_relevance(article: dict) -> dict:
    """
    Kiểm tra mức độ liên quan tới Việt Nam.
    Returns: {is_related, relevance (direct/indirect/none), impact_categories}
    """
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()

    # Kiểm tra đề cập trực tiếp Việt Nam
    direct = any(kw in text for kw in VIETNAM_KEYWORDS)

    # Phân loại chủ đề tác động
    impact_cats = []
    for cat, keywords in VIETNAM_IMPACT_CATEGORIES.items():
        if any(kw.lower() in text for kw in keywords):
            impact_cats.append(cat)

    # Kiểm tra liên quan gián tiếp (qua thực thể khu vực)
    regional_mentions = any(e.lower() in text for e in
                           ["ASEAN", "South China Sea", "Mekong", "Indo-Pacific",
                            "Southeast Asia", "Cambodia", "Laos", "Thailand",
                            "Philippines", "Indonesia", "Malaysia", "Singapore"])

    if direct:
        relevance = "direct"
    elif regional_mentions and impact_cats:
        relevance = "indirect"
    else:
        relevance = "none"

    return {
        "is_vietnam_related": relevance != "none",
        "vietnam_relevance": relevance,
        "impact_categories": impact_cats,
    }


# ═══════════════════════════════════════════════════════════════
# PHÂN TÍCH TÁC ĐỘNG VIỆT NAM
# ═══════════════════════════════════════════════════════════════

def analyze_vietnam_impact(articles: list[dict]) -> dict:
    """
    Phân tích chuyên sâu tác động tới Việt Nam.
    """
    direct_articles = []
    indirect_articles = []
    impact_by_category = {}
    threat_by_direction = {"direct": {"critical": 0, "high": 0, "medium": 0, "low": 0},
                           "indirect": {"critical": 0, "high": 0, "medium": 0, "low": 0}}

    for art in articles:
        vn = art.get("vietnam_info", {})
        rel = vn.get("vietnam_relevance", "none")
        if rel == "none":
            continue

        level = art.get("relevance_level", "low")
        if rel == "direct":
            direct_articles.append(art)
            threat_by_direction["direct"][level] += 1
        else:
            indirect_articles.append(art)
            threat_by_direction["indirect"][level] += 1

        for cat in vn.get("impact_categories", []):
            if cat not in impact_by_category:
                impact_by_category[cat] = {"count": 0, "articles": []}
            impact_by_category[cat]["count"] += 1
            if len(impact_by_category[cat]["articles"]) < 5:
                impact_by_category[cat]["articles"].append({
                    "title": art.get("title", ""),
                    "source": art.get("source", ""),
                    "url": art.get("url", ""),
                    "level": level,
                    "score": art.get("relevance_score", 0),
                })

    # Sắp xếp categories theo count
    sorted_categories = sorted(impact_by_category.items(), key=lambda x: x[1]["count"], reverse=True)

    # Tạo summary
    total_related = len(direct_articles) + len(indirect_articles)
    summary_parts = []
    summary_parts.append(f"Total Vietnam-related articles: {total_related} "
                        f"({len(direct_articles)} direct, {len(indirect_articles)} indirect)")

    if direct_articles:
        d = threat_by_direction["direct"]
        summary_parts.append(f"\nDirect mentions: {d['critical']} critical, {d['high']} high, "
                           f"{d['medium']} medium, {d['low']} low")
        summary_parts.append("\nTop direct articles:")
        for art in sorted(direct_articles, key=lambda x: x.get("relevance_score", 0), reverse=True)[:5]:
            summary_parts.append(f"  [{art.get('source', '')}] {art.get('title', '')}")
            summary_parts.append(f"    Impact: {', '.join(art.get('vietnam_info', {}).get('impact_categories', []))}")

    if sorted_categories:
        summary_parts.append(f"\nImpact areas:")
        for cat, info in sorted_categories:
            summary_parts.append(f"  {cat}: {info['count']} articles")

    return {
        "total_related": total_related,
        "direct_count": len(direct_articles),
        "indirect_count": len(indirect_articles),
        "direct_articles": direct_articles[:20],
        "indirect_articles": indirect_articles[:20],
        "threat_by_direction": threat_by_direction,
        "impact_by_category": {cat: info for cat, info in sorted_categories},
        "summary": "\n".join(summary_parts),
    }


# ═══════════════════════════════════════════════════════════════
# PHÂN TÍCH TỔNG HỢP
# ═══════════════════════════════════════════════════════════════

def analyze_articles(articles: list[dict]) -> dict:
    if not articles:
        return {
            "total": 0,
            "analyzed_articles": [],
            "summary": "No articles to analyze.",
            "threat_assessment": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "key_topics": [],
            "geographic_focus": [],
            "timeline": [],
            "source_breakdown": {},
            "vietnam_impact": analyze_vietnam_impact([]),
        }

    analyzed = []
    threat_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    all_keywords = []
    all_entities = []
    source_cat_counts = {}

    for article in articles:
        relevance = calculate_relevance_score(article)
        vietnam_info = check_vietnam_relevance(article)
        source_cats = categorize_source(article.get("source", ""))

        article_analyzed = {
            **article,
            "relevance_score": relevance["score"],
            "relevance_level": relevance["level"],
            "matched_keywords": relevance["matched_keywords"],
            "vietnam_info": vietnam_info,
            "source_categories": source_cats,
        }
        analyzed.append(article_analyzed)

        threat_counts[relevance["level"]] += 1
        all_keywords.extend([kw for kw in relevance["matched_keywords"] if not kw.startswith("[Entity]")])
        all_entities.extend([kw.replace("[Entity] ", "") for kw in relevance["matched_keywords"] if kw.startswith("[Entity]")])

        for sc in source_cats:
            source_cat_counts[sc] = source_cat_counts.get(sc, 0) + 1

    analyzed.sort(key=lambda x: x["relevance_score"], reverse=True)

    keyword_freq = Counter(all_keywords).most_common(15)
    entity_freq = Counter(all_entities).most_common(15)

    # Vietnam impact analysis
    vietnam_impact = analyze_vietnam_impact(analyzed)

    # Summary (English)
    critical_articles = [a for a in analyzed if a["relevance_level"] == "critical"]
    high_articles = [a for a in analyzed if a["relevance_level"] == "high"]

    summary_parts = []
    summary_parts.append(f"Collected {len(articles)} articles from international sources.")
    summary_parts.append(f"Classification: {threat_counts['critical']} critical, "
                        f"{threat_counts['high']} high, {threat_counts['medium']} medium, "
                        f"{threat_counts['low']} low.")
    summary_parts.append(f"Vietnam-related: {vietnam_impact['total_related']} "
                        f"({vietnam_impact['direct_count']} direct, {vietnam_impact['indirect_count']} indirect)")

    if critical_articles:
        summary_parts.append("\n--- CRITICAL ---")
        for art in critical_articles[:5]:
            summary_parts.append(f"  [{art['source']}] {art['title']}")
            summary_parts.append(f"    URL: {art['url']}")
            summary_parts.append(f"    Keywords: {', '.join(art['matched_keywords'][:5])}")

    if high_articles:
        summary_parts.append("\n--- HIGH PRIORITY ---")
        for art in high_articles[:5]:
            summary_parts.append(f"  [{art['source']}] {art['title']}")
            summary_parts.append(f"    URL: {art['url']}")

    if keyword_freq:
        summary_parts.append(f"\nKey topics: {', '.join([f'{kw[0]} ({kw[1]})' for kw in keyword_freq[:10]])}")

    if entity_freq:
        summary_parts.append(f"Key entities: {', '.join([f'{e[0]} ({e[1]})' for e in entity_freq[:10]])}")

    # Timeline
    timeline = {}
    for art in analyzed:
        try:
            dt = datetime.fromisoformat(art["published"].replace("Z", "+00:00"))
            hour_key = dt.strftime("%Y-%m-%d %H:00")
            timeline[hour_key] = timeline.get(hour_key, 0) + 1
        except Exception:
            pass

    return {
        "total": len(analyzed),
        "analyzed_articles": analyzed,
        "summary": "\n".join(summary_parts),
        "threat_assessment": threat_counts,
        "key_topics": [{"keyword": kw, "count": cnt} for kw, cnt in keyword_freq],
        "geographic_focus": [{"entity": e, "count": cnt} for e, cnt in entity_freq],
        "timeline": [{"time": k, "count": v} for k, v in sorted(timeline.items())],
        "source_breakdown": dict(sorted(source_cat_counts.items(), key=lambda x: x[1], reverse=True)),
        "vietnam_impact": vietnam_impact,
    }
