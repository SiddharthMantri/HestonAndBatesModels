import json
import plotly
import plotly.graph_objs as go
from plotly import tools


# plotly.plotly.sign_in("Newtt","V9IjGaICscoTTDmVNcN3")


def LoadData(ticker):
	with open("{}_WithHestonPrice.json".format(ticker)) as data_file:    
		json_data = json.load(data_file)
	return json_data



def PlotHestonData(data, Ticker):
	HestonPriceData = []
	PutData = []
	MarketData = []
	CallVega = []
	PutMarket = []
	Strike = []
	PutStrike = []
	Diff = []
	PutDiff = []
	PutVega = []
	MarketVega = []
	MarketPutVega = []
	for d in data:
		if float(d["Moneyness"]) and d["Type"] == "Call":
			HestonPriceData.append(d["Heston_Call"])
			MarketData.append(float(d["BSM_Price"]))
			Strike.append(float(d["Strike"]))
			Diff.append(float(d["Diff"]))
			CallVega.append(float(d["Heston_Vega"]))
			MarketVega.append(float(d["Market_Vega"]))
		elif float(d["Moneyness"]) and d["Type"] == "Put":
			PutData.append(d["Heston_Call"])
			PutMarket.append(float(d["BSM_Price"]))
			PutStrike.append(float(d["Strike"]))
			PutDiff.append(float(d["Diff"]))
			PutVega.append(float(d["Heston_Vega"]))
			MarketPutVega.append(float(d["Market_Vega"]))
	mins = min(HestonPriceData)
	maxs = max(HestonPriceData)
	trace1 = go.Scatter(
		x = Strike,
		y=HestonPriceData,
		name="Heston Model Prices",
		mode="lines+markers"
	)
	trace2 = go.Scatter(
		x = Strike,
		y=MarketData,
		name="Market Prices",
		mode="lines+markers"
	)
	trace3 = go.Scatter(
		x = PutStrike,
		y=PutMarket,
		name="Market Put Prices",
		mode="lines+markers"
	)
	trace4 = go.Scatter(
		x = PutStrike,
		y=PutData,
		name="Heston Model Put Prices",
		mode="lines+markers"
	)
	trace5 = go.Scatter(
		x = PutVega,
		y=MarketPutVega,
		name="Heston Model PutVega Prices",
		mode="lines+markers"
	)
	trace6 = go.Scatter(
		x = CallVega,
		y=MarketVega,
		name="Heston Model CallVega Prices",
		mode="lines+markers"
	)
	data = [trace1, trace2,trace3, trace4, trace5, trace6]
	layout = go.Layout(
	    title='Comparing Market Price vs Heston Model Price for {}'.format(Ticker),
	    xaxis=dict(
	        title='Strike',
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    ),
	    yaxis=dict(
	        title='Price',
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        ),
	    ),
	)
	fig = go.Figure(data=data, layout=layout)
	plotly.offline.plot(fig,filename="DataPlots/{}_PricePlot_Heston".format(Ticker))
	plotly.plotly.image.save_as(fig, filename="DataPlots/{}_PricePlot_Heston.png".format(Ticker))


def PlotVega(data, Ticker, Model):
	HestonPriceData = []
	PutData = []
	MarketData = []
	CallVega = []
	PutMarket = []
	Strike = []
	PutStrike = []
	Diff = []
	PutDiff = []
	PutVega = []
	MarketVega = []
	MarketPutVega = []
	for d in data:
		if float(d["Moneyness"]) and d["Type"] == "Call":
			HestonPriceData.append(d["Heston_Call"])
			MarketData.append(float(d["BSM_Price"]))
			Strike.append(float(d["Strike"]))
			Diff.append(float(d["Diff"]))
			CallVega.append(float(d["Heston_Vega"]))
			MarketVega.append(float(d["Market_Vega"]))
		elif float(d["Moneyness"]) and d["Type"] == "Put":
			PutData.append(d["Heston_Call"])
			PutMarket.append(float(d["BSM_Price"]))
			PutStrike.append(float(d["Strike"]))
			PutDiff.append(float(d["Diff"]))
			PutVega.append(float(d["Heston_Vega"]))
			MarketPutVega.append(float(d["Market_Vega"]))
	trace5 = go.Scatter(
		x = PutVega,
		y=MarketPutVega,
		name="Heston Model PutVega Prices",
		mode="lines+markers"
	)
	trace6 = go.Scatter(
		x = CallVega,
		y=MarketVega,
		name="Heston Model CallVega Prices",
		mode="lines+markers"
	)
	data = [trace5, trace6]
	layout = go.Layout(
	    title='Comparing Vega of {} Model Prices vs  Vega of Market Prices for {}'.format(Model, Ticker),
	    xaxis=dict(
	        title='Strike',
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    ),
	    yaxis=dict(
	        title='Price',
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        ),
	    ),
	)
	fig = go.Figure(data=data, layout=layout)
	plotly.offline.plot(fig,filename="DataPlots/{}_VegaPlot_Heston".format(Ticker))
	plotly.plotly.image.save_as(fig, filename="DataPlots/{}_VegaPlot_Heston.png".format(ticker))

	
def PlotBatesData(data, Ticker):
	HestonPriceData = []
	PutData = []
	MarketData = []
	PutMarket = []
	Strike = []
	PutStrike = []
	Diff = []
	PutDiff = []
	for d in data:
		if float(d["Moneyness"]) and d["Type"] == "Call":
			HestonPriceData.append(d["Bates_Call"])
			MarketData.append(float(d["BSM_Price"]))
			Strike.append(float(d["Strike"]))
			Diff.append(float(d["Diff"]))
		elif float(d["Moneyness"]) and d["Type"] == "Put":
			PutData.append(d["Bates_Call"])
			PutMarket.append(float(d["BSM_Price"]))
			PutStrike.append(float(d["Strike"]))
			PutDiff.append(float(d["Diff"]))
	mins = min(HestonPriceData)
	maxs = max(HestonPriceData)
	trace1 = go.Scatter(
		x = Strike,
		y=HestonPriceData,
		name="Bates Model Call Prices",
		mode="lines+markers"
	)
	trace2 = go.Scatter(
		x = Strike,
		y=MarketData,
		name="Market Call Prices",
		mode="lines+markers"
	)
	trace3 = go.Scatter(
		x = PutStrike,
		y=PutMarket,
		name="Market Put Prices",
		mode="lines+markers"
	)
	trace4 = go.Scatter(
		x = PutStrike,
		y=PutData,
		name="Bates Model Put Prices",
		mode="lines+markers"
	)
	data = [trace1, trace2, trace3, trace4]
	layout = go.Layout(
	    title='Comparing Market Price vs Bates Model Price for {}'.format(Ticker),
	    xaxis=dict(
	        title='Strike',
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    ),
	    yaxis=dict(
	        title='Price',
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        ),
	    ),
	)
	fig = go.Figure(data=data, layout=layout)
	plotly.offline.plot(fig, filename="{}_PricePlot_Bates".format(Ticker))
	plotly.plotly.image.save_as(fig, filename="{}_PricePlot_Bates.png".format(Ticker))


def GetImpliedVolatilitiesAndPlotSmile(data, ticker):
	HestonVolatility = []
	MarketVolatility = []
	Strike = []
	Diff = []
	for d in data:
		if float(d["Moneyness"]):
			K = float(d["Moneyness"])
			# if K not in Strike:
			HestonVolatility.append(d["Model_Vol"])
			MarketVolatility.append(d["Market_Vol"])
			Strike.append(K)
			Diff.append(float(d["Diff"]))
	trace1 = go.Scatter(
		x=Strike,
		y=HestonVolatility,
		name="Model Volatility",
		mode="lines+markers"
	)
	trace2 = go.Scatter(
		x=Strike,
		y=MarketVolatility,
		name="Market Volatility",
		mode="lines+markers"
	)
	data = [trace1, trace2]
	layout = go.Layout(
	    autosize=False,
	    width=1020,
	    height=768,
	    title="Model Implied Volatility vs Market Implied Volatility for {}".format(ticker),
	    xaxis={
	    	'title': 'Moneyness = Strike/Stock'
	    },
	    yaxis={
	    	'title': 'Implied Volatility',
	    },
	)
	fig = go.Figure(data=data, layout=layout, )
	plotly.offline.plot(fig, filename="DataPlots/{}_VolPlot_Heston".format(ticker))
	plotly.plotly.image.save_as(fig, filename="DataPlots/{}_VolPlot_Bates.png".format(ticker))


# data = LoadData("SDS")
# # GetImpliedVolatilitiesAndPlotSmile(data)
# PlotData(data)



