import React from "react";
import {Routes, Route, Link} from 'react-router-dom'

import Home from "./pages/Home"
import Video from "./pages/Video";
import WebCam from "./pages/WebCame";

import './App.css'

function App() {
  return (
    <div className="App">
      <nav className="top-nav">
        <Link to="/" className="nav-item">Home</Link>
        <Link to="/video" className="nav-item">Video</Link>
        <Link to="/webcam" className="nav-item">Webcam</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/video" element={<Video />} />
        <Route path="/webcam" element={<WebCam />} />
      </Routes>
    </div>
  );
}

export default App;
