# Audience Miner V0 — Frozen Scope

Status: `V0 BUILD + REALITY GATE`

## Raison d'être

Reduce the human cost of finding likely high-fit note creators who are publicly active enough to be worth reviewing for relationship-building, audience development, or future sales-network outreach.

## Observable truth

Audience Miner does **not** know private login history.

V0 may observe only public evidence:

- creator-search results exposed by note's public search UI
- authors exposed on public hashtag pages
- public creator RSS publication timestamps and titles

Therefore:

- `activity_30d` = RSS items observed in the last 30 days
- `active_days_30d` = distinct publication days observed in RSS in the last 30 days
- both are lower-bound public observations because RSS may be truncated
- neither value may be described as login frequency

## V0 input

At least one of:

- explicit note creator handle/profile URL
- creator-search query
- public hashtag

Plus scoring keywords.

## V0 output

- ranked CSV
- mobile-friendly HTML review report
- handle/profile URL
- observed posts in 30 days
- observed active publication days in 30 days
- heuristic activity score
- recent-title keyword fit score
- combined score
- recent public title evidence
- explicit evidence basis

## Discovery providers

### NOTE_PUBLIC_CREATOR_SEARCH

Uses the public `note.com/search?context=user` user-facing search surface.

### NOTE_PUBLIC_HASHTAG

Uses public `note.com/hashtag/<tag>` pages and extracts top-level creator profile links exposed in the returned page.

Both providers are replaceable adapters. HTML layout is not treated as a stable API contract.

## Bounded workload

- max 8 creator-search queries per run
- max 8 hashtags per run
- max 100 discovered candidates per provider
- sequential public requests
- no authenticated session required
- no retry storm / anti-bot bypass

## Scoring heuristic

`activity_score` saturates at 20 distinct observed publication days in the preceding 30 days.

`topic_score` is the fraction of supplied keywords found in the most recent observed titles.

`total_score = 0.6 * activity_score + 0.4 * topic_score`.

These weights are a V0 product heuristic, not a claim about conversion probability.

## Hard boundaries

1. No private/authenticated data extraction.
2. No claim that publishing activity proves login frequency.
3. No anti-bot, CAPTCHA, rate-limit, or authentication bypass.
4. No bulk auto-follow, auto-like, auto-DM, or follow-back automation in core.
5. No hidden unofficial API dependency when a public user-facing surface is sufficient.
6. Discovery adapter failure must not silently fabricate candidates.
7. Platform actions remain human-confirmed and replaceable.
8. Audience signal is not Affiliate/Seller authority in Sales Distribution Network.

## DA findings

- Creator search alone misses people whose profile does not describe the niche.
- Hashtag author discovery adds content-based coverage without private access.
- RSS can undercount active days due to feed truncation.
- Search/tag HTML can change without notice.
- Duplicate creators occur across multiple discovery seeds.
- Naive bulk action would create policy/platform-account risk and couple product value to one platform action.

## Counter-DA resolution

V0 is acceptable if:

- discovery sources stay public and bounded
- duplicate handles are removed
- all activity values are labeled public observed lower bounds
- parsers fail closed
- live smoke proves public creator search + hashtag author extraction + RSS scoring on the exact PR head
- ranking usefulness is judged by human Dogfood before adding richer scoring or action automation

## Reality Gate

Code GREEN is not product PASS.

Required evidence:

1. unit tests pass on exact PR head
2. live public smoke passes on exact PR head
3. bounded real niche run produces candidates
4. human review confirms useful prospects appear near the top often enough to justify further work
5. only then consider V0 merge / V1 expansion
