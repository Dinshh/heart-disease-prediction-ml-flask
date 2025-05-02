import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE  # For handling class imbalance
import joblib
import os

# Load the dataset
data_path = os.path.join("data", "Heart_Disease_Prediction.csv")  # Adjusted path
print("Looking for dataset at:", data_path)  # Debugging: Print the file path

# Check if the file exists
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Dataset not found at: {data_path}")

# Load the dataset
data = pd.read_csv(data_path)

# Print column names to verify
print("Column names in the dataset:", data.columns)

# Clean column names (remove extra spaces and special characters)
data.columns = data.columns.str.strip()  # Remove leading/trailing spaces
print("Cleaned column names:", data.columns)

# Define the target column
target = "Heart Disease"  # Ensure this matches the actual column name in your dataset

# Check if the target column exists
if target not in data.columns:
    raise KeyError(f"Column '{target}' not found in the dataset. Available columns: {data.columns}")

# Convert the target column to numerical values
data[target] = data[target].map({"Presence": 1, "Absence": 0})

# Print class distribution
print("Class distribution:")
print(data[target].value_counts())

# Define features (X) and target (y)
X = data[["Age", "Chest pain type", "BP", "Cholesterol", "Max HR", "ST depression", "Number of vessels fluro", "Thallium"]]
y = data[target]

# Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Print class distribution after resampling
print("Class distribution after resampling:")
print(pd.Series(y_resampled).value_counts())

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save the scaler for later use
scaler_path = os.path.join("data", "models", "scaler.joblib")
os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
joblib.dump(scaler, scaler_path)
print(f"Scaler saved successfully to '{scaler_path}'")

# Initialize the RandomForestClassifier with class weighting
model = RandomForestClassifier(random_state=42, class_weight="balanced")

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
train_accuracy = accuracy_score(y_train, model.predict(X_train))
test_accuracy = accuracy_score(y_test, model.predict(X_test))

print(f"Training Accuracy: {train_accuracy:.2f}")
print(f"Testing Accuracy: {test_accuracy:.2f}")

# Print classification report
print("Classification Report:")
print(classification_report(y_test, model.predict(X_test)))

# Print feature importance
print("Feature Importance:", model.feature_importances_)

# Save the model to a file
model_dir = os.path.join("data", "models")  # Adjusted path
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "heart_disease_model.joblib")
joblib.dump(model, model_path)

print(f"Model saved successfully to '{model_path}'")