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
        print(f"Received expense data: {expense_data}")  # New logging

        # Create a DataFrame for the new expense
        new_expense = pd.DataFrame([{
            'id': str(uuid.uuid4()),  # Generate a unique ID
            'description': expense_data['description'],
            'amount': expense_data['amount'],
            'net_amount': expense_data['amount'],  # Net amount same as total for simplicity
            'currency': 'INR',  # Assuming all expenses are in INR
            'date': datetime.now().isoformat(),
            'created_by': 'User',  # Placeholder for created by
            'category': expense_data['category']
        }])
        
        print(f"New expense DataFrame: {new_expense}")  # New logging
        
        # Append the new expense to the CSV file
        expenses_file = 'expenses.csv'
        try:
            # Load existing expenses
            expenses = pd.read_csv(expenses_file)
            print(f"Existing expenses: {expenses}")  # New logging
            # Append new expense using concat
            expenses = pd.concat([expenses, new_expense], ignore_index=True)
        except FileNotFoundError:
            # If the file doesn't exist, create it with the new expense
            expenses = new_expense

        # Save the updated expenses to the CSV file
        expenses.to_csv(expenses_file, index=False)
        print(f"Updated expenses saved to {expenses_file}")  # New logging
        
        # Re-run expense processing
        process_expenses()
        
        return jsonify({'message': 'Expense added successfully'}), 200
    except Exception as e:
        print(f"Error adding expense: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")  # New logging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)