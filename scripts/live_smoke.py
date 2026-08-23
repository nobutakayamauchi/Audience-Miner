from audience_miner.core import score_candidate
from audience_miner.discovery import (
    DiscoveryUnavailableError,
    discover_handles,
    discover_hashtag_authors,
)


def main() -> int:
    creator_search_state = 'available'
    try:
        creator_handles = discover_handles(['AI副業'], per_query=10, max_candidates=5)
    except DiscoveryUnavailableError:
        creator_search_state = 'fail_closed_client_rendered'
        creator_handles = []

    hashtag_handles = discover_hashtag_authors(['AI副業', '生成AI'], max_candidates=8)
    if not hashtag_handles:
        raise RuntimeError('public hashtag pages returned no parseable author handles')

    scored = None
    score_errors: list[str] = []
    for handle in hashtag_handles[:5]:
        try:
            candidate = score_candidate(handle, ['AI', '生成AI', 'ChatGPT', 'AI副業'])
        except Exception as exc:
            score_errors.append(f'{handle}:{exc}')
            continue
        if candidate.recent_titles:
            scored = candidate
            break

    if scored is None:
        raise RuntimeError(f'no discovered hashtag author produced RSS evidence: {score_errors}')

    print(
        'LIVE_OK '
        f'creator_search={creator_search_state} '
        f'creator_handles={len(creator_handles)} '
        f'hashtag_authors={len(hashtag_handles)} '
        f'scored={scored.handle} '
        f'posts30={scored.activity_30d} '
        f'active_days30={scored.active_days_30d} '
        f'last={scored.days_since_last_post}d'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
