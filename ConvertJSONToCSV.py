import json
import csv

def read_json(filename):
	return json.loads(open(filename).read())
 
def write_csv(data, filename):
	with open(filename, 'w') as outf:
		dw = csv.DictWriter(outf, data[0].keys())
		dw.writeheader()
		for row in data:
			dw.writerow(row)

TICKERS = ["SH", "SDS", "SPXU", "UPRO", "SSO"]

for TICKER in TICKERS:
	write_csv(read_json('{}_WithHestonPrice.json'.format(TICKER)), 'CSVWithHestonPrices/{}_WithHestonPrice_CSV.csv'.format(TICKER))
