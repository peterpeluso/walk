import walk
class Stock(object):

	def __init__(self,symbol, S0, mu, sigma, T, mu_j, sigma_j, lamda, dt=0.00396825396):
		
		self.walk = walk.JumpDiffusion(S0, mu, sigma, T, mu_j, sigma_j, lamda)
		self.S0 = S0
		self.symbol = symbol
		self.walk.random_walk()
		self.walk.to_df()





