import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Styles/Expenses.css';

function Expenses() {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');
  const [sort, setSort] = useState('date');
  const [newExpense, setNewExpense] = useState({ description: '', amount: '', category: '' });

  useEffect(() => {
    fetchExpenses();
  }, []);

  const fetchExpenses = async () => {
    const accessTokenString = localStorage.getItem('access_token');
    if (!accessTokenString) {
      setLoading(false);
      return;
    }

    try {
      const accessToken = JSON.parse(accessTokenString);
      const response = await axios.get('/api/expenses', {
        headers: { Authorization: `Bearer ${JSON.stringify(accessToken)}` }
      });
      setExpenses(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching expenses:', error);
      setError('Failed to fetch expenses. Please try again.');
      setLoading(false);
    }
  };

  const handleAddExpense = async (e) => {
    e.preventDefault();
    // Implement the API call to add a new expense
    console.log('Adding expense:', newExpense);
    // After adding, refresh the expenses list
    fetchExpenses();
    setNewExpense({ description: '', amount: '', category: '' });
  };

  const filteredExpenses = expenses.filter(expense => 
    filter === 'all' || expense.category === filter
  );

  const sortedExpenses = filteredExpenses.sort((a, b) => {
    if (sort === 'date') return new Date(b.date) - new Date(a.date);
    if (sort === 'amount') return b.amount - a.amount;
    return 0;
  });

  const formatINR = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2,
    }).format(amount);
  };

  if (loading) return <div className="expenses-loading">Loading...</div>;
  if (error) return <div className="expenses-error">Error: {error}</div>;
  if (!localStorage.getItem('access_token')) {
    return (
      <div className="expenses-login-prompt">
        <h2>Please log in to view your expenses</h2>
        <Link to="/login" className="expenses-login-button">Log In</Link>
      </div>
    );
  }

  return (
    <div className="expenses-container">
      <h1>Expense Manager</h1>
      
      <section className="add-expense-section">
        <h2>Add New Expense</h2>
        <form onSubmit={handleAddExpense}>
          <input
            type="text"
            placeholder="Description"
            value={newExpense.description}
            onChange={(e) => setNewExpense({...newExpense, description: e.target.value})}
            required
          />
          <input
            type="number"
            placeholder="Amount"
            value={newExpense.amount}
            onChange={(e) => setNewExpense({...newExpense, amount: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Category"
            value={newExpense.category}
            onChange={(e) => setNewExpense({...newExpense, category: e.target.value})}
            required
          />
          <button type="submit">Add Expense</button>
        </form>
      </section>

      <section className="expense-list-section">
        <h2>Your Expenses</h2>
        <div className="expense-controls">
          <select onChange={(e) => setFilter(e.target.value)}>
            <option value="all">All Categories</option>
            <option value="food">Food</option>
            <option value="transport">Transport</option>
            <option value="utilities">Utilities</option>
            {/* Add more categories as needed */}
          </select>
          <select onChange={(e) => setSort(e.target.value)}>
            <option value="date">Sort by Date</option>
            <option value="amount">Sort by Amount</option>
          </select>
        </div>
        <ul className="expense-list">
          {sortedExpenses.map((expense, index) => (
            <li key={index} className="expense-item">
              <div className="expense-info">
                <h3>{expense.description}</h3>
                <p>Category: {expense.category}</p>
                <p>Date: {new Date(expense.date).toLocaleDateString()}</p>
              </div>
              <div className="expense-amount">
                {formatINR(expense.amount)}
              </div>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export default Expenses;