#!/usr/bin/python
from z3 import *


class tCube(Object):
    #make a tcube object assosciated with frame t. If t is none, have it be frameless
    def __init__(model, literals, t = None):
        self.t = t
        self.cubeLiterals = [l == model[l] for l in model]

    def cube():
        return And(*self.cubeLiterals)


class PDR(Object):
    def __init__(literals, primes, init, trans, post):
        self.literals = literals
        self.primes = primes
        self.init = init
        self.trans = trans
        self.post = post
        self.R = []

    def run():
        R = list()
        R.append(self.init)

        while(1==1):
            c = getBadCube()
            if(c != None):
                if(conflict(c) == False):
                    return False
            else: ## found no bad cube, add a new state on to R
                R.append(True)
                

    # known as recblockcube in the berkeley paper
    def conflict(tcube):
        for i in range(0, len(R)):
            phi = Not(tcube.cube())
            s = Solver()
            s.add(Implies(And(R[i], self.trans), phi))
            if(s.check() == sat):
                for j in range(0, i+1):
                    



    def propagateBlockedCubes(state):
        return True

    # Using the top item in the trace, find a model of a bad state
    # and return a tcube representing it
    def getBadCube(self):
        model = And(Not(self.post), R[-1])
        s = Solver()
        s.add (model)
        if(s.check() == sat):
            return tCube(model, len(R) - 1)
        else:
            return None

    def isBlocked(tcube):
        s = Solver()
        s.add(And(R[tcube.t], tcube.cube()))
        return s.check() == unsat


    def isInitial(cube, initial):
        s = Solver()
        s.add (And(initial, cube))
        return s.check() == sat

    # is it possible to get to 
    def solveRelative(cube, state, trans):
        return None 



x = Bool('x')
y = Bool('y')
z = Bool('z')
xp = Bool('x\'')
yp = Bool('y\'')
zp = Bool('z\'')

init = And(x,y, Not(z))
trans = And(xp == y, zp == x, yp == z)
post = Or(x,y,z)

PDR([], init, trans, post)