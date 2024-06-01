import React from 'react';
import ReactDOM from 'react-dom/client';
// import './index.css';
import 'bootstrap/dist/css/bootstrap.css'
import App from './App.tsx';
import reportWebVitals from './reportWebVitals';
import './styles.css'
import {
  createBrowserRouter,
  RouterProvider,
  Route,
  Link,
} from "react-router-dom";
import HomePage from './Pages/HomePage.tsx';
import Help from './Pages/Help.tsx';
import SpotifyRedirect from './Pages/SpotifyRedirect.tsx';

const router = createBrowserRouter([
  {
   path: "/",
   element: <HomePage/>
  },
  {
    path: "help",
    element: <Help/>
  },
  {
    path:"spotify_redirect",
    element:<SpotifyRedirect/>
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router = {router}/>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
