#!/usr/bin/python
from z3 import *
from pdr import PDR

# SAFE
# This test is a simple program that rotates the variables of three booleans
# The post condition is that at least one of them must be true
# which is inductive because one is initialized to true and never negated, only swapped
def Swapper():
	x = Bool('x')
	y = Bool('y')
	z = Bool('z')
	xp = Bool('x\'')
	yp = Bool('y\'')
	zp = Bool('z\'')

	variables = [x,y,z]
	primes = [xp,yp,zp]

	init = And(x,Not(y), Not(z))
	trans = And(xp == y, zp == x, yp == z)
	post = Or(x, y, z)
	return (variables, primes, init, trans, post)

# UNSAFE
# Initialize a boolean bitfield to [TTTTTTTTTF]
# Each iteration, each boolean takes the AND of the two bits to its left
# (rolling over at the left back to the right)
# (Frame 1 will look like [FFTTTTTTTT])
# The post condition is simply that at least one boolean be true,
# which can take quite a while to fail depending on the width of the bitfield
#
# This one can take quite a while to run
def BooleanShifter():
	len = 9
	variables = [Bool(str(i)) for i in range(len)]
	primes = [Bool(str(i) + '\'') for i in variables]

	#initialize to something like [T T T T T T T T F]
	init = And(*[variables[i] for i in range(len-1)] + [Not(variables[-1])])
	trans = And(*[primes[i] == And(variables[i-1], variables[i-2]) for i in range(len)])
	post = Or(*variables)

	return (variables, primes, init, trans, post)

# UNSAFE
# Initialize a boolean bitfield [AAAAA BBBBB]
# Each iteration, add the value of BBBBB to AAAAA
# incrementing it
# In this example, BBBBB is 00001 and the postcondition is that
# AAAAA is not 11111, which is unsafe
def BooleanIncrementer():
	len = 10
	variables = [Bool(str(i)) for i in range(len)]
	primes = [Bool(str(i) + '\'') for i in variables]
	init = And(*[Not(variables[i]) for i in range(len-1)] + [variables[-1]])
	def carryout(pos):
		if pos==len/2:
			return False
		else:
			return Or(And(Xor(variables[pos],variables[pos+len/2]), carryout(pos+1)),And(variables[pos],variables[pos+len/2]))
	trans = And(*[primes[i] == Xor(Xor(variables[i],variables[i+len/2]),carryout(i+1)) for i in range(len/2)] \
		+ [primes[i+5] == variables[i+5] for i in range(len/2)])
	post = Not(And(*[variables[i] for i in range(len/2)]))
	return (variables, primes, init, trans, post)

# SAFE
# Using the same boolean incrementer from before
# In this example, BBBBB is 00010 and the postcondition is that
# AAAAA is even, which is safe
def EvenIncrementer():
	len = 10
	variables = [Bool(str(i)) for i in range(len)]
	primes = [Bool(str(i) + '\'') for i in variables]
	init = And(*[Not(variables[i]) for i in range(len-2)] + [variables[-2], Not(variables[-1])])
	def carryout(pos):
		if pos==len/2:
			return False
		else:
			return Or(And(Xor(variables[pos],variables[pos+len/2]), carryout(pos+1)),And(variables[pos],variables[pos+len/2]))
	trans = And(*[primes[i] == Xor(Xor(variables[i],variables[i+len/2]),carryout(i+1)) for i in range(len/2)] \
		+ [primes[i+len/2] == variables[i+len/2] for i in range(len/2)])
	post = Not(variables[len/2-1])
	return (variables, primes, init, trans, post)

tests = {'Swapper':Swapper, 'BooleanShifter':BooleanShifter, 'BooleanIncrementer':BooleanIncrementer, 'EvenIncrementer':EvenIncrementer}

def listTests():
	for name in tests:
		print name

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Run tests examples on the PDR algorithm")
	parser.add_argument('-ls', action='store_true')
	parser.add_argument('testname', type=str, help='The name of the test to run', default=None, nargs='?')
	args = parser.parse_args()
	if(args.ls):
		listTests()
	elif(args.testname!=None):
		name = args.testname
		print "=========== Running test", name,"==========="
		solver = PDR(*tests[name]())
		solver.run()
	else:
		for name in tests:
			print "=========== Running test", name,"==========="
			solver = PDR(*tests[name]())
			solver.run()