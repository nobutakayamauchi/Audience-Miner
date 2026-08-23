from __future__ import annotations

from html import escape
from pathlib import Path

from audience_miner.core import CandidateScore


def write_html_report(rows: list[CandidateScore], path: str) -> None:
    cards = []
    for index, row in enumerate(rows, start=1):
        titles = escape(row.recent_titles or 'No recent title evidence')
        cards.append(f'''<article class="card">
  <div class="rank">#{index}</div>
  <h2>{escape(row.handle)}</h2>
  <div class="score">{row.total_score:.2f}</div>
  <dl>
    <div><dt>Observed active days / 30d</dt><dd>{row.active_days_30d}</dd></div>
    <div><dt>Observed posts / 30d</dt><dd>{row.activity_30d}</dd></div>
    <div><dt>Topic fit</dt><dd>{row.topic_score:.2f}</dd></div>
  </dl>
  <p class="evidence">{escape(row.evidence_basis)}</p>
  <p class="titles">{titles}</p>
  <a class="open" href="{escape(row.profile_url, quote=True)}" target="_blank" rel="noopener noreferrer">Open note profile</a>
</article>''')

    document = f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Audience Miner Candidates</title>
<style>
body{{font-family:system-ui,-apple-system,sans-serif;margin:0;background:#f6f7f8;color:#111}}
main{{max-width:760px;margin:auto;padding:16px}}
h1{{font-size:24px;margin:8px 0}} .note{{font-size:13px;color:#555;margin-bottom:16px}}
.card{{background:white;border:1px solid #ddd;border-radius:16px;padding:16px;margin:12px 0;position:relative}}
.rank{{font-size:12px;color:#666}} h2{{font-size:20px;margin:4px 70px 8px 0}}
.score{{position:absolute;right:16px;top:16px;font-size:24px;font-weight:700}}
dl{{display:grid;gap:6px}} dl div{{display:flex;justify-content:space-between;gap:12px}} dt{{color:#555}} dd{{margin:0;font-weight:600}}
.evidence{{font-size:11px;color:#777}} .titles{{font-size:13px;line-height:1.5}}
.open{{display:block;text-align:center;padding:13px;border:1px solid #111;border-radius:10px;text-decoration:none;color:#111;font-weight:700;margin-top:12px}}
</style>
</head>
<body><main>
<h1>Audience Miner</h1>
<p class="note">Public evidence ranking. Activity is observed publishing evidence, not private login history.</p>
{''.join(cards) if cards else '<p>No scored candidates.</p>'}
</main></body></html>'''
    Path(path).write_text(document, encoding='utf-8')
