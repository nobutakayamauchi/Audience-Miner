from unittest.mock import patch

from audience_miner.discovery import discover_handles, parse_creator_search_html

HTML = '''
<html><body>
<a href="/search">search</a>
<a href="/alpha_user">Alpha</a>
<a href="https://note.com/beta-user">Beta</a>
<a href="/alpha_user">Alpha duplicate</a>
<a href="/gamma/n/n123">article not profile</a>
<a href="https://example.com/outside">outside</a>
</body></html>
'''


def test_parse_creator_search_html_only_top_level_profiles():
    assert parse_creator_search_html(HTML) == ['alpha_user', 'beta-user']


def test_discovery_dedupes_across_queries_and_caps():
    pages = {
        'AI': '<a href="/alpha"><a href="/beta">',
        'GPTs': '<a href="/beta"><a href="/gamma">',
    }

    def fake_fetch(query: str, size: int = 10, timeout: int = 10) -> str:
        return pages[query]

    with patch('audience_miner.discovery.fetch_creator_search', side_effect=fake_fetch):
        assert discover_handles(['AI', 'GPTs'], max_candidates=2) == ['alpha', 'beta']
