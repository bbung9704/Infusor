import React, { useCallback, useRef, useState, useEffect } from "react";
import Webcam from 'react-webcam';
import axios from "axios";

import "../css/WebCam.css"
import serviceUrl from "../utils/Utils";
import scanning from "../images/scanning.png"


const WebCam = () => {

    const webcamRef = useRef(null);
    const [imgSrc, setImgSrc] = useState(null);
    const [scanSrc, setScanSrc] = useState(scanning)
    const [windowSize, setWindowSize] = useState({
        width: window.innerWidth,
        height: window.innerHeight,
    });
    

    const videoConstraints = {
        facingMode: "environment",
        aspectRatio: 3/4,
    };
    
    const webcamStyle = {
        width: windowSize.width,
    };
    
    
    const captureImage = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        setImgSrc(imageSrc);
        setScanSrc(null);
    }, [webcamRef]);
    
    const retakeImage = () => {
        setImgSrc(null);
        setScanSrc(scanning);
    };

    const postImage = () => {
        axios.post(serviceUrl + "/uploadtest", { data: imgSrc.split(',', 2)[1] })
            .then((response) => {
                setImgSrc("data:image/jpeg;base64," + response.data);
            })
            .catch((e) => {
                alert(e.response.data.message);
            })
    };
    
    useEffect(() => {
        const handleResize = () => {
            setWindowSize({
                width: window.innerWidth,
                height: window.innerHeight,
            });
        };
        
        window.addEventListener('resize', handleResize);
        
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);
    
    return (
        <div>
            <div className="webcam-container">
                {imgSrc ? (
                    <img src={imgSrc} alt="webcam" className="print-image"/>
                ) : (
                    <Webcam ref={webcamRef}
                        screenshotFormat="image/jpeg"
                        videoConstraints={videoConstraints}
                        screenshotQuality={1}
                        mirrored={false}
                        // minScreenshotWidth={windowSize.width * 2}
                        // minScreenshotHeight={windowSize.width * 8/3}
                        style={webcamStyle}
                    />
                )}
                {imgSrc ? null : (<img src={scanSrc} alt="Overlay_Image" className="overlay-image" />)}
            </div>
            <div className="webcam-btn">
                {imgSrc ? (
                    <div className="btn-box">
                        <button onClick={retakeImage}>Retake photo</button>
                        <button onClick={postImage}>Upload photo</button>
                    </div>
                ) : (
                    <div className="btn-box">
                    <button onClick={captureImage} className="capture-btn">Capture photo</button>
                    </div>
                )}
            </div>
        </div>

    );
}
export default WebCam;
