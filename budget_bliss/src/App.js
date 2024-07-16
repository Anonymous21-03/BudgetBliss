// src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import Navigation from './components/Navigation';
import Login from './Pages/Login';
import Callback from './Pages/Callback';
import Dashboard from './Pages/Dashboard';
import Profile from './Pages/Profile';
import Expenses from './Pages/Expenses';
import Homepage from './Pages/Homepage';
import Visualizations from './Pages/Visualizations'; 

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Homepage />} />
          <Route path="/callback" element={<Callback />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/expenses" element={<Expenses />} />
          <Route path="/visualizations" element={<Visualizations />} /> {/* Add this new route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;