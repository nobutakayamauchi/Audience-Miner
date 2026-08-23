from audience_miner.core import score_candidate
from audience_miner.discovery import discover_handles, discover_hashtag_authors


def main() -> int:
    creator_handles = discover_handles(['note公式'], per_query=10, max_candidates=10)
    if 'info' not in {h.casefold() for h in creator_handles}:
        raise RuntimeError(f'expected note official handle in public creator search, got: {creator_handles}')

    hashtag_handles = discover_hashtag_authors(['AI'], max_candidates=10)
    if not hashtag_handles:
        raise RuntimeError('public #AI page returned no parseable author handles')

    row = score_candidate('info', ['note'])
    if not row.recent_titles:
        raise RuntimeError('public RSS scoring returned no title evidence for note official')

    print(
        'LIVE_OK '
        f'creator_search={len(creator_handles)} '
        f'hashtag_authors={len(hashtag_handles)} '
        f'info_posts30={row.activity_30d} '
        f'info_active_days30={row.active_days_30d}'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
