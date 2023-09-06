import React from "react";
import axios from "axios";

import Webcam from "react-webcam";
import serviceUrl from "../utils/Utils";
import '../css/WebCam.css'



const WebCam = () => {
    const webcamRef = React.useRef(null);
    const [imgSrc, setImgSrc] = React.useState(null);
    const [facingMode, setFacingMode] = React.useState("environment");

    const videoConstraints = {
        aspectRatio: 1,
        facingMode: facingMode
    };

    // 캡쳐
    const capture = React.useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        setImgSrc(imageSrc);
    }, [webcamRef]);


    // 다시찍기
    const retake = () => {
        setImgSrc(null);
    };

    const changeCamera = () => {
        setFacingMode((prevState) => prevState === "environment" ? "user" : "environment")
    };

    // 이미지 업로드
    const postImage = () => {
        const formData = new FormData()
        formData.append("file", imgSrc)

        axios.post(serviceUrl + "/upload", {
            "file": imgSrc
        })
            .then((response) => { console.log(response.data.message) })
            .catch((e) => console.log(e))
    };

    // 반응형 카메라 크기조절
    const [windowSize, setWindowSize] = React.useState({
        width: undefined,
        height: undefined,
    });

    React.useEffect(() => {
        const handleResize = () => {
            setWindowSize({
                width: window.innerWidth,
                height: window.innerHeight,
            })
        };
        window.addEventListener("resize", handleResize);

        handleResize();
    }, []);



    return (
        <div className="container">
            {imgSrc ? (
                <div>
                    <div className="img-screen">
                        <img src={imgSrc} alt="webcam" />
                    </div>
                    <button className="capture" onClick={retake}>Retake</button>
                    <button className="post" onClick={postImage}>Send</button>
                </div>
            ) : (
                <div>
                    <div className="img-screen">
                        <Webcam
                            videoConstraints={videoConstraints}
                            width={windowSize.height >= windowSize.width ? windowSize.width : windowSize.height}
                            audio={false}
                            ref={webcamRef}
                            screenshotFormat="image/jpeg"
                        />
                    </div>
                    <button className="capture" onClick={capture}>Capture</button>
                    <button className="post" onClick={changeCamera}>Change</button>
                </div>
            )}
            <button className="back" onClick={() => { window.location.href = "/" }}>Back</button>
        </div>
    );
};

export default WebCam;
