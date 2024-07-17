import pandas as pd
from flask import Flask, jsonify, request
from splitwise import Splitwise
import config
from main import fetch_user_data
from Expense import process_expenses
import os
from datetime import datetime
import uuid
from flask_cors import CORS
import traceback
import json
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for generating plots without a GUI
import matplotlib.pyplot as plt
import io
import base64
from flask import send_file

app = Flask(__name__)
CORS(app)  

@app.route('/api/authorize', methods=['POST'])
def authorize():
    sObj = Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    url, secret = sObj.getAuthorizeURL()
    return jsonify({'url': url, 'secret': secret})

@app.route('/api/callback', methods=['POST'])
def callback():
    data = request.json
    print("Received callback data:", data)
    
    oauth_token = data.get('oauth_token')
    oauth_verifier = data.get('oauth_verifier')
    secret = data.get('secret')
    
    if not oauth_token or not oauth_verifier or not secret:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    sObj = Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    try:
        access_token = sObj.getAccessToken(oauth_token, secret, oauth_verifier)
        print("Access token obtained:", access_token)
        return jsonify({'access_token': access_token})
    except Exception as e:
        print(f"Error in callback: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/fetch_data', methods=['POST'])
def fetch_data():
    try:
        access_token = request.json.get('access_token')
        if not access_token:
            return jsonify({'error': 'No access token provided'}), 400
        
        sObj = Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        sObj.setAccessToken(access_token)
        fetch_user_data(sObj)
        return jsonify({'message': 'Data fetched successfully'})
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/process_expenses', methods=['POST'])
def process_expenses_api():
    try:
        access_token = request.json.get('access_token')
        if not access_token:
            return jsonify({'error': 'No access token provided'}), 400
        
        sObj = Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        sObj.setAccessToken(access_token)
        process_expenses()
        return jsonify({'message': 'Expenses processed successfully'})
    except Exception as e:
        print(f"Error processing expenses: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_results', methods=['GET'])
def get_results():
    try:
        predictions = pd.read_csv('prediction.csv')
        expense_sums = pd.read_csv('expense_sums.csv')
        
        predictions_json = predictions.to_json(orient='records')
        expense_sums_json = expense_sums.to_json(orient='records')
        
        return jsonify({
            'predictions': predictions_json,
            'expense_sums': expense_sums_json
        })
    except Exception as e:
        print(f"Error getting results: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/plot/expense_distribution', methods=['GET'])
def plot_expense_distribution():
    try:
        expense_sums = pd.read_csv('expense_sums.csv')
        
        # Create a bar plot
        plt.figure(figsize=(10, 6))
        plt.bar(expense_sums['predicted_expense_type'], expense_sums['Paid Amount'], label='Paid')
        plt.bar(expense_sums['predicted_expense_type'], expense_sums['Owed Amount'], bottom=expense_sums['Paid Amount'], label='Owed')
        plt.xlabel('Expense Type')
        plt.ylabel('Amount (INR)')
        plt.title('Expense Distribution')
        plt.legend()
        plt.xticks(rotation=45, ha='right')
        
        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print(f"Error generating expense distribution plot: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/plot/expense_pie_chart', methods=['GET'])
def plot_expense_pie_chart():
    try:
        expense_sums = pd.read_csv('expense_sums.csv')
        
        # Create a pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(expense_sums['Paid Amount'], labels=expense_sums['predicted_expense_type'], autopct='%1.1f%%')
        plt.title('Expense Distribution (Paid Amount)')
        
        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print(f"Error generating expense pie chart: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/user_info', methods=['GET'])
def get_user_info():
    access_token = request.headers.get('Authorization')
    print("Received Authorization header:", access_token)
    
    if not access_token:
        return jsonify({'error': 'No access token provided'}), 401
    
    access_token = access_token.split(' ')[1]  # Remove 'Bearer ' prefix
    print("Extracted access token:", access_token)
    
    try:
        access_token = json.loads(access_token)
        print("Parsed access token:", access_token)
        
        sObj = Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        sObj.setAccessToken(access_token)
        
        user = sObj.getCurrentUser()
        print("Retrieved user info:", user)
        
        return jsonify({
            'id': user.getId(),
            'name': f"{user.getFirstName()} {user.getLastName()}",
            'email': user.getEmail(),
            'picture': user.getPicture().getMedium() if user.getPicture() else None
        })
    except json.JSONDecodeError as e:
        print("JSON decode error:", str(e))
        return jsonify({'error': 'Invalid access token format'}), 400
    except Exception as e:
        print(f"Error getting user info: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/add_expense', methods=['POST'])
def add_expense():
    access_token = request.headers.get('Authorization')
    if not access_token:
        return jsonify({'error': 'No access token provided'}), 401
    
    access_token = access_token.split(' ')[1]  # Remove 'Bearer ' prefix
    
    try:
        access_token = json.loads(access_token)
        sObj = Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        sObj.setAccessToken(access_token)
        
        expense_data = request.json
        print(f"Received expense data: {expense_data}")

        # Fetch latest expenses from Splitwise
        all_expenses = []
        offset = 0
        limit = 100
        while True:
            expenses = sObj.getExpenses(limit=limit, offset=offset)
            if not expenses:
                break
            all_expenses.extend(expenses)
            offset += limit
            if len(expenses) < limit:
                break

        # Convert Splitwise expenses to DataFrame, filtering out deleted expenses
        expenses = pd.DataFrame([
            {
                'id': expense.getId(),
                'description': expense.getDescription(),
                'amount': expense.getCost(),
                'net_amount': expense.getCost(),  # Simplified; you might want to calculate this based on user's share
                'currency': expense.getCurrencyCode(),
                'date': expense.getDate(),
                'created_by': expense.getCreatedBy().getFirstName() if expense.getCreatedBy() else 'Unknown',
                'category': expense.getCategory().getName() if expense.getCategory() else 'Uncategorized',
                'deleted_at': expense.getDeletedAt()
            }
            for expense in all_expenses
            if expense.getDeletedAt() is None  # Only include expenses that haven't been deleted
        ])

        # Create a DataFrame for the new expense
        new_expense = pd.DataFrame([{
            'id': str(uuid.uuid4()),  # Generate a unique ID
            'description': expense_data['description'],
            'amount': expense_data['amount'],
            'net_amount': expense_data['amount'],  # Net amount same as total for simplicity
            'currency': 'INR',  # Assuming all expenses are in INR
            'date': datetime.now().isoformat(),
            'created_by': 'User',  # Placeholder for created by
            'category': expense_data['category'],
            'deleted_at': None
        }])
        
        # Append new expense to the fetched expenses
        expenses = pd.concat([expenses, new_expense], ignore_index=True)

        # Save the updated expenses to the CSV file (overwriting)
        expenses_file = 'expenses.csv'
        expenses.to_csv(expenses_file, index=False)
        print(f"Updated expenses saved to {expenses_file}")
        
        # Re-run expense processing
        process_expenses()
        
        return jsonify({'message': 'Expense added successfully'}), 200
    except Exception as e:
        print(f"Error adding expense: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
