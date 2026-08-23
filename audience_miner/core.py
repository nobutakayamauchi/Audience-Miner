from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
import re
import urllib.request
import xml.etree.ElementTree as ET


@dataclass
class CandidateScore:
    handle: str
    profile_url: str
    activity_30d: int
    active_days_30d: int
    activity_score: float
    topic_score: float
    total_score: float
    recent_titles: str


def normalize_handle(value: str) -> str:
    value = value.strip().rstrip('/')
    m = re.search(r"note\.com/([^/?#]+)", value)
    if m:
        return m.group(1)
    return value.lstrip('@')


def fetch_rss(handle: str, timeout: int = 10) -> bytes:
    url = f"https://note.com/{handle}/rss"
    req = urllib.request.Request(url, headers={"User-Agent": "AudienceMiner/0.1 (+human-reviewed research tool)"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _item_text(item: ET.Element, tag: str) -> str:
    node = item.find(tag)
    return (node.text or '').strip() if node is not None else ''


def parse_feed(xml_bytes: bytes) -> list[tuple[str, datetime | None]]:
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall('.//item'):
        title = _item_text(item, 'title')
        raw_date = _item_text(item, 'pubDate')
        dt = None
        if raw_date:
            try:
                dt = parsedate_to_datetime(raw_date)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
            except (TypeError, ValueError):
                dt = None
        items.append((title, dt))
    return items


def score_candidate(value: str, keywords: list[str], now: datetime | None = None) -> CandidateScore:
    handle = normalize_handle(value)
    profile_url = f"https://note.com/{handle}"
    now = now or datetime.now(timezone.utc)
    items = parse_feed(fetch_rss(handle))
    cutoff = now - timedelta(days=30)
    recent = [(title, dt) for title, dt in items if dt and dt.astimezone(timezone.utc) >= cutoff]
    activity_30d = len(recent)
    active_days_30d = len({dt.astimezone(timezone.utc).date() for _, dt in recent if dt})
    activity_score = min(100.0, (active_days_30d / 20.0) * 100.0)

    normalized_keywords = [k.casefold().strip() for k in keywords if k.strip()]
    titles = [title for title, _ in items[:20]]
    haystack = ' '.join(titles).casefold()
    matched = sum(1 for k in normalized_keywords if k in haystack)
    topic_score = 0.0 if not normalized_keywords else (matched / len(normalized_keywords)) * 100.0
    total_score = round(activity_score * 0.6 + topic_score * 0.4, 2)
    return CandidateScore(handle, profile_url, activity_30d, active_days_30d, round(activity_score, 2), round(topic_score, 2), total_score, ' | '.join(titles[:5]))
