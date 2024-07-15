import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

function Navigation() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      const accessTokenString = localStorage.getItem('access_token');
      if (accessTokenString) {
        try {
          const accessToken = JSON.parse(accessTokenString);
          const response = await axios.get('/api/user_info', {
            headers: { Authorization: `Bearer ${accessToken.oauth_token}` }
          });
          setUser(response.data);
        } catch (error) {
          console.error('Error fetching user info:', error.response ? error.response.data : error.message);
          if (error.response && error.response.status === 401) {
            handleLogout();
          }
        }
      }
    };

    fetchUserData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    navigate('/');
  };

  return (
    <nav style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px' }}>
      <ul style={{ listStyle: 'none', display: 'flex', gap: '20px', margin: 0 }}>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/profile">Profile</Link></li>
        <li><Link to="/expenses">Expenses</Link></li>
      </ul>
      {user ? (
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {user.picture && <img src={user.picture} alt="User" style={{ width: '30px', height: '30px', borderRadius: '50%' }} />}
          <span>{user.name}</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <Link to="/">Login</Link>
      )}
    </nav>
  );
}

export default Navigation;