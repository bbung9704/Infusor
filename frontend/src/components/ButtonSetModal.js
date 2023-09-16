import '../css/Button.css';
import CircleButton from './CircleButton';

const ButtonSetModal = ({components, isShow}) => {

    const slide = isShow ? '' : 'slide-in';
    const className = 'right-btn-set-modal ' + slide;

    return (
        <div className={className} >
            {
                components.map((component) => {
                    return (
                        <CircleButton fn={component.fn} icon={component.icon} key={component.key} />
                    );
                })
            }
        </div>
    );
};

export default ButtonSetModal;
