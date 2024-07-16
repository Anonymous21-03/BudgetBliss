import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Styles/Profile.css'; // You'll need to create this CSS file

function Profile() {
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUserInfo();
  }, []);

  const fetchUserInfo = async () => {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      setLoading(false);
      return;
    }

    try {
      const response = await axios.get('/api/user_info', {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      setUserInfo(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching user info:', error);
      setError('Failed to fetch user information. Please try again.');
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/';
  };

  if (loading) return <div className="profile-loading">Loading...</div>;
  if (error) return <div className="profile-error">Error: {error}</div>;
  if (!userInfo) return <div className="profile-no-data">No user data available</div>;

  return (
    <div className="profile-container">
      <h1 className="profile-title">Your Profile</h1>
      <div className="profile-card">
        <div className="profile-header">
          {userInfo.picture ? (
            <img src={userInfo.picture} alt="Profile" className="profile-picture" />
          ) : (
            <div className="profile-picture-placeholder">{userInfo.name[0]}</div>
          )}
          <h2 className="profile-name">{userInfo.name}</h2>
        </div>
        <div className="profile-details">
          <p><strong>Email:</strong> {userInfo.email}</p>
          <p><strong>User ID:</strong> {userInfo.id}</p>
        </div>
        <div className="profile-actions">
          <Link to="/dashboard" className="profile-button">View Dashboard</Link>
          <Link to="/expenses" className="profile-button">Manage Expenses</Link>
          <button onClick={handleLogout} className="profile-button logout-button">Logout</button>
        </div>
      </div>
      <div className="profile-stats">
        <h3>Your Splitwise Stats</h3>
        <p>Total Expenses: ₹X,XXX.XX</p>
        <p>Groups: X</p>
        <p>Friends: X</p>
        {/* Add more stats as needed */}
      </div>
      <div className="profile-settings">
        <h3>Settings</h3>
        <p>Currency Preference: INR</p>
        <p>Notification Preferences: Email, Push</p>
        {/* Add more settings or make these editable */}
      </div>
    </div>
  );
}

export default Profile;