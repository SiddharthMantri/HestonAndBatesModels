from numpy import sqrt
from scipy import exp, log
from scipy.stats import norm
from vollib.black_scholes import black_scholes


def d1d2(S, K, T, r, v, q):
	d1 = ( log(S/K) + (r - q + 0.5*v**2)*T ) / (v*sqrt(T))
	d2 = d1 - v*sqrt(T)
	return d1, d2

def put(S, K, T, r, v, q):
	d1, d2 = d1d2(S, K, T, r, v, q)
	N1 = norm.cdf(d1)
	N2 = norm.cdf(d2)
	
	return -S*exp(-q*T)*(1-N1) + K*exp(-r*T)*(1-N2)


def call(S, K, T, r, v, q):

	d1, d2 = d1d2(S, K, T, r, v, q)
	N1 = norm.cdf(d1)
	N2 = norm.cdf(d2)
	
	return S*exp(-q*T)*N1 - K*exp(-r*T)*N2


def bs_price(cp_flag,S,K,T,v,r,q=0.0):
    price = black_scholes(cp_flag, S, K, T, r, v)
    return price

def bs_vega(cp_flag,S,K,T,v,r,q=0.0):
	d1, d2 = d1d2(S, K, T, r, v, q)
	return S * sqrt(T)*norm.pdf(d1)