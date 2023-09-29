import scanning from '../images/scanning.png'
import spinner from '../images/spinner.gif';

const VideoPrint = ({showVideo, videoRef, capturedPhoto, isLoading}) => {

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
                            className={`video-print ${isLoading ? 'opacity' : ''}`} 
                            src={capturedPhoto}
                            alt="Captured"
                        />
                    </div>
                )}
                {showVideo ? (<img src={scanning} alt="Overlay_Image" className="overlay-scan" />) : null}
                {isLoading ? (<img src={spinner} alt="spinner" className="overlay-scan" />) : null}
            </div>
    );
};

export default VideoPrint;
