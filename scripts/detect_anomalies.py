import sys
import os
import pickle
import pandas as pd
import requests
from sklearn.ensemble import IsolationForest

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.feature_extractor import extract_features

# Step 1: Extract features
df = extract_features()

# Step 2: Detect anomalies
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(df)
df["anomaly"] = model.predict(df)

# Step 3: Save results
df.to_csv("data/processed_packets_labeled.csv", index=False)
pickle.dump(model, open("models/anomaly_model.pkl", "wb"))

# Step 4: Send anomalies to dashboard
anomalies = df[df["anomaly"] == -1].to_dict(orient="records")

if anomalies:
    try:
        url = "http://localhost:5000/api/anomalies"  # 🔁 use local URL
        response = requests.post(url, json={"anomalies": anomalies})
        print("Sent anomalies:", response.status_code, response.text)
    except Exception as e:
        print("Failed to send anomalies:", str(e))
else:
    print("No anomalies detected.")
