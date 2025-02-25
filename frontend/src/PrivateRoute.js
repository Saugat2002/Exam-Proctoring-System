import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ element: Element }) => {
  const isAuthenticated = localStorage.getItem('user'); // Check if user is in localStorage

  return isAuthenticated ? <Element /> : <Navigate to="/login" />;
};

export default PrivateRoute;
