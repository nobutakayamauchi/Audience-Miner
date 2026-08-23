# Audience Miner

Find and rank high-fit note creators using public evidence, while keeping platform actions bounded and human-confirmed.

## V0

Audience Miner can now:

- discover authors exposed on public note hashtag pages (**V0 primary / Reality-proven**)
- best-effort discover creators from note's public creator-search HTML; fail closed when results are client-rendered
- accept explicit note handles/profile URLs
- read public RSS feeds
- estimate observed publishing activity over 30 days
- expose last observed public post recency
- score recent-title keyword/topic fit
- deduplicate candidates across discovery seeds
- pace public RSS requests sequentially
- output ranked CSV
- output a mobile-friendly HTML review report with one-tap profile opening
- locally mark candidates as `フォロー済み` / `除外` without automating the platform action

## Quick run

After installation you can use either `audience-miner` or `python -m audience_miner.cli`.

```bash
audience-miner \
  --keywords "AI,GPTs,生成AI,AI副業,note副業" \
  --tag "AI副業" \
  --tag "生成AI" \
  --tag "ChatGPT" \
  --max-candidates 30 \
  --out candidates.csv \
  --html-out candidates.html
```

You can also add explicit candidates. `--query` remains available as an auxiliary provider, but currently warns and fails closed when note's fetched creator-search HTML does not expose the client-rendered result body.

```bash
audience-miner \
  --keywords "AI,GPTs" \
  --candidate https://note.com/example
```

## Output meaning

- `activity_30d`: RSS posts observed within the last 30 days
- `active_days_30d`: distinct observed publication days within the last 30 days
- `last_observed_post_at`: newest dated item visible in the public RSS evidence
- `days_since_last_post`: recency derived from that observed item
- `activity_score`: V0 activity heuristic; saturates at 20 observed active days
- `topic_score`: supplied keyword coverage in recent observed titles
- `total_score`: 60% activity + 40% topic fit
- `evidence_basis`: currently `public_rss_observed_lower_bound`

RSS may be truncated, so activity counts are lower-bound observations. They are **not private login history**.

## Product boundary

Discovery and ranking are the core product value. Platform actions are replaceable adapters.

V0 does not include authenticated/private scraping, anti-bot bypass, bulk auto-follow, auto-like, or auto-DM. The HTML report opens the public profile for human review/action. Public RSS scoring is sequential and defaults to a 0.5-second delay between candidate requests.

See `docs/V0_SPEC.md` for the frozen scope, Reality finding that changed the provider priority, DA/Counter-DA findings, and the current Reality Gate.
