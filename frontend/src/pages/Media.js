import React, { useRef, useEffect, useState } from 'react';
import axios from "axios";
import serviceUrl from "../utils/Utils";
import "../css/Media.css";
import scanning from '../images/scanning.png'

const constraints = {
    video: {
        facingMode: 'environment',
        width: { ideal: 4096 }, // 원하는 가로 해상도
        height: { ideal: 2160 }, // 원하는 세로 해상도
        aspectRatio: 3 / 4.
    },
};

const Media = () => {
    const videoRef = useRef(null);
    const videoContainerRef = useRef(null);
    const canvasRef = useRef(null);
    const [capturedPhoto, setCapturedPhoto] = useState(null);
    const [showVideo, setShowVideo] = useState(true);

    useEffect(() => {
        navigator.mediaDevices
            .getUserMedia(constraints)
            .then((stream) => {
                videoRef.current.srcObject = stream;
            })
            .catch((error) => {
                console.error('Error accessing the webcam:', error);
            });
    }, [showVideo]);

    const capturePhoto = () => {
        const video = videoRef.current;
        const canvas = canvasRef.current;

        if (video && canvas) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            // 캡처한 이미지를 데이터 URL로 저장
            const photoDataUrl = canvas.toDataURL('image/jpeg');
            console.log(photoDataUrl);
            setCapturedPhoto(photoDataUrl);
            setShowVideo(false); // 비디오 숨기기
        }
    };

    const showVideoAgain = () => {
        setShowVideo(true);
        setCapturedPhoto(null); // 이미지 제거는 비디오를 다시 보이게 한 다음에 수행
    };

    const postImage = () => {
        axios.post(serviceUrl + "/uploadtest", { data: capturedPhoto.split(',', 2)[1] })
            .then((response) => {
                setCapturedPhoto("data:image/jpeg;base64," + response.data);
                alert("Transformed image returned")
            })
            .catch((e) => {
                alert(e.response.data.message);
            })
    };

    return (
        <div className="App">
            <div className="video-container" ref={videoContainerRef}>
                {showVideo ? (
                    <div>
                        <video
                            className="video-print"
                            ref={videoRef}
                            autoPlay
                            playsInline
                            muted
                        />
                    </div>
                ) : (
                    <div>
                        <img
                            className="video-print"
                            src={capturedPhoto}
                            alt="Captured"
                        />
                        {/* <button onClick={showVideoAgain} className='fixed-btn'>Show Video Again</button> */}
                    </div>
                )}
                {showVideo ? (<img src={scanning} alt="Overlay_Image" className="overlay-scan" />) : null}
            </div>
            <div className='fixed-btn'>
                {showVideo ? <button onClick={capturePhoto} className='camera-button'>Capture Photo</button> : (<div>
                    <button onClick={postImage} className='camera-button'>Upload Photo</button>
                    <button onClick={showVideoAgain} className='camera-button'>Retake Photo</button>
                </div>)}
            </div>
            <canvas ref={canvasRef} style={{ display: 'none' }} />
        </div>
    );
};

export default Media;
