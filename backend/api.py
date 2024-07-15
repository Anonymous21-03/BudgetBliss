from flask import Flask, jsonify, request
from splitwise import Splitwise
import config
from main import fetch_user_data
from Expense import process_expenses
import os

app = Flask(__name__)

@app.route('/api/authorize', methods=['POST'])
def authorize():
    sObj = Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    url, secret = sObj.getAuthorizeURL()
    return jsonify({'url': url, 'secret': secret})

@app.route('/api/callback', methods=['POST'])
def callback():
    data = request.json
    sObj = Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    access_token = sObj.getAccessToken(data['oauth_token'], data['secret'], data['oauth_verifier'])
    return jsonify({'access_token': access_token})

@app.route('/api/fetch_data', methods=['POST'])
def fetch_data():
    access_token = request.json['access_token']
    sObj = Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    sObj.setAccessToken(access_token)
    fetch_user_data(sObj)
    return jsonify({'message': 'Data fetched successfully'})

@app.route('/api/process_expenses', methods=['POST'])
def process_expenses_api():
    process_expenses()
    return jsonify({'message': 'Expenses processed successfully'})

@app.route('/api/get_results', methods=['GET'])
def get_results():
    with open('prediction.csv', 'r') as f:
        predictions = f.read()
    with open('expense_sums.csv', 'r') as f:
        expense_sums = f.read()
    return jsonify({
        'predictions': predictions,
        'expense_sums': expense_sums
    })

if __name__ == '__main__':
    app.run(debug=True)