#!/usr/bin/python
from z3 import *

def PDR(literals, init, trans, post):
    R = list()
    R.append(init)

    while(1==1):
        c = getBadCube(R[-1], post)
        if(c != None):
            if(recBlockCube((len(R) - 1, c), R, trans) == False):
                return False
        else:
            R.append(True)
            if(propagateBlockedCubes(R) == True):
                return True

# tcube is a tuple of the form (frame depth, cube)
def recBlockCube(tcube, trace, trans):
    queue = Queue.PriorityQueue()
    queue.put(tcube)

    while(len(queue) > 0):
        s = queue.get()

        # if we have found a counterexample
        if(s[0] == 0):
            return False

        if(isBlocked(R[-1], s[1]) == False):
            assert(isInitial(s[1], R[0]) == False)
            z = solveRelative(s[1], R[s[0] - 1], trans)

            if(z != None):
                addBlockedCube(z)




    return True

def propagateBlockedCubes(state):
    return True

# PDR Sat stuff
def getBadCube(state, post):
    model = And(Not(post), state)
    s = Solver()
    s.add (model)
    if(s.check() == sat):
        return model
    else:
        return None

def isBlocked(state, cube):
    s = Solver()
    s.add (Implies(state, Not(cube)))
    return s.check() == sat


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