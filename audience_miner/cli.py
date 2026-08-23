from __future__ import annotations
import argparse, csv, sys
from audience_miner.core import score_candidate

def main() -> int:
    p = argparse.ArgumentParser(description='Rank note creator candidates by public activity and topic fit.')
    p.add_argument('--keywords', required=True)
    p.add_argument('--candidate', action='append', required=True)
    p.add_argument('--out', default='candidates.csv')
    args = p.parse_args()
    keywords = [x.strip() for x in args.keywords.split(',') if x.strip()]
    rows = []
    for candidate in args.candidate:
        try:
            rows.append(score_candidate(candidate, keywords))
        except Exception as exc:
            print(f'WARN {candidate}: {exc}', file=sys.stderr)
    rows.sort(key=lambda r: r.total_score, reverse=True)
    fields = ['handle','profile_url','activity_30d','active_days_30d','activity_score','topic_score','total_score','recent_titles']
    with open(args.out, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for row in rows: w.writerow({name: getattr(row, name) for name in fields})
    for row in rows:
        print(f'{row.total_score:6.2f} {row.handle:24} active_days30={row.active_days_30d:2d} posts30={row.activity_30d:2d}')
    print(f'Wrote {len(rows)} candidates to {args.out}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
