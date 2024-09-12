# Spotify.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

try:
    with open('settings.json', 'r', encoding='utf-8') as file:
        settings = json.load(file)
        spotify_id = settings["client_id"]
        spotify_secret = settings["client_secret"]
except FileNotFoundError:
    new_json = {
        "client_id": "client_id",
        "client_secret": "client_secret",
        "token": "token",
        "redirect_url": "redirect_url"
    }
    with open("settings.json", 'w', encoding='utf-8') as file:
        json.dump(new_json, file, indent=4)

def get_current_track():
    spotify_request = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=spotify_id,
                                                                        client_secret=spotify_secret,
                                                                        redirect_uri="http://localhost:8080/callback",
                                                                        scope='user-read-currently-playing user-read-playback-state'))
    current_track = spotify_request.current_playback()
    if current_track is not None and current_track["is_playing"]:
        track = current_track["item"]
        artist = track['artists'][0]['name']
        track_name = track['name']
        if 'queue' in current_track:
            next_track = current_track['queue'][0] if current_track['queue'] else None
            if next_track:
                next_artist = next_track['artists'][0]['name']
                next_track_name = next_track['name']
                return artist, track_name, next_artist, next_track_name
        return artist, track_name, "N/A", "N/A"
    else:
        return "No playback"
