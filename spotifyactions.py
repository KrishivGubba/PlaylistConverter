import requests
import base64
import json
from urllib.parse import urlencode
from requests import get
import spotipy
from spotipy.oauth2 import SpotifyOAuth


songs = {'ILoveUIHateU': [{'name': 'Playboi Carti'}], 'Over': [{'name': 'Playboi Carti'}], 'R.I.P.': [{'name': 'Playboi Carti'}],
         'Die4Guy': [{'name': 'Playboi Carti'}], 'FE!N (feat. Playboi Carti)': [{'name': 'Travis Scott'}, {'name': 'Playboi Carti'}],
         'Not PLaying': [{'name': 'Playboi Carti'}], 'Long Time - Intro': [{'name': 'Playboi Carti'}],
         'Rockstar Made': [{'name': 'Playboi Carti'}], 'Vamp Anthem': [{'name': 'Playboi Carti'}],
         'Foreign': [{'name': 'Playboi Carti'}], 'Location': [{'name': 'Playboi Carti'}],
         'Stop Breathing': [{'name': 'Playboi Carti'}], 'Fell In Luv (feat. Bryson Tiller)': [{'name': 'Playboi Carti'}, {'name': 'Bryson Tiller'}],
         'Flex': [{'name': 'Playboi Carti'}, {'name': 'Leven Kali'}], 'R.I.P. Fredo (feat. Young Nudy) - Notice Me': [{'name': 'Playboi Carti'},
        {'name': 'Young Nudy'}], 'Sky': [{'name': 'Playboi Carti'}], 'Lean 4 Real (feat. Skepta)': [{'name': 'Playboi Carti'}, {'name': 'Skepta'}],
         'Go2DaMoon (feat. Kanye West)': [{'name': 'Playboi Carti'}, {'name': 'Kanye West'}], 'Yah Mean': [{'name': 'Playboi Carti'}],
         'On That Time': [{'name': 'Playboi Carti'}], 'FlatBed Freestyle': [{'name': 'Playboi Carti'}], 'Meh': [{'name': 'Playboi Carti'}],
         'Beef': [{'name': 'Ethereal'}, {'name': 'Playboi Carti'}], 'Let It Go': [{'name': 'Playboi Carti'}], 'New Tank': [{'name': 'Playboi Carti'}],
         'Place': [{'name': 'Playboi Carti'}], 'Love Hurts (feat. Travis Scott)': [{'name': 'Playboi Carti'}, {'name': 'Travis Scott'}],
         'Beno!': [{'name': 'Playboi Carti'}], 'New Choppa': [{'name': 'Playboi Carti'}, {'name': 'A$AP Rocky'}],
         'Home (KOD)': [{'name': 'Playboi Carti'}], "Choppa Won't Miss (feat. Young Thug)": [{'name': 'Playboi Carti'}, {'name': 'Young Thug'}],
         "Right Now (feat. Pi'erre Bourne)": [{'name': 'Playboi Carti'}, {'name': 'Pi’erre Bourne'}], 'New N3on': [{'name': 'Playboi Carti'}]}





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
        data = {"grant_type": "client_credentials",
                "scope": "playlist-modify-public playlist-modify-private"  # Add the required scopes here
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
        print(final)
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

    def new_add(self,playlistid,ids,userid):
        scope = "playlist-modify-public"

        token = SpotifyOAuth(scope=scope, username=userid,
                             client_id=self.client_id,
                             client_secret=self.client_secret,
                             redirect_uri="http://localhost:3000/spotify_redirect")
        spotifyobj = spotipy.Spotify(auth_manager=token)

        # spotifyobj.playlist_add_items(playlist_id=playlistid,
        #                               items=ids)
        print("this is the current user", spotifyobj.current_user())

    def getUserID(self, access_token):
        url = "https://api.spotify.com/v1/me"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

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


        # playlist_data = response.json()
        # playlist_id = playlist_data["id"]


new  = SpotifyActions("799f8ff7f87241c391b9c87d7a2bd5a8","d8ea189405cc433da7c4c849d165e49c")

# someting = "BQBNzCKfTx9YCUlUiIwUgpZeX5yvcxyv9N64ogEWt83WPXzXEqetX6a-wle6D-ZK3jYjm-ZENDfXCAVjppQ4FkBr2mijoCrB935pW5br6Fp4ByOedIJAn6Metho4VboKrcIcYZb1smOUs_-CtjjSgSDQ9fbhN1IF_lVprR3bsc02jZ8KzkKg5bk8RGu_9wQLHIHdTf4gOADSCH9oYR3nYFX8OoEPmaZ7tXoLHJNSJE23tsh6Qzj2RKNm7frxGQjWmeTLKrNkVPrs2P4R8qh6TchVpw"
# new.search_song("rapstar","polo g")
# token = new.getuserToken(new.userAuth())

# lst = []
# for key in songs:
#     songname = ""
#     artist = ""
#     songname = key
#     for dict in songs[key]:
#         artist += dict["name"] + " "
#     id = new.search_song(token,songname,artist)
#     lst.append(id)
#
# print(lst)
# new.create_playlist("k4rizkoy0o6o8feiri9agz9m4","token","carit")

# ids  = ['1BpKJw4RZxaFB88NE5uxXf', '08dz3ygXyFur6bL7Au8u8J', '29TPjc8wxfz4XMn21O7VsZ', '7rbalRuIx7sIXFHYTphE0n', '42VsgItocQwOQC3XWZ8JNA', '3L0IKstjUgDFVQAbQIRZRv', '54g08crXuFrb6m2M2MwR4x', '3cWmqvMwVQKDigWLSZ3w9h', '4CzhtKifG867Lu5DNQVBSA', '500l6Cwe40hkPqS7Sf7ufY', '3yk7PJnryiJ8mAPqsrujzf', '2lLG56qpLP3UbcLuzMvkWX', '1s9DTymg5UQrdorZf43JQm', '2xyBvir9n474qfsOkxXMgx', '45Ln3F9PRPYTXBcMFkZMzS', '29TPjc8wxfz4XMn21O7VsZ', '1JgkiUg9mSXSwcb5Gbi4Ur', '0F13K9dwYH2zpTWiR8d628', '5MUxrNd7Gr2HksLcAlB0IO', '3dl8bSF08LQfCf4T6CCksf', '5nayhWICkQGMTkisxVMbRw', '15JRvf02KKGHKgC31jrpuh', '47Obor5zpUwTRLEQIX9woV', '23QyE9GQpXsX9WgEDADMa6', '4txKMpsSfZRV6durPuHVq0', '4IO2X2YoXoUMv0M2rwomLC', '3K6U7TamNyVSWcFH8pCQHX', '4CYTQpr2jc4uBScYvpEK2w', '30sc425JEvj3tgmGAKORea', '5wPyd3IQAZft1vmxoIqGrU', '5O9zs6G6RcB6yP1OKwnwiM', '475jSz0H6U3duJyNiDS0tT', '7ejepEh5DJ79YI6owGRfkk']
# new.add_songs_to_playlist("3pDRcLIFtdcU6OqBEJJfXt","AQDwqSKhrOtHaszecvSAj6Duc9uuzn3htwApL4WeTnFu1its_D4HaINxlH6p-GjDpNCE9xp3HNwkYbFxHgAa8d9SNnzOFO5Tvc9HqDoUr33lVzDyn0F2e3BZIWVbGipXBJsQL-ghOj1CkM6egevQBgqwnxWbmgIDzba7Q1Mr2cHH_8zyXujDOhoqXSXWZJiNP1LXosWFTFN3jC10Z9pmX21jUd52usl88KU6CTMhuaChtOXQV6c_ygoLMSrKgFY9koJyDlmstdHT_jC3GpabX80Jl0YHDTTsHPCKRcC_BMuwZV-Ry3vHKX_LH4ilVVOCROeSa_gtmppHOpD1dOJXgqDWGsNBnV05EDbIm2dxbGbcYvg",["1BpKJw4RZxaFB88NE5uxXf"])

CLIENT_ID = "799f8ff7f87241c391b9c87d7a2bd5a8"
CLIENT_SECRET = "d8ea189405cc433da7c4c849d165e49c"
spot = SpotifyActions(CLIENT_ID, CLIENT_SECRET)
token = spot.get_token()
