import json
TICKERS = ["SPXU","SDS", "SH", "SPY", "UPRO", "SSO"]
from operator import itemgetter

def GetNumbers(data):
	return len(data)


def ReadFile():
	Main = {}
	for TICKER in TICKERS:
		with open("{}_CleanedData/{}_CleanedJSON.json".format(TICKER, TICKER)) as data_file:    
			json_data = json.load(data_file)
		Main[TICKER] = GetNumbers(json_data)
	return Main


print json.dumps(ReadFile())

