import VideoPrint from './VideoPrint';

const VideoPrintCard = ({showVideo, videoRef, capturedPhoto, processTime, isLoading}) => {

    return (
        <div className="video-container-box">
            <div className='video-container-box-title'>
                <div>Infusor Segmentation</div>
                <div>{'응답시간: ' + (processTime * 0.001).toFixed(3).toString() + 's'}</div>
            </div>
            <VideoPrint showVideo={showVideo} videoRef={videoRef} capturedPhoto={capturedPhoto} isLoading={isLoading} />
            <div className='video-container-box-bottom'>
                <ul className='text-item' >📸 최대한 가이드에 맞춰서 촬영해 주세요</ul>
                <ul className='text-item'>💡 밝은 곳에서 촬영해 주세요</ul>
            </div>
        </div>
    );
};

export default VideoPrintCard;
