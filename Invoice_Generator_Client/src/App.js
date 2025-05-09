import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {commonHeader} from './/common/header.jsx';
import InvoiceInput from './common/InvoiceInput.jsx';

function App() {
    const [message, setMessage] = useState("");

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/hello/')
            .then(response => setMessage(response.data.message))
            .catch(error => console.error("Error fetching data:", error));
    }, []);
    return (
        <div>

            
            <commonHeader/>
            <InvoiceInput/>
            {/* <h1>Django-React App</h1>
            <p>{message}</p> */}
        </div>
    );
}
export default App;