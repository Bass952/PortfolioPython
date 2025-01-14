# -*- coding: utf-8 -*-
"""BSM and Monte Carlo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15GxOmIp-Eixv22HaeN1nVn5y7Ps2-kEj

#Black and Scholes for Option Pricing

"""

import numpy as np
from scipy.stats import norm

#We set up the well known formula of Black-Scholes for option pricing:
def BSM(St, K, T, r, sigma, OPT):
  d1 = (np.log(St/K)+(r + 0.5*sigma**2)*T)/(np.sqrt(T) * sigma)
  d2 = d1 - sigma * np.sqrt(T)
  if OPT == "call":
    price = St*norm.cdf(d1) - K*np.exp(-r*T) * norm.cdf(d2)
  else:
    price = -St*norm.cdf(-d1)+K*np.exp(-r*T) * norm.cdf(-d2)
  return price

# Ask the user for the option type
option_type = input("Would you like to evaluate a 'put' or a 'call' option? ").strip().lower()

# Check user input and calculate the option price
if option_type in ["put", "call"]:
    price = BSM(100, 105, 2, 0.05, 0.2, option_type)
    print(f"The price of the {option_type} option is: {price: }")
else:
    print("Invalid input. Please choose 'put' or 'call'.")

"""#Monte Carlo Simulation for Option Pricing

Using the Monte Carlo method, we generate N scenarios for stock price ST, where the stock price follows a Gometric Brownian Motion. The variables used include: initial price S0, strike price K, time to maturity T, risk-free rate r, and volatility sigma, with an additional random shock Z, sampled from a Standard Normal Distribution, which can be generated using np.random.standard_normal.

The idea is that for each scenario, a value for Z and S_T is generated. Then, S_T is compared with strike price K and:

    For a call option, the payoff is max⁡(0,S_T−K).
    For a put option, the payoff is max⁡(0,K−S_T).

Essentially, we calculate the payoff under each scenario. The final option price is obtained by averaging these payoffs and discounting them back to the present value, as these payoffs represent the value at time T.
"""

import numpy as np

def monte_carlo_option_pricing(S0, K, T, r, sigma, N, option_type="call"):
    # Generate random numbers Z (random shock)
    Z = np.random.standard_normal(N)

    # Simulate ST prices using geometric Brownian motion
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * Z * np.sqrt(T))

    # Calculate payoff
    if option_type == "call":
        payoff = np.maximum(0, ST - K)
    elif option_type == "put":
        payoff = np.maximum(0, K - ST)

    # Option price: discounted mean of payoffs
    option_price = np.exp(-r * T) * np.mean(payoff)

    return option_price

S0 = 100  # Initial stock price
K = 105   # Strike price
T = 1     # Time to maturity
r = 0.04  # Risk-free rate
sigma = 0.2  # Volatility
N = 100000  # Number of simulations

# Call option price
call_price = monte_carlo_option_pricing(S0, K, T, r, sigma, N, option_type="call")
print(f"Call option price: {call_price}")

# Put option price
put_price = monte_carlo_option_pricing(S0, K, T, r, sigma, N, option_type="put")
print(f"Put option price: {put_price}")
