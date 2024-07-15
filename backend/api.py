from flask import Flask, jsonify, request
from splitwise import Splitwise
import config
from main import fetch_user_data
from Expense import process_expenses
import os

app = Flask(__name__)



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
        return jsonify({'error': str(e)}), 500

@app.route('/api/authorize', methods=['POST'])
def authorize():
    sObj = Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    url, secret = sObj.getAuthorizeURL()
    return jsonify({'url': url, 'secret': secret})

@app.route('/api/process_expenses', methods=['POST'])
def process_expenses_api():
    process_expenses()
    return jsonify({'message': 'Expenses processed successfully'})

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
        return jsonify({'error': str(e)}), 500

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

@app.route('/api/user_info', methods=['GET'])
def get_user_info():
    access_token = request.headers.get('Authorization')
    if not access_token:
        return jsonify({'error': 'No access token provided'}), 401
    
    access_token = access_token.split(' ')[1]  # Remove 'Bearer ' prefix
    sObj = Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    sObj.setAccessToken(access_token)
    
    try:
        user = sObj.getCurrentUser()
        return jsonify({
            'id': user.getId(),
            'name': f"{user.getFirstName()} {user.getLastName()}",
            'email': user.getEmail(),
            'picture': user.getPicture().getMedium() if user.getPicture() else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)