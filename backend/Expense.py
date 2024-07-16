import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

def clean_description(desc):
    return ' '.join(word for word in desc.split() if len(word) > 1)

def process_expenses():
    print("Starting expense processing")  # New logging
    
    # Load the data
    data = pd.read_csv("training-data.csv")
    data2 = pd.read_csv("expenses.csv")

    print(f"Loaded training data shape: {data.shape}")  # New logging
    print(f"Loaded expenses data: {data2}")  # New logging

    # Data preprocessing
    data['Description'] = data['Description'].fillna('Unknown').apply(clean_description)
    data2['Description'] = data2['Description'].fillna('Unknown').apply(clean_description)

    data['Cost'] = pd.to_numeric(data['Cost'], errors='coerce').fillna(0)
    data2['Total Cost'] = pd.to_numeric(data2['Total Cost'], errors='coerce').fillna(0)
    data2['Net Amount'] = pd.to_numeric(data2['Net Amount'], errors='coerce').fillna(0)

    data2['is_payment'] = data2['Description'].str.lower().isin(['payment', 'settle all balances'])

    X_train = data['Description']
    y_train = data['expense_type']

    X_test = data2['Description']

    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"X_test shape: {X_test.shape}")  # New logging

    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english')),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X_train, y_train_encoded)

    predictions = pipeline.predict(X_test)

    results = data2.copy()
    results['predicted_expense_type'] = le.inverse_transform(predictions)
    results.loc[results['is_payment'], 'predicted_expense_type'] = 'Payment'

    print(f"Results after prediction: {results}")  # New logging

    # Separate expense sums for paid and owed
    expense_sums_paid = results[results['Net Amount'] > 0].groupby('predicted_expense_type')['Net Amount'].sum().reset_index()
    expense_sums_paid.columns = ['predicted_expense_type', 'Paid Amount']
    
    expense_sums_owed = results[results['Net Amount'] < 0].groupby('predicted_expense_type')['Net Amount'].sum().abs().reset_index()
    expense_sums_owed.columns = ['predicted_expense_type', 'Owed Amount']

    # Merge paid and owed sums
    expense_sums = pd.merge(expense_sums_paid, expense_sums_owed, on='predicted_expense_type', how='outer').fillna(0)

    print(f"Expense sums: {expense_sums}")  # New logging

    results.to_csv("prediction.csv", index=False)
    expense_sums.to_csv("expense_sums.csv", index=False)

    print("Predictions saved to 'prediction.csv'")
    print("Expense sums saved to 'expense_sums.csv'")

if __name__ == "__main__":
    process_expenses()