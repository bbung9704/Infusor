import React, { useRef, useEffect, useState } from 'react';
import axios from "axios";
import serviceUrl from "../utils/Utils";
import "../css/List.css";

import ListCard from '../components/ListCard';


const List = () => {
    const [predictions, setPredictions] = useState(null);

    const getPredList = () => {
        axios.get(serviceUrl + "/pred")
            .then((response) => {
                setPredictions(response.data.data)
            })
            .catch((e) => {
                console.log(e)
            });
    };

    useEffect(() => {
        getPredList();
    }, []);

    return (
        <div className='list-container'>
            {
                predictions &&
                predictions.map((prediction) => {
                    return <ListCard key={prediction.key} predictions={prediction} />
                })
            }
        </div>
    );
};

export default List;
