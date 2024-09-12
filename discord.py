# Discord.py
import nextcord
from nextcord.ext import tasks
from tracks import get_current_track
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
intents = nextcord.Intents.default()

client_discord = nextcord.Client(intents=intents)

try:
    with open('settings.json', 'r', encoding='utf-8') as file:
        settings = json.load(file)
        TOKEN = settings["token"]
except FileNotFoundError:
    new_json = {
        "client_id": "client_id",
        "client_secret": "client_secret",
        "token": "token",
        "redirect_url": "redirect_url"
    }
    with open("settings.json", 'w', encoding='utf-8') as file:
        json.dump(new_json, file, indent=4)

previous_track_info = None


@client_discord.event
async def on_ready():
    print(f'Logged as {client_discord.user}')
    update_status.start()


@tasks.loop(seconds=10)
async def update_status():
    global previous_track_info
    track_info = get_current_track()
    if track_info and track_info != 'No playback':
        artist, track_name, next_artist, next_track_name = track_info
        if track_info != previous_track_info:
            await client_discord.change_presence(activity=nextcord.Activity(
                                                 type=nextcord.ActivityType.listening,
                                                 name=f"{artist}: {track_name}"))
            print(f'Playing {artist}: {track_name}. Next: {next_artist}: {next_track_name}.')

            previous_track_info = track_info
    else:
        print('No track currently playing')
        await client_discord.change_presence(activity=None)
client_discord.run(TOKEN)
