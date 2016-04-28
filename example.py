#!/usr/bin/python
from z3 import *


p = Bool('p')
q = Bool('q')
r = Bool('r')

s = Solver()
s.add(And(Or(p,q), Implies(q,r)))
print s.check()
m = s.model()

print m
print m[0] == p
print p
for var in m:
    print var

# # negate the model
# phi = True
# s.add(p != m[p])
# s.add(q != m[q])
# s.add(r != m[r])
# print s.check()
# m = s.model()
# print m

# s.add(p != m[p])
# s.add(q != m[q])
# s.add(r != m[r])

# print s.check()


# def isValid(phi):
#     s = Solver()
#     s.add (Not(phi))
#     return s.check() == unsat

# def abstract(phi, preds):
#     res = And(True)

#     for p in preds:
#         if isValid(Implies(phi,p)):
#             res = And(res,p)
#         if isValid(Implies(phi, Not(p))):
#             res = And(res, Not(p))

#     return simplify(res)


# x = Int('x')
# y = Int('y')
# xp = Int('x\'')
# yp = Int('y\'')

# varMap = [(x,xp), (y,yp)]
# varMapRev = map(lambda v: (v[1], v[0]), varMap)

# def inductive(inv,trans):
#     invprime = substitute(inv,varMap)
#     return isValid(Implies(And(inv,trans), invprime))

# init = And(x == 0, y == 0)
# trans = And(xp == x + 1, yp == y + 1)
# post = Implies (y == 10, x == 10)

# # preds = [x > 0]
# # preds = [x >= 0]
# # preds = [x >= y, x <= y]
# preds = [x == 0, y == 0, y == 1, x == 1, x == 2, y == 2]
# predsprime = map(lambda p: substitute(p,*varMap), preds)


# inv = abstract(init, preds)

# i = 0
# while not inductive(inv,trans):
#     print "\nInv at ", i, ": ", inv
#     i = i + 1

#     # existential quantifer??
#     onestep = abstract(And(inv, trans), predsprime)
#     onestep = substitute(onestep, varMapRev)
#     inv = Or(inv, onestep)


# print "\n\nFinal inv --> ", simplify(inv)

# if isValid(Implies(inv,post)):
#     print "SAFE"
# else:
#     print "UNSAFE"