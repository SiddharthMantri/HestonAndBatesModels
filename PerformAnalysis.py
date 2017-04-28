import math
import numpy as np
from compute_heston import HestonCall
from BlackScholes import bs_price as BSM
from ImpliedVolatility import implied_vol, implied_volatility
from scipy import optimize
import json
from compute_heston import HestonCall
from CalibratedJSON import CALIBRATED_JSON
from PlotData import PlotHestonData, GetImpliedVolatilitiesAndPlotSmile, PlotVega
from operator import itemgetter

from vollib.black_scholes.greeks import numerical

vega = numerical.vega

r = 0.02

def ReturnImpliedVol(d):
	option_type = d["Type"][0].lower()
	heston_vol = implied_vol(option_type, float(d["Heston_Call"]),  float(d["Stock"]), float(d["Strike"]), float(d["Diff"]),r)
	market_vol = implied_vol(option_type, float(d["Market"]), float(d["Stock"]), float(d["Strike"]), float(d["Diff"]), r)
	bsm_price = BSM(option_type, float(d["Stock"]), float(d["Strike"]), float(d["Diff"]), market_vol, r, 0)
	d["Model_Vol"] = heston_vol
	d["Market_Vol"] = market_vol
	d["BSM_Price"] = bsm_price
	d["Heston_Vega"] = vega(option_type, float(d["Stock"]), float(d["Strike"]), float(d["Diff"]), r, heston_vol)
	d["Market_Vega"] = vega(option_type, float(d["Stock"]), float(d["Strike"]), float(d["Diff"]), r, market_vol)
	return d

# print HestonCall(13.35, 14.5, 0.002, 0.0876712329, 0.12, 2, 0.3223, 0.3223, -0.9, 0)

def PassStockStrikeAndTimeAndGetHestonCallPrice(St, K, T , ticker):
	vt = CALIBRATED_JSON[ticker]["vt"]
	kap = CALIBRATED_JSON[ticker]["kap"]
	th = CALIBRATED_JSON[ticker]["th"]
	sig = CALIBRATED_JSON[ticker]["sig"]
	rho = CALIBRATED_JSON[ticker]["rho"]
	return HestonCall(St, K, r, T, vt,kap,th,sig,rho, 0)



def ReadDataAndPassParams(data, ticker, maturity):
	strike = []
	FinalData = []
	for d in data:
		St = float(d["Stock"])
		T = float(d["Diff"])
		K = float(d["Strike"])
		if float(d["Moneyness"]) and float(d["Market"]) > 0 and d["Maturity"] == maturity:
			price = PassStockStrikeAndTimeAndGetHestonCallPrice(St, K, T, ticker)
			if d["Type"] == 'Call':
				d["Heston_Call"] = price
			else:
				p =  St - price - (K*math.exp(-r*T))
				d["Heston_Call"] = -1 * p
			d = ReturnImpliedVol(d)
			FinalData.append(d)
	return FinalData


FILE_DIR = "FinalData/{}"
OP_FILE_SUFFIX = "{}.json"
S_FILE_SUFFIX = "{}.json"


def GetErrorVol(data):
	N = len(data)
	print N
	sumval = 0
	for d in data:
		if math.isnan(d["Market_Vol"]) is False and math.isnan(d["Model_Vol"]) is False:
			sumval = math.fabs(d["Market_Vol"] - d["Model_Vol"])/d["Market_Vol"]
	return sumval/float(N)


def GetErrorPrice(data):
	N = len(data)
	sumval = 0
	for d in data:
		if math.isnan(d["Heston_Call"]) is False and math.isnan(d["Market"]) is False:
			sumval = math.fabs(d["Market"] - d["Heston_Call"])/d["Market"]
	return sumval/float(N)


def LoadFileAndEnhance(TICKER, Maturity):
	with open("{}_CleanedData/{}_CleanedJSON.json".format(TICKER, TICKER)) as data_file:    
		json_data = json.load(data_file)
	enhance_json = ReadDataAndPassParams(json_data, TICKER, Maturity)	
	enhanced_json = sorted(enhance_json, key=itemgetter('Strike'))	
	if len(enhanced_json) == 0: print TICKER
	print "Volatililty error: {}".format(GetErrorVol(enhanced_json))
	print "Price Error: {}".format(GetErrorPrice(enhanced_json))
	print "We are finished enhancing with heston call prices for {}".format(TICKER)	
	return enhanced_json


TICKERS = {
	# "SPXU": "9/15/17",
	"SDS": "09/15/2017", 			
	"SH": "11/17/2017", 
	"SPY": "9/15/2017", 
	"UPRO": "9/15/2017", 
	"SSO": "9/15/17"
}
import plotly
plotly.plotly.sign_in("Newtt","V9IjGaICscoTTDmVNcN3")
for DATA_TICKER, Maturity in TICKERS.iteritems():
	# DATA_TICKER = "UPRO"
	# Maturity = "9/15/2017"	
	data = LoadFileAndEnhance(DATA_TICKER, Maturity)
	print json.dumps(data)
	PlotHestonData(data, DATA_TICKER)
	PlotVega(data, DATA_TICKER, "Heston")
	# GetImpliedVolatilitiesAndPlotSmile(data, DATA_TICKER) # Uncomment this line to see volatility smiles. Please comment above line first
