# Audience Miner

Find and rank high-fit note creators using public evidence, while keeping platform actions bounded and human-confirmed.

## V0 — Reality-proven mining core

Audience Miner can:

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

## V1 — GitHub operator run

V1 adds a phone-friendly operator surface without adding note action automation.

From GitHub:

1. open **Actions**
2. choose **Mine note audience**
3. tap **Run workflow**
4. enter comma-separated scoring keywords and note hashtags
5. choose a bounded candidate limit: 10 / 20 / 30 / 50
6. open the completed run summary for clickable candidate profiles, or download the generated report artifact

The artifact contains:

- `candidates.csv`
- `candidates.html`
- `candidates.md`

Workflow inputs are passed to Python as environment values and then to the V0 CLI as an argument vector. They are not interpolated into a shell command.

## Local CLI

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

Audience Miner does not include authenticated/private scraping, anti-bot bypass, bulk auto-follow, auto-like, or auto-DM. The HTML/Markdown surfaces open the public profile for human review/action. Public RSS scoring is sequential and operator mode cannot lower the 0.5-second minimum request delay.

See `docs/V0_SPEC.md` for the accepted mining core and `docs/V1_OPERATOR_SPEC.md` for the bounded operator workflow.
