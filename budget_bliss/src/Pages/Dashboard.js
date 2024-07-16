import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import './Styles/Dashboard.css';

function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      const accessTokenString = localStorage.getItem('access_token');
      if (!accessTokenString) {
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

  const formatINR = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  };

  if (loading) return <div className="dashboard-loading">Loading...</div>;
  if (error) return <div className="dashboard-error">Error: {error}</div>;
  if (!localStorage.getItem('access_token')) {
    return (
      <div className="dashboard-login-prompt">
        <h2>Please log in to view your dashboard</h2>
        <Link to="/login" className="dashboard-login-button">Log In</Link>
      </div>
    );
  }
  if (!data) return <div className="dashboard-no-data">No data available</div>;

  const predictions = JSON.parse(data.predictions);
  const expenseSums = JSON.parse(data.expense_sums);

  // Limit the number of predictions to display
  const displayedPredictions = predictions.slice(0, 10);

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Your Splitwise Dashboard</h1>
      
      <section className="dashboard-section">
        <h2>Recent Expense Predictions</h2>
        <div className="dashboard-table-container">
          <table className="dashboard-table">
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
                  <td>{formatINR(parseFloat(prediction.Cost))}</td>
                  <td>{prediction.predicted_expense_type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      
      <section className="dashboard-section">
        <h2>Expense Sums by Category</h2>
        <div className="dashboard-table-container">
          <table className="dashboard-table">
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
                  <td>{formatINR(parseFloat(sum.Cost))}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
