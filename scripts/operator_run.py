from __future__ import annotations

from audience_miner.operator import config_from_env, render_markdown_summary, run_operator, write_summary


def main() -> int:
    config = config_from_env()
    print(
        'OPERATOR_RUN '
        f'tags={len(config.tags)} '
        f'max_candidates={config.max_candidates} '
        f'request_delay={config.request_delay}'
    )
    run_operator(config)
    summary = render_markdown_summary()
    write_summary(summary)
    print('OPERATOR_RUN_OK candidates.csv candidates.html candidates.md')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
