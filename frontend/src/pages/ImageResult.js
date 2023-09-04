import React from "react";
import { useLocation } from "react-router-dom";

const ImageResult = () => {
    const location = useLocation();

    return (
        <div>
            <h1>Result</h1>
            <img src={location.state.img} alt="result" />
        </div>
    )
}

export default ImageResult;