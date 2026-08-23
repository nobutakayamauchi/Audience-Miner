# Audience Miner

Find and rank high-fit note creators using public evidence, while keeping platform actions bounded and human-confirmed.

## V0

Audience Miner can now:

- discover creators from note's public creator search
- discover authors exposed on public hashtag pages
- accept explicit note handles/profile URLs
- read public RSS feeds
- estimate observed publishing activity over 30 days
- score recent-title keyword/topic fit
- deduplicate candidates across discovery seeds
- output ranked CSV
- output a mobile-friendly HTML review report with one-tap profile opening

## Quick run

```bash
python -m audience_miner.cli \
  --keywords "AI,GPTs,AI副業,note副業" \
  --query "AI副業" \
  --query "GPTs" \
  --tag "AI" \
  --tag "AI副業" \
  --max-candidates 30 \
  --out candidates.csv \
  --html-out candidates.html
```

You can also add explicit candidates:

```bash
python -m audience_miner.cli \
  --keywords "AI,GPTs" \
  --candidate https://note.com/example
```

## Output meaning

- `activity_30d`: RSS posts observed within the last 30 days
- `active_days_30d`: distinct observed publication days within the last 30 days
- `activity_score`: V0 activity heuristic; saturates at 20 observed active days
- `topic_score`: supplied keyword coverage in recent observed titles
- `total_score`: 60% activity + 40% topic fit
- `evidence_basis`: currently `public_rss_observed_lower_bound`

RSS may be truncated, so activity counts are lower-bound observations. They are **not private login history**.

## Product boundary

Discovery and ranking are the core product value. Platform actions are replaceable adapters.

V0 does not include authenticated/private scraping, anti-bot bypass, bulk auto-follow, auto-like, or auto-DM. The HTML report opens the public profile for human review/action.

See `docs/V0_SPEC.md` for the frozen scope, DA/Counter-DA findings, and Reality Gate.
