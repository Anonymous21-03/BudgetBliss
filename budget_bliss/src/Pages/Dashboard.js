import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      const access_token = localStorage.getItem('access_token');
      console.log("Access token in Dashboard:", access_token);
      
      if (!access_token) {
        console.error('No access token found');
        setError('No access token found. Please log in again.');
        setLoading(false);
        return;
      }

      try {
        const response = await axios.post('/api/fetch_data', { access_token });
        console.log("Response from fetch_data:", response.data);
        await axios.post('/api/process_expenses');
        const results = await axios.get('/api/get_results');
        setData(results.data);
      } catch (error) {
        console.error('Error fetching data:', error.response ? error.response.data : error.message);
        setError('Error fetching data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>No data available</div>;

  return (
    <div>
      <h2>Your Splitwise Dashboard</h2>
      <h3>Expense Predictions</h3>
      <pre>{data.predictions}</pre>
      <h3>Expense Sums</h3>
      <pre>{data.expense_sums}</pre>
    </div>
  );
}

export default Dashboard;