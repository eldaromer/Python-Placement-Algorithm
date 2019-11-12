from bblist import *
from schematic import schematic
from formulate import solve, autosolve
import random

if __name__ == '__main__':

    # Another case study for the solver: an N-pole filter.
    # For every pole, add a capacitor to the last output to ground, and
    # an inductor leading to the next output.

    # The connector mutation does not work in cases where Pycosat takes
    # too long to return (such as this) so we need to manually specify
    # the necessary connector blocks.

    n = 4

    ws = (2*n, 4, 2)
    problem = schematic(ws, name = ("Filter-" + str(n)))

    lastInd = Inductor("Inductor 1")
    lastCap = Cap("Capacitor 1")
    lastGnd = Pass("Ground")
    problem.addConnection(lastInd, "I2", lastCap, "C1")
    problem.addConnection(lastCap, "C2", lastGnd, "P")

    for chan in range(2, n+1):
        ind = Inductor("Inductor " + str(chan))
        cap = Cap("Capacitor " + str(chan))
        gnd = Pass("Ground " + str(chan))
        problem.addConnection(lastInd, "I2", ind, 'I1')
        problem.expandLast()
        problem.addConnection(ind, "I2", cap, "C1")
        problem.addConnection(cap, "C2", gnd, "P")
        problem.addConnection(gnd, "P", lastGnd, "P")
        problem.expandLast()
        lastInd = ind
        lastCap = cap
        lastGnd = gnd

    # Call the solver, which positions the Bitblox correctly.

    fixed = autosolve(problem)

    # Draw the assembly resulting from the solution.
    fixed.showSolution() 