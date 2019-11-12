from bblist import *
from schematic import schematic
from formulate import solve, autosolve
import random, sys

if __name__ == '__main__':

    # Rob's 6 - channel remote with small batteries.
    # Note that there is no reason for the independent channels to
    # be connected (in fact, they should not be), so structural
    # blocks must be added for the solution to make sense.
    # Since this can easily be done algorithmically post-SAT, we do
    # it by hand to generate figures.

    n = 6
    ws = (9, 9, 2)

    problem = schematic(ws, name = "Robmote")
    print "Making " + problem.name + " in " + str(ws)
    for chan in range(1, n+1):
        bat1 = Bat("Battery " + str(chan) + 'A')
        bat2 = Bat("Battery " + str(chan) + 'B')
        but = But("Button " + str(chan))
        led = Led("LED " + str(chan))
        uc = Micro("uC " + str(chan))
        problem.addConnection(bat1, 'PWR', bat2, 'PWR', 3)
        problem.addConnection(bat2, 'PWR', but, 'B1', 3)
        problem.addConnection(but, 'B2', uc, 'PWR')
        problem.addConnection(uc, 'OUT2', led, 'LED')

    # Call the solver, which positions the Bitblox correctly.
    try:
        fixed = autosolve(problem)
    except:
        import pdb; pdb.set_trace()

    # Draw the assembly resulting from the solution.
    print fixed.listConnections