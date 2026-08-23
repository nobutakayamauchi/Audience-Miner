from __future__ import annotations

from html import escape
from pathlib import Path

from audience_miner.core import CandidateScore


def _recency_label(row: CandidateScore) -> str:
    if row.days_since_last_post is None:
        return '観測なし'
    if row.days_since_last_post == 0:
        return '今日'
    return f'{row.days_since_last_post}日前'


def write_html_report(rows: list[CandidateScore], path: str) -> None:
    cards = []
    for index, row in enumerate(rows, start=1):
        titles = escape(row.recent_titles or 'No recent title evidence')
        handle_attr = escape(row.handle, quote=True)
        recency = escape(_recency_label(row))
        last_at = escape(row.last_observed_post_at or 'not observed')
        cards.append(f'''<article class="card" data-handle="{handle_attr}">
  <div class="rank">#{index}</div>
  <h2>{escape(row.handle)}</h2>
  <div class="score">{row.total_score:.2f}</div>
  <div class="status" aria-live="polite">未処理</div>
  <dl>
    <div><dt>最終観測投稿</dt><dd>{recency}</dd></div>
    <div><dt>30日内の観測活動日</dt><dd>{row.active_days_30d}</dd></div>
    <div><dt>30日内の観測投稿数</dt><dd>{row.activity_30d}</dd></div>
    <div><dt>ジャンル一致</dt><dd>{row.topic_score:.2f}</dd></div>
  </dl>
  <p class="evidence">{escape(row.evidence_basis)} / last={last_at}</p>
  <p class="titles">{titles}</p>
  <a class="open" href="{escape(row.profile_url, quote=True)}" target="_blank" rel="noopener noreferrer">noteプロフィールを開く</a>
  <div class="review-actions">
    <button type="button" data-action="followed">フォロー済み</button>
    <button type="button" data-action="skip">除外</button>
    <button type="button" data-action="clear">解除</button>
  </div>
</article>''')

    cards_html = ''.join(cards) if cards else '<p>No scored candidates.</p>'
    document = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Audience Miner Candidates</title>
<style>
body{font-family:system-ui,-apple-system,sans-serif;margin:0;background:#f6f7f8;color:#111}
main{max-width:760px;margin:auto;padding:16px}
h1{font-size:24px;margin:8px 0}.note{font-size:13px;color:#555;margin-bottom:16px}
.card{background:white;border:1px solid #ddd;border-radius:16px;padding:16px;margin:12px 0;position:relative}
.card[data-status="skip"]{opacity:.55}.card[data-status="followed"]{border-width:2px}
.rank{font-size:12px;color:#666}h2{font-size:20px;margin:4px 70px 8px 0}
.score{position:absolute;right:16px;top:16px;font-size:24px;font-weight:700}
.status{font-size:12px;font-weight:700;margin:4px 0 10px}
dl{display:grid;gap:6px}dl div{display:flex;justify-content:space-between;gap:12px}dt{color:#555}dd{margin:0;font-weight:600}
.evidence{font-size:11px;color:#777}.titles{font-size:13px;line-height:1.5}
.open{display:block;text-align:center;padding:13px;border:1px solid #111;border-radius:10px;text-decoration:none;color:#111;font-weight:700;margin-top:12px}
.review-actions{display:grid;grid-template-columns:1fr 1fr auto;gap:8px;margin-top:8px}.review-actions button{padding:10px 8px;background:white;border:1px solid #bbb;border-radius:9px;font-weight:600}
</style>
</head>
<body><main>
<h1>Audience Miner</h1>
<p class="note">公開情報による候補ランキング。活動値は公開された投稿証拠であり、非公開のログイン履歴ではありません。プロフィールを確認してから人間が操作します。</p>
''' + cards_html + '''
</main>
<script>
(function(){
  const prefix = 'audience-miner-status:';
  const labels = {followed:'フォロー済み', skip:'除外'};
  function apply(card, status){
    if(status){ card.dataset.status = status; }
    else { delete card.dataset.status; }
    const node = card.querySelector('.status');
    node.textContent = labels[status] || '未処理';
  }
  document.querySelectorAll('.card[data-handle]').forEach(card => {
    const key = prefix + card.dataset.handle;
    apply(card, localStorage.getItem(key));
    card.querySelectorAll('button[data-action]').forEach(button => {
      button.addEventListener('click', () => {
        const action = button.dataset.action;
        if(action === 'clear') localStorage.removeItem(key);
        else localStorage.setItem(key, action);
        apply(card, action === 'clear' ? null : action);
      });
    });
  });
})();
</script>
</body></html>'''
    Path(path).write_text(document, encoding='utf-8')
