import React from 'react';
import axios from 'axios';

function Login() {
  const handleLogin = async () => {
    try {
      const response = await axios.post('/api/authorize');
      const { url, secret } = response.data;
      localStorage.setItem('secret', secret);
      
      window.location.href = url;

    } catch (error) {
      console.error('Error initiating login:', error);
    }
  };

  return (
    <div>
      <h2>Login with Splitwise</h2>
      <button onClick={handleLogin}>Connect to Splitwise</button>
    </div>
  );
}

export default Login;
