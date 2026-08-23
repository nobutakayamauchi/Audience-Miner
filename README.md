# Audience Miner

Find and rank high-fit note creators using public evidence, while keeping platform actions bounded and human-confirmed.

## V0

- accepts note creator handles or profile URLs
- reads public RSS feeds
- estimates recent public publishing activity over 30 days
- scores keyword/topic similarity from recent post titles
- outputs ranked CSV

## Run

```bash
python -m audience_miner.cli \
  --keywords "AI,GPTs,AI副業" \
  --candidate https://note.com/example \
  --candidate another_handle \
  --out candidates.csv
```

## Evidence boundary

`activity_30d` is public publishing activity. It is not private login history.

No authenticated/private scraping, anti-bot bypass, bulk auto-follow, auto-like, or auto-DM belongs in the core. Platform actions are replaceable adapters and remain human-confirmed unless an official supported and policy-safe path exists.
