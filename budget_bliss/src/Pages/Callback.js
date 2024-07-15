import React, { useEffect } from 'react';
import axios from 'axios';

function Callback() {
  useEffect(() => {
    const fetchToken = async () => {
      const params = new URLSearchParams(window.location.search);
      const oauth_token = params.get('oauth_token');
      const oauth_verifier = params.get('oauth_verifier');
      const secret = localStorage.getItem('secret');

      try {
        const response = await axios.post('/api/callback', {
          oauth_token,
          oauth_verifier,
          secret
        });
        localStorage.setItem('access_token', response.data.access_token);
        
        // Close this window and notify the opener
        if (window.opener) {
          window.opener.postMessage('authentication_successful', '*');
          window.close();
        } else {
          // Fallback if opener is not available
          window.location.href = '/dashboard';
        }
      } catch (error) {
        console.error('Error in callback:', error);
        // Handle error (maybe show an error message to the user)
      }
    };

    fetchToken();
  }, []);

  return <div>Processing login...</div>;
}

export default Callback;