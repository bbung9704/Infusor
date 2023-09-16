import React from "react";
import {Routes, Route, Link} from 'react-router-dom'

import Home from "./pages/Home"
import Media from "./pages/Media";
import Test from "./pages/Test";

import './App.css'

function App() {
  return (
    <div className="App">
      <nav className="top-nav">
        <Link to="/"><h3>Infusor</h3></Link>
        <div id='myname'>taeyoon.kim</div>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/media" element={<Media />} />
        <Route path="/test" element={<Test />} />
      </Routes>
    </div>
  );
}

export default App;
