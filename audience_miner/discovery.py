from __future__ import annotations

from html.parser import HTMLParser
from urllib.parse import urlencode, urlparse
import urllib.request

MAX_QUERIES = 8
MAX_CANDIDATES = 100

_RESERVED_TOP_LEVEL = {
    '', 'search', 'login', 'signup', 'register', 'terms', 'help', 'premium',
    'pro', 'about', 'pricing', 'hashtag', 'magazines', 'membership', 'memberships',
    'notifications', 'settings', 'account', 'explore', 'ranking', 'topics', 'categories',
}


class _ProfileLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.handles: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != 'a':
            return
        href = dict(attrs).get('href')
        if not href:
            return
        handle = _profile_handle_from_href(href)
        if handle and handle not in self.handles:
            self.handles.append(handle)


def _profile_handle_from_href(href: str) -> str | None:
    if href.startswith('/'):
        path = href
    else:
        parsed = urlparse(href)
        if parsed.netloc not in {'note.com', 'www.note.com'}:
            return None
        path = parsed.path
    parts = [part for part in path.split('/') if part]
    if len(parts) != 1:
        return None
    handle = parts[0]
    if handle.casefold() in _RESERVED_TOP_LEVEL:
        return None
    if not all(ch.isalnum() or ch in {'_', '-'} for ch in handle):
        return None
    return handle


def parse_creator_search_html(html: str) -> list[str]:
    parser = _ProfileLinkParser()
    parser.feed(html)
    return parser.handles


def fetch_creator_search(query: str, size: int = 10, timeout: int = 10) -> str:
    size = max(1, min(size, 50))
    qs = urlencode({'context': 'user', 'q': query, 'size': size})
    url = f'https://note.com/search?{qs}'
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'AudienceMiner/0.1 (+human-reviewed public discovery tool)'},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode('utf-8', errors='replace')


def discover_handles(
    queries: list[str],
    *,
    per_query: int = 10,
    max_candidates: int = 50,
) -> list[str]:
    clean_queries = [q.strip() for q in queries if q.strip()][:MAX_QUERIES]
    limit = max(1, min(max_candidates, MAX_CANDIDATES))
    seen: set[str] = set()
    ordered: list[str] = []
    for query in clean_queries:
        html = fetch_creator_search(query, size=per_query)
        for handle in parse_creator_search_html(html):
            key = handle.casefold()
            if key in seen:
                continue
            seen.add(key)
            ordered.append(handle)
            if len(ordered) >= limit:
                return ordered
    return ordered
