# Audience Miner V1 — Operator Run

Status: `V1 BUILD CLOSED / REALITY GATE`

## Goal

Remove local CLI setup as the next operator bottleneck without widening platform-action authority.

A repository operator should be able to open GitHub Actions from a phone, choose **Mine note audience**, enter topic keywords and note hashtags, and receive:

- a GitHub run summary with clickable candidate profiles
- ranked `candidates.csv`
- mobile review `candidates.html`
- portable `candidates.md`

## Why V1 exists

V0 proved the bounded public hashtag → author → RSS → ranking chain and candidate quality. The next missing capability is operator accessibility, not more discovery complexity.

## Inputs

GitHub `workflow_dispatch` exposes:

- scoring keywords: comma-separated string
- public note hashtags: comma-separated string
- maximum candidates: choice of 10 / 20 / 30 / 50

## Execution boundary

Workflow inputs are passed to Python through environment variables. They are not interpolated into a shell command.

Python constructs an argument vector for the existing V0 CLI and invokes it with `subprocess.run([...], check=True)`.

Operator limits:

- maximum 8 hashtags
- maximum 50 candidates
- minimum RSS request delay 0.5 seconds
- public hashtag discovery remains primary
- existing V0 fail-closed and public-evidence rules remain unchanged

## Output

### GitHub Step Summary

Shows up to 20 ranked candidates with clickable `https://note.com/<handle>` profile links, score, observed active days, and observed posting recency.

### Artifact

`audience-miner-operator-report` contains:

- `candidates.csv`
- `candidates.html`
- `candidates.md`

## Hard boundaries

1. V1 does not automate note follow/like/DM actions.
2. V1 does not add authenticated/private note access.
3. V1 does not weaken V0 request pacing or candidate caps.
4. GitHub operator status/report output is not remote note state.
5. Workflow input must not become shell code.
6. A manual operator run is an explicit action; no scheduled/background harvesting is introduced.

## DA findings

- Direct shell interpolation of workflow inputs creates avoidable command-injection risk.
- A phone workflow that only generates an artifact but no run summary is awkward to inspect.
- Unbounded candidate counts make one-tap operation capable of accidentally creating excessive workload.
- V1 must reuse the V0 truth boundary rather than relabel public posting evidence as login state.

## Counter-DA resolution

V1 is acceptable if:

- inputs cross the workflow boundary as environment values
- execution uses a Python argument vector rather than `shell=True`
- max candidate and tag counts are validated
- request pacing cannot go below V0's bounded default in operator mode
- the workflow produces both GitHub summary and downloadable review files
- the exact PR head passes unit tests and a live PR-triggered operator run using bounded default seeds

## Reality Gate

1. all repository tests pass on exact PR head
2. `Mine note audience` PR-mode workflow completes on exact PR head
3. workflow produces at least 3 candidates
4. workflow uploads all three output files
5. run summary contains clickable note profile links
6. only after 1-5 may V1 merge
