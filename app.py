import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Helper functions
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def black_scholes_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def get_text_color(value, vmin, vmax):
    mid = (vmin + vmax) / 2
    return 'white' if value > mid else 'black'

# Streamlit App
st.set_page_config(layout="wide")
st.title("Options Risk Matrix (Black-Scholes Model)")

# Sidebar Inputs
st.sidebar.header("Option Parameters")
ticker_input = st.sidebar.text_input("Enter Ticker Symbol", value="AAPL").upper()

try:
    ticker = yf.Ticker(ticker_input)
    expirations = ticker.options
    if not expirations:
        raise ValueError("No expiration dates found.")
except Exception as e:
    st.error(f"Invalid ticker symbol or data fetch error: {e}")
    st.stop()

# Auto-select expiration ~60 days out if available
today = pd.to_datetime("today").normalize()
expiration_dates = pd.to_datetime(expirations)
selected_exp_date = next((e for e in expiration_dates if (e - today).days >= 60), expiration_dates[0])
selected_exp = st.sidebar.selectbox("Select Expiration Date", expirations, index=expiration_dates.tolist().index(selected_exp_date))

rf_rate = st.sidebar.slider("Risk-Free Rate", 0.00, 0.10, 0.045, 0.001)
vol_range_slider = st.sidebar.slider("Volatility Range (Min, Max)", 0.05, 1.0, (0.2, 0.8), 0.01)

# Fetch and compute parameters
ticker_data = ticker.history(period='1mo')
current_price = ticker_data['Close'].iloc[-1]
log_returns = np.log(ticker_data['Close'] / ticker_data['Close'].shift(1)).dropna()
est_volatility = log_returns.std() * np.sqrt(252)

# Time to maturity
expiry_date = pd.to_datetime(selected_exp)
ttm = (expiry_date - today).days / 365

# Ranges
strike_range = np.round(np.linspace(current_price * 0.8, current_price * 1.2, 10), 2)
vol_range = np.round(np.linspace(vol_range_slider[0], vol_range_slider[1], 10), 2)

# Matrix generation
def create_option_matrix(call=True):
    matrix = np.zeros((len(vol_range), len(strike_range)))
    for i, sigma in enumerate(vol_range):
        for j, K in enumerate(strike_range):
            price = (
                black_scholes_call(current_price, K, ttm, rf_rate, sigma)
                if call else
                black_scholes_put(current_price, K, ttm, rf_rate, sigma)
            )
            matrix[i, j] = price
    return pd.DataFrame(matrix, index=vol_range, columns=strike_range)

call_df = create_option_matrix(call=True)
put_df = create_option_matrix(call=False)

# Plotting side-by-side heatmaps
fig, axs = plt.subplots(1, 2, figsize=(14, 6))
vmin = min(call_df.min().min(), put_df.min().min())
vmax = max(call_df.max().max(), put_df.max().max())

# Annotate with dynamic text color
call_annotations = np.empty_like(call_df.values, dtype=object)
put_annotations = np.empty_like(put_df.values, dtype=object)
call_colors = np.empty_like(call_df.values, dtype=object)
put_colors = np.empty_like(put_df.values, dtype=object)

for i in range(len(vol_range)):
    for j in range(len(strike_range)):
        val_c = call_df.iloc[i, j]
        val_p = put_df.iloc[i, j]
        call_annotations[i, j] = f"{val_c:.2f}"
        put_annotations[i, j] = f"{val_p:.2f}"
        call_colors[i, j] = get_text_color(val_c, vmin, vmax)
        put_colors[i, j] = get_text_color(val_p, vmin, vmax)

sns.heatmap(call_df, ax=axs[0], cmap='RdYlGn', cbar=True, annot=call_annotations,
            fmt='', annot_kws={"size": 8, "color": "black"}, vmin=vmin, vmax=vmax,
            linewidths=0, xticklabels=True, yticklabels=True,
            cbar_kws={"label": "Call Option Price ($)"})
axs[0].set_title("Call Price Heatmap")
axs[0].set_xlabel("Strike Price")
axs[0].set_ylabel("Volatility")
axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=0) 


for label in axs[0].get_xticklabels():
    label.set_fontsize(8)

sns.heatmap(put_df, ax=axs[1], cmap='RdYlGn', cbar=True, annot=put_annotations,
            fmt='', annot_kws={"size": 8, "color": "black"}, vmin=vmin, vmax=vmax,
            linewidths=0, xticklabels=True, yticklabels=False,
            cbar_kws={"label": "Put Option Price ($)"})
axs[1].set_title("Put Price Heatmap")
axs[1].set_xlabel("Strike Price")
axs[1].set_ylabel("")
axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=0) 

for label in axs[1].get_xticklabels():
    label.set_fontsize(8)

plt.tight_layout()
st.pyplot(fig)

# Footer warning if matrix empty
if call_df.empty or put_df.empty:
    st.warning("Please enter valid parameters to generate matrices.")
