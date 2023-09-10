import React, { useState } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";

import serviceUrl from "../utils/Utils";


const ImageResult = () => {
    const imageObject = useLocation();
    const [returnedImage, setReturnedImage] = useState(null);

    // 이미지 업로드
    const postImage = () => {
        const formData = new FormData()
        formData.append("file", imageObject.state.imageFile)

        axios.post(serviceUrl + "/uploadtest", formData)
            .then((response) => {
                setReturnedImage(response.data);
            })
            .catch((e) => {
                console.log(e.message);
            })
    };

    return (
        <div>
            <h1>Result</h1>
            <div>
                {imageObject && <img src={imageObject.state.imagePreview} alt="result1"/>}
                {returnedImage && <img src={"data:image/jpeg;base64," + returnedImage} alt='test' />}
            </div>
            <button onClick={ postImage }>제출</button>
        </div>
    )
}

export default ImageResult;