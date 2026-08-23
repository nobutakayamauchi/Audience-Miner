# Audience Miner V0 — Frozen Scope

Status: `V0 REALITY-ADAPTED / BUILD CLOSED AFTER FIX`

## Raison d'être

Reduce the human cost of finding likely high-fit note creators who are publicly active enough to be worth reviewing for relationship-building, audience development, or future sales-network outreach.

## Observable truth

Audience Miner does **not** know private login history.

V0 may observe only public evidence:

- creator profile links actually exposed in fetched public HTML
- authors exposed on public hashtag pages
- public creator RSS publication timestamps and titles

Therefore:

- `activity_30d` = RSS items observed in the last 30 days
- `active_days_30d` = distinct publication days observed in RSS in the last 30 days
- `last_observed_post_at` = newest dated item visible in that RSS evidence
- `days_since_last_post` = recency derived from the newest observed item
- all activity values are lower-bound public observations because RSS may be truncated
- none of these values may be described as login history/frequency

## V0 input

At least one of:

- explicit note creator handle/profile URL
- public hashtag (V0 primary discovery path)
- creator-search query (best-effort auxiliary provider; fail-closed when result bodies are client-rendered)

Plus scoring keywords.

## V0 output

- ranked CSV
- mobile-friendly HTML review report
- handle/profile URL
- observed posts in 30 days
- observed active publication days in 30 days
- newest observed post and recency
- heuristic activity score
- recent-title keyword fit score
- combined score
- recent public title evidence
- explicit evidence basis
- local browser review status (`フォロー済み` / `除外`) without performing the platform action

## Discovery providers

### NOTE_PUBLIC_HASHTAG — V0 PRIMARY / REALITY PROVEN

Uses public `note.com/hashtag/<tag>` pages and extracts top-level creator profile links exposed in the returned page.

The first bounded Reality run on 2026-08-23 produced six scored real candidates through this path and successfully stored CSV/HTML evidence.

### NOTE_PUBLIC_CREATOR_SEARCH — AUXILIARY / FAIL-CLOSED

Uses the public `note.com/search?context=user` user-facing search surface only when creator profile links are actually exposed in fetched HTML.

Reality finding on 2026-08-23: the fetched unauthenticated search HTML exposed navigation (`/trend`) but not the client-rendered creator result body. V0 therefore filters reserved navigation routes and raises `DiscoveryUnavailableError` when no real profile links remain. It must never fabricate a successful search result from navigation links.

Both providers are replaceable adapters. HTML layout is not treated as a stable API contract.

## Bounded workload

- max 8 creator-search queries per run
- max 8 hashtags per run
- max 100 discovered candidates per provider
- sequential public requests
- default 0.5-second delay between per-candidate RSS requests
- no authenticated session required
- no automatic retry storm / anti-bot bypass

## Scoring heuristic

`activity_score` saturates at 20 distinct observed publication days in the preceding 30 days.

`topic_score` is the fraction of supplied keywords found in the most recent observed titles.

`total_score = 0.6 * activity_score + 0.4 * topic_score`.

Recency is exposed separately for human judgment in V0 rather than silently pretending it is private session activity. These weights are a V0 product heuristic, not a claim about conversion probability.

## Hard boundaries

1. No private/authenticated data extraction.
2. No claim that publishing activity proves login frequency.
3. No anti-bot, CAPTCHA, rate-limit, or authentication bypass.
4. No bulk auto-follow, auto-like, auto-DM, or follow-back automation in core.
5. No hidden unofficial API dependency when a public user-facing surface is sufficient.
6. Discovery adapter failure must fail closed rather than silently fabricate candidates.
7. Platform actions remain human-confirmed and replaceable.
8. Audience signal is not Affiliate/Seller authority in Sales Distribution Network.
9. A local `フォロー済み` mark records the operator's review state only; it is not proof of remote note state.

## DA findings

- Creator search alone misses people whose profile does not describe the niche.
- Current unauthenticated creator-search result bodies can be client-rendered and absent from fetched HTML.
- Hashtag author discovery provides content-based coverage and is Reality-proven without private access.
- RSS can undercount active days due to feed truncation.
- A 30-day count alone can hide that someone stopped publishing recently, so V0 exposes posting recency explicitly.
- Search/tag HTML can change without notice.
- Duplicate creators occur across multiple discovery seeds.
- Naive bulk action would create policy/platform-account risk and couple product value to one platform action.

## Counter-DA resolution

V0 is acceptable if:

- hashtag discovery remains the primary V0 discovery path while creator search is unavailable
- creator search fails closed when its result body is not observable
- discovery sources stay public and bounded
- duplicate handles are removed
- all activity values are labeled public observed lower bounds
- parsers fail closed
- live smoke proves hashtag author extraction + RSS scoring on the exact PR head and reports creator-search availability state
- bounded Dogfood produces real candidates and an inspectable CSV/HTML artifact
- ranking usefulness is judged by human Dogfood before adding richer scoring or action automation

## Reality Gate

Code GREEN is not product PASS.

Required evidence:

1. unit tests pass on exact PR head
2. live public smoke passes on exact PR head, including explicit creator-search availability/fail-closed state
3. bounded real niche hashtag run produces at least 3 scored candidates and stores its CSV/HTML evidence
4. human review confirms useful prospects appear near the top often enough to justify further work
5. only then consider V0 merge / V1 expansion
