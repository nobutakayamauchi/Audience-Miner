import csv
import sys

import pytest

from audience_miner.operator import build_cli_command, config_from_env, render_markdown_summary


def test_operator_config_is_bounded_and_deduped():
    config = config_from_env({
        'AUDIENCE_KEYWORDS': 'AI,ChatGPT',
        'AUDIENCE_TAGS': '#AI副業, 生成AI,AI副業',
        'AUDIENCE_MAX_CANDIDATES': '30',
    })
    assert config.tags == ('AI副業', '生成AI')
    assert config.max_candidates == 30
    assert config.request_delay == 0.5


def test_operator_rejects_out_of_range_candidate_count():
    with pytest.raises(ValueError):
        config_from_env({
            'AUDIENCE_KEYWORDS': 'AI',
            'AUDIENCE_TAGS': 'AI副業',
            'AUDIENCE_MAX_CANDIDATES': '500',
        })


def test_build_command_uses_argument_vector_not_shell():
    config = config_from_env({
        'AUDIENCE_KEYWORDS': 'AI,"quoted"',
        'AUDIENCE_TAGS': 'AI副業,生成AI',
        'AUDIENCE_MAX_CANDIDATES': '10',
    })
    command = build_cli_command(config)
    assert command[0] == sys.executable
    assert command[1:3] == ['-m', 'audience_miner.cli']
    assert 'AI,"quoted"' in command
    assert command.count('--tag') == 2
    assert '--request-delay' in command
    assert '0.5' in command


def test_markdown_summary_has_clickable_note_profiles(tmp_path):
    target = tmp_path / 'candidates.csv'
    fields = [
        'handle', 'profile_url', 'activity_30d', 'active_days_30d',
        'last_observed_post_at', 'days_since_last_post',
        'activity_score', 'topic_score', 'total_score', 'evidence_basis',
        'recent_titles',
    ]
    with target.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerow({
            'handle': 'example',
            'profile_url': 'https://note.com/example',
            'activity_30d': '12',
            'active_days_30d': '9',
            'last_observed_post_at': '2026-08-23T00:00:00+00:00',
            'days_since_last_post': '0',
            'activity_score': '45',
            'topic_score': '80',
            'total_score': '59',
            'evidence_basis': 'public_rss_observed_lower_bound',
            'recent_titles': 'AI副業',
        })
    summary = render_markdown_summary(str(target))
    assert '[example](https://note.com/example)' in summary
    assert '| 1 |' in summary
    assert '公開RSS' in summary
