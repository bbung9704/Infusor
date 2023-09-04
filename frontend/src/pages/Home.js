import React from "react";
import axios from "axios";

const Home = () => {
    const [res, setResponse] = React.useState(null);

    const getMethod = () => {
        axios.get("http://localhost:8000/")
        .then((response) => { setResponse(response.data) })
        .catch((e) => { setResponse( e.message ) })
        .finally(() => {})
    };

    return (
        <div>
            <h1>Home 화면 입니다.</h1>
            <button onClick={ getMethod }>Get</button>
            <h2>{ res }</h2>
        </div>
    );
}

export default Home;

