import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

st.set_page_config(page_title="FairSplit AI", layout="centered")

st.title("⚡ FairSplit AI")
st.caption("By Students, For Students | Powered by Real Data")

# --- Load Data ---
df = pd.read_csv("6-Month_Updated_Room_Energy_Usage_Data.csv")
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

# --- Forecast Section ---
st.subheader("🔍 Room A: 15-Day Forecast")

room = df[df['room_id'] == 'Room A'].copy()

# Features and Target
features = ['room_size', 'occupancy_hours', 'device_count', 'avg_temp']
X = room[features]
y = room['kwh_used']

# Train/Test Split
X_train, X_test = X[:-15], X[-15:]
y_train, y_test = y[:-15], y[-15:]

# Train Model
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Accuracy
r2 = r2_score(y_test, predictions)

# Plot
fig, ax = plt.subplots()
ax.plot(room['date'].iloc[-15:], y_test.values, label="Actual", marker='o')
ax.plot(room['date'].iloc[-15:], predictions, label="Forecast", marker='x')
ax.set_title("Room A Energy Forecast")
ax.set_xlabel("Date")
ax.set_ylabel("kWh Used")
ax.legend()
st.pyplot(fig)

# Display Score
st.caption(f"📈 Linear Regression Accuracy (R²): **{round(r2, 2)}**")
