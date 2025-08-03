import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def black_scholes_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def generate_option_matrix(call=True, S=100, K_range=None, T=1.0, r=0.05, sigma_range=None):
    if K_range is None:
        K_range = np.round(np.linspace(S * 0.8, S * 1.2, 10), 2)
    if sigma_range is None:
        sigma_range = np.round(np.linspace(0.2, 0.8, 10), 2)

    matrix = np.zeros((len(sigma_range), len(K_range)))
    for i, sigma in enumerate(sigma_range):
        for j, K in enumerate(K_range):
            if call:
                matrix[i, j] = black_scholes_call(S, K, T, r, sigma)
            else:
                matrix[i, j] = black_scholes_put(S, K, T, r, sigma)
    return matrix, sigma_range, K_range