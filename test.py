#!/usr/bin/python
from z3 import *
from pdr import PDR


x = Bool('x')
y = Bool('y')
z = Bool('z')
xp = Bool('x\'')
yp = Bool('y\'')
zp = Bool('z\'')

variables = [x,y,z]
primes = [xp,yp,zp]

init = And(x,y, Not(z))
trans = And(xp == y, zp == x, yp == z)
post = Or(x, y, z)

solver = PDR(variables, primes, init, trans, post)
solver.run()