import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App';
import Exam from './Exam';
import Rules from './Rules';
import './index.css';
import Signup from './Signup';
import Login from './Login';
import PrivateRoute from './PrivateRoute'; // Import the PrivateRoute

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        {/* Private routes */}
        <Route path="/exam" element={<PrivateRoute element={Exam} />} />
        <Route path="/rules" element={<PrivateRoute element={Rules} />} />
      </Routes>
    </Router>
  </React.StrictMode>
);
