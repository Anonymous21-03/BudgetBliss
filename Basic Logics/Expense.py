
def process_expenses():
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    from sklearn.pipeline import Pipeline

    # Load the data
    data = pd.read_csv("training-data.csv")
    data2 = pd.read_csv("expenses.csv")

    # Handle missing values
    data['Description'] = data['Description'].fillna('Unknown')
    data2['Description'] = data2['Description'].fillna('Unknown')

    # Convert 'Cost' to numeric, replacing any non-numeric values with NaN
    data['Cost'] = pd.to_numeric(data['Cost'], errors='coerce')
    data2['Cost'] = pd.to_numeric(data2['Cost'], errors='coerce')

    # Prepare the features
    X_train = data['Description']
    y_train = data['expense_type']

    X_test = data2['Description']

    # Print shapes to check
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")

    # Encode labels
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)

    # Create a simplified pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english')),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    # Fit the pipeline
    pipeline.fit(X_train, y_train_encoded)

    # Make predictions
    predictions = pipeline.predict(X_test)

    # Create a DataFrame with all fields from the test data and the predicted expense type
    results = data2.copy()
    results['predicted_expense_type'] = le.inverse_transform(predictions)

    # Calculate the sum of each type of expense
    expense_sums = results.groupby('predicted_expense_type')['Cost'].sum().reset_index()

    # Save results to CSV
    results.to_csv("prediction.csv", index=False)
    expense_sums.to_csv("expense_sums.csv", index=False)

    print("Predictions saved to 'prediction.csv'")
    print("Expense sums saved to 'expense_sums.csv'")

    # # Print sample predictions
    # print("\nSample predictions:")
    # for i in range(min(10, len(X_test))):
    #     print(f"Expense ID: {results['Expense ID'].iloc[i]}")
    #     print(f"Description: {results['Description'].iloc[i]}")
    #     print(f"Predicted: {results['predicted_expense_type'].iloc[i]}")
    #     print(f"Amount: {results['Cost'].iloc[i]}")
    #     print(f"Currency Code: {results['Currency Code'].iloc[i]}")
    #     print(f"Date: {results['Date'].iloc[i]}")
    #     print(f"Created By: {results['Created By'].iloc[i]}")
    #     print()
    
if __name__ == "__main__":
    process_expenses()