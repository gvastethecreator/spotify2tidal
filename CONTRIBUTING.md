# Contributing

Thanks for improving Spotify to Tidal. Keep changes focused, preserve the local credential boundary, and explain any behavior that can write to a user's Tidal account.

## Development setup

```bash
python -m pip install -e .
python -m pytest
```

## Before opening a pull request

Run the same focused gates as CI:

```bash
python -m pytest
python -m compileall -q src tests
python -m pip check
python -m spotify_to_tidal --help
git diff --check
```

For GUI changes, also open the local app, load the public demo, and check both a desktop viewport and a 390 px mobile viewport. Never include `config.yml`, OAuth tokens, account identifiers, or private playlists in screenshots or fixtures.

## Pull requests

- Describe the user-visible outcome and the verification you ran.
- Add one focused regression test when behavior changes and a nearby seam exists.
- Keep product copy and public documentation in English.
- Avoid unrelated formatting or dependency churn.

By contributing, you agree that your work is licensed under the repository's [MIT license](LICENSE).
