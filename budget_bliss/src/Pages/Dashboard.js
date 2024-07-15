import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const access_token = localStorage.getItem('access_token');
      try {
        await axios.post('/api/fetch_data', { access_token });
        await axios.post('/api/process_expenses');
        const response = await axios.get('/api/get_results');
        setData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  if (!data) return <div>Loading...</div>;

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