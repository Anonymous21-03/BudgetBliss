// src/Pages/Visualizations.js

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import './Styles/Visualizations.css';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

function Visualizations() {
  const [expenseSums, setExpenseSums] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get('/api/get_results', {
          headers: { Authorization: `Bearer ${accessToken}` }
        });
        setExpenseSums(JSON.parse(response.data.expense_sums));
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to fetch expense data. Please try again.');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="visualizations-loading">Loading...</div>;
  if (error) return <div className="visualizations-error">Error: {error}</div>;
  if (!localStorage.getItem('access_token')) {
    return (
      <div className="visualizations-login-prompt">
        <h2>Please log in to view your expense visualizations</h2>
        <Link to="/login" className="visualizations-login-button">Log In</Link>
      </div>
    );
  }

  const categories = expenseSums.map(sum => sum.predicted_expense_type);
  const paidAmounts = expenseSums.map(sum => parseFloat(sum['Paid Amount']));
  const owedAmounts = expenseSums.map(sum => parseFloat(sum['Owed Amount']));

  const barChartData = {
    labels: categories,
    datasets: [
      {
        label: 'Paid Amount',
        data: paidAmounts,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Owed Amount',
        data: owedAmounts,
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  const pieChartData = {
    labels: categories,
    datasets: [
      {
        data: paidAmounts,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Expense Distribution',
      },
    },
  };

  return (
    <div className="visualizations-container">
      <h1 className="visualizations-title">Expense Visualizations</h1>
      <div className="charts-container">
        <div className="chart">
          <h2>Expense Distribution (Bar Chart)</h2>
          <Bar data={barChartData} options={options} />
        </div>
        <div className="chart">
          <h2>Expense Distribution (Pie Chart)</h2>
          <Pie data={pieChartData} options={options} />
        </div>
      </div>
    </div>
  );
}

export default Visualizations;