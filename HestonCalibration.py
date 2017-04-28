import math
import numpy as np
from compute_heston import HestonCall
from BlackScholes import bs_price
from ImpliedVolatility import implied_vol
from scipy import optimize
import json

x0 =[0.5,0.5,0.5,0.5,-0.5]

# Constraints
lb = [0, 0, 0, 0, -1]
ub = [1, 100, 1, 10, 0]


def is_number(val):
	try:
		val = int(val)
		return True
	except ValueError:
		return False


TICKER = "SSO"
MATURITY = "9/15/17"
with open("{}_CleanedData/{}_CleanedJSON.json".format(TICKER, TICKER)) as data_file:    #Modify the tickername before the underscore sign
	edata = json.load(data_file)
	K = []
	data = []
	for d in edata:
		if d["Type"] == "Call" and float(d["Market"]) > 0 and float(d["Moneyness"]) > 1 and d["Maturity"] == MATURITY :
			data.append(d)

print data

def costf(arr):
	cost = []
	vt,kap,th,sig,rho = arr
	N = len(data)
	for d in data:
		# d = data[i]
		St = float(d["Stock"])
		T = float(d["Diff"])
		K = float(d["Strike"])
		r = 0.02
		impvol = implied_vol("c", float(d["Market"]), float(d["Stock"]), float(d["Strike"]), float(d["Diff"]), r)
		BSMVal = bs_price("c", float(d["Stock"]), float(d["Strike"]), float(d["Diff"]), impvol, r, 0)
		heston_vol = implied_vol("c", HestonCall(St, K, r, T, vt,kap,th,sig,rho,0), float(d["Stock"]), float(d["Strike"]), float(d["Diff"]), r)
		print impvol, heston_vol
		if math.isnan(heston_vol) is False and math.isnan(impvol) is False:
			val = impvol - heston_vol
			cost.append(val)
	return cost


def PassData():
	x = optimize.least_squares(fun=costf, x0=x0, bounds=[lb, ub], verbose=2)
	# x = optimize.leastsq(costf, x0)
	# print x
	vt = x.x[0]
	kap = x.x[1]
	th = x.x[2]
	sig = x.x[3]
	rho = x.x[4]
	return {
		"vt": vt,
		"kap": kap,
		"th": th,
		"sig": sig,
		"rho": rho
	}
	

print PassData()

