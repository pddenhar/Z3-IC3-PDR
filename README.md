# Z3-IC3-PDR
Implementation of the IC3 / Property Directed Reachability algorithm using the the Z3 SMT solver.
Peter Den Hartog, 2016.  

# How to run tests
Running `python ./test.py` will run all PDR tests. Running `./test.py -ls` will list all available tests.

`./test.py <testname>` will run a single named test.

`./test.py -h` will display command line help.
# How to use PDR prover
```
x = Bool('x')
xp = Bool('x\'')

variables = [x]
primes = [xp]

init = x
trans = xp == Not(x)
post = Or(x, Not(x))

solver = PDR(variables, primes, init, trans, post)
solver.run()
```