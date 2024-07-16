import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import './Navigation.css'; // We'll create this file for styles

function Navigation() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  const fetchUserData = async () => {
    const accessTokenString = localStorage.getItem('access_token');
    if (accessTokenString) {
      try {
        const accessToken = JSON.parse(accessTokenString);
        const response = await axios.get('/api/user_info', {
          headers: { Authorization: `Bearer ${JSON.stringify(accessToken)}` }
        });
        setUser(response.data);
      } catch (error) {
        console.error('Error fetching user info:', error);
        if (error.response && error.response.status === 401) {
          handleLogout();
        }
      }
    }
  };

  useEffect(() => {
    fetchUserData();
    window.addEventListener('loginStateChange', fetchUserData);
    return () => {
      window.removeEventListener('loginStateChange', fetchUserData);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    navigate('/');
  };

  return (
    <nav className="navigation">
      <div className="nav-logo">
        <Link to="/">ExpenseAI</Link>
      </div>
      <ul className="nav-links">
        <li className={location.pathname === '/' ? 'active' : ''}>
          <Link to="/">Home</Link>
        </li>
        <li className={location.pathname === '/dashboard' ? 'active' : ''}>
          <Link to="/dashboard">Dashboard</Link>
        </li>
        <li className={location.pathname === '/expenses' ? 'active' : ''}>
          <Link to="/expenses">Expenses</Link>
        </li>
        {user && (
          <li className={location.pathname === '/profile' ? 'active' : ''}>
            <Link to="/profile">Profile</Link>
          </li>
        )}
      </ul>
      <div className="nav-auth">
        {user ? (
          <div className="user-info">
            {user.picture && (
              <img
                src={user.picture}
                alt="User"
                className="user-avatar"
              />
            )}
            <span className="user-name">{user.name}</span>
            <button onClick={handleLogout} className="logout-button">Logout</button>
          </div>
        ) : (
          <Link to="/login" className="login-button">Login</Link>
        )}
      </div>
    </nav>
  );
}

export default Navigation;