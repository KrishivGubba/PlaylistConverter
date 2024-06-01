import base64

import requests
import json
from spotifyactions import SpotifyActions

import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

spotify_actions = SpotifyActions(client_id, client_secret)


url = f"https://api.spotify.com/v1/playlists/4oLh6CXQGaXgbAGuNeV4RA/tracks"
uri = "spotify:track:4hZi9952OTtYQnXo2FJT6C"

code = "AQDQxcsaNADxeRvn0cLOrj7TbnQofiKZZRi64LjF3tc7kEKNzaxpt50l8HmBBuxPYnvIDmWK9ziccJ4NwfIpciMcQQoBZjoibytUAPy_JoOIoxd2T9MxsF0r8SO6U7RZNU0x_JVWXPpsS4ZFGhyVX87BA1UercfuKhF_Bnko3BJOI-52coabat7X6u34cB03UD79X7vVx412enSeMgYBux0eDENRk2laJgNoBh5PzYdFKAyKxaxz35tUTBJ_dyKilx4fv0lYjiktSJTzzQa0ivvhtSbLeRxxd0DeLFQpQ08ju9denhxaqXkGCeYF2pw7XlvBc2b-UwL_1hbsU1JPkqBkB7QxXGyrI5bKLu9kC3H3n68"
access_token = spotify_actions.getuserToken(code)
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
dict = {
    "uris":[uri]
}
response = requests.post(url, headers=headers, data=json.dumps(dict))


class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_access_token(self):
        # Make a request to Spotify API to get the access token
        url = "https://accounts.spotify.com/api/token"
        headers = {"Authorization": "Basic " + base64.b64encode((self.client_id + ":" + self.client_secret).encode()).decode()}
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data)
        access_token = response.json()["access_token"]
        return access_token

    def add_tracks_to_playlist(self, playlist_id, track_uris):
        access_token = self.get_access_token()

        # URL for adding tracks to a playlist
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        # Headers for authorization
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Data payload containing the track URIs
        data = {
            "uris": track_uris
        }

        # Make a POST request to add tracks to the playlist
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Check response status
        if response.status_code == 201:
            print("Tracks added to playlist successfully!")
        else:
            print("Error adding tracks to playlist:", response.status_code)

# Example usage:

playlist_id = "4oLh6CXQGaXgbAGuNeV4RA"
track_uris = ["spotify:track:4hZi9952OTtYQnXo2FJT6C", "spotify:track:1BpKJw4RZxaFB88NE5uxXf"]

spotify_api = SpotifyAPI(client_id, client_secret)
spotify_api.add_tracks_to_playlist(playlist_id, track_uris)
