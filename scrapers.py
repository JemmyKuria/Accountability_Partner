"""
scrapers.py
-----------
Job-board scrapers for the Job Hunt feature.

Each `search_*` function returns a list of dicts with the same shape:
    {
        "title": str,
        "company": str,
        "location": str,
        "url": str,
        "source": str,
        "snippet": str,
        "posted_date": date | None,
    }

Sources:
    - Fuzu (Kenya)                 role-based search URLs, no auth needed
    - BrighterMonday Kenya         category + general listing pages
    - Corporate Staffing Services  role "tag" pages
    - RemoteOK                     free public JSON API, remote tech roles

Nothing here touches Supabase or Streamlit — this module is pure data.
"""

import re
from datetime import date, timedelta
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}
REQUEST_TIMEOUT = 12


# --------------------------------------------------------------------------
# Date parsing
# --------------------------------------------------------------------------
MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}

_ISO_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
_MDY_RE = re.compile(
    r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+"
    r"(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})",
    re.I,
)
_DMY_RE = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)?\s+"
    r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?,?\s+(\d{4})",
    re.I,
)
_REL_DAYS_RE = re.compile(r"\b(\d+)\s*(?:day|days)\s*ago", re.I)
_REL_WEEKS_RE = re.compile(r"\b(\d+)\s*(?:week|weeks)\s*ago", re.I)
_REL_MONTHS_RE = re.compile(r"\b(\d+)\s*(?:month|months)\s*ago", re.I)


def _month_from_token(tok: str):
    tok = tok.lower()
    return MONTH_MAP.get(tok[:4]) or MONTH_MAP.get(tok[:3])


def parse_posted_date(text: str):
    """Return a date if we can find one in `text`, else None."""
    if not text:
        return None
    today = date.today()
    low = text.lower()

    if re.search(r"\b(today|just posted|few hours ago|hours ago|minutes ago)\b", low):
        return today
    if "yesterday" in low:
        return today - timedelta(days=1)

    m = _REL_DAYS_RE.search(low)
    if m:
        return today - timedelta(days=int(m.group(1)))
    m = _REL_WEEKS_RE.search(low)
    if m:
        return today - timedelta(weeks=int(m.group(1)))
    m = _REL_MONTHS_RE.search(low)
    if m:
        return today - timedelta(days=30 * int(m.group(1)))
    if re.search(r"\ba\s+month\s+ago", low):
        return today - timedelta(days=30)
    if re.search(r"\ba\s+week\s+ago", low):
        return today - timedelta(weeks=1)

    m = _ISO_RE.search(text)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass

    m = _MDY_RE.search(text)
    if m:
        mon = _month_from_token(m.group(1))
        if mon:
            try:
                return date(int(m.group(3)), mon, int(m.group(2)))
            except ValueError:
                pass

    m = _DMY_RE.search(text)
    if m:
        mon = _month_from_token(m.group(2))
        if mon:
            try:
                return date(int(m.group(3)), mon, int(m.group(1)))
            except ValueError:
                pass

    return None


# --------------------------------------------------------------------------
# Shared helpers
# --------------------------------------------------------------------------

def _slugify(keyword: str) -> str:
    return re.sub(r"\s+", "-", keyword.strip().lower())


def _container_text(link) -> str:
    """Walk up to a plausible card wrapper and return its text — the date
    usually lives in a sibling of the title anchor, not inside it."""
    container = (
        link.find_parent("article")
        or link.find_parent("div", class_=re.compile(r"post|entry|job|listing|card", re.I))
        or link.find_parent()
    )
    return container.get_text(" ", strip=True) if container else ""


def _dedupe(results: list) -> list:
    """URL dedupe first, then a conservative title+company pass."""
    seen_urls, seen_pairs, unique = set(), set(), []
    for r in results:
        url_key = r["url"].split("?")[0].rstrip("/").lower()
        if url_key in seen_urls:
            continue
        company = (r.get("company") or "").strip().lower()
        title_norm = re.sub(r"\W+", "", r["title"].lower())
        pair = (title_norm, company)
        if company and title_norm and pair in seen_pairs:
            continue
        seen_urls.add(url_key)
        if company:
            seen_pairs.add(pair)
        unique.append(r)
    return unique


# --------------------------------------------------------------------------
# Scrapers
# --------------------------------------------------------------------------

def search_fuzu(keyword: str, max_pages: int = 2) -> list:
    results = []
    for page in range(1, max_pages + 1):
        url = f"https://www.fuzu.com/kenya/jobs?q={quote(keyword)}&page={page}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        links = soup.find_all("a", href=re.compile(r"/kenya/job/"))
        if not links:
            break
        for link in links:
            title = link.get_text(strip=True)
            href = link.get("href", "")
            if not title or len(title) < 3:
                continue
            full_url = href if href.startswith("http") else f"https://www.fuzu.com{href}"
            container_text = _container_text(link)
            results.append({
                "title": title,
                "company": "",
                "location": "Kenya",
                "url": full_url,
                "source": "Fuzu",
                "snippet": container_text[:300],
                "posted_date": parse_posted_date(container_text),
            })
    return _dedupe(results)


def search_brightermonday(keyword: str, max_pages: int = 2) -> list:
    results = []
    for page in range(1, max_pages + 1):
        url = f"https://www.brightermonday.co.ke/jobs?q={quote(keyword)}&page={page}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        links = soup.find_all("a", href=re.compile(r"/listings/[a-z0-9\-]+"))
        if not links:
            break
        for link in links:
            title = link.get_text(strip=True)
            href = link.get("href", "")
            if not title or len(title) < 3:
                continue
            full_url = href if href.startswith("http") else f"https://www.brightermonday.co.ke{href}"
            container_text = _container_text(link)
            results.append({
                "title": title,
                "company": "",
                "location": "Kenya",
                "url": full_url,
                "source": "BrighterMonday",
                "snippet": container_text[:300],
                "posted_date": parse_posted_date(container_text),
            })
    return _dedupe(results)


def search_corporate_staffing(keyword: str) -> list:
    results = []
    slug = _slugify(keyword)
    url = f"https://www.corporatestaffing.co.ke/tag/{quote(slug)}-jobs-in-kenya/"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException:
        return results
    soup = BeautifulSoup(resp.text, "html.parser")
    links = soup.select("h2 a, h3 a, .entry-title a")
    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href", "")
        if not title or not href:
            continue
        container_text = _container_text(link)
        results.append({
            "title": title,
            "company": "",
            "location": "Kenya",
            "url": href,
            "source": "Corporate Staffing",
            "snippet": container_text[:300],
            "posted_date": parse_posted_date(container_text),
        })
    return _dedupe(results)


def search_remoteok(keyword: str) -> list:
    results = []
    try:
        resp = requests.get("https://remoteok.com/api", headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError):
        return results

    keyword_lower = keyword.lower()
    for item in data:
        if not isinstance(item, dict) or "position" not in item:
            continue
        haystack = " ".join([
            item.get("position", ""),
            item.get("description", ""),
            " ".join(item.get("tags", [])),
        ]).lower()
        if keyword_lower in haystack:
            results.append({
                "title": item.get("position", "Untitled"),
                "company": item.get("company", ""),
                "location": "Remote",
                "url": "https://remoteok.com" + item.get("url", ""),
                "source": "RemoteOK",
                "snippet": (item.get("description", "") or "")[:300],
                "posted_date": parse_posted_date(item.get("date", "")),
            })
    return _dedupe(results)


def search_all(keyword: str, sources: dict, max_pages: int = 2) -> list:
    """Run the selected sources for one keyword and return a merged, deduped list.

    `sources` is a dict like:
        {"fuzu": True, "brightermonday": True, "corporate_staffing": True, "remoteok": True}
    """
    jobs = []
    if sources.get("fuzu"):
        jobs.extend(search_fuzu(keyword, max_pages=max_pages))
    if sources.get("brightermonday"):
        jobs.extend(search_brightermonday(keyword, max_pages=max_pages))
    if sources.get("corporate_staffing"):
        jobs.extend(search_corporate_staffing(keyword))
    if sources.get("remoteok"):
        jobs.extend(search_remoteok(keyword))
    return _dedupe(jobs)


# --------------------------------------------------------------------------
# Single-job scrape (used by the tracker when you paste a URL)
# --------------------------------------------------------------------------

def detect_platform(url: str) -> str:
    low = url.lower()
    if "fuzu" in low: return "Fuzu"
    if "brightermonday" in low: return "BrighterMonday"
    if "corporatestaffing" in low: return "Corporate Staffing"
    if "remoteok" in low: return "RemoteOK"
    if "linkedin" in low: return "LinkedIn"
    return "Unknown"


def scrape_single_job(url: str) -> dict:
    """Best-effort scrape of a single job URL. Returns platform, company,
    position. Falls back gracefully to empty strings on failure so the UI
    can prompt the user to type them in manually."""
    platform = detect_platform(url)
    company, position = "", ""

    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.find("h1") or soup.find("title")
        if title_tag:
            position = title_tag.get_text(strip=True)

        comp_tag = soup.find("div", class_=re.compile(r"company|employer", re.I))
        if comp_tag:
            company = comp_tag.get_text(strip=True)
        elif " at " in position:
            parts = position.split(" at ", 1)
            position = parts[0].strip()
            company = parts[1].split("|")[0].strip()
    except Exception:
        pass

    return {"platform": platform, "company": company, "position": position}