// import logo from './logo.svg';
// import './App.css';
// import PlaylistForm from './Pages/form.tsx';
// import Button from './Pages/Button.tsx'
// import React, {useState, useEffect} from 'react'
// import PlaylistCard from './PlaylistCard.tsx'
// import './index.js'
// import Slider from 'react-slick';
// import 'slick-carousel/slick/slick.css'
// import 'slick-carousel/slick/slick-theme.css'
// import { buildQueries } from '@testing-library/react';
// import './PlaylistCard.css'; // Import CSS file with styles
// import NavBar from './Pages/NavBar.tsx'
// import {BrowserRouter, Route, Routes} from 'react-router-dom'
// import {Help} from './pages'




// function App() {
//   const [formData, setFormData] = useState({
//     toSend : ''
//   })
//   const formChange = (event) => {
//     // console.log(formData)
//     const { value } = event.target; // Extract value from the input field
//     setFormData({ ...formData, toSend: value }); // Update formData state with the new value
// };

// const [playlists, setPlaylists] = useState([]);

//   const buttonPress = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await fetch('http://localhost:5000/data', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(formData.toSend)
//       });
//       if (!response.ok) {
//         throw new Error('Failed to send data');
//       }
//       console.log('Data sent successfully');
//       setPlaylists(await response.json())
//       console.log(playlists)
      
//     } catch (error) {
//       console.error('Error sending data:', error);
//     }
//   };

//   return (
//     <>
//     <div className='changeColour'>
//       <NavBar/>
//       <PlaylistForm onSubmit={buttonPress} onChange={formChange} id = "he"/>
//       <div className="playlist-container">
//         {playlists.map((playlist, index) => (
//           <PlaylistCard
//             key={index} // Provide a unique key for each PlaylistCard
//             image={playlist.image}
//             description={playlist.description}
//             title={playlist.title}
//             tracks={playlist.tracks}
//           >
//             {/* You can render additional content inside PlaylistCard if needed */}
//           </PlaylistCard>
//         ))}
//       </div>
//     </div>
//     </>
//   );
// }

// export default App;








//   // const handleChange = (e) => {
//   //   console.log(e.target) //e.target is of the form of something like this: <input type="text" name="name" placeholder="Name" value="qw" fdprocessedid="80828d"> with a name and value
//   //   const { name, value } = e.target;// now you are making variables with the names name, value that will have the data that is attached to "name" and "value" in e.target.
//   //   console.log(name) //if you change the field "ENTERNAME" then this variable name will be name. Else, if you changed the field "ENTERAGE" the field name will be age.
//   //   console.log(value) //this is just the value of what the entry box was last changed to.
//   //   setFormData({ ...formData, [name]: value }); //by using the ...formData syntax, you are PRESERVING all of the formData, and [name]:value is only changing the in formData hashmap that has to be.
//   // };