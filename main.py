from flask import Flask, redirect, request, render_template, session, jsonify
from spotifyactions import SpotifyActions
from dotenv import load_dotenv
import os
from ytmus import youtubemusic
from flask_cors import CORS
from urllib.parse import urlparse, parse_qs

#creating the object that will get data off of youtube music.
tube = youtubemusic()

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
print("this is the client id",client_id)
app = Flask(__name__)
CORS(app)
app.secret_key = 'ration'
spotify_actions = SpotifyActions(client_id, client_secret)
global playlist_ids
playlist_ids = []

#this method will receive the spotify auth code and then generate the access token and then creat the playlists.
@app.route('/spotify_callback', methods=["POST"])
def spotifycallback():
    inputData = request.json
    url = inputData[0]
    #the actual url is in inputData[0]
    #the playlists are in the form of dictionaries, situated within an array containing several dicts. so
    #use the following to access playlists: url[1][playlist_no]["dict key of playlist"]
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    code = params.get('code', [None])[0]
    # #now we generate an access token with the user code.
    access_token = spotify_actions.getuserToken(code)
    user_id = spotify_actions.getUserID(access_token=access_token)
    nameURLhashmap = {}
    for i in range(len(inputData[1])):
        output = spotify_actions.create_playlist(user_id,access_token,inputData[1][i]["title"],
                                              tube.getplaylist(inputData[1][i]["id"]),
                                              description=inputData[1][i]["description"],image=inputData[1][i]["image"])
        nameURLhashmap[i] = output
    return nameURLhashmap

@app.route('/submit', methods=['POST'])
def submit_form():
    user_id = request.form['user_id']
    playlist_name = request.form['playlist_name']
    access_token = request.form['access_token']

    tube = youtubemusic()
    data = tube.getplaylist(session["playlist_id"])
    playlist_link = spotify_actions.create_playlist(user_id,access_token,playlist_name,ytdata = data)
    # Save the user_id and playlist_name to variables or perform actions with them
    return render_template("playlistcreated.html",link_url = playlist_link)


@app.route('/authorize')
def authorize():
    # print(request.form.get("playlist_id"))
    print("hey hi ")
    print(session.get("playlist_id"))
    return redirect(spotify_actions.userAuth())

@app.route('/getplaylist',methods = ["POST","GET"])
def playlistgetter():
        return render_template("getplaylist.html")

@app.route("/")
def enterplaylists():
    # return render_template("enterplaylistid.html")
    return jsonify({"n":1, "what":[1,2,3,3]})

@app.route('/save_playlist_id', methods=['POST'])
def save_playlist_id():
    playlist_id = request.form.get('playlist_id')
    session['playlist_id'] = playlist_id
    # Here, you can save the playlist ID to a database, session, or any other storage mechanism
    # Redirect the user to the /authorize page
    return redirect('/authorize')

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    array1 = data.split(" ")
    session["playlist_ids"] = array1 #we are saving the playlist ids in a flask session so we dont have to find them again.
    playlist_ids = array1
    print("THESE ARE THE PLAYLIST IDS:", session["playlist_ids"])
    tube = youtubemusic()
    return jsonify(tube.getplaylistarray(array=array1)) 

    # print(session.get("playlistinfo"))
    # return jsonify(session.get("playlistinfo"))

@app.route('/gotdata', methods=["POST"])
def putData():
    # print(session.get("playlistinfo"))
    return jsonify({"h":"h"})

@app.route("/spotify_redirect_url", methods=["GET"])
def sendUrl():
    return jsonify(spotify_actions.userAuth())

if __name__ == '__main__':
    app.run(debug=True)
