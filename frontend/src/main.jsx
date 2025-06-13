import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

import axios from 'axios';

// Global axios defaults
axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
