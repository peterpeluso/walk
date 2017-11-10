import option
import walk
import numpy as np
import abc
class Portfolio:

	def __init__(self, init_capital, market):
		
		self.__init_capital = init_capital
		self.stock_position = []
		self.option_positin = []
		self.market = market

	def add_option(self, option):
		self.options.append(option)

	def add_stock(self, symbol, quantity):
		self.stock_position.append(StockPosition(symbol, quantity, market.stock_price(symbol)))


class Position:

    __metaclass__ = abc.ABCMeta

    def __init__(self, type, quantity):
    	self.type = type
    	self.quantiy = quantity
    	self.entry_price = np.nan

    @abc.abstractmethod
    def current_price(self):
    	pass

class StockPosition(Position):
	
	def __init__(self, symbol, quantity, entry_price):
		Position.__init__(self, 'stock', quantity)
		self.symbol = symbol
		self.quantity = quantity
		self.entry_price = entry_price

