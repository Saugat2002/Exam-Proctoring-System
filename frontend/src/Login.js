import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './login.css';
import Navbar from './Navbar';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showDialog, setShowDialog] = useState(false);
  const [dialogMessage, setDialogMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const loggedInUser = localStorage.getItem('user');
    if (loggedInUser) {
      navigate('/rules');
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const result = await axios.post(
        "http://127.0.0.1:8000/students/login/", 
        { email, password }, 
        { withCredentials: true }
      );
      
      if (result.data.message === "Login successful!") {
        const {id, email, username } = result.data;
        localStorage.setItem("user", JSON.stringify({id, email, username }));
        navigate('/rules', { state: { user: {id, email, username } } });
      } else {
        setDialogMessage(result.data.message);
        setShowDialog(true);
      }
    } catch (err) {
      setDialogMessage("Invalid credentials. Please try again.");
      setShowDialog(true);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-page">
      <Navbar />
      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <h2>Welcome Back!</h2>
            <p>Enter your credentials to continue</p>
          </div>
          
          <form onSubmit={handleLogin} className="login-form">
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
              />
            </div>

            <button 
              type="submit primary" 
              className={`login-button ${isLoading ? 'loading' : ''}`}
              disabled={isLoading}
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </button>

            <p className="signup-link">
              Don't have an account? 
              <Link to="/signup"> Create one</Link>
            </p>
          </form>
        </div>
      </div>

      {showDialog && (
        <div className="dialog-overlay" onClick={() => setShowDialog(false)}>
          <div className="dialog-content" onClick={e => e.stopPropagation()}>
            <h3>Error</h3>
            <p>{dialogMessage}</p>
            <button onClick={() => setShowDialog(false)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Login;