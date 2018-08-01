"""Radio power control example from section 4.1 of Boyd's tutorial."""

import numpy as np
import gpkit as gp


# Seed rng for consistencyn
np.random.seed(3254)

# Number of transmitter/receiver pairs
n = 4

P = gp.VectorVariable(n, 'P', 'watt', 'Transmitter powers')
# sigma = gp.VectorVariable(n, '\\sigma', 0.1 * np.ones(n), 'watt', 'Noise power at recievers')
sigma = gp.VectorVariable(n, '\\sigma', 0.1 * np.random.rand(n), 'watt', 'Noise power at recievers')

# Path gain matrix
# G = 0.001 * np.ones((n, n))
G = 0.001 * np.random.rand(n, n)
for i in range(n):
    G[i, i] = 0.1

# Signal to interference and noise raio minimums
S_min = gp.VectorVariable(n, 'S_min', n*[10], 'dimensionless', 'Minimum SINR')

# Signal to interference and noise raio inverse for each reciever
S_inv = (sigma + np.dot(G - np.diag(np.diag(G)), P)) / (np.diagonal(G) * P)

# Formulate the Model
objective = np.sum(P)
constraints = [S_inv <= 1/S_min]
radio_model = gp.Model(objective, constraints)

# Solve
sol = radio_model.solve()

print sol.table()
