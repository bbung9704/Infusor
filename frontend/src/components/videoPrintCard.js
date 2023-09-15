import VideoPrint from './videoPrint';

const VideoPrintCard = ({showVideo, videoRef, capturedPhoto}) => {

    return (
        <div className="video-container-box">
            <div className='video-container-box-title'>
                <div>QR Code Scanner</div>
                <div>Status</div>
            </div>
            <VideoPrint showVideo={showVideo} videoRef={videoRef} capturedPhoto={capturedPhoto} />
            <div className='video-container-box-bottom'>
                <ul className='text-item' >📸 최대한 가이드에 맞춰서 촬영해 주세요</ul>
                <ul className='text-item'>💡 밝은 곳에서 촬영해 주세요</ul>
            </div>
        </div>
    );
};

export default VideoPrintCard;