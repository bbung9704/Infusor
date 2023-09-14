import React from "react";
import {Routes, Route, Link} from 'react-router-dom'

import Home from "./pages/Home"
import Media from "./pages/Media";

import './App.css'

function App() {
  return (
    <div className="App">
      <nav className="top-nav">
        <Link to="/" className="nav-item">Home</Link>
        <Link to="/media" className="nav-item">Camera</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/media" element={<Media />} />
      </Routes>
    </div>
  );
}

export default App;
