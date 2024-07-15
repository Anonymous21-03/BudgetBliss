import React from 'react';
import axios from 'axios';

function Login() {
  const handleLogin = async () => {
    try {
      const response = await axios.post('/api/authorize');
      const { url, secret } = response.data;
      localStorage.setItem('secret', secret);
      
      // Open the authorization URL in a new window
      const authWindow = window.open(url, 'Splitwise Authorization', 'width=600,height=600');
      
      // Set up a timer to check if the window has been closed
      const timer = setInterval(() => {
        if (authWindow.closed) {
          clearInterval(timer);
          // Redirect to dashboard or check for successful authentication
          window.location.href = '/dashboard';
        }
      }, 500);

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