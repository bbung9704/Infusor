import React, { useState, useRef } from "react";
import axios from "axios";

import serviceUrl from "../utils/Utils";

import '../css/Video.css'

const Video = () => {
    const [imageObject, setImageObject] = useState(
        {
            imagePreview: "https://via.placeholder.com/480.jpg",
            imageFile: "",
        }
    );

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

    // 이미지 업로드
    const postImage = () => {
        const formData = new FormData()
        formData.append("file", imageObject.imageFile)
        axios.post(serviceUrl + "/upload", formData)
            .then((response) => {
                // setReturnedImage(response.data);
                setImageObject({
                    ...imageObject,
                    imagePreview: "data:image/jpeg;base64," + response.data
                })
            })
            .catch((e) => {
                alert(e.response.data.message);
                setImageObject({
                    imagePreview: "https://via.placeholder.com/480.jpg",
                    imageFile: "",
                });
            })
    };

    return (
        <div className="container">
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
            <div>
                <img className="captured-img" src={imageObject.imagePreview} alt="result1" />
            </div>
            <div className="btn-box">
                <button onClick={handleClick}>촬영</button>
                {imageObject.imageFile && <button onClick={postImage}>업로드</button>}
            </div>
        </div>
    );
}

export default Video;