from __future__ import annotations

import argparse
from collections import Counter
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

import yaml

from . import auth as _auth
from . import sync as _sync
from .gui_ui import HTML as APP_HTML


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
DEFAULT_CONFIG = PROJECT_ROOT / "config.yml"
EXAMPLE_CONFIG = PROJECT_ROOT / "example_config.yml"
APP_ICON = PROJECT_ROOT / "assets" / "app-icon.png"


def _base_config() -> dict:
    return {
        "spotify": {
            "client_id": "",
            "client_secret": "",
            "username": "",
            "redirect_uri": "http://127.0.0.1:8888/callback",
            "open_browser": True,
        },
        "sync_favorites_default": True,
        "skip_duplicate_playlist_names": False,
        "max_concurrency": 10,
        "rate_limit": 10,
    }


def normalize_config(config: dict | None) -> dict:
    output = _base_config()
    if config:
        output.update({k: v for k, v in config.items() if k != "spotify"})
        output["spotify"].update(config.get("spotify") or {})
    output["sync_playlists"] = config.get("sync_playlists", []) if config else []
    output["included_playlists"] = config.get("included_playlists", []) if config else []
    output["excluded_playlists"] = config.get("excluded_playlists", []) if config else []
    return output


def load_config(path: Path) -> dict:
    source = path if path.exists() else EXAMPLE_CONFIG
    if source.exists():
        with source.open("r", encoding="utf-8") as f:
            return normalize_config(yaml.safe_load(f) or {})
    return normalize_config({})


def save_config(path: Path, config: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, sort_keys=False)


def _parse_lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def parse_playlist_mappings(value: str) -> list[dict[str, str]]:
    mappings = []
    for line in _parse_lines(value):
        if "->" in line:
            left, right = line.split("->", 1)
        elif "," in line:
            left, right = line.split(",", 1)
        else:
            parts = line.split()
            if len(parts) != 2:
                raise ValueError("Use one playlist mapping per line: spotify_id -> tidal_id")
            left, right = parts
        spotify_id, tidal_id = left.strip(), right.strip()
        if not spotify_id or not tidal_id:
            raise ValueError("Playlist mappings need both Spotify and Tidal ids")
        mappings.append({"spotify_id": spotify_id, "tidal_id": tidal_id})
    return mappings


def format_playlist_mappings(mappings: list[dict[str, str]]) -> str:
    return "\n".join(f"{m.get('spotify_id', '')} -> {m.get('tidal_id', '')}" for m in mappings)


def config_to_payload(config: dict, path: Path) -> dict:
    config = normalize_config(config)
    return {
        "path": str(path),
        "spotify": config["spotify"],
        "sync_favorites_default": bool(config.get("sync_favorites_default", True)),
        "skip_duplicate_playlist_names": bool(config.get("skip_duplicate_playlist_names", False)),
        "max_concurrency": int(config.get("max_concurrency", 10)),
        "rate_limit": int(config.get("rate_limit", 10)),
        "included_playlists": "\n".join(config.get("included_playlists") or []),
        "excluded_playlists": "\n".join(config.get("excluded_playlists") or []),
        "sync_playlists": format_playlist_mappings(config.get("sync_playlists") or []),
    }


def payload_to_config(payload: dict) -> dict:
    spotify = payload.get("spotify") or {}
    config = {
        "spotify": {
            "client_id": str(spotify.get("client_id", "")).strip(),
            "client_secret": str(spotify.get("client_secret", "")).strip(),
            "username": str(spotify.get("username", "")).strip(),
            "redirect_uri": str(spotify.get("redirect_uri", "")).strip(),
            "open_browser": bool(spotify.get("open_browser", True)),
        },
        "sync_favorites_default": bool(payload.get("sync_favorites_default", True)),
        "skip_duplicate_playlist_names": bool(payload.get("skip_duplicate_playlist_names", False)),
        "max_concurrency": max(1, int(payload.get("max_concurrency") or 10)),
        "rate_limit": max(1, int(payload.get("rate_limit") or 10)),
    }
    included = _parse_lines(str(payload.get("included_playlists", "")))
    excluded = _parse_lines(str(payload.get("excluded_playlists", "")))
    mappings = parse_playlist_mappings(str(payload.get("sync_playlists", "")))
    if included:
        config["included_playlists"] = [_sync.playlist_id(x) for x in included]
    if excluded:
        config["excluded_playlists"] = [_sync.playlist_id(x) for x in excluded]
    if mappings:
        config["sync_playlists"] = mappings
    return config


def run_config_for_mode(config: dict, mode: str) -> dict:
    output = copy.deepcopy(config)
    if mode in {"all", "single"}:
        output.pop("sync_playlists", None)
        output.pop("included_playlists", None)
    elif mode == "selected":
        output.pop("sync_playlists", None)
        if not output.get("included_playlists"):
            raise ValueError("Select at least one Spotify playlist before running selected mode")
    elif mode == "mapped" and not output.get("sync_playlists"):
        output.pop("included_playlists", None)
        raise ValueError("Add at least one configured playlist mapping before running this mode")
    elif mode == "mapped":
        output.pop("included_playlists", None)
    elif mode == "favorites":
        output.pop("sync_playlists", None)
        output.pop("included_playlists", None)
    else:
        raise ValueError("Unknown sync mode")
    return output


def build_cli_args(config_path: Path, mode: str, uri: str, include_favorites: bool) -> list[str]:
    args = [sys.executable, "-m", "spotify_to_tidal", "--config", str(config_path)]
    if mode == "single":
        uri = uri.strip()
        if not uri:
            raise ValueError("Add a Spotify playlist URI or id before running single playlist mode")
        args += ["--uri", uri]
        if include_favorites:
            args.append("--sync-favorites")
    elif mode == "favorites":
        args.append("--sync-favorites")
    elif mode in {"all", "selected", "mapped"} and not include_favorites:
        args.append("--no-sync-favorites")
    return args


def spotify_playlist_payloads(playlists: list[dict], current_user_id: str) -> list[dict]:
    name_counts = Counter(_sync.playlist_name_key(p) for p in playlists if p)
    output = []
    for playlist in playlists:
        if not playlist:
            continue
        owner = playlist.get("owner") or {}
        tracks = playlist.get("tracks") or playlist.get("items") or {}
        images = playlist.get("images") or []
        output.append(
            {
                "id": playlist.get("id", ""),
                "uri": playlist.get("uri", ""),
                "name": playlist.get("name", ""),
                "owner": owner.get("display_name") or owner.get("id", ""),
                "owned": owner.get("id") == current_user_id,
                "track_count": int(tracks.get("total") or 0),
                "duplicate_name_count": name_counts[_sync.playlist_name_key(playlist)],
                "image_url": images[0].get("url", "") if images else "",
            }
        )
    return output


def fetch_spotify_playlists(config: dict) -> dict:
    spotify = _auth.open_spotify_session(config["spotify"])
    current_user = spotify.current_user()
    playlists = []
    offset = 0
    while True:
        page = spotify.current_user_playlists(limit=50, offset=offset)
        playlists.extend(page.get("items") or [])
        if not page.get("next"):
            break
        offset += page.get("limit") or 50
    return {
        "user": current_user.get("display_name") or current_user.get("id", ""),
        "playlists": spotify_playlist_payloads(playlists, current_user.get("id", "")),
    }


def demo_playlist_payloads() -> dict:
    # ponytail: deterministic public/demo data; replace with live preview API if OAuth-free public lookup becomes useful.
    playlists = [
        {"id": "37i9dQZF1DXcBWIGoYBM5M", "name": "Today's Top Hits", "owner": {"id": "spotify", "display_name": "Spotify"}, "tracks": {"total": 50}, "images": [{"url": "https://picsum.photos/seed/todays-top-hits/96/96"}], "selected": True},
        {"id": "37i9dQZF1DX0XUsuxWHRQd", "name": "RapCaviar", "owner": {"id": "spotify", "display_name": "Spotify"}, "tracks": {"total": 50}, "images": [{"url": "https://picsum.photos/seed/rapcaviar/96/96"}], "selected": False},
        {"id": "37i9dQZF1DX10zKzsJ2jva", "name": "Viva Latino", "owner": {"id": "spotify", "display_name": "Spotify"}, "tracks": {"total": 50}, "images": [{"url": "https://picsum.photos/seed/viva-latino/96/96"}], "selected": True},
        {"id": "37i9dQZF1DX4UtSsGT1Sbe", "name": "All Out 80s", "owner": {"id": "spotify", "display_name": "Spotify"}, "tracks": {"total": 150}, "images": [{"url": "https://picsum.photos/seed/all-out-80s/96/96"}], "selected": True},
        {"id": "public-road-trip-a", "name": "Road Trip", "owner": {"id": "spotify", "display_name": "Spotify public"}, "tracks": {"total": 120}, "images": [{"url": "https://picsum.photos/seed/road-trip-a/96/96"}], "selected": True},
        {"id": "public-road-trip-b", "name": "road trip", "owner": {"id": "tidal-demo", "display_name": "Tidal public match"}, "tracks": {"total": 98}, "images": [{"url": "https://picsum.photos/seed/road-trip-b/96/96"}], "selected": True},
        {"id": "public-empty", "name": "Empty Playlist", "owner": {"id": "spotify", "display_name": "Spotify public"}, "tracks": {"total": 0}, "images": [{"url": "https://picsum.photos/seed/empty-playlist/96/96"}], "selected": False},
    ]
    payloads = spotify_playlist_payloads(playlists, "spotify")
    by_id = {playlist["id"]: playlist for playlist in playlists}
    for payload in payloads:
        payload["selected"] = bool(by_id[payload["id"]].get("selected"))
        payload["public_url"] = f"https://open.spotify.com/playlist/{payload['id']}" if payload["id"].startswith("37i9") else ""
    return {"user": "Public demo", "playlists": payloads}


class GuiState:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.lock = threading.Lock()
        self.logs = ""
        self.running = False
        self.status = "Ready"
        self.exit_code: int | None = None
        self.process: subprocess.Popen[str] | None = None

    def append(self, text: str) -> None:
        with self.lock:
            self.logs = (self.logs + text)[-200_000:]

    def snapshot(self) -> dict:
        with self.lock:
            return {
                "running": self.running,
                "status": self.status,
                "exit_code": self.exit_code,
                "logs": self.logs,
            }


def _start_sync(state: GuiState, config: dict, mode: str, uri: str, include_favorites: bool) -> None:
    run_config = run_config_for_mode(config, mode)
    fd, raw_path = tempfile.mkstemp(prefix=".spotify_to_tidal_run_", suffix=".yml", dir=str(PROJECT_ROOT))
    os.close(fd)
    run_config_path = Path(raw_path)
    try:
        save_config(run_config_path, run_config)
        args = build_cli_args(run_config_path, mode, uri, include_favorites)
    except Exception:
        try:
            run_config_path.unlink()
        except OSError:
            pass
        raise

    def worker() -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
        with state.lock:
            state.running = True
            state.status = "Running"
            state.exit_code = None
            state.logs = "$ " + " ".join(args) + "\n"
        try:
            process = subprocess.Popen(
                args,
                cwd=str(PROJECT_ROOT),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
            with state.lock:
                state.process = process
            assert process.stdout is not None
            for line in process.stdout:
                state.append(line)
            code = process.wait()
            with state.lock:
                state.exit_code = code
                state.status = "Finished" if code == 0 else "Error"
        except Exception as exc:
            state.append(f"\n{exc}\n")
            with state.lock:
                state.status = "Error"
        finally:
            with state.lock:
                state.running = False
                state.process = None
            try:
                run_config_path.unlink()
            except OSError:
                pass

    threading.Thread(target=worker, daemon=True).start()


HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Spotify to Tidal</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f4ef;
      --panel: #fffdf8;
      --ink: #1c2424;
      --muted: #64706f;
      --line: #d9d4ca;
      --accent: #087c76;
      --accent-ink: #ffffff;
      --spotify: #1db954;
      --tidal: #111111;
      --danger: #a6342e;
      --shadow: 0 18px 45px rgba(32, 38, 37, .08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 14px;
      letter-spacing: 0;
    }
    header {
      min-height: 76px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 18px 28px;
      border-bottom: 1px solid var(--line);
      background: rgba(255,253,248,.82);
      backdrop-filter: blur(14px);
      position: sticky;
      top: 0;
      z-index: 2;
    }
    .brand { display: flex; align-items: center; gap: 14px; min-width: 0; }
    .brand > div:last-child { min-width: 0; }
    .mark {
      width: 42px;
      height: 42px;
      flex: 0 0 42px;
      display: grid;
      place-items: center;
      background: linear-gradient(135deg, var(--spotify) 0 48%, var(--tidal) 49% 100%);
      color: white;
      font-weight: 800;
      border-radius: 8px;
      box-shadow: var(--shadow);
    }
    h1, h2, h3 { margin: 0; letter-spacing: 0; }
    h1 { font-size: 22px; line-height: 1.1; font-weight: 760; }
    .status-line {
      color: var(--muted);
      margin-top: 4px;
      font-size: 13px;
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .status-pill {
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 8px;
      padding: 9px 12px;
      color: var(--muted);
      min-width: 120px;
      text-align: center;
    }
    main {
      width: min(1220px, calc(100vw - 32px));
      margin: 24px auto;
      display: grid;
      grid-template-columns: minmax(320px, 410px) minmax(0, 1fr);
      gap: 22px;
    }
    section {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      min-width: 0;
    }
    .settings { padding: 20px; }
    .runner { display: flex; flex-direction: column; min-height: 690px; }
    .section-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 18px;
    }
    .section-head h2 { font-size: 17px; font-weight: 760; }
    .service-cues { display: flex; gap: 6px; }
    .cue { width: 10px; height: 10px; border-radius: 3px; }
    .cue.spotify { background: var(--spotify); }
    .cue.tidal { background: var(--tidal); }
    .mini-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    fieldset { border: 0; margin: 0 0 22px; padding: 0; }
    legend {
      padding: 0;
      margin-bottom: 10px;
      font-weight: 720;
      font-size: 13px;
      color: #26302f;
    }
    label { display: block; color: var(--muted); font-size: 12px; font-weight: 650; margin-bottom: 6px; }
    input, textarea {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 7px;
      background: #fffefa;
      color: var(--ink);
      padding: 10px 11px;
      font: inherit;
      outline: none;
    }
    input:focus, textarea:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(8,124,118,.12); }
    textarea { resize: vertical; min-height: 80px; line-height: 1.4; }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .row { margin-bottom: 12px; }
    .check {
      display: flex;
      align-items: center;
      gap: 9px;
      color: var(--ink);
      font-weight: 650;
      margin: 10px 0 0;
    }
    .check input { width: 16px; height: 16px; accent-color: var(--accent); }
    .segmented {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
    }
    .segmented label {
      margin: 0;
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 7px;
      color: var(--ink);
      background: #fffefa;
      cursor: pointer;
      min-height: 42px;
    }
    .segmented input { width: 14px; margin: 0 7px 0 0; accent-color: var(--accent); }
    .toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 18px;
      border-bottom: 1px solid var(--line);
    }
    .actions { display: flex; gap: 10px; flex-wrap: wrap; }
    button {
      border: 1px solid var(--line);
      border-radius: 7px;
      background: #fffefa;
      color: var(--ink);
      padding: 10px 13px;
      min-height: 40px;
      font: inherit;
      font-weight: 720;
      cursor: pointer;
    }
    button.primary { background: var(--accent); border-color: var(--accent); color: var(--accent-ink); }
    button.danger { color: var(--danger); }
    button:disabled { opacity: .48; cursor: not-allowed; }
    .mode-uri { width: min(360px, 100%); }
    .picker {
      padding: 16px 18px 0;
      border-bottom: 1px solid var(--line);
    }
    .picker-head, .picker-summary {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }
    .picker-head h2 { font-size: 17px; }
    .picker-tools {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
      margin-top: 12px;
      align-items: center;
    }
    .picker-tools .actions { flex-wrap: nowrap; }
    .picker-tools input { min-width: 180px; }
    .picker-summary { color: var(--muted); font-size: 13px; margin: 10px 0; align-items: flex-start; }
    .playlist-list {
      max-height: 245px;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fffefa;
      margin-bottom: 16px;
    }
    .playlist-row {
      display: grid;
      grid-template-columns: 22px minmax(0, 1fr) auto;
      gap: 10px;
      align-items: center;
      min-height: 54px;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
    }
    .playlist-row:last-child { border-bottom: 0; }
    .playlist-row input { width: 16px; height: 16px; accent-color: var(--accent); }
    .playlist-title { font-weight: 740; overflow-wrap: anywhere; }
    .playlist-meta { color: var(--muted); font-size: 12px; margin-top: 2px; }
    .badge {
      border: 1px solid #e3b0a8;
      color: var(--danger);
      background: #fff3f0;
      border-radius: 6px;
      padding: 4px 6px;
      font-size: 11px;
      font-weight: 760;
    }
    .log-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 16px 18px 12px;
    }
    .log-head h2 { font-size: 17px; }
    .exit { color: var(--muted); font-size: 13px; }
    pre {
      margin: 0 18px 18px;
      min-height: 560px;
      flex: 1;
      overflow: auto;
      background: #171d1d;
      color: #edf7f4;
      border-radius: 8px;
      padding: 16px;
      line-height: 1.45;
      font: 13px/1.45 "Cascadia Mono", Consolas, monospace;
      white-space: pre-wrap;
    }
    .message { min-height: 18px; color: var(--muted); font-size: 13px; }
    .message.error { color: var(--danger); }
    @media (max-width: 880px) {
      header { align-items: flex-start; padding: 16px; }
      main { width: calc(100vw - 24px); grid-template-columns: 1fr; margin-top: 12px; }
      .toolbar { align-items: stretch; flex-direction: column; }
      .mode-uri { width: 100%; }
      .grid-2, .segmented, .mini-actions { grid-template-columns: 1fr; }
      .picker-head, .picker-summary { align-items: stretch; flex-direction: column; }
      .picker-tools { grid-template-columns: 1fr; }
      .picker-tools .actions { flex-wrap: wrap; }
      .playlist-row { grid-template-columns: 22px minmax(0, 1fr); }
      .badge { width: fit-content; }
      pre { min-height: 360px; }
    }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="mark">ST</div>
      <div>
        <h1>Spotify to Tidal</h1>
        <div class="status-line" id="configPath">config.yml</div>
      </div>
    </div>
    <div class="status-pill" id="statusPill">Ready</div>
  </header>

  <main>
    <section class="settings">
      <div class="section-head">
        <h2>Configuration</h2>
        <div class="service-cues"><span class="cue spotify"></span><span class="cue tidal"></span></div>
      </div>

      <fieldset>
        <legend>Spotify</legend>
        <div class="row"><label for="clientId">Client ID</label><input id="clientId" autocomplete="off"></div>
        <div class="row"><label for="clientSecret">Client secret</label><input id="clientSecret" type="password" autocomplete="off"></div>
        <div class="row"><label for="username">Username</label><input id="username" autocomplete="username"></div>
        <div class="row"><label for="redirectUri">Redirect URI</label><input id="redirectUri"></div>
        <label class="check"><input id="openBrowser" type="checkbox"> Open browser for auth</label>
      </fieldset>

      <fieldset>
        <legend>Connections</legend>
        <div class="mini-actions">
          <button id="spotifyBtn" type="button">Connect Spotify</button>
          <button id="tidalBtn" type="button">Connect Tidal</button>
        </div>
      </fieldset>

      <fieldset>
        <legend>Sync mode</legend>
        <div class="segmented">
          <label><input type="radio" name="mode" value="all" checked>All playlists</label>
          <label><input type="radio" name="mode" value="selected">Selected playlists</label>
          <label><input type="radio" name="mode" value="single">Single playlist</label>
          <label><input type="radio" name="mode" value="mapped">Configured mappings</label>
          <label><input type="radio" name="mode" value="favorites">Favorites only</label>
        </div>
      </fieldset>

      <fieldset>
        <legend>Options</legend>
        <div class="row"><label for="playlistUri">Spotify playlist URI or ID</label><input id="playlistUri" placeholder="1ABCDEqsABCD6EaABCDa0a"></div>
        <label class="check"><input id="includeFavorites" type="checkbox"> Include favorites</label>
        <label class="check"><input id="skipDuplicates" type="checkbox"> Skip duplicate playlist names</label>
        <div class="grid-2" style="margin-top:12px">
          <div><label for="maxConcurrency">Max concurrency</label><input id="maxConcurrency" type="number" min="1" step="1"></div>
          <div><label for="rateLimit">Rate limit</label><input id="rateLimit" type="number" min="1" step="1"></div>
        </div>
      </fieldset>

      <fieldset>
        <legend>Playlist filters</legend>
        <div class="row"><label for="excludedPlaylists">Excluded playlists</label><textarea id="excludedPlaylists" placeholder="spotify:playlist:..."></textarea></div>
        <div class="row"><label for="syncPlaylists">Configured mappings</label><textarea id="syncPlaylists" placeholder="spotify_id -> tidal_id"></textarea></div>
      </fieldset>
      <div id="message" class="message"></div>
    </section>

    <section class="runner">
      <div class="toolbar">
        <div class="mode-uri"><label for="activeMode">Active mode</label><input id="activeMode" readonly value="All playlists"></div>
        <div class="actions">
          <button id="saveBtn">Save config</button>
          <button id="runBtn" class="primary">Run sync</button>
          <button id="stopBtn" class="danger" disabled>Stop</button>
        </div>
      </div>
      <div class="picker">
        <div class="picker-head">
          <h2>Spotify playlists</h2>
          <button id="loadPlaylistsBtn" type="button">Load playlists</button>
        </div>
        <div class="picker-tools">
          <input id="playlistSearch" placeholder="Search playlists">
          <div class="actions">
            <button id="selectVisibleBtn" type="button">Select visible</button>
            <button id="clearSelectedBtn" type="button">Clear</button>
          </div>
        </div>
        <div class="picker-summary">
          <span id="playlistSummary">Connect Spotify to load playlists.</span>
          <span id="duplicateSummary"></span>
        </div>
        <div class="playlist-list" id="playlistList"></div>
      </div>
      <div class="log-head">
        <h2>Activity log</h2>
        <span class="exit" id="exitCode"></span>
      </div>
      <pre id="log">Ready</pre>
    </section>
  </main>

  <script>
    const $ = (id) => document.getElementById(id);
    const modeLabel = { all: "All playlists", selected: "Selected playlists", single: "Single playlist", mapped: "Configured mappings", favorites: "Favorites only" };
    let poller = null;
    let spotifyPlaylists = [];
    let selectedPlaylistIds = new Set();
    let spotifyUser = "";

    function mode() {
      return document.querySelector('input[name="mode"]:checked').value;
    }

    function setMessage(text, isError = false) {
      $("message").textContent = text;
      $("message").classList.toggle("error", isError);
    }

    function payload() {
      return {
        spotify: {
          client_id: $("clientId").value,
          client_secret: $("clientSecret").value,
          username: $("username").value,
          redirect_uri: $("redirectUri").value,
          open_browser: $("openBrowser").checked
        },
        sync_favorites_default: $("includeFavorites").checked,
        skip_duplicate_playlist_names: $("skipDuplicates").checked,
        max_concurrency: $("maxConcurrency").value,
        rate_limit: $("rateLimit").value,
        included_playlists: [...selectedPlaylistIds].join("\n"),
        excluded_playlists: $("excludedPlaylists").value,
        sync_playlists: $("syncPlaylists").value
      };
    }

    function fill(data) {
      $("configPath").textContent = data.path;
      $("clientId").value = data.spotify.client_id || "";
      $("clientSecret").value = data.spotify.client_secret || "";
      $("username").value = data.spotify.username || "";
      $("redirectUri").value = data.spotify.redirect_uri || "";
      $("openBrowser").checked = data.spotify.open_browser !== false;
      $("includeFavorites").checked = data.sync_favorites_default !== false;
      $("skipDuplicates").checked = data.skip_duplicate_playlist_names === true;
      $("maxConcurrency").value = data.max_concurrency || 10;
      $("rateLimit").value = data.rate_limit || 10;
      selectedPlaylistIds = new Set((data.included_playlists || "").split(/\r?\n/).map(x => x.trim()).filter(Boolean));
      $("excludedPlaylists").value = data.excluded_playlists || "";
      $("syncPlaylists").value = data.sync_playlists || "";
      renderPlaylists();
    }

    async function api(path, body) {
      const res = await fetch(path, {
        method: body ? "POST" : "GET",
        headers: body ? {"Content-Type": "application/json"} : undefined,
        body: body ? JSON.stringify(body) : undefined
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Request failed");
      return data;
    }

    async function save() {
      await api("/api/config", payload());
      setMessage("Saved");
    }

    async function run() {
      setMessage("");
      await api("/api/run", {
        config: payload(),
        mode: mode(),
        uri: $("playlistUri").value,
        include_favorites: $("includeFavorites").checked
      });
      startPolling();
    }

    async function connectSpotify() {
      setMessage("Opening Spotify auth if needed...");
      const data = await api("/api/spotify-playlists", { config: payload() });
      spotifyPlaylists = data.playlists || [];
      spotifyUser = data.user || "";
      renderPlaylists();
      setMessage(`Spotify connected. Loaded ${spotifyPlaylists.length} playlists.`);
    }

    async function connectTidal() {
      setMessage("Opening Tidal device login if needed...");
      const data = await api("/api/tidal-connect", {});
      setMessage(data.ok ? "Tidal connected." : "Tidal connection failed.", !data.ok);
    }

    function visiblePlaylists() {
      const query = $("playlistSearch").value.trim().toLowerCase();
      return spotifyPlaylists.filter(p => !query || p.name.toLowerCase().includes(query) || p.id.toLowerCase().includes(query));
    }

    function setMode(value) {
      const radio = document.querySelector(`input[name="mode"][value="${value}"]`);
      if (radio) {
        radio.checked = true;
        $("activeMode").value = modeLabel[value];
      }
    }

    function renderPlaylists() {
      const list = $("playlistList");
      if (!list) return;
      const visible = visiblePlaylists();
      list.innerHTML = "";
      for (const playlist of visible) {
        const row = document.createElement("label");
        row.className = "playlist-row";
        const box = document.createElement("input");
        box.type = "checkbox";
        box.checked = selectedPlaylistIds.has(playlist.id);
        box.addEventListener("change", () => {
          box.checked ? selectedPlaylistIds.add(playlist.id) : selectedPlaylistIds.delete(playlist.id);
          setMode("selected");
          updatePlaylistSummary();
        });
        const main = document.createElement("div");
        const title = document.createElement("div");
        title.className = "playlist-title";
        title.textContent = playlist.name || "(untitled)";
        const meta = document.createElement("div");
        meta.className = "playlist-meta";
        meta.textContent = `${playlist.track_count || 0} tracks - ${playlist.owned ? "owned" : playlist.owner || "followed"} - ${playlist.id}`;
        main.append(title, meta);
        row.append(box, main);
        if ((playlist.duplicate_name_count || 0) > 1) {
          const badge = document.createElement("span");
          badge.className = "badge";
          badge.textContent = "duplicate";
          row.append(badge);
        }
        list.append(row);
      }
      updatePlaylistSummary();
    }

    function updatePlaylistSummary() {
      const duplicates = spotifyPlaylists.filter(p => (p.duplicate_name_count || 0) > 1).length;
      $("playlistSummary").textContent = spotifyPlaylists.length
        ? `${selectedPlaylistIds.size} selected from ${spotifyPlaylists.length}${spotifyUser ? ` for ${spotifyUser}` : ""}`
        : "Connect Spotify to load playlists.";
      $("duplicateSummary").textContent = duplicates ? `${duplicates} duplicate-name entries detected` : "";
    }

    async function stop() {
      await api("/api/stop", {});
      startPolling();
    }

    async function poll() {
      const data = await api("/api/status");
      $("statusPill").textContent = data.status;
      $("log").textContent = data.logs || "Ready";
      $("exitCode").textContent = data.exit_code === null ? "" : `exit ${data.exit_code}`;
      $("runBtn").disabled = data.running;
      $("stopBtn").disabled = !data.running;
      if (!data.running && poller) {
        clearInterval(poller);
        poller = null;
      }
    }

    function startPolling() {
      if (!poller) poller = setInterval(poll, 900);
      poll();
    }

    for (const radio of document.querySelectorAll('input[name="mode"]')) {
      radio.addEventListener("change", () => $("activeMode").value = modeLabel[mode()]);
    }
    $("saveBtn").addEventListener("click", () => save().catch(err => setMessage(err.message, true)));
    $("runBtn").addEventListener("click", () => run().catch(err => setMessage(err.message, true)));
    $("stopBtn").addEventListener("click", () => stop().catch(err => setMessage(err.message, true)));
    $("spotifyBtn").addEventListener("click", () => connectSpotify().catch(err => setMessage(err.message, true)));
    $("tidalBtn").addEventListener("click", () => connectTidal().catch(err => setMessage(err.message, true)));
    $("loadPlaylistsBtn").addEventListener("click", () => connectSpotify().catch(err => setMessage(err.message, true)));
    $("playlistSearch").addEventListener("input", () => renderPlaylists());
    $("selectVisibleBtn").addEventListener("click", () => {
      for (const playlist of visiblePlaylists()) selectedPlaylistIds.add(playlist.id);
      setMode("selected");
      renderPlaylists();
    });
    $("clearSelectedBtn").addEventListener("click", () => {
      selectedPlaylistIds.clear();
      renderPlaylists();
    });

    api("/api/config").then(fill).then(poll).catch(err => setMessage(err.message, true));
  </script>
</body>
</html>
"""


def _json(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    raw = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


def _read_json(handler: BaseHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length", "0"))
    return json.loads(handler.rfile.read(length).decode("utf-8") or "{}")


def make_handler(state: GuiState):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args) -> None:
            return

        def do_GET(self) -> None:
            try:
                path = urlparse(self.path).path
                if path == "/":
                    raw = APP_HTML.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(raw)))
                    self.end_headers()
                    self.wfile.write(raw)
                elif path in {"/favicon.ico", "/app-icon.png"} and APP_ICON.exists():
                    raw = APP_ICON.read_bytes()
                    self.send_response(200)
                    self.send_header("Content-Type", "image/png")
                    self.send_header("Content-Length", str(len(raw)))
                    self.end_headers()
                    self.wfile.write(raw)
                elif path == "/api/config":
                    _json(self, 200, config_to_payload(load_config(state.config_path), state.config_path))
                elif path == "/api/status":
                    _json(self, 200, state.snapshot())
                elif path == "/api/demo-playlists":
                    _json(self, 200, demo_playlist_payloads())
                else:
                    _json(self, 404, {"error": "Not found"})
            except Exception as exc:
                _json(self, 500, {"error": str(exc)})

        def do_POST(self) -> None:
            try:
                body = _read_json(self)
                if self.path == "/api/config":
                    config = payload_to_config(body)
                    save_config(state.config_path, config)
                    _json(self, 200, {"ok": True})
                elif self.path == "/api/run":
                    with state.lock:
                        if state.running:
                            _json(self, 409, {"error": "Sync already running"})
                            return
                    config = payload_to_config(body.get("config") or {})
                    save_config(state.config_path, config)
                    _start_sync(
                        state,
                        config,
                        str(body.get("mode", "all")),
                        str(body.get("uri", "")),
                        bool(body.get("include_favorites", True)),
                    )
                    _json(self, 200, {"ok": True})
                elif self.path == "/api/spotify-playlists":
                    config = payload_to_config(body.get("config") or body)
                    save_config(state.config_path, config)
                    _json(self, 200, fetch_spotify_playlists(config))
                elif self.path == "/api/tidal-connect":
                    session = _auth.open_tidal_session()
                    _json(self, 200, {"ok": bool(session.check_login())})
                elif self.path == "/api/stop":
                    with state.lock:
                        process = state.process
                        if process and state.running:
                            state.status = "Stopping"
                            process.terminate()
                    _json(self, 200, {"ok": True})
                else:
                    _json(self, 404, {"error": "Not found"})
            except SystemExit as exc:
                _json(self, 400, {"error": str(exc)})
            except Exception as exc:
                _json(self, 400, {"error": str(exc)})

    return Handler


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)

    state = GuiState(Path(args.config).resolve())
    handler = make_handler(state)
    try:
        server = ThreadingHTTPServer((args.host, args.port), handler)
    except OSError:
        server = ThreadingHTTPServer((args.host, 0), handler)
    host, port = server.server_address
    url = f"http://{host}:{port}/"
    print(f"Spotify to Tidal GUI running at {url}")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
