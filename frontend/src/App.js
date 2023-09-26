import React from "react";
import {Routes, Route, Link} from 'react-router-dom'

import Media from "./pages/Media";

import './App.css'
import Test from "./pages/Test";

function App() {
  return (
    <div className="App">
      <nav className="top-nav">
        <Link to="/"><h3>Infusor</h3></Link>
        <div id='myname'>taeyoon.kim</div>
      </nav>
      <Routes>
        <Route path="/" element={<Media />} />
        <Route path="test/" element={<Test />} />
      </Routes>
    </div>
  );
}

export default App;
