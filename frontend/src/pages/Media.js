import React, { useRef, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import serviceUrl from "../utils/Utils";
import "../css/Media.css";

// icons
import cameraIcon from "../images/camera-icon.png";

// components
import VideoPrintCard from '../components/VideoPrintCard';
import CircleButton from '../components/CircleButton';
import ButtonSetModal from '../components/ButtonSetModal';
import ComponentsArray from '../components/ComponentsArray';

const constraints = {
    video: {
        facingMode: 'environment',
        width: { ideal: 1440 }, // 원하는 가로 해상도
        height: { ideal: 1440 }, // 원하는 세로 해상도
    },
};



const Media = () => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const navigate = useNavigate();
    const [capturedPhoto, setCapturedPhoto] = useState(null);
    const [showVideo, setShowVideo] = useState(true);
    const [processTime, setProcessTime] = useState(0);
    const [predictVolume, setPredictVolume] = useState(0);
    const [isLoading, setIsLoading] = useState(false);


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
            setCapturedPhoto(photoDataUrl);
            setShowVideo(false); // 비디오 숨기기
        }
    };

    const showVideoAgain = () => {
        setShowVideo(true);
        setCapturedPhoto(null); // 이미지 제거는 비디오를 다시 보이게 한 다음에 수행
        setProcessTime(0);
        setPredictVolume(0);
    };

    const postImage = () => {
        let start = new Date();
        setIsLoading(true);
        axios.post(serviceUrl + "/upload", { data: capturedPhoto.split(',', 2)[1] }) // binary로 변환하여 보냄.
            .then((response) => {
                setIsLoading(false);
                setCapturedPhoto(response.data.url);
                setProcessTime(new Date() - start);
                console.log(response.data.volume)
                setPredictVolume(response.data.volume);
            })
            .catch((e) => {
                setIsLoading(false);
                setProcessTime(new Date() - start);
                alert(e.response.data.message);
            });
        
    };

    const moveToList = () => {
        navigate('/test');
    }

    const fns = ComponentsArray.setButtonSetModalComponentsFn([showVideoAgain, postImage]);

    useEffect(() => {
        let videoStream = null;

        if (showVideo) {
            navigator.mediaDevices
                .getUserMedia(constraints)
                .then((stream) => {
                    videoRef.current.srcObject = stream;
                    videoStream = stream;
                })
                .catch((error) => {
                    console.error('Error accessing the webcam:', error);
                });
        }

        return () => {
            if (videoStream) {
                videoStream.getTracks()[0].stop();
                videoStream = null;
            }
        }
    }, [showVideo]);

    return (
        <div className='container'>
            <VideoPrintCard showVideo={showVideo} videoRef={videoRef} capturedPhoto={capturedPhoto} processTime={processTime} predictVolume={predictVolume} isLoading={isLoading} />
            <div className='history'>
                <div className='history-btn' onClick={moveToList}>
                    📚히스토리 보기
                </div>
            </div>
            <div className='fixed-btn'>
                {
                    <div>
                        {
                            showVideo ? (<div className='fixed-btn-prev'>
                            <CircleButton fn={capturePhoto} icon={cameraIcon} />
                        </div>) : null
                        }
                        <div className='fixed-btn-next'>
                            <ButtonSetModal components={fns} isShow={showVideo} />
                        </div>
                    </div>
                }
            </div>
            <canvas ref={canvasRef} style={{ display: 'none' }} />
        </div>
    );
};

export default Media;
