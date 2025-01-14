In the first block of the code I simply applied the Black and Scholes formula, and at the end, I let the user choose what he would like to evaluate: a call option or a put option.
In the second block of code, Is still a put or a call options but using a Monte Carlo that with 10000 simulations replicates a Geometric Brownian Motion using the usual variables: initial price S0, strike price K, time to maturity T, risk-free rate r, and volatility sigma, with an additional random shock Z, sampled from a Standard Normal Distribution, which can be generated using np.random.standard_normal.
The idea is that for each scenario, a value for Z and ST is generated. Then, ST is compared with strike price K and: 
For a call option, the payoff is max⁡(0,S_T−K).
For a put option, the payoff is max⁡(0,K−S_T).
Essentially, we calculate the payoff under each scenario. The final option price is obtained by averaging these payoffs and discounting them back to the present value, as these payoffs represent the value at time T.
