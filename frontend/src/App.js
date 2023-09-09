import React from "react";
import {Routes, Route} from 'react-router-dom'

import Home from "./pages/Home"
import WebCam from "./pages/WebCam"
import ImageResult from "./pages/ImageResult"
import Video from "./pages/Video";

function App() {
  return (
    <div className="App">
      {/* <nav>
        <Link to="/">Home</Link> | <Link to="/webcam">WebCam</Link>
      </nav> */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/webcam" element={<WebCam />} />
        <Route path="/result" element={<ImageResult />} />
        <Route path="/video" element={<Video />} />
      </Routes>
    </div>
  );
}

export default App;
