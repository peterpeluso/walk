# Walk
> A library for modelling asset prices using random walks

Walk is a library built for modellling asset prices and interest rates using various stochastic processes. Walk also allows users to price options using the random walk of their choice by Monte Carlo Simulation.

## Usage Example
```Python
import walk
s0 = 100
mu = 1
sigma = .2
T = 1

radom_walk = walk.GeometricBrownianMpotion(s0, mu, sigma, T)
random_walk.monte_carlo(plot=True)
```
![Example](https://github.com/peterpeluso/walk/blob/master/img/figure_1.png)

## Development setup
Install on linux
``` 
git clone https://github.com/peterpeluso/walk
cd walk
pip install -e walk
```
## Release History
* 0.0.1
    * Work in progress
