from typing import TypedDict, Literal, List, Optional


class SpotifyConfig(TypedDict):
    client_id: str
    client_secret: str
    username: str
    redirect_url: str


class TidalConfig(TypedDict):
    access_token: str
    refresh_token: str
    session_id: str
    token_type: Literal["Bearer"]


class PlaylistConfig(TypedDict):
    spotify_id: str
    tidal_id: str


class SyncConfig(TypedDict):
    spotify: SpotifyConfig
    sync_playlists: Optional[List[PlaylistConfig]]
    included_playlists: Optional[List[str]]
    excluded_playlists: Optional[List[str]]
    skip_duplicate_playlist_names: Optional[bool]
