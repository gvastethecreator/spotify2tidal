# Spotify to Tidal GUI Design Record

## Project findings

- The repository started as a small Python CLI published as `spotify_to_tidal`.
- The synchronization engine remains in `src/spotify_to_tidal/sync.py`; the GUI reuses it instead of implementing a second sync path.
- Authentication remains in `src/spotify_to_tidal/auth.py` and uses the existing Spotify browser and Tidal device flows.
- YAML is the configuration contract: local values live in ignored `config.yml`, with safe placeholders in `example_config.yml`.
- The CLI supports the complete collection, one playlist through `--uri`, favorites through `--sync-favorites`, explicit `sync_playlists` mappings, and GUI selection through `included_playlists`.
- Progress is emitted through `print` and `tqdm`, so the GUI runs the CLI as a subprocess and captures its output.
- The main trust boundaries are local secrets, browser/device authentication, `.session.yml`, `.cache.db`, and CLI paths that can exit the process.

## Decisions

1. **Use a local web GUI.** Python's standard HTTP server provides a responsive interface without adding a web framework to the product graph.
2. **Keep the CLI authoritative.** The GUI prepares configuration and arguments, then launches the existing CLI behavior.
3. **Keep long syncs off the request thread.** The subprocess streams stdout and stderr while the local server remains responsive.
4. **Use explicit controls instead of a raw YAML editor.** The UI owns account values, sync modes, favorites, concurrency, rate limits, exclusions, and mappings.
5. **Preserve saved configuration.** Modes such as `all` prepare a temporary YAML file without destructive edits to the user's stored mappings.
6. **Offer a narrow cancellation path.** Stop terminates the active subprocess; no new queue or job database is introduced.
7. **Keep the existing cache.** `.cache.db` remains the failed-match store.
8. **Test without real services.** Unit tests cover mapping parsing, mode selection, argument construction, duplicate handling, and the local icon route.
9. **Provide a credential-free public demo.** Fixture playlists expose selection and duplicate review without OAuth or destination writes.

## Implemented MVP

- `spotify_to_tidal_gui` entry point and a local server bound to `127.0.0.1`.
- Load and save behavior for `config.yml`, with `example_config.yml` as the initial fallback.
- Spotify authentication and playlist loading from the GUI.
- Filterable multi-playlist selection and duplicate-name review.
- Tidal authentication through the existing `tidalapi` flow.
- Temporary run configuration, subprocess execution, logs, status, and stop control.
- Responsive desktop and mobile layouts.
- English UI copy across the application and public project site.

## Verification contract

- Run `python -m pytest` for the focused behavior suite.
- Run `python -m spotify_to_tidal.gui --no-browser` to verify the local server.
- Load the public demo in a real browser at desktop and 390 px mobile widths.
- Confirm no horizontal overflow, runtime errors, private configuration, or non-English application text.
- Run `python -m spotify_to_tidal --help` to confirm CLI compatibility.

## Deliberate follow-ups

- Structured progress by playlist and track instead of console-only output.
- Exportable reports for songs that could not be matched.
- Optional desktop packaging and shortcuts.
- Optional configuration storage outside the repository root.
