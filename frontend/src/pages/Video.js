import React, { useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import serviceUrl from "../utils/Utils";

import '../css/Video.css'

const Video = () => {
    // const [imageObject, setImageObject] = useState(null);

    const handleFileInput = useRef(null);

    const imageObject = useRef(null);
    
    const handleClick = () => {
        handleFileInput.current.click();
    };
    
    // const handleImageChange = (event) => {
        //     setImageObject({
            //         imagePreview: URL.createObjectURL(event.target.files[0]),
            //         imageFile: event.target.files[0],
            //     });
            // };

    const navigate = useNavigate();
    const handleImageChange = (event) => {
        
        imageObject.current = {
            imagePreview: URL.createObjectURL(event.target.files[0]),
            imageFile: event.target.files[0],
        };
        console.log(imageObject.current.imagePreview);
        navigate('/result', { state: imageObject.current });
    };

    // 이미지 업로드
    const postImage = () => {
        const formData = new FormData()
        formData.append("file", imageObject.imageFile)

        axios.post(serviceUrl + "/uploadtest", formData)
            .then((response) => {
                console.log(response.data.message);
            })
            .catch((e) => {
                console.log(imageObject.imageFile);
                console.log(e.message);
            })
    };

    return (
        <div>
            <button onClick={handleClick}>사진 촬영</button>
            <button onClick={postImage}>업로드</button>
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
        </div>
    );
}

export default Video;