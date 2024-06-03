import React from 'react'
import NavBar from './Components/NavBar.tsx'
import './HomePage.css'
import { useState } from 'react';


function SpotifyRedirect() {
    const [playlists, setPlaylists] = useState([]);
    const ConvertPlaylists = async () =>{
       let location = window.location.href; //this is the location of the current webpage.
       //must send this location back to flask because it contains the user auth CODE that
       //can be used to create the playlist needed.
       let savedDataString = JSON.parse(sessionStorage.getItem('savedData')); //accessing session data.
       console.log(savedDataString)
       try {
        const response = await fetch('http://localhost:5000/spotify_callback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify([location, savedDataString])
        });
        if (!response.ok) {
          throw new Error('Failed to send data');
        }      
        const data = await response.json();
      console.log(data);
      setPlaylists(Object.values(data)); 
      } catch (error) {
        console.error('Error sending data:', error);
      }
    }
  return (
    <>
    <NavBar/>
    <div className="App">
    <div className="changeColour">
      <h1>Hit the button below to begin converting your playlists.</h1>
      <p>You can now enjoy your favorite music.</p>
      <button onClick={ConvertPlaylists}>Convert Playlists.</button>
      <div>
      <ul>
                {Object.keys(playlists).map((key) => (
                  <li key={key}>
                    <a href={playlists[key][1]} target="_blank" rel="noopener noreferrer">
                      {playlists[key][0]}
                    </a>
                  </li>
                ))}
              </ul>
      </div>
    </div>
  </div>
  </>
  )
}

export default SpotifyRedirect