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
      const accessTokenString = localStorage.getItem('access_token');
      if (!accessTokenString) {
        setError('No access token found. Please log in again.');
        setLoading(false);
        return;
      }

      try {
        const accessToken = JSON.parse(accessTokenString);
        await axios.post('/api/fetch_data', { access_token: accessToken });
        await axios.post('/api/process_expenses', { access_token: accessToken });
        const results = await axios.get('/api/get_results');
        setData(results.data);
      } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message);
        setError('An error occurred. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>No data available</div>;

  const predictions = JSON.parse(data.predictions);
  const expenseSums = JSON.parse(data.expense_sums);

  // Limit the number of predictions to display
  const displayedPredictions = predictions.slice(0, 10);

  return (
    <div>
      <h2>Your Splitwise Dashboard</h2>
      
      <h3>Recent Expense Predictions</h3>
      <table>
        <thead>
          <tr>
            <th>Description</th>
            <th>Cost</th>
            <th>Predicted Type</th>
          </tr>
        </thead>
        <tbody>
          {displayedPredictions.map((prediction, index) => (
            <tr key={index}>
              <td>{prediction.Description}</td>
              <td>{prediction.Cost}</td>
              <td>{prediction.predicted_expense_type}</td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <h3>Expense Sums by Category</h3>
      <table>
        <thead>
          <tr>
            <th>Category</th>
            <th>Total Cost</th>
          </tr>
        </thead>
        <tbody>
          {expenseSums.map((sum, index) => (
            <tr key={index}>
              <td>{sum.predicted_expense_type}</td>
              <td>{sum.Cost}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;