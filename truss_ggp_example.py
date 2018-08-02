"""Truss generalized geometric program (GGP) example from section 6.3 of Boyd's tutorial.

GPkit does not support GGPs, so I use helper variables
(`t_1`, `t_2`) to convert the problem to a geometric program.
"""

import numpy as np
import gpkit as gp

A = gp.Variable('A', 'meter**2', 'Bar cross section area')
r = gp.Variable('r', 'meter', 'Bar inner radius')
r_min = gp.Variable('r_min', 0.01, 'meter', 'Bar inner radius minimum')
R_max = gp.Variable('R_max', 0.2, 'meter', 'Bar outer radius maximum')
sigma = gp.Variable('\\sigma', 100, 'megapascal', 'Bar stress limit')

# The outer radius - this is an evaluated free variable - A is used instead as
# a decision variable in the optimization
R = gp.Variable('R', 'meter', evalfn=lambda v: (v[A] / (2 * np.pi) + v[r]**2)**0.5)

w = gp.Variable('w', 'meter', 'Truss width')
w_min = gp.Variable('w_min', 0.5, 'meter', 'Truss width lower bound')
w_max = gp.Variable('w_max', 2, 'meter', 'Truss width upper bound')

h = gp.Variable('h', 'meter', 'Truss height')
h_min = gp.Variable('h_min', 0.5, 'meter', 'Truss height lower bound')
h_max = gp.Variable('h_max', 2, 'meter', 'Truss height upper bound')

F_1 = gp.Variable('F_1', 100, 'kilonewton', 'Vertical load')
F_2 = gp.Variable('F_2', 100, 'kilonewton', 'Horizontal load')

# helper variables to convert the GGP to GP
t_1 = gp.Variable('t_1', 'meter**2', 'Helper variable')
t_2 = gp.Variable('t_2', 'meter**2', 'Helper variable')


objective = 2 * A * t_1**0.5

constraints = [
    F_1 * t_1**0.5 / h <= sigma * A,
    F_2 * t_1**0.5 / w <= sigma * A,
    w**2 + h**2 <= t_1,
    w_min <= w,
    w <= w_max,
    h_min <= h,
    h <= h_max,
    t_2**0.5 <= R_max,
    A / (2 * np.pi) + r**2 <= t_2,
    0.21 * r**2 <= A / (2 * np.pi),
    r_min <= r,
]

m = gp.Model(objective, constraints)

m.unique_varkeys = set([R.key]) # idk what this does?

sol = m.solve()

print sol.table()
