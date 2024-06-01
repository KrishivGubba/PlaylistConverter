import React, { useState, useRef } from 'react';

interface Props {
  children: string;
  title: string;
  image: string;
  description: string;
  tracks: { [key: string]: string[] };
}

const PopupList = ({ items }) => {
  return (
    <div className="popup-list">
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
};

const PlaylistCard = ({ children, title, description, image, tracks }: Props) => {
  const [showList, setShowList] = useState(false);
  const [imageSrc, setImageSrc] = useState(image);
  const fileInputRef = useRef(null);

  const items = ["TRACKS:"];
  for (let i = 0; i < Object.entries(tracks).length; i++) {
    items.push(Object.entries(tracks)[i][0]);
  }

  const togglePopup = () => {
    setShowList(!showList);
  };

  const handleImageClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImageSrc(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="card" style={{ width: '300px' }}>
      <img
        src={imageSrc}
        className="card-img-top"
        style={{ width: '100%', cursor: 'pointer' }}
        onClick={handleImageClick}
      />
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
        accept="image/*"
      />
      <div className="card-body">
        <h5 className="card-title">{title}</h5>
        <p className="card-text">{description}</p>
        <a href="#" className="btn btn-primary" onClick={togglePopup}>
          Show all tracks
        </a>
        {showList && <PopupList items={items} />}
      </div>
    </div>
  );
};

export default PlaylistCard;
