import React from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import serviceUrl from "../utils/Utils";
import '../css/Home.css';

const Home = () => {
    const [res, setResponse] = React.useState(null);

    const getMethod = () => {
        axios.get(serviceUrl)
        .then((response) => { setResponse(response.data) })
        .catch((e) => { setResponse( e.message ) })
        .finally(() => {})
    };

    return (
        <div className="main">
            <h1>Infusor</h1>
            <div className="start-btn">
                <button onClick={ getMethod }>Network Test</button>
                <button><Link to="/webcam">Camera</Link></button>
            </div>
            <div>{res}</div>
        </div>
    );
}

export default Home;

