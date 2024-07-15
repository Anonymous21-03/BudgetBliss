import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import Navigation from './components/Navigation';
import Login from './Pages/Login';
import Callback from './Pages/Callback';
import Dashboard from './Pages/Dashboard';
import Profile from './Pages/Profile';
import Expenses from './Pages/Expenses';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/callback" element={<Callback />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/expenses" element={<Expenses />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;