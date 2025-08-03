# Options Risk Matrix (Black-Scholes Model)



This project provides an interactive Streamlit app for visualizing call and put option prices using the Black-Scholes model. Users can analyze how option premiums change with volatility and strike price, helping them understand risk and reward across different market scenarios.

[Live Demo Coming Soon]

## Preview

Below is an example preview of the Options Risk Matrix heatmaps:

Call and Put Price Heatmaps



## Features

Side-by-side call and put option heatmaps

Dynamic user input:

Ticker symbol

Expiration date (fetched live from options chain)

Risk-free rate

Volatility range

Red-to-green gradient for intuitive pricing visualization

Contrast-sensitive labeling in each matrix cell

Historical volatility estimation using log returns

Spot price line displayed for easy reference

## Tech Stack

- Python

- Streamlit

- Pandas

- NumPy

- Matplotlib

- Seaborn

- SciPy (for norm.cdf)

- yFinance (for market data)

## Installation

Clone the repository:

git clone https://github.com/your-username/options-risk-analysis.git
cd options-risk-analysis

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt

## Running the App

To launch the app:

streamlit run app.py

## Testing

To run all unit tests:

python -m unittest tests.py

## Insights

This project was inspired by educational tools like those seen in options trading tutorials and applications. It is designed to offer a clean, visual interface to understand how option premiums respond to changing market conditions.

Some design decisions:

The volatility slider gives users control over scenario testing.

Expiration dates are real options dates to reflect actual market choices.

The heatmap colors reflect intuitive market sentiment (red = cheap, green = expensive).

In the future, more advanced features like implied volatility modeling, Greeks, or P&L simulation may be added.

License

MIT License

Author

Developed by Cal Teeling as part of a finance and data science portfolio.

