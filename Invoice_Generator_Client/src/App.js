import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {commonHeader} from './/common/header.jsx';
import InvoiceInput from './common/InvoiceInput.jsx';

function App() {
    const [message, setMessage] = useState("");
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