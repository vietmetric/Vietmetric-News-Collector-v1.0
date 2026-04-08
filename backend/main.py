"""
Vietmetric News Collector - Backend API
Thu thập và phân tích thông tin quốc tế phục vụ an ninh đối ngoại Việt Nam.
"""

import os
import io
import re
import asyncio
import tempfile
import shutil
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import pdfplumber
from docx import Document as DocxDocument

from collector import collect_all
from analyzer import analyze_articles
from exporter import export_docx, export_pdf
from sources import NEWS_SOURCES, OSINT_SOURCES, SOCIAL_SOURCES, ALL_SOURCES, LANG_LABELS
from translations import expand_keywords_multilang


def parse_keywords(raw: str) -> list[str]:
    """Parse chuỗi từ khóa, hỗ trợ ngoặc kép cho cụm từ nhiều từ.

    Ví dụ:
      'AI, Vietnam'                    → ['AI', 'Vietnam']
      '"Quảng Ninh", "Điện Biên Phủ"' → ['Quảng Ninh', 'Điện Biên Phủ']
      '"South China Sea", ASEAN'       → ['South China Sea', 'ASEAN']
      'AI AND "Biển Đông"'             → ['AI AND Biển Đông']
      '"nuclear weapon", Iran'         → ['nuclear weapon', 'Iran']
    """
    if not raw or not raw.strip():
        return []
    result = []
    # Tách các cụm trong ngoặc kép trước, thay bằng placeholder
    quoted = re.findall(r'"([^"]+)"', raw)
    # Thay ngoặc kép bằng placeholder dạng __Q0__, __Q1__...
    temp = raw
    for i, q in enumerate(quoted):
        temp = temp.replace(f'"{q}"', f'__Q{i}__', 1)
    # Split phần còn lại bằng dấu phẩy
    parts = [p.strip() for p in temp.split(",")]
    for part in parts:
        if not part:
            continue
        # Khôi phục các placeholder
        restored = part
        for i, q in enumerate(quoted):
            restored = restored.replace(f'__Q{i}__', q)
        restored = restored.strip()
        if restored:
            result.append(restored)
    return result

# ═══════════════════════════════════════════════════════════════
# KHỞI TẠO APP
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title="Vietmetric News Collector",
    description="Hệ thống thu thập và phân tích thông tin quốc tế phục vụ an ninh đối ngoại",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thư mục lưu file tạm
EXPORT_DIR = os.path.join(tempfile.gettempdir(), "osint_exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "osint_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Cache kết quả gần nhất
_latest_result = {"data": None, "timestamp": None}


# ═══════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/api/sources")
async def get_sources():
    """Trả về danh sách tất cả nguồn tin."""
    return {
        "news_sources": [
            {"name": s["name"], "lang": s.get("lang", ""), "category": s.get("category", ""), "url": s["url"]}
            for s in NEWS_SOURCES
        ],
        "osint_sources": [
            {"name": s["name"], "description": s.get("description", ""), "url": s["url"]}
            for s in OSINT_SOURCES
        ],
        "social_sources": [
            {"name": s["name"], "description": s.get("description", ""), "url": s["url"]}
            for s in SOCIAL_SOURCES
        ],
        "total": len(ALL_SOURCES),
        "languages": LANG_LABELS
    }


@app.post("/api/collect")
async def collect_news(
    keywords: str = Form(""),
    hours: int = Form(24),
    minutes: Optional[int] = Form(None),
    days: Optional[int] = Form(None),
    months: Optional[int] = Form(None),
    langs: str = Form(""),
    custom_sources: str = Form(""),
):
    """
    Thu thập tin tức từ tất cả các nguồn.

    - keywords: Từ khóa tìm kiếm, phân cách bởi dấu phẩy
    - hours: Khoảng thời gian (giờ), mặc định 24
    - minutes: Khoảng thời gian (phút) - ưu tiên nếu có
    - days: Khoảng thời gian (ngày) - ưu tiên nếu có
    - months: Khoảng thời gian (tháng) - ưu tiên nếu có
    - langs: Lọc ngôn ngữ, phân cách bởi dấu phẩy (en,fr,zh...)
    - custom_sources: JSON array các nguồn tùy chỉnh [{name, url}]
    """
    import json as _json

    # Xử lý thời gian
    if months:
        actual_hours = months * 30 * 24
    elif days:
        actual_hours = days * 24
    elif minutes:
        actual_hours = max(1, minutes // 60) if minutes >= 60 else 1
    else:
        actual_hours = hours

    # Giới hạn tối đa 720 giờ (30 ngày) cho GDELT
    actual_hours = min(actual_hours, 720)

    keyword_list = parse_keywords(keywords)
    lang_list = [l.strip() for l in langs.split(",") if l.strip()] if langs else None

    # Parse custom sources
    custom_src_list = []
    if custom_sources and custom_sources.strip():
        try:
            raw_list = _json.loads(custom_sources)
            for cs in raw_list:
                url = cs.get("url", "").strip()
                if url:
                    custom_src_list.append({
                        "name": cs.get("name", "") or url,
                        "url": url,
                        "type": "rss",
                        "lang": "en",
                        "category": "Custom Source"
                    })
        except Exception:
            pass

    try:
        result = await collect_all(
            keywords=keyword_list,
            hours=actual_hours,
            langs_filter=lang_list,
            custom_sources=custom_src_list if custom_src_list else None
        )

        # Phân tích
        analysis = analyze_articles(result["articles"])

        # Cache
        _latest_result["data"] = analysis
        _latest_result["timestamp"] = datetime.now(timezone.utc).isoformat()

        # Thông tin keywords đa ngôn ngữ
        multilang_info = expand_keywords_multilang(keyword_list) if keyword_list else None

        return {
            "success": True,
            "stats": result["stats"],
            "analysis": {
                "total": analysis["total"],
                "summary": analysis["summary"],
                "threat_assessment": analysis["threat_assessment"],
                "key_topics": analysis["key_topics"],
                "geographic_focus": analysis["geographic_focus"],
                "timeline": analysis["timeline"],
                "source_breakdown": analysis.get("source_breakdown", {}),
                "vietnam_impact": analysis.get("vietnam_impact", {}),
            },
            "articles": analysis["analyzed_articles"][:200],
            "translated_keywords": multilang_info["by_lang"] if multilang_info else {},
            "untranslated_keywords": multilang_info["untranslated"] if multilang_info else [],
            "timestamp": _latest_result["timestamp"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi thu thập: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Kiểm tra kết nối tới tất cả nguồn tin (42 nguồn).
    RSS: dùng feedparser (giống collector thực tế).
    OSINT/Social: dùng httpx GET.
    """
    import httpx
    import feedparser as fp
    from collector import _disable_socks_proxy, _restore_proxy

    # Xây dựng danh sách test
    test_sources = []

    for s in NEWS_SOURCES:
        test_sources.append({
            "name": s["name"], "url": s["url"],
            "group": "News / RSS", "lang": s.get("lang", ""),
            "method": "rss"
        })

    for s in OSINT_SOURCES:
        url = s["url"]
        if "gdeltproject.org" in url and "doc/doc" in url:
            url += "?query=test&mode=ArtList&maxrecords=1&format=json&timespan=1h"
        test_sources.append({
            "name": s["name"], "url": url,
            "group": "OSINT", "lang": "", "method": "http"
        })

    for s in SOCIAL_SOURCES:
        url = s["url"]
        if "twitter.com" in url or "x.com" in url:
            test_sources.append({
                "name": s["name"], "url": url,
                "group": "Social Media", "lang": "",
                "method": "skip", "note": "Requires API key"
            })
            continue
        if ".rss" in url:
            test_sources.append({
                "name": s["name"], "url": url,
                "group": "Social Media", "lang": "", "method": "rss"
            })
        else:
            if "reddit.com" in url and ".json" in url:
                url += "?limit=1"
            test_sources.append({
                "name": s["name"], "url": url,
                "group": "Social Media", "lang": "", "method": "http"
            })

    _disable_socks_proxy()
    results = {}

    try:
        async with httpx.AsyncClient(
            timeout=15.0, follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        ) as client:

            async def check_rss(src):
                """Test RSS bằng feedparser — cách collector thực sự hoạt động."""
                name = src["name"]
                try:
                    resp = await client.get(src["url"])
                    status = resp.status_code
                    if status >= 400:
                        # Thử feedparser trực tiếp (một số feed trả 403 cho GET
                        # nhưng feedparser vẫn parse được qua cơ chế riêng)
                        feed = await asyncio.get_event_loop().run_in_executor(
                            None, fp.parse, src["url"]
                        )
                        if feed.entries and len(feed.entries) > 0:
                            return name, {
                                "ok": True, "status": status,
                                "articles": len(feed.entries),
                                "group": src["group"], "lang": src.get("lang", ""),
                                "note": f"HTTP {status} but feed works ({len(feed.entries)} articles)"
                            }
                        return name, {
                            "ok": False, "status": status,
                            "group": src["group"], "lang": src.get("lang", "")
                        }
                    # Parse RSS content
                    feed = fp.parse(resp.text)
                    n_articles = len(feed.entries) if feed.entries else 0
                    return name, {
                        "ok": True, "status": status,
                        "articles": n_articles,
                        "group": src["group"], "lang": src.get("lang", ""),
                    }
                except Exception as e:
                    # Fallback: thử feedparser trực tiếp
                    try:
                        feed = await asyncio.get_event_loop().run_in_executor(
                            None, fp.parse, src["url"]
                        )
                        if feed.entries and len(feed.entries) > 0:
                            return name, {
                                "ok": True, "status": 0,
                                "articles": len(feed.entries),
                                "group": src["group"], "lang": src.get("lang", ""),
                                "note": f"Direct feed OK ({len(feed.entries)} articles)"
                            }
                    except Exception:
                        pass
                    return name, {
                        "ok": False, "status": 0,
                        "error": str(e)[:120],
                        "group": src["group"], "lang": src.get("lang", "")
                    }

            async def check_http(src):
                """Test HTTP endpoint (OSINT API, Reddit JSON)."""
                name = src["name"]
                try:
                    resp = await client.get(src["url"])
                    return name, {
                        "ok": resp.status_code < 400,
                        "status": resp.status_code,
                        "group": src["group"], "lang": src.get("lang", ""),
                    }
                except Exception as e:
                    return name, {
                        "ok": False, "status": 0,
                        "error": str(e)[:120],
                        "group": src["group"], "lang": src.get("lang", "")
                    }

            async def check_one(src):
                if src["method"] == "skip":
                    return src["name"], {
                        "ok": None, "status": 0, "group": src["group"],
                        "lang": src.get("lang", ""), "note": src.get("note", "")
                    }
                elif src["method"] == "rss":
                    return await check_rss(src)
                else:
                    return await check_http(src)

            tasks = [check_one(s) for s in test_sources]
            done = await asyncio.gather(*tasks)
            for name, info in done:
                results[name] = info

    finally:
        _restore_proxy()

    # Thống kê
    testable = {k: v for k, v in results.items() if v.get("ok") is not None}
    ok_count = sum(1 for r in testable.values() if r["ok"])
    total_count = len(testable)
    skipped_count = len(results) - total_count
    all_ok = ok_count == total_count

    # Nhóm theo group
    groups = {}
    for name, info in results.items():
        g = info.get("group", "Other")
        if g not in groups:
            groups[g] = {"ok": 0, "fail": 0, "skip": 0, "sources": {}}
        groups[g]["sources"][name] = info
        if info.get("ok") is None:
            groups[g]["skip"] += 1
        elif info["ok"]:
            groups[g]["ok"] += 1
        else:
            groups[g]["fail"] += 1

    return {
        "connected": all_ok,
        "ok_count": ok_count,
        "total_count": total_count,
        "skipped_count": skipped_count,
        "groups": groups,
        "sources": results,
    }


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload file Word (.docx) hoặc PDF (.pdf) để trích xuất chủ đề.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Không có file")

    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ("docx", "pdf", "txt"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file .docx, .pdf, .txt")

    filepath = os.path.join(UPLOAD_DIR, file.filename)
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)

    extracted_text = ""

    try:
        if ext == "docx":
            doc = DocxDocument(filepath)
            extracted_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

        elif ext == "pdf":
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages[:50]:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"

        elif ext == "txt":
            extracted_text = content.decode("utf-8", errors="ignore")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi đọc file: {str(e)}")

    # ── Trích xuất từ khóa thông minh ──
    suggested_keywords = extract_smart_keywords(extracted_text)

    return {
        "success": True,
        "filename": file.filename,
        "text_length": len(extracted_text),
        "text_preview": extracted_text[:2000],
        "suggested_keywords": suggested_keywords
    }


def _detect_language(text: str) -> str:
    """Phát hiện ngôn ngữ: 'vi' hoặc 'en'."""
    # Ký tự đặc trưng tiếng Việt
    vi_chars = set("àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ")
    vi_count = sum(1 for c in text.lower() if c in vi_chars)
    # Nếu >0.5% ký tự là tiếng Việt → xác định là tiếng Việt
    ratio = vi_count / max(len(text), 1)
    return "vi" if ratio > 0.005 else "en"


# ═══════════════════════════════════════════════════════════════
# TỪ ĐIỂN VIỆT-ANH CHO LĨNH VỰC AN NINH / ĐỊA CHÍNH TRỊ
# ═══════════════════════════════════════════════════════════════

VI_EN_SECURITY = {
    # Quân sự & An ninh
    "chiến tranh": "war",
    "xung đột": "conflict",
    "quân sự": "military",
    "quốc phòng": "defense",
    "vũ khí": "weapons",
    "tên lửa": "missile",
    "hạt nhân": "nuclear",
    "tàu ngầm": "submarine",
    "tàu sân bay": "aircraft carrier",
    "hải quân": "navy",
    "không quân": "air force",
    "lục quân": "army",
    "tập trận": "military exercise",
    "an ninh": "security",
    "tình báo": "intelligence",
    "gián điệp": "espionage",
    "khủng bố": "terrorism",
    "đảo chính": "coup",
    "nội chiến": "civil war",
    "binh sĩ": "soldiers",
    "không kích": "airstrike",
    "ném bom": "bombing",
    "phòng không": "air defense",
    "đạn đạo": "ballistic",
    "pháo binh": "artillery",
    "đặc nhiệm": "special forces",
    "chiến đấu cơ": "fighter jet",
    "tàu chiến": "warship",
    "tuần tra": "patrol",
    "đối đầu": "confrontation",
    "leo thang": "escalation",
    "căng thẳng": "tensions",
    "đe dọa": "threat",
    "răn đe": "deterrence",

    # Biển Đông & Lãnh thổ
    "biển đông": "South China Sea",
    "biển đông nam á": "South China Sea",
    "tranh chấp": "dispute",
    "chủ quyền": "sovereignty",
    "lãnh thổ": "territorial",
    "hải phận": "maritime",
    "vùng đặc quyền kinh tế": "exclusive economic zone",
    "đường lưỡi bò": "nine-dash line",
    "đường chín đoạn": "nine-dash line",
    "hoàng sa": "Paracel Islands",
    "trường sa": "Spratly Islands",
    "tuần duyên": "coast guard",
    "tự do hàng hải": "freedom of navigation",
    "đảo nhân tạo": "artificial island",
    "bãi đá": "reef",
    "bãi cạn": "shoal",
    "ngư dân": "fishermen",
    "đánh bắt cá": "fishing",

    # Ngoại giao & Liên minh
    "ngoại giao": "diplomacy",
    "hiệp ước": "treaty",
    "liên minh": "alliance",
    "đối tác chiến lược": "strategic partnership",
    "đối tác toàn diện": "comprehensive partnership",
    "hội nghị thượng đỉnh": "summit",
    "đại sứ": "ambassador",
    "bộ trưởng ngoại giao": "foreign minister",
    "trừng phạt": "sanctions",
    "cấm vận": "embargo",
    "quan hệ song phương": "bilateral relations",
    "quan hệ đa phương": "multilateral relations",
    "đàm phán": "negotiation",
    "hòa bình": "peace",
    "hòa đàm": "peace talks",
    "ngừng bắn": "ceasefire",

    # Kinh tế & Thương mại
    "chiến tranh thương mại": "trade war",
    "thuế quan": "tariff",
    "thương mại": "trade",
    "đầu tư": "investment",
    "chuỗi cung ứng": "supply chain",
    "bán dẫn": "semiconductor",
    "công nghệ": "technology",
    "năng lượng": "energy",
    "dầu mỏ": "oil",
    "khí đốt": "natural gas",
    "kinh tế": "economy",
    "tăng trưởng": "growth",
    "lạm phát": "inflation",
    "suy thoái": "recession",
    "xuất khẩu": "export",
    "nhập khẩu": "import",
    "viện trợ": "aid",

    # Nhân quyền & Xã hội
    "nhân quyền": "human rights",
    "tị nạn": "refugee",
    "di cư": "migration",
    "nhân đạo": "humanitarian",
    "khủng hoảng": "crisis",
    "biến đổi khí hậu": "climate change",
    "thiên tai": "natural disaster",

    # Công nghệ & Mạng
    "tấn công mạng": "cyber attack",
    "an ninh mạng": "cybersecurity",
    "trí tuệ nhân tạo": "artificial intelligence",
    "giám sát": "surveillance",
    "dữ liệu": "data",
    "mạng xã hội": "social media",
    "tin giả": "disinformation",
    "chiến tranh thông tin": "information warfare",
    "chiến tranh lai": "hybrid warfare",
}

VI_EN_ENTITIES = {
    # Quốc gia
    "việt nam": "Vietnam",
    "trung quốc": "China",
    "mỹ": "United States",
    "hoa kỳ": "United States",
    "nga": "Russia",
    "nhật bản": "Japan",
    "hàn quốc": "South Korea",
    "triều tiên": "North Korea",
    "bắc triều tiên": "North Korea",
    "đài loan": "Taiwan",
    "úc": "Australia",
    "ấn độ": "India",
    "philippines": "Philippines",
    "indonesia": "Indonesia",
    "thái lan": "Thailand",
    "campuchia": "Cambodia",
    "lào": "Laos",
    "myanmar": "Myanmar",
    "malaysia": "Malaysia",
    "singapore": "Singapore",
    "nước anh": "United Kingdom",
    "vương quốc anh": "United Kingdom",
    "pháp": "France",
    "đức": "Germany",
    "iran": "Iran",
    "israel": "Israel",
    "ukraine": "Ukraine",
    "ả rập xê út": "Saudi Arabia",
    "thổ nhĩ kỳ": "Turkey",
    "ai cập": "Egypt",
    "pakistan": "Pakistan",
    "afghanistan": "Afghanistan",
    "iraq": "Iraq",
    "syria": "Syria",
    "palestine": "Palestine",
    "libya": "Libya",
    "yemen": "Yemen",
    "somalia": "Somalia",
    "sudan": "Sudan",

    # Tổ chức
    "liên hợp quốc": "United Nations",
    "liên hiệp quốc": "United Nations",
    "nato": "NATO",
    "asean": "ASEAN",
    "liên minh châu âu": "EU",
    "ngân hàng thế giới": "World Bank",
    "quỹ tiền tệ quốc tế": "IMF",
    "tổ chức thương mại thế giới": "WTO",
    "hội đồng bảo an": "UN Security Council",

    # Địa danh quan trọng
    "eo biển đài loan": "Taiwan Strait",
    "bán đảo triều tiên": "Korean Peninsula",
    "ấn độ dương - thái bình dương": "Indo-Pacific",
    "trung đông": "Middle East",
    "châu phi": "Africa",
    "sông mê kông": "Mekong River",
    "biên giới": "border",

    # Liên minh / Khung khổ
    "bộ tứ": "Quad",
    "vành đai và con đường": "Belt and Road",
    "con đường tơ lụa": "Belt and Road",
}


def extract_smart_keywords(text: str) -> list[str]:
    """
    Trích xuất từ khóa thông minh từ văn bản.
    Hỗ trợ cả tiếng Việt và tiếng Anh.
    Tiếng Việt: tìm cụm từ đã biết → dịch sang tiếng Anh.
    Tiếng Anh: NER đơn giản + từ khóa an ninh + bigrams.
    """
    import re
    from collections import Counter
    from analyzer import SECURITY_KEYWORDS, FOCUS_ENTITIES, VIETNAM_KEYWORDS

    if not text or len(text.strip()) < 20:
        return []

    lang = _detect_language(text)
    text_lower = text.lower()

    if lang == "vi":
        return _extract_vietnamese_keywords(text, text_lower)
    else:
        return _extract_english_keywords(text, text_lower)


def _extract_vietnamese_keywords(text: str, text_lower: str) -> list[str]:
    """
    Trích xuất từ khóa từ văn bản tiếng Việt → trả về tiếng Anh.
    Ưu tiên: cụm từ tìm kiếm ghép (entity + topic) > sự kiện cụ thể > chủ đề > entity đơn.
    """
    import re
    from collections import Counter

    # ── Bước 1: Tìm thực thể và chủ đề riêng biệt ──
    found_entities = {}  # en_name -> count
    found_topics = {}    # en_topic -> count

    def _count_vi(term, txt):
        if len(term) <= 3:
            pattern = r'(?<!\w)' + re.escape(term) + r'(?!\w)'
            return len(re.findall(pattern, txt))
        return txt.count(term)

    for vi_term, en_term in VI_EN_ENTITIES.items():
        count = _count_vi(vi_term, text_lower)
        if count > 0:
            found_entities[en_term] = found_entities.get(en_term, 0) + count

    for vi_term, en_term in VI_EN_SECURITY.items():
        count = _count_vi(vi_term, text_lower)
        if count > 0:
            found_topics[en_term] = found_topics.get(en_term, 0) + count

    # ── Bước 2: Tìm cụm từ ghép Việt → compound search phrases ──
    # Bảng cụm từ ghép phổ biến (entity + topic) có giá trị tìm kiếm cao
    VI_COMPOUND_PHRASES = {
        # Iran
        ("iran", "hạt nhân"): "Iran nuclear",
        ("iran", "tấn công"): "Iran attack",
        ("iran", "chiến tranh"): "Iran war",
        ("iran", "tên lửa"): "Iran missile",
        ("iran", "trừng phạt"): "Iran sanctions",
        ("iran", "israel"): "Iran Israel conflict",
        # Trung Quốc
        ("trung quốc", "biển đông"): "China South China Sea",
        ("trung quốc", "đài loan"): "China Taiwan",
        ("trung quốc", "quân sự"): "China military",
        ("trung quốc", "thương mại"): "China trade war",
        # Mỹ
        ("mỹ", "trung quốc"): "US China relations",
        ("mỹ", "iran"): "US Iran",
        ("mỹ", "quân sự"): "US military",
        ("mỹ", "trừng phạt"): "US sanctions",
        # Nga / Ukraine
        ("nga", "ukraine"): "Russia Ukraine war",
        ("nga", "quân sự"): "Russia military",
        # Israel
        ("israel", "palestine"): "Israel Palestine",
        ("israel", "chiến tranh"): "Israel war",
        ("israel", "tấn công"): "Israel attack",
        # Đài Loan
        ("đài loan", "trung quốc"): "Taiwan China tensions",
        ("đài loan", "quân sự"): "Taiwan military",
        # Triều Tiên
        ("triều tiên", "hạt nhân"): "North Korea nuclear",
        ("triều tiên", "tên lửa"): "North Korea missile",
        # Biển Đông
        ("biển đông", "tranh chấp"): "South China Sea dispute",
        ("biển đông", "quân sự"): "South China Sea military",
        # Chung
        ("xung đột", "vũ trang"): "armed conflict",
        ("hòa bình", "đàm phán"): "peace negotiations",
        ("ngừng bắn", "đàm phán"): "ceasefire negotiations",
        ("chiến tranh", "thương mại"): "trade war",
        ("an ninh", "mạng"): "cybersecurity",
        ("vũ khí", "hạt nhân"): "nuclear weapons",
        ("liên minh", "quân sự"): "military alliance",
    }

    found_compounds = {}
    for (vi1, vi2), en_phrase in VI_COMPOUND_PHRASES.items():
        if vi1 in text_lower and vi2 in text_lower:
            # Đếm dựa trên min(count1, count2) — cả 2 phải xuất hiện
            c1 = _count_vi(vi1, text_lower)
            c2 = _count_vi(vi2, text_lower)
            count = min(c1, c2)
            if count > 0:
                found_compounds[en_phrase] = count

    # ── Bước 3: Tìm sự kiện/chủ đề cụ thể từ ngữ cảnh ──
    # Phân tích proximity: entity + topic xuất hiện gần nhau trong cùng đoạn
    paragraphs = text_lower.split("\n")
    proximity_phrases = {}
    entity_en_set = set(found_entities.keys())
    topic_en_set = set(found_topics.keys())

    for para in paragraphs:
        para_entities = [e for e in VI_EN_ENTITIES.items() if e[0] in para]
        para_topics = [t for t in VI_EN_SECURITY.items() if t[0] in para]

        for vi_e, en_e in para_entities:
            for vi_t, en_t in para_topics:
                phrase = f"{en_e} {en_t}"
                if phrase not in found_compounds.values():
                    if phrase not in proximity_phrases:
                        proximity_phrases[phrase] = 0
                    proximity_phrases[phrase] += 1

    # ── Bước 4: Viết tắt quốc tế ──
    acronyms = re.findall(r'\b([A-Z]{2,6})\b', text)
    noise_acr = {"THE", "AND", "FOR", "BUT", "NOT", "PDF", "DOC", "TXT",
                 "HTTP", "HTTPS", "WWW", "COM", "ORG", "Ep"}
    acr_freq = Counter(acronyms)

    # ── Bước 5: Tên riêng tiếng Anh trong văn bản Việt ──
    english_names = re.findall(r'\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){1,3})\b', text)
    name_freq = Counter(english_names)
    noise_names = {"Theo", "Trong", "Ngay", "Sau", "Truoc", "Nhung",
                   "Noi", "Voi", "Cung", "Mot", "Hai", "Khi"}

    # ── Bước 6: Xếp hạng tổng hợp ──
    all_candidates = {}

    # Compound phrases (ưu tiên cao nhất — đây là search terms tốt nhất)
    for phrase, count in found_compounds.items():
        all_candidates[phrase] = 100 + count * 15

    # Proximity phrases (entity + topic cùng đoạn, top 10 phổ biến nhất)
    top_proximity = sorted(proximity_phrases.items(), key=lambda x: -x[1])[:10]
    for phrase, count in top_proximity:
        if count >= 2 and phrase not in all_candidates:
            # Không thêm nếu đã có compound tương tự
            already = any(phrase.lower() in c.lower() or c.lower() in phrase.lower()
                          for c in all_candidates)
            if not already:
                all_candidates[phrase] = 60 + count * 5

    # Chủ đề (topics) — chỉ lấy các chủ đề xuất hiện nhiều
    for topic, count in sorted(found_topics.items(), key=lambda x: -x[1]):
        if count >= 3 and topic not in all_candidates:
            already = any(topic.lower() in c.lower() for c in all_candidates)
            if not already:
                all_candidates[topic] = min(count * 5, 50)

    # Entity đơn — chỉ khi chưa có trong compound
    for entity, count in sorted(found_entities.items(), key=lambda x: -x[1]):
        already = any(entity.lower() in c.lower() for c in all_candidates)
        if not already and count >= 2:
            all_candidates[entity] = min(count * 4, 40)

    # Acronyms
    for acr, count in acr_freq.most_common(15):
        if acr not in noise_acr and count >= 2 and acr not in all_candidates:
            all_candidates[acr] = count * 8

    # Tên riêng tiếng Anh
    for name, count in name_freq.most_common(20):
        if name not in noise_names and count >= 2:
            already = any(name.lower() in e.lower() or e.lower() in name.lower()
                          for e in all_candidates)
            if not already:
                all_candidates[name] = count * 5

    # ── Bước 7: Loại trùng và trả kết quả ──
    sorted_kw = sorted(all_candidates.items(), key=lambda x: -x[1])

    final = []
    seen_lower = set()
    for kw, score in sorted_kw:
        kw_lower = kw.lower()
        # Bỏ từ khóa quá ngắn (1 từ, < 3 ký tự)
        if len(kw) < 3:
            continue
        # Bỏ trùng lặp
        if any(kw_lower == s for s in seen_lower):
            continue
        # Cho phép cả "Iran" và "Iran nuclear" cùng tồn tại
        # Nhưng bỏ nếu hoàn toàn chứa trong từ khác
        if len(kw.split()) == 1:  # từ đơn
            if any(kw_lower in s and kw_lower != s for s in seen_lower):
                continue
        final.append(kw)
        seen_lower.add(kw_lower)
        if len(final) >= 20:
            break

    return final


def _extract_english_keywords(text: str, text_lower: str) -> list[str]:
    """Trích xuất từ khóa từ văn bản tiếng Anh."""
    import re
    from collections import Counter
    from analyzer import SECURITY_KEYWORDS, FOCUS_ENTITIES

    all_candidates = {}

    # ── Bước 1: Thực thể địa chính trị đã biết ──
    for tier, entities in FOCUS_ENTITIES.items():
        score = {"critical": 90, "high": 70, "medium": 50}[tier]
        for e in entities:
            if e.lower() in text_lower:
                all_candidates[e] = score

    # ── Bước 2: Từ khóa an ninh đã biết ──
    for tier, words in SECURITY_KEYWORDS.items():
        score = {"high": 60, "medium": 40, "low": 20}[tier]
        for w in words:
            if len(w) > 3 and re.match(r'^[a-zA-Z\s\-]+$', w) and w.lower() in text_lower:
                display = w.title() if len(w) > 5 else w.upper()
                if display not in all_candidates:
                    all_candidates[display] = score

    # ── Bước 3: Viết tắt (NATO, ASEAN...) ──
    acronyms = re.findall(r'\b([A-Z]{2,6})\b', text)
    noise_acr = {"THE", "AND", "FOR", "BUT", "NOT", "ARE", "WAS", "HAS",
                 "HAD", "HIS", "HER", "ITS", "OUR", "WHO", "HOW", "MAY",
                 "CAN", "ALL", "ONE", "TWO", "NEW", "OLD", "BIG", "PDF",
                 "DOC", "TXT", "HTTP", "HTTPS", "WWW", "COM", "ORG"}
    acr_freq = Counter(acronyms)
    for acr, count in acr_freq.most_common(20):
        if acr not in noise_acr and count >= 2 and acr not in all_candidates:
            all_candidates[acr] = count * 10

    # ── Bước 4: Tên riêng (NER đơn giản) ──
    proper_nouns = re.findall(
        r'\b([A-Z][a-z]+(?:\s+(?:of|the|and|for|de|du|von|van|al|bin|el)\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b',
        text
    )
    noise_proper = {"The", "This", "That", "These", "Those", "There", "Their",
                    "Here", "Where", "When", "What", "Which", "Some", "Many",
                    "More", "Most", "Other", "Such", "Each", "Every", "Both",
                    "Several", "About", "After", "Before", "Between", "Under",
                    "Over", "Through", "During", "Without", "Within", "Against",
                    "According", "However", "Although", "Despite", "While",
                    "Since", "Because", "Also", "With", "From", "Into",
                    "New York", "South East", "North East"}
    proper_freq = Counter(proper_nouns)
    for name, count in proper_freq.most_common(30):
        if name not in noise_proper and count >= 2 and len(name) > 3:
            already = any(name.lower() in e.lower() or e.lower() in name.lower()
                          for e in all_candidates)
            if not already:
                all_candidates[name] = count * 5

    # ── Bước 5: Bigrams quan trọng ──
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
        "been", "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "shall", "can", "need",
        "not", "no", "nor", "so", "if", "then", "than", "too", "very",
        "just", "about", "up", "out", "into", "over", "after", "before",
        "between", "under", "through", "during", "without", "within",
        "its", "it", "he", "she", "they", "we", "you", "i", "my", "your",
        "his", "her", "their", "our", "this", "that", "these", "those",
        "which", "who", "whom", "what", "where", "when", "how", "why",
        "each", "every", "all", "both", "few", "more", "most", "other",
        "some", "such", "only", "also", "back", "even", "still", "already",
        "since", "until", "while", "because", "although", "though",
        "however", "therefore", "thus", "hence", "yet", "now",
        "said", "says", "according", "new", "many", "much", "well",
        "made", "make", "like", "use", "used", "using",
        "one", "two", "three", "four", "five", "first", "last",
        "part", "per", "year", "years", "time", "way", "day", "days",
        "people", "world", "country", "countries", "state", "states",
        "government", "report", "number", "case", "group", "area",
    }
    clean_words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
    bigram_freq = Counter()
    for i in range(len(clean_words) - 1):
        w1, w2 = clean_words[i].lower(), clean_words[i + 1].lower()
        if w1 not in stop_words and w2 not in stop_words:
            bigram_freq[f"{clean_words[i]} {clean_words[i+1]}".lower()] += 1

    for bg, count in bigram_freq.most_common(20):
        if count >= 2:
            already = any(bg in kw.lower() or kw.lower() in bg
                          for kw in all_candidates)
            if not already:
                all_candidates[bg.title()] = count * 4

    # ── Bước 6: Xếp hạng và loại trùng ──
    sorted_kw = sorted(all_candidates.items(), key=lambda x: -x[1])

    final = []
    seen_lower = set()
    for kw, score in sorted_kw:
        kw_lower = kw.lower()
        if any(kw_lower in s or s in kw_lower for s in seen_lower):
            continue
        final.append(kw)
        seen_lower.add(kw_lower)
        if len(final) >= 20:
            break

    return final


@app.post("/api/export/docx")
async def export_docx_endpoint(
    keywords: str = Form(""),
    hours: int = Form(24),
    langs: str = Form(""),
):
    """Thu thập, phân tích và xuất báo cáo .docx"""
    keyword_list = parse_keywords(keywords)
    lang_list = [l.strip() for l in langs.split(",") if l.strip()] if langs else None

    result = await collect_all(keywords=keyword_list, hours=hours, langs_filter=lang_list)
    analysis = analyze_articles(result["articles"])

    filename = os.path.join(EXPORT_DIR, f"osint_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx")
    export_docx(analysis, filename)

    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=os.path.basename(filename)
    )


@app.post("/api/export/pdf")
async def export_pdf_endpoint(
    keywords: str = Form(""),
    hours: int = Form(24),
    langs: str = Form(""),
):
    """Thu thập, phân tích và xuất báo cáo .pdf"""
    keyword_list = parse_keywords(keywords)
    lang_list = [l.strip() for l in langs.split(",") if l.strip()] if langs else None

    result = await collect_all(keywords=keyword_list, hours=hours, langs_filter=lang_list)
    analysis = analyze_articles(result["articles"])

    filename = os.path.join(EXPORT_DIR, f"osint_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    export_pdf(analysis, filename)

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=os.path.basename(filename)
    )


@app.post("/api/export/cached/docx")
async def export_cached_docx():
    """Xuất báo cáo .docx từ kết quả thu thập gần nhất (đã cache)."""
    if not _latest_result["data"]:
        raise HTTPException(status_code=404, detail="Chưa có dữ liệu. Hãy thu thập trước.")

    filename = os.path.join(EXPORT_DIR, f"osint_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx")
    export_docx(_latest_result["data"], filename)

    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=os.path.basename(filename)
    )


@app.post("/api/export/cached/pdf")
async def export_cached_pdf():
    """Xuất báo cáo .pdf từ kết quả thu thập gần nhất (đã cache)."""
    if not _latest_result["data"]:
        raise HTTPException(status_code=404, detail="Chưa có dữ liệu. Hãy thu thập trước.")

    filename = os.path.join(EXPORT_DIR, f"osint_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    export_pdf(_latest_result["data"], filename)

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=os.path.basename(filename)
    )


# Serve frontend HTML
_backend_dir = os.path.dirname(os.path.abspath(__file__))
_frontend_html_path = os.path.join(_backend_dir, "..", "frontend", "index.html")
# Also check if running from project root
if not os.path.exists(_frontend_html_path):
    _frontend_html_path = os.path.join(os.getcwd(), "..", "frontend", "index.html")

@app.get("/logo.png", include_in_schema=False)
async def serve_logo():
    for candidate in [
        os.path.join(_backend_dir, "..", "frontend", "logo.png"),
        os.path.join(os.getcwd(), "..", "frontend", "logo.png"),
        os.path.join(os.getcwd(), "frontend", "logo.png"),
    ]:
        if os.path.exists(candidate):
            return FileResponse(candidate, media_type="image/png")
    return JSONResponse(status_code=404, content={"error": "Logo not found"})

@app.get("/", include_in_schema=False)
async def serve_frontend():
    from starlette.responses import HTMLResponse
    for candidate in [
        os.path.join(_backend_dir, "..", "frontend", "index.html"),
        os.path.join(os.getcwd(), "..", "frontend", "index.html"),
        os.path.join(os.getcwd(), "frontend", "index.html"),
    ]:
        if os.path.exists(candidate):
            with open(candidate, "r", encoding="utf-8") as f:
                content = f.read()
            return HTMLResponse(
                content=content,
                headers={
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Pragma": "no-cache",
                    "Expires": "0"
                }
            )
    return {"message": "Vietmetric News Collector API v1.0", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
