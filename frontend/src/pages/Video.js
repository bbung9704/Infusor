import React, { useRef, useState } from "react";
import '../css/Video.css'

const Video = () => {
    const [imageObject, setImageObject] = useState(null);

    const handleFileInput = useRef(null);

    const handleClick = () => {
        handleFileInput.current.click();
    };

    const handleImageChange = (event) => {
        setImageObject({
            imagePreview: URL.createObjectURL(event.target.files[0]),
            imageFile: event.target.files[0],
        });
    };

    return (
        <div>
            <button onClick={handleClick}>사진 업로드</button>
            <label>
                <input
                    style={{ display: "none" }}
                    type="file"
                    accept="image/*"
                    capture="environment"
                    ref={handleFileInput}
                    onChange={handleImageChange}
                />
            </label>
            {imageObject && <img src={imageObject.imagePreview} alt="test"/>}
        </div>
    );
}

export default Video;