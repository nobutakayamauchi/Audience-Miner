from __future__ import annotations

from dataclasses import dataclass
import csv
import os
from pathlib import Path
import subprocess
import sys

MAX_OPERATOR_TAGS = 8
MAX_OPERATOR_CANDIDATES = 50
MIN_OPERATOR_DELAY = 0.5


@dataclass(frozen=True)
class OperatorConfig:
    keywords: str
    tags: tuple[str, ...]
    max_candidates: int
    request_delay: float = MIN_OPERATOR_DELAY


def _split_tags(value: str) -> tuple[str, ...]:
    tags: list[str] = []
    seen: set[str] = set()
    for raw in value.split(','):
        tag = raw.strip().lstrip('#')
        if not tag:
            continue
        if len(tag) > 80:
            raise ValueError('each tag must be <= 80 characters')
        key = tag.casefold()
        if key in seen:
            continue
        seen.add(key)
        tags.append(tag)
        if len(tags) >= MAX_OPERATOR_TAGS:
            break
    return tuple(tags)


def config_from_env(env: dict[str, str] | None = None) -> OperatorConfig:
    source = os.environ if env is None else env
    keywords = source.get('AUDIENCE_KEYWORDS', '').strip()
    if not keywords:
        raise ValueError('AUDIENCE_KEYWORDS must not be empty')
    if len(keywords) > 500:
        raise ValueError('AUDIENCE_KEYWORDS must be <= 500 characters')

    tags = _split_tags(source.get('AUDIENCE_TAGS', ''))
    if not tags:
        raise ValueError('AUDIENCE_TAGS must contain at least one tag')

    raw_max = source.get('AUDIENCE_MAX_CANDIDATES', '20').strip()
    try:
        max_candidates = int(raw_max)
    except ValueError as exc:
        raise ValueError('AUDIENCE_MAX_CANDIDATES must be an integer') from exc
    if not 1 <= max_candidates <= MAX_OPERATOR_CANDIDATES:
        raise ValueError(f'AUDIENCE_MAX_CANDIDATES must be 1-{MAX_OPERATOR_CANDIDATES}')

    return OperatorConfig(
        keywords=keywords,
        tags=tags,
        max_candidates=max_candidates,
    )


def build_cli_command(
    config: OperatorConfig,
    *,
    csv_path: str = 'candidates.csv',
    html_path: str = 'candidates.html',
) -> list[str]:
    command = [
        sys.executable,
        '-m',
        'audience_miner.cli',
        '--keywords',
        config.keywords,
        '--max-candidates',
        str(config.max_candidates),
        '--request-delay',
        str(max(MIN_OPERATOR_DELAY, config.request_delay)),
        '--out',
        csv_path,
        '--html-out',
        html_path,
    ]
    for tag in config.tags:
        command.extend(['--tag', tag])
    return command


def run_operator(config: OperatorConfig) -> None:
    subprocess.run(build_cli_command(config), check=True)


def render_markdown_summary(csv_path: str = 'candidates.csv', *, limit: int = 20) -> str:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(csv_path)

    with path.open(newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    lines = [
        '# Audience Miner result',
        '',
        f'候補: **{len(rows)}件**',
        '',
        '| # | creator | score | 30日活動日 | 最終観測 |',
        '|---:|---|---:|---:|---:|',
    ]
    for index, row in enumerate(rows[:limit], start=1):
        handle = row.get('handle', '').strip()
        profile_url = row.get('profile_url', '').strip()
        score = row.get('total_score', '')
        active_days = row.get('active_days_30d', '')
        days_since = row.get('days_since_last_post', '')
        if profile_url.startswith('https://note.com/'):
            creator = f'[{handle}]({profile_url})'
        else:
            creator = handle
        recency = '?' if days_since == '' else f'{days_since}日前'
        lines.append(f'| {index} | {creator} | {score} | {active_days} | {recency} |')

    lines.extend([
        '',
        '> 活動値は公開RSSで観測できた投稿証拠です。非公開のログイン履歴ではありません。',
        '> 実際のフォロー操作はプロフィール確認後に人間が行います。',
        '',
    ])
    return '\n'.join(lines)


def write_summary(summary: str, *, markdown_path: str = 'candidates.md') -> None:
    Path(markdown_path).write_text(summary, encoding='utf-8')
    github_summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if github_summary:
        with Path(github_summary).open('a', encoding='utf-8') as f:
            f.write(summary)
