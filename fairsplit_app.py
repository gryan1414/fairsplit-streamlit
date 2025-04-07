
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Page Settings ---
st.set_page_config(page_title="FairSplit AI", page_icon="⚡", layout="wide")

# --- Sidebar Explainer ---
with st.sidebar:
    st.header("📘 How It Works")
    st.markdown("""
    **FairSplit AI** uses real or simulated energy usage (in kWh) to:

    1. ⚡ **Measure** each room’s energy use  
    2. 💸 **Calculate** their share of the total bill  
    3. 📊 **Compare** to an equal split  
    4. 💡 **Show** who overpays or saves

    👉 Use the slider to simulate different bill totals!
    """)

# --- Header & Branding ---
st.title("⚡ FairSplit AI Demo")
st.caption("By Students, For Students | Powered by Real Data")

# --- Description ---
st.markdown("""
FairSplit AI automatically allocates utility bills based on each room's energy consumption. 
This demo shows how fair billing beats equal splits — using real consumption data!
""")

# --- Simulated Data (replace with real sensor/survey data if available) ---
rooms = ['Room A', 'Room B', 'Room C', 'Room D']
energy_kwh = [141.63, 32.06, 67.29, 145.50]
df = pd.DataFrame({
    'Room': rooms,
    'Energy Used (kWh)': energy_kwh
})

total_bill = st.slider("Adjust the Total House Bill (€)", min_value=50, max_value=300, value=120, step=5)

# --- FairSplit Calculations ---
df['FairSplit Bill (€)'] = (df['Energy Used (kWh)'] / df['Energy Used (kWh)'].sum()) * total_bill
df['Equal Split (€)'] = total_bill / len(df)
df['Over/Under Payment (€)'] = df['Equal Split (€)'] - df['FairSplit Bill (€)']

# --- Bill Table ---
st.subheader("📊 Bill Breakdown Table")
st.dataframe(df.style.format({
    'Energy Used (kWh)': '{:.2f}',
    'FairSplit Bill (€)': '€{:.2f}',
    'Equal Split (€)': '€{:.2f}',
    'Over/Under Payment (€)': '€{:.2f}'
}))

# --- Visualization ---
st.subheader("🔍 Visual Comparison")
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(rooms))
width = 0.35

ax.bar(x - width/2, df['FairSplit Bill (€)'], width, label='FairSplit Bill (€)', color='skyblue')
ax.bar(x + width/2, df['Equal Split (€)'], width, label='Equal Split (€)', color='lightcoral')

ax.set_xlabel('Room')
ax.set_ylabel('Bill Amount (€)')
ax.set_title('FairSplit AI vs Equal Split')
ax.set_xticks(x)
ax.set_xticklabels(rooms)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
st.pyplot(fig)

# --- Savings Narrative ---
st.subheader("💡 Fairness Insights")
st.markdown("The table below highlights savings or extra charges each room faces under Equal Split compared to FairSplit:")

for idx, row in df.iterrows():
    savings = row['Over/Under Payment (€)']
    if savings > 0:
        st.success(f"{row['Room']} saves €{round(savings, 2)} with FairSplit AI!")
    elif savings < 0:
        st.error(f"{row['Room']} avoids overpaying €{abs(round(savings, 2))} thanks to FairSplit AI!")
    else:
        st.info(f"{row['Room']} pays the same with either method.")

# --- Forecast Section ---
st.subheader("📈 15-Day Energy Forecast for Room A")

# Load CSV data (if not already loaded earlier in the script)
df = pd.read_csv("room_energy_data.csv")

# Convert date
df['date'] = pd.to_datetime(df['date'], dayfirst=True)
df = df[df['room_id'] == 'Room A']  # Filter for Room A only

# Features & target
X = df[['room_size', 'occupancy_hours', 'device_count', 'avg_temp']]
y = df['kwh_used']

# Train/test split
X_train, X_test = X[:-15], X[-15:]
y_train, y_test = y[:-15], y[-15:]

# Fit model
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Plot actual vs predicted
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(df['date'][-15:], y_test.values, label='Actual')
ax.plot(df['date'][-15:], y_pred, label='Predicted')
ax.set_title("Forecasted vs Actual Energy Use (kWh)")
ax.set_ylabel("Energy (kWh)")
ax.set_xlabel("Date")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Caption
st.caption("⚠️ Forecast is simulated based on linear regression with room features.")

# --- Footer ---
st.markdown("---")
st.caption("FairSplit AI | Prototype for Responsible Student Living")
