import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Loading the Iris dataset
iris = load_iris()
X = iris.data  # Feature data
y = iris.target  # Target labels

print("Data loaded successfully.")
print("Feature names:", iris.feature_names)  # Print feature names (e.g., sepal length, petal width)
print("Target names:", iris.target_names)  # Print target class names (e.g., setosa, versicolor, virginica)
print("First 5 samples:", X[:5])  # Display the first 5 feature samples
print("First 5 target values:", y[:5])  # Display the first 5 target labels

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Data split into training and testing sets.")
print("Training data shape:", X_train.shape)  # Print the shape of the training data
print("Test data shape:", X_test.shape)  # Print the shape of the test data

# Scaling the data (normalization)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # Fit and transform the training data
X_test = scaler.transform(X_test)  # Transform the test data using the same scaler

print("Data scaled.")

# Creating the K-Nearest Neighbors (KNN) model
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)  # Train the model on the training data

print("Model trained.")

# Making predictions on the test data
y_pred = model.predict(X_test)

# Evaluating accuracy and other metrics
print("Accuracy:", accuracy_score(y_test, y_pred))  # Print the accuracy of the model
print("Classification Report:\n", classification_report(y_test, y_pred, target_names=iris.target_names))  # Print detailed classification metrics