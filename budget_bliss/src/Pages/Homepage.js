import React from 'react';
import { Link } from 'react-router-dom';
import './Styles/Homepage.css';

const Homepage = () => {
  return (
    <div className='homepage-container'>
      <div className='hero-section'>
        <div className='headline'>
          <div className='heading-text'>
            <h1>Smart Expense Tracking with AI-Powered Insights</h1>
            <p className='subheading'>
              Manage your Splitwise expenses effortlessly and gain predictive insights
            </p>
            <Link to="/login" className='login-button'>
              Connect with Splitwise
            </Link>
          </div>
          <div className='heading-image'>
            {/* Add an image or SVG illustration here */}
          </div>
        </div>
      </div>
      
      <div className='features-section'>
        <h2>Key Features</h2>
        <div className='feature-grid'>
          <div className='feature-item'>
            <h3>Expense Tracking</h3>
            <p>Sync and categorize your Splitwise expenses automatically</p>
          </div>
          <div className='feature-item'>
            <h3>AI Predictions</h3>
            <p>Get intelligent predictions on your spending patterns</p>
          </div>
          <div className='feature-item'>
            <h3>Visual Analytics</h3>
            <p>View your expenses through intuitive charts and graphs</p>
          </div>
          <div className='feature-item'>
            <h3>Budget Insights</h3>
            <p>Receive personalized budgeting recommendations</p>
          </div>
        </div>
      </div>

      <div className='how-it-works'>
        <h2>How It Works</h2>
        <div className='steps'>
          <div className='step'>
            <div className='step-number'>1</div>
            <p>Connect your Splitwise account</p>
          </div>
          <div className='step'>
            <div className='step-number'>2</div>
            <p>Sync your expenses</p>
          </div>
          <div className='step'>
            <div className='step-number'>3</div>
            <p>Get AI-powered insights</p>
          </div>
          <div className='step'>
            <div className='step-number'>4</div>
            <p>Make informed financial decisions</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Homepage;