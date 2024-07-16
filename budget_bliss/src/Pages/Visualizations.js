// src/Pages/Visualizations.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Styles/Visualizations.css';
import { Link } from 'react-router-dom';


function Visualizations() {
  const [barChartSrc, setBarChartSrc] = useState('');
  const [pieChartSrc, setPieChartSrc] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCharts = async () => {
      try {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
          setLoading(false);
          return;
        }

        const barResponse = await axios.get('/api/plot/expense_distribution', {
          responseType: 'blob',
          headers: { Authorization: `Bearer ${accessToken}` }
        });
        setBarChartSrc(URL.createObjectURL(barResponse.data));

        const pieResponse = await axios.get('/api/plot/expense_pie_chart', {
          responseType: 'blob',
          headers: { Authorization: `Bearer ${accessToken}` }
        });
        setPieChartSrc(URL.createObjectURL(pieResponse.data));

        setLoading(false);
      } catch (error) {
        console.error('Error fetching charts:', error);
        setError('Failed to fetch charts. Please try again.');
        setLoading(false);
      }
    };

    fetchCharts();
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

  return (
    <div className="visualizations-container">
      <h1 className="visualizations-title">Expense Visualizations</h1>
      <div className="charts-container">
        <div className="chart">
          <h2>Expense Distribution</h2>
          <img src={barChartSrc} alt="Expense Distribution Bar Chart" />
        </div>
        <div className="chart">
          <h2>Expense Distribution (Pie Chart)</h2>
          <img src={pieChartSrc} alt="Expense Distribution Pie Chart" />
        </div>
      </div>
    </div>
  );
}

export default Visualizations;