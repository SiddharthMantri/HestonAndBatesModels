from BlackScholes import bs_price
from ImpliedVolatility import implied_vol
import math


S = 102 
K = 100
T =  731.0/365
r = 0.05
v = 0.25

target =  bs_price("c",S,K,T,v,r,q=0.0)
print target

p =  S - target - (K*math.exp(-r*T))
print p
print implied_vol("c", target, S, K, T, r)