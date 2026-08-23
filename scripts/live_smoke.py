from audience_miner.core import fetch_rss, parse_feed
from audience_miner.discovery import fetch_creator_search, parse_creator_search_html


def main() -> int:
    search_html = fetch_creator_search('AI', size=10, timeout=15)
    handles = parse_creator_search_html(search_html)
    if not handles:
        raise RuntimeError('public creator search returned no parseable handles')

    feed = parse_feed(fetch_rss('info', timeout=15))
    if not feed:
        raise RuntimeError('public RSS for note official returned no items')

    print(f'LIVE_OK discovery_handles={len(handles)} first={handles[0]} rss_items={len(feed)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
