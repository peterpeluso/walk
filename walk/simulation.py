import walk
import option

class Simulation(object):

	def __init__(self, portfolio, market):

		self.portfolio = portfolio
		self.market = market

	def run(self):

		for time in range(0, 251):
			pass