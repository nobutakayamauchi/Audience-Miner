# Provider WATCH

Status: `WATCH / BOUNDED HEALTH CHECK`

Audience Miner depends on public note surfaces that can change without notice. WATCH exists to detect breakage without turning maintenance into background harvesting.

## Schedule

GitHub Actions runs `Watch note providers` once per day at `03:17 UTC` and also supports manual dispatch.

## Probe

WATCH executes only the existing bounded `scripts/live_smoke.py` chain:

- observe whether public creator-search HTML is available or explicitly fail-closed/client-rendered
- observe public hashtag author links
- prove at least one discovered author still exposes parseable public RSS evidence

## Boundary

WATCH does not:

- generate or persist a daily prospect list
- follow, like, or DM users
- use authentication/private data
- bypass anti-bot/rate-limit controls
- retry aggressively
- widen the accepted V0/V1 workload

A failed WATCH run is evidence that a provider assumption changed and should re-open the relevant Ultimate Loop gate before further feature work.
