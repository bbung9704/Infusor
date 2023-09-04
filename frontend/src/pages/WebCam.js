import React from "react";
import { Link } from "react-router-dom";
import Webcam from "react-webcam";
import axios from "axios";

import '../css/WebCam.css'

const WebCam = () => {
    const webcamRef = React.useRef(null);
    const [imgSrc, setImgSrc] = React.useState(null);
    
    // 캡쳐
    const capture = React.useCallback(() => {
            const imageSrc = webcamRef.current.getScreenshot();
            setImgSrc(imageSrc);
        }, [webcamRef]);
    

    // 다시찍기
    const retake = () => {
        setImgSrc(null);
    };

    // 이미지 업로드
    const postImage = () => {
        const formData = new FormData()
        formData.append("file", imgSrc)
        
        axios.post("http://infusor.store/api/upload", {
            "file": imgSrc
        })
        .then((response) => { console.log(response.data.message)})
        .catch((e) => console.log(e))
    };

    

    return (
        <div>
            { imgSrc ? (
                <div>
                    <img src={imgSrc} alt="webcam" />
                    <button onClick={retake}>Retake Photo</button>
                    <Link to="/result" state={{img: imgSrc}}>
                    <button onClick={ postImage }>Send Photo</button>
                    </Link>
                </div>
                ) : (
                    <div className="webcam">
                    <Webcam 
                    audio={false}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg" 
                    />
                    <button onClick={capture}>Capture Photo</button>
                </div>
                )}
        </div>
    );
};

export default WebCam;
