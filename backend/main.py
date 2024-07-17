from splitwise import Splitwise
import config
import csv
from datetime import datetime
import os

def get_splitwise_instance():
    return Splitwise(config.CONSUMER_KEY, config.CONSUMER_SECRET)

def authorize_user(sObj):
    url, secret = sObj.getAuthorizeURL()
    print(f"Please go to this URL to authorize the app: {url}")
    print("After authorization, you'll be redirected to a callback URL.")
    print("Copy the oauth_token and oauth_verifier from the URL.")
    
    oauth_token = input("Enter the oauth_token: ")
    oauth_verifier = input("Enter the oauth_verifier: ")
    
    access_token = sObj.getAccessToken(oauth_token, secret, oauth_verifier)
    return access_token

def fetch_user_data(sObj):
    current_user = sObj.getCurrentUser()
    friends = sObj.getFriends()
    groups = sObj.getGroups()

    def update_csv(filename, headers, data):
        mode = 'w' if not os.path.exists(filename) else 'w'
        with open(filename, mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"Updated {filename}")

    group_data = [[group.getId(), group.getName(), group.getUpdatedAt()] for group in groups]
    update_csv('groups.csv', ['Group ID', 'Group Name', 'Updated At'], group_data)

    friend_data = [[friend.getId(), friend.getFirstName(), friend.getLastName(), friend.getEmail()] for friend in friends]
    update_csv('friends.csv', ['Friend ID', 'First Name', 'Last Name', 'Email'], friend_data)

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

    current_user_id = current_user.getId()

    expense_data = []
    for expense in all_expenses:
        created_by = "Unknown"
        if expense.getCreatedBy():
            first_name = expense.getCreatedBy().getFirstName() or ""
            last_name = expense.getCreatedBy().getLastName() or ""
            created_by = f"{first_name} {last_name}".strip() or "Unknown"
        
        # Calculate net amount for the current user
        net_amount = 0
        for user in expense.getUsers():
            if user.getId() == current_user_id:
                net_amount = user.getNetBalance()
                break
        
        expense_data.append([
            expense.getId(),
            expense.getDescription(),
            expense.getCost(),
            net_amount,  # Add net amount
            expense.getCurrencyCode(),
            expense.getDate(),
            created_by
        ])
    update_csv('expenses.csv', ['Expense ID', 'Description', 'Total Cost', 'Net Amount', 'Currency Code', 'Date', 'Created By'], expense_data)

    print(f"\nSummary:")
    print(f"Total number of friends: {len(friends)}")
    print(f"Total number of groups: {len(groups)}")
    print(f"Total number of expenses: {len(all_expenses)}")

def main():
    sObj = get_splitwise_instance()
    
    access_token = authorize_user(sObj)
    
    sObj.setAccessToken(access_token)
    
    fetch_user_data(sObj)

if __name__ == "__main__":
    main()
