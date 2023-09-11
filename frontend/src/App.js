import React from "react";
import {Routes, Route, Link} from 'react-router-dom'

import Home from "./pages/Home"
import Video from "./pages/Video";

import './App.css'

function App() {
  return (
    <div className="App">
      <nav className="top-nav">
        <Link to="/" className="nav-item">Home</Link>
        <Link to="/vieo" className="nav-item">Video</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/video" element={<Video />} />
      </Routes>
    </div>
  );
}

export default App;
