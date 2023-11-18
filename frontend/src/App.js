import React from "react";
import {Routes, Route, Link} from 'react-router-dom'

import Media from "./pages/Media";

import './App.css'
import List from "./pages/List";

function App() {
  return (
    <div className="App">
      <nav className="top-nav">
        <Link to="/"><h3>Infusor</h3></Link>
        <div id='myname'>taeyoon.kim</div>
      </nav>
      <Routes>
        <Route path="/" element={<Media />} />
        <Route path="test/" element={<List />} />
      </Routes>
    </div>
  );
}

export default App;
