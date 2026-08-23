from __future__ import annotations

import argparse
import csv
import sys

from audience_miner.core import score_candidate
from audience_miner.discovery import discover_handles, discover_hashtag_authors
from audience_miner.report import write_html_report


def main() -> int:
    p = argparse.ArgumentParser(description='Discover and rank note creators by public activity and topic fit.')
    p.add_argument('--keywords', required=True, help='Comma-separated scoring keywords')
    p.add_argument('--query', action='append', default=[], help='Public note creator-search query; repeatable')
    p.add_argument('--tag', action='append', default=[], help='Public note hashtag used to discover article authors; repeatable')
    p.add_argument('--candidate', action='append', default=[], help='Explicit note handle/profile URL; repeatable')
    p.add_argument('--per-query', type=int, default=10, help='Requested public search results per query (1-50)')
    p.add_argument('--max-candidates', type=int, default=50, help='Hard cap per discovery provider (1-100)')
    p.add_argument('--out', default='candidates.csv', help='CSV output path')
    p.add_argument('--html-out', default='candidates.html', help='Mobile-friendly human review report path')
    args = p.parse_args()

    if not args.query and not args.tag and not args.candidate:
        p.error('provide at least one --query, --tag, or --candidate')

    keywords = [x.strip() for x in args.keywords.split(',') if x.strip()]
    candidates = list(args.candidate)

    if args.query:
        try:
            candidates.extend(
                discover_handles(
                    args.query,
                    per_query=args.per_query,
                    max_candidates=args.max_candidates,
                )
            )
        except Exception as exc:
            print(f'WARN public creator discovery failed: {exc}', file=sys.stderr)

    if args.tag:
        try:
            candidates.extend(
                discover_hashtag_authors(
                    args.tag,
                    max_candidates=args.max_candidates,
                )
            )
        except Exception as exc:
            print(f'WARN public hashtag discovery failed: {exc}', file=sys.stderr)

    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = candidate.strip().casefold().rstrip('/')
        if key and key not in seen:
            seen.add(key)
            deduped.append(candidate)

    rows = []
    for candidate in deduped:
        try:
            rows.append(score_candidate(candidate, keywords))
        except Exception as exc:
            print(f'WARN {candidate}: {exc}', file=sys.stderr)

    rows.sort(key=lambda r: r.total_score, reverse=True)
    fields = [
        'handle', 'profile_url', 'activity_30d', 'active_days_30d',
        'activity_score', 'topic_score', 'total_score', 'evidence_basis',
        'recent_titles',
    ]
    with open(args.out, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({name: getattr(row, name) for name in fields})

    if args.html_out:
        write_html_report(rows, args.html_out)

    for row in rows:
        print(
            f'{row.total_score:6.2f} {row.handle:24} '
            f'active_days30={row.active_days_30d:2d} posts30={row.activity_30d:2d}'
        )
    print(f'Wrote {len(rows)} candidates to {args.out}')
    if args.html_out:
        print(f'Wrote review report to {args.html_out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
