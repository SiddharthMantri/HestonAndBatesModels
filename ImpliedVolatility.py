from BlackScholes import bs_price, bs_vega
from vollib.black import implied_volatility
from vollib.black import black
import math
from scipy.stats import norm
from vollib.black_scholes.implied_volatility import implied_volatility
def implied_vol(cp_type, target_value, S, K, T, r):
	return implied_volatility(target_value, S, K, T, r, cp_type)





