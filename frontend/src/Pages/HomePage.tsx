import logo from './logo.svg';
// import './App.css';
import PlaylistForm from './Components/form.tsx';
import Button from './Components/Button.tsx'
import React, {useState, useEffect} from 'react'
import PlaylistCard from './Components/PlaylistCard.tsx'
// import './index.js'
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css'
import 'slick-carousel/slick/slick-theme.css'
import { buildQueries } from '@testing-library/react';
// import './PlaylistCard.css'; // Import CSS file with styles
import NavBar from './Components/NavBar.tsx'
import {BrowserRouter, Route, Routes} from 'react-router-dom'
// import Help from './pages/Help'
import './HomePage.css';



function HomePage() {
  //SUBMIT button functionality:
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);


    const [formData, setFormData] = useState({
      toSend : ''
    })
    const formChange = (event) => {
      // console.log(formData)
      const { value } = event.target; // Extract value from the input field
      setFormData({ ...formData, toSend: value }); // Update formData state with the new value
  };

  
  const [playlists, setPlaylists] = useState([]);
  
    const buttonPress = async (e) => {
      e.preventDefault();
      setIsButtonDisabled(true); //disabling it right now so that it is enabled once the rest of the method runs.
      try {
        const response = await fetch('http://localhost:5000/data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData.toSend)
        });
        if (!response.ok) {
          throw new Error('Failed to send data');
        }
        console.log('Data sent successfully');
        console.log(playlists)
        setPlaylists(await response.json())
        //need a for loop to print this out.
        // console.log(playlists[0])
        console.log(playlists)
        sessionStorage.setItem("savedData",JSON.stringify(playlists))
        const savedDataString = sessionStorage.getItem('savedData');
        console.log(JSON.parse(savedDataString)); //stupid error you can completely ignore it.
        
      } catch (error) {
        console.error('Error sending data:', error);
      }
      setIsButtonDisabled(false) //re enabling the button now that the whole method has finished running.
    };

    const spotifyRedirectButton = async () => {
      try {
        const response = await fetch('http://localhost:5000/spotify_redirect_url');
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        const result = await response.json();
        window.location.href = result;
      } catch (error) {
        console.log("error has occurred.")
      } 
    };

    return (
      <>
    <div className='changeColour'>
      <NavBar/>
      <PlaylistForm onSubmit={buttonPress} onChange={formChange} id = "he"/>
      <div className="playlist-container">
        {playlists.map((playlist, index) => (
          <PlaylistCard
            key={index} // Provide a unique key for each PlaylistCard
            image={playlist.image}
            description={playlist.description}
            title={playlist.title}
            tracks={playlist.tracks}
          >
            {/* You can render additional content inside PlaylistCard if needed */}
          </PlaylistCard>
        ))}
      </div>
      <div><button disabled={isButtonDisabled}  onClick={spotifyRedirectButton} type="button" className='btn btn-warning'  style={{align: "center"}}>Grant Spotify Permissions</button></div>
    </div>
      </>
    );
  }





export default HomePage;