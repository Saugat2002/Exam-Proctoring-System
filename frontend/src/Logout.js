import React from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Exit full-screen mode
    if (document.fullscreenElement) {
      document.exitFullscreen();
    }

    // Destroy session (clear session storage or any other session data)
    sessionStorage.clear();

    // Redirect to login page after logging out
    navigate('/login');
  };

  return (
    <div>
      <h2>You are about to log out</h2>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Logout;
