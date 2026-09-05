# AGENTS.md

## Repository role
Audience Miner discovers and ranks high-fit note creators from public evidence while keeping platform actions human-controlled.

## Load order
1. Read `README.md` for current V0/V1 behavior and limitations.
2. Read only the implementation or workflow files needed for the task.
3. Load generated candidate artifacts only when validating a specific run.

## Source of truth
- Current code and workflow definitions on the default branch are authoritative.
- Public-source observations are evidence, not guaranteed truth.

## Context budget
- Do not crawl or ingest large public result sets unless the task explicitly needs them.
- Prefer bounded candidate sets and targeted source reads.
- Do not re-read generated CSV/HTML/Markdown artifacts unless they are relevant to the active run.

## Human gates
- AI may discover, score, deduplicate, summarize, and prepare review outputs.
- Following, messaging, publishing, purchasing, account mutation, or other platform actions require explicit human approval.

## Stop conditions
Fail closed when source pages do not expose reliable data, evidence is ambiguous, or the requested action would exceed the bounded public-evidence workflow.