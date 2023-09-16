import '../css/Button.css';

const CircleButton = ({fn, icon}) => {

    return (
        <button onClick={fn} className="camera-button">
            <img src={icon} id="camera-icon" alt='camera-icon' />
        </button>
    );
};

export default CircleButton;
