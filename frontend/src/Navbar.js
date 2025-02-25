import React from 'react';
import './navbar.css';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="nav-wrapper">
        <div className="nav-brand">
          <span className="nav-icon">📝</span>
          <Link to="/" className="nav-title">Exam Proctor</Link>
        </div>
        <ul className="nav-menu">
          <li><Link to="/">Dashboard</Link></li>
          <li><Link to="/exams">Exams</Link></li>
          <li><Link to="/profile">Profile</Link></li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;