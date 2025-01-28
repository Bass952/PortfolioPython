# -*- coding: utf-8 -*-
"""MC simulation of implied volatility.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gQZDKNJqMeN1fEHJebW2DgVW9dwFcHmp
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the Black-Scholes option price.

    Arguments:
        S (float): Current stock price.
        K (float): Option strike price.
        T (float): Time to maturity in years.
        r (float): Risk-free interest rate.
        sigma (float): Volatility (standard deviation) of stock returns.
        option_type (str): "call" or "put".

    Returns:
        float: Option price.
    """
    # Compute d1 and d2, key components of the Black-Scholes formula
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Calculate the option price based on the type (call or put)
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

def implied_volatility(S, K, T, r, market_price, option_type="call", tol=1e-5, max_iter=100):
    """
    Calculate implied volatility using the Black-Scholes model and the Newton-Raphson method.

    Arguments:
        S (float): Current stock price.
        K (float): Option strike price.
        T (float): Time to maturity in years.
        r (float): Risk-free interest rate.
        market_price (float): Observed market price of the option.
        option_type (str): "call" or "put".
        tol (float): Tolerance for convergence.
        max_iter (int): Maximum number of iterations.

    Returns:
        float: Implied volatility.
    """
    # Start with an initial guess for volatility
    sigma = 0.2  # Common initial assumption

    for i in range(max_iter):
        # Compute the option price using the current sigma estimate
        price = black_scholes(S, K, T, r, sigma, option_type)

        # Compute Vega (rate of change of option price with respect to volatility)
        vega = S * norm.pdf((np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))) * np.sqrt(T)

        if vega == 0:
            # Stop if Vega is zero to avoid division by zero
            raise ValueError("Zero Vega encountered, iteration stopped.")

        # Compute the difference between market and theoretical price
        diff = market_price - price

        # Check if the difference is within the convergence tolerance
        if abs(diff) < tol:
            return sigma

        # Update sigma using the Newton-Raphson formula
        sigma += diff / vega

    # Raise an error if the method does not converge within the allowed iterations
    raise ValueError("Implied volatility did not converge.")

def monte_carlo_volatility_smile(S, T, r, base_volatility, n_simulations=100):
    """
    Simulate a volatility smile using Monte Carlo methods.

    Arguments:
        S (float): Current stock price.
        T (float): Time to maturity in years.
        r (float): Risk-free interest rate.
        base_volatility (float): Base volatility level.
        n_simulations (int): Number of simulations.

    Returns:
        tuple: Arrays for strike prices (K) and implied volatilities.
    """
    # Generate a range of strike prices (80% to 120% of the current stock price)
    strike_prices = np.linspace(S * 0.8, S * 1.2, 50)
    implied_vols = []  # List to store implied volatilities

    for K in strike_prices:
        # Simulate random volatilities around the base level
        simulated_vols = np.random.normal(base_volatility, 0.05, n_simulations)

        # Calculate market prices for options using these volatilities
        market_prices = [
            black_scholes(S, K, T, r, sigma, option_type="call")
            for sigma in simulated_vols
        ]

        # Average the simulated market prices
        avg_market_price = np.mean(market_prices)

        try:
            # Calculate the implied volatility for the average market price
            iv = implied_volatility(S, K, T, r, avg_market_price, option_type="call")
            implied_vols.append(iv)
        except ValueError:
            # Handle cases where the implied volatility calculation fails
            implied_vols.append(np.nan)

    return strike_prices, np.array(implied_vols)

# Parameters for the Monte Carlo simulation
S = 100  # Current stock price
T = 1.0  # Time to maturity (1 year)
r = 0.05  # Risk-free interest rate
base_volatility = 0.2  # Base level of volatility

# Simulate the volatility smile
strike_prices, implied_vols = monte_carlo_volatility_smile(S, T, r, base_volatility)

# Plot the simulated volatility smile
plt.figure(figsize=(10, 6))
plt.plot(strike_prices, implied_vols, marker="o", linestyle="-", color="blue")
plt.title("Monte Carlo Simulated Volatility Smile")
plt.xlabel("Strike Price (K)")
plt.ylabel("Implied Volatility")
plt.grid(True)
plt.show()