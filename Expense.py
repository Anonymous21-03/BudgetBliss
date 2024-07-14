import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# Load the data
data = pd.read_csv("trainingdata2.csv")
data2 = pd.read_csv("expenses.csv")

# Feature engineering
def extract_time_features(df):
    df['date'] = pd.to_datetime(df['Date'])
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    df['time_of_day'] = pd.cut(df['date'].dt.hour, bins=[0, 12, 18, 24], labels=['morning', 'afternoon', 'evening'])
    return df

data = extract_time_features(data)
data2 = extract_time_features(data2)

# Use data for training and data2 for testing
X_train = data['Description'] + ' ' + data['time_of_day'].astype(str)
y_train = data['expense_type']
X_test = data2['Description'] + ' ' + data2['time_of_day'].astype(str)
amount_inr = data2['Cost']

# Handle NaN values in y_test if 'expense_type' exists in data2
if 'expense_type' in data2.columns:
    y_test = data2['expense_type'].fillna('Unknown')  # Replace NaN with 'Unknown'
else:
    y_test = None

# Encode labels
le = LabelEncoder()
y_train_encoded = le.fit_transform(y_train)

# Create a pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english', max_features=5000)),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train the model
pipeline.fit(X_train, y_train_encoded)

# Make predictions
predictions = pipeline.predict(X_test)

# Create a DataFrame with both description and predicted expense type
results = pd.DataFrame({
    'amount_inr': amount_inr,
    'description': data2['Description'],
    'predicted_expense_type': le.inverse_transform(predictions)
})

# Calculate the sum of each type of expense
expense_sums = results.groupby('predicted_expense_type')['amount_inr'].sum().reset_index()

# Save results to CSV
results.to_csv("prediction.csv", index=False)
expense_sums.to_csv("expense_sums.csv", index=False)

print("Predictions saved to 'prediction.csv'")
print("Expense sums saved to 'expense_sums.csv'")

# Calculate accuracy if y_test is available and not None
if y_test is not None:
    # Handle unknown labels in y_test
    y_test_known = y_test[y_test.isin(le.classes_)]
    predictions_known = predictions[y_test.isin(le.classes_)]
    
    if len(y_test_known) > 0:
        y_test_encoded = le.transform(y_test_known)
        accuracy = accuracy_score(y_test_encoded, predictions_known)
        print(f"Accuracy (excluding unknown labels): {accuracy}")

        # Print classification report
        print("\nClassification Report (excluding unknown labels):")
        print(classification_report(y_test_encoded, predictions_known, target_names=le.classes_))
    else:
        print("No known labels in test data to calculate accuracy")

    # Print information about unknown labels
    unknown_count = sum(~y_test.isin(le.classes_))
    print(f"\nNumber of unknown labels in test data: {unknown_count}")
else:
    print("Unable to calculate accuracy: 'expense_type' not found in test data")

# Cross-validation (using only training data)
cv_scores = cross_val_score(pipeline, X_train, y_train_encoded, cv=5)
print(f"\nCross-validation scores: {cv_scores}")
print(f"Mean CV score: {cv_scores.mean()}")

# Print sample predictions
print("\nSample predictions:")
for i in range(min(10, len(X_test))):
    print(f"Description: {data2['Description'].iloc[i]}")
    print(f"Predicted: {le.inverse_transform([predictions[i]])[0]}")
    if y_test is not None:
        print(f"Actual: {y_test.iloc[i]}")
    print()