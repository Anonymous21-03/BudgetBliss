import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report

# Sample data loading
# df = pd.read_csv('your_dataset.csv')

# Dummy data for demonstration purposes
data = {
    'Category': ['Food', 'Transport', 'Food', 'Entertainment', 'Food'],
    'Amount': [20, 15, 30, 50, 10]
}
df = pd.DataFrame(data)

# Define features and target
X = df[['Category', 'Amount']]  # Ensure this is a DataFrame
y = df['Category']

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessing
numeric_features = ['Amount']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_features = ['Category']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

# Model pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', RandomForestClassifier(random_state=42))])

# Parameter grid for GridSearchCV
param_grid = {
    'classifier__n_estimators': [10, 50, 100],
    'classifier__max_features': ['sqrt', 'log2']
}

# Use fewer splits for cross-validation due to small dataset size
grid_search = GridSearchCV(pipeline, param_grid, cv=2, scoring='accuracy')

# Ensure y_train is correctly encoded for classification
y_train_encoded = y_train.astype('category').cat.codes

# Fit the model
grid_search.fit(X_train, y_train_encoded)

# Prediction and evaluation
y_pred = grid_search.predict(X_test)
y_test_encoded = y_test.astype('category').cat.codes

print(classification_report(y_test_encoded, y_pred, zero_division=1))
