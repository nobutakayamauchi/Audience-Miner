from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from audience_miner.core import normalize_handle, parse_feed, score_candidate

FEED = b'''<?xml version="1.0"?><rss><channel>
<item><title>AI GPTs workflow</title><pubDate>Sun, 23 Aug 2026 01:00:00 +0000</pubDate></item>
<item><title>AI sales</title><pubDate>Sat, 22 Aug 2026 01:00:00 +0000</pubDate></item>
</channel></rss>'''


def test_normalize_handle():
    assert normalize_handle('https://note.com/example/') == 'example'
    assert normalize_handle('@example') == 'example'


def test_normalize_handle_rejects_path_like_input():
    with pytest.raises(ValueError):
        normalize_handle('../../other')


def test_parse_feed():
    items = parse_feed(FEED)
    assert items[0][0] == 'AI GPTs workflow'
    assert items[0][1] == datetime(2026, 8, 23, 1, 0, tzinfo=timezone.utc)


def test_score_uses_distinct_public_active_days_and_recency():
    with patch('audience_miner.core.fetch_rss', return_value=FEED):
        row = score_candidate(
            'example',
            ['AI', 'GPTs'],
            now=datetime(2026, 8, 23, 5, tzinfo=timezone.utc),
        )
    assert row.activity_30d == 2
    assert row.active_days_30d == 2
    assert row.last_observed_post_at == '2026-08-23T01:00:00+00:00'
    assert row.days_since_last_post == 0
    assert row.topic_score == 100.0
    assert row.evidence_basis == 'public_rss_observed_lower_bound'
