# Dependency review — 2026-08-12

Updated the Python graph to current PyPI releases: Spotipy 2.26.0, tidalapi 0.8.11, PyYAML 6.0.3,
tqdm 4.70.0, SQLAlchemy 2.0.52, pytest 9.1.1, and pytest-mock 3.15.1.

Changelog sources reviewed: [Spotipy](https://github.com/spotipy-dev/spotipy/releases),
[tidalapi](https://github.com/tamland/python-tidal/releases), [PyYAML](https://github.com/yaml/pyyaml/releases),
[tqdm](https://github.com/tqdm/tqdm/releases), [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy/releases),
[pytest](https://docs.pytest.org/en/stable/changelog.html), and [pytest-mock](https://github.com/pytest-dev/pytest-mock/releases).

No Bun/Node runtime exists; pnpm migration is not applicable.

The versions were checked again against the live PyPI index on 2026-08-15. An isolated Python 3.13.15 install passed `pip check`, and `pip-audit 2.10.1` reported no known vulnerabilities in the declared graph.
