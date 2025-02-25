import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './signup.css';
import Navbar from './Navbar';

const Signup = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [showDialog, setShowDialog] = useState(false);
  const [dialogMessage, setDialogMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    if (password !== confirmPassword) {
      setDialogMessage("Passwords don't match!");
      setShowDialog(true);
      setPassword('');
      setConfirmPassword('');
      setIsLoading(false);
      return;
    }

    try {
      const result = await axios.post(
        "http://127.0.0.1:8000/students/signup/", 
        { username, email, password }
      );
      
      if (result.status === 201) {
        navigate('/login');
      }
    } catch (err) {
      if (err.response?.status === 400 && err.response?.data?.error === 'Email already exists') {
        setDialogMessage("Email already registered. Please use a different email.");
      } else {
        setDialogMessage("Registration failed. Please try again.");
      }
      setShowDialog(true);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="signup-page">
      <Navbar />
      <div className="signup-container">
        <div className="signup-card">
          <div className="signup-header">
            <h2>Create Account</h2>
            <p>Join us to start your journey</p>
          </div>
          
          <form onSubmit={handleSignup} className="signup-form">
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                required
              />
            </div>

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
                placeholder="Create a password"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm your password"
                required
              />
            </div>

            <button 
              type="submit primary" 
              className={`signup-button ${isLoading ? 'loading' : ''}`}
              disabled={isLoading}
            >
              {isLoading ? 'Creating Account...' : 'Sign Up'}
            </button>

            <p className="login-link">
              Already have an account? 
              <Link to="/login"> Login here</Link>
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

export default Signup;