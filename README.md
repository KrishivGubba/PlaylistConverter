# YouTube to Spotify Playlist Transfer

This project allows you to transfer playlists from YouTube Music to Spotify. By using the YouTube Music API and Spotify API, the application retrieves a playlist from a YouTube Music account, searches for the songs on Spotify, retrieves their Spotify IDs, creates a new playlist on Spotify, and adds the songs to this new playlist.

## How it Works

1. User input
   The user inputs the unique playlist id that is associated with each playlist on Youtube Music. The data (song names and artists for each song) is saved.
   
   ![image](https://github.com/KrishivGubba/PlaylistConverter/assets/158531751/16ba3425-a6e4-4379-9787-70e2903acd9f)
3. Spotify Authentication
   
   To access and make changes within a user's account on spotify, one must grant certain permissions. The next steps only proceed if the user grants access to the web app.
5. Song lookup
   
   Using the previously saved data of each playlist, a search query that is of the following format: "(songname) + (artist)" is provided to the Spotify API. This gives us the unique track id
   that for the song on spotify.
7. Playlist creation and song additions
   
   The playlist is created, and songs are added one by one using the Spotify API.

