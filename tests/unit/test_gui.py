from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from spotify_to_tidal.gui import (
    APP_ICON,
    GuiState,
    build_cli_args,
    make_handler,
    parse_playlist_mappings,
    payload_to_config,
    run_config_for_mode,
    spotify_playlist_payloads,
)
from spotify_to_tidal.sync import filter_spotify_playlists


def test_parse_playlist_mappings():
    assert parse_playlist_mappings("sp1 -> td1\nsp2,td2") == [
        {"spotify_id": "sp1", "tidal_id": "td1"},
        {"spotify_id": "sp2", "tidal_id": "td2"},
    ]


def test_all_mode_ignores_saved_mappings():
    config = {"spotify": {}, "sync_playlists": [{"spotify_id": "sp", "tidal_id": "td"}], "included_playlists": ["sp"]}
    output = run_config_for_mode(config, "all")
    assert "sync_playlists" not in output
    assert "included_playlists" not in output


def test_selected_mode_requires_playlist_ids():
    config = {"spotify": {}, "included_playlists": ["spotify:playlist:abc"]}
    assert run_config_for_mode(config, "selected")["included_playlists"] == ["spotify:playlist:abc"]


def test_single_playlist_args_include_favorites_only_when_requested():
    args = build_cli_args(Path("run.yml"), "single", "abc", True)
    assert args[-3:] == ["--uri", "abc", "--sync-favorites"]


def test_payload_normalizes_selected_playlist_ids():
    config = payload_to_config({"spotify": {}, "included_playlists": "spotify:playlist:abc\nhttps://open.spotify.com/playlist/def/?x=1"})
    assert config["included_playlists"] == ["abc", "def"]


def test_spotify_playlist_payload_marks_duplicates():
    playlists = [
        {"id": "a", "name": "Road", "owner": {"id": "me"}, "tracks": {"total": 1}},
        {"id": "b", "name": "road", "owner": {"id": "me"}, "tracks": {"total": 2}},
    ]
    payloads = spotify_playlist_payloads(playlists, "me")
    assert [p["duplicate_name_count"] for p in payloads] == [2, 2]


def test_filter_spotify_playlists_includes_and_skips_duplicate_names():
    playlists = [
        {"id": "a", "name": "Road", "owner": {"id": "me"}},
        {"id": "b", "name": "road", "owner": {"id": "me"}},
        {"id": "c", "name": "Other", "owner": {"id": "other"}},
    ]
    assert filter_spotify_playlists(playlists, "me", {"included_playlists": ["a", "b"], "skip_duplicate_playlist_names": True}) == [playlists[0]]
    assert filter_spotify_playlists(playlists, "me", {"included_playlists": ["c"]}) == [playlists[2]]


def test_app_icon_route_serves_png(tmp_path):
    assert APP_ICON.exists()
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(GuiState(tmp_path / "config.yml")))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    conn = HTTPConnection(*server.server_address, timeout=5)
    try:
        conn.request("GET", "/app-icon.png")
        res = conn.getresponse()
        data = res.read()
        assert res.status == 200
        assert res.getheader("Content-Type") == "image/png"
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
    finally:
        conn.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
