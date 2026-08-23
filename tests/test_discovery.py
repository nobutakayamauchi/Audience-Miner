from unittest.mock import patch

import pytest

from audience_miner.discovery import (
    DiscoveryUnavailableError,
    discover_handles,
    discover_hashtag_authors,
    parse_creator_search_html,
)

HTML = '''
<html><body>
<a href="/search">search</a>
<a href="/trend">trend nav</a>
<a href="/alpha_user">Alpha</a>
<a href="https://note.com/beta-user">Beta</a>
<a href="/tracked_user?ref=search">Tracked</a>
<a href="/alpha_user">Alpha duplicate</a>
<a href="/gamma/n/n123">article not profile</a>
<a href="/hashtag/AI">tag path not profile</a>
<a href="https://example.com/outside">outside</a>
</body></html>
'''


def test_parse_creator_search_html_only_top_level_profiles():
    assert parse_creator_search_html(HTML) == ['alpha_user', 'beta-user', 'tracked_user']


def test_discovery_dedupes_across_queries_and_caps():
    pages = {
        'AI': '<a href="/alpha"><a href="/beta">',
        'GPTs': '<a href="/beta"><a href="/gamma">',
    }

    def fake_fetch(query: str, size: int = 10, timeout: int = 10) -> str:
        return pages[query]

    with patch('audience_miner.discovery.fetch_creator_search', side_effect=fake_fetch):
        assert discover_handles(['AI', 'GPTs'], max_candidates=2) == ['alpha', 'beta']


def test_creator_search_fails_closed_when_only_navigation_links_are_visible():
    with patch('audience_miner.discovery.fetch_creator_search', return_value='<a href="/trend">'):
        with pytest.raises(DiscoveryUnavailableError):
            discover_handles(['AI副業'])


def test_hashtag_discovery_dedupes_authors():
    pages = {
        'AI': '<a href="/author_a"><a href="/author_b/n/n123"><a href="/author_b">',
        'AI副業': '<a href="/author_b"><a href="/author_c">',
    }

    with patch('audience_miner.discovery.fetch_hashtag_page', side_effect=lambda tag: pages[tag]):
        assert discover_hashtag_authors(['#AI', 'AI副業']) == ['author_a', 'author_b', 'author_c']
