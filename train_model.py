import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import os

df = pd.read_csv("diabetes.csv")

cols = ["Glucose","BloodPressure","SkinThickness","Insulin","BMI"]
means = {}

for col in cols:
    mean_val = df[col].replace(0, np.nan).mean()
    df[col] = df[col].replace(0, mean_val)
    means[col] = mean_val

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

os.makedirs("model", exist_ok=True)

pickle.dump(model, open("model/model.pkl", "wb"))
pickle.dump(means, open("model/preprocessing.pkl", "wb"))

print("Model saved successfully 🚀")