"""
Module thu thập tin tức từ các nguồn quốc tế.
Hỗ trợ: RSS feeds, GDELT API, Reddit API.
"""

import asyncio
import os
import time
import hashlib
import re
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.parse import quote_plus

import feedparser
import httpx
from bs4 import BeautifulSoup

from sources import NEWS_SOURCES, OSINT_SOURCES, SOCIAL_SOURCES, LANG_LABELS


# ═══════════════════════════════════════════════════════════════
# QUẢN LÝ PROXY - Xử lý SOCKS5 không tương thích với httpx
# ═══════════════════════════════════════════════════════════════
_PROXY_VARS = ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
               "http_proxy", "https_proxy", "all_proxy"]
_saved_proxy = {}

def _get_http_proxy() -> Optional[str]:
    """Lấy HTTP proxy (không phải SOCKS) nếu có."""
    for var in ["HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"]:
        val = os.environ.get(var, "")
        if val and val.startswith("http"):
            return val
    return None

def _disable_socks_proxy():
    """Tắt SOCKS proxy (giữ HTTP proxy nếu có)."""
    for var in _PROXY_VARS:
        val = os.environ.get(var, "")
        if val and "socks" in val.lower():
            _saved_proxy[var] = os.environ.pop(var)

def _restore_proxy():
    """Khôi phục proxy env vars."""
    for var, val in _saved_proxy.items():
        os.environ[var] = val
    _saved_proxy.clear()


# ═══════════════════════════════════════════════════════════════
# TIỆN ÍCH
# ═══════════════════════════════════════════════════════════════

def generate_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:12]


def parse_date(entry) -> Optional[datetime]:
    """Trích xuất thời gian từ entry RSS."""
    for field in ("published_parsed", "updated_parsed"):
        tp = getattr(entry, field, None)
        if tp:
            try:
                return datetime(*tp[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


def clean_html(html_text: str) -> str:
    """Xóa thẻ HTML, trả về văn bản thuần."""
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text(separator=" ", strip=True)[:1000]


def matches_keywords(text: str, keywords: list[str]) -> bool:
    """Kiểm tra văn bản có chứa từ khóa không (case-insensitive)."""
    if not keywords:
        return True
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


# ═══════════════════════════════════════════════════════════════
# THU THẬP RSS
# ═══════════════════════════════════════════════════════════════

async def fetch_rss(source: dict, hours: int = 24, keywords: list[str] = None,
                    client: httpx.AsyncClient = None) -> dict:
    """Thu thập tin từ 1 nguồn RSS. Trả về dict {articles, error}."""
    results = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    try:
        if client:
            resp = await client.get(source["url"], timeout=15.0)
            # Kiểm tra HTTP status
            if resp.status_code >= 400:
                return {"articles": [], "error": f"HTTP {resp.status_code}"}
            feed = feedparser.parse(resp.text)
        else:
            feed = feedparser.parse(source["url"])

        for entry in feed.entries[:50]:
            pub_date = parse_date(entry)

            title = getattr(entry, "title", "")
            summary = clean_html(getattr(entry, "summary", getattr(entry, "description", "")))
            link = getattr(entry, "link", "")

            # Lọc theo thời gian
            if pub_date and pub_date < cutoff:
                continue

            # Lọc theo từ khóa
            combined_text = f"{title} {summary}"
            if not matches_keywords(combined_text, keywords or []):
                continue

            results.append({
                "id": generate_id(link),
                "source": source["name"],
                "source_lang": source.get("lang", "en"),
                "source_lang_label": LANG_LABELS.get(source.get("lang", "en"), "Tiếng Anh"),
                "category": source.get("category", ""),
                "title": title,
                "summary": summary,
                "url": link,
                "published": pub_date.isoformat() if pub_date else datetime.now(timezone.utc).isoformat(),
                "type": "news"
            })

    except Exception as e:
        print(f"[RSS ERROR] {source['name']}: {e}")
        return {"articles": [], "error": str(e)[:200]}

    return {"articles": results, "error": None}


# ═══════════════════════════════════════════════════════════════
# THU THẬP GDELT
# ═══════════════════════════════════════════════════════════════

async def _try_gdelt_endpoint(url: str, params: dict,
                              client: httpx.AsyncClient,
                              timeout: float = 30.0) -> Optional[dict]:
    """Thử gọi 1 GDELT endpoint. Trả về JSON data hoặc None."""
    try:
        resp = await client.get(url, params=params, timeout=timeout)
        if resp.status_code >= 400:
            print(f"[GDELT] {url} -> HTTP {resp.status_code}")
            return None

        content_type = resp.headers.get("content-type", "")
        text = resp.text.strip()

        # GDELT trả HTML khi quá tải hoặc lỗi
        if not text or text.startswith("<!") or text.startswith("<html"):
            print(f"[GDELT] {url} -> tra ve HTML/rong")
            return None

        return resp.json()
    except Exception as e:
        print(f"[GDELT] {url} -> {e}")
        return None


def _parse_gdelt_articles(data: dict, max_items: int = 75) -> list[dict]:
    """Chuyển đổi JSON response GDELT thành danh sách bài viết chuẩn."""
    results = []
    articles = data.get("articles", [])
    if not articles and isinstance(data, list):
        articles = data

    for art in articles[:max_items]:
        title = art.get("title", "")
        source_url = art.get("url", "")
        seendate = art.get("seendate", "")
        domain = art.get("domain", "")
        lang = art.get("language", "English")
        tone = art.get("tone", 0)

        pub_dt = None
        if seendate:
            try:
                pub_dt = datetime.strptime(seendate[:14], "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
            except Exception:
                pass

        tone_label = "tieu cuc" if tone < -3 else ("tich cuc" if tone > 3 else "trung tinh")

        results.append({
            "id": generate_id(source_url),
            "source": f"GDELT - {domain}",
            "source_lang": lang[:2].lower() if lang else "en",
            "source_lang_label": lang if lang else "English",
            "category": "OSINT / GDELT",
            "title": title,
            "summary": f"Tone: {tone:.1f} ({tone_label}) | Nguon: {domain}",
            "url": source_url,
            "published": pub_dt.isoformat() if pub_dt else datetime.now(timezone.utc).isoformat(),
            "type": "gdelt",
            "tone": tone
        })
    return results


async def fetch_gdelt(query: str = "", hours: int = 24,
                      client: httpx.AsyncClient = None) -> dict:
    """
    Thu thập từ GDELT Project. Trả về dict {articles, error}.

    Thử lần lượt nhiều endpoint (HTTPS Doc API -> HTTP Doc API -> Context API)
    với retry để tăng khả năng thành công.
    """
    search_term = query if query else "Vietnam OR ASEAN OR South China Sea"
    timespan = f"{min(hours, 720)}h"

    # Danh sách endpoint thử lần lượt (GDELT hỗ trợ cả HTTP và HTTPS)
    endpoints = [
        {
            "url": "https://api.gdeltproject.org/api/v2/doc/doc",
            "name": "GDELT Doc API (HTTPS)"
        },
        {
            "url": "http://api.gdeltproject.org/api/v2/doc/doc",
            "name": "GDELT Doc API (HTTP)"
        },
        {
            "url": "https://api.gdeltproject.org/api/v2/context/context",
            "name": "GDELT Context API (HTTPS)"
        },
        {
            "url": "http://api.gdeltproject.org/api/v2/context/context",
            "name": "GDELT Context API (HTTP)"
        },
    ]

    params = {
        "query": search_term,
        "mode": "ArtList",
        "maxrecords": "75",
        "timespan": timespan,
        "format": "json",
        "sort": "DateDesc"
    }

    own_client = False
    if not client:
        _disable_socks_proxy()
        try:
            client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0, connect=15.0),
                follow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
            )
            own_client = True
        finally:
            _restore_proxy()

    errors_log = []

    try:
        for ep in endpoints:
            print(f"[GDELT] Thu {ep['name']}...")

            # Thử tối đa 2 lần mỗi endpoint
            for attempt in range(2):
                data = await _try_gdelt_endpoint(ep["url"], params, client, timeout=30.0)
                if data is not None:
                    results = _parse_gdelt_articles(data)
                    if results:
                        print(f"[GDELT] Thanh cong: {ep['name']} -> {len(results)} bai viet")
                        return {"articles": results, "error": None}
                    else:
                        # JSON hợp lệ nhưng không có articles
                        errors_log.append(f"{ep['name']}: JSON OK nhung 0 bai viet")
                        break  # Không cần retry nếu server trả lời OK
                else:
                    errors_log.append(f"{ep['name']} lan {attempt+1}: khong phan hoi")
                    if attempt == 0:
                        await asyncio.sleep(2)  # Chờ 2s trước khi retry

        # Tất cả endpoint đều thất bại
        error_msg = "GDELT: tat ca endpoint that bai. " + " | ".join(errors_log[-4:])
        print(f"[GDELT ERROR]: {error_msg}")
        return {"articles": [], "error": error_msg[:300]}

    except Exception as e:
        print(f"[GDELT ERROR]: {e}")
        return {"articles": [], "error": str(e)[:200]}

    finally:
        if own_client:
            await client.aclose()


# ═══════════════════════════════════════════════════════════════
# THU THẬP REDDIT
# ═══════════════════════════════════════════════════════════════

async def fetch_reddit(source: dict, hours: int = 24, keywords: list[str] = None,
                       client: httpx.AsyncClient = None) -> dict:
    """Thu thập bài viết từ Reddit (JSON API công khai). Trả về dict {articles, error}."""
    results = []
    cutoff_ts = time.time() - (hours * 3600)

    headers = {
        "User-Agent": "OSINT-Collector/1.0 (research purpose)"
    }

    try:
        if not client:
            client = httpx.AsyncClient()

        resp = await client.get(
            source["url"],
            headers=headers,
            params={"limit": "50", "sort": "new"},
            timeout=15.0
        )
        data = resp.json()

        posts = data.get("data", {}).get("children", [])
        for post in posts:
            d = post.get("data", {})
            created = d.get("created_utc", 0)
            if created < cutoff_ts:
                continue

            title = d.get("title", "")
            selftext = d.get("selftext", "")[:500]
            url = d.get("url", "")
            permalink = f"https://www.reddit.com{d.get('permalink', '')}"
            score = d.get("score", 0)
            num_comments = d.get("num_comments", 0)

            combined = f"{title} {selftext}"
            if not matches_keywords(combined, keywords or []):
                continue

            results.append({
                "id": generate_id(permalink),
                "source": source["name"],
                "source_lang": "en",
                "source_lang_label": "Tiếng Anh",
                "category": "Mạng xã hội / Reddit",
                "title": title,
                "summary": f"Score: {score} | Bình luận: {num_comments}" + (f" | {selftext[:200]}" if selftext else ""),
                "url": url if url.startswith("http") else permalink,
                "permalink": permalink,
                "published": datetime.fromtimestamp(created, tz=timezone.utc).isoformat(),
                "type": "social",
                "score": score
            })

    except Exception as e:
        print(f"[REDDIT ERROR] {source['name']}: {e}")
        return {"articles": [], "error": str(e)[:200]}

    return {"articles": results, "error": None}


def _classify_error(err_msg: str) -> str:
    """Phân loại lỗi thu thập."""
    msg = err_msg.lower()
    if "name resolution" in msg or "getaddrinfo" in msg or "dns" in msg:
        return "DNS"
    if "403" in msg or "blocked" in msg or "allowlist" in msg or "forbidden" in msg:
        return "BLOCKED"
    if "timeout" in msg or "timed out" in msg:
        return "TIMEOUT"
    if "404" in msg:
        return "NOT_FOUND"
    return "OTHER"


# ═══════════════════════════════════════════════════════════════
# THU THẬP TỔNG HỢP
# ═══════════════════════════════════════════════════════════════

async def collect_all(
    keywords: list[str] = None,
    hours: int = 24,
    sources_filter: list[str] = None,
    langs_filter: list[str] = None
) -> dict:
    """
    Thu thập tin tức từ tất cả các nguồn.

    Args:
        keywords: Danh sách từ khóa lọc
        hours: Khoảng thời gian thu thập (giờ)
        sources_filter: Lọc theo tên nguồn cụ thể
        langs_filter: Lọc theo ngôn ngữ
    """
    start_time = time.time()
    all_results = []
    errors = []

    # Tắt SOCKS proxy (httpx không hỗ trợ), giữ HTTP proxy
    _disable_socks_proxy()

    client_kwargs = {
        "follow_redirects": True,
        "headers": {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "application/rss+xml, application/xml, application/json, text/html, */*",
            "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
        },
        "timeout": httpx.Timeout(20.0, connect=10.0),
    }

    try:
        async with httpx.AsyncClient(**client_kwargs) as client:

            tasks = []

            # RSS feeds (nguồn chính thống)
            for src in NEWS_SOURCES:
                if sources_filter and src["name"] not in sources_filter:
                    continue
                if langs_filter and src.get("lang") not in langs_filter:
                    continue
                tasks.append(fetch_rss(src, hours=hours, keywords=keywords, client=client))

            # Google News Search RSS (tìm theo từ khóa - luôn hoạt động)
            if keywords:
                gn_query = "+OR+".join(quote_plus(kw) for kw in keywords)
                gn_source = {
                    "name": "Google News - Search",
                    "url": f"https://news.google.com/rss/search?q={gn_query}&hl=en-US&gl=US&ceid=US:en",
                    "type": "rss",
                    "lang": "en",
                    "category": "Google News Search"
                }
                # Google News Search không cần lọc keywords vì query đã lọc sẵn
                tasks.append(fetch_rss(gn_source, hours=hours, keywords=None, client=client))

            # GDELT
            gdelt_query = " OR ".join(keywords) if keywords else ""
            tasks.append(fetch_gdelt(query=gdelt_query, hours=hours, client=client))

            # Reddit
            for src in SOCIAL_SOURCES:
                if src["type"] == "social" and "reddit" in src["url"]:
                    tasks.append(fetch_reddit(src, hours=hours, keywords=keywords, client=client))

            # Chạy song song
            results_lists = await asyncio.gather(*tasks, return_exceptions=True)

            for i, result in enumerate(results_lists):
                if isinstance(result, Exception):
                    err_msg = str(result)
                    errors.append({"index": i, "type": _classify_error(err_msg), "msg": err_msg[:200]})
                elif isinstance(result, dict):
                    all_results.extend(result.get("articles", []))
                    if result.get("error"):
                        errors.append({"index": i, "type": _classify_error(result["error"]), "msg": result["error"][:200]})
                elif isinstance(result, list):
                    all_results.extend(result)

    finally:
        # Luôn khôi phục proxy
        _restore_proxy()

    # Sắp xếp theo thời gian mới nhất
    all_results.sort(key=lambda x: x.get("published", ""), reverse=True)

    # Loại bỏ trùng lặp theo URL
    seen_urls = set()
    unique_results = []
    for item in all_results:
        url = item.get("url", "")
        if url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(item)

    elapsed = time.time() - start_time

    # Thống kê
    stats = {
        "total_articles": len(unique_results),
        "by_language": {},
        "by_type": {},
        "by_source": {},
        "collection_time_seconds": round(elapsed, 2),
        "time_range_hours": hours,
        "keywords": keywords or [],
        "errors_count": len(errors),
        "errors_summary": {},
    }
    for err in errors:
        t = err.get("type", "OTHER")
        stats["errors_summary"][t] = stats["errors_summary"].get(t, 0) + 1

    for item in unique_results:
        lang = item.get("source_lang_label", "Khác")
        stats["by_language"][lang] = stats["by_language"].get(lang, 0) + 1

        item_type = item.get("type", "news")
        stats["by_type"][item_type] = stats["by_type"].get(item_type, 0) + 1

        src = item.get("source", "Khác")
        stats["by_source"][src] = stats["by_source"].get(src, 0) + 1

    return {
        "articles": unique_results,
        "stats": stats
    }
