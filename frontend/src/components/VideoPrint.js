import scanning from '../images/scanning.png'

const VideoPrint = ({showVideo, videoRef, capturedPhoto}) => {

    return (
        <div className="video-container">
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
                    </div>
                )}
                {showVideo ? (<img src={scanning} alt="Overlay_Image" className="overlay-scan" />) : null}
            </div>
    );
};

export default VideoPrint;
