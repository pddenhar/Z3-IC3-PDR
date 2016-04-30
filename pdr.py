#!/usr/bin/python

# Implementation of the PDR algorithm by Peter Den Hartog. Apr 28, 2016

from z3 import *

# a tcube is a conjunction of literals assosciated with a given frame (t) in the trace
class tCube(object):
    #make a tcube object assosciated with frame t. If t is none, have it be frameless
    def __init__(self, model, lMap, t = None):
        self.t = t
        #filter out primed variables when creating cube
        self.cubeLiterals = [lMap[str(l)] == model[l] for l in model if '\'' not in str(l)]
    # return the conjection of all literals in this cube
    def cube(self):
        return And(*self.cubeLiterals)

    def __repr__(self):
        return str(self.t) + ": " + str(sorted(self.cubeLiterals, key=str))


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
                #print "Found bad cube:", c
                # we have a bad cube, which we will try to block 
                # if the cube is blocked from the previous frame 
                # we can block it from all previous frames
                trace = self.recBlockCube(c)
                if trace != None:
                    print "Found trace ending in bad state:"
                    for f in trace:
                        print f
                    return False
            else: ## found no bad cube, add a new state on to R after checking for induction
                #print "Checking for induction"
                inv = self.checkForInduction()
                if inv != None:
                    print "Found inductive invariant:", simplify(inv)
                    return True
                print "Did not find invariant, adding frame", len(self.R)
                self.R.append(True)
    
    # Check all images in R to see if one is inductive  
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
                # If a bad cube was not blocked all the way down to R[0]
                # we have found a counterexample and may extract the stack trace
                return Q

            # solve if cube s was blocked by the image of the frame before it
            z = self.solveRelative(s)

            if (z == None):
                # Cube 's' was blocked by image of predecessor:
                # block cube in all previous frames
                Q.pop() #remove cube s from Q 
                for i in range(1, s.t+1):
                    #if not self.isBlocked(s, i):
                    self.R[i] = And(self.R[i], Not(s.cube()))
            else:
                # Cube 's' was not blocked by image of predecessor
                # it will stay on the stack, and z (the model which allowed transition to s) will we added on top
                Q.append(z)
        return None
    
    #for tcube, check if cube is blocked by R[t-1] AND trans
    def solveRelative(self, tcube):
        cubeprime = substitute(tcube.cube(), self.primeMap)
        s = Solver()
        s.add(self.R[tcube.t-1])
        s.add(self.trans)
        s.add(cubeprime)
        if(s.check() != unsat): #cube was not blocked, return new tcube containing the model
            model = s.model()
            return tCube(model, self.lMap, tcube.t-1)
        return None


    # Using the top item in the trace, find a model of a bad state
    # and return a tcube representing it
    # or none if all bad states are blocked
    def getBadCube(self):
        model = And(Not(self.post), self.R[-1])
        s = Solver()
        s.add (model)
        if(s.check() == sat):
            return tCube(s.model(), self.lMap, len(self.R) - 1)
        else:
            return None

    # Is a cube ruled out given the state R[t]?
    def isBlocked(self, tcube, t):
        s = Solver()
        s.add(And(self.R[t], tcube.cube()))
        return s.check() == unsat


    def isInitial(self, cube, initial):
        s = Solver()
        s.add (And(initial, cube))
        return s.check() == sat