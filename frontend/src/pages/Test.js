import React from "react";
import CircleButton from "../components/CircleButton";

import cameraIcon from "../images/camera-icon.png";
import ButtonSetModal from "../components/ButtonSetModal";
import ComponentsArray from "../components/ComponentsArray";


const Test = () => {
    return (
        <div>
            <CircleButton fn={() => {}} icon={cameraIcon} />
            <ButtonSetModal components={ComponentsArray.buttonSetModalComponents}/>
            <div className="slide-in-element"></div>
        </div>
    );
}

export default Test;

