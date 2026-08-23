from audience_miner.core import CandidateScore
from audience_miner.report import write_html_report


def test_report_contains_safe_profile_link(tmp_path):
    row = CandidateScore(
        handle='example',
        profile_url='https://note.com/example',
        activity_30d=4,
        active_days_30d=3,
        activity_score=15.0,
        topic_score=50.0,
        total_score=29.0,
        evidence_basis='public_rss_observed_lower_bound',
        recent_titles='<unsafe> AI',
    )
    target = tmp_path / 'report.html'
    write_html_report([row], str(target))
    text = target.read_text(encoding='utf-8')
    assert 'https://note.com/example' in text
    assert '&lt;unsafe&gt; AI' in text
    assert 'Open note profile' in text
