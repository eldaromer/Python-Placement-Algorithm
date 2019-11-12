from bblist import *
from schematic import schematic
from formulate import solve, autosolve

if __name__ == '__main__':

    # Another case study for the solver: an N-channel remote.
    # Build strategy is enforcing uC and LED to be together, while allowing
    # large bridges betwen battery and bat, as well as bat and uC.

    n = 7

    ws = (10, 10, 2)
    problem = schematic(ws, name = ("Remote-" + str(n)))

    lip = Lipo("LiPo")

    but = []
    uc = []
    led = []
    for chan in range(1, n+1):
        but = But("Button " + str(chan))
        led = Led("LED " + str(chan))
        uc = Micro("uC " + str(chan))
        problem.addConnection(lip, 'PWR', but, 'B1', 3)
        problem.addConnection(but, 'B2', uc, 'PWR', 3)
        problem.addConnection(uc, 'OUT2', led, 'LED')

    # Call the solver, which positions the Bitblox correctly.

    fixed = autosolve(problem)

    # Draw the assembly resulting from the solution.
    fixed.showSolution() 