import React, { useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Navbar from './Navbar';
import './App.css';
import homeImage from './images/hero.png';

const App = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const loggedInUser = localStorage.getItem('user');
    if (loggedInUser) {
      navigate('/rules');
    }
  }, [navigate]);

  return (
    <div className="app">
      <Navbar />
      <main className="hero-section">
        <div className="container">
          <div className="content-wrapper">
            <div className="left-content">
              <h1 className="main-title">
                Smart Online
                <span className="highlight"> Exam Proctoring</span>
              </h1>
              <p className="subtitle">
                Secure and reliable online examination platform with advanced proctoring features
              </p>
              <div className="cta-buttons">
                <Link to="/login" className="primary-button">
                  Get Started
                </Link>
                <Link to="/about" className="secondary-button">
                  Learn More
                </Link>
              </div>
            </div>
            <div className="right-content">
              <img src={homeImage} alt="Online Proctoring" className="hero-image" />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;