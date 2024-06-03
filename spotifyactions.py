import requests
import base64
import json
from urllib.parse import urlencode
from requests import get
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyActions:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def userAuth(self):
        redirect_uri = "http://localhost:3000/spotify_redirect"
        scope = "user-read-private user-read-email playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private ugc-image-upload"
        authorization_url = "https://accounts.spotify.com/authorize"
        authorization_url += "?client_id=" + self.client_id
        authorization_url += "&response_type=code"
        authorization_url += "&" + urlencode({'redirect_uri': redirect_uri})
        authorization_url += "&show_dialog=true"
        authorization_url += "&scope=" + scope
        return authorization_url

    def getuserToken(self, authcode):
        url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'authorization_code',
            'code': authcode,
            'redirect_uri': "http://localhost:3000/spotify_redirect",
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        response = requests.post(url, data=data)
        return response.json().get('access_token')

    def get_token(self):
        auth_string = self.client_id + ":" + self.client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type" : "client_credentials",
                "scope" : "playlist-modify-public playlist-modify-private"  # Add the required scopes here
                }
        result = requests.post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token

    def get_auth_header(self, token):
        return {"Authorization": "Bearer " + token}

    def get_playlist(self, id, token):
        url = f"https://api.spotify.com/v1/playlists/{id}?fields=tracks.items(track(name,artists(name)))"
        headers = self.get_auth_header(token)
        result = requests.get(url, headers=headers)
        final = json.loads(result.content)["tracks"]["items"]
        dict = {}
        for row in final:
            dict[row["track"]["name"]] = row["track"]["artists"]
        return dict

    def create_playlist(self, user_id, access_token, playlist_name, ytdata, is_public=True, description="",image= ""):
        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        headers = self.get_auth_header(access_token)
        data = {
            "name": playlist_name,
            "public": is_public,
            "description": description
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))

        alltracks = ytdata["tracks"]
        songids = []
        token = self.get_token()
        for key in alltracks:
            id = self.search_song(songname=key,artist=alltracks[key][0], token = token)
            songids.append("spotify:track:"+id)

        playlist_data = response.json()
        playlist_id = playlist_data["id"]
        url1 = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "uris": songids
        }
        response = requests.post(url1, headers=headers, data=json.dumps(data))

        if image:
            #add the code to change the image of the playlist here.
            response = requests.get(image)
            if response.status_code==200:
                image_data = response.content
            else:
                raise Exception("something went wrong with the image")
            base64_image = base64.b64encode(image_data).decode('utf-8')
            url = f"https://api.spotify.com/v1/playlists/{playlist_id}/images"
            headers = {
                 "Authorization": f"Bearer {access_token}",
                 "Content-Type": "image/jpeg"
            }
            response = requests.put(url, headers=headers, data=base64_image)
        
        return [playlist_data["name"],playlist_data['external_urls']['spotify']]

    def add_songs_to_playlist(self,playlist_id, access_token, track_uris):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        if not isinstance(track_uris, list):
            track_uris = [track_uris]
        data = {
            "uris": track_uris
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 201:
            print("Songs added to playlist successfully!")
        else:
            print("Error adding songs to playlist:", response.status_code)

    def search_song(self,token,songname,artist):
        url = "https://api.spotify.com/v1/search"
        headers = self.get_auth_header(token)
        query = f"?q={songname + artist}&type=track&limit=1"
        queryurl = url + query
        result = get(queryurl,headers = headers)
        jresult = json.loads(result.content)
        track_id = jresult['tracks']['items'][0]['uri'].split(':')[-1]
        return track_id

    def getUserID(self, access_token):
        url = "https://api.spotify.com/v1/me"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        print("HI")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx and 5xx)
            # If the request is successful, parse the JSON response
            user_details = response.json()
            return user_details["id"]
        except requests.exceptions.HTTPError as err:
            # Print the HTTP error status code and message
            print(f"HTTP error occurred: {err.response.status_code} - {err.response.reason}")
            print(f"Response content: {err.response.text}")
        except Exception as err:
            # Print any other error messages
            print(f"An error occurred: {err}")