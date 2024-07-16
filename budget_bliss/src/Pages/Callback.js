import React, { useEffect } from 'react'
import axios from 'axios'
import { useLocation, useNavigate } from 'react-router-dom'

function Callback () {
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(() => {
    const params = new URLSearchParams(location.search)
    const oauth_token = params.get('oauth_token')
    const oauth_verifier = params.get('oauth_verifier')
    const secret = localStorage.getItem('secret')

    console.log('OAuth Token:', oauth_token)
    console.log('OAuth Verifier:', oauth_verifier)

    const fetchAccessToken = async () => {
      try {
        const response = await axios.post('/api/callback', {
          oauth_token,
          oauth_verifier,
          secret
        })

        if (response.data.access_token) {
          const accessToken = JSON.stringify(response.data.access_token)
          console.log('Received access token:', accessToken)
          localStorage.setItem('access_token', accessToken)
          window.dispatchEvent(new Event('loginStateChange'))
          navigate('/dashboard')
        } else {
          console.error('No access token in response:', response.data)
          navigate('/')
        }
      } catch (error) {
        console.error(
          'Error in callback:',
          error.response ? error.response.data : error.message
        )
        navigate('/')
      }
    }

    if (oauth_token && oauth_verifier) {
      fetchAccessToken()
    } else {
      console.error('Missing oauth_token or oauth_verifier')
      navigate('/')
    }
  }, [location, navigate])

  return <div>Processing authorization...</div>
}

export default Callback
