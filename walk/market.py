import stock
import matplotlib.pyplot as plt 
import numpy as np
class Market(object):

	def __init__(self):

		self.stocks = {}
		self.t = 0
		self.weights = []

	def add_symbol(self, symbol):

		S0 = 100
		mu = 1
		sigma = 0.2
		T = 1
		mu_j = 0 
		sigma_j = 1
		lamda = .02

		if symbol in self.stocks:
			raise ValueError("Stock already exists")

		self.stocks[symbol] = stock.Stock(symbol, S0, mu, sigma, T, mu_j, sigma_j, lamda)

	def add_symbols(self, symbols):
		for i in symbols:
			self.add_symbol(i)

	def plot_stocks(self):

		for _, stk in self.stocks.items():
			plt.plot(stk.walk.df['t'], stk.walk.df['S'])
		plt.show()

	def stock_nparr(self, symbol):
		if symbol not in self.stocks:
			raise ValueError("Stock is not in market")
		return self.stocks[symbol].walk.S

	def stock_price(self, symbol):
		return self.stocks[symbol].df['S'][self.t]

	def create_index(self, *args):
		""" Generates a market index 

		    Args: list of tuples with (ticker symbol, weight(as decimal))
		"""
		if args:
			self.weights = args[0]
		self.index = np.empty(0)
		counter = 0 
		for (symbol, weight) in self.weights: 
			
			if symbol not in self.stocks:
				ValueError("Stock is not in market")
			if counter == 0:
				tmp = self.stock_nparr(symbol)* weight
			else:
				tmp = np.sum((tmp, self.stock_nparr(symbol)* weight), axis=0)
			counter += 1
			
		self.index = tmp


def main():
	
	market = Market()
	symbols = ["SPX", "SPY", "QQQ", "CL"]
	weights = [0.50, 0.1, 0.2, 0.2]
	index = []
	for i in range(4):
		index.append((symbols[i], weights[i]))

	market.add_symbols(symbols)
	market.create_index(index)
	for i in symbols:
		print(market.stock_nparr(i))
	print(market.index)



if __name__ == '__main__':
	main()

