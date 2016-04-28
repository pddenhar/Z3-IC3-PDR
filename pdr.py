#!/usr/bin/python
from z3 import *

count = 0

class tCube(object):
    #make a tcube object assosciated with frame t. If t is none, have it be frameless
    def __init__(self, model, lMap, t = None):
        self.t = t
        #filter primed variables when creating cube
        self.cubeLiterals = [lMap[str(l)] == model[l] for l in model if '\'' not in str(l)]

    def cube(self):
        return And(*self.cubeLiterals)

    def __repr__(self):
        return str(self.t) + ": " + str(self.cubeLiterals)


class PDR(object):
    def __init__(self, literals, primes, init, trans, post):
        self.init = init
        self.trans = trans
        self.literals = literals
        self.lMap = {str(l):l for l in self.literals}
        self.post = post
        self.R = []
        self.primeMap = zip(literals, primes)

    def run(self):
        self.R = list()
        self.R.append(self.init)

        while(1==1):
            c = self.getBadCube()
            if(c != None):
                print "Found bad cube:", c
                # we have a bad cube, which we will try to block 
                # if the cube is blocked from the previous frame 
                # we can block it from all previous frames
                trace = self.recBlockCube(c)
                if trace != None:
                    for f in trace:
                        print f
                    return False
            else: ## found no bad cube, add a new state on to R after checking for induction
                print "Checking for induction"
                inv = self.checkForInduction()
                if inv != None:
                    print "Found invariant", inv
                    return True
                print "Did not find invariant, adding frame", len(self.R)
                self.R.append(True)
                  
    def checkForInduction(self):
        for frame in self.R:
            s=Solver()
            s.add(self.trans)
            s.add(frame)
            s.add(Not(substitute(frame, self.primeMap)))
            if s.check() == unsat:
                return frame
        return None

    #loosely based on the recBlockCube method from the berkely paper, without some of the optimizations
    def recBlockCube(self, s0):
        Q = []
        Q.append(s0);
        while (len(Q) > 0):
            s = Q[-1]
            if (s.t == 0):
                # Found counterexample, may extract it here
                return Q

            z = self.solveRelative(s)

            if (z == None):
                # Cube 's' was blocked by image of predecessor:
                # block cube in all previous frames
                Q.pop() #remove cube s from Q 
                for i in range(1, s.t+1):
                    self.R[i] = And(self.R[i], Not(s.cube()))
            else:
                # Cube 's' was not blocked by image of predecessor
                # it will stay on the stack, and z will we added on top
                Q.append(z)
        return None
    
    def solveRelative(self, tcube):
        global count
        count += 1
        cubeprime = substitute(tcube.cube(), self.primeMap)
        s = Solver()
        s.add(self.R[tcube.t-1])
        s.add(self.trans)
        s.add(cubeprime)
        if(s.check() != unsat):
            model = s.model()
            return tCube(model, self.lMap, tcube.t-1)
        return None


    # Using the top item in the trace, find a model of a bad state
    # and return a tcube representing it
    def getBadCube(self):
        model = And(Not(self.post), self.R[-1])
        s = Solver()
        s.add (model)
        if(s.check() == sat):
            return tCube(s.model(), self.lMap, len(self.R) - 1)
        else:
            return None

    # Is a cube ruled out given the current state R[N]?
    def isBlocked(self, tcube):
        s = Solver()
        s.add(And(R[tcube.t], tcube.cube()))
        return s.check() == unsat


    def isInitial(self, cube, initial):
        s = Solver()
        s.add (And(initial, cube))
        return s.check() == sat



# x = Bool('x')
# y = Bool('y')
# z = Bool('z')
# xp = Bool('x\'')
# yp = Bool('y\'')
# zp = Bool('z\'')

# variables = [x,y,z]
# primes = [xp,yp,zp]

# init = And(x,y, Not(z))
# trans = And(xp == y, zp == x, yp == z)
# post = Or(x, y, z)

# solver = PDR([x,y,z], init, trans, post)
# solver.run()


# LEN = 9
# variables = [Bool(str(i)) for i in range(LEN)]
# primes = [Bool(str(i) + '\'') for i in variables]
# on_bits = [0,1,2,5,6,7,8]
# init = And(*([variables[i] for i in on_bits] + [Not(variable) for i, variable in enumerate(variables) if not i in on_bits]))
# trans = Or([And(*[
#    (primes+primes)[j] == Not((variables+variables)[j]) if abs(j-i) <= 1 else
#    (primes+primes)[j] == (variables+variables)[j] for j in range(LEN)]) for i in range(LEN)])
# post = Or(*[var for var in variables])

# solver = PDR(variables, init, trans, post)
# solver.run()

# variables = [BitVec('x', 3), BitVec('y', 3)]
# x, y = variables
# primes = [BitVec('x\'', 3), BitVec('y\'', 3)]
# xp, yp = primes
# init = And(x == 4, y == 3)
# trans = And(xp == x + y, yp == x - y)
# post = Not(x == 2)

# solver = PDR(variables, init, trans, post)
# solver.run()

variables = [BitVec('x', 6), BitVec('y', 6)]
x, y = variables
primes = [BitVec('x\'', 6), BitVec('y\'', 6)]
xp, yp = primes
init = And(x == 4, y == 3)
trans = And(xp == x + y, yp == x - y)
post = Not(x == 32)

solver = PDR(variables, primes, init, trans, post)
solver.run()

print count