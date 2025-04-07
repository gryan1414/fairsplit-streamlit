import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Streamlit app title
st.title("FairSplit AI: Prototype for Responsible Student Living")

# --- Fair Split Section ---
st.subheader("📊 FairSplit AI vs Equal Split")
# Load the fair split data
df = pd.read_csv('room_usage.csv')

# Bar chart
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(df['Room']))
width = 0.35

ax.bar(x - width/2, df['FairSplit (€)'], width, label='FairSplit (€)', color='skyblue')
ax.bar(x + width/2, df['Equal Split (€)'], width, label='Equal Split (€)', color='lightcoral')

ax.set_xlabel('Room')
ax.set_ylabel('Bill Amount (€)')
ax.set_title('FairSplit AI vs Equal Split')
ax.set_xticks(x)
ax.set_xticklabels(df['Room'])
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
st.pyplot(fig)

# Savings Narrative
st.subheader("🌟 Fairness Insights")
st.markdown("**The table below highlights the savings or extra charges each room faces under Equal Split compared to FairSplit.**")

for idx, row in df.iterrows():
    savings = row['Over/Under (€)']
    if savings > 0:
        st.success(f"{row['Room']} saves €{round(savings, 2)} with FairSplit AI!")
    elif savings < 0:
        st.error(f"{row['Room']} avoids overpaying €{abs(round(savings, 2))} thanks to FairSplit AI!")
    else:
        st.info(f"{row['Room']} pays the same with either method.")