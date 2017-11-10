import math
import numpy as np
import matplotlib.pyplot as plt
import random
import abc
import pandas as pd
np.set_printoptions(threshold=10)

class RandomWalkBase:
    """Base Class for creating random walk classes """
    __metaclass__ = abc.ABCMeta

    def __init__(self, S0, mu, sigma, T, dt=0.00396825396):
        """
        Parameters
        ----------

        S0 : double 
            starting stock price
        sigma : double
            stock volatility
        mu : double
             drift term
        T : int 
            number of days simulated
        dt : double, optional
            step size
        """

        self.s0 = S0
        self.sigma = sigma
        self.mu = mu
        self.T = T
        self.dt = dt
        self.N = round(T/self.dt)
        """int : number of steps """
        self.S = []
        """ list of double : used to store generated random walk """
        self.t = None
        """ np array : used to store every step from 0 to T """
        self.df = None
        """ pandas df: used to store multiple walks for monte carlo """

    @abc.abstractmethod
    def random_walk(self):
        """ generates a random walk
        Parameters
        ----------
        None

        Returns
        -------
        None 
        """
        pass

    def plot(self):
        """plots the random walk

        Parameters
        ----------
        None

        Returns
        -------
        None 
        """
        self.random_walk()
        plt.plot(self.t, self.S)
        plt.show()

    def monte_carlo_walks(self, n=50):
        """Generates n random walks

        Parameters
        ----------
        n : double , optional
            number of random walks to generate

        Returns
        -------
        None

        """
        self.S_arr = []

        for i in range(n):
            self.random_walk()
            self.S_arr.append(self.S)

        self.S_arr = np.array(self.S_arr)

        plt.subplot(2, 1, 1)

        for i in range(n):
            plt.plot(self.t, self.S_arr[i])

        plt.xlabel("Time")
        plt.ylabel("Price")

        plt.subplot(2, 1, 2)

        plt.xlabel("Price")
        plt.hist(self.S_arr[:, int(self.N - 1)],  bins=10)
        plt.axvline(self.s0, color="black")
        plt.show()

    def to_df(self):
        self.df = pd.DataFrame({'t': self.t, 'S': self.S})


class GeometricBrownianMotion(RandomWalkBase):
    """ simulates geometric brownian motion with drift """

    def __init__(self, S0, mu, sigma, T, dt=0.00396825396):
        RandomWalkBase.__init__(self, S0, mu, sigma, T, dt)

    def random_walk(self):
        """ generates the random walk and stores in numpy arrr S """

        self.t = np.linspace(0, self.T, self.N)
        W = np.random.standard_normal(size=int(self.N))
        W = np.cumsum(W)*np.sqrt(self.dt)
        X = (self.mu-0.5*self.sigma**2)*self.t + self.sigma*W
        self.S = self.s0*np.exp(X)


class JumpDiffusion(RandomWalkBase):
    """ Geometric brownian motion with jump process """
    def __init__(self, S0, mu, sigma, T, mu_j, sigma_j, lamda,
                 dt=0.00396825396):
        """
        Parameters
        ----------

        S0 : double 
            starting stock price
        sigma : double
            stock volatility
        mu : double
             drift term
        T : int 
            number of days simulated
        mu_j : double
            mu of jump size
        sigma_j: double
            sigma of jump size
        lamda : double
            lambda of jump
        dt : double, optional
            step size
        """


        RandomWalkBase.__init__(self, S0, sigma, mu, T, dt)
        self.mu_j = mu_j
        self.sigma_j = sigma_j
        self.lamda = lamda

    def random_walk(self):
        """ generates a random walk
        Parameters
        ----------
        None

        Returns
        -------
        None 
        """

        self.t = np.linspace(0, self.T, self.N)
        W = np.random.standard_normal(size=int(self.N))
        W = np.cumsum(W)*np.sqrt(self.dt)
        X = (self.mu-0.5*self.sigma**2)*self.t + self.sigma*W

        num_jumps = np.random.poisson(self.lamda * self.T)
        jump_times = np.random.uniform(0, self.T, size=num_jumps)
        jump_times = np.sort(jump_times)
        jump_sizes = np.random.normal(self.mu_j,
                                      self.sigma_j, size=num_jumps)
        jump_sizes = np.cumsum(jump_sizes)
        Y = np.zeros(int(self.N))
        if num_jumps != 0:
            for ix, i in enumerate(self.t):
                count = 0
                if jump_times[-1] < i:
                    Y[ix] = jump_sizes[-1]
                else:
                    while jump_times[count] < i:
                        count = count + 1
                    if count != 0:
                        Y[ix] = jump_sizes[count-1]
        L = np.add(X, Y)
        self.S = self.s0*np.exp(L)


class __TTProcess(JumpDiffusion):
    """ This is a private class that is an experimental random
        walk I am working on """
    def __init__(self, S0, mu, sigma, T, mu_j, sigma_j, dt=0.00396825396):

        JumpDiffusion.__init__(self, S0, mu, sigma, T, mu_j, sigma_j, None, dt)
        self.rand_jump = []
        self.sized_jump = []
        self.num_jumps = 0

    def add_random_jump(self):
        self.rand_jump.append(np.random.normal(self.mu_j, self.sigma_j))
        self.num_jumps += 1

    def add_sized_jump(self, size_percet=0.04):
        self.sized_jump.append(size_percet * self.s0)
        self.num_jumps += 1

    def random_walk(self):
        """ generates random walk """

        self.t = np.linspace(0, self.T, self.N)
        W = np.random.standard_normal(size=int(self.N))
        W = np.cumsum(W)*np.sqrt(self.dt)
        X = (self.mu-0.5*self.sigma**2)*self.t + self.sigma*W
        jump_times = np.random.uniform(0, self.T, size=self.num_jumps)
        jump_times = np.sort(jump_times)
        num_jumps = self.num_jumps
        to_shuffle = np.append(np.array(self.sized_jump),
                               np.array(self.rand_jump))
        np.random.shuffle(to_shuffle)
        jump_sizes = to_shuffle
        jump_sizes = np.cumsum(jump_sizes)
        Y = np.zeros(int(self.N))
        if num_jumps != 0:
            for ix, i in enumerate(self.t):
                count = 0
                if jump_times[-1] < i:
                    Y[ix] = jump_sizes[-1]

                else:
                    while jump_times[count] < i:
                        count = count + 1
                    if count != 0:
                        Y[ix] = jump_sizes[count-1]
        L = np.add(X, Y)
        self.S = self.s0*np.exp(L)


class Vasick(RandomWalkBase):
    """Vasick model, useful in modelling short term interest rate"""
    def __init__(self, r, a, b, sigma, T, dt=0.00396825396):

        RandomWalkBase.__init__(self, r, b, sigma, T, dt)
        """
        Parameters
        ----------

        r : double 
            starting interest rate
        a : double
            speed of reversion
        b : double
            long term mean
        sigma: double
            Instantaneous volatility
        T : int 
            number of days simulated
        dt : double, optional
            step size

        """

        self.a = a
        self.r = self.s0
        self.b = self.mu

    def random_walk(self):
        """ generates a random walk
        Parameters
        ----------
        None

        Returns
        -------
        None 

        """
        self.t = np.linspace(0, self.T, self.N)
        W = np.random.standard_normal(size=int(self.N))
        self.rt =  np.random.standard_normal(size=int(self.N))
        print(self.rt)
        self.rt[0] = self.r
        for i in range(1,self.T):
            self.rt[i] = (self.a *(self.b - self.rt[i-1]))*self.dt + (self.sigma * math.sqrt(self.dt)* W[i])
        self.S = self.rt
        print(W)
        print(self.S)


def main():

    x = Vasick(0.03, 0.3, .1, 0.03, 1)
    x.monte_carlo_walks()

if __name__ == '__main__':
    main()
