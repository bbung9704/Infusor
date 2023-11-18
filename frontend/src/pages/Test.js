import React, { useRef, useEffect, useState } from 'react';
import axios from "axios";
import serviceUrl from "../utils/Utils";
import "../css/Media.css";



const Test = () => {
    const getPredList = () => {
        axios.get(serviceUrl + "/pred")
            .then((response) => {
                console.log(response.data[0].volume)
            })
            .catch((e) => {
                console.log(e)
            });
    };

    return (
        <div className='container'>
            <button onClick={getPredList}>Test</button>
        </div>
    );
};

export default Test;
