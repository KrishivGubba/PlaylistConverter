import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

scope = "playlist-modify-public"

token = SpotifyOAuth(scope=scope, username= "k4rizkoy0o6o8feiri9agz9m4",client_id="799f8ff7f87241c391b9c87d7a2bd5a8",client_secret="d8ea189405cc433da7c4c849d165e49c",redirect_uri="http://127.0.0.1:5000/spotify_callback")
spotifyobj = spotipy.Spotify(auth_manager=token)

playlist = "newplayer1"
spotifyobj.playlist_add_items(playlist_id="7HyUNK1AaskCYHZT4jGgmb",items = ["spotify:track:4hZi9952OTtYQnXo2FJT6C"])