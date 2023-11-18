import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import serviceUrl from "../utils/Utils";
import "../css/List.css";

// components
import ListCard from '../components/ListCard';
import CircleButton from '../components/CircleButton';

// icons
import toTheTop from "../images/arrowhead-up.png";
import toTheBack from "../images/left.png";

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

    const navigate = useNavigate();
    const moveToBack = () => {
        navigate('/');
    };

    const moveToTop = () => {
        window.scrollTo({top: 0, behavior: "smooth"});
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
            <div className='list-fixed-btn'>
                <div className='fixed-btn-left'>
                    <CircleButton fn={moveToBack} icon={toTheBack} />
                </div>
                <div className='fixed-btn-right'>
                    <CircleButton fn={moveToTop} icon={toTheTop} />
                </div>
            </div>
        </div>
    );
};

export default List;
