import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Styles/Login.css';

function Login() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/authorize');
      const { url, secret } = response.data;
      localStorage.setItem('secret', secret);
      
      window.location.href = url;
    } catch (error) {
      console.error('Error initiating login:', error);
      setError('Failed to connect to Splitwise. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">Welcome to Budget Bliss</h1>
        <p className="login-subtitle">Connect your Splitwise account to get started</p>
        
        {error && <div className="login-error">{error}</div>}
        
        <button 
          onClick={handleLogin} 
          className="login-button" 
          disabled={isLoading}
        >
          {isLoading ? 'Connecting...' : 'Connect to Splitwise'}
        </button>
        
        <div className="login-info">
          <h2>Why connect with Splitwise?</h2>
          <ul>
            <li>Automatically import and categorize your expenses</li>
            <li>Get AI-powered insights on your spending habits</li>
            <li>Easily manage shared expenses with friends and roommates</li>
            <li>View detailed analytics of your financial activities</li>
          </ul>
        </div>
        
        <p className="login-footer">
          Don't have a Splitwise account? <a href="https://secure.splitwise.com/#/register" target="_blank" rel="noopener noreferrer">Sign up here</a>
        </p>
      </div>
    </div>
  );
}

export default Login;