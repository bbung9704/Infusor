import React from "react";
import {Routes, Route, Link} from 'react-router-dom'

import Media from "./pages/Media";

import './App.css'

function App() {
  return (
    <div className="App">
      <nav className="top-nav">
        <Link to="/"><h3>Infusor</h3></Link>
        <div id='myname'>taeyoon.kim</div>
      </nav>
      <Routes>
        <Route path="/" element={<Media />} />
      </Routes>
    </div>
  );
}

export default App;
