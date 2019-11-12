from bblist import *
from schematic import schematic
from formulate import solve, autosolve

if __name__ == '__main__':

    # Another case study for the solver: button-battery-light serial circuit.

    lip = Lipo("LiPo")
    but1 = But("Button 1")
    but2 = But("Button 2")
    led1 = Led("LED 1")
    led2 = Led("LED 2")
    uc1 = Micro("uC 1")
    uc2 = Micro("uC 2")

    # A workspace is defined by a (x, y, z) tuple of available positions
    # in positional grid units.

    ws = (6, 3, 2)
    problem = schematic(ws, name = "Small Remote")

    problem.addConnection(lip, 'PWR', but1, 'B1')
    problem.addConnection(but1, 'B2', uc1, 'PWR')
    problem.addConnection(uc1, 'OUT2', led1, 'LED')
    problem.addConnection(lip, 'PWR', but2, 'B1')
    problem.addConnection(but2, 'B2', uc2, 'PWR')
    problem.addConnection(uc2, 'OUT2', led2, 'LED')

    # Call the solver, which positions the Bitblox correctly.

    solve(problem)

    # Draw the assembly resulting from the solution.
    problem.showSolution() 