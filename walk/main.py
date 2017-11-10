import walk 
import portfolio
import market
import stock
import option
import simulation
market = market.Market()
symbols = ['SPX', 'SPY', 'QQQ']
market.add_symbols(symbols)
portfolio = portfolio.Portfolio(1000000, market)

sim = simulation.Simulation(portfolio, market)

