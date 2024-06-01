import React from 'react';
import './PlaylistForm.css'; // Import CSS file with styles

interface Props {
  id: string;
  state : string;
  onSubmit: (event) => void;
  onChange : (event) => void;
}

const PlaylistForm: React.FC<Props> = ({ onSubmit, state, onChange, id }) => {

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    onSubmit(event); // Call the onSubmit function passed as prop
  };


const formChanged = (event: React.ChangeEvent<HTMLInputElement>) => {
    state = event.target.value;
    onChange(event);
    // console.log(state);
  }

  return (
    <form onSubmit={handleSubmit} className='playlist-entry'>
      <input type='text' name='playlistName' value = {state} onChange={formChanged} id = {id} placeholder='Enter IDs here.' className='playlist-input'/>
      <button className = "btn btn-danger" type="submit">Submit</button>
    </form>
  );
};

export default PlaylistForm;
