import math
import numpy as np
from compute_bates import BatesCall
from BlackScholes import bs_price
from ImpliedVolatility import implied_vol
from scipy import optimize
import json

# Initial values vt,kap,th,sig,rho
x0 =[0.5,0.5,0.5,0.5,-0.5, 0.5, 0.5, 0.5]

# Constraints
lb = [0, 0, 0, 0, -1, 0,-1, -1]
ub = [1, 100, 1, 10, 0, 1, 1,1]


def is_number(val):
	try:
		val = int(val)
		return True
	except ValueError:
		return False


TICKER = "SPXU"
MATURITY = "1/19/18"


with open("{}_CleanedData/{}_CleanedJSON.json".format(TICKER, TICKER)) as data_file:    #Modify the tickername before the underscore sign
	edata = json.load(data_file)
	K = []
	data = []
	for d in edata:
		if d["Type"] == "Call" and float(d["Market"]) > 02:
			data.append(d)


def costf(arr):
	cost = []
	vt,kap,th,sig,rho,lamd,muj,sigj = arr
	N = len(data)
	# for i in range(0,1):
	for d in data:
		St = float(d["Stock"])
		T = float(d["Diff"])
		K = float(d["Strike"])
		r = 0.02
		impvol = implied_vol("c", float(d["Market"]), float(d["Stock"]), float(d["Strike"]), float(d["Diff"]), r)
		BSMVal = bs_price("c", float(d["Stock"]), float(d["Strike"]), float(d["Diff"]), impvol, r, 0)
		BatesVal = BatesCall(St, K, r, T, vt,kap,th,sig,rho,0,lamd,muj,sigj)
		bates_vol = implied_vol("c", BatesVal, float(d["Stock"]), float(d["Strike"]), float(d["Diff"]), r)
		print impvol, bates_vol
		if math.isnan(bates_vol) is False and math.isnan(impvol) is False:
			val = impvol - bates_vol
			cost.append(val)
	return cost


def PassData():
	x = optimize.least_squares(fun=costf, x0=x0, bounds=[lb, ub], verbose=2,max_nfev=5000)
	vt = x.x[0]
	kap = x.x[1]
	th = x.x[2]
	sig = x.x[3]
	rho = x.x[4]
	lambd = x.x[5]
	muj = x.x[6]
	sigj = x.x[7]
	return {
		"vt": vt,
		"kap": kap,
		"th": th,
		"sig": sig,
		"rho": rho,
		"lambd": lambd,
		"muj":muj,
		"sigj": sigj
	}
	

print PassData()

