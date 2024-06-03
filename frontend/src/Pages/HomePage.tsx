import PlaylistForm from './Components/form.tsx';
import React, {useState, useEffect} from 'react'
import PlaylistCard from './Components/PlaylistCard.tsx'
import 'slick-carousel/slick/slick.css'
import 'slick-carousel/slick/slick-theme.css'
import NavBar from './Components/NavBar.tsx'
import './HomePage.css';



function HomePage() {
  //SUBMIT button functionality:
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);


    const [formData, setFormData] = useState({
      toSend : ''
    })
    const formChange = (event) => {
      const { value } = event.target; // Extract value from the input field
      setFormData({ ...formData, toSend: value }); // Update formData state with the new value
  };

  
  const [playlists, setPlaylists] = useState([]);
  
    const buttonPress = async (e) => {
      e.preventDefault();
      setIsButtonDisabled(true); //disabling it right now so that it is enabled once the rest of the method runs.
      try {
        const response = await fetch('http://localhost:5000/data', {
          method: 'POST', //fetching the playlist data from the backend api
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
        sessionStorage.setItem("savedData",JSON.stringify(playlists))
      } catch (error) {
        console.error('Error sending data:', error);
      }
      setIsButtonDisabled(false) //re enabling the button now that the whole method has finished running.
    };

    const spotifyRedirectButton = async () => { //redirects to spotify user authentication page upon being clicked.
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

    return ( //page structure.
      <>
    <div className='changeColour'>
      <NavBar/>
      <PlaylistForm onSubmit={buttonPress} onChange={formChange} id = "he"/>
      <div className="playlist-container">
        {playlists.map((playlist, index) => ( //iterating through the playlist data to build the cards.
          <PlaylistCard
            key={index} 
            image={playlist.image}
            description={playlist.description}
            title={playlist.title}
            tracks={playlist.tracks}
          >
          </PlaylistCard>
        ))}
      </div>
      <div><button disabled={isButtonDisabled}  onClick={spotifyRedirectButton} type="button" className='btn btn-warning'  style={{align: "center"}}>Grant Spotify Permissions</button></div>
    </div>
      </>
    );
  }

export default HomePage;